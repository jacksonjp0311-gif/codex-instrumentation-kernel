from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from cik.tesseract.index import write_tesseract_index


def write_index(output_root: str | Path) -> Dict[str, Any]:
    return write_tesseract_index(Path(output_root))