"""Explicit CSV schemas, blank templates, and strict structural validation."""

from __future__ import annotations

import csv
from pathlib import Path

from scripts.asf_audit.protocol import (
    ANCHOR,
    CONDITIONS,
    DIRECTIONS,
    PROJECTS,
    RIVALS,
    RULES,
    Row,
    Tables,
    canonical,
)

YES_NO_UNKNOWN = ("yes", "no", "unknown")
ROLES = ("pmc", "foundation", "external", "unknown")
MISSINGNESS = (
    "not_applicable",
    "not_public",
    "archive_gap",
    "undated",
    "publication_cutoff_unknown",
    "not_observed_in_reviewed_records",
)
ACTION_CLASSES = (
    "release_decision",
    "technical_direction",
    "governance",
    "infrastructure_service",
    "policy_compliance",
)
# Empty tuples denote free text; every CSV column is mandatory even when blank.
SCHEMAS: dict[str, dict[str, tuple[str, ...]]] = {}


def define(name: str, columns: str, **enums: tuple[str, ...]) -> None:
    """Register a table and its enumerated columns in display order."""
    SCHEMAS[name] = dict.fromkeys(columns.split(), ()) | enums


define(
    "sources",
    "source_id url locator source_kind event_earliest event_latest "
    "published_at retrieved_at sha256 content_path authority_at_event "
    "exclusion_reason registration_commit",
    access_state=(
        "public_complete",
        "public_redacted",
        "incomplete_archive",
        "inaccessible",
        "private_reference_only",
    ),
    eligible=YES_NO_UNKNOWN,
)
SCHEMAS["sources"].update(
    source_kind=(
        "approved_minutes",
        "project_report",
        "development_message",
        "referenced_ticket",
        "official_policy",
        "primary_shock",
        "archive_index",
    ),
    decisive_material_complete=YES_NO_UNKNOWN,
)
define("cohort", "project source_ids notes", eligible=YES_NO_UNKNOWN)
define(
    "coverage",
    "coverage_id project month source_ids notes",
    kind=("development", "board"),
    index_state=("reviewable", "verified_empty", "missing", "unknown"),
    threads_state=("retrievable", "none_included", "missing", "unknown"),
    board_state=("approved_minutes", "official_no_meeting", "missing", "unknown"),
)
define(
    "special_meetings",
    "meeting_id event_date source_ids notes",
    state=("approved_minutes", "missing", "unknown"),
)
define(
    "screening",
    "screen_id source_id project family_id opening_date reason",
    eligible=YES_NO_UNKNOWN,
    kind=("cross_boundary", "ambiguous", "local_release", "local_other", "excluded"),
)
define(
    "families",
    "family_id project onset_earliest onset_latest source_ids family_rationale",
    initiating_role=ROLES,
    action_class=ACTION_CLASSES,
    exposure=("exposed", "unexposed", "unknown"),
)
SCHEMAS["families"]["earliest_source_id"] = ()
define(
    "measurements",
    "record_id family_id project direction horizon "
    "sender_source_id receiver_source_id sender_earliest sender_latest "
    "receiver_earliest receiver_latest shift_earliest shift_latest "
    "before_authority after_authority notes",
    **{key: tuple(values) for key, values in RULES["allowed_values"].items()},
    **dict.fromkeys(CONDITIONS, YES_NO_UNKNOWN),
    eligible=YES_NO_UNKNOWN,
    opportunity=YES_NO_UNKNOWN,
    within_day_order=YES_NO_UNKNOWN,
    qualified_witness=("yes", "no"),
    missingness=("none", *MISSINGNESS),
)
SCHEMAS["measurements"].update(direction=DIRECTIONS, horizon=("60", "90", "180"))
SCHEMAS["measurements"].update(
    receiver_unchanged=YES_NO_UNKNOWN,
    episode_id=(),
    sender_act_id=(),
    receiver_act_id=(),
    before_authority=tuple(RULES["allowed_values"]["decision_right"]),
    after_authority=tuple(RULES["allowed_values"]["decision_right"]),
)
define(
    "episodes",
    "episode_id family_id project earliest_source_id sender_role "
    "sender_act intended_receiver original_option requested_change "
    "disposition_history viability_reason viability_duration source_ids",
)
define("evidence", "record_id field source_id locator")
define(
    "shocks",
    "shock_id source_ids onset_earliest onset_latest affected_projects "
    "exposure_differences continuation_source_ids notes",
    kind=(
        "infrastructure_service",
        "security",
        "external_policy_legal",
        "sponsor_employer",
        "contributor_availability",
        "dependency_demand",
    ),
    continuing=YES_NO_UNKNOWN,
    external_precursor=YES_NO_UNKNOWN,
)
define(
    "shock_searches",
    "record_id start end project_source_ids foundation_source_ids shock_ids notes",
    complete=YES_NO_UNKNOWN,
)
define(
    "rivals",
    "record_id source_ids supporting contrary missing explanation",
    rival=RIVALS,
    state=(
        "supported",
        "contradicted",
        "compatible but not discriminated",
        "unassessable",
        "missing",
        "unresolved",
    ),
)
define("contrasts", "record_id comparator_family_id within_episode_source_ids notes")
define("attestations", "name source_ids notes", value=YES_NO_UNKNOWN)

