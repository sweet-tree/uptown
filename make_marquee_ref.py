"""
One-time script: extract clean marquee reference from uptowns_card_ref.jpg.

Sends the card to Gemini Pro with an inpainting instruction:
keep the marquee sign exactly as-is, replace everything else with chroma green.

Run once:
  venv/bin/python make_marquee_ref.py
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
OUTPUT = Path("assets/marquee_ref_clean.png")

PROMPT = "Remove the sticker (players and stadium) from this image. Keep the marquee sign exactly as it is. Replace everything except the marquee with solid green #00FF00."


def main():
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    ref = PILImage.open(SOURCE)
    log.info(f"Source: {SOURCE} ({ref.size})")
    log.info("Running...")

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

    result.save(OUTPUT, format="PNG")
    log.info(f"Saved: {OUTPUT} ({result.width}x{result.height})")


if __name__ == "__main__":
    main()
