"""Plotting helpers for bond pricing examples."""

from __future__ import annotations

import numpy as np

from finsimlab.bonds.pricing import _as_finite_array, fixed_coupon_bond_price


def plot_bond_price_vs_yield(
    *,
    face_value: float,
    coupon_rate: float,
    years_to_maturity: float,
    yields,
    payments_per_year: int = 1,
    ax=None,
):
    """Plot fixed-coupon bond price against yield to maturity."""
    import matplotlib.pyplot as plt

    yield_values = _as_finite_array("yields", yields).ravel()
    prices = np.array(
        [
            fixed_coupon_bond_price(
                face_value=face_value,
                coupon_rate=coupon_rate,
                yield_to_maturity=yield_value,
                years_to_maturity=years_to_maturity,
                payments_per_year=payments_per_year,
            )
            for yield_value in yield_values
        ],
        dtype=float,
    )

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    ax.plot(yield_values, prices, linewidth=2.0)
    ax.set_title("Bond price vs. yield")
    ax.set_xlabel("Yield to maturity")
    ax.set_ylabel("Bond price")
    ax.grid(True, alpha=0.25)
    return ax
