# ASF Autonomy and Coordination: Registered Codebook

## Status and Scope

This codebook belongs to the
[2026-09-04 preregistration and its dated amendments](asf-autonomy-coordination-preregistration.md).
It contains instructions and invented examples, not coded ASF evidence. The
[manifest](asf-autonomy-coordination-registration.toml) fixes the cohort,
windows, and gates. Do not change this codebook after inspecting case outcomes
without the protocol's dated-amendment procedure.

The core constructs are local decision discretion (A) and cross-boundary
commitment alignment/execution (C). Keep measurement, actor attribution, and
causal adjudication in separate fields. Never infer individual motives,
private communications, employer affiliation, or hidden authority from names.

## Source and Screening Records

Maintain one source row per original document/message, with:

| Field | Rule |
| --- | --- |
| `source_id`, `url`, `locator` | Stable original ID, canonical public URL, and section/message locator; mirrors link to the same original |
| `source_kind` | Approved minutes, project report, public development-list message, referenced public ticket, official policy, or primary shock record |
| `event_earliest`, `event_latest` | Inclusive event-date interval; do not substitute publication date |
| `published_at`, `retrieved_at`, `sha256` | Publication and retrieval provenance, plus hash of the exact retrieved source; unknown publication timing is explicit |
| `authority_at_event` | Citation supporting the author's organizational role and the applicable decision rule at that date, or unknown |
| `access_state` | Public complete, public redacted, incomplete archive, inaccessible, or private reference only |
| `eligible`, `exclusion_reason` | Inclusion under the protocol or one stated exclusion; never delete negative/unknown cases |
| `registration_commit` | Full SHA of the frozen packet, not the current mutable branch name |

Inspect complete public records rather than search snippets. Use short evidence
excerpts only when necessary; prefer locators and paraphrases. Keep source
hashes and retrieval information without publishing unnecessary personal data
or bulk copyrighted correspondence. Do not retrieve private archives, solicit
credentials, contact participants, or bypass access restrictions. A reference
to a private conversation records a missing channel, not its contents.

First build the complete monthly availability inventory. Distinguish a
verified empty public-list month from a failed listing or truncated retrieval.
An empty month is observable only when the archive index establishes that
there are no entries. A month's board minutes may contain no project report
because none was due; that is not automatically a missing report or failure.
An unavailable due-date schedule cannot be reverse-engineered from observed
submission frequency. Known omissions remain visible even if G1 passes.

Screen every subject-index entry in scope, but fully code only every
cross-boundary candidate, every thread needed to resolve ambiguous eligibility,
and the registered local-only release sample. For each nonempty
project-quarter, sort eligible local-only release openings by the hexadecimal
SHA-256 of `project|YYYY-QN|source_id` and select the first. Preserve all
screened IDs, the hash key, counts, and the selected ID so another run can
reproduce the sample without reading outcomes.

## Episode and Issue-Family Records

Assign `episode_id` from the earliest original source ID and project. Assign
`family_id` to the underlying release/proposal/service request: retries,
reopened votes, follow-up reports, and repeated mentions retain the family ID.
Split only if the requested action or intended deliverable is independently
different; record the rationale. One foundation-wide directive affecting
several PMCs is one shared initiating family, with project-specific responses,
not four independent cross-effect confirmations. Report its exposure across
projects but count the shared family once in each directional threshold.

Record project, action class (release decision, technical direction,
governance, infrastructure/service, policy/compliance), initiating role,
sender act, intended receiver, original option/commitment, requested change,
and every documented disposition. Classify the initiator as PMC, foundation,
external, or unknown. Authority comes from the act and role citation, not an
email address. Retain ordinary local-only episodes alongside cross-boundary
ones; they describe what happens without a documented directed request.

An A → C opportunity exists when an exercised local choice explicitly seeks
to create or change a foundation–project commitment. A C → A opportunity
exists when a documented foundation coordination action explicitly seeks to
change the project's available choices. Both can occur in one family through
different, ordered acts. Being an opportunity does not imply success, a
qualified witness, or even an observable receiver response.

