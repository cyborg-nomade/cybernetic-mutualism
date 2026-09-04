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
CM-01 or CM-04 and changes no confidence level. The records already exist;
this is prospective specification of an analysis of historical records, not
preregistration before the historical events occurred. The source audit
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

Enumerate all public formal release-vote openings and all proposals requesting
a binding change in technical direction, project governance, or foundation
services in the projects' development lists. Include unsuccessful, withdrawn,
unanswered, and apparently routine proposals. Exclude ordinary patches, user
support, automated notifications, release announcements without a decision
record, and personnel speculation. Treat a referenced public issue tracker or
official service ticket as corroboration, not as an unrestricted additional
sampling frame. Follow references until the same episode closes or reaches
the horizon; do not follow unrelated disputes into new projects or years.

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

**G3 — Coding audit.** Complete the codebook's independent human review before
adjudicating the hypothesis. If a second reviewer is unavailable, publish a
single-coder descriptive ledger only; do not claim this gate was passed.

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
when neither changes the category. No automatic confidence increase follows
from this small, selected, nonexperimental study.

## Relation to CM-01, CM-04, and Institutional Viability

[CM-01](../claims.md#cm-01--antinomies-as-mutually-dependent-relations) receives
a concrete candidate test, not evidence merely because governance is divided.
Even a retained reciprocal interpretation would not prove that removing a
pole necessarily transforms the relation. Such necessity would require
separate intervention or removal evidence not promised here.

[CM-04](../claims.md#cm-04--cybernetic-dynamics-can-formalise-antinomies) retains
the [item 3 narrowing](../decisions/antinomy-structural-robustness.md). This
study tests whether its directional vocabulary can be mapped to observations
and discriminates accounts; it cannot validate the numerical toy model's
parameters, attractors, or predictive superiority. Do not fit logistic or
arctangent equations to narrative labels. Any later quantitative comparison
needs its own measurement model and preregistration before fitting.

Institutional viability is separate from both A and C: record an official
change in project/PMC status or an explicit inability to meet an identified
governance obligation, with its authoritative source and duration. Retirement
is not automatically failure. Lack of releases, low traffic, or a missing
report alone is not collapse. If no independent status/obligation evidence
exists, viability is unknown. No toy threshold such as 0.1 is transferred to
institutional records. CM-05 and the print/Reformation claims remain untouched.

## Deliverables and Stop Rule

The later evidence pass must publish the source inventory, screening log,
episode/family ledger, A/C component records, shock ledger, contrast pairs,
reviewer disagreements, missingness tables, per-family rival matrix, and
decision under all three horizons. Include source URLs, locators, dates,
retrieval hashes, and the registration commit. Preserve negative and
unresolved cases. Retrieve all eligible records in the fixed scope or declare
the work incomplete; resource limits do not authorize outcome-based stopping.

This item ends with the accepted registration packet. No case evidence,
outcome classifications, external contacts, publication, or scheduled
collection is authorized by creating it. The next ordered cycle deliverable
is item 5's print/Reformation evidence pass; an ASF evidence pass needs a
separate work item after this registration is accepted.

## Registration Amendment 1 — Review Clarifications

**Date:** 2026-09-04. **Reason:** CodeRabbit review of PR #13 identified six
ambiguities or incomplete guards before packet acceptance. **Exposure since
registration:** no additional ASF source, selected-project record, case
outcome, or external reviewer code was inspected. The design-stage exposure
remains exactly that disclosed in the source audit. **Affected analyses:** G3
audit-frame selection and agreement, signed-family cardinality, timing
sensitivity, and tests guarding the cohort, links, and horizons.

This amendment supersedes the ambiguous rules in registration anchor commit
`00d696ed80bd388955f622e0611853165f19508c` for future evidence work. It does
not change the institution, cohort, observation window, source cutoff,
constructs, primary horizon, rivals, thresholds, or collection status. The
original commit remains in history. The clarified rules above are prospective:
no evidence record or result exists to reclassify under either version.

## Conclusions and Next Steps

This packet warrants treating ASF project autonomy and foundation coordination
as a specified, potentially falsifiable candidate relation. It establishes no
reciprocal effect. The main risk is public-record underidentification, which
the gates must expose rather than conceal through assumed zero effects.
CM-01 remains C1 with a registered test; CM-04 retains its narrowed C1 formal
warrant and receives no empirical validation.

Review and accept this packet before retrieving case records. The next
discriminating action for the ASF study is the registered source/cohort audit,
followed only if appropriate by the full episode comparison. Neither that
evidence pass nor the print/Reformation evidence pass begins in this package.
