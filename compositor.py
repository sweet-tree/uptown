"""
Compositor — extracts the floating sticker as an isolated transparent PNG.

Uses rembg with BiRefNet-general (state of the art 2026).
Input:  raw card image (sticker on black background)
Output: transparent PNG with sticker foreground only
"""

import logging
from pathlib import Path
from PIL import Image, ImageFilter
from rembg import remove, new_session

log = logging.getLogger(__name__)

MODEL = "birefnet-general"
ERODE_PX = 3  # tighten mask edge — reduces white border thickness


def extract_sticker(
    card: Image.Image,
    erode_px: int = ERODE_PX,
) -> Image.Image:
    """
    Extract the sticker foreground from a card image on black background.

    Args:
        card:      Raw generated card (sticker on black)
        erode_px:  Pixels to erode alpha mask — tightens the white border

    Returns:
        RGBA PIL image with transparent background.
    """
    log.info(f"Extracting sticker with rembg/{MODEL}...")
    session = new_session(MODEL)
    foreground = remove(card.convert("RGB"), session=session)

    if erode_px > 0:
        r, g, b, a = foreground.split()
        for _ in range(erode_px):
            a = a.filter(ImageFilter.MinFilter(3))
        foreground = Image.merge("RGBA", (r, g, b, a))
        log.info(f"Mask eroded: {erode_px}px")

    return foreground
