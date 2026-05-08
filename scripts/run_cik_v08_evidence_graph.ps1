$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root

try {
    $env:PYTHONPATH = ".\src"

    Write-Host "============================================================"
    Write-Host " CIK v0.8 Evidence Graph Smoke"
    Write-Host "============================================================"

    Write-Host ""
    Write-Host "Running v0.7 orchestration first to ensure fresh artifacts..."
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v07_orchestration.ps1"

    if ($LASTEXITCODE -ne 0) {
        throw "v0.7 orchestration compatibility smoke failed."
    }

    Write-Host ""
    Write-Host "Building evidence graph..."
    python -m cik.evidence_graph build --out ".\outputs"

    if ($LASTEXITCODE -ne 0) {
        throw "Evidence graph build failed."
    }

    Write-Host ""
    Write-Host "Querying runs..."
    python -m cik.evidence_graph query --out ".\outputs" --kind runs

    if ($LASTEXITCODE -ne 0) {
        throw "Evidence graph runs query failed."
    }

    Write-Host ""
    Write-Host "Querying downgrades..."
    python -m cik.evidence_graph query --out ".\outputs" --kind downgrades

    if ($LASTEXITCODE -ne 0) {
        throw "Evidence graph downgrades query failed."
    }

    Write-Host ""
    Write-Host "Querying claim evidence..."
    python -m cik.evidence_graph query --out ".\outputs" --kind claim-evidence --claim "orchestration_is_not_correctness"

    if ($LASTEXITCODE -ne 0) {
        throw "Evidence graph claim-evidence query failed."
    }

    Write-Host ""
    Write-Host "CIK v0.8 evidence graph smoke passed."
}
finally {
    Pop-Location
}