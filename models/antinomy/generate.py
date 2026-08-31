"""Generate every committed output for the minimal antinomy model."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from .render import (
    create_summary,
    write_parameter_map_svg,
    write_parameter_sweep_csv,
    write_representative_trajectories_csv,
    write_robustness_checks_csv,
    write_summary_json,
)
from .sweep import (
    SweepSettings,
    create_default_sweep_settings,
    generate_representative_trajectories,
    run_parameter_sweep,
    run_robustness_checks,
)


@dataclass(frozen=True)
class OutputPaths:
    """Name every generated artifact inside one output directory."""

    parameter_sweep_csv: Path
    representative_trajectories_csv: Path
    robustness_checks_csv: Path
    parameter_map_svg: Path
    summary_json: Path


def create_output_paths(output_directory: Path) -> OutputPaths:
    """Create the output directory and return all artifact paths."""
    output_directory.mkdir(parents=True, exist_ok=True)
    return OutputPaths(
        parameter_sweep_csv=output_directory / "parameter_sweep.csv",
        representative_trajectories_csv=(
            output_directory / "representative_trajectories.csv"
        ),
        robustness_checks_csv=output_directory / "robustness_checks.csv",
        parameter_map_svg=output_directory / "parameter_map.svg",
        summary_json=output_directory / "summary.json",
    )


def generate_outputs(
    output_directory: Path,
    *,
    sweep_settings: SweepSettings | None = None,
) -> dict[str, object]:
    """Run the model once and write all reproducible output artifacts."""
    output_paths = create_output_paths(output_directory)
    selected_settings = sweep_settings or create_default_sweep_settings()
    parameter_cells = run_parameter_sweep(selected_settings)
    representative_trajectories = generate_representative_trajectories()
    robustness_checks = run_robustness_checks()

    write_parameter_sweep_csv(
        output_paths.parameter_sweep_csv,
        parameter_cells,
    )
    write_representative_trajectories_csv(
        output_paths.representative_trajectories_csv,
        representative_trajectories,
    )
    write_robustness_checks_csv(
        output_paths.robustness_checks_csv,
        robustness_checks,
    )
    write_parameter_map_svg(
        output_paths.parameter_map_svg,
        parameter_cells,
        selected_settings,
    )

    summary = create_summary(
        parameter_cells,
        representative_trajectories,
        robustness_checks,
        selected_settings,
    )
    write_summary_json(output_paths.summary_json, summary)
    return summary


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for selecting an output directory."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).with_name("outputs"),
        help="directory for CSV, JSON, and SVG outputs",
    )
    return parser


def main() -> None:
    """Generate outputs and print their aggregate summary."""
    arguments = build_argument_parser().parse_args()
    summary = generate_outputs(arguments.output_dir)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
