"""Guard source membership and locators in the evolving evidence preparation."""

from __future__ import annotations

import csv
import gzip
import importlib.util
import json
from email import policy
from email.message import EmailMessage
from pathlib import Path

import pytest

SCRIPT = (
    Path(__file__).parents[1] / "research/data/asf-item3-screening-2026-10-04/verify.py"
)
SPEC = importlib.util.spec_from_file_location("item3_screening", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def write_rows(path: Path, records: list[dict[str, str]]) -> None:
    """Retain realistic CSV rows for source-membership checks."""
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def exported_message(body: str, delivery: str) -> bytes:
    """Create distinct deliveries sharing the same original Message-ID."""
    message = EmailMessage(policy=policy.default)
    message["Message-ID"] = "<same-original@example.org>"
    message["Date"] = "Wed, 4 Jan 2023 12:00:00 +0000"
    message["Received"] = delivery
    message.set_content(body)
    return message.as_bytes()


def test_duplicate_index_does_not_multiply_export_variants(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keep delivery variants and edited bodies without a Cartesian product."""
    previous = tmp_path / "previous"
    sources = tmp_path / "access/sources"
    previous.mkdir()
    sources.mkdir(parents=True)
    index = {
        "project": "httpd",
        "month": "2023-01",
        "topic_id": "topic-reviewed",
        "source_id": "<same-original@example.org>",
    }
    write_rows(previous / "message-index.csv", [index, index])
    blocks = [
        exported_message("First body", "delivery one"),
        exported_message("First body", "delivery two"),
        exported_message("Edited body", "delivery three"),
    ]
    export = b"".join(b"From sender@example.org date\n" + raw for raw in blocks)
    (sources / "httpd-2023-01.mbox.gz").write_bytes(gzip.compress(export))
    monkeypatch.setattr(VERIFY, "REPOSITORY", tmp_path)
    monkeypatch.setattr(VERIFY, "PREVIOUS", previous)
    monkeypatch.setattr(VERIFY, "ACCESS", sources.parent)
    actual = VERIFY.message_variants({"topic-reviewed"})
    assert len(actual) == len(blocks)
    assert len({r["raw_sha256"] for r in actual}) == len(blocks)
    assert actual[0]["plain_body_sha256"] == actual[1]["plain_body_sha256"]
    assert actual[0]["plain_body_sha256"] != actual[-1]["plain_body_sha256"]
    assert [r["block_number"] for r in actual] == ["1", "2", "3"]


def test_missing_variant_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A partial body ledger cannot claim the complete reviewed membership."""
    write_rows(tmp_path / "topic-review.csv", [{"topic_id": "topic-reviewed"}])
    variants = [dict.fromkeys(VERIFY.VARIANT_FIELDS, "first")]
    write_rows(tmp_path / "reviewed-message-variants.csv", variants)
    monkeypatch.setattr(VERIFY, "ROOT", tmp_path)
    monkeypatch.setattr(
        VERIFY,
        "message_variants",
        lambda topics: [*variants, dict.fromkeys(VERIFY.VARIANT_FIELDS, "second")],
    )
    with pytest.raises(AssertionError, match="membership changed"):
        VERIFY.check_messages()


def test_changed_board_section_is_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Preserve section bytes independently of the larger file manifest."""
    (tmp_path / "minutes.txt").write_text("Original heading\nChanged body\n", "utf-8")
    write_rows(
        tmp_path / "reviewed-board-sections.csv",
        [
            {
                "source_path": "minutes.txt",
                "start_line": "1",
                "end_line": "2",
                "sha256": VERIFY.digest(b"Original heading\nOriginal body\n"),
                "reason": "Complete section read.",
            }
        ],
    )
    monkeypatch.setattr(VERIFY, "REPOSITORY", tmp_path)
    monkeypatch.setattr(VERIFY, "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="section bytes changed"):
        VERIFY.check_board()


def test_progress_cannot_assert_a_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reject a premature lock before ordinary metadata checks can bless it."""
    (tmp_path / "progress.json").write_text(
        json.dumps(
            {
                "status": "incomplete",
                "baseline_selected": False,
                "first_pass_locked_at": "2026-10-04T12:00:00Z",
            }
        ),
        "utf-8",
    )
    monkeypatch.setattr(VERIFY, "ROOT", tmp_path)
    with pytest.raises(AssertionError, match="cannot assert selection or a lock"):
        VERIFY.report()


def test_mechanical_route_cannot_hide_body_review(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Retain a human judgment even when no discussion-queue row exists."""
    previous = tmp_path / "previous"
    previous.mkdir()
    write_rows(previous / "subject-review.csv", [{"topic_id": "topic-other"}])
    indexed = {
        "project": "maven",
        "topic_id": "topic-bot",
        "source_id": "<original@example.org>",
        "index_timestamp": "2024-12-06T14:15:14+00:00",
        "subject": "[PR] Add license files",
        "preliminary_route": "automated_issue_or_pull_request_notification",
    }
    write_rows(previous / "message-index.csv", [indexed, indexed])
    review = {
        "topic_id": "topic-bot",
        "project": "maven",
        "first_date": "2024-12-06",
        "subject": "[PR] Add license files",
        "message_count": "2",
        "kind": "ambiguous",
        "reason": "Binding-policy scope requires original PR evidence.",
        "review_scope": "full_exported_plain_bodies",
    }
    write_rows(tmp_path / "topic-review.csv", [review])
    monkeypatch.setattr(VERIFY, "ROOT", tmp_path)
    monkeypatch.setattr(VERIFY, "PREVIOUS", previous)
    VERIFY.check_topics()
    review["subject"] = "Invented policy title"
    write_rows(tmp_path / "topic-review.csv", [review])
    with pytest.raises(AssertionError, match="navigation changed"):
        VERIFY.check_topics()
