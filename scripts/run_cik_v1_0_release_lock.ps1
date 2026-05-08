$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root

try {
    $env:PYTHONPATH = ".\src"

    Write-Host "============================================================"
    Write-Host " CIK v1.0 Stable Local-First Release Lock"
    Write-Host "============================================================"

    Write-Host ""
    Write-Host "Running v0.9 dashboard/Tesseract smoke..."
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v09_tesseract_dashboard.ps1"
    if ($LASTEXITCODE -ne 0) { throw "v0.9 smoke failed." }

    Write-Host ""
    Write-Host "Building v1.0 release lock..."
    python -m cik.release lock --repo-root "." --out ".\outputs"
    if ($LASTEXITCODE -ne 0) { throw "v1.0 release lock failed." }

    Write-Host ""
    Write-Host "Checking v1.0 release checklist..."
    python -m cik.release checklist --repo-root "." --out ".\outputs"
    if ($LASTEXITCODE -ne 0) { throw "v1.0 release checklist failed." }

    Write-Host ""
    Write-Host "Checking v1.0 non-claim locks..."
    python -m cik.release locks --repo-root "." --out ".\outputs"
    if ($LASTEXITCODE -ne 0) { throw "v1.0 non-claim locks failed." }

    Write-Host ""
    Write-Host "Checking v1.0 validation surface..."
    python -m cik.release validate --repo-root "." --out ".\outputs"
    if ($LASTEXITCODE -ne 0) { throw "v1.0 validation surface failed." }

    Write-Host ""
    Write-Host "CIK v1.0 release lock smoke passed."
}
finally {
    Pop-Location
}