"""Part 2 -- Gemini measurement for Lab 01.

Counts Gemini tokens for the corpus and, optionally, makes one real
Gemini request per language.

Run:
    python part2_gemini.py
    python part2_gemini.py --call
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from texts import CORPUS, LANGUAGES


load_dotenv()

OUTPUT_PATH = Path(__file__).with_name("measurements_gemini.json")

MODEL = "gemini-3.6-flash"
MAX_OUTPUT_TOKENS = 2048


def count_tokens(client: genai.Client, text: str) -> int:
    """Count Gemini tokens for one piece of text."""
    result = client.models.count_tokens(
        model=MODEL,
        contents=text,
    )
    return result.total_tokens


def count_request_tokens(
    client: genai.Client,
    lang: str,
) -> int:
    """Count tokens for the actual system-prompt + complaint request."""

    prompt = (
        CORPUS["system_prompt"][lang]
        + "\n\n"
        + CORPUS["complaint"][lang]
    )

    return count_tokens(client, prompt)


def one_real_request(
    client: genai.Client,
    lang: str,
):
    """Send one real Gemini request and return token usage."""

    response = client.models.generate_content(
        model=MODEL,
        contents=(
            CORPUS["system_prompt"][lang]
            + "\n\n"
            + CORPUS["complaint"][lang]
        ),
        config={
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        },
    )

    print("  --- answer ---")
    print("  " + response.text.replace("\n", "\n  "))

    usage = response.usage_metadata

    input_tokens = usage.prompt_token_count
    output_tokens = usage.candidates_token_count

    print(
        f"  billed: {input_tokens} input, "
        f"{output_tokens} output"
    )

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--call",
        action="store_true",
        help="also generate an answer in each language (uses API quota)",
    )

    args = parser.parse_args()

    try:
        client = genai.Client()
    except Exception as exc:
        print(f"Could not create Gemini client: {exc}", file=sys.stderr)
        print(
            "Check that GEMINI_API_KEY is present in your .env file.",
            file=sys.stderr,
        )
        return 1

    print(f"counting tokens on {MODEL}")
    print("Token counting does not generate an answer.\n")

    counts = {}

    try:
        for item_id, versions in CORPUS.items():
            counts[item_id] = {
                lang: count_tokens(client, versions[lang])
                for lang in LANGUAGES
            }

            row = "  ".join(
                f"{lang}={counts[item_id][lang]}"
                for lang in LANGUAGES
            )

            print(f"  {item_id:<14} {row}")

        request_tokens = {
            lang: count_request_tokens(client, lang)
            for lang in LANGUAGES
        }

        row = "  ".join(
            f"{lang}={request_tokens[lang]}"
            for lang in LANGUAGES
        )

        print(
            f"  {'request':<14} {row} "
            "(system prompt + complaint)"
        )

    except Exception as exc:
        print(f"Gemini API error: {exc}", file=sys.stderr)
        return 1

    billed = {}

    if args.call:
        print(
            f"\nGenerating answers with {MODEL} "
            "in each language:"
        )

        for lang in LANGUAGES:
            print(f"\n[{lang}]")

            try:
                billed[lang] = one_real_request(client, lang)
            except Exception as exc:
                print(
                    f"Gemini API error for {lang}: {exc}",
                    file=sys.stderr,
                )
                return 1

    payload = {
        "provider": "google-gemini",
        "model": MODEL,
        "token_counts": counts,
        "request_tokens": request_tokens,
        "one_request_billed": billed or None,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print(f"\nwrote {OUTPUT_PATH.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())