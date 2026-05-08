from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import os
import subprocess


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def count_lines(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text:
        return 0
    return len(text.splitlines())


def run_git(args: list[str], root: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(root),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None


@dataclass
class RootAnchor:
    root_path: str
    cwd: str
    git_branch: Optional[str]
    git_head: Optional[str]
    git_status: Optional[str]
    ledger_height: int
    timestamp: str
    pythonpath: str


def capture_anchor(repo_root: Path, ledger_path: Path) -> RootAnchor:
    repo_root = repo_root.resolve()
    return RootAnchor(
        root_path=str(repo_root),
        cwd=str(Path.cwd().resolve()),
        git_branch=run_git(["branch", "--show-current"], repo_root),
        git_head=run_git(["rev-parse", "HEAD"], repo_root),
        git_status=run_git(["status", "--short"], repo_root),
        ledger_height=count_lines(ledger_path),
        timestamp=utc_now(),
        pythonpath=os.environ.get("PYTHONPATH", ""),
    )