from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable
import hashlib


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def discover_expected_artifacts(output_root: Path, run_id: str) -> Dict[str, str]:
    output_root = output_root.resolve()
    artifacts: Dict[str, str] = {}

    candidates = {
        "state": output_root / "state",
        "evidence": output_root / "evidence",
        "report": output_root / "reports",
        "semantic": output_root / "semantic",
        "rootmirror": output_root / "rootmirror",
        "perturbation": output_root / "perturbation",
        "tesseract": output_root / "tesseract",
        "injection": output_root / "injection",
    }

    for artifact_type, folder in candidates.items():
        if not folder.exists():
            continue

        matches = [
            p for p in folder.rglob("*")
            if p.is_file() and run_id in p.name
        ]

        if not matches and artifact_type == "tesseract":
            matches = [
                p for p in folder.rglob("tesseract_lite_index.json")
                if p.is_file()
            ]

        if matches:
            artifacts[artifact_type] = str(sorted(matches)[-1])

    ledger_path = output_root / "ledger" / "cik_ledger.jsonl"
    if ledger_path.exists():
        artifacts["ledger"] = str(ledger_path)

    return artifacts


def hash_artifacts(artifacts: Dict[str, str]) -> Dict[str, str]:
    hashes: Dict[str, str] = {}
    for key, value in artifacts.items():
        path = Path(value)
        if path.exists() and path.is_file():
            hashes[key] = sha256_file(path)
    return hashes


def iter_hashable_output_files(output_root: Path) -> Iterable[Path]:
    skip_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    for path in output_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        yield path


def output_root_hash_surface(output_root: Path) -> str:
    output_root = output_root.resolve()
    child_hashes = []
    if output_root.exists():
        for path in iter_hashable_output_files(output_root):
            try:
                child_hashes.append(sha256_file(path))
            except OSError:
                continue

    payload = "\n".join(sorted(child_hashes)).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()