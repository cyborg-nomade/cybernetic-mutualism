set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

# Show the available project commands.
default:
    @just --list

# Install the locked runtime and development environment.
sync:
    uv sync --locked

# Regenerate the committed antinomy sweep and visual map.
model:
    uv run --locked python -m models.antinomy.generate

# Run the frozen 18-scenario structural robustness experiment.
robustness:
    uv run --locked python -m models.antinomy_robustness.generate --workers 4

# Independently regenerate and compare every structural robustness artifact.
robustness-check:
    #!/usr/bin/env bash
    set -euo pipefail
    output_directory="$(mktemp -d)"
    trap 'rm -rf "${output_directory}"' EXIT
    uv run --locked python -m models.antinomy_robustness.generate \
        --workers 4 --output-dir "${output_directory}" >/dev/null
    diff -rq models/antinomy_robustness/outputs "${output_directory}"

# Verify that fresh model outputs match the committed artifacts byte for byte.
model-check:
    #!/usr/bin/env bash
    set -euo pipefail
    output_directory="$(mktemp -d)"
    trap 'rm -rf "${output_directory}"' EXIT
    uv run --locked python -m models.antinomy.generate \
        --output-dir "${output_directory}" >/dev/null
    diff -rq models/antinomy/outputs "${output_directory}"

# Run the complete test suite.
test:
    uv run --locked pytest

# Run tests with branch coverage and produce coverage.xml for SonarQube.
coverage:
    uv run --locked pytest \
        --cov=models \
        --cov=scripts \
        --cov-report=term-missing \
        --cov-report=xml

# Check code correctness, complexity, documentation, and formatting.
lint:
    uv run --locked ruff check .
    uv run --locked ruff format --check .

# Apply deterministic Python formatting and safe lint fixes.
format:
    uv run --locked ruff check --fix .
    uv run --locked ruff format .

# Type-check production Python under strict mypy rules.
typecheck:
    uv run --locked mypy

# Run every local quality gate used by continuous integration.
check: lint typecheck coverage model-check robustness-check

# Send coverage and static-analysis results to a configured SonarQube server.
sonar: coverage
    command -v sonar-scanner >/dev/null || { \
        echo "sonar-scanner is required; install it and set SONAR_HOST_URL and SONAR_TOKEN" >&2; \
        exit 1; \
    }
    sonar-scanner
