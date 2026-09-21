# ASF Cohort and Source-Access Audit

- **Date:** 2026-09-21.
- **Status:** Third-cycle item 2, completed for owner review; G1 passes.
- **Authorization:** The owner authorized the next item after accepting and
  merging the executable tooling in PR #16.
- **Registration anchor:** `00d696ed80bd388955f622e0611853165f19508c`.
- **Accepted executable:** `18b13ff18500c33d8812459eda72ad6c11640f1a`.
- **Operative specification:** The two accepted registration amendments and
  `tooling-audit-supplement-2026-09-16`, including the accepted review corrections.
- **Snapshot:** [Access records and reproduction instructions](../data/asf-access-2026-09-21/README.md).

## Result and Scope

The registered access and cohort gate passes for the fixed HTTP Server,
Tomcat, Maven, and Ant cohort. Each development archive has a reviewable index
and a retrieved mailbox export for all 36 primary months. Every indexed
original message ID, including its multiplicity, appears in the corresponding
export. All 36 regular public board-minute records and the additional special
board meeting identified below are retained. This exceeds G1's requirement of
33 months for every channel without substituting projects or periods.

| Channel | Primary months verified | Indexed messages matched to retrieved exports | G1 threshold |
| --- | ---: | ---: | ---: |
| HTTP Server development list | 36/36 | 1,687 | 33/36 |
| Tomcat development list | 36/36 | 25,087 | 33/36 |
| Maven development list | 36/36 | 8,338 | 33/36 |
| Ant development list | 36/36 | 651 | 33/36 |
| Regular board minutes | 36/36 | Not a message count | 33/36 |

The [180-row coverage ledger](../data/asf-access-2026-09-21/coverage.csv)
contains every primary month, with source references and states. The
[verification report](../data/asf-access-2026-09-21/verification.json) contains
all 144 index/export comparisons and the unchanged executable's G1 result.
The 35,763 message occurrences are access counts, not eligible episodes,
independent families, or evidence of any mechanism.

The next gates have not been evaluated. Screening, sampling, outcome coding,
shock assessment, and causal adjudication have not begun. A passing access gate
does not imply sufficient opportunities or public evidence to distinguish
rivals. CM-01, CM-04, CM-12, and CM-13 remain C1.

## Cohort and Dated Authority

