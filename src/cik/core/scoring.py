from __future__ import annotations

from cik.core.metrics import clamp01


DEFAULT_CIF_COMPONENTS = {
    "dphi_declared": 1.0,
    "omega_declared": 1.0,
    "perturbation_coverage": 0.0,
    "artifact_emission": 1.0,
    "rootmirror_continuity": 0.0,
    "falsification_surface": 1.0,
    "memory_discipline": 1.0,
}


def cif_score(components: dict[str, float] | None = None) -> float:
    values = dict(DEFAULT_CIF_COMPONENTS)
    if components:
        values.update(components)
    return clamp01(sum(clamp01(v) for v in values.values()) / len(values))