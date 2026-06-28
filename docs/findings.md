# Research log

Running notes on what each exploration showed. Newest first. Keep entries short
and sourced; link to the notebook or script that produced each figure.

---

## 2026-06-27 — Scaffold

Initialized the workspace and verified all five data sources against their live
APIs (see `docs/sources/`). Decided to build ingestion on `entsoe-py` rather than
reinvent it; the tidy multi-source Nordic layer is written fresh (no European
equivalent of `gridstatus` exists). No analytical findings yet — that starts once
day-ahead prices + fundamentals are flowing.

<!-- Template for new entries:
## YYYY-MM-DD — <title>
**Question:** ...
**What I did:** ... (notebook/script: ...)
**Finding:** ...
**Caveats / next:** ...
-->
