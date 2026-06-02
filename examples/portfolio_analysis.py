"""Generate random portfolios and plot a frontier approximation."""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from finsimlab.portfolio import (
    generate_random_portfolios,
    plot_efficient_frontier,
    portfolio_return,
    portfolio_volatility,
)


def main(*, show: bool = True) -> None:
    expected_returns = np.array([0.04, 0.07, 0.10], dtype=float)
    covariance_matrix = np.array(
        [
            [0.0100, 0.0018, 0.0011],
            [0.0018, 0.0225, 0.0026],
            [0.0011, 0.0026, 0.0400],
        ],
        dtype=float,
    )
    weights = np.array([0.5, 0.3, 0.2])

    expected = portfolio_return(expected_returns, weights)
    risk = portfolio_volatility(covariance_matrix, weights)
    print(f"Sample portfolio expected return: {expected:.2%}")
    print(f"Sample portfolio volatility:      {risk:.2%}")

    portfolios = generate_random_portfolios(
        expected_returns,
        covariance_matrix,
        n_portfolios=3000,
        risk_free_rate=0.01,
        seed=42,
    )
    plot_efficient_frontier(
        portfolios,
        title="Random long-only portfolio frontier approximation",
    )
    plt.tight_layout()
    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open a plot window.",
    )
    args = parser.parse_args()
    main(show=not args.no_show)
