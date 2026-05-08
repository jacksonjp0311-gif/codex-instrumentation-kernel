from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_release_outputs(bundle: Dict[str, Any], output_root: Path) -> Dict[str, str]:
    output_root = Path(output_root).resolve()
    release_root = output_root / "release"
    release_root.mkdir(parents=True, exist_ok=True)

    bundle_path = release_root / "release_bundle_v1_0.json"
    summary_path = release_root / "release_summary_v1_0.md"
    checklist_path = release_root / "release_checklist_v1_0.json"
    validation_path = release_root / "validation_surface_v1_0.json"
    locks_path = release_root / "non_claim_locks_v1_0.json"

    write_json(bundle_path, bundle)
    write_json(checklist_path, bundle.get("release_checklist", {}))
    write_json(validation_path, bundle.get("validation_surface", {}))
    write_json(locks_path, {
        "schema": "CIK-v1.0-non-claim-lock-registry",
        "version": "1.0",
        "locks": bundle.get("non_claim_locks", {}),
    })

    lines = [
        "# CIK v1.0 Release Summary",
        "",
        f"Release: {bundle.get('release_name')}",
        f"Version: {bundle.get('version')}",
        f"Status: {bundle.get('status')}",
        f"Generated: {bundle.get('generated_at')}",
        "",
        "## Stable CLI",
        "",
    ]

    for cmd in bundle.get("stable_cli", []):
        lines.append(f"- `{cmd}`")

    lines.extend([
        "",
        "## Git cleanliness",
        "",
        f"- status: {bundle.get('git_cleanliness', {}).get('status')}",
        "",
        "## Warnings",
        "",
    ])

    warnings = bundle.get("warnings", [])
    lines.extend([f"- {w}" for w in warnings] if warnings else ["- None"])

    lines.extend(["", "## Blocking gaps", ""])
    blocking = bundle.get("blocking_gaps", [])
    lines.extend([f"- {b}" for b in blocking] if blocking else ["- None"])

    lines.extend([
        "",
        "## Non-claim locks",
        "",
        "- Stable release is not truth.",
        "- Local validation is not formal verification.",
        "- Release bundle is not provenance.",
        "- Git cleanliness is not semantic validity.",
        "- Release notes are not external validation.",
        "",
    ])

    summary_path.write_text("\n".join(lines), encoding="utf-8")

    return {
        "release_bundle": str(bundle_path),
        "release_summary": str(summary_path),
        "release_checklist": str(checklist_path),
        "validation_surface": str(validation_path),
        "non_claim_locks": str(locks_path),
    }