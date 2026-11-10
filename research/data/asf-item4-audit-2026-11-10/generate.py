"""Reproduce the registered G1/G2 stop and descriptive products, without G3.

This reporting adapter calls the frozen gate and integrity implementation. It
refuses to substitute a failed or fabricated recode for an unreached G3.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import runpy
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from scripts.asf_audit.analysis import access_gate, horizon_rows, identifiability
from scripts.asf_audit.freeze import make_bundle, read_json, verify_lock
from scripts.asf_audit.protocol import (
    AGREEMENT_FIELDS,
    CONDITIONS,
    DIRECTIONS,
    HORIZONS,
    RULES,
    Row,
    Tables,
    canonical,
    digest,
    provenance,
)
from scripts.asf_audit.sampling import (
    analysis_pairs,
    audit_frame,
    eligible_pairs,
    local_baseline,
)
from scripts.asf_audit.schema import load_tables
from scripts.asf_audit.timing import horizon_result
from scripts.asf_audit.validation import integrity_errors

PACKAGE = Path(__file__).resolve().parent
FIRST_PASS = PACKAGE.parent / "asf-item3-first-pass-2026-10-23"
LOCK_HASH = "2c5bf03e56aeb8cea66879f82acef46a6ecef05511e23d74a24451da712a4cb7"
FROZEN_COMMIT = "18b13ff18500c33d8812459eda72ad6c11640f1a"
SUMMARY_FIELDS = (
    "direction",
    "effect_sign",
    "decision_authority_shift",
    "coordination_disposition",
)


def restore_lock(target: Path) -> dict[str, Any]:
    """Reconstruct original bytes and the blank bundle; never create a new lock."""
    target.mkdir()
    verifier = runpy.run_path(str(FIRST_PASS / "verify.py"))
    verifier["verify"](target / "first-pass")
    for name in ("lock.json", "audit-frame.json"):
        shutil.copyfile(FIRST_PASS / name, target / name)
    tables = load_tables(target / "first-pass")
    bundle = target / "blank-recode"
    bundle.mkdir()
    mapping = make_bundle(
        tables, read_json(target / "audit-frame.json"), target / "first-pass", bundle
    )
    manifest = verify_lock(target, LOCK_HASH)
    if mapping != manifest["record_mapping"]:
        raise ValueError("Restored neutral mapping differs from original lock")
    return manifest


def gate_path(tables: Tables) -> dict[str, Any]:
    """Apply G1 then G2; refuse this stop-only report if any horizon reaches G3."""
    g1 = access_gate(tables)
    horizons: dict[str, Any] = {}
    for horizon in (90, 60, 180):
        g2 = (
            {
                direction: identifiability(horizon_rows(tables, horizon), direction)
                for direction in DIRECTIONS
            }
            if g1["pass"]
            else None
        )
        if g2 is not None and all(result["pass"] for result in g2.values()):
            raise ValueError(f"G3 required at {horizon} days; stop report refused")
        horizons[str(horizon)] = {
            "G2": g2,
            "stop_gate": "G2" if g1["pass"] else "G1",
            "G3": {"status": "not_reached", "pass": None, "agreement": None},
            "causal_category": None,
            "nested_claim_comparison": None,
            "decision": "registered_stop",
        }
    return {"G1": g1, "horizons": horizons}


def g2_blockers(row: Row) -> list[str]:
    """Explain the frozen observability conjunction, without changing its rule."""
    reasons = []
    if row["receiver_observed"] != "known":
        reasons.append("receiver_not_known")
    if row["temporal_order"] == "unknown":
        reasons.append("temporal_order_unknown")
    status = horizon_result(row)["status"]
    if status not in ("within", "reversed"):
        reasons.append(f"horizon_status_{status}")
    return reasons


def observability(tables: Tables) -> list[Row]:
    """Retain every G2 family and all its eligible project responses."""
    result = []
    for horizon in HORIZONS:
        groups: dict[tuple[str, str], list[Row]] = defaultdict(list)
        for row in horizon_rows(tables, horizon):
            if row["eligible"] == row["opportunity"] == "yes":
                groups[row["direction"], row["family_id"]].append(row)
        for (direction, family), rows in sorted(groups.items()):
            blocked = [row for row in rows if g2_blockers(row)]
            result.append(
                {
                    "horizon": str(horizon),
                    "direction": direction,
                    "family_id": family,
                    "projects": ";".join(sorted({r["project"] for r in rows})),
                    "project_records": str(len(rows)),
                    "classifiable_all_projects": "no" if blocked else "yes",
                    "blocked_record_ids": ";".join(r["record_id"] for r in blocked),
                    "blockers": ";".join(
                        sorted({b for row in blocked for b in g2_blockers(row)})
                    ),
                }
            )
    return result


def descriptive_counts(tables: Tables) -> list[Row]:
    """Tabulate recorded labels; audit supplements remain a separate scope."""
    pairs = analysis_pairs(tables)
    groups: dict[tuple[str, ...], list[Row]] = defaultdict(list)
    for row in tables["measurements"]:
        scope = (
            "analysis"
            if (row["family_id"], row["project"]) in pairs
            else "audit_supplement"
        )
        key = (scope, row["horizon"], *(row[field] for field in SUMMARY_FIELDS))
        groups[key].append(row)
    return [
        dict(zip(("scope", "horizon", *SUMMARY_FIELDS), key, strict=True))
        | {
            "project_records": str(len(rows)),
            "distinct_families": str(len({r["family_id"] for r in rows})),
            "distinct_family_project_pairs": str(
                len({(r["family_id"], r["project"]) for r in rows})
            ),
        }
        for key, rows in sorted(groups.items())
    ]


def measurement_blockers(tables: Tables) -> list[Row]:
    """Expose recorded failures/unknowns for every row; do not adjudicate claims."""
    pairs = analysis_pairs(tables)
    rivals: dict[str, list[Row]] = defaultdict(list)
    for rival in tables["rivals"]:
        rivals[rival["record_id"]].append(rival)
    return [
        {
            **{
                field: row[field]
                for field in (
                    "record_id",
                    "family_id",
                    "project",
                    "direction",
                    "horizon",
                    "eligible",
                    "opportunity",
                    "missingness",
                    "receiver_observed",
                    "temporal_order",
                    "qualified_witness",
                )
            },
            "scope": "analysis"
            if (row["family_id"], row["project"]) in pairs
            else "audit_supplement",
            "g2_blockers": ";".join(g2_blockers(row)),
            "g2_denominator_member": "yes"
            if (row["family_id"], row["project"]) in pairs
            and row["eligible"] == row["opportunity"] == "yes"
            else "no",
            "unknown_agreement_fields": ";".join(
                field for field in AGREEMENT_FIELDS if row[field] == "unknown"
            ),
            "conditions_not_met": ";".join(
                f"{field}:{row[field]}" for field in CONDITIONS if row[field] != "yes"
            ),
            "rival_states": ";".join(
                f"{r['rival']}:{r['state']}" for r in rivals[row["record_id"]]
            ),
        }
        for row in tables["measurements"]
    ]


def missingness(tables: Tables) -> list[Row]:
    """Keep denominators explicit for analysis rows and G2 opportunity rows."""
    result = []
    for horizon in HORIZONS:
        for direction in DIRECTIONS:
            rows = [
                r for r in horizon_rows(tables, horizon) if r["direction"] == direction
            ]
            for scope, selected in (
                ("analysis_all", rows),
                (
                    "analysis_g2_opportunities",
                    [r for r in rows if r["eligible"] == r["opportunity"] == "yes"],
                ),
            ):
                result.extend(field_counts(selected, scope, horizon, direction))
    return result


def field_counts(
    rows: list[Row], scope: str, horizon: int, direction: str
) -> list[Row]:
    """Describe field values including unknowns, without a recode score."""
    fields = (*AGREEMENT_FIELDS, "missingness", "opportunity")
    return [
        {
            "scope": scope,
            "horizon": str(horizon),
            "direction": direction,
            "field": field,
            "value": value,
            "project_records": str(count),
            "denominator_project_records": str(len(rows)),
        }
        for field in fields
        for value, count in sorted(Counter(r[field] for r in rows).items())
    ]


def claim_consequences(path: dict[str, Any]) -> dict[str, Any]:
    """State only the registered consequences of the actually reached stop."""
    mapping = "narrow" if path["G1"]["pass"] else "withhold"
    return {
        "CM-01": {"confidence": "C1", "causal_direction": None},
        "CM-12": {"confidence": "C1", "causal_direction": None},
        "CM-13": {"confidence": "C1", "causal_direction": None},
        "CM-04": {
            "confidence": "C1",
            "observational_mapping": mapping,
            "numerical_model_validated": False,
        },
        "other_claims": "unchanged",
    }


def write_csv(target: Path, rows: list[Row]) -> None:
    """Write deterministic CSV bytes, optionally with zero-time gzip."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    raw = buffer.getvalue().encode()
    target.write_bytes(gzip.compress(raw, mtime=0) if target.suffix == ".gz" else raw)


