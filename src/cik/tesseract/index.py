from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import hashlib
import json
import re

from cik.tesseract.models import ArtifactRecord, RunRecord


FULL_ROOTMIRROR_REASON = "Full RootMirror verification not enabled; RootMirror-lite local continuity only."
TESSERACT_MISSING_REASON = "Tesseract indexing not enabled."


def clamp01(x: Any) -> float:
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def load_json_if_possible(path: Path) -> Optional[Dict[str, Any]]:
    try:
        if path.suffix.lower() != ".json":
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def infer_artifact_type(path: Path) -> str:
    text = str(path).replace("\\", "/").lower()
    name = path.name.lower()

    if "/tesseract/" in text:
        return "tesseract"
    if "/rootmirror/" in text or "rootmirror" in name:
        return "rootmirror"
    if "/perturbation/" in text or "perturbation" in name:
        return "perturbation"
    if "/injection/" in text or "injection" in name:
        return "injection"
    if "/state/" in text or name.endswith("_state.json"):
        return "state"
    if "/ledger/" in text or name.endswith("ledger.jsonl"):
        return "ledger"
    if "/evidence/" in text or "evidence_package" in name:
        return "evidence"
    if "/reports/" in text or name.endswith("_report.md") or "drift_report" in name:
        return "report"
    if "/semantic/" in text or name.endswith("_summary.md"):
        return "semantic"
    return "unknown"


def extract_run_id(path: Path, data: Optional[Dict[str, Any]] = None) -> Optional[str]:
    if data and isinstance(data.get("run_id"), str) and data["run_id"].strip():
        return data["run_id"].strip()

    name = path.name

    patterns = [
        r"^(?P<run>.+?)_state\.json$",
        r"^(?P<run>.+?)_evidence_package\.json$",
        r"^(?P<run>.+?)_perturbation_evidence_package\.json$",
        r"^(?P<run>.+?)_drift_report\.md$",
        r"^(?P<run>.+?)_summary\.md$",
        r"^(?P<run>.+?)_rootmirror_lite\.json$",
        r"^(?P<run>.+?)_rootmirror_lite_report\.md$",
        r"^(?P<run>.+?)_perturbation_sweep\.json$",
        r"^(?P<run>.+?)_perturbation_sweep_report\.md$",
    ]

    for pattern in patterns:
        match = re.match(pattern, name)
        if match:
            return match.group("run")

    return None


def _iter_artifact_files(output_root: Path) -> Iterable[Path]:
    if not output_root.exists():
        return []

    skip_names = {
        "tesseract_lite_index.json",
        "tesseract_lite_index.md",
        "tesseract_lite_evidence_package.json",
    }

    files = []
    for path in output_root.rglob("*"):
        if not path.is_file():
            continue
        if path.name in skip_names:
            continue
        if path.suffix.lower() not in {".json", ".jsonl", ".md", ".txt"}:
            continue
        files.append(path)
    return files


def discover_artifacts(output_root: Path) -> List[ArtifactRecord]:
    output_root = Path(output_root).resolve()
    records: List[ArtifactRecord] = []

    for path in _iter_artifact_files(output_root):
        data = load_json_if_possible(path)
        run_id = extract_run_id(path, data=data)
        artifact_type = infer_artifact_type(path)

        try:
            relative_path = str(path.relative_to(output_root))
        except Exception:
            relative_path = str(path)

        records.append(
            ArtifactRecord(
                artifact_type=artifact_type,
                path=str(path),
                relative_path=relative_path,
                exists=path.exists(),
                size_bytes=path.stat().st_size if path.exists() else 0,
                sha256=sha256_file(path) if path.exists() else None,
                run_id=run_id,
            )
        )

    records.sort(key=lambda r: (r.run_id or "", r.artifact_type, r.path))
    return records


