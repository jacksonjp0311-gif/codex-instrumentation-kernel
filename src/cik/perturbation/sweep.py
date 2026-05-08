from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from datetime import datetime, timezone
import json
import tempfile

from .operators import apply_missing_path_perturbation, clone_tree, find_context_json_files
from .report import write_sweep_evidence_package, write_sweep_json, write_sweep_report
from .scoring import SweepMeasurement, SweepTolerances, build_sweep_result, omega_from_dphi


def _safe_load_json(path: Path) -> Dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _flatten_strings(obj: Any) -> Iterable[str]:
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from _flatten_strings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from _flatten_strings(value)


def _extract_declared_paths_from_json(data: Dict[str, Any]) -> List[str]:
    paths: List[str] = []

    def visit(obj: Any, key_hint: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                lowered = str(key).lower()
                if lowered in {"declared_paths", "required_paths", "paths", "artifacts", "outputs"}:
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, str):
                                paths.append(item)
                            elif isinstance(item, dict):
                                for s in _flatten_strings(item):
                                    if _looks_like_path(s):
                                        paths.append(s)
                    elif isinstance(value, dict):
                        for s in _flatten_strings(value):
                            if _looks_like_path(s):
                                paths.append(s)
                    elif isinstance(value, str):
                        paths.append(value)
                elif lowered in {"path", "evidence_path", "source_path", "target_path", "root_index"}:
                    if isinstance(value, str):
                        paths.append(value)
                else:
                    visit(value, lowered)
        elif isinstance(obj, list):
            for item in obj:
                visit(item, key_hint)

    visit(data)
    return paths


def _looks_like_path(text: str) -> bool:
    if not text or len(text) > 260:
        return False
    if "://" in text:
        return False
    return any(token in text for token in ["/", "\\", ".md", ".json", ".py", ".txt", ".toml", ".yml", ".yaml"])


def _normalize_candidate_path(text: str) -> str:
    return text.replace("\\", "/")


def _candidate_exists(repo_root: Path, candidate: str) -> bool:
    c = _normalize_candidate_path(candidate).strip()

    if not c:
        return True

    if c.startswith("sha256:"):
        return True

    if c.startswith("outputs/"):
        return True

    if c.startswith("./"):
        c = c[2:]

    path = Path(c)
    if path.is_absolute():
        return path.exists()

    return (repo_root / path).exists()


def discover_declared_paths(repo_root: str | Path) -> List[str]:
    root = Path(repo_root).resolve()
    paths: List[str] = []

    for context_file in find_context_json_files(root):
        data = _safe_load_json(context_file)
        if isinstance(data, dict):
            paths.extend(_extract_declared_paths_from_json(data))

    if not paths:
        if (root / "README.md").exists():
            paths.append("README.md")
        if (root / "pyproject.toml").exists():
            paths.append("pyproject.toml")
        if (root / "docs").exists():
            paths.append("docs")

    unique: List[str] = []
    for p in paths:
        if p not in unique and _looks_like_path(p):
            unique.append(p)

    return unique


def measure_repository_context(repo_root: str | Path, label: str = "measurement") -> Dict[str, Any]:
    root = Path(repo_root).resolve()
    paths = discover_declared_paths(root)

    missing: List[str] = []
    present: List[str] = []

    for candidate in paths:
        if _candidate_exists(root, candidate):
            present.append(candidate)
        else:
            missing.append(candidate)

    total = max(len(paths), 1)
    missing_path_drift = len(missing) / total

    dphi = min(1.0, missing_path_drift)
    omega = omega_from_dphi(dphi)

    run_id = f"cik_v03_{label}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}"

    return {
        "schema": "CIK-v0.3-context-measurement",
        "run_id": run_id,
        "label": label,
        "repo_root": str(root),
        "declared_path_count": len(paths),
        "present_path_count": len(present),
        "missing_path_count": len(missing),
        "missing_paths": missing,
        "present_paths": present,
        "dphi_global": dphi,
        "omega_mean": omega,
        "non_claim_locks": {
            "repository_context_measurement_is_not_code_correctness": True,
            "missing_path_drift_is_not_runtime_correctness": True,
            "omega_is_not_truth": True,
        },
    }


def _measurement_to_dataclass(measurement: Dict[str, Any]) -> SweepMeasurement:
    return SweepMeasurement(
        label=measurement["label"],
        run_id=measurement["run_id"],
        dphi_global=float(measurement["dphi_global"]),
        omega_mean=float(measurement["omega_mean"]),
        state_path="",
        evidence_path="",
    )


def run_perturbation_sweep(
    fixture: str | Path,
    out_root: str | Path,
    operator: str = "missing_path",
    tolerances: SweepTolerances | None = None,
) -> Dict[str, Any]:
    source = Path(fixture).resolve()
    out = Path(out_root).resolve()
    out.mkdir(parents=True, exist_ok=True)

    run_id = f"cik_perturbation_sweep_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

    with tempfile.TemporaryDirectory(prefix="cik_v03_sweep_") as tmp:
        tmp_root = Path(tmp)

        baseline_repo = clone_tree(source, tmp_root / "baseline")
        perturbed_repo = clone_tree(source, tmp_root / "perturbed")
        restored_repo = clone_tree(source, tmp_root / "restored")

        baseline_raw = measure_repository_context(baseline_repo, label="baseline")

        if operator != "missing_path":
            raise ValueError(f"Unsupported perturbation operator for v0.3 implementation: {operator}")

        perturbation_record = apply_missing_path_perturbation(perturbed_repo)
        perturbed_raw = measure_repository_context(perturbed_repo, label="perturbed")

        restored_raw = measure_repository_context(restored_repo, label="restored")

        result = build_sweep_result(
            run_id=run_id,
            instrument="rcc-drift-compatible-context-measurement",
            fixture=str(source),
            perturbation_operator=operator,
            baseline=_measurement_to_dataclass(baseline_raw),
            perturbed=_measurement_to_dataclass(perturbed_raw),
            restored=_measurement_to_dataclass(restored_raw),
            tolerances=tolerances or SweepTolerances(),
            perturbation_record=perturbation_record,
            evidence_complete=True,
        )

        result["raw_measurements"] = {
            "baseline": baseline_raw,
            "perturbed": perturbed_raw,
            "restored": restored_raw,
        }

        sweep_json = write_sweep_json(result, out)
        sweep_report = write_sweep_report(result, out)
        evidence = write_sweep_evidence_package(result, out, sweep_json, sweep_report)

        result["artifacts"] = {
            "sweep_json": sweep_json,
            "sweep_report": sweep_report,
            "evidence": evidence,
        }

        Path(sweep_json).write_text(json.dumps(result, indent=2), encoding="utf-8")

        return result