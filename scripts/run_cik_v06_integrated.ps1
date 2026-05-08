$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Push-Location $Root

try {
    $env:PYTHONPATH = ".\src"

    Write-Host "════════════════════════════════════════════════════════════"
    Write-Host " CIK v0.6 Integrated Smoke"
    Write-Host "════════════════════════════════════════════════════════════"

    Write-Host ""
    Write-Host "Running RootMirror Full smoke..."
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_rootmirror_full.ps1"

    if ($LASTEXITCODE -ne 0) {
        throw "RootMirror Full smoke failed."
    }

    Write-Host ""
    Write-Host "Running v0.6 unit surfaces..."
    python -m unittest tests.test_v06_rootmirror_full_scoring_integration -v
    if ($LASTEXITCODE -ne 0) {
        throw "v0.6 RootMirror scoring tests failed."
    }

    python -m unittest tests.test_v06_downgrade_reconciliation -v
    if ($LASTEXITCODE -ne 0) {
        throw "v0.6 downgrade reconciliation tests failed."
    }

    python -m unittest tests.test_v06_instrument_registry_contract -v
    if ($LASTEXITCODE -ne 0) {
        throw "v0.6 registry tests failed."
    }

    Write-Host ""
    Write-Host "Running full suite..."
    python -m unittest discover -s tests

    if ($LASTEXITCODE -ne 0) {
        throw "Full unit suite failed."
    }

    Write-Host ""
    Write-Host "CIK v0.6 integrated smoke passed."
}
finally {
    Pop-Location
}