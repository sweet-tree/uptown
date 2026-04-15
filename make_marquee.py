"""
Pass 2 — Marquee sign generator.

Takes assets/marquee_uptowns.png (blank sign) and generates a filled version
with the correct player names on chroma green background.

Usage:
  venv/bin/python make_marquee.py --p1 "Maxx Crosby" --p2 "Ashton Jeanty"
  venv/bin/python make_marquee.py --p1 "Maxx Crosby" --p2 "Ashton Jeanty" --model flash
"""

import argparse
import io
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image as PILImage

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)-8s  %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

MODELS = {
    "pro": "gemini-3-pro-image-preview",
}

# real card — model copies the exact marquee style
MARQUEE_REF = Path("assets/uptowns_card_ref.jpg")


def build_marquee_prompt(p1: str, p2: str) -> str:
    return f"""═══════════════════════════════════════════════════════════
TASK: Reproduce the marquee sign from this card with new player names.
═══════════════════════════════════════════════════════════

You are given a sports card image. It contains a theatre marquee sign in the upper center.

Reproduce ONLY that marquee sign — same shape, same gold frame, same bulbs, same cream panel, same style — with these new names:

  TOP LINE:    "{p1.upper()}"
  CENTER LINE: "UPTOWNS"
  BOTTOM LINE: "{p2.upper()}"

Match the typography exactly as it appears in the reference:
- Same font style, same relative sizes, same letter-spacing, same dark brown color
- UPTOWNS is the largest line, wide letter-spacing
- Player names are slightly smaller, condensed bold

The sign has a thin white die-cut border tracing its outer silhouette.

BACKGROUND: Pure chroma green (#00FF00). Sign centered on chroma green. No glow, no shadow, no players, no stadium — just the sign on green.

═══════════════════════════════════════════════════════════
REMINDER: Copy the marquee sign from the reference. Change only the text. Chroma green background.
Text: "{p1.upper()}" / "UPTOWNS" / "{p2.upper()}"
═══════════════════════════════════════════════════════════"""


def run(p1: str, p2: str, model_key: str = "pro") -> PILImage.Image:
    model = MODELS[model_key]
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    ref = PILImage.open(MARQUEE_REF)
    prompt = build_marquee_prompt(p1, p2)

    log.info(f"Model   : {model}")
    log.info(f"Names   : {p1.upper()} / UPTOWNS / {p2.upper()}")

    response = client.models.generate_content(
        model=model,
        contents=[prompt, ref],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    result = None
    for part in response.parts:
        if part.thought:
            continue
        if part.text:
            log.info(f"Model: {part.text[:120]}")
        elif part.inline_data is not None:
            result = PILImage.open(io.BytesIO(part.inline_data.data))
            break

    if result is None:
        raise RuntimeError("No image returned")

    return result


def main():
    parser = argparse.ArgumentParser(description="Marquee sign generator")
    parser.add_argument("--p1", default="Maxx Crosby")
    parser.add_argument("--p2", default="Ashton Jeanty")
    parser.add_argument("--model", default="pro", choices=["pro"])
    args = parser.parse_args()

    p1_slug = args.p1.split()[-1].lower()
    p2_slug = args.p2.split()[-1].lower()

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    img = run(args.p1, args.p2, args.model)

    # Raw — chroma green
    raw_path = out_dir / f"marquee_{p1_slug}_{p2_slug}_raw.png"
    img.save(raw_path, format="PNG")
    log.info(f"Raw     : {raw_path} ({img.width}x{img.height})")

    # Sticker — chroma keyed, transparent
    from compositor import extract_sticker
    sticker = extract_sticker(img)
    sticker_path = out_dir / f"marquee_{p1_slug}_{p2_slug}_sticker.png"
    sticker.save(sticker_path, format="PNG")
    log.info(f"Sticker : {sticker_path}")


if __name__ == "__main__":
    main()
