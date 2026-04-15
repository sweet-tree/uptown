"""
Uptowns — single card runner.

Usage:
  python run.py
  python run.py --team LV --p1 "Maxx Crosby" --n1 98 --p2 "Ashton Jeanty" --n2 2
  python run.py --team BAL --p1 "Lamar Jackson" --n1 8 --p2 "Derrick Henry" --n2 22
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

from cards.sports_data import get_team, PlayerSpec, CardSpec
from cards.prompt_engine import build_sticker_prompt, load_sticker_ref
from compositor import extract_sticker

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

MODEL = "gemini-3-pro-image-preview"
SIZE = "2K"


def main():
    parser = argparse.ArgumentParser(
        description="Uptowns single card generator")
    parser.add_argument("--team",  default="LV")
    parser.add_argument("--p1",    default="Maxx Crosby")
    parser.add_argument("--n1",    default="98")
    parser.add_argument("--pos1",  default="default")
    parser.add_argument("--p2",    default="Ashton Jeanty")
    parser.add_argument("--n2",    default="2")
    parser.add_argument("--pos2",  default="rb")
    args = parser.parse_args()

    spec = CardSpec(
        team=get_team(args.team),
        players=[
            PlayerSpec(name=args.p1, number=args.n1,
                       position=args.pos1, side="left"),
            PlayerSpec(name=args.p2, number=args.n2,
                       position=args.pos2, side="right"),
        ],
    )

    team_abbr = spec.team.abbreviation.lower()
    p1_slug = spec.players[0].name.split()[-1].lower()
    p2_slug = spec.players[1].name.split()[-1].lower()
    slug = f"{team_abbr}_{p1_slug}_{p2_slug}"

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    ref = load_sticker_ref()
    prompt = build_sticker_prompt(spec)

    log.info(f"Team    : {spec.team.name}")
    log.info(
        f"Players : {spec.players[0].name} #{args.n1} + {spec.players[1].name} #{args.n2}")
    log.info(f"Prompt  : {len(prompt)} chars")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    log.info(f"Generating — Pro {SIZE}...")

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, ref],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="3:2", image_size=SIZE),
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

    # Save raw
    raw_path = out_dir / f"{slug}_raw.jpg"
    raw_img.save(raw_path, format="JPEG", quality=95)
    log.info(f"Raw     : {raw_path} ({raw_img.width}x{raw_img.height}px)")

    # Chroma key → sticker PNG
    sticker = extract_sticker(raw_img)
    sticker_path = out_dir / f"{slug}_sticker.png"
    sticker.save(sticker_path, format="PNG")
    log.info(f"Sticker : {sticker_path}")


if __name__ == "__main__":
    main()
