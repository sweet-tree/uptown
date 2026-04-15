"""
One-time script: generate a clean sticker reference from the existing card ref.

Takes assets/uptowns_card_ref.jpg (Raiders card with marquee) and asks
Gemini Pro to remove the marquee sign entirely, keeping the sticker,
players, and composition identical. Output on chroma green background.

Run once:
  venv/bin/python make_sticker_ref.py
"""

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

MODEL = "gemini-3-pro-image-preview"
SOURCE = Path("assets/uptowns_card_ref.jpg")
OUTPUT = Path("assets/uptowns_sticker_ref.jpg")

PROMPT = """Using the provided image, change only the following:

1. Remove the theatre marquee sign completely — the sign in the upper-center area of the card. Replace that area with pure chroma green (#00FF00).

2. Change the entire background from black to pure chroma green (#00FF00).

Keep everything else EXACTLY as it is:
- The stadium sticker with its oval platform base — unchanged
- Both players, their positions, poses, jerseys, numbers — unchanged  
- The skyline behind the stadium — unchanged
- The white die-cut borders on the sticker and players — unchanged
- All proportions, sizes, and positions — unchanged

Output: the same card composition with no marquee sign, on a pure chroma green (#00FF00) background."""


def main():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    ref = PILImage.open(SOURCE)

    log.info(f"Source: {SOURCE} ({ref.size})")
    log.info("Generating sticker reference (no marquee, chroma green bg)...")

    response = client.models.generate_content(
        model=MODEL,
        contents=[PROMPT, ref],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="3:2", image_size="2K"),
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

    result.save(OUTPUT, format="JPEG", quality=95)
    log.info(f"Saved: {OUTPUT} ({result.width}x{result.height})")


if __name__ == "__main__":
    main()
