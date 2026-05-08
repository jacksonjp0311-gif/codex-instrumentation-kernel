$ErrorActionPreference = "Stop"

$Root = "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"

Push-Location $Root
try {
    $env:PYTHONPATH = Join-Path $Root "src"
    python ".\scripts\run_cik_v04_integrated.py"
}
finally {
    Pop-Location
}