$ErrorActionPreference = "Stop"

$Root = "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"

Push-Location $Root
try {
    $env:PYTHONPATH = ".\src"
    python ".\scripts\run_perturbation_sweep.py" --fixture ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs" --operator "missing_path"
}
finally {
    Pop-Location
}