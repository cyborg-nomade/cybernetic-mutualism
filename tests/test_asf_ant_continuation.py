"""Reject incomplete or altered evidence in the bounded Ant continuation."""

from __future__ import annotations

import csv
import gzip
import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture
def continuation() -> ModuleType:
    """Load the evidence verifier without executing its CLI."""
    path = (
        Path(__file__).resolve().parents[1]
        / "research/data/asf-ant-screening-2026-10-04/verify.py"
    )
    spec = importlib.util.spec_from_file_location("ant_continuation", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_missing_or_repeated_occurrence_fails(continuation: ModuleType) -> None:
    """An index screen cannot omit an occurrence or substitute a duplicate."""
    first = dict.fromkeys(continuation.IDENTITY_FIELDS, "first")
    second = dict.fromkeys(continuation.IDENTITY_FIELDS, "second")
    for row in (first, second):
        row.update(reason="Retained for body review", review_scope="subject only")
    continuation.check_occurrences([first, second], [first, second])
    for incomplete in ([first], [first, first]):
        with pytest.raises(AssertionError, match="occurrence membership"):
            continuation.check_occurrences([first, second], incomplete)


def test_export_change_invalidates_body_review(
    continuation: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Edited source bytes must fail even when the original Message-ID is reused."""
    monkeypatch.setattr(continuation, "ROOT", tmp_path)
    monkeypatch.setattr(continuation, "REPOSITORY", tmp_path)
    (tmp_path / "topic-review.csv").write_text("topic_id\ntopic-one\n", "utf-8")
    raw = (
        b"Message-ID: <original@example.test>\n"
        b"Date: Tue, 3 Jan 2023 10:00:00 +0000\n"
        b"Content-Type: text/plain; charset=utf-8\n\nOriginal body\n"
    )
    source = {"project": "ant", "topic_id": "topic-one", "url": "public-locator"}
    reviewed = source | continuation.message_details(raw)
    reviewed.update(export_path="source.mbox.gz", block_number="1")
    export = tmp_path / "source.mbox.gz"
    export.write_bytes(gzip.compress(b"From archive\n" + raw))
    continuation.check_messages([reviewed], [reviewed])
    export.write_bytes(gzip.compress(b"From archive\n" + raw + b"Edited\n"))
    with pytest.raises(AssertionError, match="message bytes changed"):
        continuation.check_messages([reviewed], [reviewed])
    with pytest.raises(AssertionError, match="missing or extra message bodies"):
        continuation.check_messages([], [reviewed])


def test_family_cannot_shift_vote_date_or_draw_sample(continuation: ModuleType) -> None:
    """Calendar-boundary announcements and premature draws cannot replace openings."""
    source = {
        "date_header": "Mon, 23 Dec 2024 13:11:07 +0000",
        "topic_id": "topic-vote",
    }
    row = {
        "formal_opening_source_id": "<vote@example.test>",
        "formal_opening_date": "2024-12-23",
        "formal_opening_topic_id": "topic-vote",
        "member_topic_ids": "topic-vote;topic-result;topic-announce",
        "context_topic_ids": "topic-prepare",
        "sample_selected": "no",
    }
    topics = {"topic-vote", "topic-result", "topic-announce", "topic-prepare"}
    sources = {"<vote@example.test>": source}
    continuation.check_family(row, sources, topics)
    with pytest.raises(AssertionError, match="Formal date differs"):
        continuation.check_family(
            row | {"formal_opening_date": "2025-01-02"}, sources, topics
        )
    with pytest.raises(AssertionError, match="sample prematurely selected"):
        continuation.check_family(row | {"sample_selected": "yes"}, sources, topics)


def test_board_non_submission_requires_actual_text(
    continuation: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An empty attachment alone cannot pass as an explicit non-submission."""
    monkeypatch.setattr(continuation, "ROOT", tmp_path)
    monkeypatch.setattr(continuation, "REPOSITORY", tmp_path)
    with (tmp_path / "reviewed-board-sections.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["source_path", "start_line", "end_line", "locator"]
        )
        writer.writeheader()
        writer.writerow(
            {
                "source_path": "minutes.txt",
                "start_line": "1",
                "end_line": "3",
                "locator": "Ant agenda",
            }
        )
    minutes = tmp_path / "minutes.txt"
    minutes.write_text("Ant agenda\n\nNo report was submitted.\n", "utf-8")
    continuation.check_board_sections()
    minutes.write_text("Ant agenda\n\n\n", "utf-8")
    with pytest.raises(AssertionError, match="Non-submission is not explicit"):
        continuation.check_board_sections()
