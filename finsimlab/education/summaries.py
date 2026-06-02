"""Local summaries for simulation and financial calculation results."""

from __future__ import annotations

import numpy as np


def _as_finite_array(name: str, values) -> np.ndarray:
    result = np.asarray(values, dtype=float)
    if result.size == 0:
        raise ValueError(f"{name} must not be empty.")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values.")
    return result


def _format_percentile_key(percentile: float) -> str:
    percentage = percentile * 100
    if float(percentage).is_integer():
        return f"p{int(percentage):02d}"
    return f"p{percentage:g}".replace(".", "_")


def _require_percentiles(percentiles) -> tuple[float, ...]:
    result = tuple(float(value) for value in percentiles)
    if len(result) == 0:
        raise ValueError("percentiles must not be empty.")
    for value in result:
        if not np.isfinite(value):
            raise ValueError("percentiles must contain only finite values.")
        if value < 0 or value > 1:
            raise ValueError("percentiles must be between 0 and 1.")
    return result


def summarize_array(
    values,
    *,
    name: str = "values",
    percentiles=(0.05, 0.5, 0.95),
) -> dict[str, float | int]:
    """Summarize a numeric array with basic descriptive statistics."""
    array = _as_finite_array(name, values)
    percentile_values = _require_percentiles(percentiles)
    flat = array.ravel()

    summary: dict[str, float | int] = {
        "count": int(flat.size),
        "mean": float(np.mean(flat)),
        "std": float(np.std(flat, ddof=0)),
        "min": float(np.min(flat)),
        "max": float(np.max(flat)),
    }
    for percentile, value in zip(
        percentile_values,
        np.quantile(flat, percentile_values),
    ):
        summary[_format_percentile_key(percentile)] = float(value)
    return summary


def summarize_paths(paths, *, name: str = "paths") -> dict[str, float | int]:
    """Summarize simulated paths whose first axis is time."""
    values = _as_finite_array(name, paths)
    if values.ndim == 1:
        values = values.reshape(-1, 1)
    if values.ndim != 2:
        raise ValueError(f"{name} must be a 1D or 2D array.")
    if values.shape[0] < 2:
        raise ValueError(f"{name} must contain at least two time steps.")

    initial = values[0]
    if np.any(initial == 0):
        raise ValueError(f"{name} initial values must not be 0.")
    terminal = values[-1]
    total_returns = terminal / initial - 1.0

    return {
        "time_steps": int(values.shape[0]),
        "n_paths": int(values.shape[1]),
        "initial_mean": float(np.mean(initial)),
        "terminal_mean": float(np.mean(terminal)),
        "terminal_std": float(np.std(terminal, ddof=0)),
        "terminal_min": float(np.min(terminal)),
        "terminal_max": float(np.max(terminal)),
        "total_return_mean": float(np.mean(total_returns)),
        "total_return_p05": float(np.quantile(total_returns, 0.05)),
        "total_return_p50": float(np.quantile(total_returns, 0.50)),
        "total_return_p95": float(np.quantile(total_returns, 0.95)),
    }


def format_summary(summary: dict) -> str:
    """Format a summary dictionary as compact human-readable text."""
    if not isinstance(summary, dict):
        raise TypeError("summary must be a dictionary.")
    if not summary:
        raise ValueError("summary must not be empty.")

    lines = []
    for key, value in summary.items():
        if isinstance(value, float):
            lines.append(f"{key}: {value:.6g}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)
