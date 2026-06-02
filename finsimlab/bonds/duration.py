"""Duration and convexity for fixed-coupon bonds."""

from __future__ import annotations

import numpy as np

from finsimlab.bonds.pricing import (
    _require_real,
    discount_factor,
    fixed_coupon_bond_cash_flows,
    fixed_coupon_bond_price,
)


def _discounted_bond_cash_flows(
    *,
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    payments_per_year: int = 1,
) -> tuple[np.ndarray, np.ndarray, float]:
    yield_to_maturity = _require_real("yield_to_maturity", yield_to_maturity)
    cash_flows, times = fixed_coupon_bond_cash_flows(
        face_value=face_value,
        coupon_rate=coupon_rate,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    factors = np.array(
        [
            discount_factor(
                yield_to_maturity,
                time,
                payments_per_year=payments_per_year,
            )
            for time in times
        ],
        dtype=float,
    )
    discounted = cash_flows * factors
    price = float(np.sum(discounted))
    return discounted, times, price


def macaulay_duration(
    *,
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    payments_per_year: int = 1,
) -> float:
    """Calculate Macaulay duration in years."""
    discounted, times, price = _discounted_bond_cash_flows(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_to_maturity=yield_to_maturity,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    return float(np.sum(times * discounted) / price)


def modified_duration(
    *,
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    payments_per_year: int = 1,
) -> float:
    """Calculate modified duration for periodic compounding."""
    macaulay = macaulay_duration(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_to_maturity=yield_to_maturity,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    denominator = 1.0 + yield_to_maturity / payments_per_year
    if denominator <= 0:
        raise ValueError("yield_to_maturity is too low for periodic compounding.")
    return float(macaulay / denominator)


def bond_convexity(
    *,
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    payments_per_year: int = 1,
) -> float:
    """Calculate fixed-coupon bond convexity for periodic compounding."""
    discounted, times, price = _discounted_bond_cash_flows(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_to_maturity=yield_to_maturity,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    denominator = (1.0 + yield_to_maturity / payments_per_year) ** 2
    if denominator <= 0:
        raise ValueError("yield_to_maturity is too low for periodic compounding.")
    convexity_terms = times * (times + 1.0 / payments_per_year)
    return float(np.sum(convexity_terms * discounted) / (price * denominator))


def duration_price_change_approximation(
    *,
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    yield_change: float,
    payments_per_year: int = 1,
    include_convexity: bool = True,
) -> float:
    """Approximate price change from a small yield change."""
    yield_change = _require_real("yield_change", yield_change)
    price = fixed_coupon_bond_price(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_to_maturity=yield_to_maturity,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    modified = modified_duration(
        face_value=face_value,
        coupon_rate=coupon_rate,
        yield_to_maturity=yield_to_maturity,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    approximation = -modified * yield_change * price
    if include_convexity:
        convexity = bond_convexity(
            face_value=face_value,
            coupon_rate=coupon_rate,
            yield_to_maturity=yield_to_maturity,
            years_to_maturity=years_to_maturity,
            payments_per_year=payments_per_year,
        )
        approximation += 0.5 * convexity * yield_change**2 * price
    return float(approximation)
