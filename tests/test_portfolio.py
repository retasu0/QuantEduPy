import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from finsimlab.portfolio import (
    asset_correlation_matrix,
    asset_covariance_matrix,
    generate_random_portfolios,
    generate_random_weights,
    plot_efficient_frontier,
    portfolio_return,
    portfolio_sharpe_ratio,
    portfolio_variance,
    portfolio_volatility,
    rebalance_portfolio,
)


def test_portfolio_return_variance_and_volatility():
    expected_returns = np.array([0.08, 0.04])
    covariance_matrix = np.array([[0.04, 0.01], [0.01, 0.0225]])
    weights = np.array([0.6, 0.4])

    expected_return = np.dot(weights, expected_returns)
    expected_variance = weights.T @ covariance_matrix @ weights

    assert portfolio_return(expected_returns, weights) == pytest.approx(expected_return)
    assert portfolio_variance(covariance_matrix, weights) == pytest.approx(
        expected_variance
    )
    assert portfolio_volatility(covariance_matrix, weights) == pytest.approx(
        np.sqrt(expected_variance)
    )


def test_portfolio_sharpe_ratio():
    result = portfolio_sharpe_ratio(0.08, 0.16, risk_free_rate=0.02)

    assert result == pytest.approx(0.375)


def test_asset_covariance_and_correlation_matrices():
    returns = np.array(
        [
            [0.01, 0.02],
            [0.02, 0.01],
            [-0.01, -0.02],
            [0.03, 0.04],
        ]
    )

    covariance = asset_covariance_matrix(returns)
    correlation = asset_correlation_matrix(returns)

    np.testing.assert_allclose(covariance, np.cov(returns, rowvar=False, ddof=1))
    np.testing.assert_allclose(correlation, np.corrcoef(returns, rowvar=False))


def test_random_weights_are_reproducible_and_sum_to_one():
    first = generate_random_weights(3, n_portfolios=5, seed=42)
    second = generate_random_weights(3, n_portfolios=5, seed=42)

    np.testing.assert_allclose(first, second)
    np.testing.assert_allclose(first.sum(axis=1), np.ones(5))
    assert first.shape == (5, 3)


def test_generate_random_portfolios_returns_metric_arrays():
    expected_returns = np.array([0.08, 0.04, 0.06])
    covariance_matrix = np.diag([0.04, 0.01, 0.0225])

    portfolios = generate_random_portfolios(
        expected_returns,
        covariance_matrix,
        n_portfolios=10,
        risk_free_rate=0.01,
        seed=7,
    )

    assert portfolios["weights"].shape == (10, 3)
    assert portfolios["returns"].shape == (10,)
    assert portfolios["volatility"].shape == (10,)
    assert portfolios["sharpe_ratio"].shape == (10,)
    np.testing.assert_allclose(portfolios["weights"].sum(axis=1), np.ones(10))


def test_rebalance_portfolio_preserves_total_value():
    result = rebalance_portfolio([300.0, 700.0], [0.5, 0.5])

    np.testing.assert_allclose(result, [500.0, 500.0])


def test_plot_efficient_frontier_returns_axes():
    portfolios = {
        "returns": np.array([0.04, 0.05, 0.06]),
        "volatility": np.array([0.10, 0.12, 0.20]),
        "sharpe_ratio": np.array([0.30, 0.35, 0.25]),
    }

    ax = plot_efficient_frontier(portfolios, title="Frontier test")

    assert ax.get_title() == "Frontier test"
    assert ax.get_xlabel() == "Volatility"
    assert ax.get_ylabel() == "Expected return"
    plt.close(ax.figure)


def test_portfolio_functions_reject_invalid_inputs():
    with pytest.raises(ValueError, match="weights must sum to 1"):
        portfolio_return([0.1, 0.2], [0.2, 0.2])

    with pytest.raises(ValueError, match="weights must be greater than or equal to 0"):
        portfolio_return([0.1, 0.2], [1.1, -0.1])

    with pytest.raises(ValueError, match="covariance_matrix must be a square"):
        portfolio_variance([[0.1, 0.2]], [1.0])

    with pytest.raises(ValueError, match="volatility must be greater than 0"):
        portfolio_sharpe_ratio(0.1, 0.0)

    with pytest.raises(ValueError, match="returns must contain more observations"):
        asset_covariance_matrix([[0.01, 0.02], [0.02, 0.01]], ddof=2)

    with pytest.raises(ValueError, match="values must contain a positive total"):
        rebalance_portfolio([0.0, 0.0], [0.5, 0.5])
