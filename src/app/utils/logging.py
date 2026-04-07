from __future__ import annotations

import logging
import sys
from pathlib import Path

from app.const.app import APP_NAME

_logger = logging.getLogger(APP_NAME)


def setup_logger(
    level: int = logging.WARNING, log_save_path: Path | None = None
) -> None:

    _format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    _logger.setLevel(level)

    # stream
    _stream_handler = logging.StreamHandler(sys.stdout)
    _stream_handler.setLevel(level)
    _stream_handler.setFormatter(_format)
    _logger.addHandler(_stream_handler)

    if log_save_path:
        if log_save_path.is_dir():
            log_save_path = log_save_path / "logs.log"
        _file_handler = logging.FileHandler(log_save_path, "w")
        _file_handler.setLevel(level)
        _file_handler.setFormatter(_format)
        _logger.addHandler(_file_handler)


def get_logger() -> logging.Logger:
    return _logger
