from math import exp

import numpy as np
import pytest

from finsimlab.options import (
    black_scholes_call,
    black_scholes_delta,
    black_scholes_gamma,
    black_scholes_put,
    black_scholes_rho,
    black_scholes_theta,
    black_scholes_vega,
    call_payoff,
    monte_carlo_option_price,
    put_payoff,
)


def test_black_scholes_matches_known_values():
    params = {
        "spot": 100,
        "strike": 100,
        "time_to_maturity": 1,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
    }

    assert black_scholes_call(**params) == pytest.approx(10.4506, abs=1e-4)
    assert black_scholes_put(**params) == pytest.approx(5.5735, abs=1e-4)


def test_put_call_parity():
    params = {
        "spot": 100,
        "strike": 105,
        "time_to_maturity": 2,
        "risk_free_rate": 0.03,
        "volatility": 0.25,
    }

    call = black_scholes_call(**params)
    put = black_scholes_put(**params)
    parity_value = params["spot"] - params["strike"] * exp(
        -params["risk_free_rate"] * params["time_to_maturity"]
    )

    assert call - put == pytest.approx(parity_value)


def test_payoff_helpers_return_expected_arrays():
    prices = np.array([80, 100, 120], dtype=float)

    np.testing.assert_allclose(call_payoff(prices, strike=100), [0, 0, 20])
    np.testing.assert_allclose(put_payoff(prices, strike=100), [20, 0, 0])


def test_monte_carlo_option_price_is_reproducible_with_seed():
    params = {
        "spot": 100,
        "strike": 100,
        "time_to_maturity": 1,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
        "option_type": "call",
        "n_paths": 10_000,
        "seed": 123,
    }

    first = monte_carlo_option_price(**params)
    second = monte_carlo_option_price(**params)

    assert first == pytest.approx(second)


def test_monte_carlo_option_price_is_close_to_black_scholes():
    params = {
        "spot": 100,
        "strike": 100,
        "time_to_maturity": 1,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
    }

    mc_price = monte_carlo_option_price(
        **params,
        option_type="call",
        n_paths=150_000,
        seed=42,
    )
    bs_price = black_scholes_call(**params)

    assert mc_price == pytest.approx(bs_price, abs=0.15)


def test_zero_volatility_uses_deterministic_discounted_payoff():
    params = {
        "spot": 100,
        "strike": 95,
        "time_to_maturity": 1,
        "risk_free_rate": 0.05,
        "volatility": 0.0,
    }

    expected_call = max(
        params["spot"]
        - params["strike"] * exp(-params["risk_free_rate"] * params["time_to_maturity"]),
        0,
    )
    expected_put = max(
        params["strike"] * exp(-params["risk_free_rate"] * params["time_to_maturity"])
        - params["spot"],
        0,
    )

    assert black_scholes_call(**params) == pytest.approx(expected_call)
    assert black_scholes_put(**params) == pytest.approx(expected_put)
    assert monte_carlo_option_price(**params, option_type="call") == pytest.approx(
        expected_call
    )


def test_basic_greeks_match_reference_values():
    params = {
        "spot": 100,
        "strike": 100,
        "time_to_maturity": 1,
        "risk_free_rate": 0.05,
        "volatility": 0.2,
    }

    assert black_scholes_delta(**params, option_type="call") == pytest.approx(
        0.6368, abs=1e-4
    )
    assert black_scholes_delta(**params, option_type="put") == pytest.approx(
        -0.3632, abs=1e-4
    )
    assert black_scholes_gamma(**params) == pytest.approx(0.0188, abs=1e-4)
    assert black_scholes_vega(**params) == pytest.approx(37.5240, abs=1e-4)
    assert black_scholes_theta(**params, option_type="call") == pytest.approx(
        -6.4140, abs=1e-4
    )
    assert black_scholes_rho(**params, option_type="call") == pytest.approx(
        53.2325, abs=1e-4
    )


def test_invalid_inputs_raise_clear_errors():
    with pytest.raises(ValueError, match="spot must be greater than 0"):
        black_scholes_call(
            spot=0,
            strike=100,
            time_to_maturity=1,
            risk_free_rate=0.05,
            volatility=0.2,
        )

    with pytest.raises(ValueError, match="strike must be greater than 0"):
        call_payoff([100], strike=0)

    with pytest.raises(ValueError, match='option_type must be "call" or "put"'):
        monte_carlo_option_price(
            spot=100,
            strike=100,
            time_to_maturity=1,
            risk_free_rate=0.05,
            volatility=0.2,
            option_type="straddle",
        )

    with pytest.raises(ValueError, match="volatility must be greater than 0"):
        black_scholes_delta(
            spot=100,
            strike=100,
            time_to_maturity=1,
            risk_free_rate=0.05,
            volatility=0,
        )
