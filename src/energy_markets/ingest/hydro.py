"""NVE Magasinstatistikk ingestion — Norwegian reservoir filling (keyless).

Spec: docs/sources/hydro.md. The endpoints take NO query params; you fetch the
whole array and filter client-side. We keep the elspot price areas (NO1..NO5).

IMPORTANT: ``fyllingsgrad`` is a FRACTION (0.517 = 51.7%), not a percent.
License: NLOD / CC BY 3.0 Norge (attribute NVE).
"""

from __future__ import annotations

import pandas as pd
import requests

from energy_markets.ingest.cache import cached_parquet

NVE_BASE = "https://biapi.nve.no/magasinstatistikk/api/Magasinstatistikk"


def _to_price_area_frame(rows: list[dict]) -> pd.DataFrame:
    """Keep elspot areas (omrType == 'EL', omrnr 1..5 -> NO1..NO5); tidy + rename."""
    df = pd.DataFrame(rows)
    el = df[df["omrType"] == "EL"].copy()
    el["zone"] = "NO" + el["omrnr"].astype(int).astype(str)
    out = el.rename(
        columns={
            "iso_aar": "iso_year",
            "iso_uke": "iso_week",
            "dato_Id": "date",
            "fylling_TWh": "fill_twh",
            "kapasitet_TWh": "capacity_twh",
        }
    )[["zone", "iso_year", "iso_week", "date", "fyllingsgrad", "fill_twh", "capacity_twh"]]
    out["date"] = pd.to_datetime(out["date"])
    return out.sort_values(["zone", "date"]).reset_index(drop=True)


def fetch_reservoir_filling(*, latest: bool = False, refresh: bool = False) -> pd.DataFrame:
    """Weekly reservoir filling per Norwegian price area (NO1..NO5).

    ``latest=True`` returns only the most recent week. Note the cache key is fixed,
    so pass ``refresh=True`` to pull a newly published week.
    """
    endpoint = "HentOffentligDataSisteUke" if latest else "HentOffentligData"
    relpath = f"nve/reservoir_{'latest' if latest else 'full'}.parquet"

    def _fetch() -> pd.DataFrame:
        r = requests.get(f"{NVE_BASE}/{endpoint}", timeout=60)
        r.raise_for_status()
        return _to_price_area_frame(r.json())

    return cached_parquet(relpath, _fetch, refresh=refresh)
