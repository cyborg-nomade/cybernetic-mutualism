"""Reconstruct exact finalized ASF first-pass bytes without recoding evidence.

This package verifier checks storage, transport/source hashes and frozen bundle
reconstruction. It does not compute aggregate gates, agreement or claim results.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path

PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]


def digest(data: bytes) -> str:
    """Return the exact byte digest."""
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    """Read an object without treating its contents as instructions."""
    return json.loads(path.read_text())


def beneath(root: Path, relative: str) -> Path:
    """Refuse traversal and symbolic links in reconstruction paths."""
    result = root / relative
    if result.is_symlink() or not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Unsafe package path: {relative}")
    return result


def storage_bytes(storage: dict, cache: dict) -> bytes:
    """Read existing original bytes, exact mailbox blocks or packaged gzip."""
    kind, relative = storage["kind"], storage["path"]
    root = PACKAGE if kind == "packaged_gzip" else REPOSITORY
    path = beneath(root, relative)
    if kind == "mailbox_block":
        if relative not in cache:
            cache[relative] = re.split(
                rb"(?m)^From [^\n]*\n", gzip.decompress(path.read_bytes())
            )[1:]
        return cache[relative][storage["block"] - 1]
    if kind in ("packaged_gzip", "repository_gzip"):
        return gzip.decompress(path.read_bytes())
    if kind == "repository":
        return path.read_bytes()
    raise ValueError(f"Unknown storage type: {kind}")


def check_hashes(root: Path, expected: dict) -> None:
    """Check every declared artifact before reconstructing it."""
    for relative, expected_hash in expected.items():
        if digest(beneath(root, relative).read_bytes()) != expected_hash:
            raise ValueError(f"Artifact changed: {relative}")


def materialize(target: Path) -> dict:
    """Restore native CSV/source bytes into a new directory, without mutation."""
    target.mkdir(parents=True, exist_ok=False)
    restored = {}
    for path in sorted((PACKAGE / "ledgers").glob("*.csv.gz")):
        name = path.name.removesuffix(".gz")
        raw = gzip.decompress(path.read_bytes())
        (target / name).write_bytes(raw)
        restored[name] = digest(raw)
    cache: dict = {}
    for relative, record in read_json(PACKAGE / "source-catalog.json").items():
        raw = storage_bytes(record["storage"], cache)
        if digest(raw) != record["sha256"]:
            raise ValueError(f"Original source changed: {relative}")
        output = beneath(target, relative)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(raw)
        restored[relative] = record["sha256"]
    return restored


def verify(target: Path | None) -> dict:
    """Verify the package and optionally reconstruct the complete native set."""
    manifest = read_json(PACKAGE / "manifest.json")
    check_hashes(PACKAGE, manifest["files"])
    check_hashes(REPOSITORY, read_json(PACKAGE / "accepted-inputs.json"))
    receipt = read_json(PACKAGE / "lock-receipt.json")
    lock = read_json(PACKAGE / "lock.json")
    if digest((PACKAGE / "lock.json").read_bytes()) != receipt["lock_sha256"]:
        raise ValueError("Lock differs from externally retained receipt")
    if (
        digest((PACKAGE / "audit-frame.json").read_bytes())
        != receipt["audit_frame_sha256"]
    ):
        raise ValueError("Audit frame differs from lock receipt")
    if target is not None and materialize(target) != lock["first_pass_files"]:
        raise ValueError("Reconstructed first pass differs from simultaneous lock")
    return {
        "package_integrity_pass": True,
        "native_reconstruction_pass": True if target is not None else None,
        "lock_sha256": receipt["lock_sha256"],
        "aggregate_or_claim_calculation": False,
    }


def main() -> None:
    """Check existing package bytes; reconstruction requires a new destination."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materialize", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.materialize), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
