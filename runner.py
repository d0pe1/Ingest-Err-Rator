
from __future__ import annotations
import argparse, concurrent.futures as cf, os, sys, json, time
from typing import List, Dict
from .registry import ParserRegistry
from .utils.logging_utils import get_logger
from .utils.file_utils import find_files, ensure_dir, safe_filename
from .output_handlers.txt_writer import TxtWriter
from .output_handlers.md_writer import MdWriter
from .output_handlers.json_writer import JsonWriter

def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Modular Document Ingestion Engine")
    ap.add_argument("--source", required=True, help="Input directory")
    ap.add_argument("--output", required=True, help="Output directory")
    ap.add_argument("--formats", default="txt,md,json")
    ap.add_argument("--parser", default=None, help="Force specific parser name")
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--list-parsers", action="store_true")
    ap.add_argument("--coco-mode", action="store_true")
    return ap.parse_args(argv)

def main(argv=None):
    args = parse_args(argv)
    ensure_dir(args.output)
    logger = get_logger(coco_mode=args.coco_mode)
    reg = ParserRegistry(logger=logger)

    if args.list_parsers:
        for ext, name in reg.list().items():
            print(f".{ext}: {name}")
        return 0

    writers = []
    req = {f.strip().lower() for f in args.formats.split(",") if f.strip()}
    if "txt" in req: writers.append(TxtWriter(args.output))
    if "md" in req:  writers.append(MdWriter(args.output))
    if "json" in req: writers.append(JsonWriter(args.output))

    files = find_files(args.source, set(reg.list().keys()), recursive=args.recursive)
    if args.dry_run:
        for f in files: print(f"[DRY] would parse: {f}")
        return 0

    total = 0; failed = 0; failures = []
    t0 = time.time()

    def work(path: str):
        parser = reg.get_for(path)
        if not parser:
            failures.append((path, "no parser"))
            return None
        res = parser.safe_parse(path, logger=logger)
        if not res:
            failures.append((path, "parse error"))
            return None
        for w in writers:
            w.write(path, res)
        return res

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for _ in ex.map(work, files):
            total += 1

    if failures:
        failed = len(failures)
        logger.error(f"Failures:")
        for p, r in failures:
            logger.error(f"  {os.path.basename(p)} -> {r}")

    elapsed = time.time() - t0
    logger.success(f"Processed {total} files, {failed} failed in {elapsed:.2f}s")
    if args.stats:
        # simple stats: total word count
        wc = 0
        # not retaining per-file content here; stats would require accumulation
        logger.info("Stats are basic in this minimal build.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
