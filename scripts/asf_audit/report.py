"""Verify frozen audit artifacts before exposing aggregate claim decisions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.asf_audit.analysis import decision_report
from scripts.asf_audit.freeze import decode_recode, read_json, verify_lock
from scripts.asf_audit.protocol import RULES, digest, provenance
from scripts.asf_audit.sampling import audit_frame
from scripts.asf_audit.schema import SCHEMAS, load_tables, read_rows
from scripts.asf_audit.stability import (
    ADJUDICATION_COLUMNS,
    agreement,
    recode_errors,
    reconcile,
)
from scripts.asf_audit.timing import recode_not_before, timestamp
from scripts.asf_audit.validation import integrity_errors


def verified_score(
    target: Path, manifest: dict[str, Any], score_hash: str
) -> dict[str, Any]:
    """Recalculate agreement and verify the retained submission/start hashes."""
    if digest((target / "initial-score.json").read_bytes()) != score_hash:
        raise ValueError("Initial score differs from retained hash")
    score = read_json(target / "initial-score.json")
    start = read_json(target / "recode-start.json")
    expected_lock = digest((target / "lock.json").read_bytes())
    if (
        score["recode_sha256"] != digest((target / "submitted-recode.csv").read_bytes())
        or score["start_sha256"] != digest((target / "recode-start.json").read_bytes())
        or start["lock_sha256"] != expected_lock
        or not start["no_asf_evidence_work"]
        or timestamp(start["started_at"]) < recode_not_before(manifest["locked_at"])
        or timestamp(score["submitted_at"]) < timestamp(start["started_at"])
    ):
        raise ValueError("Recode provenance, chronology, or washout mismatch")
    rows = read_rows(target / "submitted-recode.csv", list(SCHEMAS["measurements"]))
    decoded = decode_recode(rows, manifest["record_mapping"])
    first = [
        row
        for row in load_tables(target / "first-pass")["measurements"]
        if row["record_id"] in manifest["record_mapping"].values()
    ]
    calculated = agreement(first, decoded)
    if any(score[key] != value for key, value in calculated.items()):
        raise ValueError("Initial agreement arithmetic mismatch")
    if score["recode_errors"] != recode_errors(first, decoded):
        raise ValueError("Recode integrity arithmetic mismatch")
    return score


def audited_report(target: Path, lock_hash: str, score_hash: str) -> dict[str, Any]:
    """Adjudicate only after locked recoding, initial scoring, and reconciliation."""
    manifest = verify_lock(target, lock_hash)
    score = verified_score(target, manifest, score_hash)
    original = load_tables(target / "first-pass")
    errors = integrity_errors(original, target / "first-pass")
    decisions = read_rows(target / "reconciliation.csv", ADJUDICATION_COLUMNS)
    recoded = decode_recode(
        read_rows(target / "submitted-recode.csv", list(SCHEMAS["measurements"])),
        manifest["record_mapping"],
    )
    final, reconciliation_errors = reconcile(original, score, decisions, recoded)
    errors.extend(reconciliation_errors)
    errors.extend(integrity_errors(final, target / "first-pass", audit_frame(original)))
    errors.extend(score["recode_errors"])
    errors.extend(manifest["integrity_errors_at_lock"])
    agreement_passes = (
        score["agreement"] is not None
        and score["agreement"] >= RULES["solo_recode_agreement_required"]
    )
    report = decision_report(final, agreement_passes and not errors)
    return {
        "provenance": provenance(),
        "lock_sha256": lock_hash,
        "initial_score_sha256": score_hash,
        "initial_agreement": score,
        "integrity_errors": sorted(set(errors)),
        "reconciliation_sha256": digest((target / "reconciliation.csv").read_bytes()),
        **report,
    }
