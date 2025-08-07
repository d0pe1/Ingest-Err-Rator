
from __future__ import annotations
from typing import Dict
import os
from ..base_parser import BaseParser
from ..utils.text_utils import normalize_ws

class TxtParser(BaseParser):
    supported_extensions = ["txt"]

    def parse(self, file_path: str) -> Dict:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        content = normalize_ws(content)
        meta = {
            "source_file": file_path,
            "parser_name": "TxtParser",
            "word_count": len(content.split()),
            "char_count": len(content),
        }
        return {"content": content, "metadata": meta}
