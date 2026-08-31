"""Expose the public interface for the minimal antinomy model."""

from .model import (
    ClassificationThresholds,
    ModelParameters,
    RegimeClassification,
    SimulationTrajectory,
    SystemState,
    classify_trajectory,
    simulate_trajectory,
)

__all__ = [
    "ClassificationThresholds",
    "ModelParameters",
    "RegimeClassification",
    "SimulationTrajectory",
    "SystemState",
    "classify_trajectory",
    "simulate_trajectory",
]
