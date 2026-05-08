from __future__ import annotations

from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

from cik.rootmirror import (
    line_count,
    rootmirror_lite_verify,
    write_rootmirror_outputs,
    inject_rootmirror_into_state,
    inject_rootmirror_into_evidence,
)


def extract_json_object(text: str) -> dict:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < start:
        raise RuntimeError("Could not find JSON object in CIK run output.")
    return json.loads(text[start:end + 1])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=".")
    parser.add_argument("--fixture", default=r".\tests\fixtures\tiny_repo_with_context")
    parser.add_argument("--out", default=r".\outputs")
    args = parser.parse_args()

    repo_root = Path(args.repo).resolve()
    out_root = Path(args.out).resolve()
    ledger = out_root / "ledger" / "cik_ledger.jsonl"

    cwd_pre = str(Path.cwd().resolve())
    ledger_before = line_count(ledger)

    cmd = [
        sys.executable,
        "-m",
        "cik",
        "run",
        "--instrument",
        "rcc-drift",
        "--repo",
        str(Path(args.fixture).resolve()),
        "--out",
        str(out_root),
    ]

    completed = subprocess.run(
        cmd,
        cwd=str(repo_root),
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": str(repo_root / "src")},
    )

    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr, file=sys.stderr)
        return completed.returncode

    run_result = extract_json_object(completed.stdout)

    rm_result = rootmirror_lite_verify(
        repo_root=str(repo_root),
        run_result=run_result,
        ledger_count_before=ledger_before,
        cwd_pre=cwd_pre,
    )

    rm_paths = write_rootmirror_outputs(
        result=rm_result,
        out_dir=str(out_root),
        run_id=run_result.get("run_id", "cik_rootmirror_lite"),
    )

    artifacts = run_result.get("artifacts", {}) or {}
    inject_rootmirror_into_state(artifacts.get("state", ""), rm_result, rm_paths)
    inject_rootmirror_into_evidence(artifacts.get("evidence", ""), rm_result, rm_paths)

    print(json.dumps({
        "status": "ok" if rm_result["rootmirror_lite"]["status"] == "pass" else "warning",
        "rootmirror_lite": rm_result["rootmirror_lite"],
        "rootmirror_artifacts": rm_paths,
        "run_result": run_result,
    }, indent=2))

    return 0 if rm_result["rootmirror_lite"]["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())