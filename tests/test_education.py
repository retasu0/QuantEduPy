import sys

import numpy as np
import pytest

from finsimlab.education import (
    build_explanation_prompt,
    format_summary,
    generate_explanation,
    summarize_array,
    summarize_paths,
)


def test_summarize_array_returns_known_values():
    summary = summarize_array([1, 2, 3, 4], percentiles=(0.25, 0.5, 0.75))

    assert summary["count"] == 4
    assert summary["mean"] == pytest.approx(2.5)
    assert summary["std"] == pytest.approx(np.std([1, 2, 3, 4], ddof=0))
    assert summary["min"] == 1.0
    assert summary["max"] == 4.0
    assert summary["p25"] == pytest.approx(1.75)
    assert summary["p50"] == pytest.approx(2.5)
    assert summary["p75"] == pytest.approx(3.25)


def test_summarize_paths_returns_path_level_statistics():
    paths = np.array(
        [
            [100.0, 100.0],
            [110.0, 90.0],
            [121.0, 81.0],
        ]
    )

    summary = summarize_paths(paths)

    assert summary["time_steps"] == 3
    assert summary["n_paths"] == 2
    assert summary["initial_mean"] == 100.0
    assert summary["terminal_mean"] == 101.0
    assert summary["terminal_min"] == 81.0
    assert summary["terminal_max"] == 121.0
    assert summary["total_return_mean"] == pytest.approx(0.01)
    assert summary["total_return_p50"] == pytest.approx(0.01)


def test_summarize_paths_rejects_zero_initial_values():
    with pytest.raises(ValueError, match="initial values must not be 0"):
        summarize_paths([[0.0], [1.0]])


def test_format_summary_formats_numeric_values():
    text = format_summary({"count": 2, "mean": 1.23456789})

    assert "count: 2" in text
    assert "mean: 1.23457" in text


def test_build_explanation_prompt_contains_non_advisory_instruction():
    prompt = build_explanation_prompt("VaR", {"mean": 10.0})

    assert "VaR" in prompt
    assert "投資助言" in prompt
    assert "mean: 10" in prompt


def test_generate_explanation_fallback_without_openai():
    text = generate_explanation(
        "GBM",
        {"mean": 100.0, "p95": 130.0},
        fallback=True,
    )

    assert "GBM" in text
    assert "投資助言ではありません" in text
    assert "mean: 100" in text


def test_generate_explanation_requires_api_key_without_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        generate_explanation("GBM", fallback=False)


def test_generate_explanation_requires_openai_package_without_fallback(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setitem(sys.modules, "openai", None)

    with pytest.raises(RuntimeError, match="optional 'openai' package"):
        generate_explanation("GBM", fallback=False)


def test_generate_explanation_uses_responses_api_with_fake_client():
    class FakeResponse:
        output_text = "fake explanation"

    class FakeResponses:
        def __init__(self):
            self.calls = []

        def create(self, *, model, input):
            self.calls.append({"model": model, "input": input})
            return FakeResponse()

    class FakeClient:
        def __init__(self):
            self.responses = FakeResponses()

    client = FakeClient()

    text = generate_explanation(
        "オプション価格",
        {"mean": 10.0},
        model="test-model",
        client=client,
    )

    assert text == "fake explanation"
    assert client.responses.calls[0]["model"] == "test-model"
    assert "オプション価格" in client.responses.calls[0]["input"]
