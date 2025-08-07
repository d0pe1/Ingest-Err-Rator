
from __future__ import annotations
import importlib, inspect, pkgutil
from typing import Dict, Type
from .base_parser import BaseParser
from . import parsers as parsers_pkg

class ParserRegistry:
    def __init__(self, logger=None):
        self.logger = logger
        self._by_ext: Dict[str, BaseParser] = {}
        self._discover()

    def _discover(self):
        for m in pkgutil.iter_modules(parsers_pkg.__path__):
            if not m.name.endswith('_parser'):
                continue
            module = importlib.import_module(f"{parsers_pkg.__name__}.{m.name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseParser) and obj is not BaseParser:
                    inst: BaseParser = obj()
                    for ext in inst.supported_extensions:
                        ext = ext.lower()
                        if ext in self._by_ext and self.logger:
                            self.logger.warn(f"Multiple parsers for .{ext}; keeping {self._by_ext[ext].__class__.__name__}, ignoring {obj.__name__}")
                        else:
                            self._by_ext[ext] = inst

    def get_for(self, file_path: str) -> BaseParser | None:
        import os
        return self._by_ext.get(os.path.splitext(file_path)[1].lower().lstrip('.'))

    def list(self) -> Dict[str, str]:
        return {ext: p.__class__.__name__ for ext, p in sorted(self._by_ext.items())}
