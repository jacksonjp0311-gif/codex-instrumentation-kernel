from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, Optional
import json


ROOTMIRROR_LITE_REASON = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
TESSERACT_REASON = "Tesseract indexing not enabled."
NO_PERTURBATION_REASON = "No perturbation sweep yet."
ROOTMIRROR_OLD_REASON = "RootMirror verification not enabled."


def clamp01(x: Any) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def _safe_load_json(path: Path) -> Optional[Dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _candidate_roots(out_root: Any = None, repo_root: Any = None) -> Iterable[Path]:
    """
    Scope rule:
    - If out_root or repo_root is explicitly supplied, search only those roots.
    - Fall back to cwd only when no explicit root is supplied.

    This prevents tests using empty temp outputs from accidentally consuming
    real repository evidence in the current working directory.
    """
    seen = set()
    explicit = []

    for raw in [out_root, repo_root]:
        if raw:
            explicit.append(raw)

    if explicit:
        for raw in explicit:
            try:
                p = Path(raw).resolve()
                if p not in seen:
                    seen.add(p)
                    yield p
            except Exception:
                pass
        return

    try:
        cwd = Path.cwd().resolve()
        if cwd not in seen:
            seen.add(cwd)
            yield cwd
    except Exception:
        pass


def find_latest_perturbation_evidence(out_root: Any = None, repo_root: Any = None) -> Optional[Path]:
    candidates = []

    for root in _candidate_roots(out_root=out_root, repo_root=repo_root):
        search_roots = [
            root,
            root / "outputs",
            root / "evidence",
            root / "outputs" / "evidence",
            root / "perturbation",
            root / "outputs" / "perturbation",
        ]

        for search_root in search_roots:
            if not search_root.exists():
                continue

            candidates.extend(search_root.rglob("*perturbation_evidence_package.json"))
            candidates.extend(search_root.rglob("*perturbation_sweep.json"))

    unique = []
    seen = set()

    for path in candidates:
        rp = path.resolve()
        if rp not in seen and rp.exists():
            seen.add(rp)
            unique.append(rp)

    if not unique:
        return None

    unique.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return unique[0]


def load_latest_perturbation_summary(out_root: Any = None, repo_root: Any = None) -> Dict[str, Any]:
    path = find_latest_perturbation_evidence(out_root=out_root, repo_root=repo_root)

    if path is None:
        return {
            "available": False,
            "path": None,
            "status": "missing",
            "score": 0.0,
        }

    data = _safe_load_json(path) or {}

    score = data.get("perturbation_score")
    status = data.get("status")

    if score is None and isinstance(data.get("response_checks"), dict):
        checks = data.get("response_checks", {})
        score = sum(1.0 for value in checks.values() if value is True) / max(len(checks), 1)

    if status is None:
        status = "pass" if clamp01(score) >= 1.0 else "warning" if clamp01(score) >= 0.75 else "fail"

    return {
        "available": True,
        "path": str(path),
        "status": str(status),
        "score": clamp01(score),
        "run_id": data.get("run_id"),
        "operator": data.get("operator") or data.get("perturbation_operator"),
        "response_checks": data.get("response_checks", {}),
        "measurements": data.get("measurements", {}),
        "raw": data,
    }


def _normalize_reasons(reasons: Any) -> list[str]:
    if reasons is None:
        return []
    if isinstance(reasons, list):
        return [str(r) for r in reasons if str(r).strip()]
    if isinstance(reasons, str):
        return [reasons]
    return [str(reasons)]


def _dedupe(seq: Iterable[str]) -> list[str]:
    out = []
    seen = set()
    for item in seq:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def integrate_perturbation_if_available(
    result: Dict[str, Any],
    out_root: Any = None,
    repo_root: Any = None,
    require_pass: bool = True,
) -> Dict[str, Any]:
    if not isinstance(result, dict):
        return result

    summary = load_latest_perturbation_summary(out_root=out_root, repo_root=repo_root)
    updated = dict(result)

    updated["perturbation_sweep_available"] = bool(summary.get("available"))
    updated["perturbation_sweep_status"] = summary.get("status")
    updated["perturbation_sweep_score"] = clamp01(summary.get("score", 0.0))
    updated["perturbation_sweep_evidence"] = summary.get("path")
    updated["perturbation_sweep_integrated"] = False

    locks = dict(updated.get("non_claim_locks") or {})
    locks["perturbation_sweep_is_not_code_correctness"] = True
    locks["fixture_response_is_not_universal_validation"] = True
    locks["omega_recovery_is_not_truth"] = True
    locks["cifscore_is_not_truth"] = True
    locks["cif6_ready_is_not_cif8"] = True
    updated["non_claim_locks"] = locks

    reasons = _normalize_reasons(updated.get("downgrade_reason"))

    score = clamp01(summary.get("score", 0.0))
    status = str(summary.get("status", "missing")).lower()
    passed = bool(summary.get("available")) and (status == "pass") and (score >= 1.0 if require_pass else score > 0.0)

    if passed:
        updated["perturbation_sweep_integrated"] = True

        reasons = [
            r for r in reasons
            if r not in {
                NO_PERTURBATION_REASON,
                ROOTMIRROR_OLD_REASON,
                "Perturbation sweep failed or incomplete.",
            }
        ]

        if ROOTMIRROR_LITE_REASON not in reasons:
            reasons.append(ROOTMIRROR_LITE_REASON)

        if TESSERACT_REASON not in reasons:
            reasons.append(TESSERACT_REASON)

        updated["downgrade_reason"] = _dedupe(reasons)

        previous_maturity = str(updated.get("maturity", ""))
        if previous_maturity in {"", "CIF4", "CIF5", "CIF5-ready"}:
            updated["maturity_base_before_perturbation"] = previous_maturity or None
            updated["maturity"] = "CIF6-ready"

        updated["classification"] = updated.get("classification") or "CIF-B"
        if updated["classification"] in {"CIF-A", "CIF8"}:
            updated["classification"] = "CIF-B"

        updated["maturity_note"] = (
            "Perturbation sweep passed and was integrated; full RootMirror and "
            "Tesseract indexing remain deferred."
        )

        if "cif_score_integrated" not in updated:
            updated["cif_score_integrated"] = updated.get("cif_score")

    else:
        if NO_PERTURBATION_REASON not in reasons:
            reasons.insert(0, NO_PERTURBATION_REASON)
        updated["downgrade_reason"] = _dedupe(reasons)

    return updated


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Integrate latest CIK v0.3 perturbation evidence into a result JSON.")
    parser.add_argument("--result", required=True, help="Path to a result JSON file.")
    parser.add_argument("--out", default=None, help="Output/artifact root.")
    parser.add_argument("--repo", default=None, help="Repository root.")
    parser.add_argument("--write", action="store_true", help="Rewrite result file in-place.")
    args = parser.parse_args()

    result_path = Path(args.result).resolve()
    data = _safe_load_json(result_path)
    if data is None:
        raise SystemExit(f"Could not load JSON result: {result_path}")

    updated = integrate_perturbation_if_available(data, out_root=args.out, repo_root=args.repo)

    if args.write:
        result_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")

    print(json.dumps(updated, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())