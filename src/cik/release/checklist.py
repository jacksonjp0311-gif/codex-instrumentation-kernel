from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


REQUIRED_RELEASE_FILES = [
    "README.md",
    "docs/context/repository_context_index.json",
    "docs/architecture/rcc_context_map.md",
    "docs/protocols/rootmirror_full_contract.md",
    "docs/protocols/instrument_plugin_contract.md",
    "docs/protocols/orchestration_contract.md",
    "docs/protocols/evidence_graph_contract.md",
    "docs/protocols/tesseract_full_contract.md",
    "docs/protocols/dashboard_contract.md",
    "docs/release/release_notes_v1_0.md",
    "docs/release/release_checklist_v1_0.md",
    "docs/release/local_install_v1_0.md",
    "docs/release/validation_surface_v1_0.md",
    "docs/release/non_claim_locks_v1_0.md",
    "docs/release/output_contract_v1_0.md",
]


REQUIRED_SMOKES = [
    "powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v09_tesseract_dashboard.ps1",
    "powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v08_evidence_graph.ps1",
    "powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v07_orchestration.ps1",
    "powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v06_integrated.ps1",
    "powershell -ExecutionPolicy Bypass -File .\\scripts\\run_cik_v1_0_release_lock.ps1",
]


def build_release_checklist(repo_root: Path) -> Dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    items: List[Dict[str, Any]] = []

    for rel in REQUIRED_RELEASE_FILES:
        path = repo_root / rel
        items.append({
            "id": rel.replace("\\", "/"),
            "kind": "required_file",
            "description": f"Required release file exists: {rel}",
            "status": "pass" if path.exists() else "missing",
            "path": str(path),
        })

    for cmd in REQUIRED_SMOKES:
        items.append({
            "id": cmd,
            "kind": "required_smoke",
            "description": f"Required smoke command declared: {cmd}",
            "status": "declared",
            "command": cmd,
        })

    blocking = [item for item in items if item["status"] == "missing"]

    return {
        "schema": "CIK-v1.0-release-checklist",
        "version": "1.0",
        "status": "pass" if not blocking else "fail",
        "items": items,
        "blocking_gaps": blocking,
        "non_claim_locks": {
            "checklist_is_not_certification": True,
            "checklist_pass_is_not_correctness": True,
        },
    }