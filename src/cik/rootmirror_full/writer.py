from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Dict
import json

from .verifier import RootMirrorFullResult


def write_rootmirror_full_outputs(result: RootMirrorFullResult, output_root: Path) -> Dict[str, str]:
    output_root = output_root.resolve()
    root = output_root / "rootmirror_full"
    evidence_root = output_root / "evidence"

    root.mkdir(parents=True, exist_ok=True)
    evidence_root.mkdir(parents=True, exist_ok=True)

    json_path = root / f"{result.run_id}_rootmirror_full.json"
    md_path = root / f"{result.run_id}_rootmirror_full.md"
    evidence_path = evidence_root / f"{result.run_id}_rootmirror_full_evidence_package.json"

    payload = asdict(result)
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md_lines = [
        "# RootMirror Full Verification",
        "",
        f"Run ID: {result.run_id}",
        f"Instrument: {result.instrument}",
        f"Status: {result.status}",
        f"Continuity integrity score: {result.continuity_integrity_score}",
        "",
        "## Checks",
        "",
    ]

    for key, value in result.checks.items():
        md_lines.append(f"- {key}: {value}")

    md_lines.extend(["", "## Artifacts", ""])

    for key, value in result.artifacts.items():
        md_lines.append(f"- {key}: `{value}`")

    md_lines.extend(["", "## Downgrade Removed", ""])

    if result.downgrade_removed:
        for item in result.downgrade_removed:
            md_lines.append(f"- {item}")
    else:
        md_lines.append("- None")

    md_lines.extend(["", "## Remaining Downgrade Reasons", ""])

    if result.remaining_downgrade_reason:
        for item in result.remaining_downgrade_reason:
            md_lines.append(f"- {item}")
    else:
        md_lines.append("- None")

    md_lines.extend([
        "",
        "## Non-claim locks",
        "",
        "- Continuity is not correctness.",
        "- Artifact closure is not validation.",
        "- Ledger append is not semantic truth.",
        "- Hash presence is not correctness.",
        "- Replay metadata is not provenance proof.",
        "- RootMirror full is not a security proof.",
        "",
    ])

    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    evidence = {
        "schema": "CIK-v0.5-rootmirror-full-evidence",
        "run_id": result.run_id,
        "rootmirror_full_json": str(json_path),
        "rootmirror_full_markdown": str(md_path),
        "continuity_integrity_score": result.continuity_integrity_score,
        "status": result.status,
        "checks": result.checks,
        "claim_boundary": "continuity_verification_only",
        "non_claim_locks": result.non_claim_locks,
    }

    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")

    return {
        "rootmirror_full_json": str(json_path),
        "rootmirror_full_markdown": str(md_path),
        "rootmirror_full_evidence": str(evidence_path),
    }