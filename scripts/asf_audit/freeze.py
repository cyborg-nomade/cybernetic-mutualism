"""Immutable local locks, blank blinded bundles, and single-attempt scoring."""

from __future__ import annotations

import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts.asf_audit.protocol import Row, Tables, canonical, digest, provenance
from scripts.asf_audit.sampling import audit_frame
from scripts.asf_audit.schema import SCHEMAS, load_tables, read_rows, write_rows
from scripts.asf_audit.stability import (
    ADJUDICATION_COLUMNS,
    agreement,
    recode_errors,
)
from scripts.asf_audit.timing import recode_not_before, timestamp
from scripts.asf_audit.validation import identifiers, integrity_errors, local_path


def file_hashes(directory: Path) -> dict[str, str]:
    """Hash every regular file under a snapshot, refusing symbolic links."""
    paths = sorted(directory.rglob("*"))
    if any(path.is_symlink() for path in paths):
        raise ValueError("Snapshot must not contain symbolic links")
    return {
        str(path.relative_to(directory)): digest(path.read_bytes())
        for path in paths
        if path.is_file()
    }


def read_json(path: Path) -> dict[str, Any]:
    """Read a JSON object from a local lifecycle artifact."""
    value: dict[str, Any] = json.loads(path.read_text())
    return value


def freeze_first_pass(directory: Path, target: Path, now: datetime) -> dict[str, Any]:
    """Freeze input, frame, and blank bundle together before any aggregation."""
    tables = load_tables(directory)
    errors = integrity_errors(tables, directory)
    frame = audit_frame(tables)
    if not frame:
        raise ValueError(
            "No eligible audit frame; report access failure without a recode"
        )
    if target.resolve().is_relative_to(directory.resolve()):
        raise ValueError("Lock directory must be outside the mutable dataset")
    target.mkdir(parents=True, exist_ok=False)
    frozen = target / "first-pass"
    frozen.mkdir()
    for name in SCHEMAS:
        shutil.copyfile(directory / f"{name}.csv", frozen / f"{name}.csv")
    for source in tables["sources"]:
        if source["content_path"]:
            output = local_path(frozen, source["content_path"])
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(local_path(directory, source["content_path"]), output)
    bundle = target / "blank-recode"
    bundle.mkdir()
    mapping = make_bundle(tables, frame, frozen, bundle)
    (target / "audit-frame.json").write_bytes(canonical(frame))
    manifest = {
        "locked_at": now.astimezone(UTC).isoformat(),
        "provenance": provenance(),
        "first_pass_files": file_hashes(frozen),
        "bundle_files": file_hashes(bundle),
        "audit_frame_sha256": digest((target / "audit-frame.json").read_bytes()),
        "record_mapping": mapping,
        "integrity_errors_at_lock": errors,
    }
    manifest["first_pass_sha256"] = digest(canonical(manifest["first_pass_files"]))
    (target / "lock.json").write_bytes(canonical(manifest))
    # Keep this digest externally (e.g. the evidence PR) before the washout.
    return {
        "lock_sha256": digest((target / "lock.json").read_bytes()),
        "first_pass_sha256": manifest["first_pass_sha256"],
        "audit_frame_sha256": manifest["audit_frame_sha256"],
        "recode_not_before": recode_not_before(str(manifest["locked_at"])).isoformat(),
        "integrity_errors": errors,
    }


def make_bundle(
    tables: Tables, frame: list[str], frozen: Path, bundle: Path
) -> dict[str, str]:
    """Whitelist only source bytes, neutral IDs, and entirely blank coding fields."""
    mapping: dict[str, str] = {}
    rows = []
    for family in frame:
        selected = sorted(
            (row for row in tables["measurements"] if row["family_id"] == family),
            key=lambda row: digest(row["record_id"].encode()),
        )
        for row in selected:
            opaque = digest(row["record_id"].encode())
            mapping[opaque] = row["record_id"]
            blank = dict.fromkeys(SCHEMAS["measurements"], "")
            blank.update(
                record_id=opaque,
                family_id=family,
                project=row["project"],
                horizon=row["horizon"],
                direction=row["direction"],
            )
            rows.append(blank)
    write_rows(bundle / "recode.csv", list(SCHEMAS["measurements"]), rows)
    bundle_sources(tables, frame, frozen, bundle)
    return mapping


