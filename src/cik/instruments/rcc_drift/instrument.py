from __future__ import annotations

from pathlib import Path

from cik.artifacts.report_writer import build_drift_report
from cik.artifacts.writers import write_json, append_jsonl, write_text
from cik.core.classification import classify_cif
from cik.core.locks import NON_CLAIM_LOCKS
from cik.core.maturity import default_v01_maturity
from cik.core.metrics import omega_from_dphi
from cik.core.scoring import cif_score
from cik.evidence.package import build_evidence_package
from cik.injection.register import ensure_default_injection_register
from cik.instruments.base import Instrument
from cik.instruments.rcc_drift.drift_metrics import compute_drift
from cik.instruments.rcc_drift.reference_loader import load_reference
from cik.instruments.rcc_drift.scanner import scan_repo
from cik.utils.hashing import stable_hash
from cik.utils.time import run_stamp, utc_now_iso


class RCCDriftInstrument(Instrument):
    name = "rcc-drift"
    version = "v0.1"

    def anchor(self, context):
        repo_root = Path(context["repo_root"]).resolve()
        out_root = Path(context["out_root"]).resolve()
        return {
            "repo_root": repo_root,
            "out_root": out_root,
            "timestamp": utc_now_iso(),
            "run_id": f"cik_rcc_drift_{run_stamp()}",
        }

    def shape(self, anchored):
        reference = load_reference(anchored["repo_root"])
        observed = scan_repo(anchored["repo_root"])
        anchored["reference"] = reference
        anchored["observed"] = observed
        return anchored

    def measure(self, shaped):
        drift = compute_drift(shaped["repo_root"], shaped["reference"])
        shaped["drift"] = drift
        return shaped

    def weight(self, measured):
        dphi = measured["drift"]["dphi_global"]
        measured["omega_mean"] = omega_from_dphi(dphi)
        return measured

    def stress(self, weighted):
        weighted["stress"] = {
            "perturbation_tested": False,
            "downgrade": "No perturbation sweep yet."
        }
        return weighted

    def classify(self, stressed):
        score = cif_score()
        maturity = default_v01_maturity()
        downgrade = [
            "No perturbation sweep yet.",
            "RootMirror verification not enabled.",
            "Tesseract indexing not enabled."
        ]
        classification = classify_cif(score, maturity, downgrade)

        dphi = stressed["drift"]["dphi_global"]
        omega = stressed["omega_mean"]

        state = {
            "schema": "CIK-v0.1-CIF-state",
            "instrument": self.name,
            "instrument_version": self.version,
            "run_id": stressed["run_id"],
            "timestamp": stressed["timestamp"],
            "domain": {
                "type": "repository",
                "repo_root": str(stressed["repo_root"]),
                "reference": stressed["reference"].get("_reference_path"),
            },
            "geometry": {
                "residual_name": "DeltaPhi_repo",
                "residual_definition": "weighted repository-context drift",
                "dphi_global": dphi,
                "omega_rule": "1/(1+abs(DeltaPhi_repo))",
                "omega_mean": omega,
            },
            "drift_components": stressed["drift"]["components"],
            "coherence": {
                "system_coherence": omega,
                "artifact_coherence": 1.0,
                "codex_coherence": omega * 1.0,
            },
            "cif": {
                "cif_score": score,
                "maturity_level": maturity,
                "classification": classification,
                "downgrade_reason": downgrade,
            },
            "locks": NON_CLAIM_LOCKS,
        }
        state["state_hash"] = stable_hash(state)
        stressed["state"] = state
        return stressed

    def fossilize(self, classified):
        repo_root = classified["repo_root"]
        out_root = classified["out_root"]
        run_id = classified["run_id"]
        state = classified["state"]

        ensure_default_injection_register(repo_root)

        state_path = out_root / "state" / f"{run_id}_state.json"
        ledger_path = out_root / "ledger" / "cik_ledger.jsonl"
        report_path = out_root / "reports" / f"{run_id}_drift_report.md"
        semantic_path = out_root / "semantic" / f"{run_id}_summary.md"
        evidence_path = out_root / "evidence" / f"{run_id}_evidence_package.json"

        write_json(state_path, state)

        ledger_record = {
            "schema": "CIK-v0.1-ledger-record",
            "run_id": run_id,
            "timestamp": state["timestamp"],
            "instrument": self.name,
            "dphi_global": state["geometry"]["dphi_global"],
            "omega_mean": state["geometry"]["omega_mean"],
            "cif_score": state["cif"]["cif_score"],
            "classification": state["cif"]["classification"],
            "state_hash": state["state_hash"],
        }
        append_jsonl(ledger_path, ledger_record)

        report = build_drift_report(state)
        write_text(report_path, report)

        semantic = "\n".join([
            "# CIK Semantic Summary",
            "",
            f"Run ID: {run_id}",
            f"DeltaPhi_repo: {state['geometry']['dphi_global']}",
            f"Omega_repo: {state['geometry']['omega_mean']}",
            f"CIFScore: {state['cif']['cif_score']}",
            f"Maturity: {state['cif']['maturity_level']}",
            f"Class: {state['cif']['classification']}",
            "",
            "This summary is downstream. It does not rewrite upstream metrics.",
            ""
        ])
        write_text(semantic_path, semantic)

        artifact_paths = {
            "state": str(state_path),
            "ledger": str(ledger_path),
            "report": str(report_path),
            "semantic": str(semantic_path),
        }
        evidence = build_evidence_package(state, artifact_paths)
        write_json(evidence_path, evidence)

        return {
            "status": "ok",
            "run_id": run_id,
            "state": state,
            "artifacts": {
                **artifact_paths,
                "evidence": str(evidence_path),
            }
        }

    def interpret(self, indexed):
        state = indexed["state"]
        return {
            "status": indexed["status"],
            "instrument": self.name,
            "run_id": indexed["run_id"],
            "dphi_global": state["geometry"]["dphi_global"],
            "omega_mean": state["geometry"]["omega_mean"],
            "cif_score": state["cif"]["cif_score"],
            "maturity": state["cif"]["maturity_level"],
            "classification": state["cif"]["classification"],
            "downgrade_reason": state["cif"]["downgrade_reason"],
            "artifacts": indexed["artifacts"],
            "non_claim_locks": state["locks"],
        }