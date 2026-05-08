from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

from .anchors import RootAnchor, capture_anchor
from .envelope import RunEnvelope
from .manifest import discover_expected_artifacts, hash_artifacts, output_root_hash_surface


FULL_ROOTMIRROR_DOWNGRADE = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
PASS_EPSILON = 1e-9


def clamp01(x: float) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def is_full_score(x: float) -> bool:
    return abs(float(x) - 1.0) <= PASS_EPSILON


@dataclass
class RootMirrorFullResult:
    schema: str
    version: str
    run_id: str
    instrument: str
    status: str
    continuity_integrity_score: float
    run_envelope: Dict[str, Any]
    pre_anchor: Dict[str, Any]
    post_anchor: Dict[str, Any]
    checks: Dict[str, Any]
    artifacts: Dict[str, str]
    hashes: Dict[str, str]
    replay_metadata: Dict[str, Any]
    downgrade_removed: List[str]
    remaining_downgrade_reason: List[str]
    non_claim_locks: Dict[str, bool]


def continuity_score(checks: Dict[str, Any]) -> float:
    raw = (
        0.15 * float(bool(checks.get("run_envelope_declared", False)))
        + 0.15 * float(bool(checks.get("return_to_root", False)))
        + 0.15 * float(bool(checks.get("ledger_append_valid", False)))
        + 0.20 * float(bool(checks.get("artifact_manifest_closure", False)))
        + 0.15 * float(bool(checks.get("state_hash_present", False)))
        + 0.10 * float(bool(checks.get("replay_metadata_present", False)))
        + 0.10 * float(bool(checks.get("non_claim_locks_preserved", False)))
    )

    score = clamp01(raw)

    # Avoid treating mathematically complete verification as incomplete because
    # binary floating point may yield 0.9999999999999999 instead of 1.0.
    if is_full_score(score):
        return 1.0

    return score


def verify_rootmirror_full(
    repo_root: Path,
    output_root: Path,
    run_id: str,
    instrument: str,
    command: str,
    pre_anchor: RootAnchor,
    expected_artifacts: list[str] | None = None,
    ledger_append_expected: int = 1,
) -> RootMirrorFullResult:
    repo_root = repo_root.resolve()
    output_root = output_root.resolve()
    expected = expected_artifacts or ["state", "ledger", "evidence", "report", "semantic"]

    ledger_path = output_root / "ledger" / "cik_ledger.jsonl"
    post_anchor = capture_anchor(repo_root, ledger_path)

    artifacts = discover_expected_artifacts(output_root, run_id)
    hashes = hash_artifacts(artifacts)

    artifact_manifest_closure = all(
        key in artifacts and key in hashes
        for key in expected
    )

    ledger_delta = post_anchor.ledger_height - pre_anchor.ledger_height

    replay_metadata = {
        "command": command,
        "repo_root": str(repo_root),
        "output_root": str(output_root),
        "run_id": run_id,
        "instrument": instrument,
        "pre_anchor_timestamp": pre_anchor.timestamp,
        "post_anchor_timestamp": post_anchor.timestamp,
        "git_head": post_anchor.git_head,
        "pythonpath": post_anchor.pythonpath,
    }

    checks = {
        "run_envelope_declared": True,
        "return_to_root": Path.cwd().resolve() == repo_root,
        "ledger_append_delta": ledger_delta,
        "ledger_append_expected": ledger_append_expected,
        "ledger_append_valid": ledger_delta == ledger_append_expected,
        "artifact_manifest_closure": artifact_manifest_closure,
        "state_hash_present": "state" in hashes,
        "output_root_hash_surface_present": True,
        "replay_metadata_present": True,
        "tesseract_lite_cross_link_present": "tesseract" in artifacts,
        "non_claim_locks_preserved": True,
    }

    hashes["output_root_hash_surface"] = output_root_hash_surface(output_root)

    score = continuity_score(checks)
    full_pass = is_full_score(score)
    status = "pass" if full_pass else "warning"

    downgrade_removed: List[str] = []
    remaining: List[str] = []

    if full_pass:
        downgrade_removed.append(FULL_ROOTMIRROR_DOWNGRADE)
    else:
        remaining.append("Full RootMirror verification incomplete.")

    envelope = RunEnvelope(
        run_id=run_id,
        instrument=instrument,
        repo_root=str(repo_root),
        output_root=str(output_root),
        command=command,
        expected_artifacts=expected,
        declared=True,
        ledger_append_expected=ledger_append_expected,
    )

    return RootMirrorFullResult(
        schema="CIK-v0.5-rootmirror-full",
        version="0.5",
        run_id=run_id,
        instrument=instrument,
        status=status,
        continuity_integrity_score=score,
        run_envelope=asdict(envelope),
        pre_anchor=asdict(pre_anchor),
        post_anchor=asdict(post_anchor),
        checks=checks,
        artifacts=artifacts,
        hashes=hashes,
        replay_metadata=replay_metadata,
        downgrade_removed=downgrade_removed,
        remaining_downgrade_reason=remaining,
        non_claim_locks={
            "rootmirror_full_is_not_code_correctness": True,
            "continuity_is_not_truth": True,
            "artifact_closure_is_not_validation": True,
            "ledger_append_is_not_semantic_truth": True,
            "hash_presence_is_not_correctness": True,
            "replay_metadata_is_not_provenance_proof": True,
            "cifscore_is_not_truth": True,
        },
    )