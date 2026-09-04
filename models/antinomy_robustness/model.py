"""Define directional coupling, response shape, and paired update schedules."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Literal

from models.antinomy.model import (
    ClassificationThresholds,
    RegimeClassification,
    SystemState,
    calculate_trajectory_metrics,
    classify_fixed_state,
    create_seeded_initial_state,
    is_period_two_oscillation,
    sigmoid_response,
)

Response = Literal["logistic", "arctangent"]
Schedule = Literal["synchronous", "autonomy-first", "coordination-first"]
RESPONSES: tuple[Response, ...] = ("logistic", "arctangent")
SCHEDULES: tuple[Schedule, ...] = (
    "synchronous",
    "autonomy-first",
    "coordination-first",
)
MINIMUM_TAIL = 4
DEFAULT_THRESHOLDS = ClassificationThresholds()


@dataclass(frozen=True)
class DirectionParameters:
    """Store support and signed mechanisms acting on one receiving capacity."""

    support: float
    persistence: float = 2.0
    enablement: float = 2.0
    inhibition: float = 2.0

    def __post_init__(self) -> None:
        """Require finite inputs and nonnegative mechanism strengths."""
        values = (self.support, self.persistence, self.enablement, self.inhibition)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("direction parameters must be finite")
        if min(self.persistence, self.enablement, self.inhibition) < 0:
            raise ValueError("mechanism strengths cannot be negative")


@dataclass(frozen=True)
class VariantParameters:
    """Describe both directions without imposing equal mechanisms or timing."""

    autonomy: DirectionParameters
    coordination: DirectionParameters
    response: Response = "logistic"
    schedule: Schedule = "synchronous"

    def __post_init__(self) -> None:
        """Reject unsupported response functions and update schedules."""
        if self.response not in RESPONSES or self.schedule not in SCHEDULES:
            raise ValueError("unknown response or schedule")


def bounded_response(value: float, response: Response) -> float:
    """Apply logistic or slope-matched arctangent saturation."""
    if response == "logistic":
        return sigmoid_response(value)
    if response == "arctangent":
        return 0.5 + math.atan(math.pi * value / 4.0) / math.pi
    raise ValueError("unknown response")


def update_capacity(
    own: float,
    other: float,
    direction: DirectionParameters,
    response: Response,
) -> float:
    """Combine persistence and net incoming coupling before saturation."""
    self_reproduction = direction.persistence * own
    cross_effect = (direction.enablement - direction.inhibition) * other
    return bounded_response(
        direction.support + self_reproduction + cross_effect, response
    )


def advance_round(state: SystemState, parameters: VariantParameters) -> SystemState:
    """Update both capacities once, using new information only in sequential maps."""
    autonomy = state.autonomy_capacity
    coordination = state.coordination_capacity
    if parameters.schedule == "coordination-first":
        coordination = update_capacity(
            coordination,
            autonomy,
            parameters.coordination,
            parameters.response,
        )
    next_autonomy = update_capacity(
        autonomy,
        coordination,
        parameters.autonomy,
        parameters.response,
    )
    if parameters.schedule == "autonomy-first":
        autonomy = next_autonomy
    if parameters.schedule != "coordination-first":
        coordination = update_capacity(
            coordination,
            autonomy,
            parameters.coordination,
            parameters.response,
        )
    return SystemState(next_autonomy, coordination)


def simulate_states(
    parameters: VariantParameters,
    *,
    steps: int = 600,
    seed: int = 7,
    initial_state: SystemState | None = None,
) -> tuple[SystemState, ...]:
    """Return initial state and round-boundary states with deterministic seeds."""
    if not isinstance(steps, int) or isinstance(steps, bool) or steps < MINIMUM_TAIL:
        raise ValueError("steps must be an integer of at least four")
    initial = initial_state or create_seeded_initial_state(random.Random(seed))
    capacities = (initial.autonomy_capacity, initial.coordination_capacity)
    if not all(math.isfinite(value) and 0 <= value <= 1 for value in capacities):
        raise ValueError("initial capacities must be finite and in [0, 1]")
    states = [initial]
    for _round in range(steps):
        states.append(advance_round(states[-1], parameters))
    return tuple(states)


def classify_states(
    states: tuple[SystemState, ...],
    thresholds: ClassificationThresholds = DEFAULT_THRESHOLDS,
) -> RegimeClassification:
    """Use the baseline metrics and classification order without fake metadata."""
    if not MINIMUM_TAIL <= thresholds.tail_length <= len(states):
        raise ValueError("classification tail must fit and include four states")
    metrics = calculate_trajectory_metrics(states[-thresholds.tail_length :])
    if metrics.largest_step_change <= thresholds.numerical_tolerance:
        regime = classify_fixed_state(metrics, thresholds)
    elif is_period_two_oscillation(metrics, thresholds):
        regime = "oscillation"
    else:
        regime = "unresolved"
    return RegimeClassification(regime, metrics)
