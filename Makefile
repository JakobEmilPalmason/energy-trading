.PHONY: setup lint format test fetch clean

# One-command dev setup (installs runtime + dev deps into a uv-managed venv).
setup:
	uv sync --extra dev
	cp -n .env.example .env || true
	@echo "Edit .env and add your ENTSOE_API_KEY (see docs/sources/entsoe.md)."

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

# Pull DK1 + DK2 day-ahead prices for a date range into data/processed/.
# Usage: make fetch START=2026-01-01 END=2026-02-01
fetch:
	uv run python scripts/fetch_day_ahead.py --zones DK1 DK2 --start $(START) --end $(END)

clean:
	rm -rf .ruff_cache .pytest_cache **/__pycache__
