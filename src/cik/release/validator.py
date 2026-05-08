from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import subprocess


STABLE_CLI_COMMANDS = [
    'python -m cik run --instrument rcc-drift --repo ".\\tests\\fixtures\\tiny_repo_with_context" --out ".\\outputs"',
    'python -m cik.tesseract --out ".\\outputs"',
    'python -m cik.rootmirror_full --repo-root "." --out ".\\outputs" --target-repo ".\\tests\\fixtures\\tiny_repo_with_context"',
    'python -m cik.orchestration --repo-root "." --out ".\\outputs" --plan ".\\configs\\orchestration\\default_run_plan.json"',
    'python -m cik.evidence_graph build --out ".\\outputs"',
    'python -m cik.evidence_graph query --out ".\\outputs" --kind runs',
    'python -m cik.tesseract_full build --out ".\\outputs"',
    'python -m cik.tesseract_full dashboard --out ".\\outputs"',
    'python -m cik.tesseract_full readiness --out ".\\outputs"',
    'python -m cik.release lock --out ".\\outputs"',
]


VALIDATION_COMMANDS = [
    "python -m unittest tests.test_rcc_readmes -v",
    "python -m unittest discover -s tests",
    'powershell -ExecutionPolicy Bypass -File ".\\scripts\\run_cik_v09_tesseract_dashboard.ps1"',
    'powershell -ExecutionPolicy Bypass -File ".\\scripts\\run_cik_v08_evidence_graph.ps1"',
    'powershell -ExecutionPolicy Bypass -File ".\\scripts\\run_cik_v07_orchestration.ps1"',
    'powershell -ExecutionPolicy Bypass -File ".\\scripts\\run_cik_v06_integrated.ps1"',
    'powershell -ExecutionPolicy Bypass -File ".\\scripts\\run_cik_v1_0_release_lock.ps1"',
    "git status --short",
]


def read_git_status(repo_root: Path) -> Dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
            check=False,
        )
        pending = [line for line in result.stdout.splitlines() if line.strip()]
        return {
            "status": "clean" if not pending else "dirty",
            "pending": pending,
            "returncode": result.returncode,
        }
    except Exception as exc:
        return {
            "status": "unknown",
            "pending": [],
            "error": str(exc),
        }


def build_validation_surface(repo_root: Path, output_root: Path) -> Dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    output_root = Path(output_root).resolve()

    expected_outputs = [
        output_root / "state",
        output_root / "ledger",
        output_root / "evidence",
        output_root / "rootmirror_full",
        output_root / "orchestration",
        output_root / "evidence_graph",
        output_root / "tesseract_full",
        output_root / "dashboard",
        output_root / "release",
    ]

    return {
        "schema": "CIK-v1.0-validation-surface",
        "version": "1.0",
        "stable_cli_commands": STABLE_CLI_COMMANDS,
        "validation_commands": VALIDATION_COMMANDS,
        "output_status": [{"path": str(p), "exists": p.exists()} for p in expected_outputs],
        "git_cleanliness": read_git_status(repo_root),
        "non_claim_locks": {
            "local_validation_is_not_formal_verification": True,
            "stable_cli_is_not_correctness": True,
            "git_cleanliness_is_not_semantic_validity": True,
        },
    }