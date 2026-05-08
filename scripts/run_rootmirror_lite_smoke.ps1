$ErrorActionPreference = "Stop"
$Root = "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"

Push-Location $Root
try {
    $env:PYTHONPATH = ".\src"
    python ".\scripts\rootmirror_lite_smoke.py" --repo "." --fixture ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs"
}
finally {
    Pop-Location
}