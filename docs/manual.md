# Hot-Swappable Modular Document Ingestion Engine – Manual

## 1. Introduction
This tool ingests documents, extracts their content and metadata, and serialises them to output formats.

## 2. Core Concepts
- **BaseParser**: contract class
- **Registry**: discovers and registers parsers
- **Output Handlers**: writers for different formats

## 3. CLI Reference
python -m doc_ingestion_engine.runner [options]

Options:
--source PATH  Input folder
--output PATH  Output folder
--formats txt,md,json  Output formats
--parser NAME  Force specific parser
--recursive    Recurse into subfolders
--workers N    Thread pool size
--dry-run      Only list files
--stats        Print statistics
--list-parsers List parsers
--coco-mode    Funny error messages

## 4. Extending
Add parsers in /parsers or writers in /output_handlers.

## 5. Error Handling
safe_parse ensures errors are logged, not raised.

## 6. Testing
python -m unittest discover -s doc_ingestion_engine/tests -v