def build_report(tables: Tables, manifest: dict[str, Any], errors: list[str]) -> dict:
    """Distinguish executable integrity from an unreached interpretive audit."""
    path = gate_path(tables)
    return {
        "report_type": "registered_gate_stop",
        "frozen_implementation_commit": FROZEN_COMMIT,
        "provenance": provenance(),
        "reporting_adapter_sha256": digest(Path(__file__).read_bytes()),
        "lock_sha256": LOCK_HASH,
        "first_pass_sha256": manifest["first_pass_sha256"],
        "audit_frame_sha256": manifest["audit_frame_sha256"],
        "execution": read_json(PACKAGE / "execution.json"),
        "integrity": {
            "errors": errors,
            "pass": not errors,
            "original_lock_errors": manifest["integrity_errors_at_lock"],
            "package_native_and_blank_reconstruction_pass": True,
            "records_checked": len(tables["measurements"]),
            "source_records_checked": len(tables["sources"]),
        },
        **path,
        "primary_horizon": 90,
        "sensitivity_horizons": [60, 180],
        "gate_stop_timing_sensitive": False,
        "causal_category_timing_sensitivity": None,
        "claim_consequences": claim_consequences(path),
        "native_table_rows": {name: len(rows) for name, rows in tables.items()},
        "analysis_pairs": len(analysis_pairs(tables)),
        "eligible_screening_pairs": len(eligible_pairs(tables)),
        "required_pairs": len(
            analysis_pairs(tables)
            | {
                pair
                for pair in eligible_pairs(tables)
                if pair[0] in audit_frame(tables)
            }
        ),
        "thresholds": {
            key: RULES[key]
            for key in (
                "opportunity_families_per_direction_required",
                "projects_per_direction_required",
                "classifiable_opportunity_fraction_required",
            )
        },
    }


