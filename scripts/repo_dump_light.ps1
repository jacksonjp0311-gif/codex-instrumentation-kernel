$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    Get-ChildItem -Recurse -File |
      Where-Object {
        $_.FullName -notmatch "\\.git\\" -and
        $_.FullName -notmatch "__pycache__" -and
        $_.FullName -notmatch "\\outputs\\(state|ledger|evidence|reports|semantic)\\"
      } |
      ForEach-Object {
        Write-Host "===== $($_.FullName.Replace($Root, '.')) ====="
        Get-Content $_.FullName -Raw
      }
}
finally {
    Pop-Location
}