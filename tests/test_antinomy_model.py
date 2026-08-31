import tempfile
import unittest
from pathlib import Path

from models.antinomy.generate import generate
from models.antinomy.model import Parameters, classify, simulate


class AntinomyModelTests(unittest.TestCase):
    def test_state_remains_bounded(self):
        result = simulate(
            Parameters(support=3.0, opposition=13.0, noise=0.2),
            steps=200,
            seed=11,
        )
        self.assertTrue(all(0.0 <= value <= 1.0 for value in result.autonomy))
        self.assertTrue(all(0.0 <= value <= 1.0 for value in result.coordination))

    def test_seed_reproduces_initial_conditions_and_noise(self):
        parameters = Parameters(support=0.0, opposition=6.0, noise=0.05)
        first = simulate(parameters, steps=30, seed=17)
        second = simulate(parameters, steps=30, seed=17)
        different = simulate(parameters, steps=30, seed=18)
        self.assertEqual(first, second)
        self.assertNotEqual(first.autonomy, different.autonomy)

    def test_equations_are_symmetric_under_variable_exchange(self):
        parameters = Parameters(support=0.0, opposition=6.0)
        first = simulate(parameters, steps=80, seed=3, initial=(0.52, 0.48))
        second = simulate(parameters, steps=80, seed=3, initial=(0.48, 0.52))
        self.assertEqual(first.autonomy, second.coordination)
        self.assertEqual(first.coordination, second.autonomy)

    def test_reference_regimes_are_distinct(self):
        references = {
            "collapse": Parameters(support=-4.0, opposition=4.0),
            "equilibrium": Parameters(support=0.0, opposition=2.0),
            "lock-in": Parameters(support=0.0, opposition=6.0),
            "oscillation": Parameters(support=2.0, opposition=12.0),
        }
        observed = {
            name: classify(simulate(parameters, steps=600, seed=7)).regime
            for name, parameters in references.items()
        }
        self.assertEqual(observed, {name: name for name in references})

    def test_uncoupled_ablation_does_not_create_lock_in_or_coupled_oscillation(self):
        regimes = {
            classify(
                simulate(
                    Parameters(
                        support=support,
                        opposition=2.0,
                        mutual_enablement=2.0,
                    ),
                    steps=600,
                    seed=seed,
                )
            ).regime
            for support in (-4.0, -2.0, 0.0, 2.0)
            for seed in (7, 19, 41)
        }
        self.assertTrue(regimes <= {"collapse", "equilibrium"})

    def test_generator_writes_reproducible_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            first = generate(output)
            first_csv = (output / "parameter_sweep.csv").read_bytes()
            second = generate(output)
            self.assertEqual(first, second)
            self.assertEqual(first_csv, (output / "parameter_sweep.csv").read_bytes())
            self.assertEqual(first["sweep"]["cells"], 2337)
            self.assertTrue((output / "parameter_map.svg").exists())


if __name__ == "__main__":
    unittest.main()
