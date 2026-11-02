"""Configurazione del logging: ogni modulo usa get_logger(__name__)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path


class _Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.short = record.name.replace("gtd_pipeline.", "")
        return super().format(record)


def setup_logging(level: int = logging.INFO, log_file: Path | None = None) -> None:
    root = logging.getLogger("gtd_pipeline")
    root.setLevel(level)
    root.handlers.clear()
    root.propagate = False

    fmt = _Formatter("%(asctime)s  %(levelname)-7s %(short)-22s %(message)s", "%H:%M:%S")

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    root.addHandler(console)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setFormatter(
            _Formatter("%(asctime)s  %(levelname)-7s %(name)s  %(message)s")
        )
        root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
