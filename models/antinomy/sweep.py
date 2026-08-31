"""Run parameter sweeps and robustness checks for the antinomy model."""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace

from .model import (
    ClassificationThresholds,
    ModelParameters,
    Regime,
    SimulationTrajectory,
    classify_trajectory,
    simulate_trajectory,
)

REGIME_ORDER: tuple[Regime, ...] = (
    "collapse",
    "equilibrium",
    "lock-in",
    "oscillation",
    "unresolved",
)
DEFAULT_RANDOM_SEEDS = (7, 19, 41, 73, 101, 151, 211)
FIXED_POINT_BISECTION_ITERATIONS = 80
ROBUSTNESS_HORIZONS = (300, 600, 1200)
COLLAPSE_CAPACITY_CHECKS = (0.075, 0.1, 0.125)
ABLATION_SUPPORT_VALUES = (-4.0, -2.0, 0.0, 2.0)
REPRESENTATIVE_PARAMETERS: dict[Regime, ModelParameters] = {
    "collapse": ModelParameters(shared_support=-4.0, cross_inhibition=4.0),
    "equilibrium": ModelParameters(shared_support=0.0, cross_inhibition=2.0),
    "lock-in": ModelParameters(shared_support=0.0, cross_inhibition=6.0),
    "oscillation": ModelParameters(shared_support=2.0, cross_inhibition=12.0),
}
MINIMUM_AXIS_VALUES = 2


@dataclass(frozen=True)
class ParameterGrid:
    """Define all shared-support and cross-inhibition values in a sweep."""

    shared_support_values: tuple[float, ...]
    cross_inhibition_values: tuple[float, ...]


@dataclass(frozen=True)
class SweepSettings:
    """Collect every choice needed to reproduce the published sweep."""

    parameter_grid: ParameterGrid
    random_seeds: tuple[int, ...] = DEFAULT_RANDOM_SEEDS
    number_of_steps: int = 600
    classification_thresholds: ClassificationThresholds = field(
        default_factory=ClassificationThresholds
    )
    self_reinforcement: float = 2.0
    cross_enablement: float = 2.0
    shock_standard_deviation: float = 0.0


@dataclass
class RegimeCounts:
    """Count seeded trajectories assigned to each declared regime."""

    collapse: int = 0
    equilibrium: int = 0
    lock_in: int = 0
    oscillation: int = 0
    unresolved: int = 0

    def record(self, regime: Regime) -> None:
        """Increment the counter corresponding to one classification."""
        if regime == "collapse":
            self.collapse += 1
        elif regime == "equilibrium":
            self.equilibrium += 1
        elif regime == "lock-in":
            self.lock_in += 1
        elif regime == "oscillation":
            self.oscillation += 1
        else:
            self.unresolved += 1

    def as_mapping(self) -> dict[Regime, int]:
        """Return counts keyed by their external regime labels."""
        return {
            "collapse": self.collapse,
            "equilibrium": self.equilibrium,
            "lock-in": self.lock_in,
            "oscillation": self.oscillation,
            "unresolved": self.unresolved,
        }

    def modal_regime(self) -> Regime:
        """Return the most frequent regime using a stable tie-break order."""
        counts = self.as_mapping()
        modal_regime = REGIME_ORDER[0]
        for candidate_regime in REGIME_ORDER[1:]:
            if counts[candidate_regime] > counts[modal_regime]:
                modal_regime = candidate_regime
        return modal_regime

    def number_of_observed_regimes(self) -> int:
        """Return how many regimes have at least one seeded trajectory."""
        return sum(count > 0 for count in self.as_mapping().values())


@dataclass(frozen=True)
class FixedPointStability:
    """Record local stability measurements for the symmetric fixed point."""

    symmetric_fixed_point: float
    symmetric_eigenvalue: float
    antisymmetric_eigenvalue: float
    is_stable: bool


