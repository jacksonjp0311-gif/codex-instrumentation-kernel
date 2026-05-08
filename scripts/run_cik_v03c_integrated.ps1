$ErrorActionPreference = "Stop"

$Root = "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"

Push-Location $Root
try {
    $env:PYTHONPATH = Join-Path $Root "src"
    python ".\scripts\run_cik_v03c_integrated.py" --repo ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs"
}
finally {
    Pop-Location
}