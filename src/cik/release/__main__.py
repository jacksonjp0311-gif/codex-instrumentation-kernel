from __future__ import annotations

from pathlib import Path
import argparse
import json

from .bundle import build_release_bundle
from .checklist import build_release_checklist
from .locks import build_non_claim_locks
from .validator import build_validation_surface
from .writer import write_release_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CIK v1.0 stable local-first release")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name in ["lock", "checklist", "locks", "validate"]:
        p = sub.add_parser(name)
        p.add_argument("--repo-root", default=".")
        p.add_argument("--out", default="outputs")

    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    output_root = Path(args.out).resolve()

    if args.cmd == "lock":
        bundle = build_release_bundle(repo_root, output_root)
        paths = write_release_outputs(bundle, output_root)
        print(json.dumps({
            "status": bundle.get("status"),
            "paths": paths,
            "non_claim_locks": bundle.get("non_claim_locks"),
        }, indent=2))
        return 0

    if args.cmd == "checklist":
        print(json.dumps(build_release_checklist(repo_root), indent=2))
        return 0

    if args.cmd == "locks":
        print(json.dumps({
            "schema": "CIK-v1.0-non-claim-lock-registry",
            "version": "1.0",
            "locks": build_non_claim_locks(),
        }, indent=2))
        return 0

    if args.cmd == "validate":
        print(json.dumps(build_validation_surface(repo_root, output_root), indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())