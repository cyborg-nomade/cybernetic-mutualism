"""Render antinomy sweep results as transparent data and an SVG map."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .model import (
    Regime,
    SimulationTrajectory,
    classify_trajectory,
)
from .sweep import (
    REGIME_ORDER,
    ParameterCellResult,
    RobustnessCheck,
    SweepSettings,
)

type CsvValue = str | int | float | bool
type CsvRow = dict[str, CsvValue]
REGIME_COLORS: dict[Regime, str] = {
    "collapse": "#4b5563",
    "equilibrium": "#2a9d8f",
    "lock-in": "#e9c46a",
    "oscillation": "#e76f51",
    "unresolved": "#d1d5db",
}

SVG_WIDTH = 1120
SVG_HEIGHT = 760
PLOT_LEFT = 105
PLOT_TOP = 65
PLOT_WIDTH = 820
PLOT_HEIGHT = 600


def write_csv_file(output_path: Path, rows: list[CsvRow]) -> None:
    """Write dictionaries as a deterministic CSV file with Unix line endings."""
    if not rows:
        message = "cannot write a CSV file without rows"
        raise ValueError(message)
    with output_path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def parameter_cell_to_csv_row(cell: ParameterCellResult) -> CsvRow:
    """Convert one parameter-cell result to its public tabular schema."""
    stability = cell.fixed_point_stability
    counts = cell.regime_counts
    return {
        "support": cell.shared_support,
        "opposition": cell.cross_inhibition,
        "modal_regime": cell.modal_regime,
        "seed_disagreement": cell.seeds_disagree,
        "symmetric_fixed_point": f"{stability.symmetric_fixed_point:.10f}",
        "lambda_symmetric": f"{stability.symmetric_eigenvalue:.10f}",
        "lambda_antisymmetric": f"{stability.antisymmetric_eigenvalue:.10f}",
        "symmetric_fixed_stable": stability.is_stable,
        "n_collapse": counts.collapse,
        "n_equilibrium": counts.equilibrium,
        "n_lock_in": counts.lock_in,
        "n_oscillation": counts.oscillation,
        "n_unresolved": counts.unresolved,
        "regime_transition_candidate": cell.borders_regime_transition,
        "bifurcation_candidate": cell.borders_stability_change,
    }


def write_parameter_sweep_csv(
    output_path: Path,
    cells: list[ParameterCellResult],
) -> None:
    """Write every parameter cell, classification count, and stability result."""
    rows = [parameter_cell_to_csv_row(cell) for cell in cells]
    write_csv_file(output_path, rows)


def representative_trajectory_rows(
    trajectories: dict[Regime, SimulationTrajectory],
) -> list[CsvRow]:
    """Convert complete representative trajectories to CSV rows."""
    rows: list[CsvRow] = []
    for expected_regime, trajectory in trajectories.items():
        for step_number, state in enumerate(trajectory.states):
            rows.append(
                {
                    "example": expected_regime,
                    "step": step_number,
                    "autonomy": f"{state.autonomy_capacity:.10f}",
                    "coordination": f"{state.coordination_capacity:.10f}",
                    "seed": trajectory.random_seed,
                }
            )
    return rows


def write_representative_trajectories_csv(
    output_path: Path,
    trajectories: dict[Regime, SimulationTrajectory],
) -> None:
    """Write the complete trajectory for each named regime example."""
    write_csv_file(output_path, representative_trajectory_rows(trajectories))


def robustness_check_to_csv_row(check: RobustnessCheck) -> CsvRow:
    """Convert one robustness result to its public tabular schema."""
    return {
        "check": check.check_name,
        "expected": check.expected_regime,
        "observed": check.observed_regime,
        "support": check.shared_support,
        "opposition": check.cross_inhibition,
        "steps": check.number_of_steps,
        "seed": check.random_seed,
        "collapse_threshold": check.collapse_capacity,
    }


def write_robustness_checks_csv(
    output_path: Path,
    checks: list[RobustnessCheck],
) -> None:
    """Write every robustness check and its observed classification."""
    rows = [robustness_check_to_csv_row(check) for check in checks]
    write_csv_file(output_path, rows)


def count_modal_regimes(cells: list[ParameterCellResult]) -> dict[Regime, int]:
    """Count the modal classification assigned to each parameter cell."""
    counts = dict.fromkeys(REGIME_ORDER, 0)
    for cell in cells:
        counts[cell.modal_regime] += 1
    return counts


def classify_representative_trajectories(
    trajectories: dict[Regime, SimulationTrajectory],
) -> dict[Regime, Regime]:
    """Record the observed label for every representative trajectory."""
    return {
        expected_regime: classify_trajectory(trajectory).regime
        for expected_regime, trajectory in trajectories.items()
    }


def create_summary(
    cells: list[ParameterCellResult],
    trajectories: dict[Regime, SimulationTrajectory],
    checks: list[RobustnessCheck],
    settings: SweepSettings,
) -> dict[str, object]:
    """Create the machine-readable summary of methods and aggregate results."""
    thresholds = settings.classification_thresholds
    parameter_grid = settings.parameter_grid
    return {
        "model": {
            "equations": [
                "A[t+1] = sigmoid(b + p*A[t] + (m-q)*C[t])",
                "C[t+1] = sigmoid(b + p*C[t] + (m-q)*A[t])",
            ],
            "fixed_parameters": {
                "persistence": settings.self_reinforcement,
                "mutual_enablement": settings.cross_enablement,
                "noise": settings.shock_standard_deviation,
            },
        },
        "sweep": {
            "support": describe_axis(parameter_grid.shared_support_values),
            "opposition": describe_axis(parameter_grid.cross_inhibition_values),
            "seeds": list(settings.random_seeds),
            "steps": settings.number_of_steps,
            "tail": thresholds.tail_length,
            "cells": len(cells),
        },
        "classification": {
            "collapse_threshold": thresholds.collapse_capacity,
            "lock_in_gap": thresholds.lock_in_gap,
            "tolerance": thresholds.numerical_tolerance,
            "oscillation_threshold": thresholds.minimum_oscillation_amplitude,
        },
        "modal_counts": count_modal_regimes(cells),
        "regime_transition_candidate_cells": sum(
            cell.borders_regime_transition for cell in cells
        ),
        "bifurcation_candidate_cells": sum(
            cell.borders_stability_change for cell in cells
        ),
        "seed_disagreement_cells": sum(cell.seeds_disagree for cell in cells),
        "representative_classifications": classify_representative_trajectories(
            trajectories
        ),
        "robustness": {
            "checks": len(checks),
            "failures": sum(not check.passed for check in checks),
        },
    }


def describe_axis(values: tuple[float, ...]) -> dict[str, float]:
    """Summarize the minimum, maximum, and increment of a regular grid axis."""
    return {
        "minimum": values[0],
        "maximum": values[-1],
        "step": values[1] - values[0],
    }


def write_summary_json(output_path: Path, summary: dict[str, object]) -> None:
    """Write the aggregate methods and results as deterministic JSON."""
    output_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def scale_x_coordinate(
    cross_inhibition: float,
    minimum_cross_inhibition: float,
    maximum_cross_inhibition: float,
) -> float:
    """Map cross-inhibition from parameter space to the SVG plot width."""
    parameter_fraction = (cross_inhibition - minimum_cross_inhibition) / (
        maximum_cross_inhibition - minimum_cross_inhibition
    )
    return PLOT_LEFT + parameter_fraction * PLOT_WIDTH


def scale_y_coordinate(
    shared_support: float,
    minimum_shared_support: float,
    maximum_shared_support: float,
) -> float:
    """Map shared support from parameter space to the inverted SVG y-axis."""
    parameter_fraction = (maximum_shared_support - shared_support) / (
        maximum_shared_support - minimum_shared_support
    )
    return PLOT_TOP + parameter_fraction * PLOT_HEIGHT


def render_svg_header() -> list[str]:
    """Render the SVG document start, styles, title, and subtitle."""
    return [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" '
            f'height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">'
        ),
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        (
            "<style>text{font-family:system-ui,-apple-system,sans-serif;"
            "fill:#111827}.small{font-size:13px}.axis{font-size:15px}"
            ".title{font-size:23px;font-weight:650}.legend{font-size:14px}"
            "</style>"
        ),
        (
            '<text x="105" y="32" class="title">Two-variable antinomy: '
            "modal long-run regime</text>"
        ),
        (
            '<text x="105" y="53" class="small">Seven seeded initial '
            "conditions per cell; dots mark symmetric fixed-point stability "
            "crossings</text>"
        ),
    ]


def render_parameter_cells(
    cells: list[ParameterCellResult],
    settings: SweepSettings,
) -> list[str]:
    """Render colored grid cells and fixed-point stability markers."""
    support_values = settings.parameter_grid.shared_support_values
    inhibition_values = settings.parameter_grid.cross_inhibition_values
    cell_width = PLOT_WIDTH / len(inhibition_values)
    cell_height = PLOT_HEIGHT / len(support_values)
    cell_by_coordinates = {cell.coordinates: cell for cell in cells}
    svg_elements: list[str] = []

    for row_number, shared_support in enumerate(reversed(support_values)):
        y_coordinate = PLOT_TOP + row_number * cell_height
        for column_number, cross_inhibition in enumerate(inhibition_values):
            x_coordinate = PLOT_LEFT + column_number * cell_width
            cell = cell_by_coordinates[(shared_support, cross_inhibition)]
            fill_color = REGIME_COLORS[cell.modal_regime]
            svg_elements.append(
                f'<rect x="{x_coordinate:.3f}" y="{y_coordinate:.3f}" '
                f'width="{cell_width + 0.2:.3f}" '
                f'height="{cell_height + 0.2:.3f}" fill="{fill_color}"/>'
            )
            if cell.borders_stability_change:
                svg_elements.append(
                    f'<circle cx="{x_coordinate + cell_width / 2:.3f}" '
                    f'cy="{y_coordinate + cell_height / 2:.3f}" r="1.35" '
                    'fill="#111827" opacity="0.78"/>'
                )
    return svg_elements


def render_plot_border() -> str:
    """Render the outline around the parameter grid."""
    return (
        f'<rect x="{PLOT_LEFT}" y="{PLOT_TOP}" width="{PLOT_WIDTH}" '
        f'height="{PLOT_HEIGHT}" fill="none" stroke="#111827" '
        'stroke-width="1"/>'
    )


def render_horizontal_axis(settings: SweepSettings) -> list[str]:
    """Render cross-inhibition tick marks and labels."""
    inhibition_values = settings.parameter_grid.cross_inhibition_values
    minimum_inhibition = inhibition_values[0]
    maximum_inhibition = inhibition_values[-1]
    axis_bottom = PLOT_TOP + PLOT_HEIGHT
    svg_elements: list[str] = []
    for tick_value in range(0, 15, 2):
        x_coordinate = scale_x_coordinate(
            tick_value,
            minimum_inhibition,
            maximum_inhibition,
        )
        svg_elements.extend(
            [
                f'<line x1="{x_coordinate:.2f}" y1="{axis_bottom}" '
                f'x2="{x_coordinate:.2f}" y2="{axis_bottom + 6}" '
                'stroke="#111827"/>',
                f'<text x="{x_coordinate:.2f}" y="{axis_bottom + 24}" '
                f'text-anchor="middle" class="small">{tick_value}</text>',
            ]
        )
    return svg_elements


def render_vertical_axis(settings: SweepSettings) -> list[str]:
    """Render shared-support tick marks and labels."""
    support_values = settings.parameter_grid.shared_support_values
    minimum_support = support_values[0]
    maximum_support = support_values[-1]
    svg_elements: list[str] = []
    for tick_value in range(-6, 5, 2):
        y_coordinate = scale_y_coordinate(
            tick_value,
            minimum_support,
            maximum_support,
        )
        svg_elements.extend(
            [
                f'<line x1="{PLOT_LEFT - 6}" y1="{y_coordinate:.2f}" '
                f'x2="{PLOT_LEFT}" y2="{y_coordinate:.2f}" '
                'stroke="#111827"/>',
                f'<text x="{PLOT_LEFT - 13}" y="{y_coordinate + 4:.2f}" '
                f'text-anchor="end" class="small">{tick_value}</text>',
            ]
        )
    return svg_elements


def render_axis_titles() -> list[str]:
    """Render the explanatory titles for both parameter axes."""
    axis_bottom = PLOT_TOP + PLOT_HEIGHT
    vertical_center = PLOT_TOP + PLOT_HEIGHT / 2
    return [
        f'<text x="{PLOT_LEFT + PLOT_WIDTH / 2}" y="{axis_bottom + 53}" '
        'text-anchor="middle" class="axis">opposition q '
        "(cross-inhibition)</text>",
        f'<text x="26" y="{vertical_center}" text-anchor="middle" '
        f'class="axis" transform="rotate(-90 26 {vertical_center})">'
        "shared support b</text>",
    ]


def render_legend(settings: SweepSettings) -> list[str]:
    """Render regime colors, marker meaning, and fixed sweep parameters."""
    svg_elements = ['<text x="965" y="92" class="axis" font-weight="650">Regime</text>']
    for legend_index, regime in enumerate(REGIME_ORDER):
        y_coordinate = 118 + legend_index * 34
        svg_elements.extend(
            [
                f'<rect x="965" y="{y_coordinate}" width="19" height="19" '
                f'fill="{REGIME_COLORS[regime]}"/>',
                f'<text x="993" y="{y_coordinate + 15}" class="legend">{regime}</text>',
            ]
        )
    svg_elements.extend(
        [
            '<circle cx="974" cy="314" r="2.2" fill="#111827"/>',
            ('<text x="993" y="319" class="legend">bifurcation candidate</text>'),
            (
                f'<text x="965" y="365" class="small">Fixed: p = '
                f"{settings.self_reinforcement:g}, m = "
                f"{settings.cross_enablement:g}</text>"
            ),
            (
                f'<text x="965" y="386" class="small">Noise: '
                f"{settings.shock_standard_deviation:g}</text>"
            ),
            (
                f'<text x="965" y="407" class="small">Steps: '
                f"{settings.number_of_steps}</text>"
            ),
            '<text x="965" y="448" class="small">Collapse is an operational</text>',
            '<text x="965" y="466" class="small">low-low viability threshold,</text>',
            '<text x="965" y="484" class="small">not a singularity.</text>',
        ]
    )
    return svg_elements


def write_parameter_map_svg(
    output_path: Path,
    cells: list[ParameterCellResult],
    settings: SweepSettings,
) -> None:
    """Write a dependency-free visual map of modal parameter-cell regimes."""
    svg_elements = [
        *render_svg_header(),
        *render_parameter_cells(cells, settings),
        render_plot_border(),
        *render_horizontal_axis(settings),
        *render_vertical_axis(settings),
        *render_axis_titles(),
        *render_legend(settings),
        "</svg>",
    ]
    output_path.write_text("\n".join(svg_elements) + "\n", encoding="utf-8")