The [November 2022 approved minutes](https://www.apache.org/foundation/records/minutes/2022/board_minutes_2022_11_16.txt)
recognize Ant, HTTP Server, and Maven in section 6.C, 6.AB, and 6.AP and their
respective attachments. Each attachment records an existing PMC membership.
The [December 2022 approved minutes](https://www.apache.org/foundation/records/minutes/2022/board_minutes_2022_12_21.txt)
do the same for Tomcat in section 6.BY and Attachment BY. The December special
orders contain no termination or reorganization of these four committees.
These dated board records support eligibility at the 2023-01-01 opening;
the current project index is not used as a historical substitute. The
[cohort ledger](../data/asf-access-2026-09-21/cohort.csv) retains the locators.

The [official bylaws source](https://svn.apache.org/repos/asf/infrastructure/site/trunk/content/foundation/bylaws.mdtext)
has public SVN revision `1887743`, dated 2021-03-16, and records Amendment II
as effective 2021-03-11. Section 6.3 assigns active project management to PMCs
within board direction and permits the board to establish or terminate them.
Sections 5.1 and 6.4 specify board powers and appointments. This dated text
supports the corporate authority framework at the window's opening. It does
not establish how any particular actor exercised authority, a change of
decision rights, or the absence of private intervention in an episode.

Current list documentation establishes discovery routes only. Historical
episode-specific authority, policy versions, and an actor's authorized role
still require their own citations during item 3. No current guide has been
backdated to supply those observations.

## Board Inventory and Additional Records

The [public calendar](https://www.apache.org/foundation/board/calendar.html)
was reconciled with the official minute directories for
[2023](https://www.apache.org/foundation/records/minutes/2023/),
[2024](https://www.apache.org/foundation/records/minutes/2024/), and
[2025](https://www.apache.org/foundation/records/minutes/2025/).
All linked primary-period records were retrieved. Searches within the minute
files for special-meeting references were used to check the inventory, not to
select causal episodes.

| Additional entry | Evidence and disposition |
| --- | --- |
| 2025-08-25 special board meeting | The year directory lists a minute file omitted from the calendar. The dated record identifies a special board meeting and is retained in `special_meetings.csv`. Its executive-session topic is public; the deliberations are not. |
| 2025-08-24 written consent | The calendar links an image describing unanimous board action without a regular meeting, under bylaws section 5.12. Both the exact image and its public SVN revision metadata are retained as an additional corporate record. It is not counted as a second special meeting or an extra covered month. |
| Proposed 2024-09-18 special meeting | The 2024-08-21 minutes, special order 7.D, record the proposal as tabled. Its language concerns a member agenda. It is not evidence of a separately convened board meeting, and no extra board-meeting denominator is invented from the proposal. The ordinary September board record is retained. |

The [25 August minutes](https://www.apache.org/foundation/records/minutes/2025/board_minutes_2025_08_25.txt)
and [24 August consent](https://www.apache.org/foundation/records/minutes/2025/board_minutes_2025_08_24.png)
are separate records. Calendar ordering was not used to infer actual dates or
the existence of meetings. The calendar explicitly warns that special meetings
may be omitted; the directory reconciliation is therefore material to G1.
This verifies publicly listed and announced records, not the nonexistence of
an undisclosed meeting.

For every retained board record, a separate public SVN response matches the
website bytes. Its revision timestamp precedes the 2026-08-31 source cutoff;
the latest is 2026-01-21. `published_at` in this access snapshot records that
public SVN revision timestamp as a conservative known-public-by date for the
retained version, not the first website publication date or the meeting date.
The original response metadata and each alias URL remain in the retrieval
receipts. Baseline minutes are used for cohort context only.

## Development Archive Access and Missingness

The current official list pages identify `dev@httpd.apache.org`,
`dev@tomcat.apache.org`, `dev@maven.apache.org`, and `dev@ant.apache.org`:
[HTTP Server](https://httpd.apache.org/lists.html),
[Tomcat](https://tomcat.apache.org/lists.html),
[Maven](https://maven.apache.org/mailing-lists.html), and
[Ant](https://ant.apache.org/mail.html).
Legacy `mod_mbox` routes redirect to the corresponding public Pony Mail lists.
The Tomcat raw-mail link on its current page is malformed; the corrected
public path also redirects. The returned JSON identifies each list and the
requested month, providing a check against silently following a wrong alias.

The public interface's own JavaScript identifies its monthly `stats.lua` and
`mbox.lua` endpoints. Each of the 144 month requests used the exact documented
list/domain and a `YYYY-MM` date. No keyword or outcome filter was applied.
Every index's `hits` equals its returned message count; every mailbox's
original Message-ID multiset equals that index's multiset. There were no
missing IDs, extra IDs, failed final monthly requests, or unreviewable months.
G1 therefore has evidence of retrieval for every indexed message, rather than
a spot check of one convenient thread. Endpoint counts do not independently
prove that the archive preserved every message ever sent to the list.

Some discovery paths failed: the browser reader could not open the Pony Mail
application, returned a 403 for an old Maven archive route, and failed on the
calendar's consent image. Ordinary direct public requests retrieved these
resources. The legacy `static.lua` route returned 404; ViewVC history pages
returned 401. Public SVN and the application's ordinary public endpoints
provided the required records without authentication. Those unsuccessful
discovery responses are retained, not counted as missing primary months.
There was no private access, account use, external contact, or personal-data
enrichment.

Public minute completeness is not completeness of private deliberations.
Confidential sections, private correspondence, absent off-list replies, and
unavailable referenced evidence can still make an episode unclassifiable.
The special meeting's public record is sufficient to inventory that meeting,
not to reconstruct its executive session. Item 3 must retain such missingness
and cannot turn public silence into zero effects. Baseline and follow-up
development archives outside the 36 primary months are not claimed complete
by this inventory; any required episode context and horizon closure remain
part of the first pass.

## Exposure and Reproducibility

The [design-stage exposure disclosure](asf-autonomy-coordination-source-audit.md)
remains part of the record. New exposure began on 2026-09-21, after the
executable freeze and separate item-2 authorization. The calendar exposed
resolution summaries, including selected-project chair or membership changes.
Inspection of cohort attachments exposed nearby routine status and release
text, including an HTTP Server infrastructure-migration reference. Inventory
checks exposed the additional board actions and the tabled proposal above.
A diagnostic view of January 2023 Ant index metadata exposed an Ant release
vote subject, a body preview, and thread structure. These observations have
not been selected or coded as mechanism witnesses.

All primary-period index and mailbox bytes were downloaded to establish
access, including message bodies carried by the exports and previews carried
by indices. Automated verification inspected counts and original ID headers;
it did not semantically screen those bodies. The board files were inspected
for identity, cohort context, and special-meeting references, not subjected
to the required project/officer-report census. This is not complete outcome
blindness or a completed first pass. Preserve this disclosure during later
coding and the eventual delayed recode.

The snapshot retains 393 public retrieval receipts, 334 source-ledger objects,
the month and cohort ledgers, and compressed exact archive bytes. Original
response hashes and stored gzip hashes are separate. Identical web/SVN minute
copies share a physical artifact while preserving both retrieval records.
Compression changes storage only; no message or attachment has been removed.
The approximately 86 MB bundle is retained in Git so review and reproduction
do not require repeating live archive requests.

The offline verifier checks saved and decompressed source hashes, all monthly
message-ID multisets, the fixed month grid, ledger hashes, and the accepted
executable/protocol bytes before applying the existing G1 calculator. It does
not alter the frozen package or create new gate thresholds. Downstream CSVs
are header-only because they have not been started. Their emptiness is not an
attestation that no eligible episodes or shocks exist. No first-pass lock,
recode bundle, washout start, G2/G3 result, or all-horizon claim decision exists.

Verification on 2026-09-21 passes the complete offline snapshot check with no
integrity errors. `just check` passes all 193 repository tests with 90.59%
combined branch/statement coverage, Ruff lint and formatting, strict mypy,
and byte-for-byte reproduction of both model artifact sets. Changed local
documentation links also resolve. These checks establish reproducibility and
software consistency, not semantic correctness of future episode coding.

## Conclusions and Next Steps

The fixed cohort and retrieved public records meet G1 on this dated audit.
This removes the initial access obstacle and warrants proceeding, after item
review, to complete subject-index screening and the registered first pass.
It does not warrant a reciprocal, one-way, null, or nested authority-effect
finding. All claims remain C1, including CM-04's existing structural narrowing;
the wider programme gains an auditable access map rather than causal support.

The next discriminating action is item 3: screen the complete indices, retain
all cross-boundary and ambiguous families, select the deterministic routine
baseline, collect required context and follow-up, and assess opportunity
identifiability. Preserve the original access snapshot and all new exposure.
Only a completed first pass can be locked and begin the 14-complete-day
washout. This item ends with its separate PR for owner review.
