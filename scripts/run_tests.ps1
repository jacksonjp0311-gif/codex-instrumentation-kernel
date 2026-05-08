$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    $env:PYTHONPATH = Join-Path $Root "src"
    python -m unittest discover -s tests
}
finally {
    Pop-Location
}