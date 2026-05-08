from __future__ import annotations

from pathlib import Path

from cik.core.metrics import clamp01, weighted_sum
from cik.instruments.rcc_drift.defaults import DEFAULT_WEIGHTS


def fraction_missing(repo_root: Path, rel_paths: list[str]) -> float:
    if not rel_paths:
        return 0.0
    missing = 0
    for rel in rel_paths:
        if not (repo_root / rel).exists():
            missing += 1
    return clamp01(missing / len(rel_paths))


def evidence_drift(repo_root: Path, evidence_paths: list[str]) -> float:
    return fraction_missing(repo_root, evidence_paths)


def command_drift(commands: list[dict]) -> float:
    if not commands:
        return 0.0
    bad = 0
    for cmd in commands:
        if not cmd.get("declared", True):
            bad += 1
    return clamp01(bad / len(commands))


def claim_drift(claims: list[dict]) -> float:
    if not claims:
        return 0.0
    unsupported = 0
    for claim in claims:
        if not claim.get("supported", False):
            unsupported += 1
    return clamp01(unsupported / len(claims))


def staleness_drift(staleness: dict) -> float:
    if not staleness:
        return 0.0
    return 1.0 if staleness.get("is_stale", False) else 0.0


def compute_drift(repo_root: Path, reference: dict) -> dict:
    components = {
        "missing_path_drift": fraction_missing(repo_root, reference.get("declared_paths", [])),
        "staleness_drift": staleness_drift(reference.get("staleness", {})),
        "claim_drift": claim_drift(reference.get("claims", [])),
        "evidence_drift": evidence_drift(repo_root, reference.get("evidence_paths", [])),
        "command_drift": command_drift(reference.get("commands", [])),
    }
    dphi = weighted_sum(components, DEFAULT_WEIGHTS)
    return {"components": components, "dphi_global": dphi, "weights": DEFAULT_WEIGHTS}