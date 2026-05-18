"""Centralised logging configuration for the claims pipeline.

Usage in any module:

    from src.core.logger import get_logger, claim_logger

    # Module-level logger (no claim context)
    log = get_logger("my.module")
    log.info("Server started")

    # Per-claim logger (injects claim_id into every line)
    log = claim_logger("agents.data_validator", claim_id)
    log.info("Member '%s' found", member_name)

Output:
  Console  → INFO+,  human-readable
  File     → DEBUG+, full detail, rotating at 10 MB (5 backups)

Log file location: <project_root>/logs/pipeline.log
"""
from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

# ── paths ─────────────────────────────────────────────────────────────────────

_ROOT = Path(__file__).parent.parent.parent
LOGS_DIR = _ROOT / "logs"

# ── formats ───────────────────────────────────────────────────────────────────

_DATE_FMT = "%Y-%m-%d %H:%M:%S"

_CONSOLE_FMT = (
    "%(asctime)s | %(levelname)-8s | %(name)-30s | [%(claim_id)-8s] %(message)s"
)
_FILE_FMT = (
    "%(asctime)s | %(levelname)-8s | %(name)-30s | [%(claim_id)-8s] %(message)s"
)


# ── filter: ensures claim_id is always present on every LogRecord ─────────────

class _DefaultClaimId(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "claim_id"):
            record.claim_id = "--------"
        return True


# ── setup (idempotent) ────────────────────────────────────────────────────────

_SETUP_DONE = False


def setup_logging(console_level: int = logging.INFO) -> None:
    """Configure the 'claims' logger hierarchy.

    Safe to call multiple times — subsequent calls are no-ops.
    Called automatically by get_logger() so explicit calls are optional.
    """
    global _SETUP_DONE
    if _SETUP_DONE:
        return
    _SETUP_DONE = True

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger("claims")
    root.setLevel(logging.DEBUG)
    root.propagate = False  # don't bleed into uvicorn/streamlit root loggers

    _flt = _DefaultClaimId()

    # ── console handler ───────────────────────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(console_level)
    console.setFormatter(logging.Formatter(_CONSOLE_FMT, datefmt=_DATE_FMT))
    console.addFilter(_flt)
    root.addHandler(console)

    # ── rotating file handler ─────────────────────────────────────────────────
    file_handler = logging.handlers.RotatingFileHandler(
        LOGS_DIR / "pipeline.log",
        maxBytes=10 * 1024 * 1024,   # 10 MB per file
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_FILE_FMT, datefmt=_DATE_FMT))
    file_handler.addFilter(_flt)
    root.addHandler(file_handler)


# ── public helpers ────────────────────────────────────────────────────────────

def get_logger(name: str) -> logging.Logger:
    """Return a named child of the 'claims' hierarchy.

    Args:
        name: Dot-separated sub-name, e.g. 'agents.data_validator'.
              The full logger name will be 'claims.<name>'.
    """
    setup_logging()
    return logging.getLogger(f"claims.{name}")


def claim_logger(name: str, claim_id: str) -> logging.LoggerAdapter:
    """Return a LoggerAdapter that stamps every line with the claim_id.

    Args:
        name:     Sub-name passed to get_logger().
        claim_id: Short claim identifier (e.g. 'A1B2C3D4').
    """
    return logging.LoggerAdapter(get_logger(name), {"claim_id": claim_id})
