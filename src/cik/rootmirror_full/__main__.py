from __future__ import annotations

from pathlib import Path
import argparse
import json
import sys

from .integration import run_rootmirror_full_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CIK v0.5 RootMirror full verifier")
    parser.add_argument("--repo-root", default=".", help="CIK repository root")
    parser.add_argument("--out", default="outputs", help="CIK output root")
    parser.add_argument("--target-repo", default="tests/fixtures/tiny_repo_with_context", help="Target repository for rcc-drift")
    parser.add_argument("--instrument", default="rcc-drift", help="Instrument name")
    parser.add_argument("--no-tesseract", action="store_true", help="Do not run tesseract-lite after instrument command")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    output_root = (repo_root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out).resolve()
    target_repo = (repo_root / args.target_repo).resolve() if not Path(args.target_repo).is_absolute() else Path(args.target_repo).resolve()

    command = [
        sys.executable,
        "-m",
        "cik",
        "run",
        "--instrument",
        args.instrument,
        "--repo",
        str(target_repo),
        "--out",
        str(output_root),
    ]

    payload = run_rootmirror_full_command(
        repo_root=repo_root,
        output_root=output_root,
        command=command,
        instrument=args.instrument,
        run_tesseract=not args.no_tesseract,
    )

    result = payload["result"]
    print(json.dumps({
        "status": result.status,
        "run_id": result.run_id,
        "continuity_integrity_score": result.continuity_integrity_score,
        "rootmirror_full": payload["rootmirror_full"],
        "downgrade_removed": result.downgrade_removed,
        "remaining_downgrade_reason": result.remaining_downgrade_reason,
        "command_returncode": payload["command_returncode"],
    }, indent=2))

    return 0 if payload["command_returncode"] == 0 and result.status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())