
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List
import os

class BaseParser(ABC):
    """Contract for all parsers."""
    supported_extensions: List[str] = []

    @abstractmethod
    def parse(self, file_path: str) -> Dict:
        """Return {"content": str, "metadata": dict}."""
        raise NotImplementedError

    def validate(self, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        return os.path.isfile(file_path) and (ext in self.supported_extensions)

    def safe_parse(self, file_path: str, logger=None) -> Dict | None:
        try:
            if not self.validate(file_path):
                raise ValueError(f"Validation failed for {file_path}")
            return self.parse(file_path)
        except Exception as e:
            if logger:
                logger.error(f"{self.__class__.__name__} failed on '{os.path.basename(file_path)}'\n        Reason: {e}")
            return None
