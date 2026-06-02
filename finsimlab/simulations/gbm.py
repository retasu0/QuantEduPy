"""Geometric Brownian motion simulation."""

from __future__ import annotations

import numpy as np

from finsimlab.simulations._utils import (
    make_rng,
    require_non_negative,
    require_positive,
    require_positive_int,
    require_real,
)


def simulate_gbm(
    *,
    s0: float,
    mu: float,
    sigma: float,
    years: float = 1.0,
    steps: int = 252,
    n_paths: int = 1,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate geometric Brownian motion price paths.

    This is a common first model for stock prices:

        dS = mu * S * dt + sigma * S * dW

    The implementation uses the exact log-return discretization, so simulated
    prices stay positive when ``s0`` is positive. The returned array has shape
    ``(steps + 1, n_paths)`` and row 0 is ``s0``.
    """
    s0 = require_positive("s0", s0)
    mu = require_real("mu", mu)
    sigma = require_non_negative("sigma", sigma)
    years = require_positive("years", years)
    steps = require_positive_int("steps", steps)
    n_paths = require_positive_int("n_paths", n_paths)

    dt = years / steps
    rng = make_rng(seed)
    shocks = rng.normal(loc=0.0, scale=1.0, size=(steps, n_paths))
    log_increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * shocks

    paths = np.empty((steps + 1, n_paths), dtype=float)
    paths[0] = s0
    paths[1:] = s0 * np.exp(np.cumsum(log_increments, axis=0))
    return paths

