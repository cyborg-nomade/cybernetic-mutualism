"""Fail-closed integrity checks over the entire submitted corpus."""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from scripts.asf_audit.protocol import (
    ANCHOR,
    CONDITIONS,
    DIRECTIONS,
    HORIZONS,
    PROJECTS,
    RIVALS,
    RULES,
    Row,
    Tables,
    digest,
)
from scripts.asf_audit.sampling import (
    analysis_pairs,
    audit_frame,
    comparator,
    eligible_pairs,
)
from scripts.asf_audit.schema import SCHEMAS, structural_errors
from scripts.asf_audit.timing import (
    authority_shift,
    event_date,
    horizon_result,
    interval,
    primary_interval,
    timestamp,
)

POSITIVE_VALUES = {
    "yes",
    "expanded",
    "restricted",
    "increased",
    "decreased",
    "known",
    "enablement",
    "constraint",
    "both",
    "toward_pmc",
    "toward_foundation",
    "toward_shared",
    "sender_first",
    "receiver_first",
    "documented_within_day_order",
    "pmc_binding",
    "foundation_case_specific_authorization",
    "shared_authorization",
    "public_cross_reference",
    "documented_official_act",
    "public_service_record",
    "created",
    "implemented",
    "revised",
    "refused",
    "failed",
    "ongoing",
    "unchanged",
    "official_status_change",
    "explicit_obligation_failure",
    "no_documented_event",
}
ATTESTATIONS = (
    "complete_subject_indices_screened",
    "board_and_officer_reports_screened",
    "special_meeting_calendar_complete",
    "shock_ledger_precedes_witness_labels",
    "family_deduplication_reviewed",
    "all_required_records_coded",
)


def identifiers(value: str) -> list[str]:
    """Split semicolon-separated original IDs without admitting empty IDs."""
    return value.split(";") if value else []


def source_usable(source: Row) -> bool:
    """Exclude uncertain publication/access/eligibility from decisive support."""
    return (
        source["eligible"] == "yes"
        and source["access_state"] in ("public_complete", "public_redacted")
        and source["decisive_material_complete"] == "yes"
        and source["published_at"] != "unknown"
        and event_date(source["published_at"]) <= RULES["source_publication_cutoff"]
    )


def local_path(directory: Path, relative: str) -> Path:
    """Require source artifacts to be regular local files beneath the dataset."""
    path = directory / relative
    if (
        not relative
        or not relative.startswith("sources/")
        or path.is_symlink()
        or not path.resolve().is_relative_to(directory.resolve())
    ):
        raise ValueError("Source path escapes the dataset or is empty/symlinked")
    return path


def source_errors(row: Row, directory: Path) -> list[str]:
    """Validate provenance, exact retrieval bytes, and separate event dating."""
    errors = []
    if row["registration_commit"] != ANCHOR:
        errors.append("incorrect registration anchor")
    if not all(
        row[field].strip() for field in ("url", "locator", "authority_at_event")
    ):
        errors.append("missing source locator, URL, or authority declaration")
    interval(row["event_earliest"], row["event_latest"])
    retrieved = timestamp(row["retrieved_at"])
    if (
        row["published_at"] != "unknown"
        and event_date(row["published_at"]) > retrieved.date()
    ):
        errors.append("publication follows retrieval")
    if row["content_path"]:
        if (
            digest(local_path(directory, row["content_path"]).read_bytes())
            != row["sha256"]
        ):
            errors.append("retrieval hash mismatch")
    elif row["access_state"] in ("public_complete", "public_redacted") or row["sha256"]:
        errors.append("public source or hash without local artifact")
    if row["eligible"] == "no" and not row["exclusion_reason"].strip():
        errors.append("excluded source lacks reason")
    return errors


def reference_errors(tables: Tables) -> list[str]:
    """Check every foreign source/record/family key, not only sampled records."""
    sources = {row["source_id"] for row in tables["sources"]}
    records = {row["record_id"] for row in tables["measurements"]}
    families = {(row["family_id"], row["project"]) for row in tables["families"]}
    errors = []
    for table, rows in tables.items():
        for row in rows:
            for field, value in row.items():
                if (
                    field.endswith("source_ids") or field.endswith("source_id")
                ) and not set(identifiers(value)) <= sources:
                    errors.append(f"{table}: unknown source reference in {field}")
            if "record_id" in row and row["record_id"] not in records:
                errors.append(f"{table}: unknown record reference")
            if (
                table in ("screening", "measurements")
                and row["family_id"]
                and (row["family_id"], row["project"]) not in families
            ):
                errors.append(f"{table}: unknown family/project")
    errors.extend(episode_errors(tables))
    return errors


