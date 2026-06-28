# Nordic Electricity Market Primer

*Intraday-oriented primer on Nordic (and coupled European) power market mechanics. Public sources only; URLs cited inline. Last reviewed 2026-06-27.*

The Nordic spot market is operated on Nord Pool, coupled into the pan-European day-ahead and intraday markets. Wholesale price formation happens in two sequential venues: a **day-ahead auction** (the main liquidity pool) and an **intraday market** (continuous + auctions) that corrects positions after the day-ahead result is known. Below them sits **balancing**, run by the TSOs in real time.

---

## 1. Day-ahead market (SDAC / EUPHEMIA)

The day-ahead market is a **once-per-day, blind auction** clearing the 24 delivery hours of the next day (D). Buyers and sellers submit price/volume curves; the auction computes a **uniform marginal clearing price** per bidding zone per delivery period — every accepted bid pays/receives the same clearing price, set by the marginal unit, not its own bid.

- **Gate closure ~12:00 CET** on D-1. NEMO (Nominated Electricity Market Operator, e.g. Nord Pool, EPEX SPOT) order books close, are validated, and submitted to the central matcher. ([ENTSO-E SDAC](https://www.entsoe.eu/network_codes/cacm/implementation/sdac/), [emissions-euets glossary](https://www.emissions-euets.com/internal-electricity-market-glossary/2032-single-day-ahead-coupling-sdac))
- **SDAC (Single Day-Ahead Coupling)** couples ~27 European countries into one calculation. It uses the **EUPHEMIA** algorithm, which maximizes total economic surplus (social welfare = consumer + producer surplus + congestion rent) across all coupled zones simultaneously, subject to available cross-border transmission capacity. ([Nord Pool EUPHEMIA public description](https://www.nordpoolgroup.com/globalassets/download-center/single-day-ahead-coupling/euphemia-public-description.pdf), [ENTSO-E SDAC](https://www.entsoe.eu/network_codes/cacm/implementation/sdac/))
- **Market coupling = implicit auction**: cross-border capacity is allocated *together with* energy in the same clear, so power implicitly flows from low- to high-price zones until either prices equalize or the interconnector saturates. Traders never explicitly buy transmission rights for the spot.
- **Result ~12:42–13:00 CET**: zonal prices and net positions are published; if congestion appears, zones decouple in price (see §2).
- **15-minute MTU**: since trading day **30 Sep 2025** (delivery 1 Oct 2025), SDAC clears in **15-minute** Market Time Units (previously hourly). ([EPEX SPOT](https://www.epexspot.com/en/news/successful-implementation-15-minute-market-time-unit-mtu-sdac), [Nord Pool](https://www.nordpoolgroup.com/en/message-center-container/newsroom/exchange-message-list/2025/q3/market-coupling-steering-committee-confirms-go-live-of--15-minute-mtu-in-sdac-on-trading-day-30-september-2025-for-delivery-day-1-october-2025/))

---

## 2. Bidding zones & cross-border

The Nordic region is split into **12 bidding zones**: **DK1, DK2** (West / East Denmark), **NO1–NO5** (Norway), **SE1–SE4** (Sweden), and **FI** (Finland). ([Nord Pool bidding areas](https://www.nordpoolgroup.com/en/the-power-market/Bidding-areas/))

- **Why zones exist**: they map the grid's major **structural transmission bottlenecks**. Sweden was split into SE1–SE4 in 2011; Norway runs five zones. Each zone aggregates an area inside which the grid is (mostly) uncongested.
- **How spreads form**: EUPHEMIA prices each zone separately. With no binding congestion, neighboring zones converge to **one price** (full coupling). When a cross-border or internal corridor **saturates**, the auction can no longer move enough power, so it **splits prices** — the exporting (surplus) zone clears low, the importing (deficit) zone clears high. The gap is the **congestion / area-price spread**. ([Nord Pool bidding areas](https://www.nordpoolgroup.com/en/the-power-market/Bidding-areas/), [EA Energy Analyses, congestion management](https://www.ea-energianalyse.dk/wp-content/uploads/2020/02/730_congestion_management_in_the_nordic_market-evaluation_of_different_market_models.pdf))
- **Concrete patterns**: **DK1** (wind-heavy West DK, synchronous with continental Europe) frequently diverges from **DK2** (East DK, synchronous Nordic) because they sit on different synchronous areas linked by the Great Belt HVDC. North–south spreads inside Norway/Sweden are common: surplus hydro/wind in the north (NO4, SE1/SE2) vs. demand centers in the south (NO1/NO2, SE3/SE4), constrained by limited north–south transfer capacity. Surplus zones can hit **negative prices** when generation can't be exported. ([Montel — negative Nordic prices](https://montel.energy/resources/blog/why-do-negative-prices-occur-in-nordic-energy-hours))

---

## 3. Why Nordic prices are hydro- & weather-dominated

Roughly half of Nordic generation is **hydropower** (~200 TWh/yr, >50 GW installed, concentrated in Norway and northern Sweden), much of it with **reservoir storage**. This makes the supply curve fundamentally about *when* to release water. ([Energy Exemplar](https://www.energyexemplar.com/blog/nordic-power-market))

- **Water value**: a reservoir operator's marginal cost is not fuel but the **opportunity cost of water** — the expected value of generating later instead of now. It's the solution to a stochastic dynamic optimization over future inflows, prices and reservoir limits. Producers bid roughly at their water value, so it effectively sets the hydro supply curve and often the marginal price. ([ScienceDirect — Norwegian hydropower market value](https://www.sciencedirect.com/science/article/pii/S0301479725010631), [Aalto — forecasting hydro supply curves](https://aaltodoc.aalto.fi/items/7d8a1686-565f-4dba-b959-cc140ac47f2a))
- **Reservoir / hydrology**: wet years with high snowpack and full reservoirs → low water values, low spot prices, export surplus. Dry years → depleted reservoirs, higher water values, reliance on thermal/imports, elevated prices. Reservoir-fill and inflow data are leading price indicators. ([Montel — reservoir levels](https://montel.energy/resources/blog/high-and-dry-nordic-power-prices-and-reservoir-levels))
- **Wind** (esp. DK, increasingly SE/FI): high near-zero-marginal-cost wind pushes prices down and drives negative-price hours; it is also the dominant *intraday* surprise.
- **Temperature**: Nordic heating demand is highly temperature-sensitive (electric heating). Cold + dry → high demand and low inflow simultaneously → price spikes. ([Sigholm](https://www.sigholm.se/en/articles/analysis-electricity-market-hydropower))

---

## 4. Intraday market (SIDC / XBID) — primary focus

After day-ahead clears, participants trade in the **intraday market** to adjust positions toward real time. This is the **pan-European Single Intraday Coupling (SIDC)**, run on the shared **XBID** order-book/matching platform.

**Two trading modes:**

- **Continuous trading (XBID)**: a continuous, cross-border order book matching individual bids/offers on a **first-come-first-served, pay-as-bid** basis (not a uniform auction price), as long as cross-zonal capacity is free. Runs nearly up to delivery; the Nordic intraday gate typically closes ~**1 hour** (in some borders less) before delivery. *(Exact per-border closing times vary — confirm against the relevant TSO/NEMO schedule; flagged as not fully verified here.)*
- **Intraday auctions (IDA1/IDA2/IDA3)**: discrete pan-European auctions added on **13 June 2024**, run with the **EUPHEMIA** algorithm (same engine as day-ahead) to re-price intraday cross-zonal capacity and give cleaner price signals. Gate closure times ([ENTSO-E IDA](https://www.entsoe.eu/network_codes/cacm/implementation/ida/)):
  - **IDA1** — gate closes **D-1 15:00 CET**, covers delivery D [00–24h]
  - **IDA2** — gate closes **D-1 22:00 CET**, covers D [00–24h]
  - **IDA3** — gate closes **D 10:00 CET**, covers D [12–24h]
  - Continuous cross-border trading on a border is **paused ~40 min** around each IDA gate closure (20 min before/after), since capacity can't be allocated to both at once. ([ENTSO-E IDA](https://www.entsoe.eu/network_codes/cacm/implementation/ida/))

**Why intraday exists / what moves it:**
- **Renewable forecast error**: updated **wind and solar forecasts** between D-1 noon and delivery are the single biggest driver — a downward wind revision in DK1 lifts intraday prices, an upward revision depresses them.
- **Outages / plant trips**: unplanned generator or interconnector trips force quick re-buying.
- **Portfolio rebalancing & imbalance avoidance**: parties trade out of expected imbalance because intraday is usually cheaper than the balancing/imbalance price. Expected imbalance prices therefore feed directly into intraday bids. ([Montel — intraday & balancing 2025](https://montel.energy/commentary/nordic-energy-markets-intraday-balancing-shifts-2025))
- Intraday also trades **15-minute products** (cross-border 15-min available since 2025), useful for capturing within-hour ramps.

---

## 5. Balancing / imbalance (and its link to intraday)

After intraday gate closure, the **TSOs** balance the system in real time using reserves — **aFRR** (automatic) and **mFRR** (manual) frequency restoration reserves. Any participant whose metered position deviates from its scheduled (day-ahead + intraday) position is settled at the **imbalance price**. The Nordics moved to a **single imbalance price** (1 Nov 2021) and to **15-minute imbalance settlement** (19 Mar 2025). Because the imbalance price is uncertain and can be punitive, traders use the intraday market to close expected gaps *before* real time — so the intraday market is essentially the last cheap chance to avoid balancing costs, which is why imbalance-price expectations are a core intraday signal. ([nordicbalancingmodel — 15-min ISP](https://nordicbalancingmodel.net/roadmap-and-projects/15-min-time-resolution/), [Montel — Finland imbalance pricing](https://montel.energy/commentary/balancing-in-transition-how-finlands-imbalance-prices-reflect-nordic-market-reforms))

---

### Key sources
- ENTSO-E SDAC: https://www.entsoe.eu/network_codes/cacm/implementation/sdac/
- ENTSO-E Intraday Auctions (IDA): https://www.entsoe.eu/network_codes/cacm/implementation/ida/
- ENTSO-E SIDC: https://www.entsoe.eu/network_codes/cacm/implementation/sidc/
- Nord Pool — EUPHEMIA public description: https://www.nordpoolgroup.com/globalassets/download-center/single-day-ahead-coupling/euphemia-public-description.pdf
- Nord Pool — bidding areas: https://www.nordpoolgroup.com/en/the-power-market/Bidding-areas/
- EPEX SPOT — 15-min MTU in SDAC: https://www.epexspot.com/en/news/successful-implementation-15-minute-market-time-unit-mtu-sdac
- nordicbalancingmodel.net (balancing reforms): https://nordicbalancingmodel.net/

*Assumptions flagged in-text: exact continuous-intraday per-border gate-closure timing was not fully verified and should be checked against current TSO/NEMO schedules.*
