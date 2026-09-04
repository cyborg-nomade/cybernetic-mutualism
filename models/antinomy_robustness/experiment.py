"""Execute the frozen factorial design while retaining negative outcomes."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field, replace
from itertools import product

from models.antinomy.model import ClassificationThresholds, Regime, SystemState
from models.antinomy.sweep import (
    DEFAULT_RANDOM_SEEDS,
    REPRESENTATIVE_PARAMETERS,
    ParameterGrid,
    RegimeCounts,
    create_default_parameter_grid,
)

from .model import (
    MINIMUM_TAIL,
    RESPONSES,
    SCHEDULES,
    DirectionParameters,
    Response,
    Schedule,
    VariantParameters,
    classify_states,
    simulate_states,
)

ASYMMETRIES = (0.0, -0.1, 0.1)
BASELINE_NAME = "logistic_synchronous_symmetric"


@dataclass(frozen=True)
class Scenario:
    """Identify one prespecified combination of structural assumptions."""

    response: Response
    schedule: Schedule
    asymmetry: float

    @property
    def name(self) -> str:
        """Return a stable identifier suitable for data and figure labels."""
        suffix = {0.0: "symmetric", -0.1: "minus10", 0.1: "plus10"}[self.asymmetry]
        return f"{self.response}_{self.schedule}_{suffix}"


@dataclass(frozen=True)
class ExperimentSettings:
    """Store the original grid, seeds, horizon, and unchanged classifier."""

    grid: ParameterGrid = field(default_factory=create_default_parameter_grid)
    seeds: tuple[int, ...] = DEFAULT_RANDOM_SEEDS
    steps: int = 600
    thresholds: ClassificationThresholds = field(
        default_factory=ClassificationThresholds
    )

    def __post_init__(self) -> None:
        """Reject empty, repeated, unordered, or nonfinite experiment coordinates."""
        for axis in (
            self.grid.shared_support_values,
            self.grid.cross_inhibition_values,
        ):
            if not axis or tuple(sorted(set(axis))) != axis:
                raise ValueError("grid axes must be nonempty, unique, and increasing")
            if not all(math.isfinite(value) for value in axis):
                raise ValueError("grid axes must be finite")
        if min(self.grid.cross_inhibition_values) < 0:
            raise ValueError("inhibition axis cannot be negative")
        if not self.seeds or len(set(self.seeds)) != len(self.seeds):
            raise ValueError("seeds must be nonempty and unique")
        if not MINIMUM_TAIL <= self.thresholds.tail_length <= self.steps:
            raise ValueError("tail must contain at least four states and fit horizon")


@dataclass(frozen=True)
class Cell:
    """Retain seed-level labels so modal summaries cannot hide disagreement."""

    support: float
    inhibition: float
    labels: tuple[Regime, ...]

    @property
    def counts(self) -> RegimeCounts:
        """Count each observed label using the baseline tie-break implementation."""
        counts = RegimeCounts()
        for label in self.labels:
            counts.record(label)
        return counts

    @property
    def modal(self) -> Regime:
        """Select the modal regime with the original stable tie-break order."""
        return self.counts.modal_regime()

    @property
    def agreement(self) -> int:
        """Count seeds assigned to the selected modal label."""
        return self.labels.count(self.modal)


@dataclass(frozen=True)
class ScenarioResult:
    """Bundle a complete scenario grid with its distinct support-only controls."""

    scenario: Scenario
    cells: tuple[Cell, ...]
    controls: tuple[Cell, ...]


def scenarios() -> tuple[Scenario, ...]:
    """Return the 18 factorial conditions in stable baseline-first order."""
    return tuple(
        Scenario(*values) for values in product(RESPONSES, SCHEDULES, ASYMMETRIES)
    )


def parameters_for(
    scenario: Scenario,
    support: float,
    inhibition: float,
    *,
    uncoupled: bool = False,
) -> VariantParameters:
    """Scale incoming mechanisms oppositely while keeping support/persistence fixed."""
    directions = []
    for multiplier in (1 + scenario.asymmetry, 1 - scenario.asymmetry):
        enablement = 2.0 * multiplier
        incoming_inhibition = enablement if uncoupled else inhibition * multiplier
        directions.append(
            DirectionParameters(support, 2.0, enablement, incoming_inhibition)
        )
    return VariantParameters(
        directions[0], directions[1], scenario.response, scenario.schedule
    )


def evaluate_cell(
    scenario: Scenario,
    support: float,
    inhibition: float,
    settings: ExperimentSettings,
    *,
    uncoupled: bool = False,
) -> Cell:
    """Classify every seeded trajectory at one coordinate without outcome selection."""
    parameters = parameters_for(scenario, support, inhibition, uncoupled=uncoupled)
    labels = tuple(
        classify_states(
            simulate_states(parameters, steps=settings.steps, seed=seed),
            settings.thresholds,
        ).regime
        for seed in settings.seeds
    )
    return Cell(support, inhibition, labels)


def run_scenario(task: tuple[Scenario, ExperimentSettings]) -> ScenarioResult:
    """Run one full grid and all unique uncoupled support controls."""
    scenario, settings = task
    cells = tuple(
        evaluate_cell(scenario, support, inhibition, settings)
        for support, inhibition in product(
            settings.grid.shared_support_values,
            settings.grid.cross_inhibition_values,
        )
    )
    controls = tuple(
        evaluate_cell(scenario, support, 2.0, settings, uncoupled=True)
        for support in settings.grid.shared_support_values
    )
    return ScenarioResult(scenario, cells, controls)


def witness_rows(
    scenario: Scenario, settings: ExperimentSettings
) -> list[dict[str, object]]:
    """Check original reference points at two horizons and nine threshold pairs."""
    rows: list[dict[str, object]] = []
    for expected, reference in REPRESENTATIVE_PARAMETERS.items():
        parameters = parameters_for(
            scenario, reference.shared_support, reference.cross_inhibition
        )
        for seed in settings.seeds:
            states = simulate_states(parameters, steps=settings.steps * 2, seed=seed)
            for horizon in (settings.steps, settings.steps * 2):
                rows.extend(
                    classify_witness_tail(
                        states[: horizon + 1],
                        settings,
                        {
                            "scenario": scenario.name,
                            "reference": expected,
                            "seed": seed,
                            "steps": horizon,
                            "support": reference.shared_support,
                            "inhibition": reference.cross_inhibition,
                        },
                    )
                )
    return rows


def classify_witness_tail(
    states: tuple[SystemState, ...],
    settings: ExperimentSettings,
    metadata: dict[str, object],
) -> list[dict[str, object]]:
    """Reclassify a reference tail without rerunning or tuning the dynamics."""
    rows: list[dict[str, object]] = []
    for collapse, gap in product((0.075, 0.1, 0.125), (0.20, 0.25, 0.30)):
        thresholds = replace(
            settings.thresholds, collapse_capacity=collapse, lock_in_gap=gap
        )
        result = classify_states(states, thresholds)
        rows.append(
            metadata
            | {
                "collapse_threshold": collapse,
                "lock_in_gap": gap,
                "observed": result.regime,
            }
            | {name: f"{value:.10f}" for name, value in asdict(result.metrics).items()}
        )
    return rows
