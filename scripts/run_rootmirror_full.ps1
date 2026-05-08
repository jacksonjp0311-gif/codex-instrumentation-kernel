$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root

try {
    $env:PYTHONPATH = ".\src"

    Write-Host "════════════════════════════════════════════════════════════"
    Write-Host " CIK v0.5 RootMirror Full Integrated Smoke"
    Write-Host "════════════════════════════════════════════════════════════"

    python -m cik.rootmirror_full --repo-root "." --out ".\outputs" --target-repo ".\tests\fixtures\tiny_repo_with_context"

    if ($LASTEXITCODE -ne 0) {
        throw "RootMirror full smoke failed."
    }

    Write-Host ""
    Write-Host "RootMirror full smoke passed."
}
finally {
    Pop-Location
}