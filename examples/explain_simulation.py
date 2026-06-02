"""Explain a simulated GBM result with local fallback or optional OpenAI."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from finsimlab.education import generate_explanation, summarize_paths
from finsimlab.simulations import simulate_gbm


def main(*, use_openai: bool = False) -> None:
    paths = simulate_gbm(
        s0=100,
        mu=0.05,
        sigma=0.2,
        years=1,
        steps=252,
        n_paths=1_000,
        seed=42,
    )
    summary = summarize_paths(paths)
    explanation = generate_explanation(
        "幾何ブラウン運動による株価パスのシミュレーション",
        summary,
        fallback=not use_openai,
    )
    print(explanation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-openai",
        action="store_true",
        help="Call the OpenAI API instead of using the local fallback explanation.",
    )
    args = parser.parse_args()
    main(use_openai=args.use_openai)
