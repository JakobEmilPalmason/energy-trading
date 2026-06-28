"""Tiny parquet cache so public endpoints aren't re-hit on every run.

Cached files live under data/raw/<relpath>. Delete the file (or pass refresh=True)
to force a re-fetch.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from energy_markets.config import RAW_DIR


def cached_parquet(
    relpath: str,
    fetch: Callable[[], pd.DataFrame],
    *,
    refresh: bool = False,
) -> pd.DataFrame:
    """Return cached parquet at data/raw/<relpath>, else call ``fetch`` and cache it."""
    path = RAW_DIR / relpath
    if path.exists() and not refresh:
        return pd.read_parquet(path)
    df = fetch()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path)
    return df
