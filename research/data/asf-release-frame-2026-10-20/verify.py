"""Verify release-frame identities and reproduce the frozen baseline draw.

This checks retained bytes and declared identity judgments. It cannot make
historical authority/publication judgments, code causal effects, or lock item3.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from datetime import UTC
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
STRATA = 48
sys.path.insert(0, str(REPOSITORY))
from scripts.asf_audit.sampling import local_baseline  # noqa: E402


def digest(path: Path) -> str:
    """Hash exact retained bytes without interpreting their contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    """Read CSV metadata without changing original identifiers."""
    with (ROOT / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def check_hashes() -> None:
    """Verify retained outputs and accepted input bytes."""
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for group, base in (("files", ROOT), ("accepted_inputs", REPOSITORY)):
        for name, sha in manifest[group].items():
            if digest(base / name) != sha:
                raise AssertionError(f"Changed retained file: {name}")


def candidates():
    """Require candidate/review original-identity membership."""
    frame = json.loads((ROOT / "opening-candidates.json").read_text())
    reviews = json.loads((ROOT / "opening-review.json").read_text())
    if len({(r["project"], r["source_id"]) for r in frame}) != len(frame):
        raise AssertionError("Repeated project/original opening candidate")
    if {r["source_id"] for r in frame} != set(reviews):
        raise AssertionError("Candidate/review membership differs")

    return frame, reviews


def source_inventory(frame):
    """Reconstruct opening, closure and bounded-reference source variants."""
    spec = importlib.util.spec_from_file_location(
        "prior_source_verifier",
        REPOSITORY / "research/data/asf-item3-screening-2026-10-04/verify.py",
    )
    assert spec and spec.loader
    source_verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_verifier)
    related = [
        r
        for name in (
            "closure-candidates.json",
            "closure-supplement.json",
            "opening-exceptions.json",
        )
        for r in json.loads((ROOT / name).read_text())
    ]
    support = json.loads((ROOT / "identity-support.json").read_text())
    topics = {t for r in frame for t in r["topic_ids"]}
    topics.update(r["topic_id"] for r in related)
    topics.update(support["topic_ids"])
    actual = source_verifier.message_variants(topics)
    by_original: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for r in actual:
        by_original[r["project"], r["source_id"]].append(r)
    for r in related:
        observed = by_original[r["project"], r["source_id"]]
        if not any(
            (v["raw_sha256"], v["plain_body_sha256"])
            == (r["raw_sha256"], r["body_sha256"])
            for v in observed
        ):
            raise AssertionError("Closure/exception original-byte membership differs")
    expected_support = source_verifier.message_variants(set(support["topic_ids"]))
    if support["variants"] != expected_support:
        raise AssertionError("Bounded identity-support source variants differ")
    return by_original


def check_opening(r, review, original) -> None:
    """Match one reviewed opening to its exact original export variants."""
    expected = {(v["raw_sha256"], v["body_sha256"]) for v in r["variants"]}
    observed = {(v["raw_sha256"], v["plain_body_sha256"]) for v in original}
    if observed != expected:
        raise AssertionError("Opening original raw/body variants differ")
    if (review["project"], review["ordinal"]) != (r["project"], r["ordinal"]):
        raise AssertionError("Opening judgment attached to another original")
    if not review["reason"] or not review["review_scope"]:
        raise AssertionError("Opening judgment lacks reason/scope")


def family_inventory(frame, reviews):
    """Require every formal original and reject dangling family associations."""
    families = rows("release-family-frame.csv")
    associations = rows("opening-family-associations.csv")
    if len({r["family_id"] for r in families}) != len(families):
        raise AssertionError("Repeated canonical release family")
    valid = {
        (r["project"], r["source_id"]): r
        for r in frame
        if reviews[r["source_id"]]["formal_release_opening"]
    }
    if {(r["project"], r["source_id"]) for r in associations} != set(valid):
        raise AssertionError("Formal opening missing or excluded message promoted")
    association_keys = [
        (r["project"], r["source_id"], r["family_id"]) for r in associations
    ]
    if len(set(association_keys)) != len(association_keys):
        raise AssertionError("Duplicate source/family association")
    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in associations:
        by_family[r["family_id"]].append(r)
    if set(by_family) != {r["family_id"] for r in families}:
        raise AssertionError("Dangling family association")
    return families, valid, by_family


def check_family(r, members, valid) -> None:
    """Reject a reset onset or an opening from another project."""
    first = min(
        (valid[m["project"], m["source_id"]] for m in members),
        key=lambda candidate: (
            parsedate_to_datetime(
                candidate["variants"][0]["headers"]["Date"]
            ).astimezone(UTC),
            candidate["source_id"],
        ),
    )
    when = (
        parsedate_to_datetime(first["variants"][0]["headers"]["Date"])
        .astimezone(UTC)
        .date()
        .isoformat()
    )
    if (r["source_id"], r["opening_date"]) != (first["source_id"], when):
        raise AssertionError("Family onset reset to a later retry")
    if any(m["project"] != r["project"] for m in members):
        raise AssertionError("Routine baseline family crosses projects")
    if not r["identity_reason"] or r["eligible"] != "yes":
        raise AssertionError("Canonical family lacks frame eligibility reason")


def check_draw(families):
    """Reproduce all strata and check the receipt against packaged bytes."""
    baseline = local_baseline({"screening": families})
    if baseline != rows("local-baseline.csv") or len(baseline) != STRATA:
        raise AssertionError("Saved baseline differs from frozen sampling rule")
    receipt = json.loads((ROOT / "draw-receipt.json").read_text())
    if receipt["status"] != "frame_draw_only_not_first_pass_lock":
        raise AssertionError("Frame receipt cannot claim first-pass lock")
    for field in ("inputs", "outputs"):
        for name, sha in receipt[field].items():
            if digest(ROOT / name) != sha:
                raise AssertionError("Draw receipt differs from retained frame bytes")
    return baseline


def report() -> dict[str, object]:
    """Report only source/frame verification, never first-pass completeness."""
    check_hashes()
    frame, reviews = candidates()
    inventory = source_inventory(frame)
    for r in frame:
        check_opening(
            r, reviews[r["source_id"]], inventory[r["project"], r["source_id"]]
        )
    families, valid, by_family = family_inventory(frame, reviews)
    for r in families:
        check_family(r, by_family[r["family_id"]], valid)
    baseline = check_draw(families)
    return {
        "status": "verified_release_frame_only",
        "candidate_originals": len(frame),
        "formal_opening_originals": len(valid),
        "canonical_release_families": len(families),
        "families_by_project": dict(
            sorted(Counter(r["project"] for r in families).items())
        ),
        "strata": len(baseline),
        "selected_nonempty_strata": sum(bool(r["source_id"]) for r in baseline),
        "first_pass_locked_at": None,
        "publication_and_authority_verification_complete": False,
    }


if __name__ == "__main__":
    result = report()
    if result != json.loads((ROOT / "verification.json").read_text()):
        raise AssertionError("Saved frame verification differs")
    print(json.dumps(result, indent=2, sort_keys=True))
