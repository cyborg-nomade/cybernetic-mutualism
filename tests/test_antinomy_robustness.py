"""Protect model equivalence, structural interventions, and prospective decisions."""

from dataclasses import replace
from pathlib import Path

import pytest

from models.antinomy.model import (
    ClassificationThresholds,
    ModelParameters,
    SystemState,
    classify_trajectory,
    simulate_trajectory,
)
from models.antinomy.sweep import REGIME_ORDER, ParameterGrid
from models.antinomy_robustness.analysis import (
    decide,
    intersection_over_union,
    original_baseline_matches,
    surviving_regimes,
    transition_edges,
)
from models.antinomy_robustness.experiment import (
    Cell,
    ExperimentSettings,
    Scenario,
    ScenarioResult,
    parameters_for,
    run_scenario,
    scenarios,
)
from models.antinomy_robustness.generate import generate, write_csv
from models.antinomy_robustness.model import (
    RESPONSES,
    DirectionParameters,
    VariantParameters,
    advance_round,
    bounded_response,
    classify_states,
    simulate_states,
)


@pytest.mark.parametrize(
    "support,inhibition", [(-4, 4), (0, 2), (0, 6), (2, 12), (1, 8)]
)
@pytest.mark.parametrize("seed", [7, 19, 211])
def test_baseline_trajectory_and_classifier_are_exact(support, inhibition, seed):
    """Preserve every state and metric, not only a modal regime count."""
    original = simulate_trajectory(
        ModelParameters(support, inhibition), random_seed=seed
    )
    states = simulate_states(
        parameters_for(scenarios()[0], support, inhibition), seed=seed
    )
    assert states == original.states
    assert classify_states(states) == classify_trajectory(original)


@pytest.mark.parametrize("response", RESPONSES)
def test_responses_share_midpoint_slope_and_bounds(response):
    """Perturb response shape without changing zero-input gain or ordering."""
    midpoint = 0.5
    assert bounded_response(0, response) == midpoint
    epsilon = 1e-5
    derivative = (
        bounded_response(epsilon, response) - bounded_response(-epsilon, response)
    ) / (2 * epsilon)
    assert derivative == pytest.approx(0.25)
    values = [
        bounded_response(value, response) for value in (-100, -4, -1, 0, 1, 4, 100)
    ]
    assert values == sorted(values)
    assert all(0 <= value <= 1 for value in values)
    assert bounded_response(4, "logistic") != bounded_response(4, "arctangent")


@pytest.mark.parametrize("scenario", scenarios())
def test_round_matches_explicit_hand_calculation(scenario):
    """The second sequential update sees the first update but its own old state."""
    parameters = parameters_for(scenario, 0.25, 6)
    autonomy, coordination = 0.2, 0.7
    expected_autonomy = bounded_response(
        0.25 + 2 * autonomy - 4 * (1 + scenario.asymmetry) * coordination,
        scenario.response,
    )
    expected_coordination = bounded_response(
        0.25 + 2 * coordination - 4 * (1 - scenario.asymmetry) * autonomy,
        scenario.response,
    )
    if scenario.schedule == "autonomy-first":
        expected_coordination = bounded_response(
            0.25 + 2 * coordination - 4 * (1 - scenario.asymmetry) * expected_autonomy,
            scenario.response,
        )
    if scenario.schedule == "coordination-first":
        expected_autonomy = bounded_response(
            0.25 + 2 * autonomy - 4 * (1 + scenario.asymmetry) * expected_coordination,
            scenario.response,
        )
    result = advance_round(SystemState(autonomy, coordination), parameters)
    assert result.autonomy_capacity == pytest.approx(expected_autonomy)
    assert result.coordination_capacity == pytest.approx(expected_coordination)


