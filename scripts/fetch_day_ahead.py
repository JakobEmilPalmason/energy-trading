"""Fetch day-ahead prices for one or more zones and save a wide parquet.

Usage:
    uv run python scripts/fetch_day_ahead.py --zones DK1 DK2 \
        --start 2026-01-01 --end 2026-02-01

Requires ENTSOE_API_KEY in .env (see docs/sources/entsoe.md). Per-zone pulls are
cached under data/raw/; the combined wide frame lands in data/processed/.
"""

from __future__ import annotations

import argparse

from energy_markets.config import PROCESSED_DIR, REPO_ROOT, ensure_data_dirs
from energy_markets.ingest.entsoe import fetch_day_ahead_prices
from energy_markets.transform.spreads import prices_to_wide


def main() -> None:
    p = argparse.ArgumentParser(description="Fetch Nordic day-ahead prices (ENTSO-E).")
    p.add_argument("--zones", nargs="+", default=["DK1", "DK2"])
    p.add_argument("--start", required=True, help="YYYY-MM-DD (inclusive)")
    p.add_argument("--end", required=True, help="YYYY-MM-DD (exclusive)")
    p.add_argument("--refresh", action="store_true", help="ignore the cache and re-fetch")
    args = p.parse_args()

    ensure_data_dirs()
    by_zone = {}
    for zone in args.zones:
        df = fetch_day_ahead_prices(zone, args.start, args.end, refresh=args.refresh)
        by_zone[zone] = df
        print(f"{zone}: {len(df)} rows  {df.index.min()} .. {df.index.max()}")

    wide = prices_to_wide(by_zone)
    out = PROCESSED_DIR / f"day_ahead_{'_'.join(args.zones)}_{args.start}_{args.end}.parquet"
    wide.to_parquet(out)
    print(f"wrote {out.relative_to(REPO_ROOT)}  shape={wide.shape}")


if __name__ == "__main__":
    main()
