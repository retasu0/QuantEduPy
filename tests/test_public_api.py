import finsimlab as fsl


def test_top_level_exports_include_phase_2_and_phase_3_helpers():
    assert fsl.black_scholes_call(
        spot=100,
        strike=100,
        time_to_maturity=1,
        risk_free_rate=0.05,
        volatility=0.2,
    ) > 0

    assert fsl.value_at_risk([0, 10, 20], confidence_level=0.5) == 10


def test_top_level_exports_include_phase_4_and_phase_5_helpers():
    assert fsl.portfolio_return([0.05, 0.10], [0.4, 0.6]) == 0.08

    price = fsl.fixed_coupon_bond_price(
        face_value=1000,
        coupon_rate=0.05,
        yield_to_maturity=0.05,
        years_to_maturity=3,
        payments_per_year=1,
    )
    assert round(price, 6) == 1000.0


def test_top_level_exports_include_phase_6_helpers():
    summary = fsl.summarize_array([1, 2, 3])

    assert summary["mean"] == 2.0
    assert "mean: 2" in fsl.format_summary(summary)
    assert "投資助言" in fsl.build_explanation_prompt("GBM", summary)