@pytest.mark.parametrize("scenario", scenarios())
def test_exchanging_variables_and_schedule_preserves_trajectory(scenario):
    """Opposite asymmetry and order are the same map after variable relabeling."""
    orders = {
        "synchronous": "synchronous",
        "autonomy-first": "coordination-first",
        "coordination-first": "autonomy-first",
    }
    swapped = Scenario(
        scenario.response, orders[scenario.schedule], -scenario.asymmetry
    )
    original = simulate_states(
        parameters_for(scenario, 1, 9), initial_state=SystemState(0.2, 0.7)
    )
    exchanged = simulate_states(
        parameters_for(swapped, 1, 9), initial_state=SystemState(0.7, 0.2)
    )
    assert original == tuple(
        SystemState(state.coordination_capacity, state.autonomy_capacity)
        for state in exchanged
    )
    assert all(
        0 <= state.autonomy_capacity <= 1 and 0 <= state.coordination_capacity <= 1
        for state in original
    )


@pytest.mark.parametrize("scenario", scenarios())
def test_uncoupled_directions_cancel_and_ignore_order(scenario):
    """No residual asymmetry survives the zero-net-coupling intervention."""
    parameters = parameters_for(scenario, 0, 14, uncoupled=True)
    assert parameters.autonomy.enablement == parameters.autonomy.inhibition
    assert parameters.coordination.enablement == parameters.coordination.inhibition
    synchronous = replace(parameters, schedule="synchronous")
    assert simulate_states(parameters) == simulate_states(synchronous)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -1])
def test_invalid_mechanism_strengths_fail(value):
    """Reject nonfinite or negative directional mechanisms."""
    with pytest.raises(ValueError):
        DirectionParameters(0, inhibition=value)


@pytest.mark.parametrize(
    "state",
    [SystemState(-0.1, 0.5), SystemState(0.5, 1.1), SystemState(float("nan"), 0.5)],
)
def test_invalid_initial_states_fail(state):
    """Do not silently simulate invalid or nonfinite capacities."""
    with pytest.raises(ValueError):
        simulate_states(parameters_for(scenarios()[0], 0, 2), initial_state=state)


@pytest.mark.parametrize("steps", [True, 3, 5.5])
def test_invalid_horizons_fail(steps):
    """Require an integer horizon long enough to classify."""
    with pytest.raises(ValueError):
        simulate_states(parameters_for(scenarios()[0], 0, 2), steps=steps)


def test_unknown_models_and_short_tails_fail():
    """Reject unsupported map names and incomplete classifier windows."""
    direction = DirectionParameters(0)
    with pytest.raises(ValueError):
        VariantParameters(direction, direction, response="unknown")
    with pytest.raises(ValueError):
        VariantParameters(direction, direction, schedule="unknown")
    with pytest.raises(ValueError):
        bounded_response(0, "unknown")
    with pytest.raises(ValueError):
        classify_states((SystemState(0.5, 0.5),))


@pytest.mark.parametrize(
    "grid",
    [
        ParameterGrid((), (0,)),
        ParameterGrid((1, 0), (0,)),
        ParameterGrid((0, 0), (0,)),
        ParameterGrid((0,), (-1,)),
        ParameterGrid((float("inf"),), (0,)),
    ],
)
def test_invalid_experiment_grids_fail(grid):
    """The boundary analysis needs finite, unique, increasing coordinates."""
    with pytest.raises(ValueError):
        ExperimentSettings(grid=grid)


def test_factorial_and_seed_validation():
    """Preserve all 18 conditions with baseline first and explicit unique seeds."""
    expected_scenarios = 18
    assert len(scenarios()) == expected_scenarios
    assert len(set(scenarios())) == expected_scenarios
    assert scenarios()[0].name == "logistic_synchronous_symmetric"
    for seeds in ((), (7, 7)):
        with pytest.raises(ValueError):
            ExperimentSettings(seeds=seeds)
    with pytest.raises(ValueError):
        ExperimentSettings(steps=10)


def test_survival_and_tie_breaks_are_prespecified():
    """Five cells and four agreeing seeds are required, with baseline tie order."""
    stable = Cell(0, 0, ("lock-in",) * 4 + ("equilibrium",) * 3)
    minority = Cell(0, 0, ("lock-in",) * 3 + ("equilibrium",) * 2 + ("collapse",) * 2)
    assert surviving_regimes((stable,) * 5)["lock-in"]
    assert not surviving_regimes((stable,) * 4)["lock-in"]
    assert not surviving_regimes((minority,) * 5)["lock-in"]
    assert Cell(0, 0, ("equilibrium", "collapse")).modal == "collapse"


