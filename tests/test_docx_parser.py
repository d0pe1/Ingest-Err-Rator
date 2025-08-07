
import os, zipfile, tempfile, xml.etree.ElementTree as ET
from doc_ingestion_engine.parsers.docx_parser import DocxParser, NS

def _make_min_docx(path: str):
    # word/document.xml
    doc = ET.Element(f'{{{NS["w"]}}}document')
    body = ET.SubElement(doc, f'{{{NS["w"]}}}body')
    # heading
    p1 = ET.SubElement(body, f'{{{NS["w"]}}}p')
    pPr = ET.SubElement(p1, f'{{{NS["w"]}}}pPr')
    s = ET.SubElement(pPr, f'{{{NS["w"]}}}pStyle')
    s.set(f'{{{NS["w"]}}}val', 'Heading1')
    r1 = ET.SubElement(p1, f'{{{NS["w"]}}}r')
    t1 = ET.SubElement(r1, f'{{{NS["w"]}}}t')
    t1.text = "Title"
    # paragraph
    p2 = ET.SubElement(body, f'{{{NS["w"]}}}p')
    r2 = ET.SubElement(p2, f'{{{NS["w"]}}}r')
    t2 = ET.SubElement(r2, f'{{{NS["w"]}}}t')
    t2.text = "Hello world"
    doc_xml = ET.tostring(doc, encoding="utf-8", xml_declaration=True)

    # core.xml
    cp = ET.Element(f'{{{NS["cp"]}}}coreProperties')
    au = ET.SubElement(cp, f'{{{NS["dc"]}}}creator'); au.text = "Nico"
    ti = ET.SubElement(cp, f'{{{NS["dc"]}}}title'); ti.text = "Test Doc"
    core_xml = ET.tostring(cp, encoding="utf-8", xml_declaration=True)

    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", doc_xml)
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("docProps/core.xml", core_xml)

def test_parse_docx(tmp_path):
    fp = os.path.join(tmp_path, "t.docx")
    _make_min_docx(fp)
    parser = DocxParser()
    out = parser.parse(fp)
    assert "## Title" in out["content"]
    assert "Hello world" in out["content"]
    assert out["metadata"]["author"] == "Nico"
