"""Verify the antinomy model, its regime definitions, and its artifacts."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from models.antinomy.generate import generate_outputs
from models.antinomy.model import (
    ClassificationThresholds,
    ModelParameters,
    SystemState,
    classify_trajectory,
    simulate_trajectory,
)
from models.antinomy.sweep import ParameterGrid, SweepSettings


class AntinomyModelTests(unittest.TestCase):
    """Test scientific invariants and the committed reference scenarios."""

    def test_state_remains_bounded(self) -> None:
        """Sigmoid saturation should keep every simulated capacity in bounds."""
        trajectory = simulate_trajectory(
            ModelParameters(
                shared_support=3.0,
                cross_inhibition=13.0,
                shock_standard_deviation=0.2,
            ),
            number_of_steps=200,
            random_seed=11,
        )
        capacities = (
            capacity
            for state in trajectory.states
            for capacity in (
                state.autonomy_capacity,
                state.coordination_capacity,
            )
        )
        self.assertTrue(all(0.0 <= capacity <= 1.0 for capacity in capacities))

    def test_seed_reproduces_initial_conditions_and_noise(self) -> None:
        """A repeated seed should reproduce the complete noisy trajectory."""
        parameters = ModelParameters(
            shared_support=0.0,
            cross_inhibition=6.0,
            shock_standard_deviation=0.05,
        )
        first_trajectory = simulate_trajectory(
            parameters,
            number_of_steps=30,
            random_seed=17,
        )
        repeated_trajectory = simulate_trajectory(
            parameters,
            number_of_steps=30,
            random_seed=17,
        )
        different_trajectory = simulate_trajectory(
            parameters,
            number_of_steps=30,
            random_seed=18,
        )

        self.assertEqual(first_trajectory, repeated_trajectory)
        self.assertNotEqual(first_trajectory.states, different_trajectory.states)

    def test_equations_are_symmetric_under_variable_exchange(self) -> None:
        """Exchanging initial capacities should exchange deterministic outputs."""
        parameters = ModelParameters(
            shared_support=0.0,
            cross_inhibition=6.0,
        )
        autonomy_first = simulate_trajectory(
            parameters,
            number_of_steps=80,
            random_seed=3,
            initial_state=SystemState(0.52, 0.48),
        )
        coordination_first = simulate_trajectory(
            parameters,
            number_of_steps=80,
            random_seed=3,
            initial_state=SystemState(0.48, 0.52),
        )

        for first_state, exchanged_state in zip(
            autonomy_first.states,
            coordination_first.states,
            strict=True,
        ):
            self.assertEqual(
                first_state.autonomy_capacity,
                exchanged_state.coordination_capacity,
            )
            self.assertEqual(
                first_state.coordination_capacity,
                exchanged_state.autonomy_capacity,
            )

    def test_reference_regimes_are_distinct(self) -> None:
        """The four prespecified examples should receive their expected labels."""
        reference_parameters = {
            "collapse": ModelParameters(
                shared_support=-4.0,
                cross_inhibition=4.0,
            ),
            "equilibrium": ModelParameters(
                shared_support=0.0,
                cross_inhibition=2.0,
            ),
            "lock-in": ModelParameters(
                shared_support=0.0,
                cross_inhibition=6.0,
            ),
            "oscillation": ModelParameters(
                shared_support=2.0,
                cross_inhibition=12.0,
            ),
        }
        observed_regimes = {
            expected_regime: classify_trajectory(
                simulate_trajectory(
                    parameters,
                    number_of_steps=600,
                    random_seed=7,
                )
            ).regime
            for expected_regime, parameters in reference_parameters.items()
        }

        expected_regimes = {
            expected_regime: expected_regime for expected_regime in reference_parameters
        }
        self.assertEqual(observed_regimes, expected_regimes)

    def test_uncoupled_ablation_has_no_lock_in_or_coupled_oscillation(self) -> None:
        """Canceling cross-effects should remove the two coupling-led outcomes."""
        observed_regimes = {
            classify_trajectory(
                simulate_trajectory(
                    ModelParameters(
                        shared_support=shared_support,
                        cross_inhibition=2.0,
                        cross_enablement=2.0,
                    ),
                    number_of_steps=600,
                    random_seed=random_seed,
                )
            ).regime
            for shared_support in (-4.0, -2.0, 0.0, 2.0)
            for random_seed in (7, 19, 41)
        }

        self.assertTrue(observed_regimes <= {"collapse", "equilibrium"})

    def test_generator_writes_reproducible_artifacts(self) -> None:
        """Two generations should produce identical summaries and sweep bytes."""
        compact_settings = SweepSettings(
            parameter_grid=ParameterGrid(
                shared_support_values=(-6.0, 4.0),
                cross_inhibition_values=(0.0, 14.0),
            ),
            random_seeds=(7, 19),
            number_of_steps=100,
            classification_thresholds=ClassificationThresholds(tail_length=50),
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory)
            first_summary = generate_outputs(
                output_directory,
                sweep_settings=compact_settings,
            )
            first_sweep = (output_directory / "parameter_sweep.csv").read_bytes()

            repeated_summary = generate_outputs(
                output_directory,
                sweep_settings=compact_settings,
            )
            repeated_sweep = (output_directory / "parameter_sweep.csv").read_bytes()

            self.assertEqual(first_summary, repeated_summary)
            self.assertEqual(first_sweep, repeated_sweep)
            sweep_summary = first_summary["sweep"]
            self.assertIsInstance(sweep_summary, dict)
            self.assertEqual(sweep_summary["cells"], 4)
            self.assertTrue((output_directory / "parameter_map.svg").exists())


if __name__ == "__main__":
    unittest.main()
