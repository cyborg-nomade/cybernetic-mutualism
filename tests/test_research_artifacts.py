"""Protect structural conventions shared by research artifacts."""

from __future__ import annotations

import tomllib
import unittest
from datetime import timedelta
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
        self.assertIn("## Second Research Cycle — Active", roadmap)
        self.assertIn(
            "(research/decisions/first-cycle-synthesis.md)",
            roadmap,
        )
        self.assertIn("(decisions/first-cycle-synthesis.md)", claims)
        self.assertIn(
            "(posts/antinomies-are-dynamical-systems.md)",
            roadmap,
        )

    def test_manifesto_records_the_bounded_first_cycle_revision(self) -> None:
        """The published manifesto should make its dated correction visible."""
        manifesto = (REPOSITORY_ROOT / "MANIFESTO.md").read_text(encoding="utf-8")

        self.assertIn("revision note — 2026-09-01", manifesto)
        self.assertNotIn(
            "every order generates new asymmetries and new counterforces",
            manifesto,
        )

    def test_empirical_registration_packet_is_linked_and_complete(self) -> None:
        """Keep the frozen case, codebook, exposure audit, and decision connected."""
        directory = REPOSITORY_ROOT / "research/cases"
        manifest = tomllib.loads(
            (directory / "asf-autonomy-coordination-registration.toml").read_text()
        )
        expected_project_count = 4
        self.assertEqual(len(manifest["project_ids"]), expected_project_count)
        self.assertEqual(len(set(manifest["project_ids"])), expected_project_count)
        for key in ("protocol", "codebook", "source_audit", "structural_decision"):
            self.assertTrue((directory / manifest[key]).is_file(), key)
        for path in ("ROADMAP.md", "research/claims.md"):
            self.assertIn(manifest["protocol"], (REPOSITORY_ROOT / path).read_text())
        protocol = (directory / manifest["protocol"]).read_text()
        for key in ("codebook", "source_audit"):
            self.assertIn(manifest[key], protocol)

    def test_empirical_registration_windows_cover_all_response_horizons(self) -> None:
        """Prevent right-censoring the longest prespecified response sensitivity."""
        manifest = tomllib.loads(
            (
                REPOSITORY_ROOT
                / "research/cases/asf-autonomy-coordination-registration.toml"
            ).read_text()
        )
        self.assertLess(manifest["baseline_start"], manifest["baseline_end"])
        self.assertLess(manifest["baseline_end"], manifest["primary_start"])
        self.assertLess(manifest["primary_start"], manifest["primary_end"])
        longest_horizon = max(manifest["sensitivity_horizons_days"])
        self.assertLessEqual(
            manifest["primary_end"] + timedelta(days=longest_horizon),
            manifest["followup_end"],
        )
        self.assertLess(manifest["followup_end"], manifest["source_publication_cutoff"])
        self.assertLess(
            manifest["source_publication_cutoff"], manifest["registered_on"]
        )
        start, end = manifest["primary_start"], manifest["primary_end"]
        actual_months = (end.year - start.year) * 12 + end.month - start.month + 1
        self.assertEqual(manifest["primary_months"], actual_months)
        self.assertLessEqual(manifest["source_coverage_months_required"], actual_months)
        quarters = manifest["primary_months"] // 3
        self.assertEqual(
            manifest["project_quarter_blocks"],
            quarters * len(manifest["project_ids"]),
        )

    def test_empirical_registration_does_not_claim_evidence_or_external_review(
        self,
    ) -> None:
        """Keep design-time disclosures distinct from completed empirical work."""
        manifest = tomllib.loads(
            (
                REPOSITORY_ROOT
                / "research/cases/asf-autonomy-coordination-registration.toml"
            ).read_text()
        )
        self.assertFalse(manifest["outcome_collection_started_at_registration"])
        self.assertFalse(manifest["complete_outcome_blindness_claimed"])
        self.assertFalse(manifest["external_registry_submission"])
        self.assertTrue(manifest["independent_human_audit_required"])
        self.assertLessEqual(
            manifest["qualified_families_per_direction_required"],
            manifest["opportunity_families_per_direction_required"],
        )


if __name__ == "__main__":
    unittest.main()
