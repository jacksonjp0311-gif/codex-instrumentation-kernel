from __future__ import annotations

from pathlib import Path


def scan_repo(repo_root: Path) -> dict:
    paths = []
    for p in repo_root.rglob("*"):
        if any(part in {".git", "__pycache__", ".pytest_cache"} for part in p.parts):
            continue
        if p.is_file():
            try:
                paths.append(str(p.relative_to(repo_root)).replace("\\", "/"))
            except Exception:
                pass
    return {"files": sorted(paths)}