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

# best output — shows exact target layout
REFERENCE = Path("assets/uptowns_card_ref.jpg")
MARQUEE_REF = Path("assets/marquee_ref.png")


def load_references() -> tuple[PILImage.Image, PILImage.Image]:
    if not REFERENCE.exists():
        raise FileNotFoundError(f"Reference not found: {REFERENCE}")
    if not MARQUEE_REF.exists():
        raise FileNotFoundError(f"Marquee ref not found: {MARQUEE_REF}")
    return PILImage.open(REFERENCE), PILImage.open(MARQUEE_REF)


# Keep backward compat
def load_reference() -> PILImage.Image:
    return PILImage.open(REFERENCE)


def build_prompt(spec: CardSpec) -> str:
    team = spec.team
    p1, p2 = spec.players[0], spec.players[1]

    return f"""You are given two reference images:
- IMAGE 1: A completed Uptowns sports card — this shows the EXACT target layout, composition, and style. Replicate this layout precisely: the organic die-cut sticker with oval platform base in the bottom 65% of the card, two players flanking the stadium fully in front, the marquee sign floating in the top portion with black space separating it from the sticker, pure black background.
- IMAGE 2: A theatre marquee sign — copy this sign exactly (same frame, same bulbs, same cream panel, same glow) but with the new player names.

Produce a new card for a different team following this exact same layout.

---

ILLUSTRATION STYLE:
Match IMAGE 1 exactly: bold graphic cartoon-illustration hybrid. Clean ink outlines. Flat color fills with subtle cel-shading. No photorealism. No painterly brushwork. Consistent line weight throughout. Every element — stadium, players, trees, skyline, marquee — drawn in the same unified illustration style.

---

BACKGROUND:
Pure solid black (#000000). Full bleed, edge to edge. No texture, no gradient, no glow, no vignette. This applies to ALL teams regardless of team colors — the background is ALWAYS pure black, never white, never grey, never any other color.

---

LAYER 1 — STADIUM STICKER (bottom anchor):
The stadium sticker occupies the BOTTOM 65% of the card height and the full horizontal width. It sits on a thick dark oval platform base (same as IMAGE 1). The sticker does NOT extend into the top 30% of the card — that space is reserved for the marquee sign and black background.

The sticker has an organic irregular die-cut silhouette edge — the outline traces the actual shapes of the content inside: it dips and rises following the rooftops of buildings in the skyline, follows the curves of the stadium roof, and wraps tightly around the player silhouettes. The top edge of the sticker is NOT a smooth arc, NOT an oval, NOT a straight line — it is an irregular, hand-cut looking contour that follows the skyline buildings and content shapes, creating a jagged city-skyline-like top profile. A thin white border traces this entire die-cut edge consistently.

Stadium content:
- {team.uptowns_stadium_prompt}
- '{team.stadium_name}' text clearly on the stadium facade
- {team.logo_prompt} displayed on the stadium building panels
- Illustrated trees and ground-level landscaping at the base of the stadium

Skyline content (rises above the stadium roof, still inside the sticker boundary):
- {team.uptowns_skyline_prompt}
- The skyline fills the upper portion of the sticker, above the stadium roof line
- Sky behind the skyline uses team colors: primary {team.primary_hex}, secondary {team.secondary_hex}
- The sky is ALWAYS a dark or saturated color — never white, never light grey, never pale. Use the team's actual hex colors as the sky fill.
- NO clouds, NO fog, NO haze — clear sky only, solid color gradient

The top edge of the sticker (skyline + sky) reaches the upper 35% of the card. The stadium and skyline together are LARGE and DOMINANT — the sticker fills the full card width edge to edge.

---

LAYER 2 — LEFT PLAYER (midground, overlapping stadium left edge):
{p1.name} — full body, head to toe, zero cropping. EVERY part of this player — both hands, both arms, both legs, both feet — must be fully visible. Nothing hidden behind the stadium.

Spatial placement:
- Feet land on the oval platform base, left of center
- The player's ENTIRE body — including both hands and arms — is rendered IN FRONT of the stadium sticker. The stadium is behind the player, not in front.
- Head and shoulders rise ABOVE the top edge of the stadium sticker
- The player occupies the left third of the card horizontally

Appearance:
- {team.jersey_prompt}
- Jersey number #{p1.number} in {team.number_style}, clearly visible on chest
- {team.helmet_prompt}
- {team.pants_prompt}
- Dynamic action pose — explosive, athletic, mid-motion
- Thin white die-cut border around the entire player silhouette — the border must follow the organic curves of the body, never straight lines or rectangles
- Same illustration style as the stadium — bold outlines, cel-shaded, no photorealism

---

LAYER 3 — RIGHT PLAYER (foreground, overlapping stadium right edge):
{p2.name} — full body, head to toe, zero cropping. EVERY part of this player — both hands, both arms, both legs, both feet — must be fully visible. Nothing hidden behind the stadium.

Spatial placement:
- Feet land on the oval platform base, right of center
- The player's ENTIRE body is rendered IN FRONT of the stadium sticker — the foreground-most element
- Head and shoulders rise ABOVE the top edge of the stadium sticker
- Occupies the right third of the card horizontally

Appearance:
- {team.jersey_prompt}
- Jersey number #{p2.number} in {team.number_style}, clearly visible on chest
- {team.helmet_prompt}
- {team.pants_prompt}
- Dynamic action pose — explosive, athletic, mid-motion, mirrored energy to left player
- Thin white die-cut border around the entire player silhouette — the border must follow the organic curves of the body, never straight lines or rectangles
- IDENTICAL illustration style to left player

---

LAYER 4 — MARQUEE SIGN (top center, floating above the sticker):
Take the exact marquee sign from IMAGE 2 and place it onto this card. Do not redesign or reinvent it — copy it exactly as it appears in IMAGE 2: same ornate curved frame shape, same gold border, same amber glowing bulbs, same cream/ivory panel interior, same warm glow. The marquee background is ALWAYS the cream/ivory panel — never white, never transparent, never a solid rectangle with no frame details.

Only change the text to:
- TOP LINE:    "{p1.name.upper()}"
- CENTER LINE: "UPTOWNS"
- BOTTOM LINE: "{p2.name.upper()}"

Placement on the card — this is critical:
- The marquee occupies the TOP portion of the card (top 30% of card height)
- The sticker occupies the BOTTOM portion of the card (bottom 65% of card height)
- There is a clear visible black gap between the bottom edge of the marquee and the top edge of the sticker — they do NOT touch, overlap, or layer on top of each other
- The marquee is centered horizontally, spanning approximately 55% of the card width
- Pure black background is visible between the marquee and the sticker

---

DEPTH READING SUMMARY — CRITICAL, the model MUST honor this z-order exactly:
  Back  →  black background
         →  stadium sticker (large, center, bottom-anchored)
         →  left player: FULLY IN FRONT of stadium — every body part visible, nothing occluded
         →  right player: FULLY IN FRONT of everything — every body part visible, nothing occluded
  Front →  marquee sign (floating top-center, above all sticker content)

The stadium is BEHIND both players. Players are NEVER behind the stadium. Both players are fully visible head to toe, both hands visible, both arms visible. The depth illusion comes only from foot placement on the platform base.

---

ABSOLUTE RULES:
- NO text except '{team.stadium_name}' on the facade and the marquee sign text
- NO name plates, NO score panels, NO bottom banners
- NO card holder, NO slab, NO plastic case, NO frame
- Pure black background only — no foil, no texture
- Landscape 3:2 ratio, full bleed to all four edges
- Both player jersey numbers must be legible"""
