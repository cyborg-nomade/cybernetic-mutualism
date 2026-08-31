"""A bounded two-variable response map for an antinomic relation.

The state variables are dimensionless capacities in [0, 1]: ``autonomy`` is
the capacity for local initiative and ``coordination`` is the capacity for
collective coordination.  The model is exploratory and is not calibrated to a
historical case.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Literal


Regime = Literal["collapse", "equilibrium", "lock-in", "oscillation", "unresolved"]


@dataclass(frozen=True)
class Parameters:
    """Parameters of the response map.

    ``support`` is the shared exogenous enabling condition. ``persistence`` is
    within-variable reproduction. ``mutual_enablement`` and ``opposition`` are
    positive cross-effects that enter with opposite signs. ``noise`` is the
    standard deviation of independent Gaussian shocks to the response logits.
    """

    support: float
    opposition: float
    persistence: float = 2.0
    mutual_enablement: float = 2.0
    noise: float = 0.0


@dataclass(frozen=True)
class Simulation:
    autonomy: tuple[float, ...]
    coordination: tuple[float, ...]
    seed: int
    parameters: Parameters


@dataclass(frozen=True)
class Classification:
    regime: Regime
    mean_autonomy: float
    mean_coordination: float
    fixed_error: float
    period_two_error: float
    oscillation_amplitude: float


def _sigmoid(value: float) -> float:
    value = max(-60.0, min(60.0, value))
    return 1.0 / (1.0 + math.exp(-value))


def step(
    autonomy: float,
    coordination: float,
    parameters: Parameters,
    rng: random.Random,
) -> tuple[float, float]:
    """Advance the synchronous map by one response interval."""

    net_cross = parameters.mutual_enablement - parameters.opposition
    autonomy_logit = (
        parameters.support
        + parameters.persistence * autonomy
        + net_cross * coordination
    )
    coordination_logit = (
        parameters.support
        + parameters.persistence * coordination
        + net_cross * autonomy
    )
    if parameters.noise:
        autonomy_logit += rng.gauss(0.0, parameters.noise)
        coordination_logit += rng.gauss(0.0, parameters.noise)
    return _sigmoid(autonomy_logit), _sigmoid(coordination_logit)


def simulate(
    parameters: Parameters,
    *,
    steps: int = 600,
    seed: int = 0,
    initial: tuple[float, float] | None = None,
) -> Simulation:
    """Simulate a trajectory with a reproducible initial perturbation."""

    if steps < 3:
        raise ValueError("steps must be at least 3")
    rng = random.Random(seed)
    if initial is None:
        initial = (rng.uniform(0.45, 0.55), rng.uniform(0.45, 0.55))
    if any(value < 0.0 or value > 1.0 for value in initial):
        raise ValueError("initial values must lie in [0, 1]")

    autonomy = [initial[0]]
    coordination = [initial[1]]
    for _ in range(steps):
        next_autonomy, next_coordination = step(
            autonomy[-1], coordination[-1], parameters, rng
        )
        autonomy.append(next_autonomy)
        coordination.append(next_coordination)
    return Simulation(
        autonomy=tuple(autonomy),
        coordination=tuple(coordination),
        seed=seed,
        parameters=parameters,
    )


def classify(
    simulation: Simulation,
    *,
    tail: int = 100,
    collapse_threshold: float = 0.1,
    lock_in_gap: float = 0.25,
    tolerance: float = 1e-7,
    oscillation_threshold: float = 0.05,
) -> Classification:
    """Classify the final attractor using declared operational thresholds.

    Collapse is a stable low-low state below a viability threshold, not a
    mathematical singularity. Lock-in is a stable asymmetric state. Oscillation
    is a persistent period-two orbit. Everything else is left unresolved.
    """

    if tail < 4 or len(simulation.autonomy) < tail:
        raise ValueError("tail must include at least four available states")
    a = simulation.autonomy[-tail:]
    c = simulation.coordination[-tail:]
    mean_a = sum(a) / tail
    mean_c = sum(c) / tail
    fixed_error = max(
        max(abs(a[index] - a[index - 1]), abs(c[index] - c[index - 1]))
        for index in range(1, tail)
    )
    period_two_error = max(
        max(abs(a[index] - a[index - 2]), abs(c[index] - c[index - 2]))
        for index in range(2, tail)
    )
    amplitude = max(max(a) - min(a), max(c) - min(c))

    if fixed_error <= tolerance:
        if max(mean_a, mean_c) < collapse_threshold:
            regime: Regime = "collapse"
        elif abs(mean_a - mean_c) >= lock_in_gap:
            regime = "lock-in"
        else:
            regime = "equilibrium"
    elif period_two_error <= tolerance and amplitude >= oscillation_threshold:
        regime = "oscillation"
    else:
        regime = "unresolved"

    return Classification(
        regime=regime,
        mean_autonomy=mean_a,
        mean_coordination=mean_c,
        fixed_error=fixed_error,
        period_two_error=period_two_error,
        oscillation_amplitude=amplitude,
    )