def episode_errors(tables: Tables) -> list[str]:
    """Require stable episode identities and recorded acts beneath each family."""
    episodes = {row["episode_id"]: row for row in tables["episodes"]}
    families = {(row["family_id"], row["project"]) for row in tables["families"]}
    errors = []
    for row in episodes.values():
        base_id = f"{row['project']}|{row['earliest_source_id']}"
        if row["episode_id"] not in (base_id, f"{base_id}|{row['family_id']}"):
            errors.append("episode ID must use project and earliest original source ID")
        if (row["family_id"], row["project"]) not in families:
            errors.append("episode references an unknown family/project")
        if any(not value.strip() for value in row.values()):
            errors.append(
                "episode narrative has blank fields; record unknown explicitly"
            )
    for row in tables["measurements"]:
        episode = episodes.get(row["episode_id"], {})
        if (episode.get("family_id"), episode.get("project")) != (
            row["family_id"],
            row["project"],
        ):
            errors.append("measurement lacks a matching episode")
    return errors


def evidence_errors(row: Row, tables: Tables) -> list[str]:
    """Require specific usable source locators for affirmative coded fields."""
    sources = {source["source_id"]: source for source in tables["sources"]}
    entries = [
        entry for entry in tables["evidence"] if entry["record_id"] == row["record_id"]
    ]
    supported = {
        entry["field"]
        for entry in entries
        if entry["source_id"] in sources
        and entry["locator"].strip()
        and source_usable(sources[entry["source_id"]])
    }
    positive = {
        field
        for field, value in row.items()
        if field in SCHEMAS["measurements"] and value in POSITIVE_VALUES
    }
    # Metadata and exact dates are validated separately; evidence must identify acts.
    return [
        f"missing decisive locator for {field}"
        for field in sorted(positive - supported)
    ]


def rivals_addressed(row: Row, tables: Tables) -> bool:
    """Require contradiction of both sufficient family-level alternatives."""
    states = {
        entry["rival"]: entry["state"]
        for entry in tables["rivals"]
        if entry["record_id"] == row["record_id"]
    }
    return all(
        states.get(rival) == "contradicted"
        for rival in ("uncoupled_own_history", "common_shock")
    )


def qualifies(row: Row, tables: Tables) -> bool:
    """Calculate a witness from conditions, dating, eligibility, and rivals."""
    return (
        row["eligible"] == row["opportunity"] == "yes"
        and all(row[field] == "yes" for field in CONDITIONS)
        and row["receiver_observed"] == "known"
        and row["channel"]
        in (
            "public_cross_reference",
            "documented_official_act",
            "public_service_record",
        )
        and row["effect_sign"] in ("enablement", "constraint", "both")
        and row["sender_act_id"] != row["receiver_act_id"]
        and bool(row["sender_act_id"] and row["receiver_act_id"])
        and bool(row["sender_source_id"] and row["receiver_source_id"])
        and horizon_result(row)["status"] == "within"
        and primary_interval(row["sender_earliest"], row["sender_latest"])
        and rivals_addressed(row, tables)
    )


def measurement_errors(row: Row, tables: Tables) -> list[str]:
    """Recompute temporal and witness fields rather than trusting labels."""
    errors = evidence_errors(row, tables)
    timing = horizon_result(row)
    if timing["order"] != row["temporal_order"]:
        errors.append("temporal_order disagrees with event intervals")
    expected_shift = authority_shift(row["before_authority"], row["after_authority"])
    if row["decision_authority_shift"] != expected_shift:
        errors.append("authority shift disagrees with before/after rights")
    interval(row["shift_earliest"], row["shift_latest"])
    expected = "yes" if qualifies(row, tables) else "no"
    if row["qualified_witness"] != expected:
        errors.append("qualified_witness disagrees with registered conditions")
    if row["discriminating_contrast_met"] == "yes" and not rivals_addressed(
        row, tables
    ):
        errors.append("unaddressed sufficient rival blocks discrimination")
    if row["receiver_unchanged"] == "yes" and (
        row["receiver_observed"] != "known"
        or row["effect_sign"] != "no_demonstrated_effect"
    ):
        errors.append("unchanged receiver requires affirmative no-effect observation")
    if row["opportunity"] == "yes":
        errors.extend(opportunity_errors(row, tables))
    return errors


