"""Plotting helpers for risk management examples."""

from __future__ import annotations

import numpy as np

from finsimlab.risk.returns import _as_finite_array
from finsimlab.risk.var import conditional_value_at_risk, value_at_risk


def plot_loss_distribution(
    losses,
    *,
    confidence_level: float = 0.95,
    bins: int = 40,
    title: str | None = None,
    ax=None,
):
    """Plot a loss distribution with VaR and CVaR markers."""
    import matplotlib.pyplot as plt

    values = _as_finite_array("losses", losses).ravel()
    if not isinstance(bins, int):
        raise TypeError("bins must be an integer.")
    if bins <= 0:
        raise ValueError("bins must be greater than 0.")

    var_value = value_at_risk(values, confidence_level=confidence_level)
    cvar_value = conditional_value_at_risk(values, confidence_level=confidence_level)

    if ax is None:
        _, ax = plt.subplots(figsize=(10, 5))

    ax.hist(values, bins=bins, alpha=0.75, edgecolor="white")
    ax.axvline(var_value, color="tab:red", linewidth=2.0, label="VaR")
    ax.axvline(cvar_value, color="black", linewidth=2.0, linestyle="--", label="CVaR")
    ax.set_title(title or "Loss distribution")
    ax.set_xlabel("Loss")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.25)
    ax.legend()
    return ax

