# ASF Release Frame and Registered Baseline Draw

This evidence record continues item 3 in PR #19. It supplies the release
sampling frame and draw, not a completed first pass, causal result, audit lock,
or washout start. It follows the accepted executable freeze
`18b13ff18500c33d8812459eda72ad6c11640f1a`. No registered executable changed.
The preceding October screening records remain dated snapshots.

## Frame and Selection

The complete inspected primary subject index yields 724 original vote-title
candidates: Ant 10, HTTP Server 20, Maven 515, and Tomcat 179. Original bodies
distinguish 698 formal release-opening messages from governance proposals and
result messages under unchanged vote subjects. Exact duplicates, corrected
ballots and retries do not create independent families. The resulting frame
contains 647 release families: Ant 5, HTTP Server 12, Maven 475, and Tomcat 155.

The unchanged registered sampler logs all 48 project-quarter strata and
selects one family in each of 36 nonempty strata. Twelve empty strata remain
empty. `local-baseline.csv` retains every ordered source ID, family ID and
SHA-256 key, including joint-ballot ties resolved by the frozen family-ID rule.
No outcome-based replacement is permitted. These are event-date strata;
original message dates do not establish historical public availability.
Publication and historical-authority checks remain separate required work.

`opening-candidates.json` preserves literal original IDs, original headers,
archive locators and every original raw/body variant hash.
`opening-review.json` records each independent eligibility judgment and its
reading scope. `release-family-frame.csv` contains one first formal opening
per independent deliverable. `opening-family-associations.csv` preserves all
opening/retry associations. Joint ballots split independently releasable
components, including the eleven Maven 4 component/plugin candidates in one
June 2024 message; they retain the same original source ID.

## Identity Checks and Limits

The opening review used complete original prose with exact-repeat reference
ledgers. A second Maven aid omitted only standalone opaque digests, artifact
filenames and URLs, with every omission inventoried. Ambiguous artifact
locators were checked against their originals. No source bytes were changed.
The full closure aid comprised 806 original candidates and 3,142 lines; a
bounded supplement supplied 40 more messages and 404 lines. Thirteen
reply/nonstandard opening candidates were independently checked: copied
ballots, votes and comments do not reopen a release. One same-author correction
republished Resource Bundles 1.6 hyperlinks without opening a new decision.

`identity-review.json` links opening ordinals to closure ordinals and retains
reasons for merging or separating candidates. `closure-candidates.json`,
`closure-supplement.json` and `opening-exceptions.json` identify the underlying
originals and byte hashes. Ordinals are navigation within these files; they
are not episode or source IDs. Complete raw evidence remains in the accepted
monthly exports. This directory republishes metadata, not correspondence.

Relevant distinctions include:

- Surefire 3.2.4's retries culminate in 3.2.5 after the quarter boundary;
  Resolver 2.0.12's retry becomes 2.0.13 in the next quarter. Each family keeps
  its first actual opening.
- Maven alpha-10 passed in a reply without a result tag. A reference to
  scrubbed Resolver alpha-9 supplies no observed formal alpha-9 opening.
- Tomcat's October 2023 expedited releases passed before their corrective
  successors. Tomcat 10.1.45 was promoted and announced with a warning after
  a tally correction; its successor is not silently folded into a cancellation.
- Tomcat 9.0.77 was marked not released before the same-day 9.0.78 ballot;
  the release manager explicitly dropped 9.0.103 before its 9.0.104 reroll.
- Maven Archiver beta-3's approved ballot and later report that it was never
  published are both retained. Approval does not prove publication.

Two interpretive family boundaries remain explicit. Tomcat M2 closed for
insufficient quorum in January; February's M3 has a new milestone/tag and no
explicit reopening, so it remains separate despite a repeated notable-change
template. Sitetools M17 was canceled over anchor generation; M18 delivers that
unfinished feature with parser controls and further fixes, without an
intervening approved release, so it remains the same family. The delayed
replacement lacks direct respin wording. These decisions were made before
baseline measurements or causal labels. They are reviewable interpretations,
not mechanically discovered facts.

Reading identities and closures necessarily exposed some outcomes. Selection
still uses only the registered original-ID hash and disclosed family identity
decisions. The draw receipt is not a registered first-pass lock. It does not
start the 14-day washout or substitute for the complete audit/recode bundle.

## Verification

From the repository root, run
`python3 research/data/asf-release-frame-2026-10-20/verify.py`.
It re-extracts opening variants from accepted export bytes, checks original-ID
membership, family associations and earliest opening dates, verifies retained
file hashes, and reproduces the draw with the frozen sampler. It does not
automatically affirm the research judgments or any registered gate.

## Conclusions and Next Steps

The reviewed release frame now warrants a reproducible, bounded local
baseline of 36 selected families. It removes a sampling prerequisite without
changing any programme claim or completing item 3. Historical publication and
authority verification, selected-family evidence, component measurements,
shock/rival/contrast records and the registered first-pass lock remain. The
next discriminating action is to complete those records for the fixed draw
and the cross-boundary census, then generate the audit frame and blank recode
bundle together at the actual first-pass lock.
