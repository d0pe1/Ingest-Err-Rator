
from __future__ import annotations
import sys, os, time

COL = {
    "reset": "\033[0m",
    "info": "\033[36m",
    "warn": "\033[33m",
    "error": "\033[31m",
    "success": "\033[32m",
}

class Logger:
    def __init__(self, log_file: str="ingestion.log", coco_mode: bool=False):
        self.log_file = log_file
        self.coco = coco_mode

    def _fmt(self, level: str, msg: str) -> str:
        if self.coco and level == "error":
            msg = "me no worky, brain hurty"
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{ts}] {msg}"

    def _out(self, level: str, msg: str):
        c = COL.get(level, "")
        print(f"{c}{msg}{COL['reset']}")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    def info(self, msg: str): self._out("info", self._fmt("info", msg))
    def warn(self, msg: str): self._out("warn", self._fmt("warn", msg))
    def error(self, msg: str): self._out("error", self._fmt("error", msg))
    def success(self, msg: str): self._out("success", self._fmt("success", msg))

def get_logger(coco_mode: bool=False) -> Logger:
    return Logger(coco_mode=coco_mode)
