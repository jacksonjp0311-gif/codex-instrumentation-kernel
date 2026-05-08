from __future__ import annotations

from pathlib import Path
import argparse
import json

from .run_plan import load_run_plan, write_default_run_plan
from .executor import execute_orchestration
from .writer import write_orchestration_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CIK v0.7 orchestration runner")
    parser.add_argument("--plan", default="configs/orchestration/default_run_plan.json")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="outputs")
    parser.add_argument("--write-default-plan", action="store_true")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    output_root = Path(args.out)

    if not output_root.is_absolute():
        output_root = repo_root / output_root

    plan_path = Path(args.plan)

    if not plan_path.is_absolute():
        plan_path = repo_root / plan_path

    if args.write_default_plan or not plan_path.exists():
        write_default_run_plan(plan_path)

    plan = load_run_plan(plan_path)
    bundle = execute_orchestration(plan, repo_root=repo_root, output_root=output_root)
    paths = write_orchestration_outputs(bundle, output_root=output_root)

    payload = {
        "status": bundle["state"]["status"],
        "orchestration_run_id": bundle["state"]["orchestration_run_id"],
        "instrument_count": bundle["state"]["instrument_count"],
        "passed_count": bundle["state"]["passed_count"],
        "failed_count": bundle["state"]["failed_count"],
        "skipped_count": bundle["state"]["skipped_count"],
        "blocked_count": bundle["state"]["blocked_count"],
        "artifacts": paths,
        "non_claim_locks": bundle["state"]["non_claim_locks"],
    }

    print(json.dumps(payload, indent=2))

    if bundle["state"]["status"] in {"pass", "warning"}:
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())