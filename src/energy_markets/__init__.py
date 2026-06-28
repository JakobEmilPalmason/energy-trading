"""Nordic power markets research toolkit.

Sub-packages:
    ingest      I/O: fetch + cache data from public sources (one module per source).
    transform   pure functions (no I/O): reshape, spreads, resampling.
    features    feature builders (Phase 2).
    plotting    matplotlib helpers.

Zone metadata (EIC codes, coordinates, per-source codes) lives in `zones.py`.
"""

__version__ = "0.1.0"
