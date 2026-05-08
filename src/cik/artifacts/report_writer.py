from __future__ import annotations


def build_drift_report(state: dict) -> str:
    geometry = state.get("geometry", {})
    cif = state.get("cif", {})
    drift = state.get("drift_components", {})

    lines = [
        "# CIK RCC Drift Report",
        "",
        f"Instrument: {state.get('instrument')}",
        f"Run ID: {state.get('run_id')}",
        "",
        "## Metrics",
        "",
        f"- DeltaPhi_repo: {geometry.get('dphi_global')}",
        f"- Omega_repo: {geometry.get('omega_mean')}",
        f"- CIFScore: {cif.get('cif_score')}",
        f"- Maturity: {cif.get('maturity_level')}",
        f"- Classification: {cif.get('classification')}",
        "",
        "## Drift Components",
        "",
    ]

    for key, value in drift.items():
        lines.append(f"- {key}: {value}")

    lines.extend([
        "",
        "## Downgrade",
        "",
    ])

    for reason in cif.get("downgrade_reason", []):
        lines.append(f"- {reason}")

    lines.extend([
        "",
        "## Non-Claims",
        "",
        "- RCC drift is not code correctness.",
        "- CIFScore is not truth.",
        "- Coherence is not truth.",
    ])

    return "\n".join(lines) + "\n"