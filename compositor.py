"""
Compositor — chroma key extraction with green spill suppression.

Pipeline:
  1. Dual-condition mask: RGB Euclidean distance + green channel dominance
  2. Erode 2px to remove green fringing
  3. Gaussian blur the mask edge for smooth alpha transition
  4. Re-threshold to keep crisp anti-aliased edges
  5. Despill — suppress residual green color cast on semi-transparent edge pixels
"""

import logging
import numpy as np
from PIL import Image, ImageFilter

log = logging.getLogger(__name__)

CHROMA_R, CHROMA_G, CHROMA_B = 0, 255, 0
TOLERANCE   = 80
ERODE_PX    = 2      # increased from 1 — tighter edge for AI-generated images
BLUR_RADIUS = 2.0    # tightened from 3.0 — less bloom on edges


def extract_sticker(
    card: Image.Image,
    erode_px: int = ERODE_PX,
) -> Image.Image:
    """
    Remove chroma green background. Returns RGBA with clean edges and no
    green spill on semi-transparent border pixels.
    """
    log.info("Chroma key extraction...")
    arr = np.array(card.convert("RGB")).astype(np.int32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # ── Condition 1: RGB Euclidean distance ───────────────────────────────
    dist = np.sqrt(
        (r - CHROMA_R) ** 2 +
        (g - CHROMA_G) ** 2 +
        (b - CHROMA_B) ** 2
    )

    # ── Condition 2: green channel dominance ──────────────────────────────
    # Catches bright green pixels that slip past the Euclidean check.
    # Thresholds are conservative — won't remove Packers jerseys or grass.
    green_dominant = (
        (g > 200) &
        (g > r * 3) &
        (g > b * 3)
    )

    # Foreground = passes distance threshold AND is not a dominant green pixel
    fg_mask = ((dist > TOLERANCE) & ~green_dominant).astype(np.uint8) * 255
    mask_img = Image.fromarray(fg_mask, "L")

    # ── Erode ─────────────────────────────────────────────────────────────
    for _ in range(erode_px):
        mask_img = mask_img.filter(ImageFilter.MinFilter(3))

    # ── Blur for smooth anti-aliased edge ─────────────────────────────────
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=BLUR_RADIUS))

    # ── Re-threshold ──────────────────────────────────────────────────────
    mask_arr = np.array(mask_img)
    mask_arr = np.clip(
        (mask_arr.astype(np.float32) - 30) / (225 - 30) * 255,
        0, 255
    ).astype(np.uint8)

    # ── Build RGBA ────────────────────────────────────────────────────────
    rgba_arr = np.array(card.convert("RGBA"))
    rgba_arr[:, :, 3] = mask_arr

    # ── Despill — green spill suppression ─────────────────────────────────
    # Edge pixels picked up a green tint from the chroma background.
    # Fix: where G > max(R, B), clamp G down to max(R, B).
    # Apply this proportionally to semi-transparent pixels only — fully
    # opaque foreground content (green jerseys, grass) is left untouched.
    r_f = rgba_arr[:, :, 0].astype(np.float32)
    g_f = rgba_arr[:, :, 1].astype(np.float32)
    b_f = rgba_arr[:, :, 2].astype(np.float32)
    a_f = mask_arr.astype(np.float32) / 255.0

    rb_max       = np.maximum(r_f, b_f)
    g_despilled  = np.minimum(g_f, rb_max)

    # Despill strength: 0 at fully opaque (alpha=1), 1 at fully transparent (alpha=0)
    despill_strength         = np.clip(1.0 - a_f, 0.0, 1.0)
    g_final                  = g_f * (1.0 - despill_strength) + g_despilled * despill_strength
    rgba_arr[:, :, 1]        = np.clip(g_final, 0, 255).astype(np.uint8)
    # ──────────────────────────────────────────────────────────────────────

    result     = Image.fromarray(rgba_arr, "RGBA")
    fg_pixels  = int((mask_arr > 128).sum())
    total      = card.width * card.height
    log.info(f"Chroma key: {fg_pixels / total * 100:.1f}% foreground, clean edges + despilled")
    return result
