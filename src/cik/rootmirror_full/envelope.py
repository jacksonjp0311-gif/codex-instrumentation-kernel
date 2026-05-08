from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RunEnvelope:
    run_id: str
    instrument: str
    repo_root: str
    output_root: str
    command: str
    expected_artifacts: List[str]
    declared: bool = True
    ledger_append_expected: int = 1
    claim_boundary: str = "continuity_verification_only"