## Measurement Fields

| Field | Allowed values and coding rule |
| --- | --- |
| `local_origin` | `pmc` / `foundation` / `external` / `unknown`; a contributor proposal counts as local only when pursued through the PMC's public decision process |
| `decision_right` | `pmc_binding` / `foundation_case_specific_authorization` / `shared_authorization` / `unknown`; cite the historically applicable rule and observed act |
| `decision_authority_shift` | `toward_pmc` / `toward_foundation` / `toward_shared` / `unchanged` / `unknown`; requires a documented before/after allocation of binding authority for the same decision class and names only the decision-authority layer |
| `authority_outcome_link_met` | `yes` / `no` / `unknown`; yes requires contemporaneous attribution or a discriminating within-episode or matched contrast linking the authority shift to the nested outcome rather than mere co-occurrence |
| `local_disposition` | `adopted` / `rejected` / `revised` / `withdrawn` / `pending` / `unknown`; a rejected proposal can still demonstrate exercised local discretion |
| `autonomy_change` | `expanded` / `restricted` / `unchanged` / `unknown`; compare an explicitly documented prior and subsequent option set, not message counts |
| `newly_feasible_action_executed` | `yes` / `no` / `not_applicable` / `unknown`; yes requires evidence that the authority or coordination change made a previously unavailable or blocked action feasible and that the action was then performed |
| `commitment_mode` | `voluntary` / `imposed` / `mixed` / `unknown`; record whose obligation and whose authority |
| `shared_commitment_named` | `yes` / `no` / `not_applicable` / `unknown`; yes requires a publicly identified cross-boundary commitment, its parties, and its intended deliverable or rule |
| `coordination_disposition` | `created` / `implemented` / `revised` / `refused` / `failed` / `ongoing` / `unknown`; mere receipt is not implementation |
| `coordination_burden_change` | `increased` / `decreased` / `unchanged` / `unknown`; requires an added or removed authorization/reporting step, or documented duplicated, revised, or abandoned work attributed to the coordination arrangement; raw latency alone is insufficient |
| `receiver_observed` | `known` / `unknown`; known requires a source for actual receiver conduct or an explicit unchanged disposition |
| `temporal_order` | `sender_first` / `receiver_first` / `documented_within_day_order` / `unknown` |
| `channel` | `public_cross_reference` / `documented_official_act` / `public_service_record` / `private_only_reference` / `unknown` |
| `effect_sign` | `enablement` / `constraint` / `both` / `no_demonstrated_effect` / `unknown`; direction is stored separately |
| `viability_event` | `official_status_change` / `explicit_obligation_failure` / `no_documented_event` / `unknown`; retain reason and duration |

“No documented event” means only that the reviewed corpus contains none; it
does not assert institutional viability. “Unchanged” requires affirmative
receiver evidence about the relevant option or commitment, not the absence
of a reply. Standing policy plus a valid local vote establishes documented
decision authority, but cannot by itself establish that no private pressure
affected the choice. Keep such hidden influence as an identification limit.

Use one principal disposition at each horizon, retaining its dated history.
For example, an implemented commitment later revised is coded revised at a
later horizon and implemented at an earlier one. Unknown stages are not
forward-filled. Withdrawal or refusal is an observed outcome, not missingness.

Do not infer decentralisation or centralisation from the PMC/foundation labels.
A `decision_authority_shift` requires an observed change in where binding
authority resides. It says nothing about infrastructure, ownership, attention,
wealth, or communication-network concentration. Code the two nested outcome
fields only from the same evidence bundle and horizon used for the associated
family; an attractive project result cannot retroactively create an authority
shift.

Code `toward_pmc` only for a transition from foundation or shared binding
authority to PMC binding authority; code `toward_foundation` only for a
transition from PMC or shared authority to foundation binding authority. Code
`toward_shared` only when a sole authority becomes shared, and `unchanged` only
when the before/after authority is documented and identical. All other or
incompletely observed transitions are unknown. A nested CM-12/CM-13 family must
begin inside the primary event-onset window.

