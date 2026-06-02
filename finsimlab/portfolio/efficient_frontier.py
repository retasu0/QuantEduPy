"""Visualization of random-portfolio efficient frontier approximations."""

from __future__ import annotations

import numpy as np


def _portfolio_array(portfolios: dict[str, np.ndarray], key: str) -> np.ndarray:
    if key not in portfolios:
        raise ValueError(f"portfolios must contain '{key}'.")
    values = np.asarray(portfolios[key], dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError(f"portfolios['{key}'] must be a non-empty 1D array.")
    if not np.all(np.isfinite(values)):
        raise ValueError(f"portfolios['{key}'] must contain only finite values.")
    return values


def plot_efficient_frontier(
    portfolios: dict[str, np.ndarray],
    *,
    title: str | None = None,
    ax=None,
):
    """Plot a random-portfolio approximation of the efficient frontier.

    This is an educational visualization, not an optimizer. It shows the cloud
    of randomly sampled long-only portfolios and highlights the sample with the
    highest Sharpe ratio.
    """
    import matplotlib.pyplot as plt

    returns = _portfolio_array(portfolios, "returns")
    volatility = _portfolio_array(portfolios, "volatility")
    sharpe_ratio = _portfolio_array(portfolios, "sharpe_ratio")
    if not (returns.shape == volatility.shape == sharpe_ratio.shape):
        raise ValueError("portfolio metric arrays must have the same shape.")

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    scatter = ax.scatter(
        volatility,
        returns,
        c=sharpe_ratio,
        cmap="viridis",
        s=18,
        alpha=0.75,
    )
    best_index = int(np.argmax(sharpe_ratio))
    ax.scatter(
        volatility[best_index],
        returns[best_index],
        marker="*",
        s=180,
        color="tab:red",
        edgecolor="black",
        linewidth=0.8,
        label="Highest sampled Sharpe",
    )
    ax.set_title(title or "Random portfolio frontier approximation")
    ax.set_xlabel("Volatility")
    ax.set_ylabel("Expected return")
    ax.grid(True, alpha=0.25)
    ax.legend()
    ax.figure.colorbar(scatter, ax=ax, label="Sharpe ratio")
    return ax
