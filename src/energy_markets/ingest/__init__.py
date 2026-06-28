"""Ingestion (I/O) — one module per public source.

Each loader fetches, caches to data/raw/, and returns a tidy pandas frame:
    ingest.entsoe         day-ahead prices, load (free token required)
    ingest.weather        Open-Meteo historical weather (keyless)
    ingest.hydro          NVE reservoir filling (keyless)
    ingest.energy_charts  price + generation-mix cross-check (keyless)

Imported lazily by callers so that offline transform tests never need the
network or third-party clients.
"""
