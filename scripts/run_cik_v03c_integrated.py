from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from cik.core.perturbation_integration import integrate_perturbation_if_available


def extract_last_json(text: str):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in command output.")
    return json.loads(text[start:end + 1])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CIK v0.3C integrated smoke.")
    parser.add_argument("--repo", default=r".\tests\fixtures\tiny_repo_with_context")
    parser.add_argument("--out", default=r".\outputs")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out).resolve()

    sweep_cmd = [
        sys.executable,
        str(Path("scripts") / "run_perturbation_sweep.py"),
        "--fixture",
        str(repo),
        "--out",
        str(out),
        "--operator",
        "missing_path",
    ]

    subprocess.run(sweep_cmd, check=True)

    run_cmd = [
        sys.executable,
        "-m",
        "cik",
        "run",
        "--instrument",
        "rcc-drift",
        "--repo",
        str(repo),
        "--out",
        str(out),
    ]

    proc = subprocess.run(run_cmd, check=True, capture_output=True, text=True)
    base = extract_last_json(proc.stdout)

    integrated = integrate_perturbation_if_available(base, out_root=out, repo_root=repo)

    print(json.dumps(integrated, indent=2))

    expected_reasons_absent = {"No perturbation sweep yet.", "RootMirror verification not enabled."}
    reasons = set(integrated.get("downgrade_reason") or [])

    if integrated.get("perturbation_sweep_integrated") is not True:
        return 2

    if integrated.get("perturbation_sweep_score") != 1.0:
        return 3

    if reasons.intersection(expected_reasons_absent):
        return 4

    if "Tesseract indexing not enabled." not in reasons:
        return 5

    return 0


if __name__ == "__main__":
    raise SystemExit(main())