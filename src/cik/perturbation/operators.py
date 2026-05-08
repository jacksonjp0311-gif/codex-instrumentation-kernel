from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import copy
import json
import shutil


CONTEXT_FILE_NAMES = {
    "repository_context_index.json",
    "rcc_context_map.json",
    "context.json",
    "rcc.json",
}


def clone_tree(source: str | Path, target: str | Path) -> Path:
    src = Path(source).resolve()
    dst = Path(target).resolve()

    if not src.exists():
        raise FileNotFoundError(f"Source fixture not found: {src}")

    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            ".pytest_cache",
            ".git",
            "outputs",
            "*.pyc",
        ),
    )

    return dst


def restore_from_source(source: str | Path, target: str | Path) -> Path:
    return clone_tree(source, target)


def _safe_load_json(path: Path) -> Dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _safe_write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def find_context_json_files(repo: str | Path) -> List[Path]:
    root = Path(repo).resolve()
    found: List[Path] = []

    for path in root.rglob("*.json"):
        if any(part in {".git", "__pycache__", ".pytest_cache", "outputs"} for part in path.parts):
            continue

        name_match = path.name in CONTEXT_FILE_NAMES
        content_match = False

        data = _safe_load_json(path)
        if isinstance(data, dict):
            serialized = json.dumps(data).lower()
            content_match = any(
                token in serialized
                for token in [
                    "declared_paths",
                    "required_paths",
                    "evidence_path",
                    "claim_evidence",
                    "repository_context",
                    "rcc",
                    "context",
                ]
            )

        if name_match or content_match:
            found.append(path)

    return found


def _add_missing_path_to_dict(data: Dict[str, Any], missing_path: str) -> Dict[str, Any]:
    damaged = copy.deepcopy(data)

    if isinstance(damaged.get("declared_paths"), list):
        damaged["declared_paths"].append(missing_path)
        return damaged

    if isinstance(damaged.get("required_paths"), list):
        damaged["required_paths"].append(missing_path)
        return damaged

    if isinstance(damaged.get("paths"), list):
        damaged["paths"].append(missing_path)
        return damaged

    if isinstance(damaged.get("repository"), dict):
        repo = damaged["repository"]
        if isinstance(repo.get("declared_paths"), list):
            repo["declared_paths"].append(missing_path)
            return damaged

    damaged.setdefault("declared_paths", [])
    damaged["declared_paths"].append(missing_path)
    damaged.setdefault("cik_v0_3_perturbation", {})
    damaged["cik_v0_3_perturbation"]["operator"] = "missing_path"
    damaged["cik_v0_3_perturbation"]["missing_path"] = missing_path

    return damaged


def apply_missing_path_perturbation(repo: str | Path, missing_path: str = "cik_v0_3_missing_path_DO_NOT_CREATE.txt") -> Dict[str, Any]:
    root = Path(repo).resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository not found: {root}")

    candidates = find_context_json_files(root)

    if not candidates:
        fallback = root / "docs" / "context" / "repository_context_index.json"
        fallback.parent.mkdir(parents=True, exist_ok=True)
        fallback.write_text(
            json.dumps(
                {
                    "schema": "CIK-v0.3-generated-context",
                    "repository": {
                        "name": root.name,
                        "declared_paths": ["README.md", missing_path],
                    },
                    "non_claim_locks": {
                        "generated_context_is_not_correctness_proof": True
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return {
            "operator": "missing_path",
            "path": str(fallback),
            "missing_path": missing_path,
            "created_fallback_context": True,
        }

    target = candidates[0]
    data = _safe_load_json(target) or {}
    damaged = _add_missing_path_to_dict(data, missing_path)
    _safe_write_json(target, damaged)

    return {
        "operator": "missing_path",
        "path": str(target),
        "missing_path": missing_path,
        "created_fallback_context": False,
    }