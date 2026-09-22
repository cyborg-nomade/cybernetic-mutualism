"""Verify this incomplete screening checkpoint without calculating ASF gates."""

from __future__ import annotations

import csv
import gzip
import json
import re
from collections import Counter

from rebuild import ROOT, digest, duplicate_rows, message_rows, topic_rows, variant_row


def read_csv(name: str) -> list[dict[str, str]]:
    """Read a checkpoint table without changing reviewer entries."""
    with (ROOT / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def verify_reviewed_messages(rows: list[dict[str, str]]) -> None:
    """Check every reviewed message locator against its exact accepted bytes."""
    exports: dict[str, list[bytes]] = {}
    for row in rows:
        path = ROOT.parents[2] / row["export_path"]
        if row["export_path"] not in exports:
            exports[row["export_path"]] = re.split(
                rb"(?m)^From [^\n]*\n", gzip.decompress(path.read_bytes())
            )[1:]
        number = int(row["block_number"])
        actual = variant_row(
            row["project"], path, number, exports[row["export_path"]][number - 1]
        )
        for field in ("source_id", "raw_sha256", "plain_body_sha256", "date_header"):
            assert row[field] == actual[field], (row["source_id"], field)


def verify_review_queue(messages: list[dict[str, str]]) -> Counter[str]:
    """Reject missing titles, silent completion, or untraceable reviewed bodies."""
    template = {r["topic_id"]: r for r in topic_rows(messages)}
    actual = read_csv("subject-review.csv")
    assert len(actual) == len(template)
    assert {r["topic_id"] for r in actual} == set(template)
    immutable = ("topic_id", "project", "first_date", "subject", "message_count")
    for row in actual:
        assert all(row[k] == template[row["topic_id"]][k] for k in immutable), row
        assert row["review_state"] in {"pending", "body_reviewed_followup_pending"}
        if row["review_state"] == "pending":
            assert not row["classification"] and not row["reason"], row
        else:
            assert row["classification"] and row["reason"], row
    reviewed_topics = {r["topic_id"] for r in actual if r["review_state"] != "pending"}
    reviewed = read_csv("reviewed-messages.csv")
    expected = Counter(
        (r["project"], r["source_id"], r["topic_id"])
        for r in messages
        if r["topic_id"] in reviewed_topics
    )
    assert expected == Counter(
        (r["project"], r["source_id"], r["topic_id"]) for r in reviewed
    )
    public_locators = {(r["project"], r["source_id"], r["url"]) for r in messages}
    assert all(
        (r["project"], r["source_id"], r["url"]) in public_locators for r in reviewed
    )
    verify_reviewed_messages(reviewed)
    return Counter(r["review_state"] for r in actual)


def verify_board_locators() -> None:
    """Verify bounded section locators, without attesting whole-minute review."""
    for row in read_csv("reviewed-board-sections.csv"):
        lines = (ROOT.parents[2] / row["source_path"]).read_text().splitlines()
        start, end = int(row["start_line"]), int(row["end_line"])
        assert 1 <= start <= end <= len(lines), row
        if row["locator"].startswith("Attachment"):
            assert lines[start - 1] == row["locator"], row
        else:
            assert "Change the Apache Ant Project Chair" in lines[start - 1], row
            assert "approved by Unanimous Vote" in lines[end - 1], row


def report() -> dict[str, object]:
    """Check descriptive integrity while leaving G2, G3, and claims unassessed."""
    manifest = json.loads((ROOT / "checkpoint.json").read_text())
    assert manifest["status"] == "incomplete"
    assert manifest["first_pass_locked_at"] is None
    for name, expected in manifest["file_hashes"].items():
        assert digest((ROOT / name).read_bytes()) == expected, name
    messages = message_rows()
    assert read_csv("message-index.csv") == messages
    variants = duplicate_rows(messages)
    assert read_csv("duplicate-variants.csv") == variants
    states = verify_review_queue(messages)
    verify_board_locators()
    return {
        "status": "incomplete",
        "scope": "Checkpoint integrity only; not completed screening or G2/G3",
        "indexed_occurrences": len(messages),
        "distinct_project_message_pairs": len(
            {(r["project"], r["source_id"]) for r in messages}
        ),
        "duplicate_variant_rows": len(variants),
        "review_states": dict(states),
        "reviewed_message_rows": len(read_csv("reviewed-messages.csv")),
        "reviewed_board_sections": len(read_csv("reviewed-board-sections.csv")),
        "integrity_errors": [],
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
