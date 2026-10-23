# ASF Item 3: Complete First Pass and Simultaneous Audit Lock

Item 3 is complete for owner review in [PR #19](https://github.com/cyborg-nomade/cybernetic-mutualism/pull/19).
This package preserves the completed first-pass input. It supplies no aggregate
gate, agreement or claim decision. Every claim remains C1. The registration
anchor is `00d696ed80bd388955f622e0611853165f19508c`; the executable remains
`18b13ff18500c33d8812459eda72ad6c11640f1a` with its accepted amendments and
implementation clarification.

## Contents and Review Scope

| Artifact | Meaning |
| --- | --- |
| `ledgers/*.csv.gz` | All 14 exact native CSV tables, compressed with zero gzip modification time; no schema changes |
| `source-catalog.json` | Exact SHA-256 and storage recipe for every registered local source path |
| `source-store/*.gz` | Additional exact original source/provenance bytes not reconstructable from the accepted repository snapshot; one object per byte hash |
| `accepted-inputs.json` | Hashes of accepted originals used by the reconstruction |
| `reviews/` | First-pass-only act decisions, component profiles, source provenance, role review, source versions, rival/search explanations and completeness scope |
| `audit-frame.json` | Actual deterministic audit family selection, generated at simultaneous lock |
| `lock.json`, `lock-receipt.json` | Original lock manifest and externally retained digest/timestamp receipt |
| `verification.json` | Package/reconstruction and frozen integrity checks; no aggregate calculation |
| `manifest.json` | Hashes of packaged files; Git supplies the external identity of this metadata package |

The 491 required family/project pairs comprise 368 analysis pairs, including
the fixed 36-release baseline, and 123 audit-only release pairs. Both directions
and 60/90/180-day horizons produce 2,946 records. The audit supplement is not an
expanded primary release sample or a new causal denominator.

All 18,199 primary subject-topic IDs were screened. Independent body judgments
cover 541 selected primary topics and 139 context topics, with additional
bounded source checks and complete selected release-opening/retry/closure
reviews. Board review covers 1,166 retained main/officer/cohort/Comdev/Attic
sections through December 2025 and 170 follow-up sections through June 2026.
This scope does not claim every unrelated email or other project's attachment
body was read. The earlier September/October progress packages retain their
historical incomplete statuses.

The six native attestations describe the exact human completeness assertions,
which software cannot independently certify. Unknown initial dates, source
publication, provider actions, actor capacity and actual exposure remain
explicit unknowns. Broad follow-up search does not certify an exact window for
an undated act. All documented opportunities remain in their appropriate
records; missing dates do not delete them. The five-rival matrix and frozen
comparison rule do not turn missing receiving behavior into no causal effect.

The native release transfer repair preserves its prior bytes and the original
647-family frame, 48 strata and 36 selected openings. It corrects 65 repeated
opening associations rather than drawing a new baseline. Full per-act and
component records explain other merges, splits, pre-window findings and
unknown eligibility. They distinguish an adopted rule, local vote, repository
edit and actually executed service action.

## Exact Reconstruction

Run from the repository root in the locked environment:

```sh
uv run --locked python research/data/asf-item3-first-pass-2026-10-23/verify.py
uv run --locked python research/data/asf-item3-first-pass-2026-10-23/verify.py \
  --materialize /tmp/asf-first-pass-restored
uv run --locked python -m scripts.asf_audit validate /tmp/asf-first-pass-restored
```

The destination must not exist. Reconstruction restores CSV bytes and every
registered source; their complete map must equal `lock.json`'s original
`first_pass_files`. It does not retrieve current replacements, rerun judgment
helpers, redraw the baseline, overwrite the lock, or perform a recode.
Accepted original mailbox blocks are re-extracted byte for byte. All other
sources come from exact packaged gzip objects. Source bytes retain their own
notices and attribution; these are research source copies.

`reviews/source-variants.json.gz` preserves all original Message-ID versions
and occurrence provenance. Each required alternate raw representation has a
registered version ID and enters the same source bag; it is not a new act or
corroboration. Historical publication uses a conservative bound over all
required variants, remaining unknown if any required bound is unknown.
Current provider JSON records use the separately disclosed latest-represented-
update convention, not a claim that today's serialization existed historically.
SVN revisions, source commits, public capture dates and underlying act dates
are distinct. Raw transport proofs permit separate verification of those
bounds. Uncertain publication cannot supply decisive coded support.

## Blind Bundle and Washout

The original local lock is retained at
`.local/asf-first-pass-2026-09-22/item3/locked-first-pass-2026-10-23/`.
Its `first-pass/`, `audit-frame.json` and `blank-recode/` were generated in one
frozen-tool transaction. The recode uses only the latter source-only bundle,
not this README, the native first-pass tables, `reviews/`, receipt mapping or
prior interpretations. Begin that coding in a fresh context containing only
the blank source bundle and the operative frozen protocol, so this chat’s
first-pass interpretations are not supplied to the delayed coder. Every coding cell starts blank apart from the frozen
neutral identity/direction/horizon whitelist. Source locators identify whole
original bytes; no qualification, authority or eligibility judgments are
smuggled into locator text. Specific first-pass evidence locators remain in the
locked first pass only.

The lock timestamp is `2026-10-23T07:14:24.068077+00:00`. The earliest recode start
is **November 7, 2026 at 00:00 UTC (01:00 Berlin)**, provided no ASF evidence
work intervenes. Exact hashes and dates are in `lock-receipt.json`.
Fourteen complete UTC days without ASF evidence work must follow the lock.
No recode, aggregate gate or claim calculation has begun. Review corrections
that reopen evidence require a new valid lock/washout boundary; retaining a
prior timestamp does not satisfy the no-evidence-work requirement.

The 23-row initial shock/context ledger preceded directional coding. Two
independently documented follow-up precursors were added before the final
individual rival/witness adjudication. Mutable earlier `qualified_witness = no`
placeholders were explicitly incomplete. This sequence is disclosed in the
native attestation; it is not represented as complete outcome blindness.
No initial delayed recode may be retried until agreement passes.

## Conclusions and Next Steps

This package warrants a complete, hash-verifiable first-pass input for owner
review. The public-record limits still constrain identifiability and causal
interpretation; complete coding does not imply a successful gate. The wider
programme and all claim confidence remain unchanged at C1.

After review and the valid washout, item 4 is research and writing using the
frozen code: delayed blinded recoding, initial agreement, reconciliation and
the registered gate/claim report. Any registered gate failure stops later
causal comparison. Item 5 is writing the cycle synthesis for the path actually
reached and selecting the next discriminator.
