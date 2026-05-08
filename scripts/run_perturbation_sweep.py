from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from cik.perturbation import run_perturbation_sweep


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CIK v0.3 perturbation sweep.")
    parser.add_argument("--fixture", default=r".\tests\fixtures\tiny_repo_with_context")
    parser.add_argument("--out", default=r".\outputs")
    parser.add_argument("--operator", default="missing_path")
    args = parser.parse_args()

    fixture = Path(args.fixture).resolve()
    out = Path(args.out).resolve()

    if not fixture.exists():
        fallback = Path(".").resolve()
        print(
            f"[CIK v0.3] Fixture not found: {fixture}. Falling back to repo root: {fallback}",
            file=sys.stderr,
        )
        fixture = fallback

    result = run_perturbation_sweep(
        fixture=fixture,
        out_root=out,
        operator=args.operator,
    )

    print(json.dumps(result, indent=2))

    return 0 if result.get("status") == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())