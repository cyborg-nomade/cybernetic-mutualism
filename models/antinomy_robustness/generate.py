"""Generate deterministic structural robustness data, diagnostics, and maps."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from pathlib import Path

from .analysis import (
    decide,
    original_baseline_matches,
    scenario_summary,
    surviving_regimes,
    transition_edges,
)
from .experiment import (
    Cell,
    ExperimentSettings,
    ScenarioResult,
    run_scenario,
    scenarios,
    witness_rows,
)
from .render import render_maps

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "outputs"
PROTOCOL_PATH = REPOSITORY_ROOT / "research/experiments/antinomy-robustness-protocol.md"
BASELINE_CSV = REPOSITORY_ROOT / "models/antinomy/outputs/parameter_sweep.csv"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write explicit ordered columns and portable line endings."""
    if not rows:
        raise ValueError("CSV output needs at least one row")
    with path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(
            destination, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def cell_row(
    cell: Cell, result: ScenarioResult, settings: ExperimentSettings
) -> dict[str, object]:
    """Expose every seeded label alongside modal agreement and scenario factors."""
    return {
        "scenario": result.scenario.name,
        **asdict(result.scenario),
        "support": cell.support,
        "inhibition": cell.inhibition,
        **{
            f"seed_{seed}": label
            for seed, label in zip(settings.seeds, cell.labels, strict=True)
        },
        "modal_regime": cell.modal,
        "agreement": cell.agreement,
        "seed_disagreement": len(set(cell.labels)) > 1,
    }


def edge_rows(
    results: tuple[ScenarioResult, ...], settings: ExperimentSettings
) -> list[dict[str, object]]:
    """Retain the exact adjacent-cell coordinates of each classifier boundary."""
    return [
        {
            "scenario": result.scenario.name,
            "axis": edge[0],
            "support_from": edge[1],
            "inhibition_from": edge[2],
            "support_to": edge[3],
            "inhibition_to": edge[4],
        }
        for result in results
        for edge in sorted(transition_edges(result.cells, settings.grid))
    ]


def create_summary(
    results: tuple[ScenarioResult, ...], settings: ExperimentSettings
) -> dict[str, object]:
    """Record the executed design and apply the frozen rule only to full runs."""
    full_protocol = settings == ExperimentSettings()
    baseline_verified = full_protocol and original_baseline_matches(
        results[0], BASELINE_CSV
    )
    controls_clean = all(
        label not in ("lock-in", "oscillation")
        for result in results
        for cell in result.controls
        for label in cell.labels
    )
    return {
        "schema_version": 1,
        "protocol_sha256": hashlib.sha256(PROTOCOL_PATH.read_bytes()).hexdigest(),
        "full_protocol": full_protocol,
        "settings": asdict(settings),
        "baseline_verified": baseline_verified,
        "controls_clean": controls_clean,
        "decision": decide(
            [surviving_regimes(result.cells) for result in results],
            baseline_verified=baseline_verified,
            controls_clean=controls_clean,
        ),
        "scenarios": [
            scenario_summary(result, results[0], settings.grid) for result in results
        ],
    }


def write_outputs(
    output: Path,
    results: tuple[ScenarioResult, ...],
    settings: ExperimentSettings,
) -> dict[str, object]:
    """Separate raw classifications, controls, boundaries, witnesses, and summaries."""
    output.mkdir(parents=True, exist_ok=True)
    write_csv(
        output / "parameter_sweep.csv",
        [
            cell_row(cell, result, settings)
            for result in results
            for cell in result.cells
        ],
    )
    write_csv(
        output / "uncoupled_controls.csv",
        [
            cell_row(cell, result, settings)
            for result in results
            for cell in result.controls
        ],
    )
    boundaries = edge_rows(results, settings)
    if boundaries:
        write_csv(output / "transition_edges.csv", boundaries)
    else:
        (output / "transition_edges.csv").write_text(
            "scenario,axis,support_from,inhibition_from,support_to,inhibition_to\n",
            encoding="utf-8",
        )
    write_csv(
        output / "witness_checks.csv",
        [row for result in results for row in witness_rows(result.scenario, settings)],
    )
    summary = create_summary(results, settings)
    (output / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "regime_maps.svg").write_text(
        render_maps(results, settings.grid), encoding="utf-8"
    )
    return summary


def generate(
    output: Path, settings: ExperimentSettings, *, workers: int = 1
) -> dict[str, object]:
    """Execute scenarios in parallel while preserving deterministic artifact order."""
    if workers < 1:
        raise ValueError("workers must be positive")
    tasks = [(scenario, settings) for scenario in scenarios()]
    if workers == 1:
        results = tuple(map(run_scenario, tasks))
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            results = tuple(executor.map(run_scenario, tasks))
    return write_outputs(output, results, settings)


def main() -> None:
    """Run the complete frozen design; smaller designs are available only via Python."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--workers", type=int, default=1)
    arguments = parser.parse_args()
    summary = generate(
        arguments.output_dir, ExperimentSettings(), workers=arguments.workers
    )
    print(f"Generated structural robustness artifacts: {summary['decision']}")
    if not summary["baseline_verified"]:
        raise SystemExit("Baseline reproduction failed; scientific decision withheld")


if __name__ == "__main__":
    main()
