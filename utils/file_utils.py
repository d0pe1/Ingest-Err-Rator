
from __future__ import annotations
import os, re
from typing import Iterable, List, Set

def find_files(source: str, extensions: Set[str], recursive: bool=True) -> List[str]:
    exts = {e.lower().lstrip('.') for e in extensions}
    matches: List[str] = []
    if recursive:
        for root, _, files in os.walk(source):
            for f in files:
                if os.path.splitext(f)[1].lower().lstrip('.') in exts:
                    matches.append(os.path.join(root, f))
    else:
        for f in os.listdir(source):
            p = os.path.join(source, f)
            if os.path.isfile(p) and os.path.splitext(f)[1].lower().lstrip('.') in exts:
                matches.append(p)
    return matches

def safe_filename(name: str) -> str:
    name = re.sub(r'[^A-Za-z0-9._-]+', '_', name).strip('_')
    return name or "unnamed"

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)
