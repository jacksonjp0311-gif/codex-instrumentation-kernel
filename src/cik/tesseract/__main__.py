from __future__ import annotations

import argparse
import json
from pathlib import Path

from cik.tesseract.index import write_tesseract_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build CIK v0.4 Tesseract-lite artifact index.")
    parser.add_argument("--out", default="outputs", help="CIK output root to index.")
    args = parser.parse_args()

    index = write_tesseract_index(Path(args.out))
    print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())