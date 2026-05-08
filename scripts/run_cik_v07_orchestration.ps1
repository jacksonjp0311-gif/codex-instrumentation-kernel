$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root

try {
    $env:PYTHONPATH = ".\src"

    Write-Host "============================================================"
    Write-Host " CIK v0.7 Orchestration Smoke"
    Write-Host "============================================================"

    python -m cik.orchestration --repo-root "." --out ".\outputs" --plan ".\configs\orchestration\default_run_plan.json"

    if ($LASTEXITCODE -ne 0) {
        throw "CIK v0.7 orchestration smoke failed."
    }

    Write-Host ""
    Write-Host "Running RootMirror Full compatibility smoke..."
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_rootmirror_full.ps1"

    if ($LASTEXITCODE -ne 0) {
        throw "RootMirror Full compatibility smoke failed."
    }

    Write-Host ""
    Write-Host "Running Tesseract-lite compatibility..."
    python -m cik.tesseract --out ".\outputs"

    if ($LASTEXITCODE -ne 0) {
        throw "Tesseract-lite compatibility failed."
    }

    Write-Host ""
    Write-Host "CIK v0.7 orchestration smoke passed."
}
finally {
    Pop-Location
}