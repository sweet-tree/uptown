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
    return f"""The provided image IS the marquee sign. Reproduce it exactly — then change only the text.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT TO COPY — IDENTICAL, NO CHANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Frame shape — the exact ornate silhouette with decorative curved cutouts on all sides
• Frame color — deep dark brown / mahogany, same shading and depth
• Bulbs — single row of warm amber glowing bulbs running all the way around the inner frame edge, same size, same spacing, same warm glow
• Inner panel — off-white / cream color, same horizontal wood-slat lines across the panel
• Warm amber glow radiating outward from the bulbs onto the surrounding area
• Thin white die-cut border tracing the exact outer silhouette of the sign
• Overall proportions, padding, and scale of all elements

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT TO CHANGE — TEXT ONLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Replace the three text lines on the cream panel with:

  TOP LINE:    "{p1.upper()}"
  CENTER LINE: "UPTOWNS"
  BOTTOM LINE: "{p2.upper()}"

Match the typography from the reference exactly:
• "UPTOWNS" — same ultra-bold weight, same large size, same wide letter-spacing, same dark brown color
• Player name lines — same condensed bold weight, same smaller size, same dark brown color, same centered alignment
• Nothing else about the sign changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Background: pure chroma green (#00FF00) — every pixel outside the sign is exactly #00FF00
• Sign centered, filling most of the frame
• The complete sign must be fully visible — no part of the frame or bulbs is cut off at any edge
• Comfortable margin of green background visible on all four sides around the sign
• No players, no stadium, no card border — only the sign on green"""


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
            image_config=types.ImageConfig(
                aspect_ratio="4:3", image_size="2K"),
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
