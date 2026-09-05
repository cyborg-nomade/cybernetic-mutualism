# ASF Autonomy and Coordination: Empirical Preregistration

## Registration and Present Warrant

- **Registered:** 2026-09-04, before systematic case-record retrieval or coding.
- **Cycle:** Second cycle, item 4; acceptance is subject to PR review.
- **Institution:** Apache Software Foundation (ASF).
- **Design:** Retrospective, public-records, structured process comparison.
- **Packet:** This protocol, the [codebook](asf-autonomy-coordination-codebook.md),
  [source audit](asf-autonomy-coordination-source-audit.md), and
  [registration manifest](asf-autonomy-coordination-registration.toml).

This registers a test, not a finding. It provides no empirical support for
CM-01, CM-04, CM-12, or CM-13 and changes no confidence level. The records
already exist; this is prospective specification of an analysis of historical
records, not preregistration before the historical events occurred. The source audit
discloses the governance material and incidental search-result information
seen during design. No claim of complete outcome blindness is made.

The first commit containing the complete packet is its immutable registration
anchor. Its SHA must be recorded in the PR and every subsequent evidence
manifest. Retain that commit in history when merging. This is a public Git
preregistration, not an OSF registration or an independently approved study.
Any post-registration change requires a dated addendum stating its reason,
prior data exposure, and affected analyses; retain results under the original
rules. Evidence collection requires acceptance of this packet and is not part
of this PR.

## Question and Choice of Case

Do locally exercised decision rights and foundation-level coordination
recurrently enable and constrain one another, or do public records better
support one-way oversight, independent routines, or responses to common shocks?

Three nested questions reuse the same observations without changing the primary
case-selection rule:

1. Does a documented shift of binding decision authority toward PMCs show both
   generative and coordination-burdening effects in this decision layer?
2. Does a documented shift toward foundation authority show both enabling and
   suppressive effects in this decision layer?
3. Does the A/C vocabulary yield a classifiable, rival-discriminating account,
   or does it merely redescribe ordinary governance events?

