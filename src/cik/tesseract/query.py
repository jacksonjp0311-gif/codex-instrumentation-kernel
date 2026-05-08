from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
import json


def load_index(index_path: str | Path) -> Dict[str, Any]:
    path = Path(index_path)
    return json.loads(path.read_text(encoding="utf-8"))


def find_run(index: Dict[str, Any], run_id: str) -> Optional[Dict[str, Any]]:
    for record in index.get("records", []):
        if record.get("run_id") == run_id:
            return record
    return None


def artifacts_by_type(index: Dict[str, Any], artifact_type: str) -> List[Dict[str, Any]]:
    return [
        artifact
        for artifact in index.get("artifact_records", [])
        if artifact.get("artifact_type") == artifact_type
    ]


def latest_records(index: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
    records = list(index.get("records", []))
    return records[-max(1, int(limit)) :]