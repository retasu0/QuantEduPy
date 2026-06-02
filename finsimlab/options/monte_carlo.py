"""Monte Carlo pricing for European options."""

from __future__ import annotations

from math import exp, sqrt

import numpy as np

from finsimlab.options.payoff import call_payoff, put_payoff
from finsimlab.simulations._utils import (
    make_rng,
    require_non_negative,
    require_positive,
    require_positive_int,
    require_real,
)


def monte_carlo_option_price(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str = "call",
    n_paths: int = 10_000,
    seed: int | None = None,
) -> float:
    """Estimate a European option price by risk-neutral Monte Carlo simulation."""
    spot = require_positive("spot", spot)
    strike = require_positive("strike", strike)
    time_to_maturity = require_positive("time_to_maturity", time_to_maturity)
    risk_free_rate = require_real("risk_free_rate", risk_free_rate)
    volatility = require_non_negative("volatility", volatility)
    n_paths = require_positive_int("n_paths", n_paths)
    option_type = _validate_option_type(option_type)

    if volatility == 0.0:
        terminal_prices = np.array([spot * exp(risk_free_rate * time_to_maturity)])
    else:
        rng = make_rng(seed)
        shocks = rng.normal(loc=0.0, scale=1.0, size=n_paths)
        terminal_prices = spot * np.exp(
            (risk_free_rate - 0.5 * volatility**2) * time_to_maturity
            + volatility * sqrt(time_to_maturity) * shocks
        )

    if option_type == "call":
        payoffs = call_payoff(terminal_prices, strike=strike)
    else:
        payoffs = put_payoff(terminal_prices, strike=strike)

    discount_factor = exp(-risk_free_rate * time_to_maturity)
    return float(discount_factor * np.mean(payoffs))


def _validate_option_type(option_type: str) -> str:
    if option_type not in {"call", "put"}:
        raise ValueError('option_type must be "call" or "put".')
    return option_type
