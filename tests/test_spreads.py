"""Offline tests for the pure price transforms — no network, no token."""

from __future__ import annotations

import pandas as pd
import pytest

from energy_markets.transform.spreads import prices_to_wide, zone_spread


def _series(values, tz="Europe/Copenhagen"):
    idx = pd.date_range("2026-01-01", periods=len(values), freq="h", tz=tz)
    return pd.Series(values, index=idx)


def test_prices_to_wide_combines_zones():
    wide = prices_to_wide({"DK1": _series([10, 20, 30]), "DK2": _series([15, 25, 35])})
    assert list(wide.columns) == ["DK1", "DK2"]
    assert len(wide) == 3


def test_prices_to_wide_accepts_single_column_frames():
    df = _series([1, 2, 3]).rename("price_eur_mwh").to_frame()
    wide = prices_to_wide({"DK1": df})
    assert wide["DK1"].tolist() == [1, 2, 3]


def test_prices_to_wide_aligns_across_timezones():
    # DK2 (Copenhagen) and FI (Helsinki, +1h) overlap by two instants once in UTC.
    dk = _series([10, 20, 30], tz="Europe/Copenhagen")
    fi = _series([11, 21, 31], tz="Europe/Helsinki")
    wide = prices_to_wide({"DK2": dk, "FI": fi})
    overlap = wide.dropna()
    assert len(overlap) == 2
    assert str(wide.index.tz) == "UTC"


def test_zone_spread_sign_and_values():
    wide = prices_to_wide({"DK1": _series([10, 20, 30]), "DK2": _series([15, 18, 30])})
    spread = zone_spread(wide, "DK1", "DK2")
    assert spread.name == "DK1_minus_DK2"
    assert spread.tolist() == [-5, 2, 0]


def test_zone_spread_unknown_zone_raises():
    wide = prices_to_wide({"DK1": _series([1, 2])})
    with pytest.raises(KeyError):
        zone_spread(wide, "DK1", "DK2")