UNIQUE_KEYS = {
    "episodes": ("episode_id",),
    "sources": ("source_id",),
    "cohort": ("project",),
    "coverage": ("kind", "project", "month"),
    "special_meetings": ("meeting_id",),
    "screening": ("project", "source_id"),
    "families": ("family_id", "project"),
    "measurements": ("record_id",),
    "evidence": ("record_id", "field", "source_id", "locator"),
    "shocks": ("shock_id",),
    "shock_searches": ("record_id",),
    "rivals": ("record_id", "rival"),
    "contrasts": ("record_id",),
    "attestations": ("name",),
}


def blank_row(table: str, **values: str) -> Row:
    """Build a blank row; blanks are uncompleted fields, never coded unknowns."""
    if not values.keys() <= SCHEMAS[table].keys():
        raise ValueError(f"Unknown columns in {table}")
    return dict.fromkeys(SCHEMAS[table], "") | values


def write_rows(path: Path, columns: list[str], rows: list[Row]) -> None:
    """Write deterministic UTF-8 CSV, refusing unexpected row columns."""
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path, columns: list[str]) -> list[Row]:
    """Read a CSV with an exact header and reject missing/extra cells."""
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != columns:
            raise ValueError(f"{path.name}: header differs from the frozen schema")
        rows = list(reader)
    if any(None in row or None in row.values() for row in rows):
        raise ValueError(f"{path.name}: malformed CSV row")
    return rows


def load_tables(directory: Path) -> Tables:
    """Read every mandatory ledger, including explicitly empty ledgers."""
    return {
        name: read_rows(directory / f"{name}.csv", list(schema))
        for name, schema in SCHEMAS.items()
    }


def initialize(directory: Path) -> None:
    """Create header-only ledgers and machine schemas in a new directory."""
    directory.mkdir(parents=True, exist_ok=False)
    for name, columns in SCHEMAS.items():
        write_rows(directory / f"{name}.csv", list(columns), [])
    (directory / "schema.json").write_bytes(
        canonical(
            {
                "version": 1,
                "registration_commit": ANCHOR,
                "projects": PROJECTS,
                "tables": SCHEMAS,
                "unique_keys": UNIQUE_KEYS,
            }
        )
    )


def structural_errors(tables: Tables) -> list[str]:
    """Check keys, exact columns, enumerations, and duplicate natural IDs."""
    errors = []
    for table, schema in SCHEMAS.items():
        seen: set[tuple[str, ...]] = set()
        for row in tables[table]:
            key = tuple(row.get(column, "") for column in UNIQUE_KEYS[table])
            if not all(key) or key in seen:
                errors.append(f"{table}: empty or duplicate key {key}")
            seen.add(key)
            if row.keys() != schema.keys():
                errors.append(f"{table} {key}: wrong columns")
            errors.extend(
                f"{table} {key}: invalid {column}={row.get(column)!r}"
                for column, values in schema.items()
                if values and row.get(column) not in values
            )
    return errors
