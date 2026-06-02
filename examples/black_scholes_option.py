"""Small Black-Scholes and Monte Carlo option pricing example."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from finsimlab.options import (
    black_scholes_call,
    black_scholes_delta,
    black_scholes_put,
    monte_carlo_option_price,
)


def main() -> None:
    spot = 100
    strike = 100
    time_to_maturity = 1
    risk_free_rate = 0.05
    volatility = 0.2

    call = black_scholes_call(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    put = black_scholes_put(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
    )
    mc_call = monte_carlo_option_price(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type="call",
        n_paths=50_000,
        seed=42,
    )
    delta = black_scholes_delta(
        spot=spot,
        strike=strike,
        time_to_maturity=time_to_maturity,
        risk_free_rate=risk_free_rate,
        volatility=volatility,
        option_type="call",
    )

    print(f"Black-Scholes call: {call:.4f}")
    print(f"Black-Scholes put:  {put:.4f}")
    print(f"Monte Carlo call:   {mc_call:.4f}")
    print(f"Call delta:         {delta:.4f}")


if __name__ == "__main__":
    main()
