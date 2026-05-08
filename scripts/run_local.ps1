$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    $env:PYTHONPATH = Join-Path $Root "src"
    python -m cik run --instrument rcc-drift --repo ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs"
}
finally {
    Pop-Location
}