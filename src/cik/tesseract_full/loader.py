from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json

from cik.evidence_graph.builder import build_evidence_graph
from cik.evidence_graph.writer import write_graph_outputs


def load_or_build_evidence_graph(output_root: Path) -> Dict[str, Any]:
    output_root = Path(output_root).resolve()
    graph_path = output_root / "evidence_graph" / "evidence_graph.json"

    if graph_path.exists():
        return json.loads(graph_path.read_text(encoding="utf-8"))

    graph = build_evidence_graph(output_root)
    write_graph_outputs(graph, output_root)
    return graph