# ASF Autonomy and Coordination: First-Pass Working Record

## Status and Authority

- **Started:** 2026-09-22, on the owner's instruction to start third-cycle item 3.
- **Status:** Item 3 accepted by the owner on 2026-10-26. Both validation
  runs passed and [PR #19](https://github.com/cyborg-nomade/cybernetic-mutualism/pull/19)
  was merged at `c592e40a24184ee979e76dbd2950a8f8599cc600`, preserving approved
  head `46d08fe31b33f5b2ad1709a422719bd501ed3bb2`. The
  [completion package](../data/asf-item3-first-pass-2026-10-23/README.md)
  and simultaneous source/first-pass/frame/blank-recode lock are unchanged.
  Item 4 is authorized; its waiting period and blinded audit remain pending.
  G2/G3 and aggregate claim decisions are uncalculated. All claims remain C1.
- **Checkpoint acceptance:** The owner approved the initial checkpoint through
  [PR #18](https://github.com/cyborg-nomade/cybernetic-mutualism/pull/18) on
  2026-09-23. Reviewed head `98561adb68ced781767ce4c4dc43143ebdc6a88a` was merged
  at `bec2d0787f7fd5772ca8aeae11ff4a7892b46a7a`. Acceptance does not complete
  item 3 or start the washout.
- **Accepted input:** Access snapshot
  `b2f8bfa1173199f2141a187c2a9ba768225711b7`, accepted through PR #17;
  [G1 passes](asf-autonomy-coordination-access-audit.md).
- **Frozen executable:** `18b13ff18500c33d8812459eda72ad6c11640f1a`.
- **Registration:** `00d696ed80bd388955f622e0611853165f19508c`, amendments
  `pr13-review-clarifications-2026-09-04` and
  `solo-completion-and-research-yield-2026-09-05`, and accepted supplement
  `tooling-audit-supplement-2026-09-16` remain operative.

The [preregistration](asf-autonomy-coordination-preregistration.md),
[codebook](asf-autonomy-coordination-codebook.md), and
[third-cycle plan](../decisions/third-cycle-plan.md) control the work. This
record retains exposure, descriptive interpretation and the completed first pass. It changes no
registered window, sampling rule, threshold, or causal criterion. The primary
onset window remains 2023–2025; context and follow-up remain bounded by the
registration, including the 2026-08-31 source-publication cutoff.

The dated progress sections below preserve earlier incomplete states. The
October 23 completion section supersedes their outstanding-work lists; it does
not retrospectively turn an accepted checkpoint into a completed first pass.

## Accepted September Corpus and Review Progress

The [working data directory](../data/asf-first-pass-2026-09-22/README.md)
contains every primary-window index occurrence, provisional navigation queues,
exact reviewed-message hashes, bounded board-section locators, and new
referenced-source retrieval metadata. The accepted source snapshot was
reverified offline: its 393 retrieval receipts and all 144 index/export
Message-ID multisets passed. That is an input integrity result, not screening
completion.

| Project | Indexed occurrences | Review in this checkpoint |
| --- | ---: | --- |
| Ant | 651 | 21 navigation groups, 89 complete plain-text message bodies; 17 Ant attachment sections and one Board resolution |
| HTTP Server | 1,687 | Initial title reconnaissance; substantive screening pending |
| Maven | 8,338 | Initial title reconnaissance; substantive screening pending |
| Tomcat | 25,087 | Initial title reconnaissance and duplicate-body comparison; substantive screening pending |

Across all four projects there are 35,763 occurrences and 35,739 distinct
project/Message-ID pairs. The 21 repeated-ID groups have 45 exported variants.
Seven groups contain different decoded plain-text bodies: they are Tomcat
GitHub notifications whose original IDs were reused for edited descriptions.
All variants are retained with separate byte hashes. In the other repeated-ID
groups the decoded plain-text bodies match; this does not make the complete
MIME messages identical. Neither delivery multiplicity nor version count is
an independent issue-family count.

There are 6,015 navigation groups in the subject-review queue, of which 5,994
remain pending. Mechanical notification routes are also provisional; they
are not final exclusions. Subject grouping cannot establish issue identity:
the Ivy discussion spans two products, multiple years, and an external-prefix
variant. Full eligibility review must resolve changed titles, references,
different requested deliverables, and source versions before sampling.

The reviewer-facing source identifier is the original RFC Message-ID, including
angle brackets. Archive IDs remain occurrence locators. No invented source
hash is substituted into the registered release-sampling key. This implements
the existing original-ID requirement before any baseline draw. Topic hashes
are navigation aids only.

Reading selected Ant attachments does not complete the board/officer census.
Six of the 17 attachment slots read are empty. Their agenda dispositions need
checking separately; an empty slot is not a zero, proof of no report being due,
or an inferred obligation failure. The July/August 2025 reports and chair
resolution reveal a candidate that would be missed by relying only on dev-list
titles. The remaining full minutes, officer reports, and special-meeting
records must still be screened.

## Descriptive Observations Requiring Follow-Up

These observations precede measurement-grid and causal classification work.
They are not qualified witnesses. The
[review journal](../data/asf-first-pass-2026-09-22/subject-review.csv) records
every reviewed topic, provisional disposition, and reason. The
[89-message manifest](../data/asf-first-pass-2026-09-22/reviewed-messages.csv)
maps each original ID below to a public archive locator and exact accepted
export block. Do not count a project report reprinted in Board minutes as an
independent account of the project's own conduct.

### IvyDE Retirement and Ivy Continuation Are Different Deliverables

The discussion opened on 2023-08-22 with
`<87cyzfukuf.fsf@v45346.1blu.de>`. Its author explicitly characterized it as
personal opinion and discussion, not a PMC vote. It reported difficulty
maintaining Ivy and IvyDE, including vulnerability work and unfamiliarity with
the code. These are actor-reported conditions; independent shock evidence and
exposure remain to be assessed.

For IvyDE, the 2023-11-19 proposal
`<877cmd3ao2.fsf@v45346.1blu.de>` initially sought a move to the Apache Attic.
After reporting the vote passed, the proposer corrected the route on
2023-11-23 in `<87zfz5q6px.fsf@v45346.1blu.de>`: the Attic process did not apply
to this subproject, and the votes could not simply be repurposed. A replacement
local retirement vote opened in `<87v89tq6mg.fsf@v45346.1blu.de>` and passed on
2023-11-26 in `<87jzq4y210.fsf@v45346.1blu.de>`. The initial proposal, correction,
replacement vote, and retirement result concern the same underlying
deliverable. The correction does not identify a Board refusal or establish a
change in where binding authority resided.

The local procedure is supported by the
[official Ant source at SVN revision 1826197](https://svn.apache.org/repos/asf/!svn/rvr/1826197/ant/site/ant/sources/processes.xml),
last modified 2018-03-08. It places the retirement vote on the main development
list with the Ant PMC and includes requesting Infra to make the repository
read-only. The retrieved current source and immutable revision have identical
bytes. The current Attic page was consulted only for discovery; its current
wording is not independently dated evidence of the 2023 rule.

The result follow-up `<87fs0sy08o.fsf@v45346.1blu.de>` cites
[INFRA-25209](https://issues.apache.org/jira/browse/INFRA-25209) and
[INFRA-25210](https://issues.apache.org/jira/browse/INFRA-25210). Both ordinary
anonymous requests redirect to login. No ticket content, resolution, actor,
or event time was obtained. The December 2023 Ant report, Attachment C,
states that IvyDE was archived as of November 26 and links the local vote.
That supports the project's stated retirement disposition; it does not by
itself supply a separately observed Infra implementation.

For Ivy, the same broad discussion continued into October/November 2024.
`<00415bf2-1aa6-4d7d-a038-ae7f62a1bf35@apache.org>` proposed initiating a
retirement vote. On November 17,
`<457381523.1903503.1731840000859@mail.yahoo.com>` offered maintenance, and
`<9795f2a3-2acf-42dd-b2b1-e19fe7036fe7@apache.org>` explicitly stated that the
retirement plan was abandoned and Ivy would remain under the Ant PMC. The
February 2025 Ant report, Attachment D, reports subsequent maintenance and
Ivy 2.5.3. Preserve the withdrawal and continuation rather than treating a
missing retirement vote as missing disposition. The earliest relevant 2023
proposal remains part of onset/family review; do not reset the horizon clock
to October 2024 merely to bring the reversal inside it.

### Chair Succession Is an Official Act, Not Automatically an Authority Shift

The July 2025 Ant report, Attachment E, records the outgoing chair's wish to
step down and a successor-selection process. The August report, Attachment C,
states that internal PMC deliberation produced a nomination. Special Order 7D
in the August 20 Board minutes records the PMC's recommendation by vote and
the Board's unanimous appointment of the successor.

The resolution provides actual Board conduct and an organizational role
attribution. It is a promising cross-boundary candidate for full coding. The
internal deliberation is a referenced nonpublic channel; its contents and
exact timing are not reconstructed. A change of officeholder alone does not
show a before/after change in binding authority for a decision class. The
applicable bylaws, nomination interval, burden/option evidence, and relevant
shock/rival/contrast records still require a complete bundle before any
qualification decision.

### Service Reports Need Actor and Timing Checks

The June 2024 Jenkins exchange reports an unanswered Infra request, followed
by restored permission to trigger Ant jobs. Both statements come from the
requester (`<8d6ca10f-9a8f-418b-944c-5fb31e8a1673@apache.org>` and
`<b626c55b-dca0-4fad-a7c7-6a6146727f72@apache.org>`). Preserve the reported
restoration while seeking public corroboration of the actual request and
receiver act. Do not manufacture independent evidence from two self-reports.

The March/April 2025 Ivy Gitbox thread describes a temporary local GitHub-remote
workaround and later synchronization. The May 2025 Ant Gitbox message reports
a similar symptom for another repository. Common symptoms do not establish
one underlying service request or a shared independently documented shock.
The May 2023 Gump/Java 21 exchange likewise reports a build break and suggests
a workaround without establishing a foundation decision-maker or remedy.

The January and September 2023 Bugzilla-version requests were answered that
the requested changes were already present. The requesters acknowledged
overlooking them. These are important false positives for any request/response
heuristic: the available exchange does not establish foundation authority or
a sender-first change. The September 2025 RAT testutils/GitHub Linux exchange
is technical troubleshooting, with no documented foundation-project decision
request in the inspected thread.

### Local Decisions and Shared Messages Remain in the Census Queue

The Ant 1.9.x EOL vote and June 2024 result concern ending a release series,
not an ordinary version-release opening. Keep them as a local governance
candidate rather than placing them in the routine release sample. The August
2024 report restates the EOL decision. The Ivy 2.5.3 DOAP correction belongs
with release-family follow-up; mentioning a shared catalogue does not itself
establish a requested cross-boundary commitment.

The March 2023 Board reminder to PMC members and August 2023 Comdev notification
threading message require cross-project family matching. The latter announces
a default change with an opt-out, not an observed implementation in every PMC.
The messages' claimed roles, applicable authority, actual exposure, responses,
and effective rules require checking. A foundation-wide initiating directive
must not become four independent confirmations.

The November 2025 Ant SBOM discussion compares implementation options and
maintenance costs while mentioning CISA/CRA uncertainty and an ASF reference.
It is a policy/technical-direction candidate. A link to guidance is not proof
of a binding foundation mandate, and the discussion does not by itself prove
implementation. The applicable dated policy and independently documented
external precursors remain pending. No legal conclusion is drawn here.

## Verification

The accepted-input verifier and checkpoint verifier both passed. The latter
reconstructs all index occurrences and duplicate variants, checks the reviewed
message bytes and section locators, and reports the incomplete state without
calculating later gates. Four preparation tests cover human replies to
notification titles, vote/result navigation, reused IDs with changed bodies,
and refusal to overwrite reviewer notes. The full `just check` run passed:
197 tests, 90.59% production branch/statement coverage, lint/format checks,
strict production typing, and both model-output reproduction checks. These
checks validate software and declared metadata; they do not certify the
substantive review as complete or independently replicated.

The 2026-09-23 review follow-up resolved all three CodeRabbit findings:
explicit delimiter notation, UTF-8 retained-text reads, and comparison of the
saved verification report with recomputation. The updated checkpoint verifier,
all 200 tests, the full `just check` run, and both CI runs passed at the accepted
head. Evidence values and progress counts did not change during this review.

## October 4 Ant Continuation

On the owner's instruction to resume item 3, the
[additive Ant continuation](../data/asf-ant-screening-2026-10-04/README.md)
screens all 651 Ant subject-index occurrences and preserves the accepted
September data unchanged. It adds 37 complete plain-text topic reads covering
105 messages, bringing cumulative body review to 58 Ant navigation groups and
194 messages. Subject-only exclusions and pending ambiguous bodies remain
separate from full body review and final eligibility coding.

Five provisional release families preserve seven candidate-vote openings,
including the cancelled/rebuilt Ivy 2.5.2 and Ant 1.10.15 candidates. The
December 2024 Ivy 2.5.3 vote retains its January 2025 announcement as follow-up;
the announcement does not create a new baseline opening. No sample is drawn.
The classifier and Pack200 threads reveal account-access candidates that
would be missed by excluding all technical-looking subjects. Public Infra
receiver records and dated account-approval authority remain unresolved.

Six bounded Ant agenda entries now resolve the September empty-attachment
question: all explicitly state that no report was submitted. This establishes
non-submission, not a due-date schedule, cause, duration, or institutional
inability. The full Board/officer census is still pending. The continuation
records exact source locators, hashes, read scope, and remaining work without
qualifying witnesses or changing G1, claims, or the registered design.

## Corpus Continuation Within PR #19

The owner authorizes continued work in PR #19 until item 3 is complete,
followed by review. The [working corpus continuation](../data/asf-item3-screening-2026-10-04/README.md)
retains independent provisional judgments on 539 HTTP Server, Maven and Tomcat topics after
reading their complete exported plain-text bodies. Title inspection covers all
6,015 entries in the discussion-topic queue and 12,184 mechanically routed
topics across all four projects (18,199 distinct topic IDs). Tomcat's 5,969
exact payload groups preserve 11,992 original title variants; generic, policy
and service-related payloads have received original-body checks for all 235
topics in the original candidate queue. New bounded references remain open.
Baseline and follow-up subject screening is still incomplete.
Its 2,473 export variants
preserve original Message-IDs, exact raw/body hashes and monthly block
locators. Duplicate index deliveries do not multiply message variants.

The continuation also retains 1,166 exact section locators from October
2022 through December 2025 Board proceedings, including the August 2025
special meeting, foundation officer reports, selected
PMC reports, and relevant Attic/Community Development context. The March
Infrastructure report directly documents the shared GitHub Actions approval
rule and project opt-outs. The April report dates the committer-only INFRA
Jira restriction. A ticket login response therefore bounds public evidence;
it does not establish rejection of the underlying request.

The August 24 2025 logo resolution is retained separately as a visually read
action without meeting, with the exact image hash. Baseline records date Jira
account approval, Matomo transition, Travis withdrawal notice and Tomcat 8.5
EOL before the study window. Later reports do not automatically reset onset.
Bounded references, historical roles and the calendar attestation remain open.

The September HTTP Server report explicitly says the Git migration vote passed
but had not been implemented. Ant's December report dates IvyDE archiving to
November 26, while remaining a requester self-report. The January 2024 Board
supports technical enforcement of website-tracking policy, and Privacy still
lists the implementation ticket as open in February. Authorization, reported
implementation and independent receiver evidence remain distinct.

Later Git migration proposals continue the earlier HTTP Server request rather
than resetting onset. In-window mod_wasm replies continue a 2022 proposal and
remain baseline context. The local chair's list ban and a subsequent Board
PMC removal are distinct governance acts; causal linkage remains unestablished.
Maven follow-ups also preserve the October 2024 inactive-access proposal,
separate Jira/GitHub/wiki/test-project boundaries, and GitHub support cleanup
that reportedly removed JLINK PR comments as well as duplicated issues. These
are provisional candidates requiring original receiver and authority evidence.

Provisional family labels, exclusions and file-level search notes are retained
separately from final episode measurements and witness qualification.

The Java-minimum discussion explicitly resumes a July 2022 Maven proposal;
its later runtime vote cannot automatically reset onset. June 2024 Support &
Care letters describe a German-government funding submission, with no award
or ASF approval established. Current linked issue representations include
post-cutoff edits and closures and serve only as reference navigation.

At the initial October 5 continuation, further collection retained all 36 baseline/follow-up monthly
index/export pairs locally, with 72 retrieval receipts and 10,392 indexed
occurrences. Every Message-ID multiset matched. Baseline Ant, HTTP Server and
Maven titles have been inspected; Tomcat and follow-up title screening remain
open. Twelve Ant/HTTP Server baseline topics have separately retained body
judgments. These contextual reads do not increase the in-window screening
count or create new eligible onsets. Packaging these new sources and metadata
for the final first-pass lock remains unfinished.

Current index timestamps, original Date headers and historical public delivery
headers remain distinct. The latter may supply a publication bound only after
explicit provenance checks. The source exports are unchanged, and this
continuation republishes no correspondence bodies. Its verifier checks exact
membership and locators while refusing to assert a sample or lock. Remaining
subject/body review, references, coding and registered locking were still open
at that snapshot.

## October 20 Release Frame and Baseline

All baseline and bounded-follow-up subject titles have now been inspected.
The local context ledger retains 139 independent topic judgments; packaging
the context evidence for the final first-pass dataset remains required.
Earlier SecurityManager and Maven Java 17 originals establish pre-window
proposals, while Ant's November 11 2025 SBOM proposal sets its 60/90/180-day
endpoints to January 10, February 9 and May 10 2026. Later implementation
cannot silently enter an earlier horizon.

The [release frame and draw](../data/asf-release-frame-2026-10-20/README.md)
retain 724 independently screened original candidates, of which 698 are formal
opening messages. Exact duplicates, corrected ballots, canceled candidates
and version-changing retries reduce to 647 independently scoped release
families. Joint ballots split independently releasable components while
preserving their shared original source ID. The unchanged frozen sampler
selects one family in each of 36 nonempty project-quarter blocks; all 48
blocks, including 12 empty ones, retain counts and ordered hash keys. Selected
IDs will not be replaced because of an inconvenient or missing outcome.

Identity review includes 806 closure candidates, a 40-message supplement and
13 reply/nonstandard opening checks. It preserves failed votes, expedited
successful votes followed by corrective releases, and approval without
confirmed publication. The frame record explicitly documents the interpretive
M2/M3 and Sitetools M17/M18 family boundaries. Its verifier re-extracts source
variants from accepted export bytes and reproduces the draw; it does not
affirm historical publication, actor authority, causal effects or completeness
of the larger first pass.

The draw is now fixed for the ensuing baseline evidence work. Source
eligibility and dated-authority checks, selected-family outcomes, the
cross-boundary census and component/shock/rival/contrast records remain
unfinished. No first-pass lock or washout has begun.

## October 20–21 Baseline and Dated Policy Review

The [evidence-review record](../data/asf-evidence-review-2026-10-20/README.md)
now retains independent findings for all 36 selected baseline families, their
complete opening-topic body reviews and separately declared closure records.
The source check re-extracts 458 original raw/plain-body variants. Three dates
were corrected against the original result messages: GPG 3.2.8 passed on July
2, Tomcat 10.1.6 on February 24, and Tomcat 9.0.109 on September 5. Their
opening-quarter assignments are unchanged. An October 21 parser comparison
found one reply with unintelligible trailing bytes in the reading-aid decoding;
both decoded hashes and the unchanged raw hash are preserved. The explicit
vote and its interpretation are unchanged, and the frozen parser is unmodified.

The same record retains the pre-window ASF voting/release rules, all 16
2023–2025 source changes to those documents, and 24 complete dated Infra policy
versions. Thirteen independent interpretations distinguish substantive rules
from link and metadata changes. The external-contributor GitHub Actions
approval default appears in the February 3 2023 source; March 19 adds a
conditional exception. The March project experience cannot supply its earliest
onset. The 2025 expedited-release explanation requirement is not applied to
2023/2024 votes. The erroneous July date on the first August 2024 home-hosting
retirement notice remains visible alongside its correction. Repository source
dates are kept separate from website deployment and receiver implementation.

Explicit family-identity decisions merge shared circulars, separate independently
requested deliverables within joint threads, and preserve pre-window origins.
They do not yet certify all final act associations, component measurements or
causal classifications. Source publication/authority completion, the full
census, the deterministic audit supplement and registered locking remain open.

## October 23 Completion and Review Boundary

The [finalized data package](../data/asf-item3-first-pass-2026-10-23/README.md)
contains the exact native ledgers, source catalogue, versioned original bytes,
individual interpretations and simultaneous lock receipt. All 18,199 primary
subject-topic IDs were screened, including mechanical notification routes;
541 selected primary topic bodies and 139 baseline/follow-up topic bodies
have independent retained judgments. Subject screening does not mean every
unrelated correspondence body was read. The native screening table records
act/family associations rather than enumerating every ordinary excluded title.

The review covers 1,166 main, officer, fixed-cohort, Community Development and
Attic section locators through December 2025, plus 170 January–June 2026
follow-up sections. The August 24 written consent and August 25 special
meeting remain distinct. Approved minutes retain independently bounded public
SVN versions. Unknown earlier initiation is not replaced by a meeting date or
later report. New 2026 proposals do not enter as new primary-window onsets.

The final required union contains 491 family/project pairs: 368 analysis pairs,
including the fixed 36-release baseline, and 123 additional audit-only release
pairs. Each has both directions and three independently coded horizons,
giving 2,946 native measurement records. Audit-only releases do not enter the
primary baseline or causal threshold counts. The selected audit release
families fall within the prospectively reviewed source-reading superset.
Their complete opening/retry bodies and closure records are retained.

Each documented directional opportunity has a five-rival matrix, a project
and Foundation search record covering the registered lookback/horizon where
its dates are known, and the frozen deterministic contrast choice. Undated
initiation prevents certifying an exact search window, even when the broad
retained context has been searched. Unknown exposure is never an untreated
control; an absent eligible comparator is recorded explicitly. Missing provider
acts, timing, individual capacity and exposure remain unknown. Completion of
coding does not imply that the registered identifiability gate will pass.

The shock ledger distinguishes independently documented external precursors,
unverified contextual candidates and internal own-history explanations. Two
2026 upstream precursors were independently checked during follow-up before
final rival/witness adjudication. Earlier mutable `qualified_witness = no`
values were incomplete scaffold placeholders, not locked classifications.
This sequence is disclosed in the scoped completeness attestation. No
aggregate causal calculation preceded the final lock.

Several decisions materially bound the first pass:

- Pre-window release/voting rules and observed project decisions establish
  unchanged formal PMC release jurisdiction. They do not establish unchanged
  autonomy, validity of every individual ballot, or absence of private pressure.
- Sixty-five retry/repetition associations were incorrectly transferred as
  independently eligible release openings in the mutable native screening
  table. The repair preserves the 647-family universe and exactly reproduces
  all 48 recorded strata and the original 36 selected openings. Prior erroneous
  bytes and repair hashes remain available; there was no outcome-based redraw.
- Maven's October 2024 deletion of an inaccurate process description is distinct
  from its February 2025 required-review proposal. Old founder-guidance
  relocation is distinct from the new two-year Marketing approval condition.
  MFA has positive pre-window history; the continuing Atlassian Cloud migration
  has an unknown earlier onset. Nonadoption alone excludes none of these.
- The shared 2025 logo act has consistent four-project scope, with Tomcat
  source uptake recorded separately. No equal receipt or response is copied
  to the other projects. Late Ant SBOM, HTTPD retirement and Maven ATR evidence
  updates the continuing history without restarting its original horizon.
- Two mislabelled release-result subjects are retained unchanged. Exact-version
  announcements independently support the corresponding local outcomes; the
  mismatched results are not silently repaired or treated as decisive links.
- Ordinary appointment processing, entitlement repair, repository maintenance
  and dormant-service cleanup remain available rival explanations. A known
  contact or actual local edit does not by itself discriminate a cross-effect.

All required original variants have separate exact hashes. Alternative raw
representations remain versions of the same Message-ID rather than new acts.
The conservative publication bound applies across all required versions;
unknown historical availability cannot supply decisive support. Raw transport
proofs travel with the corresponding sources. The blank recode contains only
the frozen whitelist, neutral whole-original source locators and blank coding
fields. First-pass notes, source eligibility judgments and prior specific
interpretive locators remain outside that bundle.

The frozen validator passes without errors. The repository checks pass 209
tests with 90.59% coverage, lint/format, strict production typing and both model
reproduction checks. The completion verifier reconstructs native CSV and
source bytes from accepted repository originals and the additional compressed
source store. No registered executable, threshold, window or sampling rule was
changed. The owner accepted the complete item on October 26 and authorized the
merge. Both GitHub validation runs passed, and PR #19 was merged at
`c592e40a24184ee979e76dbd2950a8f8599cc600`. The separate
[audit execution record](asf-autonomy-coordination-audit.md) carries item 4;
this administrative closeout does not reopen or alter the locked evidence.

## Conclusions and Next Steps

This first pass now warrants a complete, source-qualified and reproducible
input to the registered later decision path. Explicit unknowns bound what the
public record can identify; they are not observations of no effect. The wider
programme and every claim remain at C1. The simultaneous lock begins the
washout recorded in the package receipt, subject to no further ASF evidence
work. Any renewed evidence work requires a fresh valid washout boundary.

Owner review is complete. After the required 14 complete UTC days, item 4 is a
**research and writing task using the frozen code**: delayed blinded recoding,
initial agreement, reconciliation and the registered gate/claim report. A
registered gate failure stops subsequent causal comparison. Item 5 is a
**writing task** applying the reached result or registered stop to the cycle
synthesis and next discriminator. No favorable finding or new code is needed
for either item to produce a valid research result.
