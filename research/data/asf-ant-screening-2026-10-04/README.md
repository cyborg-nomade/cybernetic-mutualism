# ASF Ant Screening Continuation — 2026-10-04

**Item 3 remains incomplete.** This is an additive continuation of the accepted
[September checkpoint](../asf-first-pass-2026-09-22/README.md), reviewed head
`98561adb68ced781767ce4c4dc43143ebdc6a88a`. The accepted sources and that
checkpoint remain unchanged. The original registration, both amendments,
accepted tooling supplement, and executable freeze
`18b13ff18500c33d8812459eda72ad6c11640f1a` remain operative. No sample, completed
measurement dataset, gate decision, audit frame, or first-pass lock is created.

## Actual Review Scope

| File | What was inspected and retained |
| --- | --- |
| `ant-subject-screen.csv` | Every one of Ant's 651 indexed occurrences across all 36 primary-window months, including original notification routes. Each subject has a scope, classification, and reason. |
| `topic-review.csv` | 37 additional navigation groups whose complete decoded plain-text bodies were read. These are descriptive notes, not final registered eligibility or opportunity codes. |
| `reviewed-messages.csv` | The 105 additional message blocks read, with original IDs, public URLs, original Date headers, exact export locators, and raw/plain-body hashes. |
| `release-families.csv` | Five provisional release families linking formal votes, retries, results, announcements, and context. No family has been selected for the baseline. |
| `reviewed-board-sections.csv` | Six Ant agenda entries resolving the empty attachments already recorded in September. This is bounded agenda review, not a full Board/officer census. |
| `checkpoint.json`, `verification.json`, `verify.py` | Exact input/file hashes and a reproducible integrity/progress report. Verification cannot certify an interpretation or substantive completeness. |

Together with September's 21 groups and 89 messages, 58 Ant navigation groups
and 194 message bodies have now been read. The September data remain the record
of those earlier reads; only the new reads are listed here. Screening a subject
does not certify every body, attachment, reference, role, or follow-up as read.
The 46 occurrences classified `body_pending` and one `release_context_body_pending`
remain explicit. Most concern OpenJDK announcements and replies; they still
need ambiguity/context review. Other retained candidates also need references,
source eligibility, family resolution, and authority checks.

Notification and ordinary-patch exclusions were made after inspecting all
Ant titles, including the titles outside September's review queue. Their
subject-only scope stays explicit. Related patch or notification evidence may
still be followed from an eligible episode. Conference/travel/campaign titles
are excluded as event announcements at this screening level; this does not
assert anything about an individual's grant outcome. Ordinary support bodies
were inspected where their eligibility needed resolution. An Apache email
address is not used as an authority citation.

`index_timestamp` is retained archive navigation metadata, not a replacement
event or publication date. The release opening dates come from the original
Date headers. Publication eligibility remains to be established separately.
Topic hashes identify navigation groups; family IDs describe provisional
deliverables and never replace original source IDs in sampling keys. These
tables are working journals, not substitutions for the frozen CSV schemas.
No new correspondence bodies, personal contact details, or new network sources
are published in this continuation.

## Release Families and Preserved Reversals

| Deliverable | First formal vote | Observed sequence in the inspected correspondence |
| --- | --- | --- |
| Ant 1.10.13 | 2023-01-04 | Passage and announcement January 10. A May reply quotes December 2022 planning; retrieve that baseline context without manufacturing another formal opening. |
| Ant 1.10.14 | 2023-08-16 | August 12 planning, August 20 passage, August 21 announcement, later launcher regression discussion. |
| Ivy 2.5.2 | 2023-08-17 | RC1 cancelled over the NOTICE year; RC2 opened the same day and passed August 20. The Eclipse update site was not built, with local environment difficulty reported. |
| Ant 1.10.15 | 2024-08-18 | February planning and July/August reminders precede RC1. RC1 cancelled August 21; corrections and RC2 August 25; passage August 29. |
| Ivy 2.5.3 | 2024-12-23 | Passage December 29, announcement January 2, 2025. DOAP correction belongs to the same release follow-up. |

Seven formal candidate-vote titles resolve into five provisional release
deliverables. Results, cancellations, and revised candidates do not add
independent families or sampling entries. The first formal vote supplies the
registered release-opening key; preceding planning remains visible as context
and must inform eventual episode-onset adjudication. The January 2025 Ivy
announcement does not supply a 2025 release-vote opening. The ordinary release
candidate frame remains provisional until the remaining project/foundation
records establish eligibility. No hash ordering or sample draw has been made.

