"""Payoff helpers for simple European options."""

from __future__ import annotations

import numpy as np

from finsimlab.simulations._utils import require_positive


def call_payoff(prices, *, strike: float) -> np.ndarray:
    """Return European call payoffs for one or more terminal prices."""
    strike = require_positive("strike", strike)
    prices_array = np.asarray(prices, dtype=float)
    return np.maximum(prices_array - strike, 0.0)


def put_payoff(prices, *, strike: float) -> np.ndarray:
    """Return European put payoffs for one or more terminal prices."""
    strike = require_positive("strike", strike)
    prices_array = np.asarray(prices, dtype=float)
    return np.maximum(strike - prices_array, 0.0)
