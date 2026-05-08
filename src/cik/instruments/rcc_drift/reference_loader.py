from __future__ import annotations

from pathlib import Path

from cik.utils.safe_json import read_json


def load_reference(repo_root: Path) -> dict:
    candidates = [
        repo_root / "docs" / "architecture" / "rcc_context_map.json",
        repo_root / "docs" / "context" / "repository_context_index.json",
        repo_root / "cik_context.json",
    ]
    for path in candidates:
        data = read_json(path, default=None)
        if isinstance(data, dict):
            data["_reference_path"] = str(path)
            return data

    return {
        "_reference_path": None,
        "declared_paths": [],
        "evidence_paths": [],
        "commands": [],
        "claims": [],
        "staleness": {"is_stale": False}
    }