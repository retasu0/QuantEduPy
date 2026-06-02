"""Mean-reverting process simulation."""

from __future__ import annotations

import numpy as np

from finsimlab.simulations._utils import (
    make_rng,
    require_non_negative,
    require_positive,
    require_positive_int,
    require_real,
)


def simulate_mean_reversion(
    *,
    initial_value: float,
    long_term_mean: float,
    speed: float,
    volatility: float,
    years: float = 1.0,
    steps: int = 252,
    n_paths: int = 1,
    seed: int | None = None,
) -> np.ndarray:
    """Simulate an Ornstein-Uhlenbeck style mean-reverting process.

    The process moves back toward ``long_term_mean`` at the rate ``speed``:

        X[t+1] = X[t] + speed * (mean - X[t]) * dt
                 + volatility * sqrt(dt) * Z

    The returned array has shape ``(steps + 1, n_paths)``.
    """
    initial_value = require_real("initial_value", initial_value)
    long_term_mean = require_real("long_term_mean", long_term_mean)
    speed = require_non_negative("speed", speed)
    volatility = require_non_negative("volatility", volatility)
    years = require_positive("years", years)
    steps = require_positive_int("steps", steps)
    n_paths = require_positive_int("n_paths", n_paths)

    dt = years / steps
    rng = make_rng(seed)
    shocks = rng.normal(loc=0.0, scale=1.0, size=(steps, n_paths))

    paths = np.empty((steps + 1, n_paths), dtype=float)
    paths[0] = initial_value
    for index in range(steps):
        previous = paths[index]
        pull = speed * (long_term_mean - previous) * dt
        noise = volatility * np.sqrt(dt) * shocks[index]
        paths[index + 1] = previous + pull + noise

    return paths

