"""Measure finite-grid survival and boundary changes without bifurcation claims."""

from __future__ import annotations

import csv
from collections import Counter
from itertools import pairwise
from pathlib import Path
from typing import Literal

from models.antinomy.sweep import REGIME_ORDER, ParameterGrid

from .experiment import BASELINE_NAME, Cell, ScenarioResult

MINIMUM_SURVIVAL_CELLS = 5
MINIMUM_AGREEMENT = 4
NAMED_REGIMES = REGIME_ORDER[:-1]
Decision = Literal["retain", "narrow", "reject-extension", "withhold"]
Edge = tuple[str, float, float, float, float]


def surviving_regimes(cells: tuple[Cell, ...]) -> dict[str, bool]:
    """Apply the frozen five-cell, four-seed finite-grid criterion."""
    counts = Counter(
        cell.modal for cell in cells if cell.agreement >= MINIMUM_AGREEMENT
    )
    return {
        regime: counts[regime] >= MINIMUM_SURVIVAL_CELLS for regime in NAMED_REGIMES
    }


def decide(
    survival: list[dict[str, bool]],
    *,
    baseline_verified: bool,
    controls_clean: bool,
) -> Decision:
    """Apply baseline failure, rejection, narrowing, then retention precedence."""
    if not baseline_verified or not survival:
        return "withhold"
    if not any(item["equilibrium"] and item["lock-in"] for item in survival[1:]):
        return "reject-extension"
    if not controls_clean or not all(all(item.values()) for item in survival):
        return "narrow"
    return "retain"


def transition_edges(cells: tuple[Cell, ...], grid: ParameterGrid) -> set[Edge]:
    """Locate adjacent horizontal and vertical modal-label changes."""
    lookup = {(cell.support, cell.inhibition): cell.modal for cell in cells}
    edges: set[Edge] = set()
    for inhibition in grid.cross_inhibition_values:
        for left, right in pairwise(grid.shared_support_values):
            if lookup[left, inhibition] != lookup[right, inhibition]:
                edges.add(("support", left, inhibition, right, inhibition))
    for support in grid.shared_support_values:
        for lower, upper in pairwise(grid.cross_inhibition_values):
            if lookup[support, lower] != lookup[support, upper]:
                edges.add(("inhibition", support, lower, support, upper))
    return edges


def intersection_over_union(first: set[object], second: set[object]) -> float | None:
    """Return overlap, or null when neither set contains an observation."""
    union = first | second
    return len(first & second) / len(union) if union else None


def original_baseline_matches(result: ScenarioResult, original_csv: Path) -> bool:
    """Compare every coordinate, modal label, and seed count with archived output."""
    with original_csv.open(newline="", encoding="utf-8") as source:
        original = list(csv.DictReader(source))
    if result.scenario.name != BASELINE_NAME or len(original) != len(result.cells):
        return False
    return all(
        cell_matches_record(cell, row)
        for cell, row in zip(result.cells, original, strict=True)
    )


def cell_matches_record(cell: Cell, row: dict[str, str]) -> bool:
    """Check coordinate identity and all regime counts in one archived row."""
    coordinates_match = cell.support == float(
        row["support"]
    ) and cell.inhibition == float(row["opposition"])
    counts_match = all(
        count == int(row[f"n_{regime.replace('-', '_')}"])
        for regime, count in cell.counts.as_mapping().items()
    )
    return coordinates_match and cell.modal == row["modal_regime"] and counts_match


def scenario_summary(
    result: ScenarioResult,
    baseline: ScenarioResult,
    grid: ParameterGrid,
) -> dict[str, object]:
    """Summarize survival, matched-grid movement, and uncoupled rival outcomes."""
    counts = Counter(cell.modal for cell in result.cells)
    robust_counts = Counter(
        cell.modal for cell in result.cells if cell.agreement >= MINIMUM_AGREEMENT
    )
    edges = transition_edges(result.cells, grid)
    baseline_edges = transition_edges(baseline.cells, grid)
    return {
        "scenario": result.scenario.name,
        "modal_counts": {regime: counts[regime] for regime in REGIME_ORDER},
        "four_seed_modal_counts": {
            regime: robust_counts[regime] for regime in REGIME_ORDER
        },
        "survives": surviving_regimes(result.cells),
        "seed_disagreement_cells": sum(
            len(set(cell.labels)) > 1 for cell in result.cells
        ),
        "changed_modal_cells": sum(
            cell.modal != reference.modal
            for cell, reference in zip(result.cells, baseline.cells, strict=True)
        ),
        "matched_modal_fraction": sum(
            cell.modal == reference.modal
            for cell, reference in zip(result.cells, baseline.cells, strict=True)
        )
        / len(result.cells),
        "regime_iou": regime_overlap(result.cells, baseline.cells),
        "transition_edges": len(edges),
        "changed_transition_edges": len(edges ^ baseline_edges),
        "transition_edge_iou": intersection_over_union(set(edges), set(baseline_edges)),
        "uncoupled_seed_counts": dict(
            sorted(
                Counter(
                    label for cell in result.controls for label in cell.labels
                ).items()
            )
        ),
        "uncoupled_forbidden_labels": sum(
            label in ("lock-in", "oscillation")
            for cell in result.controls
            for label in cell.labels
        ),
    }


def regime_overlap(
    cells: tuple[Cell, ...], baseline: tuple[Cell, ...]
) -> dict[str, float | None]:
    """Measure matched-coordinate overlap for each modal regime."""
    return {
        regime: intersection_over_union(
            {(cell.support, cell.inhibition) for cell in cells if cell.modal == regime},
            {
                (cell.support, cell.inhibition)
                for cell in baseline
                if cell.modal == regime
            },
        )
        for regime in REGIME_ORDER
    }
