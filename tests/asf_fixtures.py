"""Invented, local-only ASF-shaped ledgers; never empirical case observations."""

from datetime import date, timedelta
from pathlib import Path

from scripts.asf_audit.analysis import months
from scripts.asf_audit.protocol import (
    ANCHOR,
    DIRECTIONS,
    HORIZONS,
    PROJECTS,
    RIVALS,
    Row,
    Tables,
    digest,
)
from scripts.asf_audit.schema import SCHEMAS, blank_row, write_rows
from scripts.asf_audit.validation import ATTESTATIONS, POSITIVE_VALUES

PMC_SHIFT_FAMILIES = 2


def synthetic_tables(directory: Path) -> Tables:
    """Build four invented signed families and a fully documented access frame."""
    tables: Tables = {name: [] for name in SCHEMAS}
    source_dir = directory / "sources"
    source_dir.mkdir(parents=True)
    for number in range(2):
        payload = f"INVENTED calibration act {number}; not an ASF record.\n".encode()
        path = source_dir / f"act-{number}.txt"
        path.write_bytes(payload)
        tables["sources"].append(
            blank_row(
                "sources",
                source_id=f"s{number}",
                url=f"https://example.invalid/s{number}",
                locator="invented paragraph",
                source_kind="development_message",
                event_earliest="2023-01-01",
                event_latest="2023-01-01",
                published_at="2023-01-01",
                retrieved_at="2026-09-16T10:00:00Z",
                sha256=digest(payload),
                content_path=f"sources/act-{number}.txt",
                authority_at_event="invented policy, paragraph 1",
                eligible="yes",
                access_state="public_complete",
                registration_commit=ANCHOR,
                decisive_material_complete="yes",
            )
        )
    add_coverage(tables)
    for number, project in enumerate(PROJECTS):
        add_family(tables, number, project)
    return tables


def add_coverage(tables: Tables) -> None:
    """Supply synthetic source-backed cohort and calendar coverage."""
    for project in PROJECTS:
        tables["cohort"].append(
            blank_row(
                "cohort",
                project=project,
                eligible="yes",
                source_ids="s0",
                notes="invented",
            )
        )
    for month in months():
        for project in (*PROJECTS, "foundation"):
            tables["coverage"].append(
                blank_row(
                    "coverage",
                    coverage_id=f"{project}-{month}",
                    month=month,
                    project=project,
                    kind="board" if project == "foundation" else "development",
                    source_ids="s0",
                    index_state="reviewable",
                    threads_state="retrievable",
                    board_state="approved_minutes",
                )
            )
    tables["attestations"] = [
        blank_row(
            "attestations",
            name=name,
            value="yes",
            source_ids="s0",
            notes="invented fixture assertion",
        )
        for name in ATTESTATIONS
    ]


def add_family(tables: Tables, number: int, project: str) -> None:
    """Create a distinct two-direction family with independently coded horizons."""
    family = f"invented-{number}"
    tables["episodes"].append(
        dict.fromkeys(SCHEMAS["episodes"], "invented")
        | {
            "episode_id": f"{project}|s0",
            "family_id": family,
            "project": project,
            "earliest_source_id": "s0",
            "source_ids": "s0;s1",
        }
    )
    tables["screening"].append(
        blank_row(
            "screening",
            screen_id=family,
            source_id="s0",
            project=project,
            family_id=family,
            opening_date="2023-01-01",
            eligible="yes",
            kind="cross_boundary",
            reason="invented request",
        )
    )
    tables["families"].append(
        blank_row(
            "families",
            earliest_source_id="s0",
            family_id=family,
            project=project,
            onset_earliest="2023-01-01",
            onset_latest="2023-01-01",
            source_ids="s0;s1",
            family_rationale="independent invented deliverable",
            initiating_role="pmc",
            action_class="governance",
            exposure="exposed",
        )
    )
    for direction in DIRECTIONS:
        for horizon in HORIZONS:
            row = measurement(family, project, direction, horizon, number)
            tables["measurements"].append(row)
            add_measurement_support(tables, row)


def measurement(
    family: str, project: str, direction: str, horizon: int, number: int
) -> Row:
    """Construct a known witness with invented authority and response evidence."""
    row = {
        field: "unknown" if "unknown" in allowed else ""
        for field, allowed in SCHEMAS["measurements"].items()
    }
    row.update(
        episode_id=f"{project}|s0",
        record_id=f"{family}-{direction}-{horizon}",
        family_id=family,
        project=project,
        sender_act_id=f"{family}-sender",
        receiver_act_id=f"{family}-receiver",
        direction=direction,
        horizon=str(horizon),
        eligible="yes",
        opportunity="yes",
        sender_source_id="s0",
        receiver_source_id="s1",
        sender_earliest="2023-01-01",
        sender_latest="2023-01-01",
        receiver_earliest="2023-01-02",
        receiver_latest="2023-01-02",
        shift_earliest="2023-01-01",
        shift_latest="2023-01-01",
        within_day_order="no",
        receiver_observed="known",
        temporal_order="sender_first",
        channel="public_cross_reference",
        ordered_acts_met="yes",
        receiver_conduct_met="yes",
        linked_change_met="yes",
        discriminating_contrast_met="yes",
        qualified_witness="yes",
        missingness="none",
        authority_outcome_link_met="yes",
        newly_feasible_action_executed="yes",
        effect_sign="constraint" if number % 2 else "enablement",
        autonomy_change="restricted" if number % 2 else "expanded",
        coordination_burden_change="increased",
        shared_commitment_named="yes",
        coordination_disposition="implemented",
    )
    toward_pmc = number < PMC_SHIFT_FAMILIES
    row.update(
        before_authority="foundation_case_specific_authorization"
        if toward_pmc
        else "pmc_binding",
        after_authority="pmc_binding"
        if toward_pmc
        else "foundation_case_specific_authorization",
        decision_authority_shift="toward_pmc" if toward_pmc else "toward_foundation",
    )
    return row


def add_measurement_support(tables: Tables, row: Row) -> None:
    """Supply invented locators, contrasts, and rival/shock review records."""
    tables["evidence"].extend(
        blank_row(
            "evidence",
            record_id=row["record_id"],
            field=field,
            source_id="s0",
            locator="invented paragraph",
        )
        for field, value in row.items()
        if value in POSITIVE_VALUES
    )
    tables["rivals"].extend(
        blank_row(
            "rivals",
            record_id=row["record_id"],
            rival=rival,
            state="contradicted",
            source_ids="s0",
            explanation="invented discriminating revision",
        )
        for rival in RIVALS
    )
    tables["shock_searches"].append(
        blank_row(
            "shock_searches",
            record_id=row["record_id"],
            start="2022-12-02",
            end=(date(2023, 1, 1) + timedelta(days=int(row["horizon"]))).isoformat(),
            project_source_ids="s0",
            foundation_source_ids="s1",
            complete="yes",
            notes="invented negative search",
        )
    )
    tables["contrasts"].append(
        blank_row(
            "contrasts",
            record_id=row["record_id"],
            within_episode_source_ids="s0;s1",
            notes="invented before/after",
        )
    )


def write_tables(directory: Path, tables: Tables) -> None:
    """Write fixture ledgers in the production schema order."""
    for name, rows in tables.items():
        write_rows(directory / f"{name}.csv", list(SCHEMAS[name]), rows)
