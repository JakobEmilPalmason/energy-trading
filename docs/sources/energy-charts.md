# energy-charts.info API (Fraunhofer ISE)

Public REST API for European electricity data (generation mix, day-ahead prices,
installed capacity, cross-border flows, grid frequency, renewable share). Useful as
an independent, public-source cross-check against ENTSO-E.

- **Base URL:** `https://api.energy-charts.info`
- **Interactive docs / OpenAPI:** <https://api.energy-charts.info/> (spec at `/openapi.json`, version 1.6 as of 2026-06-27)
- **Site / publishing notes:** <https://www.energy-charts.info/api.html?l=en&c=DE>, <https://energy-charts.info/publishing-notes.html>

## Access & license

- **No API key, no registration, no token.** All requests below were made without auth and returned `200`.
- **License:** CC BY 4.0 for most series. Each `/price` response carries a `license_info`
  attribution string, e.g. `"CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur | SMARD.de"`.
  Attribute the original data source (e.g. SMARD.de / ENTSO-E) plus energy-charts.info / Fraunhofer ISE.
- **Rate limit:** Yes — rapid sequential calls returned `HTTP 429 Too Many Requests`
  (observed directly). Throttle / add backoff; ~1 request/second with retry-on-429 is safe.

## Key endpoints (all `GET`, JSON)

| Endpoint | Purpose | Region param | Time params |
|---|---|---|---|
| `/public_power` | Generation mix (per production type) | `country` (default `de`) | `start`, `end` (ISO date or unix) |
| `/price` | Day-ahead spot price | `bzn` (default `DE-LU`) | `start`, `end` |
| `/installed_power` | Installed capacity | `country` (default `de`) | `time_step` (`yearly`/`monthly`), `installation_decommission` (bool) |

Note the asymmetry: **`/public_power` and `/installed_power` use country codes**, while
**`/price` uses bidding-zone codes (`bzn`)**.

## Nordic region codes (all confirmed live)

- **`country` (for `/public_power`, `/installed_power`):** `dk`, `no`, `se`, `fi` — all returned `200`.
  (Use these whole-country codes; bidding-zone codes like `DK1` are **rejected** here:
  `"'DK1' is not the code for an available country"`.)
- **`bzn` (for `/price`):** confirmed `200` for **all** Nordic zones:
  `DK1`, `DK2`, `SE1`, `SE2`, `SE3`, `SE4`, `NO1`, `NO2`, `NO3`, `NO4`, `NO5`, `FI`.
  Day-ahead prices are returned at 15-minute resolution (96 points/day).

## Response shape (from real responses, 2026-06-20)

`/public_power?country=dk` -> `ProductionModel`:

```json
{
  "unix_seconds": [ 1750377600, ... ],
  "production_types": [
    { "name": "Wind offshore", "data": [ 1234.5, ... ] },
    { "name": "Solar", "data": [ ... ] }
  ],
  "deprecated": false
}
```

`production_types` for `dk` included: Cross border electricity trading, Biomass, Fossil oil,
Fossil gas, Waste, Wind offshore, Wind onshore, Solar, Load, Residual load,
Renewable share of load, Renewable share of generation. (Names/count differ per country —
e.g. `se` and `fi` include Nuclear.) Each `data` array aligns index-for-index with `unix_seconds`; units are MW.

`/price?bzn=DK1` -> `PriceModel`:

```json
{
  "license_info": "CC BY 4.0 (creativecommons.org/licenses/by/4.0) from Bundesnetzagentur | SMARD.de",
  "unix_seconds": [ 1781906400, 1781907300, ... ],
  "price": [ 142.44, 133.02, ... ],
  "unit": "EUR / MWh",
  "deprecated": false
}
```

`/installed_power?country=dk&time_step=yearly` -> `InstalledModel`: top-level keys
`time` (e.g. `["2014", ..., "2025"]`), `production_types` (`{name, data}` per type), `last_update`, `deprecated`.

## Minimal working snippet

```python
import requests

BASE = "https://api.energy-charts.info"

# Day-ahead price for the Copenhagen zone (DK2)
r = requests.get(f"{BASE}/price",
                 params={"bzn": "DK2", "start": "2026-06-20", "end": "2026-06-20"},
                 timeout=30)
r.raise_for_status()
data = r.json()
print(data["unit"], data["license_info"])
for ts, p in zip(data["unix_seconds"][:5], data["price"][:5]):
    print(ts, p)

# Generation mix for Denmark (whole country)
r = requests.get(f"{BASE}/public_power",
                 params={"country": "dk", "start": "2026-06-20", "end": "2026-06-20"},
                 timeout=30)
r.raise_for_status()
mix = r.json()
print([pt["name"] for pt in mix["production_types"]])
```

> Add retry/backoff on `429`. The `country`/`bzn` split is easy to trip over: generation =
> country code, price = bidding zone.

## Cross-checking ENTSO-E

energy-charts largely **redistributes ENTSO-E transparency data** (plus SMARD.de for DE),
so it is a convenient parallel pull, not a fully independent source. It is still valuable:
the JSON shape is far simpler than ENTSO-E's XML, region/zone coverage matches
(country generation mix + per-bidding-zone prices), and discrepancies usually flag
ingestion/timestamp/unit-handling issues on your side rather than upstream data differences.
For DK day-ahead prices it also carries Bundesnetzagentur/SMARD provenance, giving a
second lineage for German-coupled zones.

## Sources

- API root / OpenAPI: <https://api.energy-charts.info/>
- API page: <https://www.energy-charts.info/api.html?l=en&c=DE>
- Publishing notes (license): <https://energy-charts.info/publishing-notes.html>
- Live responses captured 2026-06-27 (endpoints, zone codes, shapes verified directly).
