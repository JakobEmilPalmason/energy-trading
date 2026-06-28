# Prior art: open-source building blocks for a Nordic power-data foundation

Scope check date: **2026-06-27**. Stars/recency below were verified live against GitHub on this date and will drift.
Goal: build the v1 ingestion layer **on** existing, well-maintained libraries where they exist, and write fresh only where the open-source options are thin or stale.

## 1. ENTSO-E clients (the core of European power data)

| Candidate | URL | Stars | Last activity | License | What it does | Verdict |
|---|---|---|---|---|---|---|
| **entsoe-py** (EnergieID) | https://github.com/EnergieID/entsoe-py | ~690 | v0.8.0, Apr 2026 — active | MIT | Mature pandas client for the ENTSO-E Transparency Platform: day-ahead prices, load + load forecast, generation (actual/forecast/installed/per-unit), cross-border flows & scheduled exchanges, NTC, imbalance prices/volumes, wind/solar forecasts. Auto-splits multi-year requests. | **ADOPT** — the spine of ingestion. |
| python-entsoe (datons) | https://github.com/datons/python-entsoe | ~30 | v0.6.1, May 2026 — active | MIT | Newer, typed/namespaced ENTSO-E client; similar coverage (60+ zones, PSR filtering, retry/backoff, ZIP handling). Nicer ergonomics but far smaller community. | **SKIP for now** (watch) — same data as entsoe-py with a fraction of the adoption; revisit only if entsoe-py friction appears. |
| entsoe-apy (BerriJ) | https://github.com/BerriJ/entsoe-apy | small | active | MIT | Thin endpoint-complete wrapper, auto request-splitting. | **SKIP** — entsoe-py covers the same ground with more traction. |

Note: ENTSO-E covers **day-ahead** richly; "intraday" is limited to intraday *capacity* and intraday wind/solar forecasts — **not** continuous-trade order books.

## 2. A "gridstatus for Europe"?

[gridstatus](https://github.com/gridstatus/gridstatus) is US/Canada ISO only (CAISO, ERCOT, PJM, …) — no European zones. **No maintained, tidy, multi-source European/Nordic equivalent exists.** Claims of a "unified Nord Pool + EPEX + ENTSO-E + EEX client" did not resolve to any real repository. **Verdict: SKIP / write fresh** — our own thin tidy-wrapper over entsoe-py (+ a couple of sources below) effectively *is* the Nordic "gridstatus" and is the value we add.

## 3. Nord Pool / Nordic-specific clients

| Candidate | URL | Stars | Last activity | License | What it does | Verdict |
|---|---|---|---|---|---|---|
| kipe/nordpool | https://github.com/kipe/nordpool | ~125 | v0.5.1, Jan 2026 — active | MIT | Fetches Nord Pool Elspot **day-ahead spot prices** per area/currency. Narrow but solid and maintained. | **ADOPT (optional)** — handy cross-check / direct day-ahead source; ENTSO-E already gives Nordic day-ahead. |
| alexmgl/nordpool_client | https://github.com/alexmgl/nordpool_client | ~1 | v1.0.0, Mar 2025 | MIT | Wraps the Nord Pool Data Portal: day-ahead, intraday stats, EPAD, system price, flows, production/consumption — broad. | **SKIP (watch)** — best *scope* match (EPAD/intraday/flows) but essentially one author, 4 commits, no traction; vendor those API patterns rather than depend on it. |

## 4. Full repos / templates to fork or learn structure from

| Candidate | URL | Stars | Last activity | License | What it is | Verdict |
|---|---|---|---|---|---|---|
| BitePy | https://github.com/dschaurecker/bitepy | ~45 | v0.6.16, Jan 2026 — active | MIT | C++/Python battery **intraday** trading engine on EPEX order-book (LOB) data; rolling-intrinsic dynamic programming. | **REFERENCE** for the trading north star — EPEX-shaped, not Nord Pool, so don't fork as a base; study methodology. |
| power-data-downloader | https://github.com/MaurerErik/power-data-downloader | small | active | check repo | Selenium+BS4 scraper archiving EPEX day-ahead/intraday/continuous tables. | **SKIP** — fragile scraping, EPEX-centric, wrong shape for a clean cached pipeline. |
| mroeckl/electricity-prices, oskar456/electricity_market_prices | https://github.com/mroeckl/electricity-prices · https://github.com/oskar456/electricity_market_prices | small | mixed | check repo | Minimal "pull ENTSO-E day-ahead to CSV" scripts. | **SKIP** — too thin to build on; entsoe-py + our own caching beats them. |

No permissively licensed, well-maintained **Nordic data-pipeline template** worth forging from was found — **write our own project structure fresh** around entsoe-py.

## 5. Other source clients (weather / hydro / fundamentals)

| Candidate | URL | Stars | Last activity | License | What it does | Verdict |
|---|---|---|---|---|---|---|
| **openmeteo-requests** (official) | https://github.com/open-meteo/python-requests | ~45 | v1.7.5, Jan 2026 — active | MIT (Apache-2.0 pkg) | Official Open-Meteo client; FlatBuffers, zero-copy into numpy/pandas/polars; historical data from 1940. No key for non-commercial. | **ADOPT** — weather/forecast source. |
| alexanderblinn/Energy-Charts | https://github.com/alexanderblinn/Energy-Charts | ~10 | low activity | MIT | Wrapper for the Fraunhofer **energy-charts.info** API: generation by source, day-ahead prices, cross-border flows, installed capacity. No auth. | **REFERENCE / thin-adopt** — the *API* is great and free; the wrapper is low-traffic, so call the documented REST API (https://api.energy-charts.info/) directly. |
| SMHI clients (LasseRegin et al.) | https://github.com/LasseRegin/smhi-open-data | ~12 | stale, no releases | MIT | Python interface to SMHI (Swedish met/hydro) open data. | **SKIP** — stale; hit the SMHI Open Data REST API directly. |
| NVE HydAPI examples | https://github.com/NVE/HydAPI · https://hydapi.nve.no/ | ~8 | examples only | NLOD (data) | Official NVE Norwegian hydrology API — **code examples, not a pip package**. Reservoir/discharge/water-stage time series. | **REFERENCE** — wrap the HydAPI REST endpoint ourselves; NLOD-licensed data, key required. |

## Bottom line

- **Spine: entsoe-py.** Build the tidy/cached ingestion layer on top of it.
- **Adopt:** entsoe-py, openmeteo-requests; optionally kipe/nordpool for a direct day-ahead cross-check.
- **Wrap REST directly (no good maintained client):** energy-charts.info, SMHI, NVE HydAPI.
- **Write fresh:** the tidy multi-source layer (the "Nordic gridstatus"), caching, and project scaffolding — no existing template fits.
- **Reference only:** BitePy (intraday-trading methodology), alexmgl/nordpool_client (Nord Pool Data Portal endpoint patterns: EPAD/intraday/flows).
