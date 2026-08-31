"""Generate the antinomy parameter sweep and dependency-free SVG map."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Iterable

from .model import Parameters, classify, simulate


REGIMES = ("collapse", "equilibrium", "lock-in", "oscillation", "unresolved")
COLORS = {
    "collapse": "#4b5563",
    "equilibrium": "#2a9d8f",
    "lock-in": "#e9c46a",
    "oscillation": "#e76f51",
    "unresolved": "#d1d5db",
}
SEEDS = (7, 19, 41, 73, 101, 151, 211)
EXAMPLES = {
    "collapse": Parameters(support=-4.0, opposition=4.0),
    "equilibrium": Parameters(support=0.0, opposition=2.0),
    "lock-in": Parameters(support=0.0, opposition=6.0),
    "oscillation": Parameters(support=2.0, opposition=12.0),
}


def _values(start: float, stop: float, step: float) -> list[float]:
    count = round((stop - start) / step)
    return [round(start + index * step, 10) for index in range(count + 1)]


def sweep(
    supports: Iterable[float],
    oppositions: Iterable[float],
    *,
    seeds: tuple[int, ...] = SEEDS,
    steps: int = 600,
    tail: int = 100,
    collapse_threshold: float = 0.1,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for support in supports:
        for opposition in oppositions:
            counts = {regime: 0 for regime in REGIMES}
            for seed in seeds:
                result = classify(
                    simulate(
                        Parameters(support=support, opposition=opposition),
                        steps=steps,
                        seed=seed,
                    ),
                    tail=tail,
                    collapse_threshold=collapse_threshold,
                )
                counts[result.regime] += 1
            modal = max(REGIMES, key=lambda regime: (counts[regime], -REGIMES.index(regime)))
            nonzero = sum(count > 0 for count in counts.values())
            fixed_point = symmetric_fixed_point(
                Parameters(support=support, opposition=opposition)
            )
            slope = fixed_point * (1.0 - fixed_point)
            lambda_symmetric = slope * (4.0 - opposition)
            lambda_antisymmetric = slope * opposition
            rows.append(
                {
                    "support": support,
                    "opposition": opposition,
                    "modal_regime": modal,
                    "seed_disagreement": nonzero > 1,
                    "symmetric_fixed_point": f"{fixed_point:.10f}",
                    "lambda_symmetric": f"{lambda_symmetric:.10f}",
                    "lambda_antisymmetric": f"{lambda_antisymmetric:.10f}",
                    "symmetric_fixed_stable": abs(lambda_symmetric) < 1.0
                    and abs(lambda_antisymmetric) < 1.0,
                    **{f"n_{regime.replace('-', '_')}": counts[regime] for regime in REGIMES},
                }
            )
    return rows


def symmetric_fixed_point(parameters: Parameters) -> float:
    """Find the unique symmetric fixed point on the swept parameter domain."""

    net_coefficient = (
        parameters.persistence
        + parameters.mutual_enablement
        - parameters.opposition
    )

    def residual(state: float) -> float:
        logit = parameters.support + net_coefficient * state
        logit = max(-60.0, min(60.0, logit))
        return 1.0 / (1.0 + math.exp(-logit)) - state

    low, high = 0.0, 1.0
    for _ in range(80):
        midpoint = (low + high) / 2.0
        if residual(midpoint) > 0.0:
            low = midpoint
        else:
            high = midpoint
    return (low + high) / 2.0


def mark_transition_candidates(rows: list[dict[str, object]]) -> None:
    """Mark empirical regime edges and local-stability crossing cells.

    A local-stability crossing is a bifurcation candidate, not a proof of its
    normal form. Formal continuation is outside this model's claims.
    """

    lookup = {
        (float(row["support"]), float(row["opposition"])): row for row in rows
    }
    supports = sorted({key[0] for key in lookup})
    oppositions = sorted({key[1] for key in lookup})
    support_step = supports[1] - supports[0]
    opposition_step = oppositions[1] - oppositions[0]
    for (support, opposition), row in lookup.items():
        neighbours = [
            lookup.get((round(support + support_step, 10), opposition)),
            lookup.get((round(support - support_step, 10), opposition)),
            lookup.get((support, round(opposition + opposition_step, 10))),
            lookup.get((support, round(opposition - opposition_step, 10))),
        ]
        row["regime_transition_candidate"] = bool(row["seed_disagreement"]) or any(
            neighbour is not None
            and neighbour["modal_regime"] != row["modal_regime"]
            for neighbour in neighbours
        )
        stable = bool(row["symmetric_fixed_stable"])
        row["bifurcation_candidate"] = any(
            neighbour is not None
            and bool(neighbour["symmetric_fixed_stable"]) != stable
            for neighbour in neighbours
        )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def write_examples(path: Path) -> dict[str, str]:
    classifications: dict[str, str] = {}
    with path.open("w", encoding="utf-8", newline="") as handle:
        fields = ("example", "step", "autonomy", "coordination", "seed")
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for expected, parameters in EXAMPLES.items():
            trajectory = simulate(parameters, steps=200, seed=7)
            observed = classify(trajectory, tail=100).regime
            classifications[expected] = observed
            for index, (autonomy, coordination) in enumerate(
                zip(trajectory.autonomy, trajectory.coordination)
            ):
                writer.writerow(
                    {
                        "example": expected,
                        "step": index,
                        "autonomy": f"{autonomy:.10f}",
                        "coordination": f"{coordination:.10f}",
                        "seed": trajectory.seed,
                    }
                )
    return classifications


def write_robustness(path: Path) -> dict[str, int]:
    """Check representative regimes across horizons, seeds, and thresholds."""

    rows: list[dict[str, object]] = []
    for expected, parameters in EXAMPLES.items():
        for steps in (300, 600, 1200):
            for seed in SEEDS:
                observed = classify(
                    simulate(parameters, steps=steps, seed=seed), tail=100
                ).regime
                rows.append(
                    {
                        "check": "reference_horizon_seed",
                        "expected": expected,
                        "observed": observed,
                        "support": parameters.support,
                        "opposition": parameters.opposition,
                        "steps": steps,
                        "seed": seed,
                        "collapse_threshold": 0.1,
                    }
                )
    for threshold in (0.075, 0.1, 0.125):
        parameters = EXAMPLES["collapse"]
        for seed in SEEDS:
            observed = classify(
                simulate(parameters, steps=600, seed=seed),
                tail=100,
                collapse_threshold=threshold,
            ).regime
            rows.append(
                {
                    "check": "collapse_threshold",
                    "expected": "collapse",
                    "observed": observed,
                    "support": parameters.support,
                    "opposition": parameters.opposition,
                    "steps": 600,
                    "seed": seed,
                    "collapse_threshold": threshold,
                }
            )
    for support in (-4.0, -2.0, 0.0, 2.0):
        for seed in SEEDS:
            parameters = Parameters(
                support=support, opposition=2.0, mutual_enablement=2.0
            )
            observed = classify(simulate(parameters, steps=600, seed=seed)).regime
            rows.append(
                {
                    "check": "uncoupled_ablation",
                    "expected": "collapse_or_equilibrium",
                    "observed": observed,
                    "support": support,
                    "opposition": 2.0,
                    "steps": 600,
                    "seed": seed,
                    "collapse_threshold": 0.1,
                }
            )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
    failures = sum(
        row["observed"] != row["expected"]
        and not (
            row["expected"] == "collapse_or_equilibrium"
            and row["observed"] in {"collapse", "equilibrium"}
        )
        for row in rows
    )
    return {"checks": len(rows), "failures": failures}


def write_svg(path: Path, rows: list[dict[str, object]]) -> None:
    width, height = 1120, 760
    left, top, plot_width, plot_height = 105, 65, 820, 600
    supports = sorted({float(row["support"]) for row in rows})
    oppositions = sorted({float(row["opposition"]) for row in rows})
    cell_width = plot_width / len(oppositions)
    cell_height = plot_height / len(supports)
    lookup = {
        (float(row["support"]), float(row["opposition"])): row for row in rows
    }

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<style>text{font-family:system-ui,-apple-system,sans-serif;fill:#111827}.small{font-size:13px}.axis{font-size:15px}.title{font-size:23px;font-weight:650}.legend{font-size:14px}</style>',
        '<text x="105" y="32" class="title">Two-variable antinomy: modal long-run regime</text>',
        '<text x="105" y="53" class="small">Seven seeded initial conditions per cell; dots mark symmetric fixed-point stability crossings</text>',
    ]
    for y_index, support in enumerate(reversed(supports)):
        y = top + y_index * cell_height
        for x_index, opposition in enumerate(oppositions):
            x = left + x_index * cell_width
            row = lookup[(support, opposition)]
            color = COLORS[str(row["modal_regime"])]
            svg.append(
                f'<rect x="{x:.3f}" y="{y:.3f}" width="{cell_width + 0.2:.3f}" height="{cell_height + 0.2:.3f}" fill="{color}"/>'
            )
            if row["bifurcation_candidate"]:
                svg.append(
                    f'<circle cx="{x + cell_width / 2:.3f}" cy="{y + cell_height / 2:.3f}" r="1.35" fill="#111827" opacity="0.78"/>'
                )
    svg.append(
        f'<rect x="{left}" y="{top}" width="{plot_width}" height="{plot_height}" fill="none" stroke="#111827" stroke-width="1"/>'
    )
    for tick in range(0, 15, 2):
        x = left + (tick - oppositions[0]) / (oppositions[-1] - oppositions[0]) * plot_width
        svg.append(f'<line x1="{x:.2f}" y1="{top + plot_height}" x2="{x:.2f}" y2="{top + plot_height + 6}" stroke="#111827"/>')
        svg.append(f'<text x="{x:.2f}" y="{top + plot_height + 24}" text-anchor="middle" class="small">{tick}</text>')
    for tick in range(-6, 5, 2):
        y = top + (supports[-1] - tick) / (supports[-1] - supports[0]) * plot_height
        svg.append(f'<line x1="{left - 6}" y1="{y:.2f}" x2="{left}" y2="{y:.2f}" stroke="#111827"/>')
        svg.append(f'<text x="{left - 13}" y="{y + 4:.2f}" text-anchor="end" class="small">{tick}</text>')
    svg.extend(
        [
            f'<text x="{left + plot_width / 2}" y="{top + plot_height + 53}" text-anchor="middle" class="axis">opposition q (cross-inhibition)</text>',
            f'<text x="26" y="{top + plot_height / 2}" text-anchor="middle" class="axis" transform="rotate(-90 26 {top + plot_height / 2})">shared support b</text>',
            '<text x="965" y="92" class="axis" font-weight="650">Regime</text>',
        ]
    )
    for index, regime in enumerate(REGIMES):
        y = 118 + index * 34
        svg.append(f'<rect x="965" y="{y}" width="19" height="19" fill="{COLORS[regime]}"/>')
        svg.append(f'<text x="993" y="{y + 15}" class="legend">{regime}</text>')
    svg.extend(
        [
            '<circle cx="974" cy="314" r="2.2" fill="#111827"/>',
            '<text x="993" y="319" class="legend">bifurcation candidate</text>',
            '<text x="965" y="365" class="small">Fixed: p = 2, m = 2</text>',
            '<text x="965" y="386" class="small">Noise: 0</text>',
            '<text x="965" y="407" class="small">Steps: 600</text>',
            '<text x="965" y="448" class="small">Collapse is an operational</text>',
            '<text x="965" y="466" class="small">low-low viability threshold,</text>',
            '<text x="965" y="484" class="small">not a singularity.</text>',
            '</svg>',
        ]
    )
    path.write_text("\n".join(svg) + "\n", encoding="utf-8")


def generate(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    supports = _values(-6.0, 4.0, 0.25)
    oppositions = _values(0.0, 14.0, 0.25)
    rows = sweep(supports, oppositions)
    mark_transition_candidates(rows)
    write_csv(output_dir / "parameter_sweep.csv", rows)
    examples = write_examples(output_dir / "representative_trajectories.csv")
    robustness = write_robustness(output_dir / "robustness_checks.csv")
    write_svg(output_dir / "parameter_map.svg", rows)

    modal_counts = {regime: 0 for regime in REGIMES}
    regime_transition_count = 0
    bifurcation_count = 0
    seed_disagreement_count = 0
    for row in rows:
        modal_counts[str(row["modal_regime"])] += 1
        regime_transition_count += int(bool(row["regime_transition_candidate"]))
        bifurcation_count += int(bool(row["bifurcation_candidate"]))
        seed_disagreement_count += int(bool(row["seed_disagreement"]))
    summary: dict[str, object] = {
        "model": {
            "equations": [
                "A[t+1] = sigmoid(b + p*A[t] + (m-q)*C[t])",
                "C[t+1] = sigmoid(b + p*C[t] + (m-q)*A[t])",
            ],
            "fixed_parameters": {"persistence": 2.0, "mutual_enablement": 2.0, "noise": 0.0},
        },
        "sweep": {
            "support": {"minimum": -6.0, "maximum": 4.0, "step": 0.25},
            "opposition": {"minimum": 0.0, "maximum": 14.0, "step": 0.25},
            "seeds": list(SEEDS),
            "steps": 600,
            "tail": 100,
            "cells": len(rows),
        },
        "classification": {
            "collapse_threshold": 0.1,
            "lock_in_gap": 0.25,
            "tolerance": 1e-7,
            "oscillation_threshold": 0.05,
        },
        "modal_counts": modal_counts,
        "regime_transition_candidate_cells": regime_transition_count,
        "bifurcation_candidate_cells": bifurcation_count,
        "seed_disagreement_cells": seed_disagreement_count,
        "representative_classifications": examples,
        "robustness": robustness,
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).with_name("outputs"),
        help="directory for CSV, JSON, and SVG outputs",
    )
    arguments = parser.parse_args()
    summary = generate(arguments.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
