from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional
import json
import subprocess
import sys

from .anchors import capture_anchor
from .verifier import verify_rootmirror_full, RootMirrorFullResult
from .writer import write_rootmirror_full_outputs


def find_latest_run_id(output_root: Path) -> Optional[str]:
    state_dir = output_root / "state"
    if not state_dir.exists():
        return None

    state_files = sorted(
        [p for p in state_dir.glob("*_state.json") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
    )

    if not state_files:
        return None

    latest = state_files[-1]
    try:
        payload = json.loads(latest.read_text(encoding="utf-8"))
        for key in ("run_id", "id"):
            if key in payload and payload[key]:
                return str(payload[key])
    except Exception:
        pass

    name = latest.name
    if name.endswith("_state.json"):
        return name[:-len("_state.json")]
    return latest.stem


def maybe_run_tesseract(repo_root: Path, output_root: Path) -> None:
    try:
        subprocess.run(
            [sys.executable, "-m", "cik.tesseract", "--out", str(output_root)],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
            check=False,
        )
    except Exception:
        return


def run_rootmirror_full_command(
    repo_root: Path,
    output_root: Path,
    command: List[str],
    instrument: str = "rcc-drift",
    expected_artifacts: list[str] | None = None,
    ledger_append_expected: int = 1,
    run_tesseract: bool = True,
) -> Dict[str, object]:
    repo_root = repo_root.resolve()
    output_root = output_root.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    ledger_path = output_root / "ledger" / "cik_ledger.jsonl"
    pre_anchor = capture_anchor(repo_root, ledger_path)

    completed = subprocess.run(
        command,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )

    if run_tesseract:
        maybe_run_tesseract(repo_root, output_root)

    run_id = find_latest_run_id(output_root)
    if not run_id:
        run_id = "unknown_run"

    result: RootMirrorFullResult = verify_rootmirror_full(
        repo_root=repo_root,
        output_root=output_root,
        run_id=run_id,
        instrument=instrument,
        command=" ".join(command),
        pre_anchor=pre_anchor,
        expected_artifacts=expected_artifacts,
        ledger_append_expected=ledger_append_expected,
    )

    paths = write_rootmirror_full_outputs(result, output_root)

    return {
        "command_returncode": completed.returncode,
        "command_stdout": completed.stdout,
        "command_stderr": completed.stderr,
        "run_id": run_id,
        "rootmirror_full": paths,
        "result": result,
    }