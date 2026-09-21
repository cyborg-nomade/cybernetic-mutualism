# ASF Access Snapshot — 2026-09-21

This is the evidence bundle for the [item 2 access audit](../../cases/asf-autonomy-coordination-access-audit.md).
G1 passes; no later gate or causal decision has been calculated.

| Artifact | Meaning |
| --- | --- |
| `coverage.csv` | 144 project-development months and 36 foundation-board months |
| `cohort.csv` | Four historically supported opening-date PMC classifications |
| `special_meetings.csv` | The additional 2025-08-25 board meeting |
| `sources.csv` | 334 source objects, locators, dates, authority scope, and stored hashes |
| `retrievals/` | 393 independent public request receipts, including failures and redirects |
| `sources/` | Retained response bytes; indices and mailbox exports compressed without alteration |
| `schema.json` | Exact accepted CSV schemas; downstream ledgers remain header-only |
| `snapshot.json` | Registration, accepted executable, operative-file hashes, and ledger hashes |
| `verification.json` | G1 and every monthly index/export comparison |
| `verify.py` | Offline checks for this snapshot, using the existing G1 calculator |

Run from the repository root, with the locked environment:

```bash
uv run --locked python -c "import runpy; runpy.run_path('research/data/asf-access-2026-09-21/verify.py', run_name='__main__')" > /tmp/asf-access-verification.json
diff -u research/data/asf-access-2026-09-21/verification.json /tmp/asf-access-verification.json
```

The verifier refuses changed operative code/protocol files or input ledgers.
Use the accepted snapshot commit to reproduce it after later programme changes.
It does not run the first-pass validator, which correctly requires screening
and coding attestations that do not yet exist. It performs the frozen structural,
foreign-reference, source-hash, and G1 checks applicable to this stage.

Each receipt records the original URL, final URL, retrieval timestamp, status,
content type, byte length, and SHA-256. Later retrieval batches also preserve
HTTP response headers. Compressed artifacts additionally retain the raw response
length and SHA-256. Gzip uses a zero modification timestamp for deterministic
storage. The downloaded third-party records retain their own notices and
attribution; these are research source copies, not newly authored project prose.

Collection used ordinary public GET requests through curl, following redirects,
with at most three concurrent requests per batch. Monthly indices used
`https://lists.apache.org/api/stats.lua?list=dev&domain=PROJECT.apache.org&d=YYYY-MM`;
mailbox exports used the same parameters at `api/mbox.lua`. These routes came
from the public interface's retained `ponymail.js`. The exact requests,
including the documented legacy paths, are in the receipts. The full calendar
and year directories determined the board record list. All sources were
retrieved on 2026-09-21; board events, public SVN revision timestamps, and
retrieval timestamps remain distinct.

`published_at` for minute and bylaws sources records the retained version's
public SVN revision date, a conservative known-public-by bound, not a guessed
first website publication date. Current archive indices and bulk mailboxes
have unknown analytical publication eligibility: they establish access only.
Individual messages still require their own provenance and eligibility checks
when selected for evidence. A month export is a storage object, not a family.

The empty downstream ledgers mean **not started**, not zero observations.
The `special_meeting_calendar_complete` attestation includes reconciliation
against all three official year directories. The 24 August written consent
is retained in `sources.csv` but is not a meeting. No empirical lock, audit
frame, or recode bundle was created. The washout clock has not started.

## Conclusions and Next Steps

This snapshot supports a dated G1 pass and reproducible access checks. It changes
the programme's access assessment while leaving every causal claim at C1.
The next discriminating work is the complete item 3 screening and first pass,
with episode-level missingness retained despite the aggregate access pass.
