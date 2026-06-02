"""Estimate simple portfolio VaR and CVaR from simulated price paths."""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from finsimlab.risk import (
    conditional_value_at_risk,
    losses_from_returns,
    plot_loss_distribution,
    value_at_risk,
)
from finsimlab.simulations import simulate_gbm


def main(*, show: bool = True) -> None:
    initial_price = 100.0
    portfolio_value = 10_000.0

    paths = simulate_gbm(
        s0=initial_price,
        mu=0.05,
        sigma=0.2,
        years=1,
        steps=252,
        n_paths=5_000,
        seed=42,
    )

    terminal_returns = paths[-1] / paths[0] - 1.0
    losses = losses_from_returns(terminal_returns, portfolio_value=portfolio_value)

    var_95 = value_at_risk(losses, confidence_level=0.95)
    cvar_95 = conditional_value_at_risk(losses, confidence_level=0.95)

    print(f"95% VaR:  {var_95:,.2f}")
    print(f"95% CVaR: {cvar_95:,.2f}")

    plot_loss_distribution(
        losses,
        confidence_level=0.95,
        title="Simulated one-year portfolio loss distribution",
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