@pytest.mark.parametrize(
    "baseline_verified,controls_clean,variant,expected",
    [
        (False, True, "all", "withhold"),
        (True, True, "all", "retain"),
        (True, False, "all", "narrow"),
        (True, True, "no-oscillation", "narrow"),
        (True, True, "no-lock-in", "reject-extension"),
    ],
)
def test_scientific_decision_precedence(
    baseline_verified, controls_clean, variant, expected
):
    """Negative structural results must not be mistaken for software failures."""
    baseline = dict.fromkeys(REGIME_ORDER[:-1], True)
    modified = dict(baseline)
    if variant != "all":
        modified[variant.removeprefix("no-")] = False
    assert (
        decide(
            [baseline, modified],
            baseline_verified=baseline_verified,
            controls_clean=controls_clean,
        )
        == expected
    )
    assert decide([], baseline_verified=True, controls_clean=True) == "withhold"


def test_transition_edges_and_empty_overlap():
    """Export edge coordinates on both axes and distinguish absent sets from zero."""
    cells = (
        Cell(0, 0, ("collapse",)),
        Cell(0, 1, ("collapse",)),
        Cell(1, 0, ("equilibrium",)),
        Cell(1, 1, ("lock-in",)),
    )
    edges = transition_edges(cells, ParameterGrid((0, 1), (0, 1)))
    assert edges == {
        ("support", 0, 0, 1, 0),
        ("support", 0, 1, 1, 1),
        ("inhibition", 1, 0, 1, 1),
    }
    assert intersection_over_union(set(), set()) is None
    assert intersection_over_union({1}, {2}) == 0


def test_archived_baseline_comparison_detects_changes(tmp_path):
    """Verify seed counts as well as modal labels and grid length."""
    path = tmp_path / "original.csv"
    record = {
        "support": 0,
        "opposition": 2,
        "modal_regime": "equilibrium",
        **{
            f"n_{regime.replace('-', '_')}": int(regime == "equilibrium")
            for regime in REGIME_ORDER
        },
    }
    write_csv(path, [record])
    cell = Cell(0, 2, ("equilibrium",))
    result = ScenarioResult(scenarios()[0], (cell,), ())
    assert original_baseline_matches(result, path)
    assert not original_baseline_matches(replace(result, cells=()), path)
    assert not original_baseline_matches(
        replace(result, cells=(replace(cell, labels=("lock-in",)),)), path
    )
    assert not original_baseline_matches(replace(result, scenario=scenarios()[1]), path)


def test_small_generation_is_complete_and_byte_reproducible(tmp_path):
    """Compare serial and parallel outputs, including witness diagnostics."""
    settings = ExperimentSettings(
        grid=ParameterGrid((-4.0, 0.0), (2.0, 6.0)), seeds=(7,), steps=100
    )
    first, second = tmp_path / "first", tmp_path / "second"
    summary = generate(first, settings)
    assert summary["decision"] == "withhold"
    assert not summary["full_protocol"]
    generate(second, settings, workers=2)
    expected_artifacts = 6
    assert len(list(first.iterdir())) == expected_artifacts
    assert {path.name: path.read_bytes() for path in first.iterdir()} == {
        path.name: path.read_bytes() for path in second.iterdir()
    }
    result = run_scenario((scenarios()[0], settings))
    assert len(result.cells) == len(settings.grid.shared_support_values) * len(
        settings.grid.cross_inhibition_values
    )
    assert len(result.controls) == len(settings.grid.shared_support_values)
    with pytest.raises(ValueError):
        generate(first, settings, workers=0)
    with pytest.raises(ValueError):
        write_csv(Path(first / "empty.csv"), [])


def test_generation_without_boundaries_still_writes_header(tmp_path):
    """Single-cell smoke runs have an explicit empty boundary table."""
    settings = ExperimentSettings(
        grid=ParameterGrid((0.0,), (2.0,)),
        seeds=(7,),
        steps=100,
        thresholds=ClassificationThresholds(),
    )
    generate(tmp_path, settings)
    assert len((tmp_path / "transition_edges.csv").read_text().splitlines()) == 1
