from __future__ import annotations

from pathlib import Path
import argparse
import json

from .package import build_tesseract_package
from .writer import write_tesseract_outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CIK v0.9 full Tesseract and dashboard package")
    sub = parser.add_subparsers(dest="cmd", required=True)

    build = sub.add_parser("build")
    build.add_argument("--out", default="outputs")

    dashboard = sub.add_parser("dashboard")
    dashboard.add_argument("--out", default="outputs")

    readiness = sub.add_parser("readiness")
    readiness.add_argument("--out", default="outputs")

    args = parser.parse_args(argv)

    output_root = Path(args.out).resolve()
    bundle = build_tesseract_package(output_root)
    paths = write_tesseract_outputs(bundle, output_root)

    if args.cmd == "build":
        payload = {
            "status": bundle["release_readiness"]["status"],
            "node_count": bundle["package"]["node_count"],
            "edge_count": bundle["package"]["edge_count"],
            "artifacts": paths,
            "non_claim_locks": bundle["package"]["non_claim_locks"],
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.cmd == "dashboard":
        print(json.dumps({
            "status": "emitted",
            "dashboard_json": paths["dashboard_json"],
            "dashboard_report": paths["dashboard_report"],
            "non_claim_locks": bundle["dashboard"]["non_claim_locks"],
        }, indent=2))
        return 0

    if args.cmd == "readiness":
        print(json.dumps(bundle["release_readiness"], indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())