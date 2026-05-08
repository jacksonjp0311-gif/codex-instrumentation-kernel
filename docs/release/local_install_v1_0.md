# CIK v1.0 Local Install and Run

## Requirements

- Windows PowerShell
- Python 3.11+ recommended
- Git

## Local validation

From the repository root:

    $env:PYTHONPATH = ".\src"
    python -m unittest discover -s tests
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v1_0_release_lock.ps1"

## Release lock command

    python -m cik.release lock --repo-root "." --out ".\outputs"

## Non-claim boundary

Local install success is not proof of correctness, security, provenance, or external validity.