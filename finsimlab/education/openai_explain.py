"""Optional OpenAI-powered educational explanations."""

from __future__ import annotations

import os

from finsimlab.education.summaries import format_summary


def build_explanation_prompt(
    topic: str,
    summary: dict | None = None,
    language: str = "ja",
) -> str:
    """Build a prompt for an educational, non-advisory explanation."""
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string.")
    if not isinstance(language, str) or not language.strip():
        raise ValueError("language must be a non-empty string.")

    language_instruction = (
        "日本語で説明してください。"
        if language == "ja"
        else f"Use this language for the explanation: {language}."
    )
    lines = [
        "あなたは金融工学を初心者に教える教育用アシスタントです。",
        "投資助言、売買推奨、個別銘柄の推奨は行わないでください。",
        "数式や結果の意味を、学習目的に限定して簡潔に説明してください。",
        language_instruction,
        "",
        f"トピック: {topic.strip()}",
    ]
    if summary is not None:
        lines.extend(["", "計算結果の要約:", format_summary(summary)])
    return "\n".join(lines)


def _local_explanation(topic: str, summary: dict | None, language: str) -> str:
    if language == "ja":
        lines = [
            f"{topic} のローカル要約です。",
            "これは教育目的の説明であり、投資助言ではありません。",
        ]
        if summary is not None:
            lines.extend(["", format_summary(summary)])
        lines.append("")
        lines.append(
            "平均、ばらつき、分位点を見比べると、シミュレーション結果の"
            "中心的な水準と極端な結果の大きさを確認できます。"
        )
        return "\n".join(lines)

    lines = [
        f"Local explanation for {topic}.",
        "This is for education only and is not investment advice.",
    ]
    if summary is not None:
        lines.extend(["", format_summary(summary)])
    lines.append("")
    lines.append(
        "Compare the mean, dispersion, and percentiles to understand the "
        "central outcome and the size of more extreme simulated results."
    )
    return "\n".join(lines)


def _raise_missing_openai() -> None:
    raise RuntimeError(
        "OpenAI explanation requires the optional 'openai' package. "
        "Install it separately or call generate_explanation(..., fallback=True)."
    )


def _raise_missing_api_key() -> None:
    raise RuntimeError(
        "OpenAI explanation requires OPENAI_API_KEY to be set. "
        "Set the environment variable or call generate_explanation(..., fallback=True)."
    )


def generate_explanation(
    topic: str,
    summary: dict | None = None,
    model: str = "gpt-4.1-mini",
    language: str = "ja",
    client=None,
    fallback: bool = False,
) -> str:
    """Generate an educational explanation with optional OpenAI fallback.

    If ``fallback=True``, no network call is required and a local educational
    explanation is returned when a client is not explicitly supplied.
    """
    prompt = build_explanation_prompt(topic, summary, language)

    if client is None:
        if fallback:
            return _local_explanation(topic, summary, language)
        if not os.environ.get("OPENAI_API_KEY"):
            _raise_missing_api_key()
        try:
            from openai import OpenAI
        except ImportError:
            _raise_missing_openai()
        client = OpenAI()

    response = client.responses.create(model=model, input=prompt)
    try:
        return response.output_text
    except AttributeError as exc:
        raise RuntimeError("OpenAI response did not include output_text.") from exc
