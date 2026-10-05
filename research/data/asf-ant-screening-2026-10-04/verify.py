"""Verify a bounded Ant review continuation without sampling or gate decisions."""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
from collections import Counter
from datetime import UTC
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
PREVIOUS = REPOSITORY / "research/data/asf-first-pass-2026-09-22"
IDENTITY_FIELDS = (
    "project",
    "source_id",
    "archive_id",
    "url",
    "index_timestamp",
    "month",
    "subject",
    "topic_id",
)


def rows(path: Path) -> list[dict[str, str]]:
    """Read retained UTF-8 metadata, preserving literal original identifiers."""
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(data: bytes) -> str:
    """Hash exact retained bytes."""
    return hashlib.sha256(data).hexdigest()


def check_occurrences(
    expected: list[dict[str, str]], actual: list[dict[str, str]]
) -> None:
    """Reject missing, repeated, or edited index occurrences."""
    expected_keys = Counter(tuple(r[f] for f in IDENTITY_FIELDS) for r in expected)
    actual_keys = Counter(tuple(r[f] for f in IDENTITY_FIELDS) for r in actual)
    if actual_keys != expected_keys:
        raise AssertionError("Ant occurrence membership or index fields changed")
    if any(not r["reason"] or not r["review_scope"] for r in actual):
        raise AssertionError("Subject-screen decision lacks a reason or scope")


def check_hashes(manifest: dict[str, object]) -> None:
    """Check both new files and the specific accepted inputs they reference."""
    for group, base in (("files", ROOT), ("accepted_inputs", REPOSITORY)):
        values = manifest[group]
        if not isinstance(values, dict):
            raise AssertionError("Invalid hash manifest")
        for name, sha in values.items():
            if digest((base / name).read_bytes()) != sha:
                raise AssertionError(f"Retained bytes changed: {name}")


def message_details(raw: bytes) -> dict[str, str]:
    """Recompute hashes and event-header metadata from an exact export block."""
    message = BytesParser(policy=policy.default).parsebytes(raw)
    part = message.get_body(preferencelist=("plain",))
    body = part.get_content() if part else ""
    if not isinstance(body, str):
        raise AssertionError("Expected a decoded plain-text body")
    return {
        "source_id": str(message.get("Message-ID", "")).strip(),
        "raw_sha256": digest(raw),
        "plain_body_sha256": digest(body.encode("utf-8")),
        "date_header": str(message.get("Date", "")),
    }


def check_messages(reviewed: list[dict[str, str]], index: list[dict[str, str]]) -> None:
    """Require complete indexed membership for every newly body-reviewed topic."""
    topics = {r["topic_id"] for r in rows(ROOT / "topic-review.csv")}
    keys = ("project", "source_id", "topic_id", "url")
    expected = Counter(
        tuple(r[k] for k in keys) for r in index if r["topic_id"] in topics
    )
    if expected != Counter(tuple(r[k] for k in keys) for r in reviewed):
        raise AssertionError("Reviewed topic has missing or extra message bodies")
    exports = {}
    for row in reviewed:
        path = row["export_path"]
        if path not in exports:
            exports[path] = re.split(
                rb"(?m)^From [^\n]*\n",
                gzip.decompress((REPOSITORY / path).read_bytes()),
            )[1:]
        details = message_details(exports[path][int(row["block_number"]) - 1])
        if any(row[key] != value for key, value in details.items()):
            raise AssertionError(f"Reviewed message bytes changed: {row['source_id']}")


def check_topics(index: list[dict[str, str]]) -> None:
    """Keep accepted navigation fields unchanged; never treat topics as families."""
    previous = {r["topic_id"]: r for r in rows(PREVIOUS / "subject-review.csv")}
    for row in rows(ROOT / "topic-review.csv"):
        original = previous[row["topic_id"]]
        for key in ("project", "first_date", "subject", "message_count"):
            if row[key] != original[key]:
                raise AssertionError("Accepted topic navigation fields changed")
    check_messages(rows(ROOT / "reviewed-messages.csv"), index)


