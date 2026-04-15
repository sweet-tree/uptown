"""
Pass 3 — Pillow compositor.

Merges Pass 1 sticker + Pass 2 marquee into a final card.

Strategy:
  - Sticker is 2528x1696, content starts at y~275
  - Marquee is placed ABOVE the sticker content top with a gap
  - Canvas is extended upward to fit the marquee without overlap
  - Foil background tiles the full extended canvas

Usage:
  venv/bin/python compose.py --sticker output/lv_crosby_jeanty_sticker.png \
                              --marquee output/marquee_crosby_jeanty_sticker.png \
                              --out output/lv_crosby_jeanty_final.jpg
"""

import argparse
import logging
import numpy as np
from pathlib import Path
from PIL import Image

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)-8s  %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger(__name__)

CANVAS_W = 2528
CANVAS_H = 1696
FOIL = Path("assets/foil_black.png")
MARQUEE_WIDTH_FRAC = 0.52    # marquee spans 52% of card width
GAP_PX = 40      # gap between marquee bottom and sticker content top
TOP_PADDING = 30      # breathing room above marquee


def compose(sticker_path: str, marquee_path: str, out_path: str):
    sticker = Image.open(sticker_path).convert("RGBA")
    marquee = Image.open(marquee_path).convert("RGBA")
    foil = Image.open(FOIL).convert("RGBA")

    log.info(f"Sticker : {sticker.size}")
    log.info(f"Marquee : {marquee.size}")

    # ── Scale marquee ─────────────────────────────────────────────────────────
    target_w = int(CANVAS_W * MARQUEE_WIDTH_FRAC)
    scale = target_w / marquee.width
    target_h = int(marquee.height * scale)
    marquee_scaled = marquee.resize((target_w, target_h), Image.LANCZOS)

    # ── Find sticker content top ──────────────────────────────────────────────
    arr = np.array(sticker)
    rows = np.where(arr[:, :, 3].max(axis=1) > 10)[0]
    sticker_content_top = int(rows[0]) if len(rows) else 0
    log.info(f"Sticker content top: y={sticker_content_top}")

    # ── Calculate canvas extension ────────────────────────────────────────────
    # marquee bottom = sticker_content_top - GAP_PX
    # marquee top    = marquee_bottom - target_h
    # extra_top      = TOP_PADDING - marquee_top  (if marquee_top < TOP_PADDING)
    marquee_bottom = sticker_content_top - GAP_PX
    marquee_top = marquee_bottom - target_h
    extra_top = max(0, TOP_PADDING - marquee_top)
    new_h = CANVAS_H + extra_top

    log.info(f"Canvas: {CANVAS_W}x{new_h} (extended {extra_top}px)")

    # ── Build canvas with foil background ────────────────────────────────────
    canvas = Image.new("RGBA", (CANVAS_W, new_h), (0, 0, 0, 255))
    if foil.size != (CANVAS_W, CANVAS_H):
        foil = foil.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    canvas.paste(foil, (0, extra_top))

    # ── Layer 1: Sticker ──────────────────────────────────────────────────────
    if sticker.size != (CANVAS_W, CANVAS_H):
        sticker = sticker.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
    canvas.paste(sticker, (0, extra_top), sticker)
    log.info("Sticker composited")

    # ── Layer 2: Marquee ──────────────────────────────────────────────────────
    mx = (CANVAS_W - target_w) // 2
    my = extra_top + marquee_top
    my = max(0, my)
    canvas.paste(marquee_scaled, (mx, my), marquee_scaled)
    log.info(
        f"Marquee at ({mx},{my}), size {target_w}x{target_h}, gap={GAP_PX}px")

    # ── Save ──────────────────────────────────────────────────────────────────
    Path(out_path).parent.mkdir(exist_ok=True)
    canvas.convert("RGB").save(out_path, format="JPEG", quality=95)
    log.info(f"Saved   : {out_path} ({CANVAS_W}x{new_h})")


def main():
    parser = argparse.ArgumentParser(
        description="Pass 3 — compose sticker + marquee")
    parser.add_argument("--sticker", required=True)
    parser.add_argument("--marquee", required=True)
    parser.add_argument("--out",     required=True)
    args = parser.parse_args()
    compose(args.sticker, args.marquee, args.out)


if __name__ == "__main__":
    main()
