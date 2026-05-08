from __future__ import annotations

from typing import Any, Dict, Optional
import hashlib


def edge_id(edge_type: str, source: str, target: str) -> str:
    raw = f"{edge_type}|{source}|{target}".encode("utf-8")
    return "edge:" + hashlib.sha256(raw).hexdigest()[:24]


def make_edge(
    edge_type: str,
    source: str,
    target: str,
    support: Optional[str] = None,
    confidence: float = 1.0,
    status: str = "artifact_backed",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "id": edge_id(edge_type, source, target),
        "type": edge_type,
        "source": source,
        "target": target,
        "support": support,
        "confidence": float(confidence),
        "status": status,
        "metadata": metadata or {},
        "non_claim_locks": {
            "edge_presence_is_not_truth": True,
            "edge_linkage_is_not_correctness": True,
        },
    }