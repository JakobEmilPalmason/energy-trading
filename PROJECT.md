# Energy Markets Research — Project Notes

A personal workspace for learning my way around energy markets and the data
behind them. I haven't settled on a direction yet, so this stays exploratory for
now: a place to understand how power prices form and what drives them, and to
build reusable tooling so future questions are cheap to ask.

## Scope & framing

- **Personal, independent research. Learning-first.** The direction is open;
  right now the work is about building a solid data layer and getting familiar
  with the markets.
- **Data-layer-first.** Whatever I end up analysing depends on reliable, tidy,
  cached data underneath, so that comes first.
- **Do NOT reference any employer, company, recruiter, or interview anywhere in
  this repo.** No proprietary data, no internal figures. Every number must trace
  to a public, citable source.
- **Where I've started: European / Nordic power markets.** The free,
  well-documented public sources below cover this region, so it's a natural
  starting point rather than a fixed boundary. These markets are hydro- and
  weather-sensitive, so reservoir levels, precipitation, temperature and wind
  matter as price drivers and are treated as first-class.

## What I'm building first (the data foundation)

1. Reliable ingestion of power prices + system fundamentals (load, generation
   mix, cross-border flows) into tidy, cached local datasets.
2. Weather (Open-Meteo) and hydro reservoir (NVE) ingestion, since these are
   strong price drivers in the markets currently in view.
3. A small reusable library (data loaders, transforms, plotting helpers) so new
   analyses take minutes, not hours.
4. Exploratory analysis: price seasonality and zone spreads, price vs wind /
   temperature / reservoir levels.
5. A running research log (`docs/findings.md`).

## A direction I'm curious about (not committed)

Intraday markets are one thing I'd like to understand better — intraday-auction
(IDA) clearing prices, imbalance prices/volumes, and how intraday prices respond
to wind/solar forecast updates and outages. That's a maybe-later interest, and
it would still depend on the data layer being solid first.

> **Honest data caveat (verified — `docs/sources/entsoe.md`):** ENTSO-E exposes
> IDA auction prices, imbalance prices/volumes and intraday RES forecasts for
> free, **but the continuous-market (SIDC/XBID) order book and individual trades
> are NOT publicly available** — tick-level intraday data requires a paid EPEX
> SPOT / Nord Pool feed. This project deliberately does not depend on that.

## Explicitly out of scope

Live trading, paper-trading "books", real-money anything, production forecasting
models, and any reliance on non-public/paid market-data feeds. Keep claims modest
and sourced.

## Build-on-prior-art decision (verified — `docs/prior-art.md`)

- **Adopt `entsoe-py`** (MIT, actively maintained, pandas-native) as the
  ingestion spine for ENTSO-E data. **Adopt** Open-Meteo for weather.
- **There is no "gridstatus for Europe"** — the tidy, cached, multi-source data
  layer is this project's own value-add, written fresh on top of those libraries.
- Wrap the keyless REST APIs (NVE, SMHI, energy-charts) directly; no mature client
  is worth a dependency. No pipeline/template repo was worth forking.

## Data sources (free-first, all verified 2026-06-27)

| Source | What | Access | Spec |
|--------|------|--------|------|
| **ENTSO-E Transparency** | Day-ahead prices, load, generation, flows, IDA & imbalance | Free token | [entsoe.md](docs/sources/entsoe.md) |
| **Open-Meteo** | Historical + forecast weather (temp, wind, solar, precip) | Keyless | [open-meteo.md](docs/sources/open-meteo.md) |
| **NVE Magasinstatistikk** | Norwegian reservoir filling by price area (NO1–NO5) | Keyless | [hydro.md](docs/sources/hydro.md) |
| **SMHI Open Data** | Swedish hydrology + meteorology | Keyless | [hydro.md](docs/sources/hydro.md) |
| **energy-charts.info** | Generation mix + price cross-check (Fraunhofer ISE) | Keyless | [energy-charts.md](docs/sources/energy-charts.md) |

## Notes that shape the schema

- **Day-ahead now clears in 15-minute MTUs** (since 30 Sep 2025) — storage and
  transforms are resolution-agnostic, never hardcoded to hourly.
- ENTSO-E API is UTC (`yyyyMMddHHmm`); always pass tz-aware timestamps.

## What exists so far

- [x] Repo initialized: `.gitignore`, `README.md`, `LICENSE`, `pyproject.toml` (pinned deps), `.python-version`.
- [x] `.env.example` listing `ENTSOE_API_KEY` (no real value committed).
- [x] Per-source specs in `docs/sources/` + `docs/data-sources.md` index + `docs/market-primer.md`.
- [x] Working ingestion for DK1 + DK2 day-ahead prices, cached to `data/`, via `scripts/fetch_day_ahead.py`.
- [x] Notebook loading the data and plotting a price series + a zone spread.
- [x] Ruff lint + an offline smoke test wired into GitHub Actions.
