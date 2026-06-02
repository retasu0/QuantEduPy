"""Run a geometric Brownian motion simulation and plot the result."""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import finsimlab as fsl


def main(*, show: bool = True) -> None:
    paths = fsl.simulate_gbm(
        s0=100,
        mu=0.05,
        sigma=0.2,
        years=1,
        steps=252,
        n_paths=100,
        seed=42,
    )

    fsl.plot_paths(paths, title="GBM stock price simulation")
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
