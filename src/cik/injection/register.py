from __future__ import annotations

from pathlib import Path

from cik.utils.safe_json import write_json, read_json


DEFAULT_REGISTER = {
    "schema": "CIK-v0.1-injection-register",
    "injection_status": "ACTIVE",
    "injection_version": "I-v0.1",
    "host_artifact": "CIK v0.1 Software Runtime",
    "injected_artifacts": [
        {
            "artifact": "CIF v2.1",
            "operator": "Anchor -> Shape -> Measure -> Weight -> Stress -> Classify -> Fossilize -> Verify -> Index -> Interpret",
            "injection_point": "runtime loop and maturity classification",
            "failure_surface_repaired": "theory standard not executable as software"
        },
        {
            "artifact": "RCC v1.3",
            "operator": "repository context surfaces + claim/evidence + AI task protocol",
            "injection_point": "repository structure and context validation",
            "failure_surface_repaired": "AI agents can modify code without bounded context"
        },
        {
            "artifact": "AIT v1.0 / HYDRA",
            "operator": "Anchor -> Inject -> Retract -> Seal",
            "injection_point": "instrument registry and module admission",
            "failure_surface_repaired": "new instruments can be added without edge evidence"
        }
    ],
    "phase_change_status": "STRUCTURAL_LIFT",
    "downgrade_rule": "If injected layers weaken host locks or add ceremony without runtime evidence, classify partial or rejected."
}


def injection_register_path(repo_root: Path) -> Path:
    return repo_root / "outputs" / "injection" / "injection_register.json"


def ensure_default_injection_register(repo_root: Path) -> Path:
    path = injection_register_path(repo_root)
    existing = read_json(path, default=None)
    if existing is None:
        write_json(path, DEFAULT_REGISTER)
    return path