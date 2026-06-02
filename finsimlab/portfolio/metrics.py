"""Basic mean-variance portfolio metrics."""

from __future__ import annotations

from numbers import Real

import numpy as np


def _as_finite_array(name: str, values) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.size == 0:
        raise ValueError(f"{name} must not be empty.")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values.")
    return result


def _as_vector(name: str, values) -> np.ndarray:
    result = _as_finite_array(name, values)
    if result.ndim != 1:
        raise ValueError(f"{name} must be a 1D array.")
    return result


def _as_covariance_matrix(values) -> np.ndarray:
    matrix = _as_finite_array("covariance_matrix", values)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("covariance_matrix must be a square 2D array.")
    return matrix


def _validate_weights(weights, *, n_assets: int | None = None) -> np.ndarray:
    result = _as_vector("weights", weights)
    if n_assets is not None and result.shape[0] != n_assets:
        raise ValueError("weights must have one value per asset.")
    if np.any(result < 0):
        raise ValueError("weights must be greater than or equal to 0.")
    if not np.isclose(np.sum(result), 1.0):
        raise ValueError("weights must sum to 1.")
    return result


def _require_real(name: str, value: Real) -> float:
    if not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite.")
    return result


def portfolio_return(expected_returns, weights) -> float:
    """Calculate expected portfolio return as ``weights dot returns``."""
    returns = _as_vector("expected_returns", expected_returns)
    weights = _validate_weights(weights, n_assets=returns.shape[0])
    return float(np.dot(weights, returns))


def portfolio_variance(covariance_matrix, weights) -> float:
    """Calculate portfolio variance as ``w.T @ covariance @ w``."""
    covariance_matrix = _as_covariance_matrix(covariance_matrix)
    weights = _validate_weights(weights, n_assets=covariance_matrix.shape[0])
    return float(weights.T @ covariance_matrix @ weights)


def portfolio_volatility(covariance_matrix, weights) -> float:
    """Calculate portfolio volatility from a covariance matrix and weights."""
    variance = portfolio_variance(covariance_matrix, weights)
    if variance < 0 and np.isclose(variance, 0.0):
        variance = 0.0
    if variance < 0:
        raise ValueError("portfolio variance must not be negative.")
    return float(np.sqrt(variance))


def portfolio_sharpe_ratio(
    expected_return: float,
    volatility: float,
    *,
    risk_free_rate: float = 0.0,
) -> float:
    """Calculate a simple Sharpe ratio."""
    expected_return = _require_real("expected_return", expected_return)
    volatility = _require_real("volatility", volatility)
    risk_free_rate = _require_real("risk_free_rate", risk_free_rate)
    if volatility <= 0:
        raise ValueError("volatility must be greater than 0.")
    return float((expected_return - risk_free_rate) / volatility)
