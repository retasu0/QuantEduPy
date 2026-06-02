"""Black-Scholes pricing for European options."""

from __future__ import annotations

from math import erf, exp, log, pi, sqrt

from finsimlab.simulations._utils import (
    require_non_negative,
    require_positive,
    require_real,
)


def standard_normal_cdf(value: float) -> float:
    """Return the cumulative probability of the standard normal distribution."""
    return 0.5 * (1.0 + erf(value / sqrt(2.0)))


def standard_normal_pdf(value: float) -> float:
    """Return the density of the standard normal distribution."""
    return exp(-0.5 * value**2) / sqrt(2.0 * pi)


def black_scholes_call(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Price a European call option with the Black-Scholes formula."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )

    if volatility == 0.0:
        return max(spot - strike * exp(-risk_free_rate * time_to_maturity), 0.0)

    d1, d2 = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    discounted_strike = strike * exp(-risk_free_rate * time_to_maturity)
    return spot * standard_normal_cdf(d1) - discounted_strike * standard_normal_cdf(d2)


def black_scholes_put(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> float:
    """Price a European put option with the Black-Scholes formula."""
    spot, strike, time_to_maturity, risk_free_rate, volatility = _validate_inputs(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )

    if volatility == 0.0:
        return max(strike * exp(-risk_free_rate * time_to_maturity) - spot, 0.0)

    d1, d2 = _d1_d2(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    discounted_strike = strike * exp(-risk_free_rate * time_to_maturity)
    return discounted_strike * standard_normal_cdf(-d2) - spot * standard_normal_cdf(-d1)


def _validate_inputs(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> tuple[float, float, float, float, float]:
    return (
        require_positive("spot", spot),
        require_positive("strike", strike),
        require_positive("time_to_maturity", time_to_maturity),
        require_real("risk_free_rate", risk_free_rate),
        require_non_negative("volatility", volatility),
    )


def _d1_d2(
    *,
    spot: float,
    strike: float,
    time_to_maturity: float,
    risk_free_rate: float,
    volatility: float,
) -> tuple[float, float]:
    denominator = volatility * sqrt(time_to_maturity)
    d1 = (
        log(spot / strike)
        + (risk_free_rate + 0.5 * volatility**2) * time_to_maturity
    ) / denominator
    d2 = d1 - denominator
    return d1, d2
