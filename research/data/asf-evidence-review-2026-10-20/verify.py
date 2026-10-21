"""Check review metadata and retained policy/source bytes without causal coding."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FRAME = REPOSITORY / "research/data/asf-release-frame-2026-10-20"


def read_json(path: Path):
    """Read retained JSON without modifying the source."""
    return json.loads(path.read_text())


def read_csv(path: Path):
    """Read original identifiers literally from CSV."""
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(path: Path) -> str:
    """Identify exact bytes, not the truth of their interpretation."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes() -> None:
    """Require every packaged file and declared accepted input to match."""
    manifest = read_json(ROOT / "manifest.json")
    for group, base in (("files", ROOT), ("accepted_inputs", REPOSITORY)):
        for name, sha in manifest[group].items():
            if digest(base / name) != sha:
                raise AssertionError(f"Changed retained file: {name}")


def reviewed_topics(records):
    """Include the separately declared, previously read closure topics."""
    topics = {t for record in records for t in record["opening_topic_ids"]}
    for field, name in (
        ("closure_candidate_ordinals", "closure-candidates.json"),
        ("closure_supplement_ordinals", "closure-supplement.json"),
    ):
        requested = {o for record in records for o in record[field]}
        actual = {r["ordinal"]: r for r in read_json(FRAME / name)}
        if not requested <= actual.keys():
            raise AssertionError("Unknown original closure ordinal")
        topics.update(actual[o]["topic_id"] for o in requested)
    return topics


def check_draw(records) -> None:
    """Reject a changed sample or a record attached to another opening."""
    selected = [r for r in read_csv(FRAME / "local-baseline.csv") if r["family_id"]]
    by_key = {(r["project"], r["quarter"]): r for r in records}
    if len(records) != len(by_key) or len(records) != len(selected):
        raise AssertionError("Duplicate or missing baseline review")
    for row in selected:
        record = by_key[row["project"], row["quarter"]]
        if (record["family_id"], record["formal_opening_source_id"]) != (
            row["family_id"],
            row["source_id"],
        ):
            raise AssertionError("Review differs from fixed draw")
        if not record["findings"].strip() or not record["review_scope"].strip():
            raise AssertionError("Review lacks an independent finding/scope")


def check_variants(records):
    """Re-extract declared original variants from accepted monthly exports."""
    spec = importlib.util.spec_from_file_location(
        "earlier_source_verifier",
        REPOSITORY / "research/data/asf-item3-screening-2026-10-04/verify.py",
    )
    assert spec and spec.loader
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    wanted = {v["source_id"] for record in records for v in record["reviewed_variants"]}
    actual = [
        r
        for r in verifier.message_variants(reviewed_topics(records))
        if r["source_id"] in wanted
    ]
    if actual != read_csv(ROOT / "reviewed-message-variants.csv"):
        raise AssertionError("Original export occurrence metadata differs")
    declared = {
        (r["project"], v["source_id"], v["raw_sha256"], v["body_sha256"])
        for r in records
        for v in r["reviewed_variants"]
    }
    observed = {
        (r["project"], r["source_id"], r["raw_sha256"], r["plain_body_sha256"])
        for r in actual
    }
    if declared != observed:
        raise AssertionError("Declared raw/plain-body variants differ")
    return actual


def check_policies() -> int:
    """Require exact files behind every dated interpretation and version receipt."""
    policy = ROOT / "policy"
    review = read_json(policy / "dated-policy-review.json")
    for finding in review["findings"]:
        for source in finding["files"]:
            if digest(policy / source["path"]) != source["sha256"]:
                raise AssertionError("Dated policy interpretation source changed")
    receipt = read_json(policy / "infra-service-versions.receipt.json")
    for source in receipt["records"]:
        if digest(policy / source["file"]) != source["sha256"]:
            raise AssertionError("Complete dated policy version changed")
    return len(receipt["records"])


def check_decoding(records) -> None:
    """Require the sole reading-aid decoding difference to remain explicit."""
    review = read_json(ROOT / "source-decoding-review.json")
    differences = {
        (
            v["source_id"],
            v["raw_sha256"],
            v["reading_aid_body_sha256"],
            v["body_sha256"],
        )
        for record in records
        for v in record["reviewed_variants"]
        if v["reading_aid_body_sha256"] != v["body_sha256"]
    }
    expected = {
        (
            review["source_id"],
            review["raw_sha256"],
            review["reading_aid_body_sha256"],
            review["frozen_parser_body_sha256"],
        )
    }
    if differences != expected:
        raise AssertionError("Undeclared reading-aid decoding difference")


def report():
    """Return source-review counts without gates, effects, or a lock timestamp."""
    check_hashes()
    records = read_json(ROOT / "baseline-evidence-review.json")["selected_families"]
    check_draw(records)
    check_decoding(records)
    variants = check_variants(records)
    policies = check_policies()
    return {
        "status": "evidence_review_integrity_only",
        "baseline_families": len(records),
        "reviewed_export_occurrences": len(variants),
        "reviewed_original_variants": len({r["raw_sha256"] for r in variants}),
        "complete_infra_policy_versions": policies,
        "first_pass_complete": False,
        "first_pass_locked_at": None,
    }


if __name__ == "__main__":
    result = report()
    if read_json(ROOT / "verification.json") != result:
        raise AssertionError("Saved verification report differs")
    print(json.dumps(result, indent=2, sort_keys=True))
