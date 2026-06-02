"""Present value and fixed-coupon bond pricing helpers."""

from __future__ import annotations

from math import exp
from numbers import Real

import numpy as np


def _require_real(name: str, value: Real) -> float:
    if not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite.")
    return result


def _require_positive(name: str, value: Real) -> float:
    result = _require_real(name, value)
    if result <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return result


def _require_non_negative(name: str, value: Real) -> float:
    result = _require_real(name, value)
    if result < 0:
        raise ValueError(f"{name} must be greater than or equal to 0.")
    return result


def _require_positive_int(name: str, value: int) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return value


def _as_finite_array(name: str, values) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.size == 0:
        raise ValueError(f"{name} must not be empty.")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values.")
    return result


def _validate_rate_for_periodic_compounding(
    rate: float,
    payments_per_year: int,
) -> None:
    if 1.0 + rate / payments_per_year <= 0:
        raise ValueError("rate is too low for periodic compounding.")


def discount_factor(
    rate: float,
    time: float,
    *,
    compounding: str = "annual",
    payments_per_year: int = 1,
) -> float:
    """Calculate a discount factor for a future cash flow.

    ``compounding='annual'`` uses periodic compounding with
    ``payments_per_year``. ``compounding='continuous'`` uses ``exp(-rate*time)``.
    """
    rate = _require_real("rate", rate)
    time = _require_non_negative("time", time)
    payments_per_year = _require_positive_int("payments_per_year", payments_per_year)

    if compounding == "annual":
        _validate_rate_for_periodic_compounding(rate, payments_per_year)
        return float((1.0 + rate / payments_per_year) ** (-payments_per_year * time))
    if compounding == "continuous":
        return float(exp(-rate * time))
    raise ValueError("compounding must be 'annual' or 'continuous'.")


def present_value(
    cash_flows,
    times,
    rate: float,
    *,
    compounding: str = "annual",
    payments_per_year: int = 1,
) -> float:
    """Calculate the present value of dated cash flows."""
    cash_flows = _as_finite_array("cash_flows", cash_flows)
    times = _as_finite_array("times", times)
    if cash_flows.shape != times.shape:
        raise ValueError("cash_flows and times must have the same shape.")
    if np.any(times < 0):
        raise ValueError("times must be greater than or equal to 0.")

    factors = np.array(
        [
            discount_factor(
                rate,
                time,
                compounding=compounding,
                payments_per_year=payments_per_year,
            )
            for time in times
        ],
        dtype=float,
    )
    return float(np.sum(cash_flows * factors))


def _bond_period_count(years_to_maturity: float, payments_per_year: int) -> int:
    raw_periods = years_to_maturity * payments_per_year
    periods = int(round(raw_periods))
    if not np.isclose(raw_periods, periods):
        raise ValueError("years_to_maturity must align with payments_per_year.")
    return periods


def fixed_coupon_bond_cash_flows(
    *,
    face_value: float,
    coupon_rate: float,
    years_to_maturity: float,
    payments_per_year: int = 1,
) -> tuple[np.ndarray, np.ndarray]:
    """Return cash flows and payment times for a fixed-coupon bond."""
    face_value = _require_positive("face_value", face_value)
    coupon_rate = _require_non_negative("coupon_rate", coupon_rate)
    years_to_maturity = _require_positive("years_to_maturity", years_to_maturity)
    payments_per_year = _require_positive_int("payments_per_year", payments_per_year)

    periods = _bond_period_count(years_to_maturity, payments_per_year)
    coupon = face_value * coupon_rate / payments_per_year
    cash_flows = np.full(periods, coupon, dtype=float)
    cash_flows[-1] += face_value
    times = np.arange(1, periods + 1, dtype=float) / payments_per_year
    return cash_flows, times


def fixed_coupon_bond_price(
    *,
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years_to_maturity: float,
    payments_per_year: int = 1,
) -> float:
    """Price a fixed-coupon bond by discounting each cash flow."""
    yield_to_maturity = _require_real("yield_to_maturity", yield_to_maturity)
    cash_flows, times = fixed_coupon_bond_cash_flows(
        face_value=face_value,
        coupon_rate=coupon_rate,
        years_to_maturity=years_to_maturity,
        payments_per_year=payments_per_year,
    )
    return present_value(
        cash_flows,
        times,
        yield_to_maturity,
        payments_per_year=payments_per_year,
    )
