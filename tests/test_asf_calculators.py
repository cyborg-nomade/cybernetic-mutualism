"""Synthetic adversarial checks for the registered sampling and decision rules."""

import hashlib
from copy import deepcopy
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
from asf_fixtures import synthetic_tables

from scripts.asf_audit.analysis import (
    access_gate,
    decision_category,
    decision_report,
    directional_summary,
    identifiability,
    nested_summary,
    supported_inventory,
)
from scripts.asf_audit.protocol import AGREEMENT_FIELDS, RULES
from scripts.asf_audit.sampling import (
    analysis_pairs,
    audit_frame,
    comparator,
    hash_key,
    local_baseline,
)
from scripts.asf_audit.stability import agreement
from scripts.asf_audit.timing import (
    authority_shift,
    event_date,
    horizon_result,
    interval,
    recode_not_before,
)
from scripts.asf_audit.validation import integrity_errors, qualifies

EXPECTED_BASELINE_STRATA = 48
EXPECTED_RECODE_SAMPLE = 3


def test_synthetic_full_result_and_all_bounded_c2_routes(tmp_path: Path) -> None:
    """All gates and signed nested witnesses are needed for each bounded upgrade."""
    tables = synthetic_tables(tmp_path)
    assert integrity_errors(tables, tmp_path) == []
    report = decision_report(tables, True)
    assert report["horizons"]["90"]["category"] == "bounded_reciprocal"
    assert not report["timing_sensitive"]
    assert {claim: row["confidence"] for claim, row in report["claims"].items()} == {
        "CM-01": "C2",
        "CM-04": "C1",
        "CM-12": "C2",
        "CM-13": "C2",
    }


@pytest.mark.parametrize("horizon", [60, 180])
def test_either_sensitivity_can_block_c2(tmp_path: Path, horizon: int) -> None:
    """Keep the primary category while reporting either changed sensitivity."""
    tables = synthetic_tables(tmp_path)
    for row in tables["measurements"]:
        if row["horizon"] == str(horizon):
            row["linked_change_met"] = "unknown"
            row["qualified_witness"] = "no"
    report = decision_report(tables, True)
    assert report["horizons"]["90"]["category"] == "bounded_reciprocal"
    assert report["changed_horizons"] == [str(horizon)]
    assert report["claims"]["CM-01"]["confidence"] == "C1"
    assert report["claims"]["CM-12"]["confidence"] == "C1"


def test_failed_gates_and_observational_mapping(tmp_path: Path) -> None:
    """G3 failure narrows vocabulary; G1 failure withholds the mapping decision."""
    tables = synthetic_tables(tmp_path)
    report = decision_report(tables, False)
    assert report["horizons"]["90"]["category"] == "gate_failed"
    assert report["claims"]["CM-04"]["decision"] == "narrow_observational_applicability"
    tables["cohort"][0]["eligible"] = "no"
    report = decision_report(tables, True)
    assert report["claims"]["CM-04"]["decision"] == "withhold_mapping_decision"
    assert all(row["confidence"] == "C1" for row in report["claims"].values())


def test_g1_counts_months_not_rows_and_requires_special_records(tmp_path: Path) -> None:
    """Exactly 33 months pass; duplicated rows cannot replace a missing month."""
    tables = synthetic_tables(tmp_path)
    for row in tables["coverage"]:
        if row["month"] in ("2023-01", "2023-02", "2023-03"):
            row["index_state"] = "missing"
            row["board_state"] = "missing"
    assert access_gate(tables)["pass"]
    tables["coverage"][15]["index_state"] = "missing"
    tables["coverage"].append(deepcopy(tables["coverage"][-5]))
    assert not access_gate(tables)["pass"]
    tables["coverage"][15]["index_state"] = "reviewable"
    tables["special_meetings"] = [
        {
            "meeting_id": "special",
            "event_date": "2023-01-03",
            "state": "missing",
            "source_ids": "",
            "notes": "unknown",
        }
    ]
    assert not access_gate(tables)["pass"]


def test_g2_unknowns_stay_in_denominator_and_shared_family_counts_once(
    tmp_path: Path,
) -> None:
    """Three of four known families pass, two fail; repeated PMCs add no families."""
    tables = synthetic_tables(tmp_path)
    rows = [
        row
        for row in tables["measurements"]
        if row["horizon"] == "90" and row["direction"] == "A_to_C"
    ]
    rows[0]["receiver_observed"] = "unknown"
    assert identifiability(rows, "A_to_C")["pass"]
    rows[1]["receiver_observed"] = "unknown"
    assert not identifiability(rows, "A_to_C")["pass"]
    for row in rows:
        row["family_id"] = "shared-directive"
    assert identifiability(rows, "A_to_C")["families"] == 1