@dataclass
class ParameterCellResult:
    """Store classifications and stability results for one parameter cell."""

    shared_support: float
    cross_inhibition: float
    regime_counts: RegimeCounts
    modal_regime: Regime
    seeds_disagree: bool
    fixed_point_stability: FixedPointStability
    borders_regime_transition: bool = False
    borders_stability_change: bool = False

    @property
    def coordinates(self) -> tuple[float, float]:
        """Return the cell coordinates used by neighbor lookups."""
        return self.shared_support, self.cross_inhibition


@dataclass(frozen=True)
class RobustnessCheck:
    """Record one expected and observed result from a robustness exercise."""

    check_name: str
    expected_regime: str
    observed_regime: Regime
    shared_support: float
    cross_inhibition: float
    number_of_steps: int
    random_seed: int
    collapse_capacity: float

    @property
    def passed(self) -> bool:
        """Return whether the observation satisfies the declared expectation."""
        if self.expected_regime == "collapse_or_equilibrium":
            return self.observed_regime in {"collapse", "equilibrium"}
        return self.observed_regime == self.expected_regime


def generate_parameter_values(
    minimum: float,
    maximum: float,
    increment: float,
) -> tuple[float, ...]:
    """Generate inclusive, rounded values for one regularly spaced axis."""
    number_of_increments = round((maximum - minimum) / increment)
    return tuple(
        round(minimum + index * increment, 10)
        for index in range(number_of_increments + 1)
    )


def create_default_parameter_grid() -> ParameterGrid:
    """Create the parameter grid used for the committed visual map."""
    return ParameterGrid(
        shared_support_values=generate_parameter_values(-6.0, 4.0, 0.25),
        cross_inhibition_values=generate_parameter_values(0.0, 14.0, 0.25),
    )


def create_default_sweep_settings() -> SweepSettings:
    """Create every setting used for the committed parameter sweep."""
    return SweepSettings(parameter_grid=create_default_parameter_grid())


def create_model_parameters(
    shared_support: float,
    cross_inhibition: float,
    settings: SweepSettings,
) -> ModelParameters:
    """Combine swept coordinates with the parameters held fixed."""
    return ModelParameters(
        shared_support=shared_support,
        cross_inhibition=cross_inhibition,
        self_reinforcement=settings.self_reinforcement,
        cross_enablement=settings.cross_enablement,
        shock_standard_deviation=settings.shock_standard_deviation,
    )


def symmetric_fixed_point_residual(
    capacity: float,
    parameters: ModelParameters,
) -> float:
    """Return next capacity minus current capacity under a symmetric state."""
    symmetric_coefficient = parameters.self_reinforcement + parameters.net_cross_effect
    response_input = parameters.shared_support + symmetric_coefficient * capacity
    numerically_safe_input = max(-60.0, min(60.0, response_input))
    next_capacity = 1.0 / (1.0 + math.exp(-numerically_safe_input))
    return next_capacity - capacity


def find_symmetric_fixed_point(parameters: ModelParameters) -> float:
    """Locate a symmetric fixed point that is unique on the published domain."""
    lower_capacity = 0.0
    upper_capacity = 1.0
    for _iteration in range(FIXED_POINT_BISECTION_ITERATIONS):
        midpoint = (lower_capacity + upper_capacity) / 2.0
        residual = symmetric_fixed_point_residual(midpoint, parameters)
        if residual > 0.0:
            lower_capacity = midpoint
        else:
            upper_capacity = midpoint
    return (lower_capacity + upper_capacity) / 2.0


def analyze_fixed_point_stability(
    parameters: ModelParameters,
) -> FixedPointStability:
    """Calculate both Jacobian eigenvalues at the symmetric fixed point."""
    fixed_point = find_symmetric_fixed_point(parameters)
    sigmoid_derivative = fixed_point * (1.0 - fixed_point)
    symmetric_coefficient = parameters.self_reinforcement + parameters.net_cross_effect
    antisymmetric_coefficient = (
        parameters.self_reinforcement - parameters.net_cross_effect
    )
    symmetric_eigenvalue = sigmoid_derivative * symmetric_coefficient
    antisymmetric_eigenvalue = sigmoid_derivative * antisymmetric_coefficient
    is_stable = abs(symmetric_eigenvalue) < 1.0 and abs(antisymmetric_eigenvalue) < 1.0
    return FixedPointStability(
        symmetric_fixed_point=fixed_point,
        symmetric_eigenvalue=symmetric_eigenvalue,
        antisymmetric_eigenvalue=antisymmetric_eigenvalue,
        is_stable=is_stable,
    )


