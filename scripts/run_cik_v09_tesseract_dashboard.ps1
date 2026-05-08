$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root

try {
    $env:PYTHONPATH = ".\src"

    Write-Host "============================================================"
    Write-Host " CIK v0.9 Full Tesseract + Dashboard Smoke"
    Write-Host "============================================================"

    Write-Host ""
    Write-Host "Running v0.8 evidence graph smoke first..."
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v08_evidence_graph.ps1"

    if ($LASTEXITCODE -ne 0) {
        throw "v0.8 evidence graph compatibility smoke failed."
    }

    Write-Host ""
    Write-Host "Building full Tesseract package..."
    python -m cik.tesseract_full build --out ".\outputs"

    if ($LASTEXITCODE -ne 0) {
        throw "Full Tesseract package build failed."
    }

    Write-Host ""
    Write-Host "Building dashboard outputs..."
    python -m cik.tesseract_full dashboard --out ".\outputs"

    if ($LASTEXITCODE -ne 0) {
        throw "Dashboard output build failed."
    }

    Write-Host ""
    Write-Host "Building release-readiness summary..."
    python -m cik.tesseract_full readiness --out ".\outputs"

    if ($LASTEXITCODE -ne 0) {
        throw "Release-readiness summary failed."
    }

    Write-Host ""
    Write-Host "CIK v0.9 full Tesseract + dashboard smoke passed."
}
finally {
    Pop-Location
}