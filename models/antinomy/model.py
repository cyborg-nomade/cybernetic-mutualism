"""Simulate and classify a minimal two-variable antinomic relation.

The model tracks two dimensionless capacities between zero and one:

* local autonomy: the capacity of local units to initiate or vary action; and
* collective coordination: the capacity to align action and maintain common
  commitments.

The module deliberately uses descriptive names and small functions. Readers
should be able to follow the implementation alongside the equations in the
model README without needing prior Python experience.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Literal

Regime = Literal[
    "collapse",
    "equilibrium",
    "lock-in",
    "oscillation",
    "unresolved",
]
MINIMUM_SIMULATION_STEPS = 3
MINIMUM_CLASSIFICATION_TAIL = 4


@dataclass(frozen=True)
class SystemState:
    """Store both capacities at one response interval.

    Attributes:
        autonomy_capacity: Capacity for local initiative, bounded in ``[0, 1]``.
        coordination_capacity: Capacity for collective coordination, also
            bounded in ``[0, 1]``.
    """

    autonomy_capacity: float
    coordination_capacity: float


@dataclass(frozen=True)
class ModelParameters:
    """Define the mechanisms that determine the next system state.

    Attributes:
        shared_support: Exogenous conditions available to both capacities.
        cross_inhibition: Strength with which each capacity suppresses the
            other capacity.
        self_reinforcement: Strength with which each capacity reproduces itself.
        cross_enablement: Strength with which each capacity supports the other.
        shock_standard_deviation: Size of optional independent Gaussian shocks.
    """

    shared_support: float
    cross_inhibition: float
    self_reinforcement: float = 2.0
    cross_enablement: float = 2.0
    shock_standard_deviation: float = 0.0

    def __post_init__(self) -> None:
        """Reject a negative shock standard deviation."""
        if self.shock_standard_deviation < 0.0:
            message = "shock_standard_deviation cannot be negative"
            raise ValueError(message)

    @property
    def net_cross_effect(self) -> float:
        """Return enablement minus inhibition between the two capacities."""
        return self.cross_enablement - self.cross_inhibition


@dataclass(frozen=True)
class SimulationTrajectory:
    """Store a complete simulation and the choices needed to reproduce it.

    Attributes:
        states: Initial state followed by every simulated state.
        random_seed: Seed used for the initial perturbation and optional shocks.
        parameters: Mechanism parameters held fixed during the simulation.
    """

    states: tuple[SystemState, ...]
    random_seed: int
    parameters: ModelParameters


@dataclass(frozen=True)
class ClassificationThresholds:
    """Define the operational boundaries between named regimes.

    Attributes:
        tail_length: Number of final states used to classify a trajectory.
        collapse_capacity: Upper capacity bound for operational collapse.
        lock_in_gap: Minimum gap between capacities for asymmetric lock-in.
        numerical_tolerance: Maximum numerical error for a repeated state.
        minimum_oscillation_amplitude: Minimum size of a period-two cycle.
    """

    tail_length: int = 100
    collapse_capacity: float = 0.1
    lock_in_gap: float = 0.25
    numerical_tolerance: float = 1e-7
    minimum_oscillation_amplitude: float = 0.05


@dataclass(frozen=True)
class TrajectoryMetrics:
    """Summarize the final states used for regime classification.

    Attributes:
        mean_autonomy_capacity: Mean local autonomy over the classification tail.
        mean_coordination_capacity: Mean coordination over the same tail.
        largest_step_change: Largest change between consecutive states.
        period_two_error: Largest difference between states two intervals apart.
        oscillation_amplitude: Largest range observed in either capacity.
    """

    mean_autonomy_capacity: float
    mean_coordination_capacity: float
    largest_step_change: float
    period_two_error: float
    oscillation_amplitude: float


@dataclass(frozen=True)
class RegimeClassification:
    """Pair a named long-run regime with the measurements supporting it."""

    regime: Regime
    metrics: TrajectoryMetrics


def sigmoid_response(response_input: float) -> float:
    """Convert an unbounded response input to a capacity between zero and one."""
    numerically_safe_input = max(-60.0, min(60.0, response_input))
    return 1.0 / (1.0 + math.exp(-numerically_safe_input))


def calculate_response_input(
    own_capacity: float,
    other_capacity: float,
    parameters: ModelParameters,
) -> float:
    """Calculate the pre-saturation input for one capacity.

    The same calculation is used for autonomy and coordination. This shared
    rule is the model's symmetry assumption.
    """
    self_reproduction = parameters.self_reinforcement * own_capacity
    cross_effect = parameters.net_cross_effect * other_capacity
    return parameters.shared_support + self_reproduction + cross_effect


def add_optional_shock(
    response_input: float,
    shock_standard_deviation: float,
    random_number_generator: random.Random,
) -> float:
    """Add a seeded Gaussian shock when its configured size is above zero."""
    if shock_standard_deviation == 0.0:
        return response_input
    random_shock = random_number_generator.gauss(0.0, shock_standard_deviation)
    return response_input + random_shock


def advance_one_interval(
    current_state: SystemState,
    parameters: ModelParameters,
    random_number_generator: random.Random,
) -> SystemState:
    """Apply the response rule synchronously to both capacities."""
    autonomy_input = calculate_response_input(
        current_state.autonomy_capacity,
        current_state.coordination_capacity,
        parameters,
    )
    coordination_input = calculate_response_input(
        current_state.coordination_capacity,
        current_state.autonomy_capacity,
        parameters,
    )
    autonomy_input = add_optional_shock(
        autonomy_input,
        parameters.shock_standard_deviation,
        random_number_generator,
    )
    coordination_input = add_optional_shock(
        coordination_input,
        parameters.shock_standard_deviation,
        random_number_generator,
    )
    return SystemState(
        autonomy_capacity=sigmoid_response(autonomy_input),
        coordination_capacity=sigmoid_response(coordination_input),
    )


def create_seeded_initial_state(
    random_number_generator: random.Random,
) -> SystemState:
    """Create a small seeded perturbation around the balanced state ``0.5``."""
    return SystemState(
        autonomy_capacity=random_number_generator.uniform(0.45, 0.55),
        coordination_capacity=random_number_generator.uniform(0.45, 0.55),
    )


def validate_initial_state(initial_state: SystemState) -> None:
    """Require both initial capacities to lie inside the model bounds."""
    capacities = (
        initial_state.autonomy_capacity,
        initial_state.coordination_capacity,
    )
    if any(capacity < 0.0 or capacity > 1.0 for capacity in capacities):
        message = "initial capacities must lie in [0, 1]"
        raise ValueError(message)


def simulate_trajectory(
    parameters: ModelParameters,
    *,
    number_of_steps: int = 600,
    random_seed: int = 0,
    initial_state: SystemState | None = None,
) -> SimulationTrajectory:
    """Simulate a trajectory from a supplied or reproducible initial state."""
    if number_of_steps < MINIMUM_SIMULATION_STEPS:
        message = "number_of_steps must be at least 3"
        raise ValueError(message)

    random_number_generator = random.Random(random_seed)
    starting_state = initial_state or create_seeded_initial_state(
        random_number_generator
    )
    validate_initial_state(starting_state)

    states = [starting_state]
    for _step_number in range(number_of_steps):
        next_state = advance_one_interval(
            states[-1],
            parameters,
            random_number_generator,
        )
        states.append(next_state)

    return SimulationTrajectory(
        states=tuple(states),
        random_seed=random_seed,
        parameters=parameters,
    )


def state_distance(first_state: SystemState, second_state: SystemState) -> float:
    """Return the largest capacity difference between two states."""
    autonomy_difference = abs(
        first_state.autonomy_capacity - second_state.autonomy_capacity
    )
    coordination_difference = abs(
        first_state.coordination_capacity - second_state.coordination_capacity
    )
    return max(autonomy_difference, coordination_difference)


def calculate_largest_step_change(states: tuple[SystemState, ...]) -> float:
    """Measure the largest change between consecutive states."""
    consecutive_pairs = zip(states[1:], states[:-1], strict=True)
    return max(
        state_distance(current_state, previous_state)
        for current_state, previous_state in consecutive_pairs
    )


def calculate_period_two_error(states: tuple[SystemState, ...]) -> float:
    """Measure how closely each state repeats the state two intervals earlier."""
    period_two_pairs = zip(states[2:], states[:-2], strict=True)
    return max(
        state_distance(current_state, previous_cycle_state)
        for current_state, previous_cycle_state in period_two_pairs
    )


def calculate_capacity_range(capacity_values: list[float]) -> float:
    """Return the observed range of a nonempty capacity series."""
    return max(capacity_values) - min(capacity_values)


def calculate_trajectory_metrics(
    tail_states: tuple[SystemState, ...],
) -> TrajectoryMetrics:
    """Calculate the measurements needed to classify a trajectory tail."""
    autonomy_values = [state.autonomy_capacity for state in tail_states]
    coordination_values = [state.coordination_capacity for state in tail_states]
    oscillation_amplitude = max(
        calculate_capacity_range(autonomy_values),
        calculate_capacity_range(coordination_values),
    )
    return TrajectoryMetrics(
        mean_autonomy_capacity=sum(autonomy_values) / len(autonomy_values),
        mean_coordination_capacity=sum(coordination_values) / len(coordination_values),
        largest_step_change=calculate_largest_step_change(tail_states),
        period_two_error=calculate_period_two_error(tail_states),
        oscillation_amplitude=oscillation_amplitude,
    )


def classify_fixed_state(
    metrics: TrajectoryMetrics,
    thresholds: ClassificationThresholds,
) -> Regime:
    """Distinguish collapse, lock-in, and balanced fixed equilibrium."""
    largest_mean_capacity = max(
        metrics.mean_autonomy_capacity,
        metrics.mean_coordination_capacity,
    )
    if largest_mean_capacity < thresholds.collapse_capacity:
        return "collapse"

    capacity_gap = abs(
        metrics.mean_autonomy_capacity - metrics.mean_coordination_capacity
    )
    if capacity_gap >= thresholds.lock_in_gap:
        return "lock-in"
    return "equilibrium"


def is_period_two_oscillation(
    metrics: TrajectoryMetrics,
    thresholds: ClassificationThresholds,
) -> bool:
    """Return whether the metrics meet the declared period-two definition."""
    repeats_after_two_steps = metrics.period_two_error <= thresholds.numerical_tolerance
    has_meaningful_amplitude = (
        metrics.oscillation_amplitude >= thresholds.minimum_oscillation_amplitude
    )
    return repeats_after_two_steps and has_meaningful_amplitude


def classify_trajectory(
    trajectory: SimulationTrajectory,
    *,
    thresholds: ClassificationThresholds | None = None,
) -> RegimeClassification:
    """Classify the final trajectory as a declared regime or unresolved.

    Collapse is a stable low-low state below a viability threshold, not a
    mathematical singularity. Lock-in is a stable asymmetric state.
    Oscillation is a persistent period-two orbit. Everything else remains
    unresolved rather than being forced into a named category.
    """
    selected_thresholds = thresholds or ClassificationThresholds()
    if selected_thresholds.tail_length < MINIMUM_CLASSIFICATION_TAIL:
        message = "the classification tail must include at least four states"
        raise ValueError(message)
    if len(trajectory.states) < selected_thresholds.tail_length:
        message = "the trajectory is shorter than the classification tail"
        raise ValueError(message)

    tail_states = trajectory.states[-selected_thresholds.tail_length :]
    metrics = calculate_trajectory_metrics(tail_states)
    is_fixed_state = (
        metrics.largest_step_change <= selected_thresholds.numerical_tolerance
    )
    if is_fixed_state:
        regime = classify_fixed_state(metrics, selected_thresholds)
    elif is_period_two_oscillation(metrics, selected_thresholds):
        regime = "oscillation"
    else:
        regime = "unresolved"

    return RegimeClassification(regime=regime, metrics=metrics)
