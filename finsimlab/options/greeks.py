"""Basic Black-Scholes Greeks for European options."""

from __future__ import annotations

from math import exp, sqrt

from finsimlab.options.black_scholes import (
    _d1_d2,
    _validate_inputs,
    standard_normal_cdf,
    standard_normal_pdf,
)


def black_scholes_delta(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str = "call",
) -> float:
    """Return Black-Scholes delta for a European call or put."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_greek_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    option_type = _validate_option_type(option_type)
    d1, _ = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    if option_type == "call":
        return standard_normal_cdf(d1)
    return standard_normal_cdf(d1) - 1.0


def black_scholes_gamma(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Return Black-Scholes gamma."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_greek_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    d1, _ = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    return standard_normal_pdf(d1) / (spot * volatility * sqrt(time_to_maturity))


def black_scholes_vega(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Return Black-Scholes vega for a 1.0 change in volatility."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_greek_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    d1, _ = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    return spot * standard_normal_pdf(d1) * sqrt(time_to_maturity)


def black_scholes_theta(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str = "call",
) -> float:
    """Return Black-Scholes theta per year for a European call or put."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_greek_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    option_type = _validate_option_type(option_type)
    d1, d2 = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    first_term = -(
        spot * standard_normal_pdf(d1) * volatility / (2.0 * sqrt(time_to_maturity))
    )
    discounted_strike = strike * exp(-risk_free_rate * time_to_maturity)
    if option_type == "call":
        return first_term - risk_free_rate * discounted_strike * standard_normal_cdf(d2)
    return first_term + risk_free_rate * discounted_strike * standard_normal_cdf(-d2)


def black_scholes_rho(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
    option_type: str = "call",
) -> float:
    """Return Black-Scholes rho for a 1.0 change in the risk-free rate."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_greek_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    option_type = _validate_option_type(option_type)
    _, d2 = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    discounted_strike = strike * exp(-risk_free_rate * time_to_maturity)
    if option_type == "call":
        return time_to_maturity * discounted_strike * standard_normal_cdf(d2)
    return -time_to_maturity * discounted_strike * standard_normal_cdf(-d2)


def _validate_greek_inputs(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> tuple[float, float, float, float, float]:
    values = _validate_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    if values[4] <= 0:
        raise ValueError("volatility must be greater than 0 for Greeks.")
    return values


def _validate_option_type(option_type: str) -> str:
    if option_type not in {"call", "put"}:
        raise ValueError('option_type must be "call" or "put".')
    return option_type
