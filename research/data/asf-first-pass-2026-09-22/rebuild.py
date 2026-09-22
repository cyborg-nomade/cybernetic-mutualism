"""Rebuild descriptive work queues from the accepted access snapshot, offline.

This is evidence preparation, not a replacement for the frozen ASF audit.
It never samples, codes eligibility, calculates gates, or locks a first pass.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import UTC, datetime
from email import policy
from email.parser import BytesParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ACCESS = ROOT.parent / "asf-access-2026-09-21"
MESSAGE_FIELDS = [
    "project",
    "source_id",
    "original_message_id",
    "archive_id",
    "url",
    "index_timestamp",
    "month",
    "subject",
    "topic_id",
    "preliminary_route",
    "index_path",
]
TOPIC_FIELDS = [
    "topic_id",
    "project",
    "first_date",
    "subject",
    "message_count",
    "review_state",
    "classification",
    "reason",
]
VARIANT_FIELDS = [
    "project",
    "source_id",
    "month",
    "export_path",
    "block_number",
    "raw_sha256",
    "plain_body_sha256",
    "date_header",
]


def digest(data: bytes) -> str:
    """Identify bytes without assigning substantive meaning to the hash."""
    return hashlib.sha256(data).hexdigest()


def normalized_subject(subject: str) -> str:
    """Group titles for navigation only, preserving vote/result distinctions."""
    return re.sub(r"^(?:(?:re|fw|fwd):\s*)+", "", subject, flags=re.I).strip()


def route(subject: str, sender: str) -> str:
    """Suggest a queue; never turn a title pattern into completed screening."""
    if re.match(r"^(?:\(tomcat[^)]*\)|\[tomcat[^]]*\]|svn commit:)", subject):
        return "automated_commit_notification"
    if re.match(r"^(?:\[GitHub\]|\[PR\])", subject) and (
        "via GitHub" in sender or "GitBox" in sender
    ):
        return "automated_issue_or_pull_request_notification"
    if re.match(r"^Bug report for Ant \[\d{4}/\d{2}/\d{2}\]$", subject):
        return "automated_bug_summary"
    return "requires_subject_review"


def message_rows() -> list[dict[str, str]]:
    """Retain every occurrence and its original Message-ID, including duplicates."""
    rows = []
    for path in sorted((ACCESS / "sources").glob("*-index.json.gz")):
        index = json.loads(gzip.decompress(path.read_bytes()))
        project = index["domain"].split(".")[0]
        for entry in index["emails"]:
            original = entry["message-id"].strip()
            title = normalized_subject(entry["subject"])
            rows.append(
                {
                    "project": project,
                    "source_id": original,
                    "original_message_id": original,
                    "archive_id": entry["mid"],
                    "url": "https://lists.apache.org/api/source.lua?id=" + entry["mid"],
                    "index_timestamp": datetime.fromtimestamp(
                        entry["epoch"], UTC
                    ).isoformat(),
                    "month": index["searchParams"]["d"],
                    "subject": entry["subject"],
                    "topic_id": "topic-"
                    + digest((project + "|" + title.casefold()).encode())[:16],
                    "preliminary_route": route(entry["subject"], entry["from"]),
                    "index_path": str(path.relative_to(ROOT.parents[2])),
                }
            )
    return rows


def topic_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build a blank review queue; a topic is not a thread or issue family."""
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["preliminary_route"] == "requires_subject_review":
            groups[row["topic_id"]].append(row)
    result = []
    for topic, members in groups.items():
        first = min(members, key=lambda r: (r["index_timestamp"], r["source_id"]))
        result.append(
            {
                "topic_id": topic,
                "project": first["project"],
                "first_date": first["index_timestamp"][:10],
                "subject": normalized_subject(first["subject"]),
                "message_count": str(len(members)),
                "review_state": "pending",
                "classification": "",
                "reason": "",
            }
        )
    return sorted(result, key=lambda r: (r["project"], r["first_date"], r["topic_id"]))


def variant_row(project: str, path: Path, number: int, raw: bytes) -> dict[str, str]:
    """Locate an exported message version without publishing its body."""
    message = BytesParser(policy=policy.default).parsebytes(raw)
    part = message.get_body(preferencelist=("plain",))
    body = part.get_content() if part else ""
    if not isinstance(body, str):
        raise ValueError("Expected a decoded plain-text body")
    return {
        "project": project,
        "source_id": str(message.get("Message-ID", "")).strip(),
        "month": path.name.removesuffix(".mbox.gz").split("-", 1)[1],
        "export_path": str(path.relative_to(ROOT.parents[2])),
        "block_number": str(number),
        "raw_sha256": digest(raw),
        "plain_body_sha256": digest(body.encode()),
        "date_header": str(message.get("Date", "")),
    }


def duplicate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Retain all versions of repeated IDs, without choosing a canonical body."""
    counts = Counter((r["project"], r["source_id"]) for r in rows)
    duplicates = {key for key, count in counts.items() if count > 1}
    result = []
    for path in sorted((ACCESS / "sources").glob("*.mbox.gz")):
        project = path.name.split("-", 1)[0]
        blocks = re.split(rb"(?m)^From [^\n]*\n", gzip.decompress(path.read_bytes()))[
            1:
        ]
        for number, raw in enumerate(blocks, 1):
            header = BytesParser().parsebytes(raw, headersonly=True)
            original = str(header.get("Message-ID", "")).strip()
            if (project, original) in duplicates:
                result.append(variant_row(project, path, number, raw))
    return result


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    """Write deterministic UTF-8 metadata to a newly created output directory."""
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Refuse to overwrite any working review data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    rows = message_rows()
    write_csv(args.output_dir / "message-index.csv", MESSAGE_FIELDS, rows)
    write_csv(args.output_dir / "subject-review.csv", TOPIC_FIELDS, topic_rows(rows))
    write_csv(
        args.output_dir / "duplicate-variants.csv", VARIANT_FIELDS, duplicate_rows(rows)
    )


if __name__ == "__main__":
    main()
