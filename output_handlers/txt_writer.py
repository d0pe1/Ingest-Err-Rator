
from __future__ import annotations
import os
from typing import Dict
from ..utils.file_utils import ensure_dir, safe_filename

class TxtWriter:
    def __init__(self, out_dir: str):
        self.out = out_dir
        ensure_dir(self.out)

    def write(self, source_path: str, parsed: Dict):
        base = os.path.splitext(os.path.basename(source_path))[0]
        fn = os.path.join(self.out, safe_filename(base) + ".txt")
        with open(fn, "w", encoding="utf-8") as f:
            f.write(parsed.get("content",""))
