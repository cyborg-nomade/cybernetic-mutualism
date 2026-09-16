"""Exercise the frozen first-pass and solo recode lifecycle on invented bytes."""

from copy import deepcopy
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from asf_fixtures import synthetic_tables, write_tables

from scripts.asf_audit.__main__ import main
from scripts.asf_audit.freeze import (
    begin_recode,
    freeze_first_pass,
    read_json,
    submit_recode,
    verify_lock,
)
from scripts.asf_audit.protocol import Row, Tables, digest
from scripts.asf_audit.report import audited_report
from scripts.asf_audit.schema import (
    SCHEMAS,
    initialize,
    load_tables,
    read_rows,
    write_rows,
)
from scripts.asf_audit.stability import (
    ADJUDICATION_COLUMNS,
    agreement,
    recode_errors,
    reconcile,
)
from scripts.asf_audit.validation import integrity_errors

LOCK_TIME = datetime(2026, 9, 16, 12, tzinfo=UTC)
START_TIME = datetime(2026, 10, 1, tzinfo=UTC)
INPUT_ERROR_EXIT = 2
ACCEPTED_AMENDMENTS = 2


def make_lock(tmp_path: Path) -> tuple[Tables, Path, dict[str, object]]:
    """Freeze a synthetic pass without performing any aggregate calculation."""
    source = tmp_path / "dataset"
    tables = synthetic_tables(source)
    write_tables(source, tables)
    target = tmp_path / "lock"
    result = freeze_first_pass(source, target, LOCK_TIME)
    return tables, target, result


def exact_recode(tables: Tables, target: Path) -> Path:
    """Stand in for hand coding only in synthetic tests, never in real recoding."""
    mapping = read_json(target / "lock.json")["record_mapping"]
    reverse = {original: opaque for opaque, original in mapping.items()}
    rows = [
        row | {"record_id": reverse[row["record_id"]]} for row in tables["measurements"]
    ]
    path = target.parent / "completed-recode.csv"
    write_rows(path, list(SCHEMAS["measurements"]), rows)
    return path


def test_complete_synthetic_lifecycle_scores_and_adjudicates_once(
    tmp_path: Path,
) -> None:
    """A valid lock, full washout, and exact synthetic recode pass G3."""
    tables, target, locked = make_lock(tmp_path)
    lock_hash = str(locked["lock_sha256"])
    assert not locked["integrity_errors"]
    blank = read_rows(target / "blank-recode/recode.csv", list(SCHEMAS["measurements"]))
    assert len(blank) == len(tables["measurements"])
    for row in blank:
        assert all(
            not value
            for field, value in row.items()
            if field
            not in {
                "record_id",
                "family_id",
                "project",
                "horizon",
                "direction",
            }
        )
    assert not (target / "initial-score.json").exists()
    begin_recode(target, lock_hash, START_TIME, True)
    submitted = submit_recode(
        target, exact_recode(tables, target), lock_hash, START_TIME
    )
    assert submitted["agreement"] == 1
    assert not submitted["disagreements"]
    report = audited_report(target, lock_hash, submitted["score_sha256"])
    assert not report["integrity_errors"]
    assert report["horizons"]["90"]["gates"]["G3"]
    with pytest.raises(FileExistsError):
        submit_recode(target, exact_recode(tables, target), lock_hash, START_TIME)


@pytest.mark.parametrize(
    ("start", "attested"),
    [
        (START_TIME - timedelta(seconds=1), True),
        (START_TIME, False),
    ],
)
def test_no_recode_before_washout_or_without_attestation(
    tmp_path: Path, start: datetime, attested: bool
) -> None:
    """Elapsed preregistration time cannot substitute for the first-pass washout."""
    _, target, locked = make_lock(tmp_path)
    with pytest.raises(ValueError, match="washout"):
        begin_recode(target, str(locked["lock_sha256"]), start, attested)
    assert not (target / "recode-start.json").exists()


@pytest.mark.parametrize(
    "relative",
    [
        "first-pass/sources/act-0.txt",
        "blank-recode/recode.csv",
        "audit-frame.json",
        "lock.json",
    ],
)
def test_any_frozen_file_tampering_is_detected(tmp_path: Path, relative: str) -> None:
    """Externally retained digests expose source, frame, bundle, or manifest edits."""
    _, target, locked = make_lock(tmp_path)
    with (target / relative).open("ab") as stream:
        stream.write(b"\nchanged")
    with pytest.raises(ValueError):
        verify_lock(target, str(locked["lock_sha256"]))