## Horizon and Missingness Rules

Evaluate each receiver act at 90 days, then independently at 60 and 180 days.
For uncertain dates, compute minimum lag as receiver-earliest minus
sender-latest and maximum lag as receiver-latest minus sender-earliest. A
response is within the horizon only when its maximum lag fits and order is
known. If the lag interval straddles the boundary, its horizon status is
unknown. Events definitely beyond the horizon do not qualify for that horizon.
Record whether later evidence confirms the absence of an earlier disposition;
do not infer “no response by day 90” solely from a response observed on day 120.

Use distinct missingness codes: `not_applicable`, `not_public`, `archive_gap`,
`undated`, `publication_cutoff_unknown`, and `not_observed_in_reviewed_records`.
None maps to zero or to “no causal effect.” Unknown public status, a redacted
receiver act, or a missing shock assessment prevents qualification of the
affected mechanism witness. Exclude sources known to have first appeared after
the publication cutoff from primary adjudication; uncertain eligibility
cannot supply decisive evidence. Retain these exclusions in the audit.

## Shock Ledger and Rival Matrix

For each shock, record its family, public source, date interval, continuing
status, affected projects, and observable differences in exposure. Distinguish
an independently documented external precursor from a foundation response
caused by the project itself. A shared message mentions an event; it does not
automatically prove equal exposure. Lack of employment or resource data stays
unknown rather than being filled from presumed commercial affiliations.

For each opportunity, record whether each rival is supported, contradicted,
compatible but not discriminated, or unassessable. Attach the relevant source
IDs and explain what distinguishes or fails to distinguish it. The rivals are
reciprocal coupling, uncoupled own-history dynamics, common shock, A → C only,
and C → A only. Coding a mechanism witness requires the four protocol
conditions, not simply a majority of favorable matrix entries.

Keep a separate `qualified_witness` flag per direction and horizon with four
condition fields: `ordered_acts_met`, `receiver_conduct_met`,
`linked_change_met`, and `discriminating_contrast_met`. Each field is yes, no,
or unknown. A `qualified_witness` is yes only when all four are yes; otherwise
it is no, with the unresolved conditions retained. Count distinct issue
families, not messages or repeated votes.
Do not count one self-report and the board's reprint as independent accounts.
Multiple signs in one family do not increase its independent-family count.

## Solo Stability and Reproducibility Audit: G3

The researcher records measurements before making causal classifications. On
completion of the first pass, freeze and hash the full source, screening,
measurement, and classification files. Before calculating aggregate results or
a claim decision, use a local script to freeze an audit frame containing:

1. every family marked as an A → C or C → A opportunity in the first pass; and
2. a deterministic screening sample from every other eligible family.

For item 2, stratify by project and documented initiating role (`pmc`,
`foundation`, `external`, or `unknown`). Within each stratum, sort ascending by
the hexadecimal SHA-256 of `project|initiating_role|family_id` and take the first
20%, rounded upward, with at least one family from each nonempty stratum.
Recode all eligible families when fewer than eight exist overall. Freeze and
hash the full audit-frame ID list and generate the blank recoding bundle at the
same lock point.

Wait at least 14 complete calendar days after the first-pass lock without
opening the locked coding tables or doing other ASF evidence work. Record the
lock timestamp, recode start timestamp, and both hashes. The generated recoding
bundle contains the public source material and blank fields for the audit-frame
union in hash order.
It must omit the first-pass measurements, opportunity flags, causal and
qualification classifications, selection reasons, aggregate results, and claim
decision. Recode the bundle from the sources. This is blindness to earlier
codes and results, not to historical events; memory of a source may remain and
must be acknowledged as a limitation. Do not use an AI-generated imitation of
a second person and call it independent review.

