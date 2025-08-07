
from __future__ import annotations
from ..base_parser import BaseParser

class PdfParser(BaseParser):
    supported_extensions = ["pdf"]

    def parse(self, file_path: str):
        raise NotImplementedError("lol")
