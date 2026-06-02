"""Helpers for visualizing simulated paths."""

from __future__ import annotations

import numpy as np


def plot_paths(
    paths,
    *,
    title: str | None = None,
    xlabel: str = "Step",
    ylabel: str = "Value",
    max_paths: int = 50,
    show_mean: bool = True,
    ax=None,
):
    """Plot simulated paths and optionally their cross-sectional mean.

    Parameters
    ----------
    paths:
        Array-like object with shape ``(steps + 1, n_paths)``.
    max_paths:
        Maximum number of individual paths to draw. Large simulations remain
        readable by plotting only the first ``max_paths`` paths.
    show_mean:
        Whether to overlay the average value across all paths at each step.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the plot.
    """
    import matplotlib.pyplot as plt

    values = np.asarray(paths, dtype=float)
    if values.ndim == 1:
        values = values.reshape(-1, 1)
    if values.ndim != 2:
        raise ValueError("paths must be a 1D or 2D array.")
    if values.shape[0] < 2:
        raise ValueError("paths must contain at least two time steps.")

    if max_paths <= 0:
        raise ValueError("max_paths must be greater than 0.")

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    count = min(max_paths, values.shape[1])
    x = np.arange(values.shape[0])
    ax.plot(x, values[:, :count], alpha=0.35, linewidth=1.0)

    if show_mean and values.shape[1] > 1:
        ax.plot(x, values.mean(axis=1), color="black", linewidth=2.0, label="Mean")
        ax.legend()

    ax.set_title(title or "Simulated paths")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25)
    return ax

