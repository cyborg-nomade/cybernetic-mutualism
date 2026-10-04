"""Check retained screening judgments against the accepted source bytes.

This evidence-preparation check is separate from the frozen registered audit.
It cannot attest corpus completion, draw a baseline, code a gate, or lock data.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
from collections import Counter
from email import policy
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
PREVIOUS = REPOSITORY / "research/data/asf-first-pass-2026-09-22"
ACCESS = REPOSITORY / "research/data/asf-access-2026-09-21"
VARIANT_FIELDS = (
    "project",
    "month",
    "source_id",
    "export_path",
    "block_number",
    "raw_sha256",
    "plain_body_sha256",
    "date_header",
)


def rows(path: Path) -> list[dict[str, str]]:
    """Read UTF-8 metadata without changing original identifiers."""
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def digest(data: bytes) -> str:
    """Identify exact bytes, without interpreting the digest as evidence."""
    return hashlib.sha256(data).hexdigest()


def message_variants(topics: set[str]) -> list[dict[str, str]]:
    """Reconstruct every export variant for the explicitly reviewed topics.

    Original IDs can occur twice in an index. Match against a set of original
    IDs per monthly export, rather than multiplying index occurrences by raw
    variants. Preserve every export block, including changed plain bodies.
    """
    wanted: dict[tuple[str, str], set[str]] = {}
    for row in rows(PREVIOUS / "message-index.csv"):
        if row["topic_id"] in topics:
            wanted.setdefault((row["project"], row["month"]), set()).add(
                row["source_id"]
            )
    result = []
    for (project, month), identities in sorted(wanted.items()):
        path = ACCESS / "sources" / f"{project}-{month}.mbox.gz"
        blocks = re.split(rb"(?m)^From [^\n]*\n", gzip.decompress(path.read_bytes()))[
            1:
        ]
        found = set()
        for number, raw in enumerate(blocks, 1):
            message = BytesParser(policy=policy.default).parsebytes(raw)
            source_id = str(message.get("Message-ID", "")).strip()
            if source_id not in identities:
                continue
            found.add(source_id)
            part = message.get_body(preferencelist=("plain",))
            body = part.get_content() if part else ""
            if not isinstance(body, str):
                raise AssertionError("Expected decoded plain text")
            result.append(
                {
                    "project": project,
                    "month": month,
                    "source_id": source_id,
                    "export_path": str(path.relative_to(REPOSITORY)),
                    "block_number": str(number),
                    "raw_sha256": digest(raw),
                    "plain_body_sha256": digest(body.encode("utf-8")),
                    "date_header": str(message.get("Date", "")),
                }
            )
        if found != identities:
            raise AssertionError(f"Indexed original has no export block: {path}")
    return result


def check_messages() -> None:
    """Reject missing or additional variants, including duplicate deliveries."""
    topics = {row["topic_id"] for row in rows(ROOT / "topic-review.csv")}
    expected = message_variants(topics)
    actual = rows(ROOT / "reviewed-message-variants.csv")

    def key(row: dict[str, str]) -> tuple[str, ...]:
        return tuple(row[field] for field in VARIANT_FIELDS)

    if Counter(map(key, expected)) != Counter(map(key, actual)):
        raise AssertionError("Reviewed original-message/export membership changed")


def check_topics() -> None:
    """Preserve navigation while keeping provisional families separate."""
    previous = {r["topic_id"]: r for r in rows(PREVIOUS / "subject-review.csv")}
    actual = rows(ROOT / "topic-review.csv")
    if len({r["topic_id"] for r in actual}) != len(actual):
        raise AssertionError("Repeated topic review")
    for row in actual:
        original = previous[row["topic_id"]]
        for field in ("project", "first_date", "subject", "message_count"):
            if row[field] != original[field]:
                raise AssertionError("Accepted topic navigation changed")
        if row["kind"] not in {
            "cross_boundary",
            "ambiguous",
            "local_other",
            "excluded",
        }:
            raise AssertionError("Unknown provisional screening kind")
        if not row["reason"] or row["review_scope"] != "full_exported_plain_bodies":
            raise AssertionError("Missing body-review reason or scope")


def check_titles() -> None:
    """Check title-inspection membership without promoting it to body review."""
    previous = {r["topic_id"]: r for r in rows(PREVIOUS / "subject-review.csv")}
    inspected = rows(ROOT / "title-inspection.csv")
    if len({r["topic_id"] for r in inspected}) != len(inspected):
        raise AssertionError("Repeated title inspection")
    for row in inspected:
        original = previous[row["topic_id"]]
        if any(
            row[field] != original[field]
            for field in ("project", "first_date", "subject", "message_count")
        ):
            raise AssertionError("Title navigation differs from accepted index")
        if row["review_scope"] != "subject_title_only":
            raise AssertionError("Title inspection cannot assert body review")


def check_board() -> None:
    """Recompute exact section hashes, preserving full original line locators."""
    sections = rows(ROOT / "reviewed-board-sections.csv")
    identities = [(r["source_path"], r["start_line"], r["end_line"]) for r in sections]
    if len(identities) != len(set(identities)):
        raise AssertionError("Repeated Board section")
    for row in sections:
        lines = (
            (REPOSITORY / row["source_path"])
            .read_text("utf-8")
            .splitlines(keepends=True)
        )
        start, end = int(row["start_line"]), int(row["end_line"])
        if not 1 <= start <= end <= len(lines):
            raise AssertionError("Board locator outside source")
        section = lines[start - 1 : end]
        if row["sha256"] != digest("".join(section).encode("utf-8")):
            raise AssertionError("Board section bytes changed")
        if not row["reason"]:
            raise AssertionError("Missing Board review note")


def report() -> dict[str, object]:
    """Report only declared source-review progress, never audit completion."""
    state = json.loads((ROOT / "progress.json").read_text("utf-8"))
    if (
        state["status"] != "incomplete"
        or state["baseline_selected"]
        or state["first_pass_locked_at"] is not None
    ):
        raise AssertionError("A progress record cannot assert selection or a lock")
    manifest = json.loads((ROOT / "manifest.json").read_text("utf-8"))
    for group, base in (("files", ROOT), ("accepted_inputs", REPOSITORY)):
        for name, sha in manifest[group].items():
            if digest((base / name).read_bytes()) != sha:
                raise AssertionError(f"Retained input/output bytes changed: {name}")
    check_topics()
    check_titles()
    check_messages()
    check_board()
    return {
        "status": "incomplete",
        "topic_titles_inspected": len(rows(ROOT / "title-inspection.csv")),
        "new_body_reviewed_topics": len(rows(ROOT / "topic-review.csv")),
        "new_reviewed_export_variants": len(
            rows(ROOT / "reviewed-message-variants.csv")
        ),
        "new_reviewed_board_sections": len(rows(ROOT / "reviewed-board-sections.csv")),
        "baseline_selected": False,
        "first_pass_locked_at": None,
    }


def main() -> None:
    """Check retained verification output before reporting a successful check."""
    computed = report()
    if computed != json.loads((ROOT / "verification.json").read_text("utf-8")):
        raise AssertionError("Saved verification differs from recomputation")
    print(json.dumps(computed, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
