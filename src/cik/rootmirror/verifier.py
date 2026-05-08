from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import hashlib
import json

REQUIRED_ARTIFACTS = ["state", "ledger", "evidence", "report", "semantic"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    if not text:
        return 0
    return len(text.splitlines())


def verify_artifacts(artifacts: Dict[str, str]) -> Dict[str, Any]:
    records: Dict[str, Dict[str, Any]] = {}
    ok_count = 0

    for key in REQUIRED_ARTIFACTS:
        raw = artifacts.get(key, "")
        exists = bool(raw) and Path(raw).exists()
        records[key] = {"path": raw, "exists": exists}
        if exists:
            ok_count += 1

    score = ok_count / len(REQUIRED_ARTIFACTS)

    return {
        "required": records,
        "artifact_emission_score": score,
        "artifact_manifest_ok": score == 1.0,
    }


def rootmirror_lite_verify(
    repo_root: str,
    run_result: Dict[str, Any],
    ledger_count_before: int,
    cwd_pre: str,
) -> Dict[str, Any]:
    root = Path(repo_root).resolve()
    cwd_post = str(Path.cwd().resolve())
    artifacts = run_result.get("artifacts", {}) or {}

    manifest = verify_artifacts(artifacts)

    state_raw = artifacts.get("state", "")
    state_path = Path(state_raw) if state_raw else Path("__missing_state__")
    state_exists = state_raw != "" and state_path.exists()

    state_hash = {
        "algorithm": "sha256",
        "state_path": state_raw,
        "computed": state_exists,
        "sha256": sha256_file(state_path) if state_exists else "",
    }

    ledger_raw = artifacts.get("ledger", "")
    ledger_path = Path(ledger_raw) if ledger_raw else Path("__missing_ledger__")
    ledger_count_after = line_count(ledger_path)
    append_delta = ledger_count_after - int(ledger_count_before)
    append_once_ok = append_delta == 1

    return_to_root_ok = (
        Path(cwd_post).resolve() == Path(cwd_pre).resolve()
        or Path(cwd_post).resolve() == root
    )

    checks = {
        "root_anchor_ok": root.exists(),
        "artifact_manifest_ok": bool(manifest["artifact_manifest_ok"]),
        "state_hash_ok": bool(state_hash["computed"] and state_hash["sha256"]),
        "ledger_append_once_ok": bool(append_once_ok),
        "return_to_root_ok": bool(return_to_root_ok),
    }

    score = sum(1.0 for value in checks.values() if value) / len(checks)

    if score == 1.0:
        status = "pass"
    elif score >= 0.75:
        status = "warning"
    else:
        status = "fail"

    return {
        "schema": "CIK-v0.2-rootmirror-lite",
        "run_id": run_result.get("run_id", ""),
        "instrument": run_result.get("instrument", ""),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repo_root": str(root),
        "root_anchor": {
            "repo_root_resolved": str(root),
            "cwd_pre": cwd_pre,
            "cwd_post": cwd_post,
            "return_to_root_ok": return_to_root_ok,
        },
        "artifact_manifest": manifest,
        "state_hash": state_hash,
        "ledger_verification": {
            "ledger_path": ledger_raw,
            "line_count_before": int(ledger_count_before),
            "line_count_after": int(ledger_count_after),
            "append_delta": int(append_delta),
            "append_once_ok": bool(append_once_ok),
        },
        "rootmirror_lite": {
            "score": score,
            "status": status,
            "checks": checks,
            "full_rootmirror_claimed": False,
            "security_proof_claimed": False,
            "code_correctness_claimed": False,
        },
        "non_claim_locks": {
            "rootmirror_lite_is_not_full_rootmirror": True,
            "state_hash_is_not_truth": True,
            "ledger_append_is_not_correctness": True,
            "artifact_existence_is_not_validity": True,
            "continuity_is_not_security": True,
        },
    }


def render_markdown_report(result: Dict[str, Any]) -> str:
    rm = result.get("rootmirror_lite", {})
    checks = rm.get("checks", {})
    ledger = result.get("ledger_verification", {})
    state_hash = result.get("state_hash", {})

    def mark(value: bool) -> str:
        return "PASS" if value else "FAIL"

    rows = []
    for key, record in result.get("artifact_manifest", {}).get("required", {}).items():
        rows.append(f"| {key} | `{record.get('path', '')}` | {mark(bool(record.get('exists')))} |")

    artifact_table = "\n".join(rows)

    return f"""# CIK v0.2 RootMirror-lite Continuity Report

## Status

- **Run ID:** `{result.get('run_id', '')}`
- **Instrument:** `{result.get('instrument', '')}`
- **Status:** `{rm.get('status', 'unknown')}`
- **Score:** `{rm.get('score', 0.0)}`

## Checks

| Check | Result |
|---|---:|
| Root anchor | {mark(bool(checks.get('root_anchor_ok')))} |
| Artifact manifest | {mark(bool(checks.get('artifact_manifest_ok')))} |
| State hash | {mark(bool(checks.get('state_hash_ok')))} |
| Ledger append once | {mark(bool(checks.get('ledger_append_once_ok')))} |
| Return to root | {mark(bool(checks.get('return_to_root_ok')))} |

## Artifact Manifest

| Artifact | Path | Exists |
|---|---|---:|
{artifact_table}

## State Hash

- **Algorithm:** `{state_hash.get('algorithm', 'sha256')}`
- **State path:** `{state_hash.get('state_path', '')}`
- **SHA-256:** `{state_hash.get('sha256', '')}`

## Ledger Verification

- **Ledger path:** `{ledger.get('ledger_path', '')}`
- **Line count before:** `{ledger.get('line_count_before', '')}`
- **Line count after:** `{ledger.get('line_count_after', '')}`
- **Append delta:** `{ledger.get('append_delta', '')}`
- **Append once:** `{mark(bool(ledger.get('append_once_ok')))}`

## Non-Claim Locks

- RootMirror-lite is not full RootMirror.
- State hash is not truth.
- Ledger append is not correctness.
- Artifact existence is not validity.
- Continuity is not security.
"""


def write_rootmirror_outputs(
    result: Dict[str, Any],
    out_dir: str,
    run_id: Optional[str] = None,
) -> Dict[str, str]:
    out_root = Path(out_dir).resolve()
    rm_dir = out_root / "rootmirror"
    rm_dir.mkdir(parents=True, exist_ok=True)

    rid = run_id or result.get("run_id") or "cik_rootmirror_lite"
    json_path = rm_dir / f"{rid}_rootmirror_lite.json"
    md_path = rm_dir / f"{rid}_rootmirror_lite_report.md"

    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown_report(result), encoding="utf-8")

    return {
        "rootmirror_json": str(json_path),
        "rootmirror_markdown": str(md_path),
    }


