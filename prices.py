"""Gemini API list prices, in US dollars per million tokens.

Prices are a snapshot of Google's published Gemini API prices.
Checked: 20 September 2026.

Source:
https://ai.google.dev/gemini-api/docs/pricing
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


PRICE_SOURCE = "https://ai.google.dev/gemini-api/docs/pricing"
PRICE_CHECKED = "2026-09-20"


@dataclass(frozen=True)
class Model:
    """One Gemini model's list price."""

    model_id: str
    input_per_mtok: float
    output_per_mtok: float


MODELS: Dict[str, Model] = {
    "gemini-3.5-flash": Model(
        "gemini-3.5-flash",
        1.50,
        9.00,
    ),
    "gemini-3.6-flash": Model(
        "gemini-3.6-flash",
        0.75,
        3.75,
    ),
    "gemini-3.7-flash": Model(
        "gemini-3.7-flash",
        0.75,
        3.75,
    ),
    "gemini-3.8-flash": Model(
        "gemini-3.8-flash",
        0.75,
        3.75,
    ),
}


DEFAULT_MODEL = "gemini-3.6-flash"


def cost_usd(
    model_key: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    """Return the list-price cost of one request in US dollars."""

    model = MODELS[model_key]

    return (
        input_tokens * model.input_per_mtok
        + output_tokens * model.output_per_mtok
    ) / 1_000_000