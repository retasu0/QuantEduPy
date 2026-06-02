import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from finsimlab.risk import (
    calculate_returns,
    conditional_value_at_risk,
    losses_from_returns,
    plot_loss_distribution,
    value_at_risk,
    volatility,
)


def test_calculate_simple_returns_known_values():
    returns = calculate_returns([100.0, 110.0, 99.0])

    np.testing.assert_allclose(returns, np.array([0.10, -0.10]))


def test_calculate_log_returns_known_values():
    prices = np.array([100.0, 110.0, 99.0])
    returns = calculate_returns(prices, method="log")

    np.testing.assert_allclose(returns, np.log(prices[1:] / prices[:-1]))


def test_calculate_returns_preserves_path_shape():
    prices = np.array(
        [
            [100.0, 200.0],
            [110.0, 190.0],
            [121.0, 209.0],
        ]
    )

    returns = calculate_returns(prices)

    assert returns.shape == (2, 2)
    np.testing.assert_allclose(returns[:, 0], np.array([0.10, 0.10]))
    np.testing.assert_allclose(returns[:, 1], np.array([-0.05, 0.10]))


def test_losses_from_returns_uses_positive_losses():
    losses = losses_from_returns(np.array([0.10, -0.05]), portfolio_value=1000)

    np.testing.assert_allclose(losses, np.array([-100.0, 50.0]))


def test_volatility_and_annualized_volatility():
    returns = np.array([0.01, -0.02, 0.03, -0.04])

    daily = volatility(returns, annualize=False)
    annualized = volatility(returns, annualize=True, periods_per_year=252)

    assert daily == pytest.approx(np.std(returns, ddof=1))
    assert annualized == pytest.approx(daily * np.sqrt(252))


def test_volatility_along_time_axis_returns_per_path_values():
    returns = np.array(
        [
            [0.01, 0.02],
            [0.02, 0.00],
            [0.03, -0.02],
        ]
    )

    result = volatility(returns, axis=0)

    np.testing.assert_allclose(result, np.std(returns, axis=0, ddof=1))


def test_value_at_risk_matches_numpy_quantile():
    losses = np.array([-10.0, 0.0, 20.0, 40.0, 100.0])

    result = value_at_risk(losses, confidence_level=0.8)

    assert result == pytest.approx(np.quantile(losses, 0.8))


def test_conditional_value_at_risk_uses_losses_at_or_above_var():
    losses = np.array([0.0, 10.0, 20.0, 30.0, 40.0])

    result = conditional_value_at_risk(losses, confidence_level=0.6)

    var_value = np.quantile(losses, 0.6)
    expected = np.mean(losses[losses >= var_value])
    assert result == pytest.approx(expected)


def test_var_and_cvar_accept_axis():
    losses = np.array(
        [
            [0.0, 5.0],
            [10.0, 15.0],
            [20.0, 25.0],
            [30.0, 35.0],
        ]
    )

    var_result = value_at_risk(losses, confidence_level=0.75, axis=0)
    cvar_result = conditional_value_at_risk(losses, confidence_level=0.75, axis=0)

    np.testing.assert_allclose(var_result, np.quantile(losses, 0.75, axis=0))
    np.testing.assert_allclose(cvar_result, np.array([30.0, 35.0]))


def test_risk_functions_reject_invalid_inputs():
    with pytest.raises(ValueError, match="prices must be greater than 0"):
        calculate_returns([100.0, 0.0])

    with pytest.raises(ValueError, match="method must be 'simple' or 'log'"):
        calculate_returns([100.0, 101.0], method="unknown")

    with pytest.raises(ValueError, match="confidence_level must be between 0 and 1"):
        value_at_risk([1.0, 2.0], confidence_level=1.0)

    with pytest.raises(ValueError, match="losses must contain only finite values"):
        conditional_value_at_risk([1.0, np.nan])

    with pytest.raises(ValueError, match="portfolio_value must be greater than 0"):
        losses_from_returns([0.01], portfolio_value=0)

    with pytest.raises(ValueError, match="returns must contain more observations"):
        volatility([0.01], ddof=1)


def test_plot_loss_distribution_returns_axes():
    losses = np.array([-10.0, 0.0, 5.0, 20.0, 50.0])

    ax = plot_loss_distribution(losses, confidence_level=0.8, title="Risk test")

    assert ax.get_title() == "Risk test"
    assert ax.get_xlabel() == "Loss"
    assert ax.get_ylabel() == "Frequency"
    assert len(ax.lines) == 2
    plt.close(ax.figure)

