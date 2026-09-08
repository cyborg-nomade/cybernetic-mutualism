# Print/Reformation First-Pass Codebook

## Freeze and Scope

Frozen on 2026-09-08 before new source retrieval for this pass. The parent
[paired design](print-reformation-paired-design.md) and its named sources have
already been read. Saxony's public reform and Venice's divergent outcome are
known selection criteria, not discoveries or held-out predictions. This is a
prospective coding freeze for a retrospective, purposively selected comparison.
Commit this document before collecting observations; subsequent amendments must
identify their date, reason, and exposure to evidence. Preserve the freeze commit
in the review and merge history.

The first-pass jurisdiction list is closed:

| ID | Jurisdiction and role | Boundary rule |
| --- | --- | --- |
| ES | Electoral Saxony; principal positive trace | Ernestine electoral territory until 1547; record the transfer of Wittenberg and electoral authority separately thereafter. |
| DS | Ducal Saxony; within-Empire comparison | Albertine territory under George until 1539 and Henry thereafter; never pool its adoption date with ES. |
| VE | Republic of Venice; principal difficult trace | Record city, mainland, or dominion-wide scope for each observation; a city record does not establish mainland coverage. |

These are three historical jurisdiction trajectories, not three independent
random observations. Rome and imperial institutions may enter as external actors
but do not expand the sample. No pan-European adoption rate will be estimated.

## Periods and Outcomes

Phases are 1470–1516 (baseline), 1517–1525 (initial controversy), 1526–1546
(institution building), and 1547–1565 (consolidation). German explanatory records
stop at 1555; Italian explanatory records stop at 1565. German records after
1555, and Italian records after 1565, may establish durability only. Event dates
remain intervals within phases; the ten-year rule is inherited from the design.

Code public reorganization as `authorized`, `implemented`, `durable`,
`documented_absent`, or `unknown`. These are evidence states, not a numeric scale.
An authorization alone does not establish implementation or persistence.
`durable` requires an effective public change and sourced continuity for ten
years or to a case-ending settlement. Specify which route establishes it.
`documented_absent` requires an explicit historical account of non-adoption over
a named interval; failure to find an ordinance is `unknown`.

Record worship, clergy, property/finance, and enforcement separately in prose
even when a single event concerns several. Secondary outcomes are discursive
diffusion, organized dissent, and institutional counter-adaptation. Possession,
publication, reception, and population belief are never interchangeable.

## Evidence Record

Each ledger record must have a stable ID; earliest/latest date (year, month, or
day, with its precision stated); place and jurisdiction; actor; event type;
observation; outcome component; source ID and exact available locator; standpoint
and proximity; confidence; predecessor/successor IDs or `unknown`; and limitation.
Source records give URL, title, author or institution, access date, access extent,
provenance, and reuse conditions. A search snippet is a lead, not event evidence.

Event types are `print`, `circulation`, `reception`, `protection`, `ordinance`,
`implementation`, `censorship`, `dissent`, `settlement`, and `boundary_change`.
Confidence is `high` for a directly inspected contemporary document's explicit
act, `medium` for an explicit reconstruction in inspected scholarly or curated
historical text, and `low` for contested attribution or indirect inference.
Confidence applies to the stated observation, not its proposed causal effect.
Modern editorial introductions remain secondary evidence even beside primary
texts. Prescriptions establish intended rules, not compliance.

Use `unknown` for unobserved fields, never zero. Retain conflicting dates as an
interval or separate attributed assertions; do not average them. A later edition
does not establish an earlier reception date. Historical calendar labels stay
as reported; no unsupported day-level synchronization is allowed.

## Collection, Catalog Audit, and Stop Rules

One researcher must be able to finish using public texts and local tools. Search
the parent design's sources first, then public scholarly or institutional sources
for missing links. Stop this pass when both principal traces, a DS comparison,
an ordinance/censorship ledger, and a catalog feasibility decision are recorded,
including unresolved fields. If a central record is inaccessible, try one public
alternative and record the residual gap. No paid access or external reviewer is
required. This is a bounded evidence pass, not an exhaustive archival census.

Audit VD16, EDIT16, and USTC for scope, stable identifiers, usable metadata,
export/access conditions, deduplication, and historically meaningful edges.
Where accessible, inspect at most one candidate edition per phase and region,
selected in this order: a dated institutional or censorship artifact; an ordinary
devotional or Catholic work; a reforming controversial work. Resolve ties by
earliest year then catalog identifier. Record empty or inaccessible strata;
do not substitute famous Protestant artifacts and call the sample complete.
The target is eight strata, not a representative estimate of book production.
Record query terms and selection limitations; no claim of an exhaustive earliest
result is permitted without an enumerated result set.

A reproducible network study requires a retrievable bounded record universe,
documented reuse/export route, stable edition IDs, deduplication, manually checked
edge semantics, and sensitivity to missing or uncertain records in both regions.
Shared place or title words alone do not establish transmission. If these gates
are not met in this pass, choose bounded process tracing and identify exactly
what would reopen the network path. Website access failure is not proof that
the underlying data do not exist.

## Comparison and Claim Decisions

Reconstruct topology, production, artifacts, worldview, and political organization
from the same ledger for each principal case. For onset of diffusion, ordinance
timing, dissent survival, control, and divergent outcomes, compare the full account
against topology-plus-demand, state-plus-grievance, and independent shocks.
Classify each comparison `favours`, `compatible`, `contradicts`, or `unresolved`,
with event IDs and an explicit missing observation. Chronology alone does not
identify necessity, sufficiency, or a causal effect. Do not count correlated
retellings as independent replications.

CM-07 can reach bounded C2 only with sourced relational changes in both regions
and at least one within-region contrast that discriminates a named rival; output
counts alone fail. CM-08 can reach bounded C2 only if a sourced communication
change precedes a consequential institutional change and resolves timing that
state/production alternatives miss. Otherwise retain C1 and state which account
the trace strengthens. CM-09 can reach bounded C2 only if a specific reduced
account misclassifies a sourced observation that the five-domain account explains
with a distinct, evidenced link. More narrative detail does not pass this test.
Failure to meet a gate is not evidence of absence; separately report contradictions
and research-direction decisions. No confidence level above C2 is available from
this selected first pass.

## Amendment 1 — Military Context

2026-09-08, after source inspection: add `military_context` to the event types
to record the battle of Mühlberg without misclassifying it as a settlement.
This is an exposed descriptive amendment, not a new confirmatory test, new
jurisdiction, or change to the confidence gates. The original rules remain
available at `fdea00e`.

## Conclusions and Next Steps

This freeze makes the evidence pass executable without external assistance and
fixes the comparison before new retrieval. It warrants no historical finding or
confidence change. Next, collect the dated ledger and source audit, reconstruct
the three trajectories, and decide between a feasible network study and bounded
process tracing using the gates above.
