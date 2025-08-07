
from __future__ import annotations
import re
from typing import Iterable

def normalize_ws(s: str) -> str:
    s = s.replace('\r', '\n')
    s = re.sub(r'\s+\n', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    s = re.sub(r'[ \t\xa0]+', ' ', s)
    return s.strip()
