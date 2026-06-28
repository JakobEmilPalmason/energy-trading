# Energy Markets Research — Conventions

Read `PROJECT.md` for scope and goals. This file is the rulebook for working in
the repo.

## Hard rules

- **No employer, company, recruiter, or interview references anywhere** — code,
  comments, commits, docs. This is a personal, public-source research project.
- **Never commit data or secrets.** Everything under `data/` and `.env` is
  gitignored. Commit `.env.example` instead.
- **Every figure traces to a public source.** No invented numbers. When you add a
  data source, document its endpoint + license in `docs/sources/` first.

## Stack

- **Python 3.12**, managed with **uv** (`uv sync`, `uv run`). Lockfile committed.
- **Ruff** for lint + format. **pytest** for tests. Type hints on public functions.
- **pandas** for analysis; **entsoe-py** as the ENTSO-E ingestion spine;
  **requests** for the keyless REST sources; **matplotlib** for plotting.

## Layout

```
src/energy_markets/     importable package
  ingest/             I/O — one module per source. Functions FETCH, cache, return tidy frames.
  transform/          pure functions only (no I/O) — reshape, spreads, resampling.
  features/           feature builders (Phase 2).
  plotting/           matplotlib helpers.
  zones.py            single source of truth for zone metadata (EIC, coords, source codes).
  config.py           paths + token loading; creates data dirs at runtime.
scripts/              runnable entry points.
notebooks/            exploration (strip heavy output before commit).
data/                 GITIGNORED — raw/ (API cache) and processed/.
docs/                 market-primer.md, sources/*.md (verified specs), data-sources.md, findings.md.
tests/                fast, OFFLINE tests on the pure transforms (no network, no token).
.github/workflows/    lint + test on push.
```

## Data discipline

- **Cache API pulls to `data/raw/`** so endpoints aren't hammered on every run.
  The ENTSO-E rate limit is 400 req/min; energy-charts returns 429 on bursts.
- **Keep ingestion (I/O) separate from transforms (pure functions) separate from
  plotting.** Pure functions are testable; I/O is not (so tests stay offline).
- **Zone codes live in `zones.py` only.** Don't scatter EIC strings or coordinates
  through the codebase — the source APIs disagree on codes (e.g. energy-charts
  uses `country` for generation but `bzn` for price; NVE uses integer area numbers).
- ENTSO-E token loaded from `.env` via `config.get_entsoe_api_key()`. The API is
  UTC — always pass tz-aware `pandas.Timestamp`s.
- **`fyllingsgrad` (NVE) is a fraction, not a percent** — multiply by 100 to display.

## Working with the verified specs

`docs/sources/*.md` were verified against live APIs on 2026-06-27 and are the
source of truth for endpoints, params, response shapes and licenses. If an API
seems to behave differently, re-verify and update the spec rather than guessing.
Known trap: `entsoe-py` `query_intraday_offered_capacity` is broken post-IDA
(upstream issue #527) — avoid it.

## Workflow

- Small, focused commits. Branch for anything non-trivial.
- Update `docs/findings.md` when an analysis shows something worth remembering.
- When unsure about market mechanics (bidding zones, coupling, hydro, intraday),
  state the assumption in a comment rather than guessing silently, and check
  `docs/market-primer.md`.
- Run `uv run ruff check . && uv run pytest` before committing.
