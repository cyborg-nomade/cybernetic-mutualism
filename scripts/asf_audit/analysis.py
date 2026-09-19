"""Registered gate arithmetic and bounded claim decisions at each horizon."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from scripts.asf_audit.protocol import (
    DIRECTIONS,
    HORIZONS,
    PROJECTS,
    RULES,
    Row,
    Tables,
)
from scripts.asf_audit.sampling import analysis_pairs
from scripts.asf_audit.timing import horizon_result, primary_interval
from scripts.asf_audit.validation import identifiers, qualifies, source_usable


def months() -> list[str]:
    """Enumerate exactly the 36 primary calendar months."""
    return [
        f"{year}-{month:02d}"
        for year in range(RULES["primary_start"].year, RULES["primary_end"].year + 1)
        for month in range(1, 13)
    ]


def supported_inventory(
    row: Row, sources: dict[str, Row], access_only: bool = False
) -> bool:
    """Require usable provenance for a declared access or eligibility success."""
    refs = identifiers(row["source_ids"])
    return bool(refs) and all(
        ref in sources
        and (
            source_usable(sources[ref])
            or (
                access_only
                and sources[ref]["source_kind"] == "archive_index"
                and sources[ref]["access_state"] == "public_complete"
                and sources[ref]["decisive_material_complete"] == "yes"
            )
        )
        for ref in refs
    )


def access_gate(tables: Tables) -> dict[str, Any]:
    """Calculate G1 with exact monthly denominators and separate special meetings."""
    sources = {row["source_id"]: row for row in tables["sources"]}
    cohort = {
        row["project"]
        for row in tables["cohort"]
        if row["eligible"] == "yes" and supported_inventory(row, sources)
    }
    coverage = [
        row
        for row in tables["coverage"]
        if row["month"] in months()
        and supported_inventory(row, sources, access_only=row["kind"] == "development")
    ]
    counts = {
        project: len(
            {
                row["month"]
                for row in coverage
                if row["project"] == project
                and row["kind"] == "development"
                and row["index_state"] in ("reviewable", "verified_empty")
                and row["threads_state"] in ("retrievable", "none_included")
            }
        )
        for project in PROJECTS
    }
    board = len(
        {
            row["month"]
            for row in coverage
            if row["kind"] == "board"
            and row["project"] == "foundation"
            and row["board_state"] in ("approved_minutes", "official_no_meeting")
        }
    )
    special = all(
        row["state"] == "approved_minutes" and supported_inventory(row, sources)
        for row in tables["special_meetings"]
    )
    calendar = any(
        row["name"] == "special_meeting_calendar_complete"
        and row["value"] == "yes"
        and supported_inventory(row, sources, access_only=True)
        for row in tables["attestations"]
    )
    threshold = RULES["source_coverage_months_required"]
    return {
        "pass": cohort == set(PROJECTS)
        and board >= threshold
        and special
        and calendar
        and all(count >= threshold for count in counts.values()),
        "eligible_projects": sorted(cohort),
        "development_months": counts,
        "board_months": board,
        "special_meetings_complete": special and calendar,
        "required_months": threshold,
        "denominator_months": len(months()),
    }


def horizon_rows(tables: Tables, horizon: int) -> list[Row]:
    """Use the analysis census/baseline, excluding routine audit supplements."""
    pairs = analysis_pairs(tables)
    return [
        row
        for row in tables["measurements"]
        if int(row["horizon"]) == horizon
        and (row["family_id"], row["project"]) in pairs
    ]


def identifiability(rows: list[Row], direction: str) -> dict[str, Any]:
    """Count opportunities once per family; unknown responses remain denominator."""
    groups: dict[str, list[Row]] = defaultdict(list)
    for row in rows:
        if (
            row["direction"] == direction
            and row["opportunity"] == row["eligible"] == "yes"
        ):
            groups[row["family_id"]].append(row)
    classifiable = sum(
        all(
            row["receiver_observed"] == "known"
            and row["temporal_order"] != "unknown"
            and horizon_result(row)["status"] in ("within", "reversed")
            for row in family
        )
        for family in groups.values()
    )
    projects = {row["project"] for family in groups.values() for row in family}
    fraction = classifiable / len(groups) if groups else 0.0
    return {
        "pass": len(groups) >= RULES["opportunity_families_per_direction_required"]
        and len(projects) >= RULES["projects_per_direction_required"]
        and fraction >= RULES["classifiable_opportunity_fraction_required"],
        "families": len(groups),
        "classifiable": classifiable,
        "classifiable_fraction": fraction,
        "projects": sorted(projects),
    }


def distinct_signs(first: set[str], second: set[str]) -> bool:
    """Require two different families, allowing two distinct both-sign families."""
    return any(left != right for left in first for right in second)


def directional_summary(rows: list[Row], direction: str) -> dict[str, Any]:
    """Count qualified families, observed projects, and separate signed families."""
    selected = [row for row in rows if row["direction"] == direction]
    families = {row["family_id"] for row in selected}
    projects = {row["project"] for row in selected}
    enabling = {
        row["family_id"]
        for row in selected
        if row["effect_sign"] in ("enablement", "both")
    }
    constraining = {
        row["family_id"]
        for row in selected
        if row["effect_sign"] in ("constraint", "both")
    }
    return {
        "families": sorted(families),
        "projects": sorted(projects),
        "enablement": sorted(enabling),
        "constraint": sorted(constraining),
        "full": len(families) >= RULES["qualified_families_per_direction_required"]
        and len(projects) >= RULES["projects_per_direction_required"]
        and distinct_signs(enabling, constraining),
    }


def matches(row: Row, requirements: list[str]) -> bool:
    """Apply a manifest conjunction of explicit field:value requirements."""
    return all(
        row[field] == value
        for field, value in (item.split(":", 1) for item in requirements)
    )


def nested_summary(rows: list[Row], claim: str) -> dict[str, Any]:
    """Evaluate separate signed families in the registered decision-authority layer."""
    prefix = claim.lower().replace("-", "")
    selected = [
        row
        for row in rows
        if matches(row, RULES["nested_claim_family_required_values"])
        and matches(row, RULES[f"{prefix}_family_required_values"])
        and primary_interval(row["shift_earliest"], row["shift_latest"])
    ]
    first_key = "generative" if claim == "CM-12" else "enabling"
    first = {
        row["family_id"]
        for row in selected
        if matches(row, RULES[f"{prefix}_{first_key}_required_values"])
    }
    second = {row["family_id"] for row in selected if nested_second(row, claim)}
    contributing = [row for row in selected if row["family_id"] in first | second]
    projects = {row["project"] for row in contributing}
    mixed = (
        distinct_signs(first, second)
        and len(projects) >= RULES["nested_claim_projects_required"]
        and len(first | second) >= RULES["nested_claim_families_required"]
    )
    category = "mixed" if mixed else "limited_or_single_sign"
    if not selected:
        category = "no_qualifying_families"
    return {
        "category": category,
        "first_sign": sorted(first),
        "second_sign": sorted(second),
        "families": sorted({row["family_id"] for row in selected}),
        "projects": sorted(projects),
    }


def nested_second(row: Row, claim: str) -> bool:
    """Evaluate the registered burden/failure disjunction or suppressive outcome."""
    if claim == "CM-13":
        return matches(row, RULES["cm13_suppressive_required_values"])
    return any(
        matches(row, conditions)
        for conditions in RULES["cm12_disorganising_any_condition_sets"]
    )


def informative_null(rows: list[Row], tables: Tables) -> bool:
    """Recognize evidenced unchanged dispositions or supported sufficient rivals."""
    candidates = {
        row["record_id"]
        for row in rows
        if row["opportunity"] == "yes"
        and row["receiver_observed"] == "known"
        and row["effect_sign"] == "no_demonstrated_effect"
    }
    unchanged = any(
        row["record_id"] in candidates and row["receiver_unchanged"] == "yes"
        for row in rows
    )
    supported = any(
        entry["record_id"] in candidates
        and entry["state"] == "supported"
        and entry["rival"] in ("uncoupled_own_history", "common_shock")
        for entry in tables["rivals"]
    )
    return unchanged or supported


def decision_category(directions: dict[str, Any], informative: bool) -> str:
    """Apply the registered outcome table in its declared order."""
    summaries = list(directions.values())
    if all(item["full"] for item in summaries):
        return "bounded_reciprocal"
    present = sum(bool(item["families"]) for item in summaries)
    if present == len(DIRECTIONS):
        return "reciprocal_interaction"
    if present:
        return "one_way"
    return "not_demonstrated" if informative else "indeterminate"


def adjudicate_horizon(
    tables: Tables, horizon: int, audit_passed: bool
) -> dict[str, Any]:
    """Calculate G1-G3 and nested results without changing the primary horizon."""
    rows = horizon_rows(tables, horizon)
    access = access_gate(tables)
    identification = {
        direction: identifiability(rows, direction) for direction in DIRECTIONS
    }
    gates = {
        "G1": access["pass"],
        "G2": all(item["pass"] for item in identification.values()),
        "G3": audit_passed,
    }
    qualified = [row for row in rows if qualifies(row, tables)]
    directions = {
        direction: directional_summary(qualified, direction) for direction in DIRECTIONS
    }
    category = decision_category(directions, informative_null(rows, tables))
    if not all(gates.values()):
        category = "gate_failed"
    nested = {claim: nested_summary(qualified, claim) for claim in ("CM-12", "CM-13")}
    return {
        "horizon": horizon,
        "gates": gates,
        "category": category,
        "G1_details": access,
        "G2_details": identification,
        "directions": directions,
        "nested": nested,
    }


def claim_decisions(results: dict[str, Any]) -> dict[str, Any]:
    """Permit bounded C2 only when all horizons pass the registered criterion."""
    primary = results[str(RULES["primary_horizon_days"])]
    all_pass = all(all(item["gates"].values()) for item in results.values())
    claims: dict[str, Any] = {
        "CM-01": {
            "confidence": "C2"
            if all_pass
            and all(
                item["category"] == "bounded_reciprocal" for item in results.values()
            )
            else "C1",
            "domain": "ASF project-foundation relations; no necessity claim",
        }
    }
    mapping = "retain_observational_vocabulary"
    if not primary["gates"]["G1"]:
        mapping = "withhold_mapping_decision"
    elif not all(primary["gates"].values()) or primary["category"] == "indeterminate":
        mapping = "narrow_observational_applicability"
    claims["CM-04"] = {
        "confidence": "C1",
        "decision": mapping,
        "numerical_model_validated": False,
    }
    for claim in ("CM-12", "CM-13"):
        stable = all(
            item["nested"][claim]["category"] == "mixed" for item in results.values()
        )
        claims[claim] = {
            "confidence": "C2" if all_pass and stable else "C1",
            "domain": "ASF decision-authority layer",
            "direction": nested_decision(results, claim, all_pass, stable),
        }
    return claims


def nested_decision(
    results: dict[str, Any], claim: str, gates: bool, stable: bool
) -> str:
    """Separate failed identification from evidence against this instantiation."""
    if not gates:
        return "no_claim_level_direction"
    if stable:
        return "bounded_mixed_support"
    if all(not item["nested"][claim]["families"] for item in results.values()):
        return "against_this_instantiation"
    return "narrow_conditions"


def decision_report(tables: Tables, audit_passed: bool) -> dict[str, Any]:
    """Report all horizons, primary timing sensitivity, counts, and blocked fields."""
    results = {
        str(horizon): adjudicate_horizon(tables, horizon, audit_passed)
        for horizon in HORIZONS
    }
    primary = results[str(RULES["primary_horizon_days"])]
    changes = [
        horizon
        for horizon, item in results.items()
        if item["category"] != primary["category"]
        or any(
            primary["gates"][gate] and not passed
            for gate, passed in item["gates"].items()
        )
    ]
    counts = Counter(
        (
            row["horizon"],
            row["direction"],
            row["effect_sign"],
            row["decision_authority_shift"],
            row["coordination_disposition"],
        )
        for horizon in HORIZONS
        for row in horizon_rows(tables, horizon)
    )
    return {
        "primary_horizon": RULES["primary_horizon_days"],
        "horizons": results,
        "timing_sensitive": bool(changes),
        "changed_horizons": changes,
        "claims": claim_decisions(results),
        "descriptive_response_counts": [
            {"stratum": key, "count": value} for key, value in sorted(counts.items())
        ],
        "blocked_candidates": [
            {
                "record_id": row["record_id"],
                "conditions": {
                    field: row[field]
                    for field in (
                        "ordered_acts_met",
                        "receiver_conduct_met",
                        "linked_change_met",
                        "discriminating_contrast_met",
                        "missingness",
                    )
                },
            }
            for row in tables["measurements"]
            if not qualifies(row, tables)
        ],
    }
