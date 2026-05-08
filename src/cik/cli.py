from __future__ import annotations

import argparse
import json
from pathlib import Path

from cik.instruments.registry import get_instrument, list_instruments
from cik.core.loop import InstrumentationLoop
from cik.injection.register import ensure_default_injection_register


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cik",
        description="Codex Instrumentation Kernel v0.1"
    )
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="Run an instrument")
    run.add_argument("--instrument", default="rcc-drift")
    run.add_argument("--repo", default=".")
    run.add_argument("--out", default=None)

    sub.add_parser("list-instruments", help="List available instruments")

    inj = sub.add_parser("validate-injection-register", help="Ensure injection register exists")
    inj.add_argument("--repo", default=".")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "list-instruments":
        print(json.dumps({"instruments": list_instruments()}, indent=2))
        return 0

    if args.command == "validate-injection-register":
        path = ensure_default_injection_register(Path(args.repo).resolve())
        print(json.dumps({"status": "ok", "injection_register": str(path)}, indent=2))
        return 0

    if args.command == "run":
        repo = Path(args.repo).resolve()
        out_root = Path(args.out).resolve() if args.out else repo / "outputs"
        instrument = get_instrument(args.instrument)
        loop = InstrumentationLoop()
        result = loop.run(instrument, {"repo_root": repo, "out_root": out_root})
        try:
            from cik.core.perturbation_integration import integrate_perturbation_if_available
            result = integrate_perturbation_if_available(
                result,
                out_root=getattr(args, "out", None),
                repo_root=getattr(args, "repo", None),
            )
        except Exception:
            pass
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