def test_both_signs_require_distinct_families_and_two_projects(tmp_path: Path) -> None:
    """One both-sign family spanning four projects still fails the full criterion."""
    tables = synthetic_tables(tmp_path)
    rows = [row for row in tables["measurements"] if row["horizon"] == "90"]
    for row in rows:
        row["effect_sign"] = "both"
        row["family_id"] = "one"
    assert not directional_summary(rows, "A_to_C")["full"]
    rows[-1]["family_id"] = "two"
    assert directional_summary(rows, "C_to_A")["full"]


@pytest.mark.parametrize(
    "state",
    [
        "supported",
        "compatible but not discriminated",
        "unassessable",
        "missing",
        "unresolved",
    ],
)
def test_only_contradiction_addresses_sufficient_rival(
    tmp_path: Path, state: str
) -> None:
    """An unresolved own-history or shock entry prevents qualification."""
    tables = synthetic_tables(tmp_path)
    row = tables["measurements"][0]
    rival = next(
        entry
        for entry in tables["rivals"]
        if entry["record_id"] == row["record_id"] and entry["rival"] == "common_shock"
    )
    rival["state"] = state
    assert not qualifies(row, tables)
    assert any("unaddressed" in error for error in integrity_errors(tables, tmp_path))


@pytest.mark.parametrize(
    ("present", "informative", "expected"),
    [
        (0, False, "indeterminate"),
        (0, True, "not_demonstrated"),
        (1, False, "one_way"),
        (2, False, "reciprocal_interaction"),
    ],
)
def test_decision_table_order(present: int, informative: bool, expected: str) -> None:
    """Separate absence of qualified witnesses from informative contrary evidence."""
    directions = {
        str(number): {"full": False, "families": ["f"] if number < present else []}
        for number in range(2)
    }
    assert decision_category(directions, informative) == expected


def test_nested_authority_link_onset_sign_and_scope(tmp_path: Path) -> None:
    """Nested counts require linked in-window authority shifts in distinct families."""
    tables = synthetic_tables(tmp_path)
    rows = [row for row in tables["measurements"] if row["horizon"] == "90"]
    assert nested_summary(rows, "CM-12")["category"] == "mixed"
    for row in rows:
        row["authority_outcome_link_met"] = "unknown"
    assert nested_summary(rows, "CM-12")["category"] == "no_qualifying_families"
    for row in rows:
        row["authority_outcome_link_met"] = "yes"
        row["shift_earliest"] = row["shift_latest"] = "2026-01-01"
    assert nested_summary(rows, "CM-13")["category"] == "no_qualifying_families"


@pytest.mark.parametrize(
    ("earliest", "latest", "within", "order", "status"),
    [
        ("2023-04-01", "2023-04-01", "no", "sender_first", "within"),
        ("2023-04-01", "2023-04-02", "no", "sender_first", "unknown"),
        ("2023-05-01", "2023-05-01", "no", "sender_first", "beyond"),
        ("2023-01-01", "2023-01-01", "no", "unknown", "unknown"),
        ("2023-01-01", "2023-01-01", "yes", "documented_within_day_order", "within"),
        ("2022-12-31", "2022-12-31", "no", "receiver_first", "reversed"),
        ("unknown", "unknown", "no", "unknown", "unknown"),
    ],
)
def test_interval_horizons(
    earliest: str, latest: str, within: str, order: str, status: str
) -> None:
    """Inclusive day boundaries never turn delayed evidence into an earlier zero."""
    result = horizon_result(
        {
            "horizon": "90",
            "sender_earliest": "2023-01-01",
            "sender_latest": "2023-01-01",
            "receiver_earliest": earliest,
            "receiver_latest": latest,
            "within_day_order": within,
        }
    )
    assert result["order"] == order
    assert result["status"] == status


def test_utc_ordering_invalid_intervals_and_full_calendar_washout() -> None:
    """Normalize offsets and reject partial-day or preregistration-based washout."""
    assert event_date("2023-01-01T23:30:00-03:00") == date(2023, 1, 2)
    with pytest.raises(ValueError, match="offset"):
        event_date("2023-01-01T23:30:00")
    with pytest.raises(ValueError, match="Reversed"):
        interval("2023-01-02", "2023-01-01")
    assert recode_not_before("2026-09-16T12:00:00Z") == datetime(
        2026, 10, 1, tzinfo=UTC
    )
    assert recode_not_before("2026-09-16T00:00:00Z") == datetime(
        2026, 9, 30, tzinfo=UTC
    )
    assert RULES["primary_end"] + timedelta(days=180) <= RULES["followup_end"]


def test_only_documented_authority_transitions_count() -> None:
    """Unknown prior rights cannot be turned into decentralisation by a PMC label."""
    assert authority_shift("unknown", "pmc_binding") == "unknown"
    assert authority_shift("pmc_binding", "pmc_binding") == "unchanged"
    assert authority_shift("shared_authorization", "pmc_binding") == "toward_pmc"
    assert authority_shift("pmc_binding", "shared_authorization") == "toward_shared"