def inject_rootmirror_into_state(
    state_path: str,
    rootmirror_result: Dict[str, Any],
    rootmirror_paths: Dict[str, str],
) -> None:
    path = Path(state_path)
    if not path.exists():
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return

    rm = rootmirror_result.get("rootmirror_lite", {})
    checks = rm.get("checks", {})

    data["rootmirror_lite"] = {
        "enabled": True,
        "status": rm.get("status", "unknown"),
        "score": rm.get("score", 0.0),
        "root_anchor_ok": checks.get("root_anchor_ok", False),
        "artifact_manifest_ok": checks.get("artifact_manifest_ok", False),
        "state_hash_ok": checks.get("state_hash_ok", False),
        "ledger_append_once_ok": checks.get("ledger_append_once_ok", False),
        "return_to_root_ok": checks.get("return_to_root_ok", False),
        "state_sha256": rootmirror_result.get("state_hash", {}).get("sha256", ""),
        "rootmirror_json": rootmirror_paths.get("rootmirror_json", ""),
        "rootmirror_report": rootmirror_paths.get("rootmirror_markdown", ""),
        "full_rootmirror_claimed": False,
    }

    data.setdefault("non_claim_locks", {})
    data["non_claim_locks"]["rootmirror_lite_is_not_full_rootmirror"] = True
    data["non_claim_locks"]["continuity_is_not_correctness"] = True

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def inject_rootmirror_into_evidence(
    evidence_path: str,
    rootmirror_result: Dict[str, Any],
    rootmirror_paths: Dict[str, str],
) -> None:
    path = Path(evidence_path)
    if not path.exists():
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return

    data["continuity_evidence"] = {
        "rootmirror_lite_json": rootmirror_paths.get("rootmirror_json", ""),
        "rootmirror_lite_report": rootmirror_paths.get("rootmirror_markdown", ""),
        "state_sha256": rootmirror_result.get("state_hash", {}).get("sha256", ""),
        "ledger_append_once_ok": rootmirror_result.get("ledger_verification", {}).get("append_once_ok", False),
        "return_to_root_ok": rootmirror_result.get("root_anchor", {}).get("return_to_root_ok", False),
        "artifact_manifest_ok": rootmirror_result.get("artifact_manifest", {}).get("artifact_manifest_ok", False),
        "rootmirror_lite_status": rootmirror_result.get("rootmirror_lite", {}).get("status", "unknown"),
        "full_rootmirror_claimed": False,
    }

    data.setdefault("non_claim_locks", {})
    data["non_claim_locks"]["rootmirror_lite_is_not_full_rootmirror"] = True
    data["non_claim_locks"]["continuity_is_not_correctness"] = True

    path.write_text(json.dumps(data, indent=2), encoding="utf-8")