The ASF separates project technical direction from foundation oversight in its
[governance account](https://www.apache.org/foundation/governance/pmcs).
This makes the relationship a candidate for study, not an antinomy by
definition. ASF projects are corporate committees, not sovereign member
cooperatives; “federated” is an analytical description of distributed authority,
not a legal classification or evidence of mutualist commitments.

Fix four nested project–foundation relationships: Apache HTTP Server (`httpd`),
Apache Tomcat (`tomcat`), Apache Maven (`maven`), and Apache Ant (`ant`). These
are a purposive, familiar software-project cohort spanning server and build
tool work, not a random or representative sample. Neither a known conflict nor
an observed regime determined inclusion. Verify their top-level PMC status at
the window's opening from dated official records during the evidence pass.
An ineligible project fails the registered cohort gate; do not silently replace
it with a more informative project. Keep retirement or reorganization during
the window as an outcome, not a reason to select only survivors.

All four share the same foundation and may share contributors, employers, or
technical dependencies. They are dependent comparisons, not four independent
institutional replications. No population effect, significance test, or causal
coefficient will be estimated from them.

## Units, Windows, and Timing

| Element | Fixed rule |
| --- | --- |
| Primary unit | A dated decision or coordination episode in one named PMC–foundation relationship |
| Primary event-onset window | 2023-01-01 through 2025-12-31, inclusive |
| Baseline context | 2022-10-01 through 2022-12-31; earlier documents only to establish governing authority, not additional outcome episodes |
| Follow-up | Through 2026-06-30, solely to close in-window episodes and check longer response lags |
| Primary response horizon | 90 calendar days after the documented initiating event |
| Timing sensitivity | Reassess at 60 and 180 days, retaining the primary decision |
| Source publication cutoff | 2026-08-31; later interpretations are excluded from the registered analysis |
| Descriptive blocks | Four projects × twelve calendar quarters = 48 project-quarter blocks |

Record event time, publication time, and retrieval time separately. Use UTC
when a timestamp supplies an offset; retain date intervals when the exact day
is unknown. Strict ordering requires the sender's latest possible date to
precede the receiver's earliest possible date. Same-day events without a
documented within-day sequence and overlapping intervals have unknown order.
Publication of approved minutes is not the time of the underlying decision.

Reports are periodic observations, not synchronized institutional updates.
The [reporting process](https://www.apache.org/foundation/board/reporting)
describes quarterly project reporting and later publication in approved minutes.
Reconstruct actual event order from dated acts; do not impose a quarterly lag,
interpolate unobserved states, or code administrative reporting rhythms as
oscillation. Response-horizon uncertainty is coded explicitly in the codebook.

## Observable Proxies

Retain separate components; do not manufacture a single [0, 1] capacity index.

| Construct | Observations | What they do not establish |
| --- | --- | --- |
| Local autonomy, A | Proposal origin, documented binding decision rights, available options, adoption/rejection/revision/withdrawal, and case-specific foundation authorization or veto | These measure exercised discretion, not latent freedom. Release frequency, silence, and commit volume are not autonomy. |
| Collective coordination, C | A cross-boundary commitment with named PMC and authorized foundation roles, a deliverable or rule, an agreed or imposed obligation, and an observed disposition | Alignment and execution are not simply central authority, report submission, or foundation message counts. |

For each episode, code A's option set as expanded, restricted, unchanged, or
unknown relative to an explicitly documented prior state. Code C's commitment
as created, implemented, revised, refused, failed, ongoing, or unknown. Separate
voluntary agreement from imposed obligation. An imposed obligation can
coordinate conduct while reducing discretion; it is not normatively endorsed.
Both high autonomy and effective coordination may coexist; the measures are
not complements and their denominators are not shared.

Ordinary locally decided release votes provide observations of exercised
decision rights even when no foundation intervention is visible. That absence
is not itself evidence that there was no private intervention. A declaration
of “no board issues” describes the report's claim, not a zero cross-effect.
Current governance documents guide source discovery; historical authority
must be supported by a version effective at the event date or remain unknown.

Quarterly summaries retain counts of eligible episodes, known and unknown
rights, option changes, and commitment dispositions separately. They are
descriptive tables, not a time series suitable for fitting the toy equations.
The episode ledger, not an attractive aggregate pattern, adjudicates rivals.

## Corpus and Outcome-Independent Inclusion

After acceptance, inventory all approved public board minutes for the primary
window, including special meetings listed in the calendar, and the fixed
projects' public development-list archives. Extract all four projects' reports
and all foundation actions naming those projects. Read foundation-wide officer
reports for possible shocks, including periods without a selected-project
dispute. The [board process](https://www.apache.org/foundation/board/meeting)
identifies project and foundation officer reports; it does not guarantee that
every relevant exchange will be public.

Screen the complete public subject index for formal release-vote openings and
proposals requesting a binding change in technical direction, project
governance, or foundation services. Extract every cross-boundary candidate and
every ambiguous thread needed to decide eligibility. Include unsuccessful,
withdrawn, unanswered, and apparently routine proposals. For the local-only
release baseline, do not code a census: within each nonempty project-quarter,
sort eligible release-vote openings by the hexadecimal SHA-256 of
`project|YYYY-QN|source_id` and code the first one. Preserve the screened count
and sampled ID for every stratum. This caps routine baseline coding at 48
families without outcome-based selection.

Exclude ordinary patches, user support, automated notifications, release
announcements without a decision record, and personnel speculation. Treat a
referenced public issue tracker or official service ticket as corroboration,
not as an unrestricted additional sampling frame. Follow references until the
same episode closes or reaches the horizon; do not follow unrelated disputes
into new projects or years.

Search aids include `vote`, `result`, `proposal`, `board`, `PMC`, `policy`,
`infra`, `legal`, `brand`, `retire`, and their inflections. Keywords assist
screening; they do not replace inspection of the full subject index and any
ambiguous thread. Retain an inclusion/exclusion ledger with stable message or
document IDs, dates, and reasons. De-duplicate quoted messages and mirrors.
Repeated votes on the same release or revisions of the same request remain
one issue family, not independent confirmations. There is no discretionary
sample cap or stopping after a compelling example.

Foundation actors include the Board and formally authorized officers or
services, but an individual's ASF affiliation alone does not make an action
foundation coordination. Preserve role and authority citations. Requests made
by a PMC chair in a personal capacity are not automatically PMC decisions.

## Rival Models and Discriminating Observations

These are competing event-level causal accounts, not calibrated numerical
models. They constrain which transitions each account must explain.

| Account | Registered expectation | Observation that challenges it |
| --- | --- | --- |
| Reciprocal coupling | A changes the available or executed forms of C, and C changes A's options, through enabling and constraining pathways | Missing directions or signs despite adequate observation; mere replies, compliance, or contemporaneous activity |
| Uncoupled dynamics | Each pole's changes follow its own history without a cross-effect | A cross-boundary change alters a receiver's feasible action with a contrast not explained by its own history |
| Common shock | A third process precedes both changes and explains their timing/exposure without a cross-effect | Divergent responses under comparable documented exposure or a mechanism-specific within-episode revision remain unexplained |
| A → C only | Local decisions alter coordination, but coordination does not alter local options | A qualified C → A witness |
| C → A only | Foundation oversight or support alters local options, but local decisions do not change coordination | A qualified A → C witness |

A directional mechanism witness requires all of the following:

1. Separate sender and receiver acts, with reliable temporal order within the
   primary horizon; one document copied twice is not two acts.
2. An identified channel and documented receiving action. Sender self-report
   alone, a formal acknowledgement, or a scheduled report is insufficient.
3. A concrete change in the receiver's options or commitments, linked by
   contemporaneous documents to the sender's action. An actor's explanation is
   evidence of an attribution, not automatically a demonstrated cause.
4. A discriminating contrast: a documented before/after revision, a failed or
   refused request, or the prespecified comparison episode, with own-history
   and shock alternatives explicitly assessed. Cross-contact alone does not
   discriminate coupling from an ordinary administrative routine.

Record **enablement** when the sender makes a previously unavailable action
feasible or enables execution of a specifically blocked commitment. Record
**constraint** when it removes an option, prevents execution, or forces a
revision of an intended commitment. A → C must change coordination beyond
merely triggering its prescribed acknowledgement; C → A must change local
discretion beyond the standing existence of corporate rules. Record both
signs separately when both are evidenced, without double-counting the family.

For each potential witness, select the earliest other eligible family in the
same PMC, same action class, and same calendar year with a different observed
cross-boundary exposure. Break ties by stable source ID. Selection uses
exposure, not receiver outcome. If none exists, widen only to the adjacent
calendar year within the primary window; otherwise record no matched episode.
No replacement is allowed after seeing an inconvenient contrast. Unknown
exposure cannot serve as an untreated comparison. A documented within-episode
contrast can satisfy criterion 4 when no separate comparator exists.

## Common Shocks and Other Confounding

Create a separate shock ledger before assigning causal witness labels.
Prespecified families are infrastructure/service disruption, public security
events, externally imposed policy or legal changes, sponsor/employer changes,
contributor availability, and shared dependency or demand changes. Record the
source, onset interval, affected projects, observable exposure differences,
and missing information. Candidate shocks must be identified from primary
public sources, not inferred from the very A/C outcomes they are meant to
explain. Search both selected-project and foundation-wide records over the
30 days preceding each initiating event and through its response horizon.
Carry forward a previously documented continuing shock only with an explicit
continuation record. Disclose potentially older, unobserved causes as a limit.

A foundation action caused by project feedback is a candidate mediator, not
automatically an exogenous shock. Separate an external precursor from the
institutional response. Different projects can have different exposure to
the same event; a common calendar date is not a control for that exposure.

For each candidate witness complete a rival matrix: supporting observation,
contrary observation, missing evidence, and whether the alternatives remain
observationally indistinguishable. Missing shock information produces an
unresolved comparison, not a clean coupled effect. A shock and coupling may
both contribute; label a mixed account instead of crediting everything to
either one. No number of correlated reports can exclude an unmeasured cause.

## Access, Identifiability, and Decision Gates

Apply gates in order. The thresholds are declared audit rules, not statistical
power calculations or significance levels.

**G1 — Access and cohort.** All four projects must be eligible at the start.
For each project, at least 33 of the 36 primary months must have a reviewable
public development-list index and retrievable included threads; at least 33
months must have the approved public board minutes or an official statement
that no meeting occurred. Inventory announced special meetings separately and
require their records too. Any missing section needed to adjudicate an episode
still makes that episode incomplete, even when overall coverage passes.
Do not invent a project's report due date from a private reporting schedule.

**G2 — Identifiability.** There must be at least four distinct opportunity
families in each direction, spanning at least two PMCs per direction. An
opportunity is a documented sender action that proposes or imposes a change
on a specified receiving option/commitment, regardless of whether it works.
At least three quarters of opportunities in each direction must have both
receiver disposition and time order classifiable from public records. Unknown
cases remain in the denominator. These conditions test observability, not
the required number of successful coupling witnesses.

**G3 — Solo stability and reproducibility audit.** Complete the codebook's
frozen, delayed blinded recoding and executable integrity checks before
adjudicating the hypotheses. The initial recode agreement must reach 90% under
the registered calculation. This is an intra-rater stability gate, not evidence
of inter-rater reliability. It requires no collaborator, payment, institution,
private access, or external service. Failure yields a completed but unstable
descriptive study; it does not authorize recruiting a gatekeeper or repeatedly
recoding until the threshold passes.

| Outcome after gates | Registered decision |
| --- | --- |
| Any gate fails | Public-record design is underidentified/infeasible at the stated level; publish missingness and stop the registered causal comparison. No replacement cohort or confidence change. |
| Both directions have at least two qualified witness families, including an enabling and a constraining witness in separate families in each direction, with at least two PMCs represented per direction; no decisive rival remains unaddressed | Provisionally retain this **bounded reciprocal-mechanism interpretation**, not the necessity or universal validity of antinomy. |
| Both directions have at least one qualified witness but fail the full signed-family criterion above | Reciprocal interaction only; the registered antinomy criterion is not met. |
| Only one direction has any qualified witnesses | Narrow this candidate to an observed one-way account; do not infer that the reverse direction is universally absent. |
| Neither direction has qualified witnesses, with informative unchanged outcomes or rival-supported changes | Do not retain this candidate as a demonstrated antinomy; identify whether uncoupled, common-shock, or mixed accounts suffice. |
| Neither direction has qualified witnesses and rival explanations remain unresolved | Indeterminate; do not relabel uncertainty as either confirmation or refutation. |

Apply the table from top to bottom. If receiver changes reverse the claimed
temporal order, they cannot qualify as witnesses of that direction. Repeated
acknowledgements do not satisfy the count threshold. A mixed shock/coupling
account can support a witness only if the cross-effect itself meets all four
requirements and the remaining shock contribution is separately reported.
For the rival-resolution gate, each family-level rival entry asks whether
uncoupled own-history dynamics or a common shock can account for the receiver
change without the claimed cross-effect. `contradicted` is the only addressed
state. `supported`, `compatible but not discriminated`, `unassessable`, a
missing entry, or an otherwise unresolved entry is unaddressed; it prevents
`discriminating_contrast_met` from being yes and therefore prevents that
family from qualifying. A documented partial shock contribution in a mixed
account is reported separately: it does not count as a supported sufficient
rival when independent evidence still establishes the cross-effect.

Treat the directional one-way accounts at the corpus level. `A → C only` is
addressed only by at least one qualified C → A family, and `C → A only` is
addressed only by at least one qualified A → C family. The stronger bounded
criterion's two-family, signed requirement in both directions necessarily
addresses both one-way accounts. Reciprocal coupling is the focal account,
not a rival that can block itself. Consequently, “no decisive rival remains
unaddressed” means that both family-level alternatives are addressed for every
family counted toward the threshold and that both one-way accounts are
addressed. Do not use a majority of rival-matrix entries or treat unknown as
contradiction.

For each direction, the sign condition requires distinct `family_id` values:
there must be an enablement-or-both family and a different constraint-or-both
family. One family coded `both` cannot satisfy both required sign observations;
two distinct `both` families can. This rule does not allow either family to
count more than once toward the two-family minimum.

Run the complete gates and adjudication independently at 60 and 180 days. Keep
the 90-day category as the primary decision. If **either** sensitivity horizon
returns a different decision category or fails a gate that passed at 90 days,
qualify the primary conclusion as timing-sensitive and state which horizon
changed and how. Do not replace or upgrade the primary category when a
sensitivity result is more favorable. Report both sensitivity results even
when neither changes the category.

## Registered Outputs and Claim Decisions

[CM-01](../claims.md#cm-01--antinomies-as-mutually-dependent-relations) receives
a concrete candidate test, not evidence merely because governance is divided.
If G1 through G3 pass and the full bounded reciprocal category holds at 60, 90,
and 180 days, raise CM-01 from C1 to C2 for the explicitly bounded ASF
project–foundation domain. This is enough for provisional evidence bearing on
an existential “some relations” claim, but cannot exceed C2 because the four
comparisons share one selected institution and no removal intervention occurs.
If the primary result is timing-sensitive or falls in any lower category, keep
CM-01 at C1 and record whether this candidate is narrowed, not retained, or
indeterminate. No result here proves that removing a pole necessarily
transforms the relation; that requires a separate intervention or removal test.

[CM-04](../claims.md#cm-04--cybernetic-dynamics-can-formalise-antinomies) retains
the [item 3 narrowing](../decisions/antinomy-structural-robustness.md). This
study tests whether its directional vocabulary can be mapped to observations
and discriminates accounts; it cannot validate the numerical toy model's
parameters, attractors, or predictive superiority. Do not fit logistic or
arctangent equations to narrative labels. Any later quantitative comparison
needs its own measurement model and preregistration before fitting.

Make an explicit observational-adequacy decision for CM-04. If G1 through G3
pass and the decision table returns a non-indeterminate category at the primary
horizon, retain the A/C directional vocabulary as observationally usable in
this domain. If G1 passes but G2 fails for insufficient or unclassifiable
opportunities, or G3 fails for coding instability, narrow its empirical
applicability and state which failure occurred. If G1 fails, withhold the
mapping decision because source access, not the vocabulary, failed. None of
these outcomes changes CM-04's C1 confidence in the numerical model; it changes
only the warranted empirical scope of its terms.

For the nested [CM-12](../claims.md#cm-12--decentralisation-has-generative-and-disorganising-effects)
test, use only qualified families with a documented shift of binding decision
authority toward the PMC that begins inside the primary event-onset window.
Provisional bounded support requires two distinct families across at least two
PMCs: at least one generative family with `autonomy_change = expanded` and
`newly_feasible_action_executed = yes`, and at least one disorganising family
with `coordination_burden_change = increased` or a named shared commitment coded
`failed`. For
[CM-13](../claims.md#cm-13--centralisation-has-enabling-and-suppressive-effects),
apply the same cardinality and onset rules to shifts toward foundation
authority: at least one enabling family must have
`newly_feasible_action_executed = yes`, and at least one suppressive family must
have `autonomy_change = restricted`. Every family must meet the primary
directional witness and rival-resolution rules, and
`authority_outcome_link_met` must be yes; the two signs must be in separate
families.

If G1 through G3 pass and a nested mixed-effect criterion holds at all three
horizons, raise that claim to C2 only for the ASF decision-authority layer. A
timing-sensitive or single-sign result leaves it at C1 and narrows the proposed
conditions. No qualifying families under passed gates count against this ASF
instantiation; failed gates produce no claim-level direction. These tests do
not measure communication-network concentration, ownership, or the other
layers named in the general claims.

Institutional viability is separate from both A and C: record an official
change in project/PMC status or an explicit inability to meet an identified
governance obligation, with its authoritative source and duration. Retirement
is not automatically failure. Lack of releases, low traffic, or a missing
report alone is not collapse. If no independent status/obligation evidence
exists, viability is unknown. No toy threshold such as 0.1 is transferred to
institutional records. CM-05 and the print/Reformation claims remain untouched.

Regardless of causal gate outcomes, publish four reusable registered products:
the month-level source-access map; the screened and sampled episode inventory;
direction × sign × authority-shift × disposition tables at all horizons; and a
ledger of which measurement or rival condition blocked each candidate. These
are descriptive infrastructure, not consolation prizes recoded as confirmation.

## Deliverables and Stop Rule

The later evidence pass must publish the source inventory, screening and
deterministic-sampling log, episode/family ledger, A/C and authority-shift
component records, shock ledger, contrast pairs, first and blinded-recode
values, recode disagreements, executable audit report, missingness tables,
per-family rival matrix, nested claim tables, and decisions under all three
horizons. Include source URLs, locators, dates, retrieval hashes, and the
registration commit. Preserve negative and unresolved cases. Retrieve all
eligible cross-boundary records and the fixed local baseline sample or declare
the work incomplete; resource limits do not authorize outcome-based stopping.

Before retrieving case records, implement and freeze the blank data schemas,
sampling functions, horizon calculations, gate calculator, nested-claim
calculator, and synthetic tests for the executable audit. Later bug fixes
require the same dated-amendment disclosure as prose changes.

This item ends with the accepted registration packet. No case evidence,
outcome classifications, external contacts, publication, or scheduled
collection is authorized by creating it. The next ordered cycle deliverable
is item 5's print/Reformation evidence pass; an ASF evidence pass needs a
separate work item after this registration is accepted.

## Registration Amendment 1 — Review Clarifications

**Date:** 2026-09-04. **Reason:** CodeRabbit review and re-review of PR #13
identified eight ambiguities or incomplete guards before packet acceptance.
**Exposure since registration:** no additional ASF source, selected-project
record, case outcome, or external reviewer code was inspected. The design-stage
exposure remains exactly that disclosed in the source audit. **Affected
analyses:** G3 audit-frame selection and agreement, rival resolution,
signed-family cardinality, timing sensitivity, and tests guarding the cohort,
links, horizons, and manifest types.

This amendment supersedes the ambiguous rules in registration anchor commit
`00d696ed80bd388955f622e0611853165f19508c` for future evidence work. It does
not change the institution, cohort, observation window, source cutoff,
constructs, primary horizon, rivals, thresholds, or collection status. The
original commit remains in history. The clarified rules above are prospective:
no evidence record or result exists to reclassify under either version.

## Registration Amendment 2 — Solo Completion and Research Yield

**Date:** 2026-09-05. **Reason:** The researcher disclosed that the programme is
independent, has no institutional or grant backing, has no budget for a second
coder, and requires every experiment to be completable without external human
aid. Review also found that the original corpus cost was disproportionate to
its prespecified claim consequences. **Exposure since Amendment 1:** no
additional ASF source, selected-project record, case outcome, or external
reviewer code was inspected. The design-stage exposure remains exactly that
disclosed in the source audit. **Affected analyses:** G3, routine-release
sampling, measurement fields, deliverables, and decision rules for CM-01,
CM-04, CM-12, and CM-13.

This amendment replaces the mandatory second-human audit with the solo
stability and reproducibility gate, replaces the local-only release census with
a deterministic project-quarter sample, and adds the nested analyses and
claim-level consequences above. The original human-audit rule remains visible
in Git history but is infeasible under the programme constraint and will not be
reported as a primary or sensitivity result. An optional independent
replication may be added later only as a separately labelled robustness study;
it cannot determine completion or overwrite the registered solo analysis.
Because no case record has been collected or coded, these changes are
prospective and do not respond to observed results.

## Conclusions and Next Steps

This packet warrants treating ASF project autonomy and foundation coordination
as a specified, potentially falsifiable candidate relation. It establishes no
reciprocal effect. The main risks are public-record underidentification and
single-researcher coding instability, which the gates must expose rather than
conceal through assumed zero effects or fictitious independence. CM-01, CM-12,
and CM-13 remain C1 pending evidence but now have explicit bounded routes to C2.
CM-04 retains its narrowed C1 formal warrant and gains an empirical-scope
decision rather than a promise of numerical validation.

Review and accept this packet before retrieving case records. The next action
for the ASF study is to implement and freeze its blank schemas and executable
audit, followed by the registered source/cohort audit and, only if appropriate,
the full episode comparison. Neither that implementation nor either evidence
pass begins in this package.