def classify_seeded_trajectories(
    parameters: ModelParameters,
    settings: SweepSettings,
) -> RegimeCounts:
    """Simulate and count one trajectory for every configured seed."""
    regime_counts = RegimeCounts()
    for random_seed in settings.random_seeds:
        trajectory = simulate_trajectory(
            parameters,
            number_of_steps=settings.number_of_steps,
            random_seed=random_seed,
        )
        classification = classify_trajectory(
            trajectory,
            thresholds=settings.classification_thresholds,
        )
        regime_counts.record(classification.regime)
    return regime_counts


def evaluate_parameter_cell(
    shared_support: float,
    cross_inhibition: float,
    settings: SweepSettings,
) -> ParameterCellResult:
    """Evaluate trajectories and fixed-point stability for one grid cell."""
    parameters = create_model_parameters(
        shared_support,
        cross_inhibition,
        settings,
    )
    regime_counts = classify_seeded_trajectories(parameters, settings)
    return ParameterCellResult(
        shared_support=shared_support,
        cross_inhibition=cross_inhibition,
        regime_counts=regime_counts,
        modal_regime=regime_counts.modal_regime(),
        seeds_disagree=regime_counts.number_of_observed_regimes() > 1,
        fixed_point_stability=analyze_fixed_point_stability(parameters),
    )


def calculate_grid_increment(values: tuple[float, ...]) -> float:
    """Return the increment of an axis containing at least two values."""
    if len(values) < MINIMUM_AXIS_VALUES:
        message = "a parameter-grid axis must contain at least two values"
        raise ValueError(message)
    return values[1] - values[0]


def neighboring_coordinates(
    cell: ParameterCellResult,
    shared_support_increment: float,
    cross_inhibition_increment: float,
) -> tuple[tuple[float, float], ...]:
    """Return the four orthogonal grid coordinates around one cell."""
    shared_support = cell.shared_support
    cross_inhibition = cell.cross_inhibition
    return (
        (round(shared_support + shared_support_increment, 10), cross_inhibition),
        (round(shared_support - shared_support_increment, 10), cross_inhibition),
        (shared_support, round(cross_inhibition + cross_inhibition_increment, 10)),
        (shared_support, round(cross_inhibition - cross_inhibition_increment, 10)),
    )


def mark_transition_boundaries(
    cells: list[ParameterCellResult],
    parameter_grid: ParameterGrid,
) -> None:
    """Mark cells bordering a regime change or fixed-point stability change."""
    cell_by_coordinates = {cell.coordinates: cell for cell in cells}
    shared_support_increment = calculate_grid_increment(
        parameter_grid.shared_support_values
    )
    cross_inhibition_increment = calculate_grid_increment(
        parameter_grid.cross_inhibition_values
    )

    for cell in cells:
        coordinates = neighboring_coordinates(
            cell,
            shared_support_increment,
            cross_inhibition_increment,
        )
        neighbors = [
            cell_by_coordinates[coordinate]
            for coordinate in coordinates
            if coordinate in cell_by_coordinates
        ]
        cell.borders_regime_transition = cell.seeds_disagree or any(
            neighbor.modal_regime != cell.modal_regime for neighbor in neighbors
        )
        cell.borders_stability_change = any(
            neighbor.fixed_point_stability.is_stable
            != cell.fixed_point_stability.is_stable
            for neighbor in neighbors
        )


def run_parameter_sweep(settings: SweepSettings) -> list[ParameterCellResult]:
    """Evaluate the full parameter grid and mark its transition boundaries."""
    cells = [
        evaluate_parameter_cell(shared_support, cross_inhibition, settings)
        for shared_support in settings.parameter_grid.shared_support_values
        for cross_inhibition in settings.parameter_grid.cross_inhibition_values
    ]
    mark_transition_boundaries(cells, settings.parameter_grid)
    return cells


