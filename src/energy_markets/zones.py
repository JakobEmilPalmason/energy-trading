"""Single source of truth for Nordic bidding-zone metadata.

EIC codes verified 2026-06-27 against entsoe-py `mappings.py`; reference
coordinates and per-source codes from docs/sources/*.md. The source APIs disagree
on identifiers (ENTSO-E uses EIC / aliases, energy-charts splits country vs bzn,
NVE uses integer elspot-area numbers) — keep all of that mapping here, nowhere else.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Zone:
    code: str  # our canonical short code, e.g. "DK1"
    eic: str  # ENTSO-E EIC code
    entsoe_alias: str  # entsoe-py Area enum name, e.g. "DK_1"
    tz: str  # IANA timezone
    lat: float  # representative point for weather (Open-Meteo)
    lon: float
    ec_country: str  # energy-charts /public_power country code (dk/no/se/fi)
    nve_area: int | None  # NVE elspot-area number (NO1..NO5 -> 1..5); else None

    @property
    def ec_bzn(self) -> str:
        """energy-charts /price uses the bidding-zone code, identical to ours."""
        return self.code


# fmt: off
ZONES: dict[str, Zone] = {
    "DK1": Zone("DK1", "10YDK-1--------W", "DK_1", "Europe/Copenhagen", 55.47,  8.45, "dk", None),
    "DK2": Zone("DK2", "10YDK-2--------M", "DK_2", "Europe/Copenhagen", 55.68, 12.57, "dk", None),
    "NO1": Zone("NO1", "10YNO-1--------2", "NO_1", "Europe/Oslo",       59.91, 10.75, "no", 1),
    "NO2": Zone("NO2", "10YNO-2--------T", "NO_2", "Europe/Oslo",       58.15,  7.99, "no", 2),
    "NO3": Zone("NO3", "10YNO-3--------J", "NO_3", "Europe/Oslo",       63.43, 10.39, "no", 3),
    "NO4": Zone("NO4", "10YNO-4--------9", "NO_4", "Europe/Oslo",       69.65, 18.96, "no", 4),
    "NO5": Zone("NO5", "10Y1001A1001A48H", "NO_5", "Europe/Oslo",       60.39,  5.32, "no", 5),
    "SE1": Zone("SE1", "10Y1001A1001A44P", "SE_1", "Europe/Stockholm",  65.58, 22.15, "se", None),
    "SE2": Zone("SE2", "10Y1001A1001A45N", "SE_2", "Europe/Stockholm",  62.39, 17.31, "se", None),
    "SE3": Zone("SE3", "10Y1001A1001A46L", "SE_3", "Europe/Stockholm",  59.33, 18.07, "se", None),
    "SE4": Zone("SE4", "10Y1001A1001A47J", "SE_4", "Europe/Stockholm",  55.60, 13.00, "se", None),
    "FI":  Zone("FI",  "10YFI-1--------U", "FI",   "Europe/Helsinki",   60.17, 24.94, "fi", None),
}
# fmt: on


def get_zone(code: str) -> Zone:
    """Look up a zone by its canonical code (case-insensitive)."""
    try:
        return ZONES[code.upper()]
    except KeyError:
        raise KeyError(f"Unknown zone {code!r}. Known: {', '.join(ZONES)}") from None
