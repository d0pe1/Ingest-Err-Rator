
import unittest
from doc_ingestion_engine.registry import ParserRegistry

class TestParserRegistry(unittest.TestCase):
    def test_discovery(self):
        reg = ParserRegistry()
        m = reg.list()
        assert 'docx' in m and 'txt' in m and 'pdf' in m

    def test_get_parser(self):
        reg = ParserRegistry()
        assert reg.get_for("/tmp/file.docx").__class__.__name__ == "DocxParser"
        assert reg.get_for("/tmp/file.txt").__class__.__name__ == "TxtParser"
