# Data sources — index & licensing

All sources are public and free. Each per-source file below was verified against
the live API on **2026-06-27** (endpoints, params, response shapes, licenses).
Attribution is required for every source — credit it on any published figure.

| Source | Used for | Key? | Resolution | License | Spec |
|--------|----------|------|-----------|---------|------|
| **ENTSO-E Transparency Platform** | Day-ahead prices, load, generation mix, cross-border flows, IDA & imbalance prices | Free token (`ENTSOE_API_KEY`) | 15-min / hourly | CC BY 4.0 (attribute ENTSO-E) | [entsoe.md](sources/entsoe.md) |
| **Open-Meteo** | Historical + forecast weather (temperature, wind 10m/100m, solar radiation, precipitation, cloud cover) | None | Hourly | CC BY 4.0 (+ ERA5/ECMWF); free tier non-commercial | [open-meteo.md](sources/open-meteo.md) |
| **NVE Magasinstatistikk** | Norwegian reservoir filling by price area (NO1–NO5) + national | None | Weekly | NLOD / CC BY 3.0 Norge (attribute NVE) | [hydro.md](sources/hydro.md) |
| **SMHI Open Data** | Swedish hydrology (discharge, water level) + meteorology | None | Varies | CC BY 4.0 (attribute SMHI) | [hydro.md](sources/hydro.md) |
| **energy-charts.info** | Generation-mix & price cross-check (Fraunhofer ISE) | None | 15-min / hourly | CC BY 4.0 (+ upstream SMARD/ENTSO-E) | [energy-charts.md](sources/energy-charts.md) |

## Key facts to remember (the easy-to-trip-over ones)

- **ENTSO-E** — token is a `securityToken` query param (entsoe-py handles it);
  400 req/min limit; UTC `yyyyMMddHHmm`, pass tz-aware timestamps; continuous
  intraday (SIDC) trades are **not** free.
- **Open-Meteo** — historical = `archive-api.open-meteo.com/v1/archive`,
  forecast = `api.open-meteo.com/v1/forecast`; free tier is non-commercial.
- **NVE** — host `biapi.nve.no/magasinstatistikk`; endpoints take **no query
  params** (filter the returned array client-side); `omrType=="EL"`, `omrnr`
  1–5 → NO1–NO5; **`fyllingsgrad` is a fraction (0.517 = 51.7%)**.
- **energy-charts** — `/public_power` & `/installed_power` take a `country` code
  (`dk/no/se/fi`); `/price` takes a `bzn` code (`DK1`…`FI`). Backoff on 429.
- **SMHI** — traverse `parameter → station → period → data`; timestamps are
  Unix epoch **milliseconds**.

## Background

See [`market-primer.md`](market-primer.md) for how the Nordic day-ahead,
intraday and balancing markets work and why hydro + weather dominate prices.
Prior-art / library audit: [`prior-art.md`](prior-art.md).
