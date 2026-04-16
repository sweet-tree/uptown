"""
Background Plate Generator — Stadium + City Skyline + Sky.

Generates one wide landscape image per team combining the stadium (centered,
dominant), the city skyline behind it, and the sky above. No players, no die-cut.
Chroma green (#00FF00) background — key out manually in Photoshop.

Style reference: assets/uptowns_sticker_ref.jpg
Resolution:      2K at 16:9 (2752×1548) — Flash (default, for iteration)
                 4K at 16:9 (5504×3096) — Pro

Usage:
  venv/bin/python make_background.py --team KC
  venv/bin/python make_background.py --team DAL --model pro
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
from cards.prompt_engine import build_background_prompt, load_style_ref

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
ASPECT = "16:9"
SIZE   = {"pro": "4K", "flash": "2K"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Background plate generator (stadium + skyline + sky)")
    parser.add_argument("--team",  required=True, help="Team abbreviation (e.g. KC, DAL)")
    parser.add_argument("--model", default="flash", choices=["pro", "flash"])
    args = parser.parse_args()

    team   = get_team(args.team)
    ref    = load_style_ref()
    prompt = build_background_prompt(team)
    model  = MODELS[args.model]
    size   = SIZE[args.model]

    out_dir = Path("output/backgrounds")
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

    # Raw chroma green — key out manually in Photoshop
    raw_path = out_dir / f"{slug}_background_raw.jpg"
    raw_img.save(raw_path, format="JPEG", quality=97)
    log.info(f"Saved   : {raw_path}  ({raw_img.width}×{raw_img.height})")


if __name__ == "__main__":
    main()
