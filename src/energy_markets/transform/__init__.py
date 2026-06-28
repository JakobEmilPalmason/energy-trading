"""Pure transforms (no I/O) — safe to unit-test offline."""

from energy_markets.transform.spreads import prices_to_wide, zone_spread

__all__ = ["prices_to_wide", "zone_spread"]
