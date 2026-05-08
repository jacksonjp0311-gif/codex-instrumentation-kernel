$ErrorActionPreference = "Stop"

$Root = "C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel"

Push-Location $Root
try {
    $env:PYTHONPATH = Join-Path $Root "src"
    python ".\scripts\run_tesseract_lite_index.py" --out ".\outputs"
}
finally {
    Pop-Location
}