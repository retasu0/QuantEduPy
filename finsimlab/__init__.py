"""FinSimLab: educational financial engineering simulations.

The public API intentionally starts small. Functions exported here are the
ones beginners are expected to try first in examples and notebooks.
"""

from finsimlab.plotting import plot_paths
from finsimlab.options import (
    black_scholes_call,
    black_scholes_delta,
    black_scholes_gamma,
    black_scholes_put,
    black_scholes_rho,
    black_scholes_theta,
    black_scholes_vega,
    call_payoff,
    monte_carlo_option_price,
    put_payoff,
)
from finsimlab.bonds import (
    bond_convexity,
    discount_factor,
    duration_price_change_approximation,
    fixed_coupon_bond_cash_flows,
    fixed_coupon_bond_price,
    macaulay_duration,
    modified_duration,
    plot_bond_price_vs_yield,
    present_value,
)
from finsimlab.education import (
    build_explanation_prompt,
    format_summary,
    generate_explanation,
    summarize_array,
    summarize_paths,
)
from finsimlab.portfolio import (
    asset_correlation_matrix,
    asset_covariance_matrix,
    generate_random_portfolios,
    generate_random_weights,
    plot_efficient_frontier,
    portfolio_return,
    portfolio_sharpe_ratio,
    portfolio_variance,
    portfolio_volatility,
    rebalance_portfolio,
)
from finsimlab.risk import (
    calculate_returns,
    conditional_value_at_risk,
    losses_from_returns,
    plot_loss_distribution,
    value_at_risk,
    volatility,
)
from finsimlab.simulations import (
    simulate_gbm,
    simulate_mean_reversion,
    simulate_random_walk,
)

__all__ = [
    "asset_correlation_matrix",
    "asset_covariance_matrix",
    "black_scholes_call",
    "black_scholes_delta",
    "black_scholes_gamma",
    "black_scholes_put",
    "black_scholes_rho",
    "black_scholes_theta",
    "black_scholes_vega",
    "bond_convexity",
    "build_explanation_prompt",
    "calculate_returns",
    "call_payoff",
    "conditional_value_at_risk",
    "discount_factor",
    "duration_price_change_approximation",
    "fixed_coupon_bond_cash_flows",
    "fixed_coupon_bond_price",
    "format_summary",
    "generate_explanation",
    "generate_random_portfolios",
    "generate_random_weights",
    "losses_from_returns",
    "macaulay_duration",
    "modified_duration",
    "monte_carlo_option_price",
    "plot_bond_price_vs_yield",
    "plot_efficient_frontier",
    "plot_loss_distribution",
    "plot_paths",
    "portfolio_return",
    "portfolio_sharpe_ratio",
    "portfolio_variance",
    "portfolio_volatility",
    "present_value",
    "put_payoff",
    "rebalance_portfolio",
    "simulate_gbm",
    "simulate_mean_reversion",
    "simulate_random_walk",
    "summarize_array",
    "summarize_paths",
    "value_at_risk",
    "volatility",
]