def generate(output: Path) -> None:
    """Reconstruct, audit, apply ordered gates, then export descriptive products."""
    output.mkdir(parents=True, exist_ok=False)
    with TemporaryDirectory(prefix="asf-item4-") as temporary:
        target = Path(temporary) / "restored-lock"
        manifest = restore_lock(target)
        tables = load_tables(target / "first-pass")
        errors = integrity_errors(
            tables, target / "first-pass", read_json(target / "audit-frame.json")
        )
        report = build_report(tables, manifest, errors)
        (output / "report.json").write_bytes(canonical(report))
        export_products(output, tables)
    hashes = {p.name: digest(p.read_bytes()) for p in sorted(output.iterdir())}
    (output / "manifest.json").write_bytes(canonical(hashes))


def export_products(output: Path, tables: Tables) -> None:
    """Publish the four registered reusable products with original identifiers."""
    products = {
        "source-access.csv": tables["coverage"],
        "screened-inventory.csv.gz": tables["screening"],
        "family-inventory.csv.gz": tables["families"],
        "local-baseline.csv": local_baseline(tables),
        "recorded-label-counts.csv": descriptive_counts(tables),
        "candidate-blockers.csv.gz": measurement_blockers(tables),
        "family-observability.csv": observability(tables),
        "field-missingness.csv": missingness(tables),
    }
    for name, rows in products.items():
        write_csv(output / name, rows)


def main() -> None:
    """Require a new output directory for reproducible report generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
