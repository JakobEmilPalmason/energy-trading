"""ENTSO-E Transparency Platform ingestion (the spine), via entsoe-py.

Spec: docs/sources/entsoe.md. The API works in UTC and entsoe-py wants tz-aware
pandas Timestamps, so naive start/end are localized to the zone. Rate limit is
400 req/min; results are cached to data/raw/entsoe/.
"""

from __future__ import annotations

import pandas as pd
from entsoe import EntsoePandasClient

from energy_markets.config import get_entsoe_api_key
from energy_markets.ingest.cache import cached_parquet
from energy_markets.zones import get_zone

PRICE_COL = "price_eur_mwh"


def _client() -> EntsoePandasClient:
    return EntsoePandasClient(api_key=get_entsoe_api_key())


def _ts(value, tz: str) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    return ts.tz_localize(tz) if ts.tzinfo is None else ts.tz_convert(tz)


def fetch_day_ahead_prices(zone: str, start, end, *, refresh: bool = False) -> pd.DataFrame:
    """Day-ahead prices (EUR/MWh) for a bidding zone, cached to data/raw.

    Returns a tidy DataFrame indexed by local-time ``timestamp`` with a single
    ``price_eur_mwh`` column. Resolution follows the market (15-min since
    2025-09-30, hourly before) — never assume hourly.
    """
    z = get_zone(zone)
    start_ts, end_ts = _ts(start, z.tz), _ts(end, z.tz)
    relpath = f"entsoe/day_ahead_prices/{z.code}_{start_ts.date()}_{end_ts.date()}.parquet"

    def _fetch() -> pd.DataFrame:
        series = _client().query_day_ahead_prices(z.entsoe_alias, start=start_ts, end=end_ts)
        df = series.rename(PRICE_COL).to_frame()
        df.index.name = "timestamp"
        return df

    return cached_parquet(relpath, _fetch, refresh=refresh)


def fetch_load(zone: str, start, end, *, refresh: bool = False) -> pd.DataFrame:
    """Actual total load (MW) for a bidding zone, cached to data/raw."""
    z = get_zone(zone)
    start_ts, end_ts = _ts(start, z.tz), _ts(end, z.tz)
    relpath = f"entsoe/load/{z.code}_{start_ts.date()}_{end_ts.date()}.parquet"

    def _fetch() -> pd.DataFrame:
        df = _client().query_load(z.entsoe_alias, start=start_ts, end=end_ts)
        df.index.name = "timestamp"
        return df

    return cached_parquet(relpath, _fetch, refresh=refresh)