def test_missing_recodes_fail_initial_agreement_without_retry(tmp_path: Path) -> None:
    """A missing recode remains a scored disagreement, not a dropped comparison."""
    _, target, locked = make_lock(tmp_path)
    lock_hash = str(locked["lock_sha256"])
    begin_recode(target, lock_hash, START_TIME, True)
    missing = tmp_path / "missing.csv"
    write_rows(missing, list(SCHEMAS["measurements"]), [])
    score = submit_recode(target, missing, lock_hash, START_TIME)
    assert score["agreement"] == 0
    report = audited_report(target, lock_hash, score["score_sha256"])
    assert not report["horizons"]["90"]["gates"]["G3"]
    assert report["claims"]["CM-01"]["confidence"] == "C1"


def test_score_tampering_and_recode_identity_injection(tmp_path: Path) -> None:
    """Scoring checks identity and its own arithmetic before accepting results."""
    tables, target, locked = make_lock(tmp_path)
    lock_hash = str(locked["lock_sha256"])
    begin_recode(target, lock_hash, START_TIME, True)
    path = exact_recode(tables, target)
    rows = read_rows(path, list(SCHEMAS["measurements"]))
    rows[0]["record_id"] = "injected"
    write_rows(path, list(SCHEMAS["measurements"]), rows)
    score = submit_recode(target, path, lock_hash, START_TIME)
    assert score["recode_errors"]
    (target / "initial-score.json").write_text("{}")
    with pytest.raises(ValueError, match="score differs"):
        audited_report(target, lock_hash, score["score_sha256"])


def unresolved_rows(score: dict[str, object]) -> list[Row]:
    """Preserve both original values with explicit unresolved adjudications."""
    return [
        dict.fromkeys(ADJUDICATION_COLUMNS, "")
        | item
        | {
            "status": "unresolved",
            "rationale": "invented evidence cannot discriminate",
        }
        for item in score["disagreements"]
    ]


@pytest.mark.parametrize(
    "field", ["qualified_witness", "sender_earliest", "authority_outcome_link_met"]
)
def test_unresolved_disputes_remove_only_the_registered_warrant(
    tmp_path: Path, field: str
) -> None:
    """Never overwrite the originals or count disputed witnesses/nested links."""
    tables = synthetic_tables(tmp_path)
    row = tables["measurements"][0]
    recode = row | {field: "unknown"}
    score = agreement([row], [recode])
    final, errors = reconcile(tables, score, unresolved_rows(score))
    assert not errors
    assert tables["measurements"][0] == row
    disputed = final["measurements"][0]
    if field == "authority_outcome_link_met":
        assert disputed[field] == "unknown"
    else:
        assert disputed["qualified_witness"] == "no"


def test_positive_fields_require_usable_source_locators(tmp_path: Path) -> None:
    """Late publications, unknown cutoffs, and missing relevant text cannot decide."""
    tables = synthetic_tables(tmp_path)
    tables["sources"][0]["published_at"] = "2026-09-01"
    assert any("locator" in error for error in integrity_errors(tables, tmp_path))
    tables["sources"][0]["published_at"] = "unknown"
    assert any("locator" in error for error in integrity_errors(tables, tmp_path))
    tables["sources"][0]["published_at"] = "2023-01-01"
    tables["sources"][0]["decisive_material_complete"] = "unknown"
    assert any("locator" in error for error in integrity_errors(tables, tmp_path))


@pytest.mark.parametrize(
    "mutation", ["hash", "duplicate", "enum", "source", "path", "date", "frame"]
)
def test_integrity_rejects_corrupt_records(tmp_path: Path, mutation: str) -> None:
    """Audit every record rather than only fields in the blinded sample."""
    tables = synthetic_tables(tmp_path)
    if mutation == "hash":
        tables["sources"][0]["sha256"] = "0" * 64
    elif mutation == "duplicate":
        tables["sources"].append(deepcopy(tables["sources"][0]))
    elif mutation == "enum":
        tables["measurements"][0]["eligible"] = "maybe"
    elif mutation == "source":
        tables["measurements"][0]["receiver_source_id"] = "absent"
    elif mutation == "path":
        tables["sources"][0]["content_path"] = "../../private"
    elif mutation == "date":
        tables["measurements"][0]["receiver_latest"] = "2022-01-01"
    else:
        tables["measurements"].pop()
    assert integrity_errors(tables, tmp_path)


