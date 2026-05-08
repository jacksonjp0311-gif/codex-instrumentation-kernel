from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .checklist import build_release_checklist
from .locks import build_non_claim_locks
from .validator import build_validation_surface


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_release_bundle(repo_root: Path, output_root: Path) -> Dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    output_root = Path(output_root).resolve()

    locks = build_non_claim_locks()
    checklist = build_release_checklist(repo_root)
    validation = build_validation_surface(repo_root, output_root)

    status = "ready"
    warnings = []
    blocking = []

    if checklist.get("status") != "pass":
        status = "not_ready"
        blocking.extend(checklist.get("blocking_gaps", []))

    git_status = validation.get("git_cleanliness", {}).get("status")
    if git_status == "dirty":
        status = "partial" if status == "ready" else status
        warnings.append("Git working tree has pending changes at release bundle generation time.")

    if git_status == "unknown":
        status = "partial" if status == "ready" else status
        warnings.append("Git cleanliness could not be determined.")

    return {
        "schema": "CIK-v1.0-release-bundle",
        "version": "1.0",
        "release_name": "Stable Local-First Release",
        "generated_at": utc_now(),
        "source_version": "CIK v0.9",
        "status": status,
        "warnings": warnings,
        "blocking_gaps": blocking,
        "stable_cli": validation.get("stable_cli_commands", []),
        "required_artifacts": checklist.get("items", []),
        "validation_surface": validation,
        "release_checklist": checklist,
        "git_cleanliness": validation.get("git_cleanliness", {}),
        "outputs": {
            "release_bundle": str(output_root / "release" / "release_bundle_v1_0.json"),
            "release_summary": str(output_root / "release" / "release_summary_v1_0.md"),
            "release_checklist": str(output_root / "release" / "release_checklist_v1_0.json"),
            "validation_surface": str(output_root / "release" / "validation_surface_v1_0.json"),
            "non_claim_locks": str(output_root / "release" / "non_claim_locks_v1_0.json"),
            "release_notes": str(repo_root / "docs" / "release" / "release_notes_v1_0.md"),
        },
        "non_claim_locks": locks,
    }