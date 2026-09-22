"""Protect original identifiers and incomplete review state during preparation."""

from __future__ import annotations

import gzip
import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

REPOSITORY = Path(__file__).resolve().parents[1]
PREPARATION = REPOSITORY / "research/data/asf-first-pass-2026-09-22/rebuild.py"


@pytest.fixture
def preparation() -> ModuleType:
    """Load the evidence helper without invoking its write command."""
    spec = importlib.util.spec_from_file_location("asf_preparation", PREPARATION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_notification_replies_remain_reviewable(preparation: ModuleType) -> None:
    """Do not exclude a human reply merely because its root title is automated."""
    assert preparation.route("svn commit: r123", "bot") == (
        "automated_commit_notification"
    )
    assert preparation.route("Re: svn commit: r123", "contributor") == (
        "requires_subject_review"
    )
    assert preparation.route("[PR] Add feature", "contributor") == (
        "requires_subject_review"
    )
    assert preparation.route("[PR] Add feature", "GitBox") == (
        "automated_issue_or_pull_request_notification"
    )


def test_title_normalization_does_not_merge_vote_and_result(
    preparation: ModuleType,
) -> None:
    """Navigation may strip reply prefixes, but cannot decide family identity."""
    assert preparation.normalized_subject("Re: Fwd: [VOTE] Retire component") == (
        "[VOTE] Retire component"
    )
    assert preparation.normalized_subject("Re: [RESULT] Retire component") != (
        preparation.normalized_subject("Re: [VOTE] Retire component")
    )


def test_reused_message_id_retains_both_body_versions(
    preparation: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A reused ID must neither invent two sources nor discard revised content."""
    access = tmp_path / "research/data/access"
    (access / "sources").mkdir(parents=True)
    monkeypatch.setattr(preparation, "ACCESS", access)
    monkeypatch.setattr(preparation, "ROOT", tmp_path / "research/data/stage")
    raw = (
        b"Message-ID: <original@example.test>\n"
        b"Date: Tue, 3 Jan 2023 10:00:00 +0000\n"
        b"Content-Type: text/plain; charset=utf-8\n\n"
    )
    export = b"From archive\n" + raw + b"Original\n"
    export += b"From archive\n" + raw + b"Revised\n"
    (access / "sources/ant-2023-01.mbox.gz").write_bytes(gzip.compress(export))
    entries = [{"project": "ant", "source_id": "<original@example.test>"}] * 2
    variants = preparation.duplicate_rows(entries)
    assert [r["source_id"] for r in variants] == [r["source_id"] for r in entries]
    assert [r["block_number"] for r in variants] == ["1", "2"]
    assert variants[0]["raw_sha256"] != variants[1]["raw_sha256"]
    assert variants[0]["plain_body_sha256"] != variants[1]["plain_body_sha256"]


def test_rebuild_cannot_overwrite_a_review_checkpoint(
    preparation: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Refuse existing destinations before touching reviewer annotations."""
    review = tmp_path / "subject-review.csv"
    review.write_text("retained reviewer notes\n")
    monkeypatch.setattr("sys.argv", ["rebuild", "--output-dir", str(tmp_path)])
    with pytest.raises(FileExistsError):
        preparation.main()
    assert review.read_text() == "retained reviewer notes\n"
