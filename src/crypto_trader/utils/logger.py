"""표준 라이브러리 기반 간단 로거. 콘솔 + 파일(logs/) 동시 출력."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

_CONFIGURED = False


def _configure_root(level: str = "INFO") -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger("crypto_trader")
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    root.propagate = False

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    root.addHandler(console)

    file_handler = logging.FileHandler(log_dir / "trader.log", encoding="utf-8")
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)

    _CONFIGURED = True


def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """`crypto_trader.<name>` 네임스페이스 로거 반환."""
    _configure_root(level)
    return logging.getLogger(f"crypto_trader.{name}")
