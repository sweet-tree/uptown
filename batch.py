"""
Uptowns — batch runner.

Generates 6 verified NFL cards. All players confirmed on NFL.com rosters April 2026.

Usage:
  python batch.py
  python batch.py --dry-run
"""

import argparse
import io
import logging
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image as PILImage

from cards.sports_data import get_team, PlayerSpec, CardSpec
from cards.prompt_engine import build_prompt, load_reference
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
DELAY = 5  # seconds between cards

# ── Verified batch — NFL.com rosters, April 2026 ─────────────────────────────
BATCH = [
    CardSpec(
        team=get_team("BAL"),
        players=[
            PlayerSpec(name="Lamar Jackson",   number="8",
                       position="qb", side="left"),
            PlayerSpec(name="Derrick Henry",   number="22",
                       position="rb", side="right"),
        ],
    ),
    CardSpec(
        team=get_team("KC"),
        players=[
            PlayerSpec(name="Patrick Mahomes", number="15",
                       position="qb", side="left"),
            PlayerSpec(name="Travis Kelce",    number="87",
                       position="te", side="right"),
        ],
    ),
    CardSpec(
        team=get_team("DAL"),
        players=[
            PlayerSpec(name="Dak Prescott",    number="4",
                       position="qb", side="left"),
            PlayerSpec(name="CeeDee Lamb",     number="88",
                       position="wr", side="right"),
        ],
    ),
    CardSpec(
        team=get_team("CHI"),
        players=[
            PlayerSpec(name="Caleb Williams",  number="18",
                       position="qb", side="left"),
            PlayerSpec(name="Rome Odunze",     number="15",
                       position="wr", side="right"),
        ],
    ),
    CardSpec(
        team=get_team("LV"),
        players=[
            PlayerSpec(name="Maxx Crosby",     number="98",
                       position="default", side="left"),
            PlayerSpec(name="Ashton Jeanty",   number="2",
                       position="rb",      side="right"),
        ],
    ),
    CardSpec(
        team=get_team("GB"),
        players=[
            PlayerSpec(name="Jordan Love",     number="10",
                       position="qb", side="left"),
            PlayerSpec(name="Jayden Reed",     number="11",
                       position="wr", side="right"),
        ],
    ),
]
# ─────────────────────────────────────────────────────────────────────────────


def slug(spec: CardSpec) -> str:
    team = spec.team.abbreviation.lower()
    p1 = spec.players[0].name.split()[-1].lower()
    p2 = spec.players[1].name.split()[-1].lower()
    return f"{team}_{p1}_{p2}"


def run_card(client, spec: CardSpec, ref, out_dir: Path):
    s = slug(spec)
    prompt = build_prompt(spec)

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
            log.info(f"   Model: {part.text[:120]}")
        elif part.inline_data is not None:
            raw_img = PILImage.open(io.BytesIO(part.inline_data.data))
            break

    if raw_img is None:
        raise RuntimeError("No image returned")

    raw_path = out_dir / f"{s}_raw.jpg"
    raw_img.save(raw_path, format="JPEG", quality=92)
    log.info(f"   Raw     : {raw_path}")

    sticker = extract_sticker(raw_img)
    sticker_path = out_dir / f"{s}_sticker.png"
    sticker.save(sticker_path, format="PNG")
    log.info(f"   Sticker : {sticker_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    log.info(f"Batch: {len(BATCH)} cards — Pro {SIZE}")
    log.info("=" * 60)

    if args.dry_run:
        for i, spec in enumerate(BATCH, 1):
            p1, p2 = spec.players
            log.info(
                f"[{i}] {spec.team.name}: {p1.name} #{p1.number} + {p2.name} #{p2.number}")
        return

    ref = load_reference()
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    succeeded, failed = 0, 0
    for i, spec in enumerate(BATCH, 1):
        p1, p2 = spec.players
        log.info(
            f"\n[{i}/{len(BATCH)}] {spec.team.name}: {p1.name} + {p2.name}")
        try:
            run_card(client, spec, ref, out_dir)
            succeeded += 1
        except Exception as e:
            log.error(f"   FAILED: {e}")
            failed += 1

        if i < len(BATCH):
            log.info(f"   Waiting {DELAY}s...")
            time.sleep(DELAY)

    log.info("\n" + "=" * 60)
    log.info(f"Done: {succeeded} succeeded, {failed} failed")
    log.info(f"Output: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
