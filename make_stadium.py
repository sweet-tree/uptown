"""
Isolated Stadium Asset Generator.

Generates a single front-facing stadium illustration on chroma green background.
Output is a high-resolution isolated asset ready for Photoshop compositing.

Style reference: assets/uptowns_sticker_ref.jpg
Resolution:      4K at 4:3 (4800×3584)

Usage:
  venv/bin/python make_stadium.py --team KC
  venv/bin/python make_stadium.py --team DAL --model flash
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

from cards.sports_data import get_team
from cards.prompt_engine import build_stadium_prompt, load_style_ref
from compositor import extract_asset

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

MODELS = {
    "pro":   "gemini-3-pro-image-preview",
    "flash": "gemini-3.1-flash-image-preview",
}
ASPECT = "4:3"
SIZE   = {"pro": "4K", "flash": "2K"}   # Flash caps at 2K for this ratio


def main() -> None:
    parser = argparse.ArgumentParser(description="Isolated stadium asset generator")
    parser.add_argument("--team",  required=True, help="Team abbreviation (e.g. KC, DAL)")
    parser.add_argument("--model", default="flash", choices=["pro", "flash"])
    args = parser.parse_args()

    team   = get_team(args.team)
    ref    = load_style_ref()
    prompt = build_stadium_prompt(team)
    model  = MODELS[args.model]
    size   = SIZE[args.model]

    out_dir = Path("output/stadiums")
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = team.abbreviation.lower()

    log.info(f"Team    : {team.name}")
    log.info(f"Stadium : {team.stadium_name}")
    log.info(f"Model   : {model}  {ASPECT} {size}")
    log.info(f"Prompt  : {len(prompt)} chars")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    response = client.models.generate_content(
        model=model,
        contents=[prompt, ref],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=ASPECT, image_size=size),
        ),
    )

    raw_img = None
    for part in response.parts:
        if part.thought:
            continue
        if part.text:
            log.info(f"Model: {part.text[:200]}")
        elif part.inline_data is not None:
            raw_img = PILImage.open(io.BytesIO(part.inline_data.data))
            break

    if raw_img is None:
        raise RuntimeError("No image returned from API")

    # Raw — white background, lossless PNG
    raw_path = out_dir / f"{slug}_stadium_raw.png"
    raw_img.save(raw_path, format="PNG")
    log.info(f"Raw     : {raw_path}  ({raw_img.width}×{raw_img.height})")

    # Extracted — transparent PNG via BiRefNet neural background removal
    asset = extract_asset(raw_img, model_name="birefnet-general")
    asset_path = out_dir / f"{slug}_stadium.png"
    asset.save(asset_path, format="PNG")
    log.info(f"Asset   : {asset_path}")


if __name__ == "__main__":
    main()
