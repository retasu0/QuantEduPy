import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from finsimlab.bonds import (
    bond_convexity,
    discount_factor,
    duration_price_change_approximation,
    fixed_coupon_bond_cash_flows,
    fixed_coupon_bond_price,
    macaulay_duration,
    modified_duration,
    plot_bond_price_vs_yield,
    present_value,
)


def test_discount_factor_matches_known_values():
    assert discount_factor(0.05, 1.0) == pytest.approx(1 / 1.05)
    assert discount_factor(0.05, 1.0, compounding="continuous") == pytest.approx(
        np.exp(-0.05)
    )


def test_present_value_matches_manual_calculation():
    cash_flows = np.array([100.0, 110.0])
    times = np.array([1.0, 2.0])

    result = present_value(cash_flows, times, 0.05)
    expected = 100 / 1.05 + 110 / 1.05**2

    assert result == pytest.approx(expected)


def test_fixed_coupon_bond_cash_flows():
    cash_flows, times = fixed_coupon_bond_cash_flows(
        face_value=1000,
        coupon_rate=0.04,
        years_to_maturity=2,
        payments_per_year=2,
    )

    np.testing.assert_allclose(cash_flows, [20.0, 20.0, 20.0, 1020.0])
    np.testing.assert_allclose(times, [0.5, 1.0, 1.5, 2.0])


def test_zero_coupon_bond_price_matches_discounted_face_value():
    price = fixed_coupon_bond_price(
        face_value=1000,
        coupon_rate=0.0,
        yield_to_maturity=0.05,
        years_to_maturity=3,
    )

    assert price == pytest.approx(1000 / 1.05**3)


def test_coupon_bond_price_matches_manual_cash_flow_pv():
    price = fixed_coupon_bond_price(
        face_value=1000,
        coupon_rate=0.04,
        yield_to_maturity=0.05,
        years_to_maturity=2,
        payments_per_year=2,
    )
    expected = sum(20 / 1.025**period for period in range(1, 4))
    expected += 1020 / 1.025**4

    assert price == pytest.approx(expected)


def test_coupon_rate_equal_yield_prices_near_par():
    price = fixed_coupon_bond_price(
        face_value=1000,
        coupon_rate=0.05,
        yield_to_maturity=0.05,
        years_to_maturity=5,
        payments_per_year=2,
    )

    assert price == pytest.approx(1000)


def test_duration_and_convexity_relationships():
    params = {
        "face_value": 1000,
        "coupon_rate": 0.04,
        "yield_to_maturity": 0.05,
        "years_to_maturity": 5,
        "payments_per_year": 2,
    }

    macaulay = macaulay_duration(**params)
    modified = modified_duration(**params)
    convexity = bond_convexity(**params)

    assert modified == pytest.approx(macaulay / (1 + 0.05 / 2))
    assert 0 < macaulay < params["years_to_maturity"]
    assert convexity > 0


def test_bond_price_decreases_when_yield_increases():
    low_yield = fixed_coupon_bond_price(
        face_value=1000,
        coupon_rate=0.04,
        yield_to_maturity=0.03,
        years_to_maturity=5,
    )
    high_yield = fixed_coupon_bond_price(
        face_value=1000,
        coupon_rate=0.04,
        yield_to_maturity=0.06,
        years_to_maturity=5,
    )

    assert low_yield > high_yield


def test_duration_price_change_approximation_has_expected_direction():
    change = duration_price_change_approximation(
        face_value=1000,
        coupon_rate=0.04,
        yield_to_maturity=0.05,
        years_to_maturity=5,
        yield_change=0.01,
    )

    assert change < 0


def test_plot_bond_price_vs_yield_returns_axes():
    ax = plot_bond_price_vs_yield(
        face_value=1000,
        coupon_rate=0.04,
        years_to_maturity=5,
        yields=np.linspace(0.02, 0.08, 7),
    )

    assert ax.get_title() == "Bond price vs. yield"
    assert ax.get_xlabel() == "Yield to maturity"
    assert ax.get_ylabel() == "Bond price"
    plt.close(ax.figure)


def test_bond_functions_reject_invalid_inputs():
    with pytest.raises(ValueError, match="face_value must be greater than 0"):
        fixed_coupon_bond_price(
            face_value=0,
            coupon_rate=0.04,
            yield_to_maturity=0.05,
            years_to_maturity=5,
        )

    with pytest.raises(ValueError, match="coupon_rate must be greater than or equal"):
        fixed_coupon_bond_price(
            face_value=1000,
            coupon_rate=-0.01,
            yield_to_maturity=0.05,
            years_to_maturity=5,
        )

    with pytest.raises(ValueError, match="years_to_maturity must align"):
        fixed_coupon_bond_price(
            face_value=1000,
            coupon_rate=0.04,
            yield_to_maturity=0.05,
            years_to_maturity=1.25,
            payments_per_year=2,
        )

    with pytest.raises(ValueError, match="cash_flows and times must have the same"):
        present_value([100.0], [1.0, 2.0], 0.05)

    with pytest.raises(ValueError, match="compounding must be"):
        discount_factor(0.05, 1.0, compounding="monthly")
