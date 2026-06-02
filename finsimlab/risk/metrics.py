"""Basic risk metrics."""

from __future__ import annotations

import numpy as np

from finsimlab.risk.returns import _as_finite_array, _normalize_axis


def _require_non_negative_int(name: str, value: int) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < 0:
        raise ValueError(f"{name} must be greater than or equal to 0.")
    return value


def _require_positive_int(name: str, value: int) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return value


def _scalar_or_array(value):
    array = np.asarray(value)
    if array.ndim == 0:
        return float(array)
    return value


def volatility(
    returns,
    *,
    annualize: bool = False,
    periods_per_year: int = 252,
    ddof: int = 1,
    axis: int | None = 0,
) -> np.ndarray | float:
    """Calculate return volatility.

    When ``annualize`` is true, the result is multiplied by
    ``sqrt(periods_per_year)``. The default ``axis=0`` matches simulated path
    arrays with time along rows.
    """
    values = _as_finite_array("returns", returns)
    ddof = _require_non_negative_int("ddof", ddof)
    periods_per_year = _require_positive_int("periods_per_year", periods_per_year)

    if axis is None:
        observations = values.size
    else:
        axis = _normalize_axis(axis, values.ndim)
        observations = values.shape[axis]

    if observations <= ddof:
        raise ValueError("returns must contain more observations than ddof.")

    result = np.std(values, axis=axis, ddof=ddof)
    if annualize:
        result = result * np.sqrt(periods_per_year)

    return _scalar_or_array(result)