def test_blank_schemas_roundtrip_but_do_not_claim_integrity(tmp_path: Path) -> None:
    """Header-only artifacts contain no observations and cannot pass a study gate."""
    directory = tmp_path / "blank"
    initialize(directory)
    assert all(not rows for rows in load_tables(directory).values())
    assert integrity_errors(load_tables(directory), directory)
    with pytest.raises(FileExistsError):
        initialize(directory)
    with (directory / "sources.csv").open("a") as stream:
        stream.write("too,few,cells\n")
    with pytest.raises(ValueError, match="malformed"):
        load_tables(directory)


def test_cli_initializes_and_reports_failures(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Commands expose JSON and fail nonzero for invalid or incomplete inputs."""
    directory = tmp_path / "cli"
    monkeypatch.setattr("sys.argv", ["asf-audit", "init", str(directory)])
    assert main() == 0
    assert '"evidence_records": 0' in capsys.readouterr().out
    monkeypatch.setattr("sys.argv", ["asf-audit", "validate", str(directory)])
    assert main() == 1
    monkeypatch.setattr("sys.argv", ["asf-audit", "sample", str(directory)])
    assert main() == 0
    monkeypatch.setattr("sys.argv", ["asf-audit", "access", str(directory)])
    assert main() == 0
    monkeypatch.setattr("sys.argv", ["asf-audit", "init", str(directory)])
    assert main() == INPUT_ERROR_EXIT
    assert '"error"' in capsys.readouterr().out


def test_lock_contains_provenance_and_full_source_hashes(tmp_path: Path) -> None:
    """Preserve the original registration and both amendments in every run."""
    _, target, locked = make_lock(tmp_path)
    manifest = verify_lock(target, str(locked["lock_sha256"]))
    assert len(manifest["provenance"]["amendment_ids"]) == ACCEPTED_AMENDMENTS
    assert manifest["first_pass_files"]["sources/act-0.txt"] == digest(
        (target / "first-pass/sources/act-0.txt").read_bytes()
    )


def test_recode_grid_and_dates_cannot_be_silently_relabelled(tmp_path: Path) -> None:
    """Matching coded values do not excuse changed frame identity or invalid dates."""
    row = synthetic_tables(tmp_path)["measurements"][0]
    assert recode_errors([row], [row | {"horizon": "180"}])
    assert recode_errors([row], [row | {"sender_latest": "invalid"}])


def test_dependent_resolution_preserves_initial_agreement(tmp_path: Path) -> None:
    """A corrected date can invalidate an agreed witness without recoding again."""
    tables = synthetic_tables(tmp_path)
    first = tables["measurements"][0]
    recoded = [
        first | {"receiver_earliest": "2023-05-01", "receiver_latest": "2023-05-01"}
    ]
    score = agreement([first], recoded)
    assert score["agreement"] == 1
    decisions = [
        dict.fromkeys(ADJUDICATION_COLUMNS, "")
        | item
        | {
            "status": "resolved",
            "final_value": item["recode_value"],
            "source_ids": "s1",
            "locator": "invented date clarification",
            "rationale": "correct a date from frozen source",
        }
        for item in score["disagreements"]
    ]
    decisions.extend(
        {
            "record_id": first["record_id"],
            "field": field,
            "first_value": "yes",
            "recode_value": "yes",
            "final_value": "no",
            "status": "resolved",
            "source_ids": "s1",
            "locator": "same date clarification",
            "rationale": "corrected response is beyond the horizon",
        }
        for field in ("ordered_acts_met", "qualified_witness")
    )
    final, errors = reconcile(tables, score, decisions, recoded)
    assert not errors
    assert not integrity_errors(final, tmp_path)
    assert first["qualified_witness"] == "yes"
    assert final["measurements"][0]["qualified_witness"] == "no"
    assert score["agreement"] == 1


def test_family_bundle_must_include_all_recode_support(tmp_path: Path) -> None:
    """A family source list cannot hide contrary/shock or receiver material."""
    tables = synthetic_tables(tmp_path)
    tables["families"][0]["source_ids"] = "s0"
    assert any("bundle omits" in error for error in integrity_errors(tables, tmp_path))
