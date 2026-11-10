# ASF Item 4: Registered Identifiability Stop

The [case report](../../cases/asf-autonomy-coordination-audit.md) records a
completed G2 stop pending owner review. G1 passes. G2 fails in both directions
at 60, 90 and 180 days: 0/34 A → C and 1/41 C → A opportunity families are
classifiable, below 75%. G3 is not reached; no recode, agreement, reconciliation
or downstream causal/nested comparison was performed. All claims remain C1.
CM-04's observational mapping is narrowed for this design under its registered
rule, with the prior formal-model consequence unchanged.

## Reproduce and Check

From the repository root, with the locked environment:

```sh
PYTHONPATH=. uv run --locked python \
  research/data/asf-item4-audit-2026-11-10/generate.py \
  --output /tmp/asf-item4-reproduced

diff -rq research/data/asf-item4-audit-2026-11-10/outputs /tmp/asf-item4-reproduced
uv run --locked pytest tests/test_asf_item4_report.py tests/test_research_artifacts.py
```

The output destination must not already exist. The adapter verifies the
accepted item 3 package, reconstructs every original native/source byte in a
disposable directory, restores the original lock and frame, and deterministically
reconstructs the original blank bundle. The frozen verifier checks the entire
restored lock against its retained digest and provenance. This is byte
reconstruction, not a new freeze, a recode or a fresh evidence interpretation.
No current source is retrieved and no original artifact is overwritten.

`generate.py` is an item-specific reporting adapter **outside** the frozen
implementation `18b13ff18500c33d8812459eda72ad6c11640f1a`. It uses the existing
integrity, G1 and G2 functions, preserves the shared-family all-project rule,
and refuses this stop-only report if any horizon requires G3. It never invokes
the downstream causal decision calculator. The locked first pass and operative
protocol/executable remain unchanged. The adapter hash is in the report;
`outputs/manifest.json` hashes every generated product.

`execution.json` retains the actual November 10 resumption clock, exact owner
confirmation, original local lock verification and absence of recode artifacts.
The owner's abstention statement is a provenance assertion, not independently
verified surveillance. The fourteen complete UTC days were October 24–November
6, with earliest permitted resumption November 7 at 00:00 UTC. Waiting checks
alone did not provide this confirmation. Reproduction does not generate a new
attestation or backdate any work.

## Products and Denominators

| Artifact | Scope and interpretation |
| --- | --- |
| `outputs/report.json` | Operative hashes, executable integrity, G1, independent horizon G2 results, explicit unreached G3 and bounded claim consequences |
| `outputs/source-access.csv` | All 180 original development/board month records |
| `outputs/screened-inventory.csv.gz` | All 1,110 native screening rows, including eligibility and original identifiers |
| `outputs/family-inventory.csv.gz` | All 1,028 native family/project rows, preserving dates, role, exposure and source IDs |
| `outputs/local-baseline.csv` | All 48 fixed project/quarter strata, eligible openings, original hash ordering and 36 selected release openings |
| `outputs/recorded-label-counts.csv` | First-pass direction/sign/authority-shift/disposition counts for each horizon, separating analysis from audit-only supplements |
| `outputs/family-observability.csv` | 75 direction/family denominator members × three horizons; all eligible project responses required for a classifiable family |
| `outputs/candidate-blockers.csv.gz` | All 2,946 original measurement rows, with scope, G2 denominator membership, observability failures, unknown fields, unmet conditions and available rival states |
| `outputs/field-missingness.csv` | Field values including unknowns, with explicit project-record denominators for all analysis rows and eligible opportunity rows |

The 368 analysis family/project pairs include the original 36-release baseline.
The 123 audit-only pairs enter integrity and descriptive exports, not G2 causal
denominators. Their union is the complete 491-pair measured frame. The 979-pair
eligible screening universe also includes unsampled releases and is not a
measurement shortfall. Every measurement row has one direction and one horizon;
distinct-family counts within descriptive cells cannot be summed across cells
as independent families. The 136 C → A project-level opportunity records at
each horizon represent 41 distinct families, not 136 independent opportunities.
Unknowns remain in G2 denominators. A row-level blocker outside G2 membership
is diagnostic only and cannot become an extra denominator member.

Recorded sign, shift, witness and rival labels are the preserved first pass,
not stability-validated or causal gate-passing results. Candidate blockers
expose values without selecting a causal account. Original per-field source
URLs/locators, dates, retrieval hashes, contrast records, shock/search ledgers,
rival explanations and the 14 native tables remain available through the
[unchanged item 3 package](../asf-item3-first-pass-2026-10-23/README.md).

## Validation — 2026-11-10

`just check` passes 214 tests with 90.59% production coverage, lint/format,
strict production typing and byte-for-byte reproduction of both model output
sets. The five new report tests protect gate ordering, an unreached G3,
sensitivity-horizon refusal, shared-family unknowns, complete export membership
and agreement with the frozen G2 family denominators. The complete report
regenerates byte for byte into a fresh directory. Changed local document links,
`git diff --check`, and the publication dry run pass. The frozen ASF scripts
and accepted item 3 package have no changes.

## Conclusions and Next Steps

The package warrants a reproducible registered identifiability stop and
reusable descriptive infrastructure. It narrows the empirical mapping in this
design and leaves all claim confidence at C1; it does not establish an absent
mechanism or validate the numerical model. The next action is owner review.
Item 5 is writing the synthesis and selecting a separately registered
observability discriminator. It has not begun.
