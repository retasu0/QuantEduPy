"""Random long-only portfolios for educational frontier examples."""

from __future__ import annotations

import numpy as np

from finsimlab.portfolio.metrics import (
    _as_covariance_matrix,
    _as_vector,
    _require_real,
    portfolio_return,
    portfolio_sharpe_ratio,
    portfolio_volatility,
)
from finsimlab.simulations._utils import make_rng, require_positive_int


def generate_random_weights(
    n_assets: int,
    *,
    n_portfolios: int = 1000,
    seed: int | None = None,
) -> np.ndarray:
    """Generate random long-only weights whose rows sum to 1."""
    n_assets = require_positive_int("n_assets", n_assets)
    n_portfolios = require_positive_int("n_portfolios", n_portfolios)
    rng = make_rng(seed)
    return rng.dirichlet(np.ones(n_assets), size=n_portfolios)


def generate_random_portfolios(
    expected_returns,
    covariance_matrix,
    *,
    n_portfolios: int = 1000,
    risk_free_rate: float = 0.0,
    seed: int | None = None,
) -> dict[str, np.ndarray]:
    """Generate random long-only portfolios and their risk/return metrics."""
    expected_returns = _as_vector("expected_returns", expected_returns)
    covariance_matrix = _as_covariance_matrix(covariance_matrix)
    if covariance_matrix.shape[0] != expected_returns.shape[0]:
        raise ValueError("covariance_matrix shape must match expected_returns.")
    risk_free_rate = _require_real("risk_free_rate", risk_free_rate)

    weights = generate_random_weights(
        expected_returns.shape[0],
        n_portfolios=n_portfolios,
        seed=seed,
    )
    returns = np.array(
        [portfolio_return(expected_returns, row) for row in weights],
        dtype=float,
    )
    volatilities = np.array(
        [portfolio_volatility(covariance_matrix, row) for row in weights],
        dtype=float,
    )
    sharpe_ratios = np.array(
        [
            portfolio_sharpe_ratio(
                portfolio_return_value,
                volatility_value,
                risk_free_rate=risk_free_rate,
            )
            for portfolio_return_value, volatility_value in zip(
                returns,
                volatilities,
                strict=True,
            )
        ],
        dtype=float,
    )
    return {
        "weights": weights,
        "returns": returns,
        "volatility": volatilities,
        "sharpe_ratio": sharpe_ratios,
    }
