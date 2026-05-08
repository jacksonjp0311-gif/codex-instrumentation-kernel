from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import json


ROOTMIRROR_FULL_EVIDENCE_SCHEMA = "CIK-v0.5-rootmirror-full-evidence"
ROOTMIRROR_FULL_CLAIM_BOUNDARY = "continuity_verification_only"


def load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_rootmirror_full_evidence(output_root: Path, run_id: Optional[str] = None) -> Optional[Path]:
    evidence_dir = Path(output_root) / "evidence"
    if not evidence_dir.exists():
        return None

    candidates = sorted(evidence_dir.glob("*_rootmirror_full_evidence_package.json"))

    if run_id:
        candidates = [p for p in candidates if run_id in p.name]

    if not candidates:
        return None

    return candidates[-1]


def consume_rootmirror_full_evidence(output_root: Path, run_id: Optional[str] = None) -> Dict[str, Any]:
    """Convert RootMirror Full sidecar evidence into a bounded core scoring signal.

    This consumer accepts evidence only when:
    - schema is CIK-v0.5-rootmirror-full-evidence
    - status is pass
    - continuity_integrity_score is effectively 1.0
    - claim_boundary is continuity_verification_only

    The returned score is instrumentation compliance only, not correctness.
    """
    path = find_rootmirror_full_evidence(output_root, run_id=run_id)

    if path is None:
        return {
            "available": False,
            "score": 0.0,
            "status": "missing",
            "path": None,
            "reason": "RootMirror Full evidence package missing.",
            "non_claim_lock": "RootMirror Full evidence is continuity evidence, not correctness proof.",
        }

    payload = load_json(path)

    if not payload:
        return {
            "available": False,
            "score": 0.0,
            "status": "invalid",
            "path": str(path),
            "reason": "RootMirror Full evidence package unreadable.",
            "non_claim_lock": "Unreadable evidence cannot support scoring.",
        }

    schema = payload.get("schema")
    status = payload.get("status")
    claim_boundary = payload.get("claim_boundary")
    continuity_score = float(payload.get("continuity_integrity_score", 0.0))

    passed = (
        schema == ROOTMIRROR_FULL_EVIDENCE_SCHEMA
        and status == "pass"
        and abs(continuity_score - 1.0) <= 1e-9
        and claim_boundary == ROOTMIRROR_FULL_CLAIM_BOUNDARY
    )

    if passed:
        return {
            "available": True,
            "score": 1.0,
            "status": "pass",
            "path": str(path),
            "payload": payload,
            "reason": "RootMirror Full evidence consumed.",
            "non_claim_lock": "RootMirror Full verifies continuity only, not correctness.",
        }

    return {
        "available": True,
        "score": 0.0,
        "status": "warning",
        "path": str(path),
        "payload": payload,
        "reason": "RootMirror Full evidence did not pass all gates.",
        "gates": {
            "schema_ok": schema == ROOTMIRROR_FULL_EVIDENCE_SCHEMA,
            "status_ok": status == "pass",
            "score_ok": abs(continuity_score - 1.0) <= 1e-9,
            "claim_boundary_ok": claim_boundary == ROOTMIRROR_FULL_CLAIM_BOUNDARY,
        },
        "non_claim_lock": "Failed continuity evidence cannot remove downgrade.",
    }