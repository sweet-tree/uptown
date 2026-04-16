"""
Player Reference Generator.

Sends the full sticker reference to Gemini and asks it to re-render
one isolated player (left OR right) on chroma green — full body,
portrait 3:4, high-detail face, NO visor.

NAMING CONVENTION — named after the CARD SLOT, not the facing direction:
  assets/player_ref_left.jpg   → LEFT  slot reference → player faces RIGHT toward center
  assets/player_ref_right.jpg  → RIGHT slot reference → player faces LEFT  toward center

Usage:
  venv/bin/python make_player_ref.py --side left
  venv/bin/python make_player_ref.py --side right
  venv/bin/python make_player_ref.py --side right --model pro
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

MODELS = {
    "pro":   "gemini-3-pro-image-preview",
    "flash": "gemini-3.1-flash-image-preview",
}
STICKER_REF = Path("assets/uptowns_sticker_ref.jpg")

PROMPTS = {
    "left": """You are given a collectible sports card illustration with two NFL players flanking a stadium.

Your task: RE-RENDER the LEFT player only as a clean isolated asset.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT TO REPRODUCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Copy the LEFT player (jersey #3) from the reference EXACTLY:
• Same illustration style — bold ink outlines, detailed cel-shading, premium sports card art
• Same Cowboys white jersey with number 3 in blue
• Same Cowboys star helmet
• Same running pose — carrying football tucked under arm, driving forward, body and gaze facing RIGHT
• Same athletic body proportions and dynamic energy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACE — HIGH PRIORITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• NO visor — completely open face mask, full face visible
• High-detail face: skin texture, eyes, nose, mouth, expression clearly rendered
• The face is the most detailed part of the illustration — premium portrait quality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Background: pure flat chroma green (#00FF00), full bleed to all edges
• NOTHING else — no stadium, no skyline, no ground, no shadow, no other players
• Every pixel outside the player is solid #00FF00

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FRAMING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Full body — top of helmet to bottom of cleats, NO cropping of any body part
• Both feet and cleats fully visible at the bottom of frame
• Player fills ~85% of frame height, centered horizontally
• ~7% green margin on all four sides
• Portrait 3:4 format""",

    "right": """Generate a premium isolated NFL player illustration for a collectible sports card — using the provided reference image as the EXACT style guide.

This is a MIRROR of the left player in the reference: same illustration quality, same energy, same premium card art — but the player faces LEFT instead of right.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ILLUSTRATION STYLE — MATCH THE REFERENCE EXACTLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Bold clean ink outlines on every edge — same line weight as reference
• Smooth cel-shaded colors with sharp highlight gradients — no painterly blur
• High-contrast premium sports card illustration — vivid, saturated, crisp
• Same level of detail as the left player in the reference — not simpler, not softer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Dallas Cowboys #88 — white home jersey, blue numbers, Cowboys star helmet
• Athletic wide receiver body — lean, muscular, explosive
• FACING LEFT — entire body oriented left, stride driving toward viewer's left

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Sprinting at full speed toward the LEFT — explosive stride, body leaning forward
• Lead leg fully extended forward, drive leg pushing off behind
• Arms pumping naturally — elbows bent ~90°, fists closed in football gloves
• Body weight forward, aggressive athletic lean — same explosive energy as the left reference player

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACE — MOST IMPORTANT DETAIL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ZERO visor — completely open face cage, nothing covering the face
• Full face turned slightly LEFT with the body — clearly and fully visible
• Eyes: detailed irises, whites visible, focused intense gaze
• Skin: realistic tone with light and shadow — same quality as the reference left player face
• Nose, lips, jaw, cheekbones — all clearly defined with proper shading
• Determined, intense athletic expression — premium portrait-quality face rendering
• The face must be as detailed and clear as the LEFT player face in the reference

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARMS & HANDS — CRITICAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Both arms fully rendered — proper muscular anatomy, no missing limbs
• Biceps and forearms clearly defined with shading and highlight
• Hands in football gloves — gloves fit tight, fingers naturally closed in a running fist
• NEVER open splayed hands, NEVER jazz hands, NEVER distorted fingers
• Glove texture visible — same quality as reference

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UNIFORM DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• White jersey tucked in, number 88 large and clearly legible on chest
• Silver metallic Cowboys helmet with blue five-pointed star on the side
• White cleats, both feet fully visible

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS & FRAMING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Background: pure flat chroma green (#00FF00) — every pixel outside the player
• NOTHING else — no stadium, no ground, no shadow, no other players, no decorations
• Full body — helmet top to cleat bottoms — ZERO cropping
• Player fills ~85% of frame height, centered horizontally
• ~7% green margin on all sides
• Portrait 3:4 format""",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate player reference via Gemini")
    parser.add_argument("--side",  required=True, choices=["left", "right"],
                        help="Which player to extract from the sticker ref")
    parser.add_argument("--model", default="flash", choices=["pro", "flash"])
    args = parser.parse_args()

    out_path = Path(f"assets/player_ref_{args.side}.jpg")
    model_id = MODELS[args.model]
    size     = "4K" if args.model == "pro" else "2K"

    log.info(f"Side     : {args.side} → faces {'right' if args.side == 'left' else 'left'}")
    log.info(f"Model    : {model_id}  3:4 {size}")
    log.info(f"Input    : {STICKER_REF}")
    log.info(f"Output   : {out_path}")

    ref = PILImage.open(STICKER_REF)

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=model_id,
        contents=[PROMPTS[args.side], ref],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="3:4", image_size=size),
        ),
    )

    raw_img = None
    for part in response.parts:
        if part.thought:
            continue
        if part.text:
            log.info(f"Model    : {part.text[:200]}")
        elif part.inline_data is not None:
            raw_img = PILImage.open(io.BytesIO(part.inline_data.data))
            break

    if raw_img is None:
        raise RuntimeError("No image returned from API")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    raw_img.save(out_path, format="JPEG", quality=97)
    log.info(f"Saved    : {out_path}  ({raw_img.width}×{raw_img.height})")


if __name__ == "__main__":
    main()
