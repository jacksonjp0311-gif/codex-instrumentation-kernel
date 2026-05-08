from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
import hashlib


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def safe_node_id(prefix: str, value: str) -> str:
    cleaned = str(value).replace("\\", "/").replace(" ", "_")
    cleaned = cleaned.replace(":", "_")
    return f"node:{prefix}:{cleaned}"


def make_node(
    node_type: str,
    label: str,
    source: str = "file",
    path: Optional[str] = None,
    file_hash: Optional[str] = None,
    run_id: Optional[str] = None,
    instrument: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    identity = file_hash or run_id or label
    node_id = safe_node_id(node_type, identity)

    return {
        "id": node_id,
        "type": node_type,
        "label": label,
        "source": source,
        "path": path,
        "hash": file_hash,
        "run_id": run_id,
        "instrument": instrument,
        "metadata": metadata or {},
        "non_claim_locks": {
            "node_presence_is_not_correctness": True,
            "node_presence_is_not_truth": True,
        },
    }


def infer_artifact_type(path: Path) -> str:
    parts = [p.lower() for p in Path(path).parts]
    name = Path(path).name.lower()

    if "evidence_graph" in parts:
        return "evidence_graph"

    if "orchestration" in parts:
        return "orchestration"

    if "rootmirror_full" in parts or "rootmirror_full" in name:
        return "rootmirror"

    if "rootmirror" in parts or "rootmirror" in name:
        return "rootmirror"

    if "tesseract" in parts or "tesseract" in name:
        return "tesseract"

    if "perturbation" in parts or "perturbation" in name:
        return "perturbation"

    if "evidence" in parts or "evidence_package" in name:
        return "evidence"

    if "state" in parts or name.endswith("_state.json"):
        return "state"

    if "ledger" in parts or name.endswith(".jsonl"):
        return "ledger"

    if "reports" in parts or name.endswith("_report.md"):
        return "report"

    if "semantic" in parts or name.endswith("_summary.md"):
        return "semantic"

    return "artifact"


def infer_run_id(path: Path, payload: Optional[Dict[str, Any]] = None) -> Optional[str]:
    if payload:
        for key in [
            "run_id",
            "orchestration_run_id",
            "instrument_run_id",
            "parent_run_id",
        ]:
            if payload.get(key):
                return str(payload.get(key))

    name = Path(path).name

    suffixes = [
        "_orchestration_evidence_package.json",
        "_orchestration_state.json",
        "_composed_evidence_bundle.json",
        "_instrument_results.json",
        "_rootmirror_full_evidence_package.json",
        "_rootmirror_full.json",
        "_rootmirror_lite.json",
        "_evidence_package.json",
        "_state.json",
        "_drift_report.md",
        "_summary.md",
        "_perturbation_sweep.json",
        "_perturbation_sweep_report.md",
    ]

    for suffix in suffixes:
        if name.endswith(suffix):
            return name[:-len(suffix)]

    return None