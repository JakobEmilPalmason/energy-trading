"""Open-Meteo historical weather ingestion (keyless).

Spec: docs/sources/open-meteo.md. Uses the ERA5 archive endpoint and one
representative coordinate per zone (see zones.py). We request UTC and convert to
the zone's local time to sidestep DST localization edge cases.

Free tier is non-commercial; data is CC BY 4.0 ("Weather data by Open-Meteo.com").
For higher throughput the official `openmeteo-requests` client is an alternative;
plain requests is enough for research-scale pulls.
"""

from __future__ import annotations

import pandas as pd
import requests

from energy_markets.ingest.cache import cached_parquet
from energy_markets.zones import get_zone

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
DEFAULT_VARIABLES = (
    "temperature_2m",
    "wind_speed_10m",
    "wind_speed_100m",
    "precipitation",
    "shortwave_radiation",
    "cloud_cover",
)


def fetch_weather_history(
    zone: str,
    start_date,
    end_date,
    *,
    variables: tuple[str, ...] = DEFAULT_VARIABLES,
    refresh: bool = False,
) -> pd.DataFrame:
    """Hourly historical weather for a zone's reference point.

    Returns a DataFrame indexed by local ``timestamp`` with one column per
    requested variable. Dates are ``YYYY-MM-DD``.
    """
    z = get_zone(zone)
    start, end = str(start_date), str(end_date)
    relpath = f"open-meteo/{z.code}_{start}_{end}.parquet"

    def _fetch() -> pd.DataFrame:
        params = {
            "latitude": z.lat,
            "longitude": z.lon,
            "start_date": start,
            "end_date": end,
            "hourly": ",".join(variables),
            "timezone": "UTC",
        }
        r = requests.get(ARCHIVE_URL, params=params, timeout=60)
        r.raise_for_status()
        hourly = r.json()["hourly"]
        df = pd.DataFrame(hourly)
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df.set_index("time").tz_convert(z.tz)
        df.index.name = "timestamp"
        return df

    return cached_parquet(relpath, _fetch, refresh=refresh)