def test_deterministic_baseline_and_screening_recode_strata(tmp_path: Path) -> None:
    """Hash selection is independent of input order and keeps all 48 strata."""
    tables = synthetic_tables(tmp_path)
    template = tables["screening"][0]
    family = tables["families"][0]
    tables["screening"] = [
        template | {"source_id": f"s{i}", "family_id": f"f{i}", "kind": "local_release"}
        for i in range(11)
    ]
    tables["families"] = [family | {"family_id": f"f{i}"} for i in range(11)]
    tables["measurements"] = []
    expected = min(
        tables["screening"],
        key=lambda row: hashlib.sha256(
            f"httpd|2023-Q1|{row['source_id']}".encode()
        ).hexdigest(),
    )
    log = local_baseline(tables)
    assert len(log) == EXPECTED_BASELINE_STRATA
    assert log[0]["source_id"] == expected["source_id"]
    assert len(audit_frame(tables)) == EXPECTED_RECODE_SAMPLE
    baseline = audit_frame(tables)
    tables["screening"].reverse()
    tables["families"].reverse()
    assert local_baseline(tables) == log
    assert audit_frame(tables) == baseline
    tables["measurements"] = [{"family_id": "f0", "opportunity": "yes"}]
    assert "f0" in audit_frame(tables)
    with pytest.raises(ValueError, match="pipes"):
        hash_key("httpd|ambiguous", "id")


def test_contrast_selection_uses_exposure_year_and_original_id(tmp_path: Path) -> None:
    """Never choose a comparison from unknown exposure or by receiver outcome."""
    family = synthetic_tables(tmp_path)["families"][0]
    earlier = family | {
        "family_id": "earlier",
        "onset_earliest": "2022-01-01",
        "exposure": "unexposed",
    }
    same_year = family | {
        "family_id": "same",
        "earliest_source_id": "z",
        "exposure": "unexposed",
    }
    tied = same_year | {"family_id": "tie", "earliest_source_id": "a"}
    assert comparator(family, [earlier, same_year, tied]) == "tie"
    assert comparator(family, [same_year | {"exposure": "unknown"}]) == ""


def test_agreement_counts_matching_unknowns_but_discloses_them(tmp_path: Path) -> None:
    """Score missing recodes as disagreements and disclose shared uncertainty."""
    row = synthetic_tables(tmp_path)["measurements"][0]
    first = row | dict.fromkeys(AGREEMENT_FIELDS, "unknown")
    report = agreement([first], [first.copy()])
    assert report["agreement"] == 1
    assert report["fields"]["eligible"]["known_agreement"] is None
    assert report["fields"]["eligible"]["first_unknown_rate"] == 1
    assert agreement([first], [])["agreement"] == 0


def test_access_index_metadata_cannot_become_historical_evidence(
    tmp_path: Path,
) -> None:
    """A current index can establish availability without deciding a causal field."""
    source = synthetic_tables(tmp_path)["sources"][0]
    source.update(source_kind="archive_index", published_at="unknown")
    row = {"source_ids": source["source_id"]}
    assert supported_inventory(row, {source["source_id"]: source}, access_only=True)
    assert not supported_inventory(row, {source["source_id"]: source})


def test_audit_supplement_never_expands_primary_release_baseline(
    tmp_path: Path,
) -> None:
    """Recode every small-corpus family while keeping primary analysis sampled."""
    tables = synthetic_tables(tmp_path)
    for number, row in enumerate(tables["screening"]):
        row.update(project="httpd", kind="local_release", source_id=f"opening-{number}")
    pairs = analysis_pairs(tables)
    assert len(pairs) == 1
    assert set(audit_frame(tables)) == {row["family_id"] for row in tables["screening"]}


def test_informative_unchanged_requires_receiver_evidence(tmp_path: Path) -> None:
    """Unchanged burden alone cannot decide the registered informative-null category."""
    tables = synthetic_tables(tmp_path)
    for row in tables["measurements"]:
        row.update(
            qualified_witness="no",
            linked_change_met="no",
            effect_sign="no_demonstrated_effect",
            coordination_burden_change="unchanged",
        )
    report = decision_report(tables, True)
    assert report["horizons"]["90"]["category"] == "indeterminate"
    for row in tables["measurements"]:
        row["receiver_unchanged"] = "yes"
    report = decision_report(tables, True)
    assert report["horizons"]["90"]["category"] == "not_demonstrated"


def test_two_document_copies_cannot_supply_two_acts(tmp_path: Path) -> None:
    """Act identity, not the number of files, determines separate acts."""
    tables = synthetic_tables(tmp_path)
    row = tables["measurements"][0]
    row["receiver_act_id"] = row["sender_act_id"]
    assert not qualifies(row, tables)
    row["receiver_act_id"] = "another-act"
    row["receiver_source_id"] = row["sender_source_id"]
    assert qualifies(row, tables)
