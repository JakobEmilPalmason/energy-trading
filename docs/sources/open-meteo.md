# Open-Meteo (weather ingestion)

Open-Meteo is a free, open-source weather API. We use it as the weather-driver
source for Nordic electricity-market research (temperature, wind, solar, etc.).
Verified against the live docs and a real API request on 2026-06-27.

## APIs and base URLs

| Purpose | Base URL | Source / model |
|---|---|---|
| Historical (reanalysis) | `https://archive-api.open-meteo.com/v1/archive` | ERA5 / ERA5-Land, hourly, global, 0.25°/0.1° (~9–25 km), 1940–present, ~5-day delay |
| Forecast | `https://api.open-meteo.com/v1/forecast` | Blend of national weather models (ICON, GFS, etc.) |

Docs: [historical](https://open-meteo.com/en/docs/historical-weather-api) ·
[forecast](https://open-meteo.com/en/docs/docs).

## Power-relevant hourly variables

Pass these in the `hourly=` parameter (comma-separated). Exact spellings confirmed
against a live response:

| Variable | Param name | Unit (default) |
|---|---|---|
| 2 m air temperature | `temperature_2m` | °C |
| 10 m wind speed | `wind_speed_10m` | km/h |
| 100 m wind speed | `wind_speed_100m` | km/h |
| Precipitation | `precipitation` | mm |
| Shortwave (global) solar radiation | `shortwave_radiation` | W/m² |
| Cloud cover (total) | `cloud_cover` | % |

Notes: `wind_speed_100m` is available from ERA5 (archive) and most forecast models;
some forecast models instead expose hub heights like `wind_speed_80m` /
`wind_speed_120m`. Use `&windspeed_unit=ms` for m/s if preferred. Most variables are
instantaneous for the stamped hour; `precipitation` is the sum over the preceding hour.

## Nordic bidding-zone query points

One representative coordinate per zone (lat, lon). Adjust as needed for wind/solar
weighting per zone.

| Zone | Reference point | Latitude | Longitude |
|---|---|---|---|
| DK1 | Esbjerg | 55.47 | 8.45 |
| DK2 | Copenhagen | 55.68 | 12.57 |
| NO1 | Oslo | 59.91 | 10.75 |
| NO2 | Kristiansand | 58.15 | 7.99 |
| NO3 | Trondheim | 63.43 | 10.39 |
| NO4 | Tromsø | 69.65 | 18.96 |
| NO5 | Bergen | 60.39 | 5.32 |
| SE1 | Luleå | 65.58 | 22.15 |
| SE2 | Sundsvall | 62.39 | 17.31 |
| SE3 | Stockholm | 59.33 | 18.07 |
| SE4 | Malmö | 55.60 | 13.00 |
| FI | Helsinki | 60.17 | 24.94 |

Query a point with `latitude=` / `longitude=`, plus `start_date` / `end_date`
(`YYYY-MM-DD`) for the archive endpoint.

## Access, limits, license

- **No API key**, no sign-up, no credit card for the free tier.
- **Rate limits (free):** < 600 calls/min, < 5,000 calls/hour, < 10,000 calls/day.
- **Use:** free tier is **non-commercial only** (private/personal, non-profit,
  public research, education). Commercial use requires a paid plan.
- **Data license:** **CC BY 4.0**. Attribution required — display a link such as
  `Weather data by Open-Meteo.com` next to any location the data is shown. ERA5 data
  carries its own ECMWF/Copernicus attribution; credit the underlying model where
  relevant.

Refs: [terms](https://open-meteo.com/en/terms) ·
[licence](https://open-meteo.com/en/licence) ·
[pricing](https://open-meteo.com/en/pricing).

## Response shape

`timezone=Europe/Copenhagen` (or `auto`) returns local timestamps; default is UTC.
Confirmed top-level keys from a live archive request:

```
latitude, longitude, generationtime_ms, utc_offset_seconds,
timezone, timezone_abbreviation, elevation, hourly_units, hourly
```

- `hourly.time` is an ISO8601 string array (`"2024-01-01T00:00"`, …); each requested
  variable is a parallel array of equal length, index-aligned to `time`.
- `hourly_units` maps each variable to its unit string (e.g. `temperature_2m: "°C"`,
  `wind_speed_10m: "km/h"`, `shortwave_radiation: "W/m²"`, `cloud_cover: "%"`).
- `utc_offset_seconds` reflects the requested timezone (e.g. `7200` for
  Europe/Copenhagen in winter).

## Minimal `requests` snippet

```python
import requests

# DK2 = Copenhagen
params = {
    "latitude": 55.68,
    "longitude": 12.57,
    "start_date": "2024-01-01",
    "end_date": "2024-01-02",
    "hourly": ",".join([
        "temperature_2m",
        "wind_speed_10m",
        "wind_speed_100m",
        "precipitation",
        "shortwave_radiation",
        "cloud_cover",
    ]),
    "timezone": "Europe/Copenhagen",
}

r = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params, timeout=30)
r.raise_for_status()
data = r.json()

times = data["hourly"]["time"]
temps = data["hourly"]["temperature_2m"]
print(data["timezone"], data["hourly_units"]["temperature_2m"])
print(times[0], temps[0])  # e.g. 2024-01-01T00:00 5.6
```

Swap the base URL to `https://api.open-meteo.com/v1/forecast` and drop
`start_date`/`end_date` (use `forecast_days=` / `past_days=`) for the forecast API.

---
Sources: <https://open-meteo.com/en/docs/historical-weather-api>,
<https://open-meteo.com/en/docs>, <https://open-meteo.com/en/terms>,
<https://open-meteo.com/en/licence>, <https://open-meteo.com/en/pricing>.
Verified with a live request to `archive-api.open-meteo.com` on 2026-06-27.
