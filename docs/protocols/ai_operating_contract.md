# AI Operating Contract — CIK v0.1

Before modifying CIK:

1. Read root README.
2. Read `docs/architecture/rcc_context_map.md`.
3. Read `docs/context/repository_context_index.json`.
4. Read target folder README.
5. Inspect relevant code/tests/configs only.
6. Patch the smallest necessary surface.
7. Run local verification.
8. Preserve non-claim locks.

Required verification:

    $env:PYTHONPATH = ".\src"
    python -m unittest discover -s tests
    python -m unittest tests.test_rcc_readmes -v

If instrument behavior changed:

    python -m cik run --instrument rcc-drift --repo ".\tests\fixtures\tiny_repo_with_context" --out ".\outputs"