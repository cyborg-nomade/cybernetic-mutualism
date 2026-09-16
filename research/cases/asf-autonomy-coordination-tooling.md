# ASF Audit Tooling: Pre-Evidence Implementation Record

- **Date:** 2026-09-16.
- **Status:** Third-cycle item 1; implementation submitted for review, not yet
  an accepted executable freeze or an empirical run.
- **Original registration:** `00d696ed80bd388955f622e0611853165f19508c`.
- **Accepted amendments:** `pr13-review-clarifications-2026-09-04` and
  `solo-completion-and-research-yield-2026-09-05`.
- **Exposure:** No additional ASF source, case record, or outcome has been
  retrieved or coded. The existing [exposure audit](asf-autonomy-coordination-source-audit.md)
  remains the complete exposure disclosure. Tests use invented local bytes.

## Implementation and Warrant

The [offline Python package](../../scripts/asf_audit/__init__.py) implements
blank CSV schemas, deterministic local-release selection, exposure-based
comparison selection, uncertain-date horizons, G1–G3 arithmetic, primary and
nested decisions, first-pass/source hashes, audit-frame selection, blank
recoding bundles, initial agreement diagnostics, and preserved reconciliation.
The [operating guide](../../docs/ASF_AUDIT.md) connects the commands to the
researcher's work. The existing locked Python environment is sufficient; no
new runtime package, account, paid service, collaborator, or network request is
required by the tooling.

The accepted [protocol](asf-autonomy-coordination-preregistration.md),
[codebook](asf-autonomy-coordination-codebook.md), and
[manifest](asf-autonomy-coordination-registration.toml) remain unchanged.
Software checks declared values, dates, provenance, membership, and arithmetic.
It cannot verify that a source actually supports an interpretation, an archive
inventory is complete, or the researcher abstained from evidence work during
washout. Those assertions remain explicit, source-linked human responsibilities.

## Proposed Pre-Evidence Clarification: Audit Supplement

**Identifier:** `tooling-audit-supplement-2026-09-16`.
**Status:** Proposed for owner acceptance with this item. This is not silently
added to the list of accepted amendments in the original TOML.
**Reason:** The codebook requires a recode sample from every eligible
non-opportunity family, while primary routine-release coding is restricted to
one opening per nonempty project-quarter. Some eligible families selected for
recoding therefore have no primary first-pass measurements to compare.
**Prior exposure:** None beyond the unchanged source audit.
**Affected analysis:** G3 first-pass coverage and work required by the audit;
primary baseline membership, gate thresholds, and claim rules are unchanged.

The implementation includes the entire eligible screening universe in audit
selection. Before locking, complete first-pass measurements for audit-selected
families outside the primary baseline as an **audit-only supplement**. These
records supply genuine initial values for the registered agreement calculation.
They do not enter the primary baseline, direction counts, nested counts, or
descriptive analysis sample. The primary routine-release baseline remains at
most 48 families; the supplement adds disclosed audit work whose size depends
on the screened universe. No feasibility estimate is asserted before screening.

If examination of a supplement reveals an actual cross-boundary opportunity,
correct the screening classification and include it in the required census
before lock. Regenerate the deterministic frame until it represents the
completed first pass; never select on the later aggregate result. After lock,
frame membership is fixed and cannot be resampled during reconciliation.

This resolves a real implementation gap and must be accepted before retrieval.
It preserves all available first-pass values and avoids either shrinking the
registered audit universe or inventing unknown codes for unread records. No
empirical result exists under the unclarified or proposed convention. The
original packet remains identifiable in Git; if this clarification is changed
in review, revise implementation and tests before the executable freeze.

## Other Explicit Operational Conventions

