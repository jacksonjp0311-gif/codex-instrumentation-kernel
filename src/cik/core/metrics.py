from __future__ import annotations


def clamp01(value: float) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except Exception:
        return 0.0


def omega_from_dphi(dphi: float) -> float:
    return 1.0 / (1.0 + abs(float(dphi)))


def weighted_sum(components: dict[str, float], weights: dict[str, float]) -> float:
    total = 0.0
    for key, weight in weights.items():
        total += float(weight) * clamp01(float(components.get(key, 0.0)))
    return clamp01(total)