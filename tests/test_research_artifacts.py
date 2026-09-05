"""Protect structural conventions shared by research artifacts."""

from __future__ import annotations

import tomllib
import unittest
from datetime import date, timedelta
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
        expected_project_ids = {"httpd", "tomcat", "maven", "ant"}
        self.assertEqual(set(manifest["project_ids"]), expected_project_ids)
        self.assertEqual(len(manifest["project_ids"]), len(expected_project_ids))
        expected_claims = {"CM-01", "CM-04", "CM-12", "CM-13"}
        self.assertEqual(set(manifest["claims"]), expected_claims)
        self.assertEqual(len(manifest["claims"]), len(expected_claims))
        self.assertEqual(
            manifest["amendment_ids"],
            [
                "pr13-review-clarifications-2026-09-04",
                "solo-completion-and-research-yield-2026-09-05",
            ],
        )
        for key in ("protocol", "codebook", "source_audit", "structural_decision"):
            self.assertTrue((directory / manifest[key]).is_file(), key)
        expected_targets = {
            "ROADMAP.md": f"research/cases/{manifest['protocol']}",
            "research/claims.md": f"cases/{manifest['protocol']}",
        }
        for path, target in expected_targets.items():
            document = (REPOSITORY_ROOT / path).read_text()
            self.assertIn(f"]({target})", document)
        protocol = (directory / manifest["protocol"]).read_text()
        self.assertIn("## Registration Amendment 2", protocol)
        self.assertIn(
            "primary category is indeterminate,\nnarrow its empirical applicability",
            protocol,
        )
        for key in ("codebook", "source_audit"):
            self.assertIn(f"]({manifest[key]})", protocol)
        source_audit = (directory / manifest["source_audit"]).read_text()
        self.assertIn("Initial audit date: 2026-09-04", source_audit)
        self.assertIn("Amendment check date: 2026-09-05", source_audit)

    def test_empirical_registration_windows_cover_all_response_horizons(self) -> None:
        """Prevent right-censoring the longest prespecified response sensitivity."""
        manifest = tomllib.loads(
            (
                REPOSITORY_ROOT
                / "research/cases/asf-autonomy-coordination-registration.toml"
            ).read_text()
        )
        frozen_values = {
            "registered_on": date(2026, 9, 4),
            "amended_on": date(2026, 9, 5),
            "baseline_start": date(2022, 10, 1),
            "baseline_end": date(2022, 12, 31),
            "primary_start": date(2023, 1, 1),
            "primary_end": date(2025, 12, 31),
            "followup_end": date(2026, 6, 30),
            "source_publication_cutoff": date(2026, 8, 31),
            "primary_horizon_days": 90,
            "sensitivity_horizons_days": [60, 180],
            "primary_months": 36,
            "project_quarter_blocks": 48,
            "local_release_baseline_per_nonempty_project_quarter": 1,
            "maximum_local_release_baseline_families": 48,
            "source_coverage_months_required": 33,
            "opportunity_families_per_direction_required": 4,
            "classifiable_opportunity_fraction_required": 0.75,
            "qualified_families_per_direction_required": 2,
            "projects_per_direction_required": 2,
            "required_signs": ["enablement", "constraint"],
        }
        for key, expected in frozen_values.items():
            with self.subTest(key=key):
                self.assertEqual(manifest[key], expected)
        self.assertLess(manifest["baseline_start"], manifest["baseline_end"])
        self.assertLess(manifest["baseline_end"], manifest["primary_start"])
        self.assertLess(manifest["primary_start"], manifest["primary_end"])
        horizons = [
            manifest["primary_horizon_days"],
            *manifest["sensitivity_horizons_days"],
        ]
        self.assertTrue(
            all(
                isinstance(horizon, int)
                and not isinstance(horizon, bool)
                and horizon > 0
                for horizon in horizons
            )
        )
        longest_horizon = max(horizons)
        self.assertLessEqual(
            manifest["primary_end"] + timedelta(days=longest_horizon),
            manifest["followup_end"],
        )
        self.assertLess(manifest["followup_end"], manifest["source_publication_cutoff"])
        self.assertLess(
            manifest["source_publication_cutoff"], manifest["registered_on"]
        )
        self.assertGreaterEqual(manifest["amended_on"], manifest["registered_on"])
        start, end = manifest["primary_start"], manifest["primary_end"]
        actual_months = (end.year - start.year) * 12 + end.month - start.month + 1
        self.assertEqual(manifest["primary_months"], actual_months)
        self.assertLessEqual(manifest["source_coverage_months_required"], actual_months)
        quarters = manifest["primary_months"] // 3
        self.assertEqual(
            manifest["project_quarter_blocks"],
            quarters * len(manifest["project_ids"]),
        )

    def test_empirical_registration_is_solo_completable_without_claiming_evidence(
        self,
    ) -> None:
        """Keep design-time disclosures distinct from completed empirical work."""
        manifest = tomllib.loads(
            (
                REPOSITORY_ROOT
                / "research/cases/asf-autonomy-coordination-registration.toml"
            ).read_text()
        )
        self.assertIs(manifest["outcome_collection_started_at_registration"], False)
        self.assertIs(manifest["complete_outcome_blindness_claimed"], False)
        self.assertIs(manifest["external_registry_submission"], False)
        self.assertIs(manifest["independent_human_audit_required"], False)
        self.assertIs(manifest["external_human_replication_optional"], True)
        self.assertIs(manifest["solo_completion_required"], True)
        self.assertIs(manifest["solo_recode_required"], True)
        self.assertIs(manifest["executable_integrity_audit_required"], True)
        self.assertGreaterEqual(manifest["solo_recode_washout_days"], 14)
        self.assertEqual(manifest["solo_recode_agreement_required"], 0.90)
        self.assertEqual(manifest["nonopportunity_recode_fraction"], 0.20)
        self.assertIs(manifest["separate_family_per_required_sign"], True)
        self.assertIs(
            manifest["sensitivity_difference_at_either_horizon_qualifies"], True
        )
        self.assertIs(manifest["audit_all_opportunity_families"], True)
        self.assertIs(manifest["audit_selection_reason_blinded"], True)

    def test_empirical_registration_fixes_nested_claim_decisions(self) -> None:
        """Keep the added claim yield bounded by machine-readable decision rules."""
        manifest = tomllib.loads(
            (
                REPOSITORY_ROOT
                / "research/cases/asf-autonomy-coordination-registration.toml"
            ).read_text()
        )
        expected_allowed_values = {
            "local_origin": ["pmc", "foundation", "external", "unknown"],
            "decision_right": [
                "pmc_binding",
                "foundation_case_specific_authorization",
                "shared_authorization",
                "unknown",
            ],
            "decision_authority_shift": [
                "toward_pmc",
                "toward_foundation",
                "toward_shared",
                "unchanged",
                "unknown",
            ],
            "authority_outcome_link_met": ["yes", "no", "unknown"],
            "local_disposition": [
                "adopted",
                "rejected",
                "revised",
                "withdrawn",
                "pending",
                "unknown",
            ],
            "autonomy_change": ["expanded", "restricted", "unchanged", "unknown"],
            "newly_feasible_action_executed": [
                "yes",
                "no",
                "not_applicable",
                "unknown",
            ],
            "commitment_mode": ["voluntary", "imposed", "mixed", "unknown"],
            "shared_commitment_named": [
                "yes",
                "no",
                "not_applicable",
                "unknown",
            ],
            "coordination_disposition": [
                "created",
                "implemented",
                "revised",
                "refused",
                "failed",
                "ongoing",
                "unknown",
            ],
            "coordination_burden_change": [
                "increased",
                "decreased",
                "unchanged",
                "unknown",
            ],
            "receiver_observed": ["known", "unknown"],
            "temporal_order": [
                "sender_first",
                "receiver_first",
                "documented_within_day_order",
                "unknown",
            ],
            "channel": [
                "public_cross_reference",
                "documented_official_act",
                "public_service_record",
                "private_only_reference",
                "unknown",
            ],
            "effect_sign": [
                "enablement",
                "constraint",
                "both",
                "no_demonstrated_effect",
                "unknown",
            ],
            "viability_event": [
                "official_status_change",
                "explicit_obligation_failure",
                "no_documented_event",
                "unknown",
            ],
        }
        self.assertEqual(manifest["allowed_values"], expected_allowed_values)
        self.assertIs(manifest["claim_c2_requires_all_gates"], True)
        self.assertIs(manifest["cm01_c2_requires_full_result_at_all_horizons"], True)
        self.assertEqual(
            manifest["cm04_indeterminate_decision"],
            "narrow_observational_applicability",
        )
        self.assertIs(
            manifest["nested_claim_c2_requires_mixed_result_at_all_horizons"], True
        )
        self.assertEqual(manifest["nested_claim_families_required"], 2)
        self.assertEqual(manifest["nested_claim_projects_required"], 2)
        self.assertEqual(
            manifest["nested_claim_family_required_values"],
            ["qualified_witness:yes", "authority_outcome_link_met:yes"],
        )
        self.assertEqual(
            manifest["cm12_family_required_values"],
            ["decision_authority_shift:toward_pmc"],
        )
        self.assertEqual(
            manifest["cm12_generative_required_values"],
            [
                "autonomy_change:expanded",
                "newly_feasible_action_executed:yes",
            ],
        )
        self.assertEqual(
            manifest["cm12_disorganising_any_condition_sets"],
            [
                ["coordination_burden_change:increased"],
                ["shared_commitment_named:yes", "coordination_disposition:failed"],
            ],
        )
        self.assertEqual(
            manifest["cm13_family_required_values"],
            ["decision_authority_shift:toward_foundation"],
        )
        self.assertEqual(
            manifest["cm13_enabling_required_values"],
            [
                "newly_feasible_action_executed:yes",
            ],
        )
        self.assertEqual(
            manifest["cm13_suppressive_required_values"],
            [
                "autonomy_change:restricted",
            ],
        )
        self.assertEqual(
            manifest["maximum_local_release_baseline_families"],
            manifest["project_quarter_blocks"]
            * manifest["local_release_baseline_per_nonempty_project_quarter"],
        )
        self.assertEqual(manifest["rival_addressed_states"], ["contradicted"])
        self.assertEqual(
            manifest["rival_unaddressed_states"],
            [
                "supported",
                "compatible but not discriminated",
                "unassessable",
                "missing",
                "unresolved",
            ],
        )
        required_agreement_fields = {
            "eligible",
            "decision_right",
            "decision_authority_shift",
            "autonomy_change",
            "newly_feasible_action_executed",
            "coordination_disposition",
            "shared_commitment_named",
            "coordination_burden_change",
            "authority_outcome_link_met",
            "receiver_observed",
            "temporal_order",
            "channel",
            "effect_sign",
            "ordered_acts_met",
            "receiver_conduct_met",
            "linked_change_met",
            "discriminating_contrast_met",
            "qualified_witness",
        }
        self.assertEqual(
            set(manifest["audit_agreement_fields"]), required_agreement_fields
        )
        self.assertEqual(
            len(manifest["audit_agreement_fields"]), len(required_agreement_fields)
        )
        self.assertLessEqual(
            manifest["qualified_families_per_direction_required"],
            manifest["opportunity_families_per_direction_required"],
        )


if __name__ == "__main__":
    unittest.main()