def _first_present(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def _collect_json_metrics(path: Path) -> Dict[str, Any]:
    data = load_json_if_possible(path) or {}
    metrics = {}

    metrics["instrument"] = data.get("instrument")
    metrics["dphi_global"] = _first_present(data.get("dphi_global"), data.get("delta_phi"), data.get("DeltaPhi"))
    metrics["omega_mean"] = _first_present(data.get("omega_mean"), data.get("omega"), data.get("Omega"))
    metrics["cif_score"] = _first_present(data.get("cif_score"), data.get("cif_score_integrated"))
    metrics["maturity"] = data.get("maturity")
    metrics["classification"] = data.get("classification")

    if isinstance(data.get("downgrade_reason"), list):
        metrics["downgrade_reason"] = data.get("downgrade_reason")

    if isinstance(data.get("non_claim_locks"), dict):
        metrics["non_claim_locks"] = data.get("non_claim_locks")

    return metrics


def group_by_run(artifacts: List[ArtifactRecord]) -> List[RunRecord]:
    grouped: Dict[str, List[ArtifactRecord]] = {}
    unbound: List[ArtifactRecord] = []

    for artifact in artifacts:
        if artifact.run_id:
            grouped.setdefault(artifact.run_id, []).append(artifact)
        else:
            unbound.append(artifact)

    run_records: List[RunRecord] = []

    for run_id, items in grouped.items():
        record = RunRecord(
            run_id=run_id,
            non_claim_locks={
                "tesseract_lite_is_not_memory_agency": True,
                "artifact_indexing_is_not_truth": True,
                "index_presence_is_not_correctness": True,
                "hash_presence_is_not_correctness": True,
                "run_linkage_is_not_provenance": True,
                "cif7_ready_is_not_cif8": True,
            },
        )

        for artifact in items:
            key = artifact.artifact_type
            if key in record.artifacts:
                key = f"{artifact.artifact_type}_{len(record.artifacts) + 1}"

            record.artifacts[key] = artifact.path
            if artifact.sha256:
                record.artifact_hashes[key] = artifact.sha256

            if Path(artifact.path).suffix.lower() == ".json":
                metrics = _collect_json_metrics(Path(artifact.path))
                record.instrument = _first_present(metrics.get("instrument"), record.instrument)
                record.dphi_global = _first_present(record.dphi_global, metrics.get("dphi_global"))
                record.omega_mean = _first_present(record.omega_mean, metrics.get("omega_mean"))
                record.cif_score = _first_present(record.cif_score, metrics.get("cif_score"))
                record.maturity = _first_present(record.maturity, metrics.get("maturity"))
                record.classification = _first_present(record.classification, metrics.get("classification"))

                if metrics.get("downgrade_reason"):
                    record.downgrade_reason = metrics["downgrade_reason"]

                if metrics.get("non_claim_locks"):
                    record.non_claim_locks.update(metrics["non_claim_locks"])

        record.non_claim_locks.update(
            {
                "tesseract_lite_is_not_memory_agency": True,
                "artifact_indexing_is_not_truth": True,
                "index_presence_is_not_correctness": True,
                "hash_presence_is_not_correctness": True,
                "run_linkage_is_not_provenance": True,
                "cif7_ready_is_not_cif8": True,
            }
        )

        run_records.append(record)

    run_records.sort(key=lambda r: r.run_id)
    return run_records


def index_integrity_score(
    json_emitted: bool,
    md_emitted: bool,
    artifacts: List[ArtifactRecord],
    run_records: List[RunRecord],
    locks_preserved: bool,
) -> float:
    hash_coverage = 1.0 if not artifacts else sum(1 for a in artifacts if a.sha256) / len(artifacts)
    run_binding_presence = 1.0 if run_records else 0.0

    return clamp01(
        0.20 * float(json_emitted)
        + 0.15 * float(md_emitted)
        + 0.25 * hash_coverage
        + 0.25 * run_binding_presence
        + 0.15 * float(locks_preserved)
    )


def _artifact_type_counts(artifacts: List[ArtifactRecord]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for artifact in artifacts:
        counts[artifact.artifact_type] = counts.get(artifact.artifact_type, 0) + 1
    return dict(sorted(counts.items()))


def build_tesseract_index(output_root: Path, include_self: bool = False) -> Dict[str, Any]:
    output_root = Path(output_root).resolve()
    artifacts = discover_artifacts(output_root)
    run_records = group_by_run(artifacts)

    index = {
        "schema": "CIK-v0.4-tesseract-lite-index",
        "index_version": "0.4",
        "generated_at": utc_now(),
        "output_root": str(output_root),
        "record_count": len(run_records),
        "artifact_count": len(artifacts),
        "artifact_type_counts": _artifact_type_counts(artifacts),
        "records": [asdict(r) for r in run_records],
        "artifact_records": [asdict(a) for a in artifacts],
        "unbound_artifacts": [asdict(a) for a in artifacts if not a.run_id],
        "non_claim_locks": {
            "tesseract_lite_is_not_full_tesseract": True,
            "tesseract_lite_is_not_memory_agency": True,
            "artifact_indexing_is_not_truth": True,
            "index_presence_is_not_correctness": True,
            "hash_presence_is_not_correctness": True,
            "run_linkage_is_not_provenance": True,
            "cifscore_is_not_truth": True,
        },
    }

    index["hash_coverage"] = 1.0 if not artifacts else sum(1 for a in artifacts if a.sha256) / len(artifacts)
    index["run_binding_presence"] = 1.0 if run_records else 0.0

    return index


def render_markdown(index: Dict[str, Any]) -> str:
    lines = [
        "# Tesseract-lite Index",
        "",
        f"Schema: {index.get('schema')}",
        f"Generated: {index.get('generated_at')}",
        f"Output root: {index.get('output_root')}",
        f"Run records: {index.get('record_count')}",
        f"Artifacts: {index.get('artifact_count')}",
        f"Index integrity score: {index.get('index_integrity_score', 'pending')}",
        f"Maturity: {index.get('maturity', 'pending')}",
        f"Classification: {index.get('classification', 'pending')}",
        "",
        "## Non-claim locks",
        "",
        "- Tesseract-lite is not full Codex Tesseract.",
        "- Tesseract-lite is not autonomous memory.",
        "- Artifact indexing is not truth.",
        "- Hash presence is not correctness.",
        "- Run linkage is not provenance.",
        "- CIFScore is not truth.",
        "",
        "## Artifact type counts",
        "",
    ]

    for key, value in (index.get("artifact_type_counts") or {}).items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Run records", ""])

    for record in index.get("records", []):
        lines.append(f"### {record.get('run_id')}")
        lines.append("")
        lines.append(f"- Instrument: {record.get('instrument')}")
        lines.append(f"- DeltaPhi: {record.get('dphi_global')}")
        lines.append(f"- Omega: {record.get('omega_mean')}")
        lines.append(f"- CIFScore: {record.get('cif_score')}")
        lines.append(f"- Maturity: {record.get('maturity')}")
        lines.append(f"- Classification: {record.get('classification')}")
        lines.append("")
        lines.append("Artifacts:")
        for artifact_type, artifact_path in (record.get("artifacts") or {}).items():
            lines.append(f"- {artifact_type}: `{artifact_path}`")
        lines.append("")

    return "\n".join(lines) + "\n"


def write_tesseract_index(output_root: Path) -> Dict[str, Any]:
    output_root = Path(output_root).resolve()
    tesseract_root = output_root / "tesseract"
    tesseract_root.mkdir(parents=True, exist_ok=True)

    index_json = tesseract_root / "tesseract_lite_index.json"
    index_md = tesseract_root / "tesseract_lite_index.md"
    evidence_json = tesseract_root / "tesseract_lite_evidence_package.json"

    index = build_tesseract_index(output_root)
    index_json.write_text(json.dumps(index, indent=2), encoding="utf-8")

    provisional_md = render_markdown(index)
    index_md.write_text(provisional_md, encoding="utf-8")

    score = index_integrity_score(
        json_emitted=index_json.exists(),
        md_emitted=index_md.exists(),
        artifacts=discover_artifacts(output_root),
        run_records=group_by_run(discover_artifacts(output_root)),
        locks_preserved=True,
    )

    index["index_json"] = str(index_json)
    index["index_markdown"] = str(index_md)
    index["index_integrity_score"] = score
    index["maturity"] = "CIF7-ready" if score >= 1.0 else "CIF6-ready"
    index["classification"] = "CIF-B"
    index["downgrade_reason"] = []

    if score >= 1.0:
        index["downgrade_reason"].append(FULL_ROOTMIRROR_REASON)
    else:
        index["downgrade_reason"].append("Tesseract-lite indexing failed or incomplete.")
        index["downgrade_reason"].append(FULL_ROOTMIRROR_REASON)

    evidence = {
        "schema": "CIK-v0.4-tesseract-lite-evidence",
        "generated_at": utc_now(),
        "index_json": str(index_json),
        "index_markdown": str(index_md),
        "record_count": index.get("record_count", 0),
        "artifact_count": index.get("artifact_count", 0),
        "hash_coverage": index.get("hash_coverage", 0.0),
        "run_binding_presence": index.get("run_binding_presence", 0.0),
        "index_integrity_score": score,
        "claim_boundary": "artifact_indexing_only",
        "non_claim_locks": index["non_claim_locks"],
    }

    evidence_json.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    index["tesseract_lite_evidence"] = str(evidence_json)

    index_json.write_text(json.dumps(index, indent=2), encoding="utf-8")
    index_md.write_text(render_markdown(index), encoding="utf-8")

    return index