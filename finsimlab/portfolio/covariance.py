"""Covariance and correlation helpers for asset return matrices."""

from __future__ import annotations

import numpy as np

from finsimlab.portfolio.metrics import _as_finite_array


def _require_non_negative_int(name: str, value: int) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value < 0:
        raise ValueError(f"{name} must be greater than or equal to 0.")
    return value


def _return_matrix(returns) -> np.ndarray:
    values = _as_finite_array("returns", returns)
    if values.ndim == 1:
        values = values.reshape(-1, 1)
    if values.ndim != 2:
        raise ValueError("returns must be a 1D or 2D array.")
    if values.shape[0] < 2:
        raise ValueError("returns must contain at least two observations.")
    return values


def asset_covariance_matrix(returns, *, ddof: int = 1) -> np.ndarray:
    """Estimate an asset covariance matrix from return observations.

    Rows are observations and columns are assets. A 1D return series is treated
    as one asset and returns a ``(1, 1)`` matrix.
    """
    values = _return_matrix(returns)
    ddof = _require_non_negative_int("ddof", ddof)
    if values.shape[0] <= ddof:
        raise ValueError("returns must contain more observations than ddof.")
    result = np.cov(values, rowvar=False, ddof=ddof)
    return np.atleast_2d(result).astype(float)


def asset_correlation_matrix(returns) -> np.ndarray:
    """Estimate an asset correlation matrix from return observations."""
    values = _return_matrix(returns)
    result = np.corrcoef(values, rowvar=False)
    return np.atleast_2d(result).astype(float)
