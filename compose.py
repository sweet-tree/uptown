"""
Pass 3 — Card compositor.

Assembles a print-ready collectible landscape card from three layers:

  Layer 0 — Foil background  (foil_black.png, full-bleed)
  Layer 1 — Sticker          (die-cut cartoon illustration, RGBA PNG)
  Layer 2 — Marquee sign     (die-cut theatre sign, RGBA PNG)

Layout algorithm
────────────────
The marquee NEVER overlaps the sticker art. It floats in the foil header zone,
directly above the sticker's die-cut top edge — this is the Panini/Topps rule:
the nameplate lives above the illustration, never on it.

  ┌─────────────────────────────────────────────────────┐  ← canvas top
  │  MARQUEE_TOP_MARGIN px of foil                      │
  │  ┌───────── MARQUEE (visible sign) ───────────┐     │
  │  └─────────────────────────────────────────────┘     │
  │  MARQUEE_GAP_PX of foil                              │
  │  ╔══ sticker die-cut top edge ═════════════════════╗ │
  │  ║                                                  ║ │
  │  ║   sticker illustration (stadium · skyline ·     ║ │
  │  ║   players)                                       ║ │
  │  ╚═════════════════════════════════════════════════╝ │
  │  bottom foil border                                  │
  └─────────────────────────────────────────────────────┘  ← canvas bottom

Canvas base is 2528×1696 (matching foil_black.png and sticker output).
If the sticker's own transparent header is smaller than the required header
zone, the canvas is extended upward by exactly the shortfall. The sticker
shifts down the same amount so its content position is unchanged.

Usage:
  venv/bin/python compose.py \\
    --sticker output/kc_mahomes_kelce_sticker.png \\
    --marquee output/marquee_mahomes_kelce_sticker.png \\
    --out output/kc_mahomes_kelce_final.jpg
"""

import argparse
import logging
import numpy as np
from pathlib import Path
from PIL import Image

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Canonical canvas ───────────────────────────────────────────────────────────
CANVAS_W = 2528
CANVAS_H = 1696
FOIL     = Path("assets/foil_black.png")

# ── Layout constants ───────────────────────────────────────────────────────────
# Marquee visible sign width as a fraction of canvas width.
# 0.32 gives a commanding sign that fills the center third comfortably.
MARQUEE_W_FRAC     = 0.32

# Foil gap between the marquee sign bottom and the sticker die-cut top edge.
MARQUEE_GAP_PX     = 24

# Foil breathing room from canvas top edge to marquee sign top.
MARQUEE_TOP_MARGIN = 44

# Foil breathing room below the sticker die-cut bottom edge.
# Matched to the top margin so the card is balanced on all sides.
BOTTOM_MARGIN      = 60


# ── Helpers ────────────────────────────────────────────────────────────────────

def _content_bbox(img: Image.Image) -> tuple[int, int, int, int]:
    """
    Bounding box (left, top, right, bottom) of non-transparent pixels.
    Threshold α > 10 excludes near-invisible anti-aliased fringe pixels.
    Returns full image bounds if the image is fully transparent.
    """
    arr   = np.array(img.convert("RGBA"))
    alpha = arr[:, :, 3]
    rows  = np.where(alpha.max(axis=1) > 10)[0]
    cols  = np.where(alpha.max(axis=0) > 10)[0]
    if len(rows) == 0 or len(cols) == 0:
        return (0, 0, img.width, img.height)
    return (int(cols[0]), int(rows[0]), int(cols[-1] + 1), int(rows[-1] + 1))


def _overlay(base: Image.Image, layer: Image.Image, x: int, y: int) -> None:
    """Alpha-composite layer onto base at (x, y), in-place."""
    base.paste(layer, (x, y), layer)


def _scale_foil(foil: Image.Image, w: int, h: int) -> Image.Image:
    """
    Tile the foil texture to cover an arbitrary canvas size.
    Because the foil is a repeating diamond pattern, tiling preserves
    the texture scale exactly — no stretching artefacts.
    """
    fw, fh = foil.size
    tiled  = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    for y in range(0, h, fh):
        for x in range(0, w, fw):
            tiled.paste(foil, (x, y))
    return tiled


# ── Compositor ─────────────────────────────────────────────────────────────────

