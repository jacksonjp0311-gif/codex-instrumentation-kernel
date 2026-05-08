from __future__ import annotations


def classify_cif(score: float, maturity: str, downgrade_reasons: list[str]) -> str:
    if score >= 0.90 and maturity in {"CIF6", "CIF7", "CIF8"} and not downgrade_reasons:
        return "CIF-A"
    if score >= 0.60 and maturity in {"CIF4", "CIF5", "CIF6", "CIF7", "CIF8"}:
        return "CIF-B"
    if score >= 0.40:
        return "CIF-C"
    if score >= 0.20:
        return "CIF-D"
    return "CIF-E"