def opportunity_errors(row: Row, tables: Tables) -> list[str]:
    """Require explicit rival/shock coverage and the frozen comparison rule."""
    errors = []
    entries = [
        entry for entry in tables["rivals"] if entry["record_id"] == row["record_id"]
    ]
    if {entry["rival"] for entry in entries} != set(RIVALS):
        errors.append("opportunity lacks complete rival matrix")
    if any(not entry["explanation"].strip() for entry in entries):
        errors.append("rival state lacks explanation")
    errors.extend(shock_search_errors(row, tables))
    family = next(
        item
        for item in tables["families"]
        if (item["family_id"], item["project"]) == (row["family_id"], row["project"])
    )
    eligible = eligible_pairs(tables)
    candidates = [
        item
        for item in tables["families"]
        if (item["family_id"], item["project"]) in eligible
    ]
    expected = comparator(family, candidates)
    contrast = next(
        (item for item in tables["contrasts"] if item["record_id"] == row["record_id"]),
        None,
    )
    if contrast is None or contrast["comparator_family_id"] != expected:
        errors.append("contrast differs from deterministic comparator")
    if (
        row["discriminating_contrast_met"] == "yes"
        and contrast is not None
        and not (
            contrast["comparator_family_id"] or contrast["within_episode_source_ids"]
        )
    ):
        errors.append("discrimination lacks matched or within-episode contrast")
    return errors


def shock_search_errors(row: Row, tables: Tables) -> list[str]:
    """Check the 30-day lookback and full horizon; unknown stays unresolved."""
    search = next(
        (
            item
            for item in tables["shock_searches"]
            if item["record_id"] == row["record_id"]
        ),
        None,
    )
    if search is None:
        return ["missing shock search record"]
    sender = interval(row["sender_earliest"], row["sender_latest"])
    errors = []
    if sender is not None:
        start, end = (
            sender[0] - timedelta(days=30),
            sender[1] + timedelta(days=int(row["horizon"])),
        )
        if search["start"] != start.isoformat() or search["end"] != end.isoformat():
            errors.append(
                "shock search window differs from registered lookback/horizon"
            )
    if row["discriminating_contrast_met"] == "yes" and (
        search["complete"] != "yes"
        or not (search["project_source_ids"] and search["foundation_source_ids"])
    ):
        errors.append("discrimination requires both shock search frames")
    shock_ids = {item["shock_id"] for item in tables["shocks"]}
    if not set(identifiers(search["shock_ids"])) <= shock_ids:
        errors.append("unknown shock reference")
    return errors


def frame_errors(tables: Tables, frozen_frame: list[str] | None = None) -> list[str]:
    """Require complete independent horizons/directions for analysis and audit."""
    eligible = eligible_pairs(tables)
    frame = set(audit_frame(tables) if frozen_frame is None else frozen_frame)
    required = analysis_pairs(tables) | {pair for pair in eligible if pair[0] in frame}
    expected = {
        (family, project, direction, str(horizon))
        for family, project in required
        for direction in DIRECTIONS
        for horizon in HORIZONS
    }
    actual = [
        (row["family_id"], row["project"], row["direction"], row["horizon"])
        for row in tables["measurements"]
    ]
    errors = []
    if len(actual) != len(set(actual)):
        errors.append("duplicate family/project/direction/horizon coding")
    if set(actual) != expected:
        errors.append("coding frame differs from census/baseline/audit supplement")
    analysis = analysis_pairs(tables)
    errors.extend(
        "audit opportunity must enter cross-boundary census"
        for row in tables["measurements"]
        if row["opportunity"] == "yes"
        and (row["family_id"], row["project"]) not in analysis
    )
    return errors