| Rule | Executable convention and consequence |
| --- | --- |
| Measurement unit | One principal family × project × direction × horizon row, with underlying episode/act identities and disposition history retained. Both direction rows exist for every coded family at each horizon, including non-opportunities. Agreement counts all 18 registered fields per required row; no post hoc weighting or field dropping. |
| Shared initiating family | Count once in each directional family denominator and witness count, retaining project-specific responses. A shared opportunity is classifiable only if all its recorded eligible project responses in that direction/horizon are classifiable. Unknown responses cannot disappear behind a known response elsewhere. This conservative aggregation convention is disclosed before data. |
| Required signs | Enablement and constraint must occur in separate families. Two distinct `both` families can qualify; one cannot. Nested tests likewise require distinct signed families across the registered PMC count. |
| Dates | Normalize offset timestamps to UTC dates for calendar-day lags; retain uncertain inclusive intervals. Exact same-day order requires an explicit documented sequence. Unknown or boundary-straddling lags do not establish response within a horizon. |
| Complete-day washout | Count 14 complete UTC calendar days after lock; a partial lock day is excluded. A lock at 12:00 UTC on 16 September permits recoding at 00:00 UTC on 1 October. Record lock and actual recode start separately. |
| Blinding | Audit-family union ordered by SHA-256 of UTF-8 family ID, with ties by ID; row order within family uses a hash of neutral record ID. Include only public source bytes and neutral IDs plus the fixed direction/horizon grid. These axes appear for every family and disclose no earlier opportunity or causal decision. Measurements, selection reasons, annotations, and results remain blank or absent. |
| Contrasts | Prefer the earliest other eligible family with known different exposure in the same PMC/class/year. If absent, consider both adjacent years inside the primary window, choosing the earliest and breaking ties by original source ID. No outcome-based replacement. |
| Source support | Positive fields need a source and locator with known publication eligibility and the relevant material available. A partially redacted document may support visible facts only when the cited decisive material is explicitly recorded complete. Current archive indices can establish access, but unknown publication timing cannot decide historical eligibility or a witness. |
| Act independence | Stable sender/receiver act IDs must differ. Two acts can be documented in one original source; copying or reprinting an act does not create another act. Source and family de-duplication still require interpretation. |
| Missing recodes | Missing cells or records are disagreements; matching `unknown` values are matches. Report unknown rates and agreement excluding unknown values separately. No initial-score replacement or repeated recoding to pass. |
| Reconciliation | Preserve both passes. Unresolved witness/date disputes remove qualification; unresolved authority/nested-outcome disputes remove nested support. Integrity and initial agreement failures remain G3 failures even if later reconciliation improves the values. |

These conventions make otherwise unspecified file-level behavior reviewable;
they do not change the cohort, observation windows, numerical thresholds, or
claim-confidence routes. Together with the audit supplement, they form the
proposed execution specification. Acceptance is the freeze boundary; future
bug fixes or rule changes require dated disclosure and retention of the
previous results under the protocol's amendment procedure.

## Verification and Review Boundary

Synthetic tests exercise successful and failed gate paths, both timing
sensitivities, family/sign de-duplication, incomplete observations, source
provenance, uncertain dates, washout boundaries, tamper detection, absent
recodes, and unresolved adjudications. Fixtures deliberately use
`example.invalid` URLs and invented text; they are never case observations.
The repository's lint, strict typing, test/coverage, and model-reproduction
gates apply to this package. An accepted commit and its CI results will identify
the reviewed executable version; the work branch itself is not an immutable
freeze.

Local verification on 2026-09-16 passes all 179 tests, including 59 new synthetic
checks, with 90.37% combined branch/statement coverage. Ruff lint and formatting,
strict mypy, local documentation links, and byte-for-byte reproduction of both
committed model artifact sets also pass. These are software checks, not ASF
findings.

## Conclusions and Next Steps

The tooling makes a prospective execution of the ASF registration locally
reviewable and testable. It warrants no empirical conclusion, independence
claim, or increase above C1, and leaves CM-04's structural narrowing intact.
Review the implementation and disclosed audit supplement, accept an executable
freeze, then separately authorize the access/cohort audit. No case collection,
historical follow-up, or publication is part of this item.
