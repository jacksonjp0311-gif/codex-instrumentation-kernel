from __future__ import annotations


def maturity_from_features(features: dict[str, bool]) -> str:
    if features.get("reusable_injectable") and features.get("evidence_package"):
        return "CIF8"
    if features.get("indexed"):
        return "CIF7"
    if features.get("rootmirror_verified"):
        return "CIF6"
    if features.get("perturbation_tested"):
        return "CIF5"
    if features.get("artifact_emitting"):
        return "CIF4"
    if features.get("runnable"):
        return "CIF3"
    if features.get("architecture"):
        return "CIF2"
    if features.get("theory"):
        return "CIF1"
    return "CIF0"


def default_v01_maturity() -> str:
    return "CIF4"