def inventory_errors(tables: Tables) -> list[str]:
    """Validate declared cohort, screening universe, dating, and family grouping."""
    errors = []
    for row in tables["families"]:
        if row["project"] not in PROJECTS or not row["family_rationale"].strip():
            errors.append("family lacks cohort project or deduplication rationale")
        dates = interval(row["onset_earliest"], row["onset_latest"])
        if dates is not None and not primary_interval(
            row["onset_earliest"], row["onset_latest"]
        ):
            errors.append(
                "family onset is outside or not identified within primary window"
            )
    for row in tables["screening"]:
        if row["project"] not in PROJECTS or not row["reason"].strip():
            errors.append(
                "screening lacks cohort project or inclusion/exclusion reason"
            )
        if not primary_interval(row["opening_date"], row["opening_date"]):
            errors.append("screening opening outside primary window")
    errors.extend(shock_inventory_errors(tables))
    errors.extend(coverage_inventory_errors(tables))
    errors.extend(bundle_inventory_errors(tables))
    return errors


def coverage_inventory_errors(tables: Tables) -> list[str]:
    """Require an explicit row for each required month, including missing months."""
    required_months = {
        f"{year}-{month:02d}"
        for year in range(RULES["primary_start"].year, RULES["primary_end"].year + 1)
        for month in range(1, 13)
    }
    expected = {
        ("development", project, month)
        for project in PROJECTS
        for month in required_months
    } | {("board", "foundation", month) for month in required_months}
    actual = {(row["kind"], row["project"], row["month"]) for row in tables["coverage"]}
    errors = []
    if actual != expected:
        errors.append("coverage must explicitly inventory all 180 required month rows")
    if {row["project"] for row in tables["cohort"]} != set(PROJECTS):
        errors.append(
            "cohort must explicitly inventory exactly the four fixed projects"
        )
    errors.extend(
        "special meeting falls outside the primary calendar"
        for row in tables["special_meetings"]
        if not primary_interval(row["event_date"], row["event_date"])
    )
    return errors


def bundle_inventory_errors(tables: Tables) -> list[str]:
    """Ensure recoding bundles include every referenced source for their records."""
    bundles = {
        (row["family_id"], row["project"]): set(identifiers(row["source_ids"]))
        for row in tables["families"]
    }
    records = {row["record_id"]: row for row in tables["measurements"]}
    errors = []
    for table in ("measurements", "evidence", "rivals", "shock_searches", "contrasts"):
        for row in tables[table]:
            record = records[row["record_id"]]
            bundle = bundles[record["family_id"], record["project"]]
            refs = {
                source
                for field, value in row.items()
                if field.endswith("source_id") or field.endswith("source_ids")
                for source in identifiers(value)
            }
            if not refs <= bundle:
                errors.append(f"{table}: recode family bundle omits referenced sources")
    return errors


def shock_inventory_errors(tables: Tables) -> list[str]:
    """Check continuing-shock provenance independently of episode inventories."""
    errors = []
    for row in tables["shocks"]:
        interval(row["onset_earliest"], row["onset_latest"])
        if not set(identifiers(row["affected_projects"])) <= set(PROJECTS):
            errors.append("shock lists noncohort project")
        if row["continuing"] == "yes" and not row["continuation_source_ids"]:
            errors.append("continuing shock lacks continuation record")
    return errors


def integrity_errors(
    tables: Tables, directory: Path, frozen_frame: list[str] | None = None
) -> list[str]:
    """Audit all records and return explicit failures, never repair the data."""
    errors = structural_errors(tables)
    if errors:
        return errors
    errors.extend(reference_errors(tables))
    if errors:
        return errors
    try:
        for row in tables["sources"]:
            errors.extend(
                f"source {row['source_id']}: {error}"
                for error in source_errors(row, directory)
            )
        errors.extend(inventory_errors(tables))
        errors.extend(frame_errors(tables, frozen_frame))
        for row in tables["measurements"]:
            errors.extend(
                f"record {row['record_id']}: {error}"
                for error in measurement_errors(row, tables)
            )
        errors.extend(attestation_errors(tables))
    except (ValueError, OSError, KeyError, StopIteration) as error:
        errors.append(f"unreadable or inconsistent corpus: {error}")
    return errors


def attestation_errors(tables: Tables) -> list[str]:
    """Expose completeness assertions the software cannot independently verify."""
    rows = {row["name"]: row for row in tables["attestations"]}
    return [
        f"missing completeness attestation: {name}"
        for name in ATTESTATIONS
        if name not in rows
        or rows[name]["value"] != "yes"
        or not rows[name]["notes"].strip()
    ]