def compose(sticker_path: str, marquee_path: str, out_path: str) -> None:
    sticker = Image.open(sticker_path).convert("RGBA")
    marquee = Image.open(marquee_path).convert("RGBA")
    foil    = Image.open(FOIL).convert("RGBA")

    log.info(f"Sticker input  : {sticker.width}×{sticker.height}")
    log.info(f"Marquee input  : {marquee.width}×{marquee.height}")

    # ── Normalize sticker to canonical canvas ──────────────────────────────────
    if sticker.size != (CANVAS_W, CANVAS_H):
        log.info(f"Resizing sticker → {CANVAS_W}×{CANVAS_H}")
        sticker = sticker.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)

    # ── Sticker die-cut top (highest non-transparent pixel across full width) ──
    sticker_bbox    = _content_bbox(sticker)
    sticker_die_top = sticker_bbox[1]   # y coord of top die-cut edge in sticker frame
    log.info(f"Sticker content bbox   : {sticker_bbox}  (die-cut top y={sticker_die_top})")

    # ── Scale marquee to target width (content-aware — strips transparent padding) ──
    m_bbox    = _content_bbox(marquee)
    m_crop_w  = m_bbox[2] - m_bbox[0]
    m_crop_h  = m_bbox[3] - m_bbox[1]
    log.info(f"Marquee content bbox   : {m_bbox}  ({m_crop_w}×{m_crop_h} visible)")

    marquee_crop = marquee.crop(m_bbox)
    target_w     = int(CANVAS_W * MARQUEE_W_FRAC)
    target_h     = int(m_crop_h * (target_w / m_crop_w))
    marquee_scaled = marquee_crop.resize((target_w, target_h), Image.LANCZOS)
    log.info(f"Marquee scaled         : {target_w}×{target_h}")

    # ── Required header zone height ───────────────────────────────────────────
    # = top margin + marquee height + gap to sticker die-cut
    required_header = MARQUEE_TOP_MARGIN + target_h + MARQUEE_GAP_PX

    # Canvas must be extended upward if the sticker's own transparent header
    # is shorter than the required header zone.
    ext_top   = max(0, required_header - sticker_die_top)

    # Canvas height: just enough to fit sticker content + balanced bottom margin.
    # We don't blindly use CANVAS_H — we trim based on actual content bottom.
    sticker_die_bottom = sticker_bbox[3]   # y of lowest content pixel in sticker frame
    sticker_y          = ext_top           # where sticker frame starts in canvas
    canvas_h           = sticker_y + sticker_die_bottom + BOTTOM_MARGIN

    log.info(f"Header zone required   : {required_header}px")
    log.info(f"Sticker own header     : {sticker_die_top}px")
    log.info(f"Sticker content bottom : y={sticker_die_bottom} (in sticker frame)")
    log.info(f"Canvas extension (top) : {ext_top}px  →  {CANVAS_W}×{canvas_h}")

    # ── Build canvas ───────────────────────────────────────────────────────────
    canvas = Image.new("RGBA", (CANVAS_W, canvas_h), (0, 0, 0, 255))

    # Layer 0: tiled foil background
    canvas.paste(_scale_foil(foil, CANVAS_W, canvas_h), (0, 0))
    log.info("  ✓ foil (tiled)")

    # Layer 1: sticker — shifted down by ext_top so its art position is unchanged
    _overlay(canvas, sticker, 0, sticker_y)
    log.info(f"  ✓ sticker at (0, {sticker_y})")

    # Layer 2: marquee — bottom flush with sticker die-cut top minus gap
    sticker_die_top_canvas = sticker_y + sticker_die_top   # in canvas coords
    marquee_bottom = sticker_die_top_canvas - MARQUEE_GAP_PX
    marquee_top    = marquee_bottom - target_h
    marquee_x      = (CANVAS_W - target_w) // 2

    _overlay(canvas, marquee_scaled, marquee_x, marquee_top)
    log.info(
        f"  ✓ marquee at ({marquee_x}, {marquee_top})  "
        f"size {target_w}×{target_h}  "
        f"top-margin={marquee_top}px  "
        f"gap={MARQUEE_GAP_PX}px  "
        f"bottom={marquee_bottom}px"
    )

    # ── Save ───────────────────────────────────────────────────────────────────
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(str(out), format="JPEG", quality=95)
    log.info(f"Saved : {out}  ({CANVAS_W}×{canvas_h})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pass 3 — compose sticker + marquee into final card")
    parser.add_argument("--sticker", required=True, help="Sticker PNG path (RGBA)")
    parser.add_argument("--marquee", required=True, help="Marquee PNG path (RGBA)")
    parser.add_argument("--out",     required=True, help="Output JPEG path")
    args = parser.parse_args()
    compose(args.sticker, args.marquee, args.out)


if __name__ == "__main__":
    main()
