from __future__ import annotations

from pathlib import Path
import argparse
import json

from .builder import build_evidence_graph
from .queries import query_graph
from .writer import write_graph_outputs


def load_graph(output_root: Path) -> dict:
    path = Path(output_root) / "evidence_graph" / "evidence_graph.json"
    if not path.exists():
        graph = build_evidence_graph(output_root)
        write_graph_outputs(graph, output_root)
        return graph
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CIK v0.8 evidence graph")
    sub = parser.add_subparsers(dest="cmd", required=True)

    build = sub.add_parser("build")
    build.add_argument("--out", default="outputs")

    query = sub.add_parser("query")
    query.add_argument("--out", default="outputs")
    query.add_argument("--kind", required=True)
    query.add_argument("--run-id", default=None)
    query.add_argument("--claim", default=None)
    query.add_argument("--artifact", default=None)

    args = parser.parse_args(argv)

    output_root = Path(args.out).resolve()

    if args.cmd == "build":
        graph = build_evidence_graph(output_root)
        paths = write_graph_outputs(graph, output_root)
        payload = {
            "status": graph.get("validation", {}).get("status"),
            "node_count": graph.get("node_count"),
            "edge_count": graph.get("edge_count"),
            "artifacts": paths,
            "non_claim_locks": graph.get("non_claim_locks"),
        }
        print(json.dumps(payload, indent=2))
        return 0

    if args.cmd == "query":
        graph = load_graph(output_root)
        result = query_graph(
            graph,
            kind=args.kind,
            run_id=args.run_id,
            claim=args.claim,
            artifact=args.artifact,
        )
        print(json.dumps(result, indent=2))
        if result.get("status") == "unsupported":
            return 2
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())