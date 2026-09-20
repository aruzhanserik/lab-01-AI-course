"""Part 3 -- turn the measured Gemini token counts into money.

Reads ``measurements_gemini.json`` from Part 2 and answers:

* what one support request costs in each language;
* what a year of them costs at a chosen volume;
* how the input-token ratio differs from the total-bill ratio;
* how the same measured workload compares across Gemini models.

The token counts were actually measured on Gemini 3.6 Flash.
The other model rows apply their list prices to the same measured
workload, so they are price comparisons, not separate model runs.

Run:
    python part3_cost_gemini.py
    python part3_cost_gemini.py --requests-per-day 5000
    python part3_cost_gemini.py --output-tokens 300
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

from prices import MODELS, PRICE_CHECKED, PRICE_SOURCE, cost_usd
from texts import LANGUAGES


DEFAULT_MEASUREMENTS = Path(__file__).with_name(
    "measurements_gemini.json"
)

FALLBACK_OUTPUT_TOKENS = 300

MODEL_ORDER = (
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.8-flash",
)


def load_measurements(path: Path) -> Dict[str, object]:
    """Read the JSON written by the Gemini measurement script."""

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(
            f"{path.name} not found. Run part2_gemini.py first."
        )
    except json.JSONDecodeError as exc:
        sys.exit(
            f"{path.name} is not valid JSON: {exc}"
        )


def request_input_tokens(
    data: Dict[str, object],
    lang: str,
) -> int:
    """Return measured input tokens for one language."""

    request_tokens = data.get("request_tokens")

    if not request_tokens or lang not in request_tokens:
        sys.exit(
            f"{data.get('model', 'Gemini')} measurements have no "
            f"request_tokens for {lang!r}."
        )

    return int(request_tokens[lang])


def resolve_output_tokens(
    billed: Optional[Dict[str, Dict[str, int]]],
    override: Optional[int],
) -> Tuple[Dict[str, int], str]:
    """Choose measured or explicitly supplied output-token counts."""

    if override is not None:
        return (
            {lang: override for lang in LANGUAGES},
            "fixed by --output-tokens",
        )

    if billed and all(lang in billed for lang in LANGUAGES):
        return (
            {
                lang: int(billed[lang]["output_tokens"])
                for lang in LANGUAGES
            },
            "measured in Part 2, per language",
        )

    return (
        {
            lang: FALLBACK_OUTPUT_TOKENS
            for lang in LANGUAGES
        },
        "ASSUMED -- Part 2 ran without --call",
    )


def _header() -> str:
    """Column header shared by the tables."""

    return (
        f"{'':<22}"
        + "".join(
            f"{lang.upper():>14}"
            for lang in LANGUAGES
        )
    )


def main() -> int:
    """Print Gemini cost tables."""

    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        "--measurements",
        type=Path,
        default=DEFAULT_MEASUREMENTS,
        help="Gemini measurements JSON",
    )

    parser.add_argument(
        "--requests-per-day",
        type=int,
        default=2000,
        help="support volume per day (default: 2000)",
    )

    parser.add_argument(
        "--output-tokens",
        type=int,
        default=None,
        help="override measured output tokens",
    )

    parser.add_argument(
        "--model",
        default="gemini-3.6-flash",
        choices=sorted(MODELS),
        help="model used for the ratio summary",
    )

    args = parser.parse_args()

    data = load_measurements(args.measurements)

    billed = data.get("one_request_billed")

    outputs, provenance = resolve_output_tokens(
        billed,
        args.output_tokens,
    )

    measured_model = data.get(
        "model",
        "unknown",
    )

    print(
        f"prices from {PRICE_SOURCE}"
    )
    print(
        f"checked {PRICE_CHECKED}; "
        f"tokens measured on {measured_model}"
    )
    print(
        f"answer length: {provenance}\n"
    )

    inputs = {
        lang: request_input_tokens(data, lang)
        for lang in LANGUAGES
    }

    print(
        "ONE SUPPORT REQUEST -- tokens, "
        "and cost in US cents"
    )
    print("-" * 78)
    print(_header())

    print(
        f"{'input tokens':<22}"
        + "".join(
            f"{inputs[lang]:>14}"
            for lang in LANGUAGES
        )
    )

    print(
        f"{'output tokens':<22}"
        + "".join(
            f"{outputs[lang]:>14}"
            for lang in LANGUAGES
        )
    )

    for model_key in MODEL_ORDER:
        cents = [
            cost_usd(
                model_key,
                inputs[lang],
                outputs[lang],
            )
            * 100
            for lang in LANGUAGES
        ]

        print(
            f"{model_key:<22}"
            + "".join(
                f"{value:>14.4f}"
                for value in cents
            )
        )

    per_year = args.requests_per_day * 365

    print(
        f"\nAT {args.requests_per_day:,} REQUESTS/DAY "
        "-- US dollars per year"
    )
    print("-" * 78)
    print(_header())

    for model_key in MODEL_ORDER:
        yearly = [
            cost_usd(
                model_key,
                inputs[lang],
                outputs[lang],
            )
            * per_year
            for lang in LANGUAGES
        ]

        print(
            f"{model_key:<22}"
            + "".join(
                f"{value:>14,.0f}"
                for value in yearly
            )
        )

    print(
        "\nTWO RATIOS THAT ARE NOT THE SAME NUMBER"
    )
    print("-" * 78)
    print(_header())

    print(
        f"{'input only':<22}"
        + "".join(
            f"{inputs[lang] / inputs['en']:>13.2f}x"
            for lang in LANGUAGES
        )
    )

    base_bill = cost_usd(
        args.model,
        inputs["en"],
        outputs["en"],
    )

    print(
        f"{'total bill':<22}"
        + "".join(
            f"{cost_usd(args.model, inputs[lang], outputs[lang]) / base_bill:>13.2f}x"
            for lang in LANGUAGES
        )
    )

    print(
        "\nThe input row reflects tokenization. "
        "The total-bill row also includes output length."
    )

    print(
        f"\nTHE NUMBER TO REMEMBER "
        f"-- {args.model}"
    )
    print("-" * 78)

    en_year = (
        cost_usd(
            args.model,
            inputs["en"],
            outputs["en"],
        )
        * per_year
    )

    for lang in ("ru", "kk"):
        lang_year = (
            cost_usd(
                args.model,
                inputs[lang],
                outputs[lang],
            )
            * per_year
        )

        print(
            f"{lang.upper()} instead of EN, "
            f"same workload and volume: "
            f"${lang_year - en_year:,.2f}/year more "
            f"({lang_year / en_year:.2f}x)."
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())