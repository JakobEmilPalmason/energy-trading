"""Paths and credential loading.

Data lives outside the package, under the repo's gitignored `data/` dir. The
ENTSO-E token is read from `.env` (never committed) via python-dotenv.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# src/energy_markets/config.py -> parents[2] == repo root (editable install).
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.environ.get("NORDIC_POWER_DATA_DIR", REPO_ROOT / "data"))
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

load_dotenv(REPO_ROOT / ".env")


def ensure_data_dirs() -> None:
    """Create data/raw and data/processed if absent (they're gitignored)."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def get_entsoe_api_key() -> str:
    """Return the ENTSO-E API token, or raise a helpful error if unset."""
    key = os.environ.get("ENTSOE_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "ENTSOE_API_KEY is not set. Copy .env.example to .env and add your token "
            "(see docs/sources/entsoe.md)."
        )
    return key
