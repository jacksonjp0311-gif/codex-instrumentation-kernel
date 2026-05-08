from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ArtifactRecord:
    artifact_type: str
    path: str
    exists: bool
    size_bytes: int
    sha256: Optional[str]
    run_id: Optional[str]
    relative_path: Optional[str] = None


@dataclass
class RunRecord:
    run_id: str
    instrument: str = "unknown"
    dphi_global: Optional[float] = None
    omega_mean: Optional[float] = None
    cif_score: Optional[float] = None
    maturity: Optional[str] = None
    classification: Optional[str] = None
    downgrade_reason: List[str] = field(default_factory=list)
    artifacts: Dict[str, str] = field(default_factory=dict)
    artifact_hashes: Dict[str, str] = field(default_factory=dict)
    non_claim_locks: Dict[str, bool] = field(default_factory=dict)