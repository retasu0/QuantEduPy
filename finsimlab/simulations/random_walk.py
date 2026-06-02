"""Random walk simulation."""

from __future__ import annotations

import numpy as np

from finsimlab.simulations._utils import (
    make_rng,
    require_non_negative,
    require_positive,
    require_positive_int,
    require_real,
)


def simulate_random_walk(
    *,
    initial_value: float = 0.0,
    drift: float = 0.0,
    volatility: float = 1.0,
    steps: int = 252,
    n_paths: int = 1,
    dt: float = 1.0,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate arithmetic random walk paths.

    The process is:

        X[t+1] = X[t] + drift * dt + volatility * sqrt(dt) * Z

    where Z is a standard normal random variable. The returned array has shape
    ``(steps + 1, n_paths)`` and the first row is always ``initial_value``.
    """
    initial_value = require_real("initial_value", initial_value)
    drift = require_real("drift", drift)
    volatility = require_non_negative("volatility", volatility)
    steps = require_positive_int("steps", steps)
    n_paths = require_positive_int("n_paths", n_paths)
    dt = require_positive("dt", dt)

    rng = make_rng(seed)
    shocks = rng.normal(loc=0.0, scale=1.0, size=(steps, n_paths))
    increments = drift * dt + volatility * np.sqrt(dt) * shocks

    paths = np.empty((steps + 1, n_paths), dtype=float)
    paths[0] = initial_value
    paths[1:] = initial_value + np.cumsum(increments, axis=0)
    return paths

