# Hydrology data sources (Nordic)

Reservoir filling is a core Nordic price driver (the system is hydro-dominated, ~87 TWh
of Norwegian reservoir capacity). Two public, key-free sources cover it.

_Verified 2026-06-27 by live calls against the endpoints below._

---

## 1. NVE Magasinstatistikk (Norway reservoir filling) — gold standard

Weekly water-level statistics from NVE (Norges vassdrags- og energidirektorat) for ~490
of the most important reservoirs, aggregated to **elspot price areas NO1–NO5**, the
**country**, and **watercourse regions**.

- **Docs:** https://api.nve.no/doc/magasinstatistikk/
- **Swagger:** https://biapi.nve.no/magasinstatistikk/swagger/index.html
- **API host (confirmed):** `https://biapi.nve.no/magasinstatistikk`
- **No API key required.**

### Endpoints (all `GET`, no query params; you filter the returned array client-side)

| Path | Returns |
|------|---------|
| `/api/Magasinstatistikk/HentOffentligData` | Full history (weekly, back to 1993) |
| `/api/Magasinstatistikk/HentOffentligDataSisteUke` | Latest week only |
| `/api/Magasinstatistikk/HentOffentligDataMinMaxMedian` | 20-yr min/median/max per week |
| `/api/Magasinstatistikk/HentOmråder` | Area definitions (land / elspot / vassdrag) |

### Response shape (`MagasinstatistikkModel`, one object per area per ISO week)

```json
{
  "dato_Id": "2026-06-21",
  "omrType": "EL",          // EL = elspot area, NO = country, VASS = watercourse region
  "omrnr": 2,               // for EL: 1..5 = NO1..NO5; for NO: 0 = whole country
  "iso_aar": 2026,
  "iso_uke": 25,
  "fyllingsgrad": 0.5174129,        // filling FRACTION (0.517 = 51.7%), not percent
  "kapasitet_TWh": 34.04359,        // reservoir capacity, TWh
  "fylling_TWh": 17.614592,         // stored energy, TWh
  "neste_Publiseringsdato": "2026-07-01T13:00:00",
  "fyllingsgrad_forrige_uke": 0.4976233,
  "endring_fyllingsgrad": 0.019789606
}
```

### Price-area mapping (confirmed via `HentOmråder`)

Filter on `omrType == "EL"`, then `omrnr` → price area:
`1 = NO1` (East), `2 = NO2` (Southwest), `3 = NO3` (Mid), `4 = NO4` (North),
`5 = NO5` (West). National total: `omrType == "NO"`, `omrnr == 0`. Watercourse
regions use `omrType == "VASS"` (not price-relevant).

### Units & cadence

- `fyllingsgrad`: dimensionless fraction (multiply by 100 for %).
- `kapasitet_TWh` / `fylling_TWh`: terawatt-hours (energy equivalent, not volume).
- **Cadence:** weekly; aggregated area/national figures normally published **Wednesday
  afternoon** (`neste_Publiseringsdato` gives the next release timestamp).

### License

NLOD (Norsk lisens for offentlige data), compatible with CC BY 3.0 Norge. Attribute NVE
and, where possible, link back to the service. (Note: the data.norge.no catalog entry
lists license as "not provided", but the official API docs state NLOD/CC BY 3.0.)

### Minimal `requests` snippet — weekly filling per price area

```python
import requests

BASE = "https://biapi.nve.no/magasinstatistikk"
rows = requests.get(f"{BASE}/api/Magasinstatistikk/HentOffentligDataSisteUke", timeout=30).json()

# Latest filling per Norwegian price area NO1..NO5
price_areas = sorted(
    (r for r in rows if r["omrType"] == "EL"),
    key=lambda r: r["omrnr"],
)
for r in price_areas:
    print(f"NO{r['omrnr']}  wk{r['iso_uke']}/{r['iso_aar']}  "
          f"{r['fyllingsgrad']*100:5.1f}%  {r['fylling_TWh']:.1f}/{r['kapasitet_TWh']:.1f} TWh")

# National total
nat = next(r for r in rows if r["omrType"] == "NO" and r["omrnr"] == 0)
print(f"Norway  {nat['fyllingsgrad']*100:.1f}%")
```

---

## 2. SMHI Open Data (Sweden) — meteorology & hydrology

REST download services. Hydrology is the relevant one here; the same structure applies to
the meteorology service (`metobs`).

- **Portal / docs:** https://opendata.smhi.se/hydroobs/introduction
- **Hydrology base URL (confirmed):** `https://opendata-download-hydroobs.smhi.se`
- **Meteorology base URL:** `https://opendata-download-metobs.smhi.se`
- **No API key required.** All timestamps are **Unix epoch milliseconds**.

### REST hierarchy

Entry point: `/api.json` → versions → **parameter → station → period → data**.
Each response embeds links to the next level, so you traverse down by following them.

```
/api/version/latest.json                                  # list parameters
/api/version/latest/parameter/{p}.json                    # stations for parameter p
/api/version/latest/parameter/{p}/station/{id}.json       # periods for that station
/api/version/latest/parameter/{p}/station/{id}/period/{period}/data.json   # data
```

`{period}` is one of `latest-hour`, `latest-day`, `latest-months`, `corrected-archive`.
Output format set by extension: `.json`, `.xml`, `.csv`, `.atom`.

### Hydrological parameters (confirmed via `version/latest.json`)

| key | parameter | unit |
|-----|-----------|------|
| 1 | Vattenföring (Dygn) — discharge, daily | m³/s |
| 2 | Vattenföring (15 min) — discharge | m³/s |
| 3 | Vattenstånd — water level | cm |
| 4 | Vattendragstemperatur — water temperature | °C |
| 5 / 6 | Isläggning / Islossning — ice on/off | date |
| 7 | Istjocklek — ice thickness | cm |
| 8 | Snödensitet — snow density | g/cm³ |
| 9 | Vatteninnehåll — snow water content | mm |
| 10 | Vattenföring (Månad) — discharge, monthly | m³/s |

### Station discovery & response shape

`parameter/{p}.json` returns a `station` array; each entry has `key`, `id`, `name`,
`latitude`, `longitude`, `active`, `owner`, `catchmentName`, plus links to drill in.
Example confirmed entries for parameter 1 (daily discharge): `2357 ABISKO`
(68.1936, 19.9859, active), `2000 ACKSJÖN NEDRE` (inactive). Data responses contain a
`value` array of `{date, value, quality}` objects.

### Example call

```python
import requests
HYD = "https://opendata-download-hydroobs.smhi.se"
params = requests.get(f"{HYD}/api/version/latest.json", timeout=30).json()["resource"]
stations = requests.get(f"{HYD}/api/version/latest/parameter/1.json", timeout=30).json()["station"]
```

### License

**Creative Commons Attribution 4.0 International (CC BY 4.0).** Free for any use including
commercial; attribute SMHI as the source.

---

## Sources

- NVE Magasinstatistikk docs — https://api.nve.no/doc/magasinstatistikk/
- NVE Swagger — https://biapi.nve.no/magasinstatistikk/swagger/index.html
- NVE about-page — https://www.nve.no/energi/analyser-og-statistikk/om-magasinstatistikken/
- data.norge.no dataset — https://data.norge.no/en/datasets/01decbac-3cf4-3548-83da-2f991f25bbce/magasinstatistikk
- SMHI hydroobs portal — https://opendata.smhi.se/hydroobs/introduction
- SMHI hydroobs API entry — https://opendata-download-hydroobs.smhi.se/api.json
- SMHI open data license (CC BY 4.0) — https://opendata.smhi.se/ / https://www.smhi.se/en/services/open-data
