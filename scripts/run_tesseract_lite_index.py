from __future__ import annotations

import argparse
import json
from pathlib import Path

from cik.tesseract.index import write_tesseract_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CIK v0.4 Tesseract-lite indexing.")
    parser.add_argument("--out", default="outputs")
    args = parser.parse_args()

    index = write_tesseract_index(Path(args.out))
    print(json.dumps(index, indent=2))

    if index.get("index_integrity_score") != 1.0:
        return 2

    if index.get("maturity") != "CIF7-ready":
        return 3

    locks = index.get("non_claim_locks") or {}
    required_locks = [
        "tesseract_lite_is_not_full_tesseract",
        "tesseract_lite_is_not_memory_agency",
        "artifact_indexing_is_not_truth",
        "index_presence_is_not_correctness",
        "hash_presence_is_not_correctness",
        "run_linkage_is_not_provenance",
    ]

    if not all(locks.get(lock) is True for lock in required_locks):
        return 4

    return 0


if __name__ == "__main__":
    raise SystemExit(main())