
from __future__ import annotations
import os, yaml
from typing import Dict
from ..utils.file_utils import ensure_dir, safe_filename

class MdWriter:
    def __init__(self, out_dir: str):
        self.out = out_dir
        ensure_dir(self.out)

    def write(self, source_path: str, parsed: Dict):
        base = os.path.splitext(os.path.basename(source_path))[0]
        fn = os.path.join(self.out, safe_filename(base) + ".md")
        meta = parsed.get("metadata", {})
        content = parsed.get("content","")
        with open(fn, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(yaml.safe_dump(meta, sort_keys=False))
            f.write("---\n\n")
            f.write(content)
