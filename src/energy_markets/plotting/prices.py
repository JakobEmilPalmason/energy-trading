"""Quick matplotlib helpers for prices and spreads."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_price_series(prices_wide: pd.DataFrame, *, ax=None, title: str = "Day-ahead prices"):
    """Line plot of one column per zone."""
    ax = ax or plt.gca()
    prices_wide.plot(ax=ax)
    ax.set_ylabel("EUR/MWh")
    ax.set_xlabel("")
    ax.set_title(title)
    ax.legend(title="zone")
    return ax


def plot_spread(spread: pd.Series, *, ax=None):
    """Line plot of a zone spread, with a zero reference line."""
    ax = ax or plt.gca()
    spread.plot(ax=ax, color="tab:red")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("EUR/MWh")
    ax.set_xlabel("")
    ax.set_title(str(spread.name) if spread.name is not None else "spread")
    return ax
