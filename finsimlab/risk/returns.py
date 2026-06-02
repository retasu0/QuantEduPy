"""Return calculations for price series."""

from __future__ import annotations

import numpy as np


def _as_finite_array(name: str, values) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.size == 0:
        raise ValueError(f"{name} must not be empty.")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values.")
    return result


def _normalize_axis(axis: int, ndim: int) -> int:
    if not isinstance(axis, int):
        raise TypeError("axis must be an integer.")
    if axis < 0:
        axis += ndim
    if axis < 0 or axis >= ndim:
        raise ValueError("axis is out of range for the input array.")
    return axis


def calculate_returns(
    prices,
    *,
    method: str = "simple",
    axis: int = 0,
) -> np.ndarray:
    """Calculate simple or log returns from price observations.

    ``prices`` may be a 1D series or a 2D array of simulated paths. The
    default ``axis=0`` matches FinSimLab simulations, where rows are time steps
    and columns are paths.
    """
    values = _as_finite_array("prices", prices)
    axis = _normalize_axis(axis, values.ndim)
    if values.shape[axis] < 2:
        raise ValueError("prices must contain at least two observations.")
    if np.any(values <= 0):
        raise ValueError("prices must be greater than 0.")

    moved = np.moveaxis(values, axis, 0)
    previous = moved[:-1]
    current = moved[1:]

    if method == "simple":
        returns = current / previous - 1.0
    elif method == "log":
        returns = np.log(current / previous)
    else:
        raise ValueError("method must be 'simple' or 'log'.")

    return np.moveaxis(returns, 0, axis)


def losses_from_returns(
    returns,
    *,
    portfolio_value: float = 1.0,
) -> np.ndarray:
    """Convert returns into losses, where positive values mean losses.

    A return of ``-0.05`` on a portfolio worth ``1000`` becomes a loss of
    ``50``. Positive returns become negative losses, representing gains.
    """
    values = _as_finite_array("returns", returns)
    portfolio_value = float(portfolio_value)
    if not np.isfinite(portfolio_value):
        raise ValueError("portfolio_value must be finite.")
    if portfolio_value <= 0:
        raise ValueError("portfolio_value must be greater than 0.")

    return -values * portfolio_value

