"""Initial intra-rater agreement and preserved, evidence-linked reconciliation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from scripts.asf_audit.protocol import AGREEMENT_FIELDS, CONDITIONS, Row, Tables
from scripts.asf_audit.schema import SCHEMAS
from scripts.asf_audit.timing import interval

DATE_FIELDS = (
    "sender_earliest",
    "sender_latest",
    "receiver_earliest",
    "receiver_latest",
    "shift_earliest",
    "shift_latest",
)
REVIEW_FIELDS = (
    *AGREEMENT_FIELDS,
    *DATE_FIELDS,
    "direction",
    "opportunity",
    "before_authority",
    "after_authority",
    "within_day_order",
    "receiver_unchanged",
    "sender_act_id",
    "receiver_act_id",
    "sender_source_id",
    "receiver_source_id",
)
NESTED_FIELDS = {
    "decision_authority_shift",
    "authority_outcome_link_met",
    "autonomy_change",
    "newly_feasible_action_executed",
    "coordination_burden_change",
    "shared_commitment_named",
    "coordination_disposition",
}
ADJUDICATION_COLUMNS = [
    "record_id",
    "field",
    "first_value",
    "recode_value",
    "status",
    "final_value",
    "source_ids",
    "locator",
    "rationale",
]


def agreement(first: list[Row], recode: list[Row]) -> dict[str, Any]:
    """Score once before reconciliation; absent recodes never match unknowns."""
    second = {row["record_id"]: row for row in recode}
    diagnostics = {
        field: field_agreement(first, second, field) for field in AGREEMENT_FIELDS
    }
    comparisons = len(first) * len(AGREEMENT_FIELDS)
    matches = sum(item["matches"] for item in diagnostics.values())
    disagreements: list[Row] = []
    for row in first:
        other = second.get(row["record_id"], {})
        disagreements.extend(
            {
                "record_id": row["record_id"],
                "field": field,
                "first_value": row[field],
                "recode_value": other.get(field, ""),
            }
            for field in REVIEW_FIELDS
            if row[field] != other.get(field, "")
        )
    return {
        "matches": matches,
        "comparisons": comparisons,
        "agreement": matches / comparisons if comparisons else None,
        "fields": diagnostics,
        "disagreements": disagreements,
    }


def field_agreement(
    first: list[Row], second: dict[str, Row], field: str
) -> dict[str, Any]:
    """Expose shared uncertainty and substantive agreement for every field."""
    pairs = [
        (row[field], second.get(row["record_id"], {}).get(field, "")) for row in first
    ]
    matches = sum(left == right and bool(right) for left, right in pairs)
    known = [
        (left, right)
        for left, right in pairs
        if left != "unknown" and right != "unknown"
    ]
    return {
        "matches": matches,
        "comparisons": len(pairs),
        "exact_agreement": matches / len(pairs) if pairs else None,
        "first_unknown_rate": sum(left == "unknown" for left, _ in pairs) / len(pairs)
        if pairs
        else None,
        "recode_unknown_rate": sum(right == "unknown" for _, right in pairs)
        / len(pairs)
        if pairs
        else None,
        "known_comparisons": len(known),
        "known_agreement": sum(left == right and bool(right) for left, right in known)
        / len(known)
        if known
        else None,
    }


def recode_errors(first: list[Row], second: list[Row]) -> list[str]:
    """Reject duplicate or injected recode IDs and invalid nonblank values."""
    expected = {row["record_id"] for row in first}
    ids = [row["record_id"] for row in second]
    errors = []
    if len(ids) != len(set(ids)) or not set(ids) <= expected:
        errors.append("duplicate or unexpected recode IDs")
    for row in second:
        for field, allowed in SCHEMAS["measurements"].items():
            if allowed and row[field] and row[field] not in allowed:
                errors.append(f"invalid recode value: {row['record_id']} {field}")
        errors.extend(recode_metadata_errors(first, row))
    return errors


def recode_metadata_errors(first: list[Row], row: Row) -> list[str]:
    """Protect the neutral grid and reject malformed nonblank recode dates."""
    original = next(
        (item for item in first if item["record_id"] == row["record_id"]), {}
    )
    errors = []
    if any(
        row[field] != original.get(field)
        for field in ("family_id", "project", "direction", "horizon")
    ):
        errors.append("recode altered fixed family/project/direction/horizon axes")
    try:
        for prefix in ("sender", "receiver", "shift"):
            if row[f"{prefix}_earliest"] and row[f"{prefix}_latest"]:
                interval(row[f"{prefix}_earliest"], row[f"{prefix}_latest"])
    except ValueError:
        errors.append("malformed recode event interval")
    return errors


def reconcile(
    tables: Tables,
    initial: dict[str, Any],
    decisions: list[Row],
    recoded: list[Row] | None = None,
) -> tuple[Tables, list[str]]:
    """Keep originals intact; apply evidenced resolutions or conservative exclusions."""
    result = deepcopy(tables)
    rows = {row["record_id"]: row for row in result["measurements"]}
    expected = {
        (item["record_id"], item["field"]): item for item in initial["disagreements"]
    }
    given = {(row["record_id"], row["field"]): row for row in decisions}
    required = set(expected)
    if recoded is not None:
        expected.update(comparison_values(tables["measurements"], recoded))
    errors = []
    if len(given) != len(decisions) or not required <= set(given) <= set(expected):
        errors.append(
            "reconciliation must preserve exactly one entry for each disagreement"
        )
        return result, errors
    unresolved: dict[str, set[str]] = {}
    for key, decision in given.items():
        errors.extend(resolution_errors(decision, expected[key], tables))
        if decision["status"] == "resolved":
            rows[key[0]][key[1]] = decision["final_value"]
            result["evidence"].extend(
                {
                    "record_id": key[0],
                    "field": key[1],
                    "source_id": source,
                    "locator": decision["locator"],
                }
                for source in decision["source_ids"].split(";")
                if source
            )
        else:
            unresolved.setdefault(key[0], set()).add(key[1])
    for record, fields in unresolved.items():
        exclude_unresolved(rows[record], fields)
    # Several resolutions may cite an existing field locator; retain one copy.
    result["evidence"] = [
        dict(items)
        for items in dict.fromkeys(
            tuple(sorted(row.items())) for row in result["evidence"]
        )
    ]
    return result, errors


def comparison_values(
    first: list[Row], recoded: list[Row]
) -> dict[tuple[str, str], Row]:
    """Allow documented dependent corrections without rewriting either pass."""
    second = {row["record_id"]: row for row in recoded}
    return {
        (row["record_id"], field): {
            "first_value": row[field],
            "recode_value": second[row["record_id"]][field],
        }
        for row in first
        if row["record_id"] in second
        for field in REVIEW_FIELDS
    }


def resolution_errors(decision: Row, expected: Row, tables: Tables) -> list[str]:
    """Require retained values and source locators for each adjudicated change."""
    errors = []
    if any(
        decision[field] != expected[field] for field in ("first_value", "recode_value")
    ):
        errors.append("reconciliation altered an original value")
    if (
        decision["status"] not in ("resolved", "unresolved")
        or not decision["rationale"].strip()
    ):
        errors.append("reconciliation lacks status or rationale")
    sources = {row["source_id"] for row in tables["sources"]}
    if decision["status"] == "resolved" and (
        not decision["source_ids"]
        or not decision["locator"].strip()
        or not set(decision["source_ids"].split(";")) <= sources
    ):
        errors.append("resolution lacks frozen source evidence")
    return errors


def exclude_unresolved(row: Row, fields: set[str]) -> None:
    """Remove disputed witnesses/dates or nested outcomes from qualifying counts."""
    if fields & (
        set(CONDITIONS)
        | set(DATE_FIELDS)
        | {
            "qualified_witness",
            "receiver_observed",
            "temporal_order",
            "channel",
            "effect_sign",
            "eligible",
            "direction",
            "opportunity",
            "within_day_order",
            "sender_act_id",
            "receiver_act_id",
            "sender_source_id",
            "receiver_source_id",
        }
    ):
        row["discriminating_contrast_met"] = "unknown"
        row["qualified_witness"] = "no"
    if fields & (NESTED_FIELDS | {"before_authority", "after_authority"}):
        row["authority_outcome_link_met"] = "unknown"
