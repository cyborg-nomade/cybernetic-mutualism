"""Protect structural conventions shared by research artifacts."""

from __future__ import annotations

import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CONCLUSION_HEADING = "## Conclusions and Next Steps"


def find_research_artifacts() -> list[Path]:
    """Return current case, decision, experiment, and model-note files."""
    artifact_patterns = (
        "research/cases/*.md",
        "research/decisions/*.md",
        "research/experiments/*.md",
        "models/**/README.md",
    )
    return sorted(
        artifact_path
        for pattern in artifact_patterns
        for artifact_path in REPOSITORY_ROOT.glob(pattern)
    )


class ResearchArtifactTests(unittest.TestCase):
    """Require a clear conclusion and handoff in every research artifact."""

    def test_conclusions_and_next_steps_is_final_major_section(self) -> None:
        """Each artifact should end under the shared conclusion heading."""
        artifact_paths = find_research_artifacts()
        self.assertTrue(artifact_paths, "expected at least one research artifact")

        for artifact_path in artifact_paths:
            with self.subTest(path=artifact_path.relative_to(REPOSITORY_ROOT)):
                document = artifact_path.read_text(encoding="utf-8")
                conclusion_position = document.find(CONCLUSION_HEADING)
                self.assertGreaterEqual(conclusion_position, 0)
                later_major_heading = document.find("\n## ", conclusion_position + 1)
                self.assertEqual(later_major_heading, -1)

    def test_cycle_status_and_decision_links_are_registered(self) -> None:
        """Cycle labels should retain their decision record and proposal status."""
        roadmap = (REPOSITORY_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
        claims = (REPOSITORY_ROOT / "research/claims.md").read_text(encoding="utf-8")

        self.assertIn("## First Research Cycle — Complete", roadmap)
        self.assertIn("## Second Research Cycle — Proposed", roadmap)
        self.assertIn(
            "(research/decisions/first-cycle-synthesis.md)",
            roadmap,
        )
        self.assertIn("(decisions/first-cycle-synthesis.md)", claims)

    def test_manifesto_records_the_bounded_first_cycle_revision(self) -> None:
        """The published manifesto should make its dated correction visible."""
        manifesto = (REPOSITORY_ROOT / "MANIFESTO.md").read_text(encoding="utf-8")

        self.assertIn("revision note — 2026-09-01", manifesto)
        self.assertNotIn(
            "every order generates new asymmetries and new counterforces",
            manifesto,
        )


if __name__ == "__main__":
    unittest.main()
