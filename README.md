# cybernetic mutualism

Cybernetic mutualism is a research program for rebuilding mutualism as a
materialist, cybernetic theory of history and society.

The project begins from a Proudhonian claim: social antinomies are not errors
waiting for a final synthesis. Centralisation and decentralisation, liberty and
authority, cooperation and conflict continually produce, constrain, and
transform one another. It adds a second claim: the topology of communication
networks is a primary material constraint on productive organisation, culture,
worldviews, and political institutions.

The initial statement of the project is the
[provisional manifesto](MANIFESTO.md).

## repository structure

- `MANIFESTO.md` — the current canonical statement of the theory.
- `ROADMAP.md` — the research program, case portfolio, simulation agenda, and
  publication sequence.
- `research/glossary.md` — provisional inherited, technical, and
  project-specific definitions for the research program.
- `research/claims.md` — falsification and revision ledger for the manifesto's
  historical, conceptual, causal, empirical, model, and normative claims.
- `research/cases/` — comparative designs and dated case evidence.
- `models/` — reproducible formal models, generated outputs, and model notes.
- `posts/` — essays and shorter texts intended for publication.
- `scripts/publish_wordpress.py` — Markdown-to-WordPress publisher.
- `docs/PUBLISHING.md` — local and GitHub Actions publishing runbook.
- `docs/SOCIAL.md` — Facebook automation and manual X distribution runbook.
- `docs/STYLE.md` — prose conventions for blog-bound writing.
- `docs/DEVELOPMENT.md` — reproducible Python environment and quality workflow.
- `docs/WORKFLOW.md` — one-chat, one-branch, one-PR working convention.
- `tests/` — checks for models and publishing tools.

## editorial principles

- Distinguish the author's claims from exploratory scaffolding and inherited
  concepts.
- Treat quotations, citations, historical data, and mathematical claims as
  unverified until checked against primary or authoritative sources.
- State what would falsify a model, not only what appears to confirm it.
- Preserve unresolved antinomies instead of forcing premature synthesis.
- Keep prose readable independently of its formal models.

## development

```bash
just sync
just check
```

See the [development guide](docs/DEVELOPMENT.md) for model, test, lint, type,
coverage, and SonarQube commands.

## publish a local dry run

```bash
uv run --locked python scripts/publish_wordpress.py MANIFESTO.md --dry-run
```

Publishing is deliberately manual and draft-first. See
[the publishing runbook](docs/PUBLISHING.md) before configuring WordPress
credentials or running a live publication.

## status

This is groundwork: the theory, vocabulary, formal models, evidence, and
bibliography are all provisional and expected to change.
