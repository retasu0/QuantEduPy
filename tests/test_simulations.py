import numpy as np
import pytest

import finsimlab as fsl


def test_random_walk_shape_and_initial_value():
    paths = fsl.simulate_random_walk(
        initial_value=10,
        drift=0.1,
        volatility=0.2,
        steps=5,
        n_paths=3,
        seed=1,
    )

    assert paths.shape == (6, 3)
    np.testing.assert_allclose(paths[0], np.array([10.0, 10.0, 10.0]))


def test_random_walk_is_reproducible_with_seed():
    first = fsl.simulate_random_walk(steps=5, n_paths=2, seed=123)
    second = fsl.simulate_random_walk(steps=5, n_paths=2, seed=123)

    np.testing.assert_allclose(first, second)


def test_gbm_shape_initial_value_and_positivity():
    paths = fsl.simulate_gbm(
        s0=100,
        mu=0.05,
        sigma=0.2,
        years=1,
        steps=10,
        n_paths=4,
        seed=2,
    )

    assert paths.shape == (11, 4)
    np.testing.assert_allclose(paths[0], np.array([100.0] * 4))
    assert np.all(paths > 0)


def test_gbm_zero_volatility_matches_deterministic_growth():
    paths = fsl.simulate_gbm(
        s0=100,
        mu=0.05,
        sigma=0.0,
        years=1,
        steps=4,
        n_paths=1,
        seed=2,
    )

    expected = 100 * np.exp(0.05 * np.linspace(0, 1, 5))
    np.testing.assert_allclose(paths[:, 0], expected)


def test_mean_reversion_shape_and_reproducibility():
    first = fsl.simulate_mean_reversion(
        initial_value=3,
        long_term_mean=1,
        speed=0.5,
        volatility=0.1,
        years=1,
        steps=8,
        n_paths=2,
        seed=3,
    )
    second = fsl.simulate_mean_reversion(
        initial_value=3,
        long_term_mean=1,
        speed=0.5,
        volatility=0.1,
        years=1,
        steps=8,
        n_paths=2,
        seed=3,
    )

    assert first.shape == (9, 2)
    np.testing.assert_allclose(first, second)


def test_invalid_inputs_raise_clear_errors():
    with pytest.raises(ValueError, match="s0 must be greater than 0"):
        fsl.simulate_gbm(s0=0, mu=0.0, sigma=0.2)

    with pytest.raises(ValueError, match="steps must be greater than 0"):
        fsl.simulate_random_walk(steps=0)

