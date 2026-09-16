"""Outcome-independent local baselines, contrast pairs, and solo audit frames."""

from __future__ import annotations

import math
from collections import defaultdict

from scripts.asf_audit.protocol import PROJECTS, RULES, Row, Tables, digest
from scripts.asf_audit.timing import event_date, primary_interval

SMALL_CORPUS_CENSUS_LIMIT = 8  # Registered in the codebook's G3 section.


def hash_key(*parts: str) -> str:
    """Hash the registered pipe-separated UTF-8 identifiers."""
    if any("|" in part for part in parts):
        raise ValueError("Sampling identifiers cannot contain pipes")
    return digest("|".join(parts).encode())


def quarter(value: str) -> str:
    """Return the calendar year-quarter key for an exact opening date."""
    day = event_date(value)
    return f"{day.year}-Q{(day.month - 1) // 3 + 1}"


def local_baseline(tables: Tables) -> list[Row]:
    """Log all 48 strata, their screened counts, hash keys, and selected IDs."""
    groups: dict[tuple[str, str], list[Row]] = defaultdict(list)
    for row in tables["screening"]:
        if row["eligible"] == "yes" and row["kind"] == "local_release":
            groups[row["project"], quarter(row["opening_date"])].append(row)
    return [
        baseline_stratum(project, f"{year}-Q{number}", groups)
        for project in PROJECTS
        for year in range(RULES["primary_start"].year, RULES["primary_end"].year + 1)
        for number in range(1, 5)
    ]


def baseline_stratum(
    project: str,
    block: str,
    groups: dict[tuple[str, str], list[Row]],
) -> Row:
    """Select a release opening, retaining its underlying family identity."""
    candidates = sorted(
        groups[project, block],
        key=lambda row: (hash_key(project, block, row["source_id"]), row["source_id"]),
    )
    selected = candidates[0] if candidates else {}
    return {
        "project": project,
        "quarter": block,
        "count": str(len(candidates)),
        "ordered_source_ids": ";".join(row["source_id"] for row in candidates),
        "ordered_hashes": ";".join(
            hash_key(project, block, row["source_id"]) for row in candidates
        ),
        "source_id": selected.get("source_id", ""),
        "family_id": selected.get("family_id", ""),
        "hash": hash_key(project, block, selected["source_id"]) if selected else "",
    }


def eligible_pairs(tables: Tables) -> set[tuple[str, str]]:
    """Return the full eligible screening universe, including unsampled releases."""
    return {
        (row["family_id"], row["project"])
        for row in tables["screening"]
        if row["eligible"] == "yes"
    }


def analysis_pairs(tables: Tables) -> set[tuple[str, str]]:
    """Admit the census and only the registered routine-release baseline."""
    census = {
        (row["family_id"], row["project"])
        for row in tables["screening"]
        if row["eligible"] == "yes" and row["kind"] != "local_release"
    }
    return census | {
        (row["family_id"], row["project"])
        for row in local_baseline(tables)
        if row["source_id"]
    }


def audit_frame(tables: Tables) -> list[str]:
    """Select every opportunity and the registered nonopportunity strata union."""
    eligible = eligible_pairs(tables)
    families = {family for family, _ in eligible}
    opportunities = {
        row["family_id"]
        for row in tables["measurements"]
        if row["opportunity"] == "yes" and row["family_id"] in families
    }
    if len(families) < SMALL_CORPUS_CENSUS_LIMIT:
        return sorted(families, key=lambda family: (digest(family.encode()), family))
    strata: dict[tuple[str, str], list[str]] = defaultdict(list)
    for row in tables["families"]:
        if (row["family_id"], row["project"]) in eligible and row[
            "family_id"
        ] not in opportunities:
            strata[row["project"], row["initiating_role"]].append(row["family_id"])
    selected = set(opportunities)
    for (project, role), members in strata.items():
        ordered = sorted(
            set(members), key=lambda family: (hash_key(project, role, family), family)
        )
        count = max(
            1, math.ceil(len(ordered) * RULES["nonopportunity_recode_fraction"])
        )
        selected.update(ordered[:count])
    return sorted(selected, key=lambda family: (digest(family.encode()), family))


def comparator(family: Row, families: list[Row]) -> str:
    """Choose earliest alternate exposure, same year then either adjacent year."""
    if family["exposure"] == "unknown" or family["onset_earliest"] == "unknown":
        return ""
    year = event_date(family["onset_earliest"]).year
    candidates = [other for other in families if comparison_eligible(family, other)]
    for distance in (0, 1):
        subset = [
            other
            for other in candidates
            if abs(event_date(other["onset_earliest"]).year - year) == distance
        ]
        if subset:
            return min(
                subset,
                key=lambda row: (
                    event_date(row["onset_earliest"]),
                    row["earliest_source_id"],
                    row["family_id"],
                ),
            )["family_id"]
    return ""


def comparison_eligible(family: Row, other: Row) -> bool:
    """Exclude same-family, unknown-exposure, unmatched-class, and undated rows."""
    return (
        other["family_id"] != family["family_id"]
        and other["project"] == family["project"]
        and other["action_class"] == family["action_class"]
        and other["exposure"] not in (family["exposure"], "unknown")
        and other["onset_earliest"] != "unknown"
        and primary_interval(other["onset_earliest"], other["onset_latest"])
    )