def bundle_sources(
    tables: Tables, frame: list[str], frozen: Path, bundle: Path
) -> None:
    """Include the complete family source bundle with no first-pass annotations."""
    sources = {row["source_id"]: row for row in tables["sources"]}
    rows = []
    for family in tables["families"]:
        if family["family_id"] not in frame:
            continue
        for source_id in identifiers(family["source_ids"]):
            source = sources[source_id]
            filename = ""
            if source["content_path"]:
                filename = f"source-{digest(source_id.encode())}.bin"
                shutil.copyfile(
                    local_path(frozen, source["content_path"]), bundle / filename
                )
            rows.append(
                {
                    "family_id": family["family_id"],
                    "project": family["project"],
                    "source_id": source_id,
                    "url": source["url"],
                    "locator": source["locator"],
                    "file": filename,
                }
            )
    write_rows(
        bundle / "sources.csv",
        ["family_id", "project", "source_id", "url", "locator", "file"],
        rows,
    )


def verify_lock(target: Path, expected_hash: str) -> dict[str, Any]:
    """Verify an externally retained lock hash and every frozen component."""
    if digest((target / "lock.json").read_bytes()) != expected_hash:
        raise ValueError("Lock manifest differs from the retained digest")
    manifest = read_json(target / "lock.json")
    checks = (
        (manifest["first_pass_files"], file_hashes(target / "first-pass")),
        (manifest["bundle_files"], file_hashes(target / "blank-recode")),
        (
            manifest["audit_frame_sha256"],
            digest((target / "audit-frame.json").read_bytes()),
        ),
        (manifest["provenance"], provenance()),
    )
    if any(left != right for left, right in checks):
        raise ValueError(
            "Frozen input, bundle, frame, protocol, or executable has changed"
        )
    tables = load_tables(target / "first-pass")
    if json.loads((target / "audit-frame.json").read_text()) != audit_frame(tables):
        raise ValueError("Audit membership differs from deterministic selection")
    return manifest


def begin_recode(
    target: Path, expected_hash: str, now: datetime, no_evidence_work: bool
) -> None:
    """Record recode start once after complete-day washout and explicit attestation."""
    manifest = verify_lock(target, expected_hash)
    if (
        now.astimezone(UTC) < recode_not_before(manifest["locked_at"])
        or not no_evidence_work
    ):
        raise ValueError(
            "Recode requires full washout and no-ASF-evidence-work attestation"
        )
    start = {
        "started_at": now.astimezone(UTC).isoformat(),
        "lock_sha256": expected_hash,
        "no_asf_evidence_work": no_evidence_work,
    }
    with (target / "recode-start.json").open("xb") as stream:
        stream.write(canonical(start))


def decode_recode(rows: list[Row], mapping: dict[str, str]) -> list[Row]:
    """Restore original IDs only after the blind recode is submitted."""
    return [
        row
        | {"record_id": mapping.get(row["record_id"], "unexpected:" + row["record_id"])}
        for row in rows
    ]


def submit_recode(
    target: Path, recode: Path, expected_hash: str, now: datetime
) -> dict[str, Any]:
    """Lock and score the initial recode exactly once, preserving missing fields."""
    manifest = verify_lock(target, expected_hash)
    start = read_json(target / "recode-start.json")
    if (
        start["lock_sha256"] != expected_hash
        or not start["no_asf_evidence_work"]
        or timestamp(start["started_at"]) < recode_not_before(manifest["locked_at"])
        or now.astimezone(UTC) < timestamp(start["started_at"])
    ):
        raise ValueError("Invalid recode start or chronology")
    rows = read_rows(recode, list(SCHEMAS["measurements"]))
    decoded = decode_recode(rows, manifest["record_mapping"])
    first = [
        row
        for row in load_tables(target / "first-pass")["measurements"]
        if row["record_id"] in manifest["record_mapping"].values()
    ]
    score = agreement(first, decoded)
    score.update(
        recode_errors=recode_errors(first, decoded),
        submitted_at=now.astimezone(UTC).isoformat(),
        recode_sha256=digest(recode.read_bytes()),
        start_sha256=digest((target / "recode-start.json").read_bytes()),
    )
    # The exclusive submission file is the attempt boundary, even if later output fails.
    with (target / "submitted-recode.csv").open("xb") as stream:
        stream.write(recode.read_bytes())
    (target / "initial-score.json").write_bytes(canonical(score))
    resolutions = [
        dict.fromkeys(ADJUDICATION_COLUMNS, "") | item
        for item in score["disagreements"]
    ]
    write_rows(target / "reconciliation.csv", ADJUDICATION_COLUMNS, resolutions)
    return {
        "score_sha256": digest((target / "initial-score.json").read_bytes()),
        **score,
    }