def check_families(index: list[dict[str, str]]) -> None:
    """Check release links and formal dates, preserving the undrawn sample."""
    known_topics = {r["topic_id"] for r in index}
    reviewed = {r["source_id"]: r for r in rows(ROOT / "reviewed-messages.csv")}
    families = rows(ROOT / "release-families.csv")
    openings = [r["formal_opening_source_id"] for r in families]
    if len(set(openings)) != len(openings):
        raise AssertionError("Release families duplicate a formal opening")
    for row in families:
        check_family(row, reviewed, known_topics)


def check_family(
    row: dict[str, str],
    reviewed: dict[str, dict[str, str]],
    known_topics: set[str],
) -> None:
    """Validate one provisional family without adjudicating its interpretation."""
    source = reviewed[row["formal_opening_source_id"]]
    date = parsedate_to_datetime(source["date_header"]).astimezone(UTC).date()
    if date.isoformat() != row["formal_opening_date"]:
        raise AssertionError("Formal date differs from original message header")
    members = set(row["member_topic_ids"].split(";"))
    context = set(row["context_topic_ids"].split(";"))
    if not (members | context) <= known_topics:
        raise AssertionError("Family links an unknown Ant topic")
    if source["topic_id"] != row["formal_opening_topic_id"]:
        raise AssertionError("Formal opening source and topic disagree")
    if source["topic_id"] not in members or row["sample_selected"] != "no":
        raise AssertionError("Opening not linked or sample prematurely selected")


def check_board_sections() -> None:
    """Verify bounded agenda locators without claiming full minutes review."""
    for row in rows(ROOT / "reviewed-board-sections.csv"):
        lines = (REPOSITORY / row["source_path"]).read_text("utf-8").splitlines()
        section = lines[int(row["start_line"]) - 1 : int(row["end_line"])]
        if section[0].strip() != row["locator"]:
            raise AssertionError("Board agenda locator changed")
        if "No report was submitted." not in "\n".join(section):
            raise AssertionError("Non-submission is not explicit in agenda section")


def report() -> dict[str, object]:
    """Report declared review progress, with every later registered step open."""
    manifest = json.loads((ROOT / "checkpoint.json").read_text("utf-8"))
    if (
        manifest["status"] != "incomplete"
        or manifest["baseline_selected"]
        or manifest["first_pass_locked_at"] is not None
    ):
        raise AssertionError("This continuation cannot assert sampling or a lock")
    check_hashes(manifest)
    expected = [
        r for r in rows(PREVIOUS / "message-index.csv") if r["project"] == "ant"
    ]
    screened = rows(ROOT / "ant-subject-screen.csv")
    check_occurrences(expected, screened)
    check_topics(expected)
    check_families(expected)
    check_board_sections()
    return {
        "status": "incomplete",
        "scope": "Ant continuation integrity; not a complete census or gate decision",
        "ant_subject_occurrences_screened": len(screened),
        "new_body_reviewed_topics": len(rows(ROOT / "topic-review.csv")),
        "new_body_reviewed_messages": len(rows(ROOT / "reviewed-messages.csv")),
        "new_board_agenda_sections": len(rows(ROOT / "reviewed-board-sections.csv")),
        "provisional_release_families": len(rows(ROOT / "release-families.csv")),
        "classification_counts": dict(
            sorted(Counter(r["classification"] for r in screened).items())
        ),
        "baseline_selected": False,
        "first_pass_locked_at": None,
    }


def main() -> None:
    """Fail on stale saved output before printing a successful integrity report."""
    computed = report()
    saved = json.loads((ROOT / "verification.json").read_text("utf-8"))
    if saved != computed:
        raise AssertionError("Saved verification report differs from recomputation")
    print(json.dumps(computed, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
