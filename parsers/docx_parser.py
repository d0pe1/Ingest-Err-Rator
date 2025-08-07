
from __future__ import annotations
import os, zipfile, xml.etree.ElementTree as ET
from typing import Dict
from ..base_parser import BaseParser
from ..utils.text_utils import normalize_ws

NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
}

def _get_text(p):
    parts = []
    for r in p.findall('.//w:t', NS):
        parts.append(r.text or '')
    return ''.join(parts)

def _is_heading(p):
    pPr = p.find('w:pPr', NS)
    if pPr is None: return False
    style = pPr.find('w:pStyle', NS)
    if style is None: return False
    val = style.get(f'{{{NS["w"]}}}val') or style.get('w:val')
    return bool(val and val.lower().startswith("heading"))

class DocxParser(BaseParser):
    supported_extensions = ["docx"]

    def parse(self, file_path: str) -> Dict:
        with zipfile.ZipFile(file_path) as z:
            doc_xml = z.read('word/document.xml')
            core = None
            try:
                core = z.read('docProps/core.xml')
            except KeyError:
                pass

        root = ET.fromstring(doc_xml)
        text_lines = []
        for p in root.findall('.//w:p', NS):
            t = _get_text(p).strip()
            if not t:
                continue
            if _is_heading(p):
                text_lines.append(f"## {t}")
            else:
                text_lines.append(t)
        content = normalize_ws("\n".join(text_lines))

        metadata = {
            "source_file": file_path,
            "parser_name": "DocxParser",
            "word_count": len(content.split()),
            "char_count": len(content),
        }

        if core:
            core_root = ET.fromstring(core)
            def g(tag):
                e = core_root.find(tag, NS)
                return e.text if e is not None else None
            metadata.update({
                "author": g('dc:creator'),
                "title": g('dc:title'),
                "created": g('dcterms:created'),
                "last_modified_by": g('cp:lastModifiedBy'),
                "modified": g('dcterms:modified'),
            })

        return {"content": content, "metadata": metadata}
