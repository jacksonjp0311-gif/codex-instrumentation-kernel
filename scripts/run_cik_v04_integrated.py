from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from cik.tesseract.index import write_tesseract_index
from cik.tesseract.integration import integrate_tesseract_if_available


def extract_last_json(text: str):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in command output.")
    return json.loads(text[start:end + 1])


def main() -> int:
    root = Path.cwd()
    out = root / "outputs"
    repo = root / "tests" / "fixtures" / "tiny_repo_with_context"

    # Ensure current v0.3 artifacts exist.
    pert_script = root / "scripts" / "run_perturbation_sweep.ps1"
    if pert_script.exists():
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(pert_script)],
            check=True,
        )

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

    index = write_tesseract_index(out)
    integrated = integrate_tesseract_if_available(base, output_root=out)

    print(json.dumps(integrated, indent=2))

    if index.get("index_integrity_score") != 1.0:
        return 2
    if integrated.get("tesseract_lite_integrated") is not True:
        return 3
    if integrated.get("maturity") != "CIF7-ready":
        return 4
    if "Tesseract indexing not enabled." in (integrated.get("downgrade_reason") or []):
        return 5

    return 0


if __name__ == "__main__":
    raise SystemExit(main())