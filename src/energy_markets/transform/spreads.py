"""Combine per-zone prices and compute zone spreads. Pure functions only."""

from __future__ import annotations

import pandas as pd


def prices_to_wide(prices_by_zone: dict[str, pd.Series | pd.DataFrame]) -> pd.DataFrame:
    """Combine per-zone day-ahead prices into one wide frame (one column per zone).

    Accepts either a Series or a single-column DataFrame per zone (as the ingest
    loaders return). tz-aware indexes are normalised to UTC so zones in different
    timezones align on the same instants; the outer join keeps every timestamp.
    """
    cols: dict[str, pd.Series] = {}
    for zone, obj in prices_by_zone.items():
        s = obj.iloc[:, 0] if isinstance(obj, pd.DataFrame) else obj
        if isinstance(s.index, pd.DatetimeIndex) and s.index.tz is not None:
            s = s.copy()
            s.index = s.index.tz_convert("UTC")
        cols[zone] = s
    return pd.DataFrame(cols).sort_index()


def zone_spread(prices_wide: pd.DataFrame, a: str, b: str) -> pd.Series:
    """Price spread ``a - b`` (EUR/MWh). Positive => zone *a* is the more expensive."""
    for z in (a, b):
        if z not in prices_wide.columns:
            raise KeyError(f"zone {z!r} not in columns {list(prices_wide.columns)}")
    return (prices_wide[a] - prices_wide[b]).rename(f"{a}_minus_{b}")