def classify_robustness_trajectory(
    parameters: ModelParameters,
    number_of_steps: int,
    random_seed: int,
    thresholds: ClassificationThresholds,
) -> Regime:
    """Simulate and classify one trajectory for a robustness check."""
    trajectory = simulate_trajectory(
        parameters,
        number_of_steps=number_of_steps,
        random_seed=random_seed,
    )
    return classify_trajectory(trajectory, thresholds=thresholds).regime


def run_representative_scenario_checks() -> list[RobustnessCheck]:
    """Check named regimes across seven seeds and three simulation horizons."""
    checks = []
    thresholds = ClassificationThresholds()
    for expected_regime, parameters in REPRESENTATIVE_PARAMETERS.items():
        for number_of_steps in ROBUSTNESS_HORIZONS:
            for random_seed in DEFAULT_RANDOM_SEEDS:
                observed_regime = classify_robustness_trajectory(
                    parameters,
                    number_of_steps,
                    random_seed,
                    thresholds,
                )
                checks.append(
                    RobustnessCheck(
                        check_name="reference_horizon_seed",
                        expected_regime=expected_regime,
                        observed_regime=observed_regime,
                        shared_support=parameters.shared_support,
                        cross_inhibition=parameters.cross_inhibition,
                        number_of_steps=number_of_steps,
                        random_seed=random_seed,
                        collapse_capacity=thresholds.collapse_capacity,
                    )
                )
    return checks


def run_collapse_threshold_checks() -> list[RobustnessCheck]:
    """Check the collapse example under three nearby viability thresholds."""
    checks = []
    parameters = REPRESENTATIVE_PARAMETERS["collapse"]
    for collapse_capacity in COLLAPSE_CAPACITY_CHECKS:
        thresholds = replace(
            ClassificationThresholds(),
            collapse_capacity=collapse_capacity,
        )
        for random_seed in DEFAULT_RANDOM_SEEDS:
            observed_regime = classify_robustness_trajectory(
                parameters,
                600,
                random_seed,
                thresholds,
            )
            checks.append(
                RobustnessCheck(
                    check_name="collapse_threshold",
                    expected_regime="collapse",
                    observed_regime=observed_regime,
                    shared_support=parameters.shared_support,
                    cross_inhibition=parameters.cross_inhibition,
                    number_of_steps=600,
                    random_seed=random_seed,
                    collapse_capacity=collapse_capacity,
                )
            )
    return checks


def run_uncoupled_ablation_checks() -> list[RobustnessCheck]:
    """Check outcomes after canceling enablement with equal inhibition."""
    checks = []
    thresholds = ClassificationThresholds()
    for shared_support in ABLATION_SUPPORT_VALUES:
        parameters = ModelParameters(
            shared_support=shared_support,
            cross_inhibition=2.0,
            cross_enablement=2.0,
        )
        for random_seed in DEFAULT_RANDOM_SEEDS:
            observed_regime = classify_robustness_trajectory(
                parameters,
                600,
                random_seed,
                thresholds,
            )
            checks.append(
                RobustnessCheck(
                    check_name="uncoupled_ablation",
                    expected_regime="collapse_or_equilibrium",
                    observed_regime=observed_regime,
                    shared_support=shared_support,
                    cross_inhibition=parameters.cross_inhibition,
                    number_of_steps=600,
                    random_seed=random_seed,
                    collapse_capacity=thresholds.collapse_capacity,
                )
            )
    return checks


def run_robustness_checks() -> list[RobustnessCheck]:
    """Run every recorded horizon, seed, threshold, and ablation check."""
    return [
        *run_representative_scenario_checks(),
        *run_collapse_threshold_checks(),
        *run_uncoupled_ablation_checks(),
    ]


def generate_representative_trajectories() -> dict[Regime, SimulationTrajectory]:
    """Simulate one complete trajectory for each named example."""
    return {
        expected_regime: simulate_trajectory(
            parameters,
            number_of_steps=200,
            random_seed=7,
        )
        for expected_regime, parameters in REPRESENTATIVE_PARAMETERS.items()
    }
