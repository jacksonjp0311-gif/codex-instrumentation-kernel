# CIK v1.0 Validation Surface

Required local validation:

    $env:PYTHONPATH = ".\src"
    python -m unittest tests.test_rcc_readmes -v
    python -m unittest discover -s tests
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v09_tesseract_dashboard.ps1"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v08_evidence_graph.ps1"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v07_orchestration.ps1"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v06_integrated.ps1"
    powershell -ExecutionPolicy Bypass -File ".\scripts\run_cik_v1_0_release_lock.ps1"
    git status --short

Passing these checks means the local validation surface passed. It is not formal verification.