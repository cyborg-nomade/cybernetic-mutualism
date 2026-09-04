# Python development

## Quick start

Install [uv](https://docs.astral.sh/uv/) and
[just](https://github.com/casey/just), then run:

```bash
just sync
just check
```

`uv` creates an isolated `.venv` and installs the exact versions recorded in
`uv.lock`. `just check` runs the same formatting, linting, type, test, coverage,
and model-reproduction gates used in continuous integration.

## Common recipes

| Recipe | Purpose |
| --- | --- |
| `just` | List available recipes |
| `just model` | Regenerate the committed antinomy outputs |
| `just model-check` | Generate into a temporary directory and compare every artifact byte for byte |
| `just robustness` | Run the frozen 18-scenario antinomy structural experiment |
| `just robustness-check` | Independently reproduce every structural experiment artifact |
| `just test` | Run the pytest suite |
| `just coverage` | Run tests with branch coverage and create `coverage.xml` |
| `just lint` | Check Ruff rules and deterministic formatting |
| `just format` | Apply Ruff formatting and safe automatic fixes |
| `just typecheck` | Run strict mypy over production code |
| `just check` | Run all local and continuous-integration quality gates |
| `just sonar` | Generate coverage and run a configured SonarScanner |

Run a tool directly through the locked environment when no recipe is needed:

```bash
uv run --locked python -m models.antinomy.generate --help
uv run --locked pytest tests/test_antinomy_model.py
```

The full `just check` includes both model sweeps and can take several minutes.
For fast feedback while editing, run `just lint typecheck test`. Structural
robustness generation uses four processes, with deterministic output ordering;
pass `--workers 1` to its Python module for a serial run. Scientific failure of
a robustness hypothesis is a valid result, not a failing test. Failure to
reproduce the archived baseline or committed artifacts is a failing gate.

## Readability standard

Code in this repository is part of the scientific argument. A reader should be
able to connect a variable, transformation, test, and output to the research
note without reverse-engineering implementation shorthand.

New Python code should therefore:

- use domain names in code and reserve compact symbols for displayed equations;
- give every module, public class, and public function a useful docstring;
- separate model calculation, classification, parameter sweeping, rendering,
  and file output;
- prefer small single-purpose functions and keep McCabe complexity at or below
  eight;
- make units, bounds, seeds, thresholds, and defaults explicit;
- use type annotations to make inputs and outputs inspectable before execution;
- explain *why* a surprising choice exists instead of narrating obvious syntax;
- raise specific errors at invalid boundaries rather than permitting silent
  coercion;
- name tests after the scientific invariant or behavior they protect;
- preserve unresolved or negative outcomes rather than forcing a successful
  classification;
- keep generated data reproducible and separate from handwritten source.

Ruff checks formatting, imports, common correctness errors, simplifications,
naming, docstrings, performance traps, Pylint-derived maintainability rules,
and an eight-point complexity ceiling. Strict mypy checks production code.
Pytest and coverage.py measure behavior and branch coverage; the repository
currently requires at least 80 percent total coverage.

These automated checks are a floor, not a substitute for readable structure.
Review should also ask whether names reflect the research vocabulary, whether a
function has one reason to change, whether intermediate values make the
mechanism visible, and whether a non-programmer can trace one representative
state through the model.

## SonarQube

`sonar-project.properties` declares source, test, exclusion, Python-version,
and coverage-report paths. SonarQube does not generate Python coverage itself;
`just sonar` first creates the Cobertura-compatible `coverage.xml`, then calls
`sonar-scanner`.

The scanner and server credentials are intentionally not repository
dependencies. Install SonarScanner separately, then set `SONAR_HOST_URL` and
`SONAR_TOKEN` for the target server before running `just sonar`. The project key
can be overridden on the command line if the target server uses another key.
Continuous integration runs the same scan when repository secrets with those
two names are configured; otherwise the SonarQube step is skipped.
