"""
Marquee compositor.

Renders three lines onto the cream panel of assets/marquee_uptowns.png:

    LINE 1  — Player 1 name   (Anton — condensed bold)
    LINE 2  — UPTOWNS         (Bebas Neue — tracked wide, spans panel)
    LINE 3  — Player 2 name   (Anton — condensed bold)

UPTOWNS is the largest line and is letter-spaced so it spans the full
usable panel width, matching the reference card exactly.
All three lines are stacked as a tight block, vertically centered.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

MARQUEE_ASSET = Path("assets/marquee_uptowns.png")

# Fonts
_FONT_BEBAS = "assets/fonts/BebasNeue-Regular.ttf"   # UPTOWNS — wide, bold
# player names — condensed bold
_FONT_ANTON = "assets/fonts/Anton-Regular.ttf"
_FONT_FALLBACK = "/System/Library/Fonts/Supplemental/Impact.ttf"

TEXT_COLOR = (42, 14, 2, 255)   # deep warm brown

# ── Cream panel interior on the 2528x1696 canvas ─────────────────────────────
PANEL_LEFT = 430
PANEL_RIGHT = 2098
PANEL_TOP = 535
PANEL_BOTTOM = 1085
PANEL_CX = (PANEL_LEFT + PANEL_RIGHT) // 2   # 1264
PANEL_W = PANEL_RIGHT - PANEL_LEFT           # 1668
PANEL_H = PANEL_BOTTOM - PANEL_TOP           # 550

# UPTOWNS spans this fraction of panel width (tracked out to fill it)
UPTOWNS_SPAN_FRAC = 0.90   # 90% of panel width = 1501px

# Font height targets as fraction of panel height
UPTOWNS_H_FRAC = 0.42   # UPTOWNS is the tallest line
NAMES_H_FRAC = 0.28   # names are smaller
LINE_GAP_FRAC = 0.03   # tight gap between lines


def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype(_FONT_FALLBACK, size)


def _fit_font_to_height(text: str, font_path: str,
                        target_h: int, max_w: int,
                        start_size: int = 700) -> ImageFont.FreeTypeFont:
    """Largest font where rendered cap height <= target_h and width <= max_w."""
    dummy = Image.new("RGBA", (1, 1))
    draw = ImageDraw.Draw(dummy)
    lo, hi = 10, start_size
    best = _load_font(font_path, lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        font = _load_font(font_path, mid)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if th <= target_h and tw <= max_w:
            best = font
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def _measure(draw: ImageDraw.ImageDraw, text: str,
             font: ImageFont.FreeTypeFont) -> tuple[int, int, tuple]:
    """Return (w, h, bbox) of rendered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1], bbox


def _draw_centered(draw: ImageDraw.ImageDraw, text: str,
                   font: ImageFont.FreeTypeFont,
                   cx: int, y_top: int, color: tuple):
    """Draw text centered on cx, top of glyph at y_top."""
    bbox = draw.textbbox((0, 0), text, font=font)
    x = cx - (bbox[2] - bbox[0]) // 2 - bbox[0]
    y = y_top - bbox[1]
    draw.text((x, y), text, font=font, fill=color)


def _draw_tracked(draw: ImageDraw.ImageDraw, text: str,
                  font: ImageFont.FreeTypeFont,
                  cx: int, y_top: int,
                  target_w: int, color: tuple):
    """
    Draw text with letter-spacing so total width == target_w, centered on cx.
    Each character is placed individually with equal inter-character gaps.
    """
    chars = list(text)
    n = len(chars)

    # Measure each character
    char_data = []
    for ch in chars:
        bbox = draw.textbbox((0, 0), ch, font=font)
        w = bbox[2] - bbox[0]
        char_data.append((ch, w, bbox))

    natural_w = sum(d[1] for d in char_data)
    gap = (target_w - natural_w) / (n - 1) if n > 1 else 0

    # Start x so the full tracked string is centered on cx
    x = cx - target_w / 2

    for ch, cw, bbox in char_data:
        draw.text((x - bbox[0], y_top - bbox[1]), ch, font=font, fill=color)
        x += cw + gap


def render_marquee(player1_name: str, player2_name: str) -> Image.Image:
    """
    Render the marquee sign with player names and UPTOWNS wordmark.

    Args:
        player1_name: Full name of the left/first player  (e.g. "Maxx Crosby")
        player2_name: Full name of the right/second player (e.g. "Ashton Jeanty")

    Returns:
        RGBA PIL Image, same canvas size as the card (2528x1696).
    """
    marquee = Image.open(MARQUEE_ASSET).convert("RGBA")
    draw = ImageDraw.Draw(marquee)

    p1 = player1_name.upper()
    p2 = player2_name.upper()

    # ── Target dimensions ─────────────────────────────────────────────────────
    target_up_h = int(PANEL_H * UPTOWNS_H_FRAC)    # ~231px
    target_name_h = int(PANEL_H * NAMES_H_FRAC)      # ~154px
    gap_px = int(PANEL_H * LINE_GAP_FRAC)      # ~16px
    uptowns_w = int(PANEL_W * UPTOWNS_SPAN_FRAC)  # ~1501px

    # Max width for names — same as UPTOWNS span so they feel aligned
    max_name_w = uptowns_w

    # ── Fit fonts ─────────────────────────────────────────────────────────────
    font_up = _fit_font_to_height(
        "UPTOWNS", _FONT_BEBAS,  target_up_h,   uptowns_w)
    font_p1 = _fit_font_to_height(
        p1,        _FONT_ANTON,  target_name_h, max_name_w)
    font_p2 = _fit_font_to_height(
        p2,        _FONT_ANTON,  target_name_h, max_name_w)

    # ── Measure actual rendered heights ───────────────────────────────────────
    _, h_p1, _ = _measure(draw, p1,        font_p1)
    _, h_up, _ = _measure(draw, "UPTOWNS", font_up)
    _, h_p2, _ = _measure(draw, p2,        font_p2)

    # ── Stack block, vertically centered in panel ─────────────────────────────
    total_h = h_p1 + gap_px + h_up + gap_px + h_p2
    block_top = PANEL_TOP + (PANEL_H - total_h) // 2

    y_p1 = block_top
    y_up = y_p1 + h_p1 + gap_px
    y_p2 = y_up + h_up + gap_px

    # ── Draw ──────────────────────────────────────────────────────────────────
    _draw_centered(draw, p1,        font_p1, PANEL_CX, y_p1, TEXT_COLOR)
    _draw_tracked(draw, "UPTOWNS", font_up, PANEL_CX,
                  y_up, uptowns_w, TEXT_COLOR)
    _draw_centered(draw, p2,        font_p2, PANEL_CX, y_p2, TEXT_COLOR)

    return marquee


if __name__ == "__main__":
    out = render_marquee("Maxx Crosby", "Ashton Jeanty")
    out.save("output/marquee_test.png")
    print(f"Saved output/marquee_test.png ({out.width}x{out.height})")
