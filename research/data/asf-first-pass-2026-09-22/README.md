# ASF First-Pass Working Checkpoint — 2026-09-22

**Incomplete evidence work.** This directory is a resumable preparation and
review checkpoint for third-cycle item 3. It is not a completed dataset for
`scripts.asf_audit`, a sample, an audit-frame lock, or a gate decision. The
[first-pass note](../../cases/asf-autonomy-coordination-first-pass.md) states
the substantive observations and remaining work.

## Provenance and Scope

The accepted input is
[the item 2 access snapshot](../asf-access-2026-09-21/), commit
`b2f8bfa1173199f2141a187c2a9ba768225711b7`. Original registration
`00d696ed80bd388955f622e0611853165f19508c`, both dated amendments, and executable
freeze `18b13ff18500c33d8812459eda72ad6c11640f1a` remain operative. The new
preparation scripts do not alter the frozen code or adjudication rules.

| File | Meaning |
| --- | --- |
| `message-index.csv` | All 35,763 primary-window index occurrences, including repeated deliveries. Original Message-ID is the source identifier; archive ID locates an occurrence. |
| `subject-review.csv` | 6,015 navigation groups from messages routed for subject review; 21 groups have had their indexed message bodies read. All other groups remain pending. |
| `duplicate-variants.csv` | Every exported version of repeated project/Message-ID pairs, with exact byte locators and hashes. No version has been silently selected or discarded. |
| `reviewed-messages.csv` | Exact local export blocks for the 89 Ant messages read in the 21 groups, plus date headers, hashes, and public locators. |
| `reviewed-board-sections.csv` | 17 Ant attachment sections and one chair-change resolution read; these are bounded section reviews, not whole-minute completion. |
| `retrievals.json` | New referenced-source access attempts, status chains, response hashes, and selected provenance headers. Login HTML is not ticket evidence. |
| `sources/ant-processes-r1826197.xml` | Small official, licensed rule source at an immutable 2018 SVN revision. New correspondence bodies and login responses remain local only. |
| `checkpoint.json` | Descriptive scope and hashes for this mutable work checkpoint. This is not the registered first-pass lock. |
| `verification.json` | Recomputed metadata integrity and progress counts; no causal or claim calculations. |

`index_timestamp` comes from the current archive index. It is not a substituted
event date or independently certified historical publication date. Review the
original message header and content, then enter event intervals and publication
eligibility separately in the eventual frozen-schema dataset.

`topic_id` hashes the project and normalized subject for navigation. It is
**not** a thread, episode, or issue-family identifier. Only repeated leading
`Re:`, `Fw:`, and `Fwd:` prefixes are stripped. Result/cancellation and external
prefixes remain distinct; identical titles may span years. Thread references,
body content, and independently requested deliverables control later family
assignment. All original IDs, including angle brackets, remain unchanged for
the registered sampling key.

The `preliminary_route` field is a mechanical suggestion, not an exclusion or
completed screening decision. It identifies some original notification titles;
human replies ordinarily remain in the subject-review queue. Neither the
notification routes nor the remaining subject groups have been certified as
completely screened. The temporary local refinements used to navigate titles
are not final screening data. There are no opportunity or witness labels here.

`body_reviewed_followup_pending` means the complete plain-text bodies of the
indexed messages in that navigation group were read. It does not assert that
all references, attachments, cross-posts, changed titles, relevant authority,
or horizon follow-ups have been collected. `classification` and `reason` are
provisional review notes, including false positives; they are not the frozen
codebook's final eligibility or causal fields.

An export block is numbered from 1 after splitting the accepted decompressed
mbox on its `From ` envelope separators. Its `raw_sha256` includes original
message headers and MIME content but excludes the envelope separator. The
plain-body hash covers Python's decoded plain-text part encoded as UTF-8; equal
plain-body hashes do not certify equality of headers or other MIME parts.
The original accepted gzip files and receipts supply the enclosing retrieval
provenance. Repeated Message-IDs require explicit source-version treatment
before populating a one-source-per-ID ledger.

## Reproduction

From the repository root, verify the accepted input first:

```bash
uv run --locked python -c "import runpy; runpy.run_path('research/data/asf-access-2026-09-21/verify.py', run_name='__main__')"
```

Use a new, nonexistent output directory to regenerate the descriptive queues:

```bash
uv run --locked python research/data/asf-first-pass-2026-09-22/rebuild.py \
  --output-dir /tmp/asf-review-rebuild
```

This emits the message index, duplicate-version inventory, and a **blank**
subject-review queue. It refuses to overwrite an existing directory. It does
not reconstruct the researcher's notes or retrieve any network sources.

Verify retained working notes against those inputs without changing them:

```bash
uv run --locked python research/data/asf-first-pass-2026-09-22/verify.py
```

The verifier checks checkpoint file hashes, complete occurrence membership,
duplicate versions, unchanged navigation fields, exact reviewed-message
membership/bytes, and bounded board locators. A successful result cannot
establish the truth or completeness of a researcher's interpretation. The
accepted snapshot verifier separately checks the input's enclosing hashes.
The ignored `.local/asf-first-pass-2026-09-22/` directory contains working
decoded bodies and response bytes; it is not a publishable source bundle.

## Conclusions and Next Steps

This checkpoint makes the beginning of item 3 reproducible and preserves
observed reversals, failed source access, source variants, and unfinished work.
It supplies no completed census, G2/G3 decision, or confidence increase. Finish
the full subject and board/officer review, resolve families and source gaps,
then perform the registered sampling, coding, shock/rival checks, and lock.
