"""energy-charts.info ingestion (Fraunhofer ISE, keyless) — cross-check on ENTSO-E.

Spec: docs/sources/energy-charts.md. Watch the region-param asymmetry:
``/price`` takes a bidding-zone code (``bzn``) while ``/public_power`` takes a
country code. The API returns 429 on bursts, so we back off. CC BY 4.0.
"""

from __future__ import annotations

import time

import pandas as pd
import requests

from energy_markets.ingest.cache import cached_parquet
from energy_markets.zones import get_zone

EC_BASE = "https://api.energy-charts.info"


def _get(path: str, params: dict, *, retries: int = 4) -> dict:
    """GET with exponential backoff on HTTP 429."""
    resp = None
    for attempt in range(retries):
        resp = requests.get(f"{EC_BASE}{path}", params=params, timeout=60)
        if resp.status_code == 429:
            time.sleep(2**attempt)
            continue
        resp.raise_for_status()
        return resp.json()
    resp.raise_for_status()  # exhausted retries, still 429
    return {}


def fetch_price(zone: str, start, end, *, refresh: bool = False) -> pd.DataFrame:
    """Day-ahead price (EUR/MWh) for a bidding zone via /price (bzn code).

    Returns a DataFrame indexed by UTC ``timestamp`` with a ``price_eur_mwh`` column.
    """
    z = get_zone(zone)
    relpath = f"energy-charts/price_{z.code}_{start}_{end}.parquet"

    def _fetch() -> pd.DataFrame:
        data = _get("/price", {"bzn": z.ec_bzn, "start": str(start), "end": str(end)})
        idx = pd.to_datetime(data["unix_seconds"], unit="s", utc=True)
        df = pd.DataFrame({"price_eur_mwh": data["price"]}, index=idx)
        df.index.name = "timestamp"
        return df

    return cached_parquet(relpath, _fetch, refresh=refresh)


def fetch_generation_mix(zone: str, start, end, *, refresh: bool = False) -> pd.DataFrame:
    """Generation mix (MW per production type) for the zone's WHOLE COUNTRY.

    /public_power uses a country code (dk/no/se/fi); bidding-zone strings are
    rejected upstream, so we map the zone to its country. Returns a DataFrame
    indexed by UTC ``timestamp`` with one column per production type.
    """
    z = get_zone(zone)
    relpath = f"energy-charts/genmix_{z.ec_country}_{start}_{end}.parquet"

    def _fetch() -> pd.DataFrame:
        data = _get(
            "/public_power", {"country": z.ec_country, "start": str(start), "end": str(end)}
        )
        idx = pd.to_datetime(data["unix_seconds"], unit="s", utc=True)
        cols = {pt["name"]: pt["data"] for pt in data["production_types"]}
        df = pd.DataFrame(cols, index=idx)
        df.index.name = "timestamp"
        return df

    return cached_parquet(relpath, _fetch, refresh=refresh)
