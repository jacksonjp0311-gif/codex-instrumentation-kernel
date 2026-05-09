# CIK v1.0 Contract Inspection Report

Generated: 2026-05-09T08:25:40.5743637-04:00
Root: C:\Users\jacks\OneDrive\Desktop\codex-instrumentation-kernel
HEAD: d8c02af02493f7c37c9ee533e4a3921aaddc7060

## Required Files

- [True] .\README.md
  - sha256: 84b65a22f972ec99b6f8eaf10e44e289ba8e3ea81c7c04ea4b26de91f479ba72
- [True] .\docs\context\repository_context_index.json
  - sha256: 616e651147c323d060772e94e7bf1df08d7806fa11b5569173c2bff7038d3457
- [True] .\docs\architecture\rcc_context_map.md
  - sha256: f8c6f69cc6297970379e94890ca6c04ecab50717d1c6f7d7444768a896ecdf4b
- [True] .\docs\protocols\rootmirror_full_contract.md
  - sha256: a2c04411e8580d46c2b77a0f838883dd7b6adbf39dc9d9e61f64f82a797de818
- [True] .\docs\protocols\instrument_plugin_contract.md
  - sha256: abb2936ba80d39190e37a3a44ace2a907077458a8ec56259641efdd2a5514291
- [True] .\docs\protocols\orchestration_contract.md
  - sha256: 28dc9870eb5999799ff66b8efeb36d59ff08c80189b5bb06207b20b1b3223cc5
- [True] .\docs\protocols\evidence_graph_contract.md
  - sha256: a24002fa29dd92f885e5c32ca2e81ea35764b32c4aa8d497c6658c216038c731
- [True] .\docs\protocols\tesseract_full_contract.md
  - sha256: 4fa31ae23a9e45848ce54e201be8fc17dbe4964bd9d164eaa0fe4803a9d2e4df
- [True] .\docs\protocols\dashboard_contract.md
  - sha256: 20b2da1eeb1310ce5b039256335dd55acaaa2ecc2a3135529654d5ce9fb157ce
- [True] .\docs\release\release_notes_v1_0.md
  - sha256: ecde59680ceb55e417368177c5604d826623555aacc0002873039a5f093feca6
- [True] .\docs\release\release_checklist_v1_0.md
  - sha256: f05f4502cf43c985841835dc2996baced9abd64715f2ec298e8d5fd23724ec6c
- [True] .\docs\release\local_install_v1_0.md
  - sha256: d6193ef9ca16b10e9a2b66ea6c426fd57db5464db879b20279018b3903594ced
- [True] .\docs\release\validation_surface_v1_0.md
  - sha256: f8178f2466efbfe98e2a604ebbacc9500d7b7929b8b861ce3c95fb1724216fed
- [True] .\docs\release\non_claim_locks_v1_0.md
  - sha256: 64417a2edf06d50171f91da675c17bfd598e52ab42ee29078d87e316e5c1f0ed
- [True] .\docs\release\output_contract_v1_0.md
  - sha256: ccbfee01e48da2049366015ee0a8ecff04ba70c09e070d93ecbf7714bcb0fd59
- [True] .\src\cik\release\__init__.py
  - sha256: 32b52811cd29048e0b7951094cc124e73a9e9d49364e1ab8eabdb85ac2792b2c
- [True] .\src\cik\release\bundle.py
  - sha256: f57a7fc0d2f81f9356b8ccb6469490f8d6a68fb69480f138bd4c1c598960cb7a
- [True] .\src\cik\release\checklist.py
  - sha256: dd6c8515910ecc0939f2cf09514630917b1b0c30a776a1d3f5d5f9e8b0829a03
- [True] .\src\cik\release\validator.py
  - sha256: 9b559158bc0786389c2d21ec167d2044b66dae5da00938b7718a4dcba222664c
- [True] .\src\cik\release\locks.py
  - sha256: be4ce466fb49f9a3731079d54065d9fb58b45074716acc5a6882e03b120592a2
- [True] .\src\cik\release\writer.py
  - sha256: ca25f921b100cdbca62663c46b15e3cfff722abe57a04d66e29e7fe13b569322
- [True] .\src\cik\release\__main__.py
  - sha256: d510b58f256a5b23a29b5632a88d64dbdefc697dcb97c290add4d3d9643e0d31
- [True] .\scripts\run_cik_v1_0_release_lock.ps1
  - sha256: 86a3e62d3a3cec77f6b10e159da840560a8833f00900e64f78c5875075080c23
- [True] .\outputs\release\release_bundle_v1_0.json
  - sha256: a4d644117fbda0d7beb97ea2b0ecf62f5a83fb7339ab877ecabc8513d635d5e1
- [True] .\outputs\release\release_summary_v1_0.md
  - sha256: 50aeddfba4719d950e5fdc9a786af9439c417bc83477df6417dc93375a32b04e
- [True] .\outputs\release\release_checklist_v1_0.json
  - sha256: 595c900398b6acf12c3543c45140c5e23bf010cdfa800b2c39a302c262ca9251
- [True] .\outputs\release\validation_surface_v1_0.json
  - sha256: c18087ef614a35588256dbf4bbffea46477dd45c7528668b95b4c1116d0682c2
- [True] .\outputs\release\non_claim_locks_v1_0.json
  - sha256: 40e8b70b385d952d8c0a3260b72f382e35dd0112bd700550c8b2bc2685ed9cfd

## README Anchor Check

- present: PART I
- present: HUMAN README
- present: PART II
- present: AI RECONSTRUCTION README
- present: AI operating contract
- present: RCC documentation contract
- present: AI non-claim lock
- present: Required local verification

## Non-Claim Locks Confirmed

- Stable release is not truth.
- Local validation is not formal verification.
- Release bundle is not provenance.
- Git cleanliness is not semantic validity.
- Release notes are not external validation.

## Validation Commands Run

- python -m unittest tests.test_rcc_readmes -v
- python -m unittest tests.test_v10_release_bundle -v
- python -m unittest tests.test_v10_release_checklist -v
- python -m unittest tests.test_v10_release_validator -v
- python -m unittest tests.test_v10_non_claim_locks -v
- python -m unittest tests.test_v10_cli_contract -v
- python -m unittest discover -s tests
- scripts/run_cik_v1_0_release_lock.ps1
- scripts/run_cik_v09_tesseract_dashboard.ps1
- scripts/run_cik_v08_evidence_graph.ps1
- scripts/run_cik_v07_orchestration.ps1
- scripts/run_cik_v06_integrated.ps1