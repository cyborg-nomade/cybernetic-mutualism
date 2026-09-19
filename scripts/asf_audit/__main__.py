"""Run the offline ASF ledger, lock, recode, and decision workflow."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from scripts.asf_audit.analysis import access_gate
from scripts.asf_audit.freeze import begin_recode, freeze_first_pass, submit_recode
from scripts.asf_audit.protocol import canonical
from scripts.asf_audit.report import audited_report
from scripts.asf_audit.sampling import audit_frame, local_baseline
from scripts.asf_audit.schema import initialize, load_tables
from scripts.asf_audit.validation import integrity_errors


def parser() -> argparse.ArgumentParser:
    """Describe commands and require explicit lock/score digests at boundaries."""
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    for name in (
        "init",
        "sample",
        "validate",
        "access",
        "lock",
        "start-recode",
        "submit-recode",
        "adjudicate",
    ):
        command = commands.add_parser(name)
        command.add_argument("directory", type=Path)
        if name == "lock":
            command.add_argument("--output", type=Path, required=True)
        if name in ("start-recode", "submit-recode", "adjudicate"):
            command.add_argument("--lock-hash", required=True)
        if name == "start-recode":
            command.add_argument("--no-asf-evidence-work", action="store_true")
        if name == "submit-recode":
            command.add_argument("--recode", type=Path, required=True)
        if name == "adjudicate":
            command.add_argument("--score-hash", required=True)
    return result


def dispatch(args: argparse.Namespace) -> object:
    """Execute a command without network requests or implicit file updates."""
    now = datetime.now(UTC)
    if args.command == "init":
        initialize(args.directory)
        return {"created": str(args.directory), "evidence_records": 0}
    if args.command == "lock":
        return freeze_first_pass(args.directory, args.output, now)
    if args.command == "start-recode":
        begin_recode(args.directory, args.lock_hash, now, args.no_asf_evidence_work)
        return {"recode_started": True}
    if args.command == "submit-recode":
        return submit_recode(args.directory, args.recode, args.lock_hash, now)
    if args.command == "adjudicate":
        return audited_report(args.directory, args.lock_hash, args.score_hash)
    return inspect_tables(args)


def inspect_tables(args: argparse.Namespace) -> object:
    """Expose sampling/access checks without premature aggregate claim decisions."""
    tables = load_tables(args.directory)
    if args.command == "sample":
        return {
            "local_baseline": local_baseline(tables),
            "audit_frame": audit_frame(tables),
        }
    if args.command == "access":
        return {"G1": access_gate(tables), "claim_confidence_changed": False}
    errors = integrity_errors(tables, args.directory)
    return {"integrity_pass": not errors, "errors": errors}


def main() -> int:
    """Print a machine-readable report; malformed inputs return nonzero status."""
    args = parser().parse_args()
    try:
        report = dispatch(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print(canonical({"error": str(error)}).decode(), end="")
        return 2
    print(canonical(report).decode(), end="")
    if isinstance(report, dict) and (
        report.get("integrity_pass") is False or report.get("integrity_errors")
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
