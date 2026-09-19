"""Load the operative registration and identify its immutable provenance."""

from __future__ import annotations

import hashlib
import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "research/cases"
REGISTRATION = PACKET / "asf-autonomy-coordination-registration.toml"
ANCHOR = "00d696ed80bd388955f622e0611853165f19508c"
RULES: dict[str, Any] = tomllib.loads(REGISTRATION.read_text())
PROJECTS: tuple[str, ...] = tuple(RULES["project_ids"])
HORIZONS = (60, 90, 180)
DIRECTIONS = ("A_to_C", "C_to_A")
CONDITIONS = (
    "ordered_acts_met",
    "receiver_conduct_met",
    "linked_change_met",
    "discriminating_contrast_met",
)
AGREEMENT_FIELDS: tuple[str, ...] = tuple(RULES["audit_agreement_fields"])
RIVALS = (
    "reciprocal_coupling",
    "uncoupled_own_history",
    "common_shock",
    "A_to_C_only",
    "C_to_A_only",
)
Row = dict[str, str]
Tables = dict[str, list[Row]]


def digest(value: bytes) -> str:
    """Return a lowercase hexadecimal SHA-256 digest."""
    return hashlib.sha256(value).hexdigest()


def canonical(value: object) -> bytes:
    """Serialize machine reports deterministically without float coercion."""
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def provenance() -> dict[str, object]:
    """Identify the anchor, amendments, executable code, and operative files."""
    paths = [
        REGISTRATION,
        *(
            PACKET / RULES[key]
            for key in ("protocol", "codebook", "source_audit", "structural_decision")
        ),
    ]
    paths.extend(sorted(Path(__file__).parent.glob("*.py")))
    paths.append(ROOT / "uv.lock")
    paths.append(PACKET / "asf-autonomy-coordination-tooling.md")
    return {
        "registration_commit": ANCHOR,
        "amendment_ids": RULES["amendment_ids"],
        "implementation_clarification_id": "tooling-audit-supplement-2026-09-16",
        "files": {
            str(path.relative_to(ROOT)): digest(path.read_bytes()) for path in paths
        },
    }