Before reconciliation, require at least 90% exact agreement across `eligible`,
`decision_right`, `decision_authority_shift`, `autonomy_change`,
`newly_feasible_action_executed`, `coordination_disposition`,
`shared_commitment_named`, `coordination_burden_change`,
`authority_outcome_link_met`, `receiver_observed`, `temporal_order`, `channel`,
`effect_sign`, each of the four condition fields, and `qualified_witness`.
Compute the aggregate as exact matching values divided by all jointly required
field comparisons. Matching unknown values remain matches in that denominator.
For every field, separately report exact agreement, each pass's unknown rate,
and agreement restricted to records where neither pass used unknown; do not let
common uncertainty look like substantive stability. Missing recode fields are
disagreements.

Run a locally executable audit over every record, not only the recode sample.
It must validate schema and allowed values, source and retrieval hashes, event
interval order, horizon calculations, unique IDs, family de-duplication,
deterministic sample membership, non-missing evidence locators for positive
causal fields, gate arithmetic, and claim-decision arithmetic. Publish the
script, tests, environment lock, and machine-readable report with the evidence.
Software verifies declared rules; it does not supply a second interpretation.

After the recode is locked and scored, inspect every disagreement about a
qualified witness, authority shift, nested-claim outcome, or event-date
interval. Resolve it against the public evidence and preserve both original
values plus the documented adjudication. An unresolved witness or date dispute
removes that witness from qualification; an unresolved authority-shift or
nested-outcome dispute removes the family from CM-12/CM-13 counts.

Failure of the initial 90% threshold or of any executable integrity check fails
G3. Publish the descriptive ledger, stability diagnostics, and failed audit as
the completed registered result, but make no causal confidence increase. Do
not repeat recoding until it passes. An optional later human replication is
welcome as separately registered robustness work, never as a completion gate
or retroactive replacement for this solo analysis.

## Invented Calibration Examples

These examples define coding behavior; they are not observations about any
named project and cannot enter evidence counts.

| Invented episode | Required classification |
| --- | --- |
| A PMC conducts a valid release vote and rejects the release; nothing is said about the foundation | Exercised local decision authority and rejected disposition; C and hidden intervention unknown, not an uncoupled causal finding |
| A public foundation reply says “received” and the local proposal proceeds | Receipt alone is not a coordination implementation or a qualified cross-effect |
| An external outage precedes both a missed local action and a foundation service response | Candidate common shock; coupled effects unresolved until separately demonstrated |
| A foundation service refusal explicitly removes one proposed local option; the PMC publicly records choosing another because of that refusal | Candidate C → A constraint; qualify only after timing, contrast, authority, and rival checks |
| A local design requirement produces a documented change in a joint service plan, which then enables the local action | Candidate effects in both directions; one issue family, not two independent confirmations |
| A dated rule moves a release decision from case-specific foundation approval to PMC authority; the PMC then performs a formerly blocked release | `decision_authority_shift = toward_pmc`; candidate CM-12 generative family only if the directional and rival gates also pass |
| A PMC gains binding authority but the same record documents a new duplicated approval path that causes the shared commitment to fail | Candidate CM-12 disorganising family; code the burden and failure, but do not treat it as a second family if it is the same issue |
| A foundation takes binding authority and supplies a service that enables one project action while blocking a different local option in another issue family | Candidate CM-13 enablement and suppression in two families; each must qualify independently |
| A report refers to private board feedback with no public receiver act | Not-public channel/receiver; cannot infer sign, success, or absence of effect |
| A receiver first acts on day 120, with no record of what happened earlier | Potentially classifiable at 180 days; earlier horizons unknown unless earlier disposition is independently established |

## Conclusions and Next Steps

The codebook makes the candidate relation observable in principle without
equating autonomy with activity or coordination with centralisation. It also
separates changes in one decision-authority layer from claims about an entire
network and defines failures that can prevent a causal interpretation. It
supplies no case observations and changes no claim confidence.

After packet acceptance, first implement and freeze the blank schemas,
sampling functions, decision calculator, audit script, and synthetic tests.
Then inventory sources, verify dated authority, and apply the measurement rules
before assigning witnesses or selecting a preferred account. Freeze the first
pass, complete the delayed blinded recode and executable audit, and apply the
registered claim decisions. A later external replication is optional rather
than a dependency of this research programme.
