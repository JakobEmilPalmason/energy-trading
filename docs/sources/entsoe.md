# ENTSO-E Transparency Platform

Primary public-source data feed for the Nordic ingestion layer: day-ahead prices,
load, generation, cross-border flows, plus intraday-auction and imbalance data.
Verified 2026-06-27 against official ENTSO-E docs and the `entsoe-py` library.

## Auth — obtaining the free RESTful API token

1. Register at <https://transparency.entsoe.eu/> — "Sign in" -> "Register". Password
   must be >= 14 chars with >= 1 special char. Confirm via the activation email.
2. Email **transparency@entsoe.eu** with subject **"Restful API access"** and the
   **registered email address in the body**. (This explicit request step is required;
   registration alone does not enable the API.)
3. Approval typically within ~3 working days (often next business day). On approval,
   generate the token under **My Account Settings** on the Transparency Platform.
4. Pass it as the URL query parameter **`securityToken`** (not an HTTP header), e.g.
   `...&securityToken=<token>`. Base URL: `https://web-api.tp.entsoe.eu/api`.

Sources: [How to get security token](https://transparencyplatform.zendesk.com/hc/en-us/articles/12845911031188-How-to-get-security-token),
[amsleser walkthrough](https://www.amsleser.no/blog/post/21-obtaining-api-token-from-entso-e).

## Nordic bidding-zone EIC codes

All 12 verified against `entsoe-py` `mappings.py` `Area` enum (the codes the production
API accepts). Source: <https://github.com/EnergieID/entsoe-py/blob/master/entsoe/mappings.py>.

| Zone | EIC code         | Time zone         |
|------|------------------|-------------------|
| DK1  | 10YDK-1--------W | Europe/Copenhagen |
| DK2  | 10YDK-2--------M | Europe/Copenhagen |
| NO1  | 10YNO-1--------2 | Europe/Oslo       |
| NO2  | 10YNO-2--------T | Europe/Oslo       |
| NO3  | 10YNO-3--------J | Europe/Oslo       |
| NO4  | 10YNO-4--------9 | Europe/Oslo       |
| NO5  | 10Y1001A1001A48H | Europe/Oslo       |
| SE1  | 10Y1001A1001A44P | Europe/Stockholm  |
| SE2  | 10Y1001A1001A45N | Europe/Stockholm  |
| SE3  | 10Y1001A1001A46L | Europe/Stockholm  |
| SE4  | 10Y1001A1001A47J | Europe/Stockholm  |
| FI   | 10YFI-1--------U | Europe/Helsinki   |

Note: NO5, SE1–SE4 use generic `10Y1001A1001A...` IDs (not `10YNO-`/`10YSE-` patterns) —
this is correct, not a typo. DK1/DK2, NO1–NO4 and FI follow the `10Y<cc>-n` pattern.
No zone failed verification. In `entsoe-py` these map to short codes `DK_1`, `SE_3`, etc.,
but you can also pass the raw EIC string or the country code.

## Core queries (`entsoe-py` `EntsoePandasClient`)

- **Day-ahead prices** — `query_day_ahead_prices(zone, start, end)` (doc type A44).
- **Actual load** — `query_load(zone, start, end)`; **forecast** —
  `query_load_forecast(zone, start, end)`; combined — `query_load_and_forecast(...)` (A65).
- **Actual generation per production type** — `query_generation(zone, start, end, psr_type=None)`
  (A75; `psr_type` filters fuel, e.g. `B16` solar, `B19` wind onshore).
- **Cross-border physical flows** — `query_crossborder_flows(zone_from, zone_to, start, end)` (A11).

## Intraday-relevant data — and honest limits

Freely available via the API / Transparency Platform:
- **Intraday-auction (IDA) prices** — IDAs went live across the SIDC area on 13 Jun 2024
  (incl. DK, NO, SE, FI). Implicit-auction clearing prices per bidding zone are published.
- **Imbalance prices** — `query_imbalance_prices(zone, start, end)` (A85).
- **Imbalance volumes** — `query_imbalance_volumes(zone, start, end)` (A86).
- **Intraday wind/solar forecast** — `query_intraday_wind_and_solar_forecast(zone, start, end)`.
- Aggregated continuous-market figures (traded volumes, offered intraday cross-zonal capacity).

NOT freely available at trade-level granularity (be explicit about this):
- **Continuous-market (SIDC) order-book and individual trades are NOT on the Transparency
  Platform.** Only aggregated traded volumes / capacity are published. Tick-level order
  book, individual matched trades, and the SIDC continuous price curve require a paid
  exchange data feed (EPEX SPOT / Nord Pool). The platform is a transparency reporting
  feed, not a market-data terminal — granularity is hourly/PTU aggregates, not per-order.
- The `query_intraday_offered_capacity` path has known breakage since IDA go-live
  ([entsoe-py #527](https://github.com/EnergieID/entsoe-py/issues/527)) — validate before relying on it.

Sources: [SIDC](https://www.entsoe.eu/network_codes/cacm/implementation/sidc/),
[IDA on SIDC](https://www.entsoe.eu/network_codes/cacm/implementation/ida/).

## Rate limits & quirks

- **400 requests / minute** per security token AND per IP. Exceeding it = **10-minute
  temporary ban**. ([token doc](https://transparencyplatform.zendesk.com/hc/en-us/articles/12845911031188-How-to-get-security-token)).
- **Request-window limit**: a single query returns a bounded document count; large spans
  raise a pagination/limit error (the typical safe window is ~1 year per call — page your
  requests). `entsoe-py` retries (3x, 10s) and raises `PaginationError` when the requested
  span exceeds the allowed document count.
- **Time zones**: the API works in **UTC** with `yyyyMMddHHmm` timestamps. `entsoe-py`
  takes **tz-aware `pandas.Timestamp`** start/end and returns series indexed in the
  zone's local time — always pass `tz=`, never naive timestamps.

## License / terms of reuse

Data designated open is published under **Creative Commons Attribution 4.0 (CC-BY 4.0)**
(applied since Feb 2022) — free reuse without prior permission from the data owner,
**attribution required** (credit ENTSO-E Transparency Platform). Verify a given dataset is
on the open-reuse list, and check the platform's Terms & Conditions before redistribution.
Sources: [TSOs increase open data](https://www.entsoe.eu/news/2019/02/01/tsos-increase-number-of-open-data-available-through-entso-e-s-transparency-platform/),
[Legal Terms & Conditions](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions).

## Library

`entsoe-py` — `pip install entsoe-py`. Current version **0.8.0** (Apr 2026). **MIT** license.
Repo: <https://github.com/EnergieID/entsoe-py> · PyPI: <https://pypi.org/project/entsoe-py/>.
`EntsoePandasClient` returns pandas Series/DataFrames; `EntsoeRawClient` returns raw XML.

## Minimal working snippet — DK1 + DK2 day-ahead prices

```python
import os
import pandas as pd
from entsoe import EntsoePandasClient

client = EntsoePandasClient(api_key=os.environ["ENTSOE_API_KEY"])

start = pd.Timestamp("2026-01-01", tz="Europe/Copenhagen")
end   = pd.Timestamp("2026-02-01", tz="Europe/Copenhagen")

for zone in ("DK_1", "DK_2"):           # or raw EICs "10YDK-1--------W" / "10YDK-2--------M"
    prices = client.query_day_ahead_prices(zone, start=start, end=end)
    print(zone, prices.head())          # EUR/MWh, indexed in local time
```
