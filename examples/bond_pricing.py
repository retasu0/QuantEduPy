"""Price a fixed-coupon bond and plot price sensitivity to yield."""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from finsimlab.bonds import (
    bond_convexity,
    fixed_coupon_bond_price,
    macaulay_duration,
    modified_duration,
    plot_bond_price_vs_yield,
)


def main(*, show: bool = True) -> None:
    params = {
        "face_value": 1000.0,
        "coupon_rate": 0.04,
        "yield_to_maturity": 0.05,
        "years_to_maturity": 5.0,
        "payments_per_year": 2,
    }

    price = fixed_coupon_bond_price(**params)
    macaulay = macaulay_duration(**params)
    modified = modified_duration(**params)
    convexity = bond_convexity(**params)

    print(f"Bond price:        {price:,.2f}")
    print(f"Macaulay duration: {macaulay:.3f} years")
    print(f"Modified duration: {modified:.3f}")
    print(f"Convexity:         {convexity:.3f}")

    yields = np.linspace(0.01, 0.09, 41)
    plot_bond_price_vs_yield(
        face_value=params["face_value"],
        coupon_rate=params["coupon_rate"],
        years_to_maturity=params["years_to_maturity"],
        payments_per_year=params["payments_per_year"],
        yields=yields,
    )
    plt.tight_layout()
    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-show", action="store_true", help="Do not open a plot window.")
    args = parser.parse_args()
    main(show=not args.no_show)
