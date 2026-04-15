"""
Uptowns Prompt Engine — v4.

Pass 1 — sticker (stadium + skyline + players) on chroma green. No marquee.
Pass 2 — marquee sign on chroma green. See make_marquee.py.
Pass 3 — composite: sticker + marquee. See compose.py.

Reference: assets/uptowns_sticker_ref_red_diecut.jpg
  The reference uses a RED die-cut border to illustrate the correct shape.
  All generated cards use a WHITE die-cut border.
"""

from pathlib import Path
from PIL import Image as PILImage
from .sports_data import CardSpec

STICKER_REF = Path("assets/uptowns_sticker_ref_red_diecut.jpg")
MARQUEE_REF = Path("assets/marquee_uptowns.png")
CARD_REF    = Path("assets/uptowns_card_ref.jpg")


def load_sticker_ref() -> PILImage.Image:
    if not STICKER_REF.exists():
        raise FileNotFoundError(f"Sticker ref not found: {STICKER_REF}")
    return PILImage.open(STICKER_REF)


def load_marquee_ref() -> PILImage.Image:
    if not MARQUEE_REF.exists():
        raise FileNotFoundError(f"Marquee ref not found: {MARQUEE_REF}")
    return PILImage.open(MARQUEE_REF)


def load_card_ref() -> PILImage.Image:
    if not CARD_REF.exists():
        raise FileNotFoundError(f"Card ref not found: {CARD_REF}")
    return PILImage.open(CARD_REF)


def load_references() -> tuple[PILImage.Image, PILImage.Image]:
    """Legacy compat for batch.py."""
    return load_marquee_ref(), load_card_ref()


def load_reference() -> PILImage.Image:
    return load_sticker_ref()


def _player_action(position: str) -> str:
    pos = position.lower()
    if pos == "qb":
        return "throwing a perfect spiral — arm fully cocked back, football clearly visible in throwing hand, classic QB release motion"
    elif pos == "rb":
        return "running at full speed — football tucked under arm, driving forward with explosive stride, low powerful burst"
    elif pos in ("wr", "te"):
        return "leaping to make a catch — arms fully extended overhead, football clearly visible at fingertips, full extension"
    elif pos == "de":
        return "explosive pass rush burst — arms raised high, powerful athletic stance, no ball"
    else:
        return "explosive athletic action pose — dynamic, powerful, full energy"


def build_sticker_prompt(spec: CardSpec) -> str:
    team = spec.team
    p1, p2 = spec.players[0], spec.players[1]
    p1_action = _player_action(p1.position)
    p2_action = _player_action(p2.position)
    sky = (team.uptowns_sky_prompt
           or f"Sky in team colors {team.primary_hex} to {team.secondary_hex}, atmospheric and saturated")

    return f"""Generate a new Uptowns collectible sticker for a different team, using the provided reference image as the exact style and composition guide.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFERENCE GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COPY from the reference exactly:
• Illustration style — bold graphic cartoon, clean ink outlines, flat cel-shaded colors, consistent line weight throughout
• Composition — oval platform base, stadium centered on the platform, skyline filling the background, two players standing in front
• Die-cut border SHAPE — curvy and organic, tracing the exact content silhouette

CHANGE from the reference:
• Die-cut border COLOR — the reference uses red to show the correct shape; this card must use WHITE (#FFFFFF)
• All team content — stadium, skyline, players, colors as specified below

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Background: pure chroma green (#00FF00), full bleed to all four edges
• Every pixel outside the sticker content is exactly #00FF00 — no shadows, no anti-aliasing, no color bleeding into the green
• Aspect ratio: 3:2 landscape

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPOSITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLATFORM:
Wide oval base spanning the full card width, centered — identical in scale and shape to the reference.

STADIUM (sits on the platform):
• {team.uptowns_stadium_prompt}
• "{team.stadium_name}" clearly lettered on the facade
• {team.logo_prompt} on the building panels
• Trees and landscaping at the base of the platform

SKYLINE (background — fills the space behind the stadium, rises above the roofline):
• {team.uptowns_skyline_prompt}
• {sky}
• Sky elements fill all the way to the very top of the sticker — there is zero flat or empty sky zone. The organic tops of buildings, trees, or clouds physically define the die-cut top edge.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLAYERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Both players:
• Full body — head to boots, zero cropping of any body part
• Face fully visible — helmet on with no visor covering the face
• Feet planted on the platform surface, head and shoulders in the upper sticker area
• Entire body in front of the stadium — stadium is background layer only
• Rendered at the same illustration quality, line weight, and style

LEFT — {p1.name} #{p1.number}:
• Positioned in the left third of the card
• {team.jersey_prompt}
• {team.helmet_prompt}
• {team.pants_prompt}
• Number #{p1.number} in {team.number_style} — clearly legible on chest
• Pose: {p1_action}
• Thin WHITE (#FFFFFF) die-cut border tracing the exact body silhouette

RIGHT — {p2.name} #{p2.number}:
• Positioned in the right third of the card
• {team.jersey_prompt}
• {team.helmet_prompt}
• {team.pants_prompt}
• Number #{p2.number} in {team.number_style} — clearly legible on chest
• Pose: {p2_action}
• Thin WHITE (#FFFFFF) die-cut border tracing the exact body silhouette

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIE-CUT BORDER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Color: WHITE (#FFFFFF) — solid, clean, uniform
• Traces the exact organic silhouette of all sticker content
• Top edge: rises and falls with each building, tree, or cloud — no flat sections, no smooth arcs, no ovals or rectangles
• The content silhouette IS the die-cut shape — there is no separate outer border geometry
• Match the reference border shape precision exactly — just change red to white

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• No marquee sign, banners, name plates, or card frame
• No text except "{team.stadium_name}" on the facade
• Both jersey numbers clearly legible
• Background: pure #00FF00 only — nothing else outside the sticker"""


def build_prompt(spec: CardSpec) -> str:
    """Legacy alias."""
    return build_sticker_prompt(spec)
