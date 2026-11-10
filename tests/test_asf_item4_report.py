"""Protect the item 4 stop against fabricated G3 results and lost denominators."""

from __future__ import annotations

import csv
import gzip
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.asf_audit.analysis import identifiability
from scripts.asf_audit.protocol import HORIZONS, digest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "research/data/asf-item4-audit-2026-11-10"
SPEC = importlib.util.spec_from_file_location(
    "asf_item4_report", PACKAGE / "generate.py"
)
assert SPEC is not None and SPEC.loader is not None
ADAPTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ADAPTER)


class Item4GateStopTests(unittest.TestCase):
    """Check ordered stops and the boundary between labels and causal decisions."""

    def test_g1_stop_does_not_measure_g2_or_g3(self) -> None:
        """Unreached gates must retain absent measurements instead of failures."""
        with (
            patch.object(ADAPTER, "access_gate", return_value={"pass": False}),
            patch.object(ADAPTER, "identifiability") as g2,
        ):
            result = ADAPTER.gate_path({})
        g2.assert_not_called()
        for horizon in result["horizons"].values():
            self.assertIsNone(horizon["G2"])
            self.assertEqual(horizon["stop_gate"], "G1")
            self.assertIsNone(horizon["G3"]["pass"])
            self.assertIsNone(horizon["G3"]["agreement"])

    def test_sensitivity_reaching_g3_refuses_stop_report(self) -> None:
        """A passing sensitivity cannot be hidden by the primary G2 failure."""
        with (
            patch.object(ADAPTER, "access_gate", return_value={"pass": True}),
            patch.object(ADAPTER, "horizon_rows", side_effect=lambda _, h: h),
            patch.object(
                ADAPTER,
                "identifiability",
                side_effect=lambda h, _: {"pass": h == max(HORIZONS)},
            ),
            self.assertRaisesRegex(ValueError, "G3 required at 180"),
        ):
            ADAPTER.gate_path({})

    def test_shared_family_keeps_unknown_project_in_denominator(self) -> None:
        """One observable response cannot stand in for a whole shared family."""
        known = {
            "record_id": "known",
            "family_id": "shared",
            "project": "ant",
            "horizon": "90",
            "direction": "C_to_A",
            "eligible": "yes",
            "opportunity": "yes",
            "receiver_observed": "known",
            "temporal_order": "sender_first",
            "within_day_order": "no",
            "sender_earliest": "2024-01-01",
            "sender_latest": "2024-01-01",
            "receiver_earliest": "2024-01-02",
            "receiver_latest": "2024-01-02",
        }
        unknown = known | {
            "record_id": "unknown",
            "project": "httpd",
            "receiver_observed": "unknown",
            "temporal_order": "unknown",
            "receiver_earliest": "unknown",
            "receiver_latest": "unknown",
        }
        rows = [known, unknown]
        with patch.object(ADAPTER, "horizon_rows", return_value=rows):
            observed = ADAPTER.observability({})
        measured = identifiability(rows, "C_to_A")
        self.assertEqual(measured["families"], 1)
        self.assertEqual(measured["classifiable"], 0)
        for row in observed:
            self.assertEqual(row["classifiable_all_projects"], "no")
            self.assertEqual(row["blocked_record_ids"], "unknown")
            self.assertEqual(row["project_records"], "2")

    def test_committed_report_preserves_stop_and_every_original_record(self) -> None:
        """Exports preserve the original rows, hashes, and frozen gate arithmetic."""
        output = PACKAGE / "outputs"
        manifest = json.loads((output / "manifest.json").read_text())
        for name, expected in manifest.items():
            self.assertEqual(digest((output / name).read_bytes()), expected, name)
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(
            report["reporting_adapter_sha256"],
            digest((PACKAGE / "generate.py").read_bytes()),
        )
        self.assertEqual(
            report["execution"], json.loads((PACKAGE / "execution.json").read_text())
        )
        self.assertEqual(report["required_pairs"], 491)
        self.assertTrue(report["integrity"]["pass"])
        for horizon in report["horizons"].values():
            self.assertEqual(horizon["stop_gate"], "G2")
            self.assertEqual(horizon["G3"]["status"], "not_reached")
            self.assertIsNone(horizon["G3"]["agreement"])
            self.assertIsNone(horizon["causal_category"])
            self.assertIsNone(horizon["nested_claim_comparison"])
        native = ROOT / "research/data/asf-item3-first-pass-2026-10-23/ledgers"
        original = read_gzip_csv(native / "measurements.csv.gz")
        exported = read_gzip_csv(output / "candidate-blockers.csv.gz")
        self.assertEqual(len(exported), len(original))
        self.assertEqual(
            {r["record_id"] for r in exported}, {r["record_id"] for r in original}
        )
        self.assertEqual(
            sum(r["g2_denominator_member"] == "yes" for r in exported),
            sum(r["eligible"] == r["opportunity"] == "yes" for r in original),
        )

    def test_exported_family_denominators_match_frozen_gate_results(self) -> None:
        """Descriptive exports must account for exactly the measured G2 families."""
        output = PACKAGE / "outputs"
        report = json.loads((output / "report.json").read_text())
        with (output / "family-observability.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        for horizon, result in report["horizons"].items():
            for direction, gate in result["G2"].items():
                selected = [
                    r
                    for r in rows
                    if r["horizon"] == horizon and r["direction"] == direction
                ]
                self.assertEqual(len(selected), gate["families"])
                self.assertEqual(
                    len({r["family_id"] for r in selected}), gate["families"]
                )
                self.assertEqual(
                    sum(r["classifiable_all_projects"] == "yes" for r in selected),
                    gate["classifiable"],
                )


def read_gzip_csv(path: Path) -> list[dict[str, str]]:
    """Read deterministic compressed research exports."""
    return list(
        csv.DictReader(io.StringIO(gzip.decompress(path.read_bytes()).decode()))
    )
