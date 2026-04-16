"""
Pass 3 (AI) — Gemini composite card generator.

Sends the sticker, marquee, and foil reference to Gemini and asks it to
compose the final collectible card. No PIL compositing — the model does
the layout.

Usage:
  venv/bin/python compose_ai.py \
    --sticker output/kc_mahomes_kelce_sticker.png \
    --marquee output/marquee_mahomes_kelce_sticker.png \
    --out output/kc_mahomes_kelce_final_ai.jpg
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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

MODEL  = "gemini-3.1-flash-image-preview"
FOIL   = Path("assets/foil_black.png")
REF_W  = 1264   # downscale inputs to 1K before sending — reduces payload


def build_compose_prompt() -> str:
    return """Task: composite three provided images into one landscape collectible card.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THE THREE IMAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Image 1 — BACKGROUND: black diamond foil texture. Tile it to fill the entire card.

Image 2 — STICKER: cartoon NFL players + stadium on a solid bright green background.
  The bright green is a chroma key — it is NOT part of the art. Remove it.
  What remains is the sticker: players, stadium, skyline, white die-cut border around the edge.

Image 3 — MARQUEE: a theatre sign (dark frame + amber bulbs + cream panel + player names) on a solid bright green background.
  The bright green is a chroma key — it is NOT part of the art. Remove it.
  What remains is the marquee sign with its white die-cut border.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXACT CARD LAYOUT — TOP TO BOTTOM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The card is divided into these vertical zones, from top to bottom:

  [ZONE A — top ~5% of card height]   Foil only. Empty margin above the marquee.
  [ZONE B — next ~25% of card height] MARQUEE sign centered here. Nothing else.
  [ZONE C — next ~5% of card height]  Foil only. Empty gap between marquee and sticker.
  [ZONE D — next ~55% of card height] STICKER illustration centered here. Nothing else.
  [ZONE E — bottom ~10% of card height] Foil only. Empty margin below the sticker.

The foil texture shows in ALL zones, but Zones A, C, and E are completely empty — no art.
The marquee (Zone B) and sticker (Zone D) are completely separate — they do not touch, overlap, or share any pixels.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Reproduce Image 2 and Image 3 art exactly — do not redraw, redesign, or change them
• Replace all bright green pixels in Image 2 and Image 3 with the foil texture from Image 1
• The marquee and sticker are always separated by a clear foil gap — never touching
• No additional text, graphics, or borders beyond what is in the three source images"""


def compose(sticker_path: str, marquee_path: str, out_path: str) -> None:
    def _resize(img: PILImage.Image) -> PILImage.Image:
        if img.width <= REF_W:
            return img
        ratio = REF_W / img.width
        return img.resize((REF_W, int(img.height * ratio)), PILImage.LANCZOS)

    foil    = _resize(PILImage.open(FOIL).convert("RGB"))
    sticker = _resize(PILImage.open(sticker_path).convert("RGB"))
    marquee = _resize(PILImage.open(marquee_path).convert("RGB"))

    log.info(f"Sticker : {sticker.width}×{sticker.height}")
    log.info(f"Marquee : {marquee.width}×{marquee.height}")
    log.info(f"Foil    : {foil.width}×{foil.height}")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = build_compose_prompt()

    log.info("Sending to Gemini for AI composite...")

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, foil, sticker, marquee],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="3:2", image_size="2K"
            ),
        ),
    )

    result = None
    for part in response.parts:
        if part.thought:
            continue
        if part.text:
            log.info(f"Model: {part.text[:200]}")
        elif part.inline_data is not None:
            result = PILImage.open(io.BytesIO(part.inline_data.data))
            break

    if result is None:
        raise RuntimeError("No image returned from API")

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.save(str(out), format="JPEG", quality=95)
    log.info(f"Saved : {out}  ({result.width}×{result.height})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pass 3 AI — Gemini composite")
    parser.add_argument("--sticker", required=True)
    parser.add_argument("--marquee", required=True)
    parser.add_argument("--out",     required=True)
    args = parser.parse_args()
    compose(args.sticker, args.marquee, args.out)


if __name__ == "__main__":
    main()