The Ant 1.10.15 correction explains that adding a contributor to the list was
withheld because of the contributor's preference; it also reports fixing the
manual and misplaced release-note entry. Preserve the actual correction rather
than assume every stated cancellation issue was remedied in the same way.
The inspected messages describe local quality checks and changes, not a
documented foundation intervention. Repeated work alone cannot establish a
coordination burden caused by a foundation arrangement.

The Ivy 2.5.2 vulnerability disclosure states that the issue was reported to
the ASF security team on 2022-11-30 and made public on 2023-08-20. This is a
reference to earlier nonpublic reporting, not access to that channel or proof
of its contents. Preserve distinct report, publication, and release dates.
Java SecurityManager and Pack200 changes also supply possible dependency
context; they do not become independently established shocks merely through
the project's description. Dated primary sources and registered searches
remain necessary before shock/rival adjudication.

## Service Candidates Inside Technical Threads

The classifier discussion `topic-936778472cfc2862` contains a different
deliverable from the software patch. On 2024-02-03,
`<MW5PR16MB4848CC2A236D2F8842D72F1A91412@MW5PR16MB4848.namprd16.prod.outlook.com>`
reports that the Jira self-service page rejected Ant as a Jira project. The
reply `<87fry9wuvw.fsf@v45346.1blu.de>` explains that Ant uses Bugzilla while
Ivy uses Jira and states an intention to file an Infra bug. On February 5,
`<878r3yokvl.fsf@v45346.1blu.de>` says the author was told account creation
should work again. On February 15, the requester reports applying again and
`<87o7chlkkv.fsf@v45346.1blu.de>` states that the request was approved.

Retain account access separately from the classifier patch and the broader
Ivy continuation discussion. The inspected exchange does not provide an Infra
ticket, a direct Infra implementation record, or a dated delegation for account
approval. An intention to file a bug is not an observed filing; a statement
that a repair should work is not the requester's observed successful access.
The approval is a reported act requiring role attribution. These missing
links remain unknown rather than be converted to either a qualified effect
or an absence of opportunity.

The Pack200 thread `topic-d917f7ba5a2e5720` likewise includes an explicit
November 9, 2024 Jira account approval alongside ordinary build advice. Keep
the role/family question open; sharing the service name does not establish
that this is the same February request or service defect. Packaging Ivy with
Eclipse instead contains an informal licensing question and opinion, with no
identified requested foundation authorization. It is excluded as support;
no legal interpretation is adopted.

## Empty Attachments and Non-Submission

The Ant agenda entries for May/November 2023, February/November 2024, and
May/June 2025 explicitly state that no report was submitted. Their exact
bounded locators are retained in the Board review table. This resolves the
September ambiguity about those six empty attachment slots: they are explicit
non-submissions, rather than evidence that no report was due. It does not
establish the due-date schedule, inability to meet an obligation, cause,
duration, or collapse. Subsequent submitted reports and the chair succession
remain separate records; none is silently inferred from missing content.

## Reproduction and Remaining Work

From the repository root, verify accepted inputs, the accepted checkpoint,
and then this continuation:

```bash
uv run --locked python -c "import runpy; runpy.run_path('research/data/asf-access-2026-09-21/verify.py', run_name='__main__')"
uv run --locked python research/data/asf-first-pass-2026-09-22/verify.py
uv run --locked python research/data/asf-ant-screening-2026-10-04/verify.py
```

The continuation verifier checks every Ant index occurrence, new topic
membership and original message bytes, family-link membership and Date-header
dates, bounded agenda locators, retained hashes, and saved-output agreement.
It does not fetch sources, draw a sample, qualify witnesses, or start washout.
The other three project screens and full Board/officer census remain open.
Ant's pending ambiguity/reference work, dated authority and source-publication
checks, complete family census, registered local baseline, measurements,
shock/rival searches, contrasts, and audit/recode bundle are still required.

All three real-data verifiers passed. The full `just check` passed with 204
tests and 90.59% production statement/branch coverage, lint/format checks,
strict production typing, and both model-output reproduction checks. Four new
tests check occurrence omissions/duplication, modified source bytes and missing
bodies, vote-date substitution/premature selection, and the distinction between
an empty attachment and explicit agenda non-submission. These checks validate
the integrity workflow, not substantive eligibility or independent reliability.

## Conclusions and Next Steps

This continuation warrants one complete Ant subject-level screening record,
five provisional release-family links preserving retries and calendar
boundaries, two account-access candidates embedded in technical discussions,
and six explicit report non-submissions. It does not warrant a completed Ant
eligibility census or a causal claim. G1 and the wider programme remain as
accepted; G2/G3 are unassessed and all claim confidence levels remain C1. The
next discriminator is completing ambiguous bodies and project/foundation
source links across the fixed cohort, including the missing account-access
receiver records and historical authority, before sampling or locking item 3.
