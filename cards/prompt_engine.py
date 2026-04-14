"""
Uptowns Prompt Engine — v2.

Single render style: sticker.
  Bold graphic cartoon-illustration. Die-cut borders. Pure black background.
  Reference: assets/uptowns_box_card_clean.png (Cowboys card).

Composition:
  Layer 0 — pure black background
  Layer 1 — stadium + skyline sticker, large, dominant, center-bottom anchored
  Layer 2 — LEFT player, overlapping the LEFT edge of the stadium sticker,
             feet on the platform base, head fully above the stadium roof line
  Layer 3 — RIGHT player, overlapping the RIGHT edge of the stadium sticker,
             feet on the platform base, head fully above the stadium roof line,
             in FRONT of everything

Both players are ALWAYS fully visible head-to-toe. Neither is occluded by the stadium.
The depth illusion comes from foot placement and edge overlap only.

The foil/marquee background is composited programmatically — never generated here.
"""

from pathlib import Path
from PIL import Image as PILImage
from .sports_data import CardSpec

REFERENCE = Path("assets/uptowns_box_card_clean.png")


def load_reference() -> PILImage.Image:
    if not REFERENCE.exists():
        raise FileNotFoundError(f"Reference not found: {REFERENCE}")
    return PILImage.open(REFERENCE)


def build_prompt(spec: CardSpec) -> str:
    team = spec.team
    p1, p2 = spec.players[0], spec.players[1]

    return f"""You are given a reference card image. Study it carefully — replicate its exact illustration style, sticker die-cut treatment, oval platform base, and graphic composition. Then produce a new card with the team and players described below.

---

ILLUSTRATION STYLE:
Match the reference exactly: bold graphic cartoon-illustration hybrid. Clean ink outlines. Flat color fills with subtle cel-shading. No photorealism. No painterly brushwork. Consistent line weight throughout. Every element — stadium, players, trees, skyline — drawn in the same unified illustration style.

---

BACKGROUND:
Pure solid black (#000000). Full bleed, edge to edge. No texture, no gradient, no glow, no vignette.

---

LAYER 1 — STADIUM STICKER (background anchor):
The stadium sticker is the largest element. It occupies the full horizontal width of the card and the bottom 65% of the card height. It sits on a thick dark oval platform base (same as reference).

The sticker has an organic irregular die-cut silhouette edge — not a rectangle, not a perfect oval. The edge is hand-cut looking, slightly uneven, bleeding naturally into the black background. A thin white border traces the entire die-cut edge.

Stadium content:
- {team.uptowns_stadium_prompt}
- '{team.stadium_name}' text clearly on the stadium facade
- {team.logo_prompt} displayed on the stadium building panels
- Illustrated trees and ground-level landscaping at the base of the stadium

Skyline content (rises above the stadium roof, still inside the sticker boundary):
- {team.uptowns_skyline_prompt}
- The skyline fills the upper portion of the sticker, above the stadium roof line
- Sky behind the skyline uses team colors: primary {team.primary_hex}, secondary {team.secondary_hex}

The top edge of the sticker (skyline + sky) reaches the upper 20% of the card. The stadium and skyline together are LARGE and DOMINANT — they are the visual anchor of the entire composition.

---

LAYER 2 — LEFT PLAYER (midground, overlapping stadium left edge):
{p1.name} — full body, head to toe, zero cropping.

Spatial placement:
- Feet land on the oval platform base, left of center
- The player's body overlaps the LEFT edge of the stadium sticker — torso and legs are in front of the stadium sticker edge, creating a depth layer
- Head and shoulders rise ABOVE the top edge of the stadium sticker, into the black background zone
- The player occupies the left third of the card horizontally

Appearance:
- {team.jersey_prompt}
- Jersey number #{p1.number} in {team.number_style}, clearly visible on chest
- {team.helmet_prompt}
- {team.pants_prompt}
- Dynamic action pose — explosive, athletic, mid-motion
- Thin white die-cut border around the entire player silhouette (same weight as reference)
- Same illustration style as the stadium — bold outlines, cel-shaded, no photorealism

---

LAYER 3 — RIGHT PLAYER (foreground, overlapping stadium right edge):
{p2.name} — full body, head to toe, zero cropping.

Spatial placement:
- Feet land on the oval platform base, right of center
- The player's body overlaps the RIGHT edge of the stadium sticker — visually IN FRONT of the stadium, the foreground-most element
- Head and shoulders rise ABOVE the top edge of the stadium sticker, into the black background zone
- The player occupies the right third of the card horizontally

Appearance:
- {team.jersey_prompt}
- Jersey number #{p2.number} in {team.number_style}, clearly visible on chest
- {team.helmet_prompt}
- {team.pants_prompt}
- Dynamic action pose — explosive, athletic, mid-motion, mirrored energy to left player
- Thin white die-cut border around the entire player silhouette (same weight as reference)
- IDENTICAL illustration style to left player — same line weight, same shading, same rendering

---

DEPTH READING SUMMARY (critical — the model must honor this z-order):
  Back  →  black background
         →  stadium sticker (large, center, bottom-anchored)
         →  left player (overlaps stadium left edge, head above stadium top)
  Front →  right player (overlaps stadium right edge, head above stadium top, in front of everything)

Both players are fully visible head to toe. Neither player is hidden behind the stadium. The depth illusion is created by foot placement on the platform and edge overlap only.

---

ABSOLUTE RULES:
- NO marquee sign
- NO text of any kind except '{team.stadium_name}' on the stadium facade
- NO name plates, NO score panels, NO bottom banners
- NO card holder, NO slab, NO plastic case, NO frame
- Pure black background only — no foil, no texture (added separately)
- Landscape 3:2 ratio, full bleed to all four edges
- Both player jersey numbers must be legible"""
