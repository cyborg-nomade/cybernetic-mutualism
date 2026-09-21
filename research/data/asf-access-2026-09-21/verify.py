"""Verify this access snapshot offline against the accepted ASF audit code."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
from collections import Counter
from email.parser import BytesHeaderParser
from pathlib import Path

from scripts.asf_audit.analysis import access_gate
from scripts.asf_audit.schema import load_tables, structural_errors
from scripts.asf_audit.validation import reference_errors, source_errors

ROOT = Path(__file__).resolve().parent


def sha256(data: bytes) -> str:
    """Identify exact saved or decompressed source bytes."""
    return hashlib.sha256(data).hexdigest()


def verify_receipts() -> int:
    """Verify every retained response, including failed discovery routes."""
    receipts = sorted((ROOT / "retrievals").glob("*.json"))
    for path in receipts:
        receipt = json.loads(path.read_text())
        content = (ROOT / receipt["file"]).read_bytes()
        assert sha256(content) == receipt["sha256"], path
        assert len(content) == receipt["bytes"], path
        if receipt["file"].endswith(".gz"):
            raw = gzip.decompress(content)
            assert sha256(raw) == receipt["raw_sha256"], path
            assert len(raw) == receipt["raw_bytes"], path
    return len(receipts)


def mailbox_ids(raw: bytes) -> Counter[str]:
    """Read only original message-ID headers, without interpreting message bodies."""
    blocks = re.split(rb"(?m)^From [^\n]*\n", raw)[1:]
    ids = []
    for block in blocks:
        header = block.split(b"\n\n", 1)[0] + b"\n\n"
        parsed = BytesHeaderParser().parsebytes(header)
        ids.append(str(parsed.get("Message-ID", "")).strip())
    assert all(ids), "Export contains a message without an original Message-ID"
    return Counter(ids)


def verify_month(path: Path) -> dict[str, object]:
    """Compare the complete public index with the complete retrieved mailbox."""
    index = json.loads(gzip.decompress(path.read_bytes()))
    prefix = path.name.removesuffix("-index.json.gz")
    project, month = prefix.split("-", 1)
    export = ROOT / "sources" / f"{prefix}.mbox.gz"
    actual = mailbox_ids(gzip.decompress(export.read_bytes()))
    expected = Counter(row["message-id"].strip() for row in index["emails"])
    assert index["list"] == f"dev@{project}.apache.org", path
    assert index["searchParams"]["d"] == month, path
    assert len(index["emails"]) == index["hits"], path
    assert actual == expected, (path, expected - actual, actual - expected)
    return {
        "project": project,
        "month": month,
        "indexed_messages": index["hits"],
        "exported_messages": sum(actual.values()),
        "unique_message_ids": len(actual),
        "message_id_multisets_match": True,
    }


def verify_dataset() -> dict[str, object]:
    """Apply the frozen structural, source, reference, and G1 checks only."""
    tables = load_tables(ROOT)
    errors = structural_errors(tables) + reference_errors(tables)
    for row in tables["sources"]:
        errors.extend(
            f"{row['source_id']}: {error}" for error in source_errors(row, ROOT)
        )
    assert not errors, errors
    return access_gate(tables)


def verify_versions() -> None:
    """Bind the calculation to accepted executable bytes and retained ledger hashes."""
    snapshot = json.loads((ROOT / "snapshot.json").read_text())
    repository = ROOT.parents[2]
    for name, digest in snapshot["operative_files"].items():
        assert sha256((repository / name).read_bytes()) == digest, name
    for name, digest in snapshot["ledger_hashes"].items():
        assert sha256((ROOT / name).read_bytes()) == digest, name


def report() -> dict[str, object]:
    """Return deterministic access verification without calculating later gates."""
    verify_versions()
    receipts = verify_receipts()
    rows = [
        verify_month(path)
        for path in sorted((ROOT / "sources").glob("*-index.json.gz"))
    ]
    expected = {
        (p, f"{y}-{m:02d}")
        for p in ("httpd", "tomcat", "maven", "ant")
        for y in (2023, 2024, 2025)
        for m in range(1, 13)
    }
    assert {(row["project"], row["month"]) for row in rows} == expected
    gate = verify_dataset()
    return {
        "registration_commit": "00d696ed80bd388955f622e0611853165f19508c",
        "executable_commit": "18b13ff18500c33d8812459eda72ad6c11640f1a",
        "scope": "G1 access only; not screening, G2, G3, or a first-pass lock",
        "retrieval_receipts_verified": receipts,
        "integrity_errors": [],
        "G1": gate,
        "monthly_message_checks": rows,
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
