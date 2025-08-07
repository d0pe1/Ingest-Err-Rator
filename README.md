# Hot-Swappable Modular Document Ingestion Engine™

A pluggable, extensible framework for ingesting and normalising document content into multiple output formats.  
Designed for speed, modularity, and "enterprise weapon" adaptability.

## ✨ Features

- **Dynamic parser discovery** – just drop a new parser in `/parsers`, it’s picked up automatically.
- **BaseParser contract** – guarantees consistent interface across all parsers.
- **Multi-format output** – TXT, Markdown (with YAML frontmatter), JSON.
- **CLI runner** – recursive scans, parallel processing, dry-run mode, stats, forced parser selection.
- **Fail-safe execution** – individual parser errors don’t halt the batch.
- **Humorous “coco-mode”** – optional, replaces error messages with `"me no worky, brain hurty"`.
- **Tests included** – for core parser and registry logic.

## 📦 Folder Structure

```
doc_ingestion_engine/
    base_parser.py
    config.yaml
    registry.py
    runner.py
    /parsers
        docx_parser.py
        txt_parser.py
        pdf_parser.py
    /output_handlers
        txt_writer.py
        md_writer.py
        json_writer.py
    /utils
        file_utils.py
        logging_utils.py
        text_utils.py
    /tests
        test_docx_parser.py
        test_registry.py
```

## 🚀 Quickstart

### Install
```bash
pip install pyyaml
```

### Run
```bash
python -m doc_ingestion_engine.runner --source ./data --output ./out --formats txt,md,json --recursive --workers 4 --stats
```

### List Available Parsers
```bash
python -m doc_ingestion_engine.runner --list-parsers
```

### Dry Run
```bash
python -m doc_ingestion_engine.runner --dry-run
```

### Coco Mode
```bash
python -m doc_ingestion_engine.runner --coco-mode
```

## 🧩 Adding a New Parser

1. Create a file `yourformat_parser.py` in `/parsers`.
2. Subclass `BaseParser` and set `supported_extensions`.
3. The registry will auto-load it.

## 🧪 Running Tests
```bash
python -m unittest discover -s doc_ingestion_engine/tests -v
```
