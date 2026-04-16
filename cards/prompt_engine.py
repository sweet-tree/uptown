"""
Uptowns Prompt Engine — v5.

Pass 1 — sticker (stadium + skyline + players) on chroma green. No marquee.
Pass 2 — marquee sign on chroma green. See make_marquee.py.
Pass 3 — composite: sticker + marquee. See compose.py.

Isolated asset passes:
  make_stadium.py — isolated stadium on chroma green, 4K 4:3
  make_scene.py   — sky + city skyline background, 4K 16:9
  make_player.py  — isolated single player on chroma green, 4K 3:4

Style reference for all isolated assets: assets/uptowns_sticker_ref.jpg
  Semi-realistic sports card illustration — bold ink outlines, detailed shading.
"""

from pathlib import Path
from PIL import Image as PILImage
from .sports_data import CardSpec, TeamData

STICKER_REF    = Path("assets/uptowns_sticker_ref_red_diecut.jpg")
STYLE_REF      = Path("assets/uptowns_sticker_ref.jpg")       # style anchor for backgrounds
# Reference images — named after the CARD SLOT, not the direction the player faces:
#   player_ref_left.jpg  = reference for LEFT  slot → player faces RIGHT (toward center)
#   player_ref_right.jpg = reference for RIGHT slot → player faces LEFT  (toward center)
PLAYER_REF_LEFT  = Path("assets/player_ref_left.jpg")
PLAYER_REF_RIGHT = Path("assets/player_ref_right.jpg")
MARQUEE_REF    = Path("assets/marquee_uptowns.png")
CARD_REF       = Path("assets/uptowns_card_ref.jpg")


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


# ── Style reference loader ─────────────────────────────────────────────────────

def load_style_ref() -> PILImage.Image:
    """Original sticker reference (no red die-cut). Style anchor for background assets."""
    if not STYLE_REF.exists():
        raise FileNotFoundError(f"Style ref not found: {STYLE_REF}")
    return PILImage.open(STYLE_REF)


def load_player_ref(side: str = "left") -> PILImage.Image:
    """Return the reference image matching the card slot.
    side='left'  → player_ref_left.jpg  → player in ref faces RIGHT
    side='right' → player_ref_right.jpg → player in ref faces LEFT
    Model copies the reference direction — no mirroring needed in the prompt.
    """
    path = PLAYER_REF_LEFT if side == "left" else PLAYER_REF_RIGHT
    if not path.exists():
        raise FileNotFoundError(
            f"Player ref not found: {path}\n"
            f"Run: venv/bin/python make_player_ref.py --side {side}"
        )
    return PILImage.open(path)


# ══════════════════════════════════════════════════════════════════════════════
# ISOLATED ASSET PROMPT BUILDERS
# Each function returns a prompt string. Every script also sends STYLE_REF
# as the visual anchor — the model matches that exact illustration style.
# ══════════════════════════════════════════════════════════════════════════════

_STYLE_ANCHOR = """\
Match the exact illustration style visible in the provided reference image:
• Semi-realistic sports card illustration — NOT flat cartoon
• Bold consistent ink outlines with even line weight throughout
• Multi-value shading — visible light, midtone, and shadow on every surface
• Detailed fabric texture on jerseys, 3D volumetric helmet with reflective sheen
• Rich architectural detail on the stadium, window detail on skyline buildings\
"""


def build_stadium_prompt(team: TeamData) -> str:
    return f"""Generate a single isolated stadium illustration for a collectible sports card.
The provided reference image shows the exact illustration style to match.

{_STYLE_ANCHOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STADIUM ASSET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STADIUM: {team.uptowns_stadium_prompt}
NAME: "{team.stadium_name}" clearly lettered on the facade in the same sign/typography style as the reference
LOGO: {team.logo_prompt} displayed prominently on the facade panels
BASE: oval platform base — same dark gray elliptical base as in the reference — with trees, shrubs, and landscaping at ground level

COMPOSITION:
• Stadium perfectly centered horizontally and vertically
• Stadium fills ~85% of frame width — equal ~7% margin on all four sides
• Front-facing view — symmetrical, facing the viewer directly
• No players, no skyline, no sky behind the stadium — only the stadium on green

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Background: pure flat white (#FFFFFF), full bleed to all edges
• Every pixel outside the stadium illustration is solid white — no gradients, no shadows cast onto the background
• Landscape 4:3 format"""


def build_background_prompt(team: TeamData) -> str:
    """
    Background plate: floating island composition (stadium + skyline + sky) on chroma green.
    Same organic floating shape as the reference sticker — no players, no die-cut.
    Chroma green background for clean manual keying in Photoshop — any sky color works.
    """
    return f"""Generate a background plate illustration for a collectible sports card, using the provided reference image as the exact composition and style guide.

{_STYLE_ANCHOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS LAYOUT — TOP TO BOTTOM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Background: pure chroma green (#00FF00) everywhere outside the drawn elements.

The canvas is divided into TWO zones from top to bottom:

The canvas is a SANDWICH — three horizontal layers, like a sandwich with two red slices of bread and the island filling in the middle:

TOP BREAD — solid red (#FF0000), top 28% of canvas height, full width edge to edge. Nothing enters this zone.

FILLING — the floating stadium island, middle 62% of canvas height. Left: ~1% green. Right: ~1% green. The island is centered in this middle zone. Every element — clouds, buildings, flags, trees — must stay strictly inside the filling zone. Nothing touches the top bread or the bottom bread.

BOTTOM BREAD — solid red (#FF0000), bottom 10% of canvas height, full width edge to edge. Nothing enters this zone.

The island is physically trapped between two red bands. It cannot escape upward or downward. The red bands are solid, flat, featureless red — no content, no gradients, just flat #FF0000.

No players. No die-cut border. Wide landscape 16:9 format.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFERENCE GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COPY from the reference exactly:
• The floating island composition — the entire scene (platform + stadium + skyline + sky) sits as one organic floating shape inside the chroma green canvas
• The wide dark oval platform base at the bottom with trees and landscaping
• The stadium sitting large and dominant on the platform, front-facing
• The city skyline and sky visible only inside the organic shape — NOT bleeding to the canvas corners

CHANGE from the reference:
• No players — only stadium, platform, skyline, and sky
• Team content as specified below

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SILHOUETTE — ORGANIC AND ASYMMETRIC (never a dome)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The top silhouette of the floating island must look like a natural skyline or mountain range — irregular, varied, and ASYMMETRIC. It must NEVER resemble a dome, arch, oval, or any smooth symmetric curve.

Three rules that guarantee no dome:
1. The single highest point of the composition is positioned to ONE SIDE (left or right of center) — NOT at the center
2. The left and right edges of the composition reach noticeably DIFFERENT heights from each other
3. At least 3 distinct peaks (cloud formations, building tips, or landmark spires) appear at clearly different heights across the width — like a rugged mountain ridge, never a smooth hill

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPOSITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PERSPECTIVE: Standing close to the stadium entrance — ground level, intimate. The stadium fills most of the frame. Not a distant aerial view.

PLATFORM: Wide dark oval base. Spans ~80% of the canvas width (not edge-to-edge — green is visible on both sides). Sits near the bottom with ~8% green below it.

STADIUM:
• {team.uptowns_stadium_prompt}
• "{team.stadium_name}" clearly lettered on the EXTERIOR facade wall — large visible signage on the outside of the building, never on glass, never inside
• {team.logo_prompt} prominently on the facade panels
• Large and dominant — fills ~78% of the canvas width, front-facing and symmetrical
• Facade details, signage, and architecture clearly visible

SKYLINE:
• {team.uptowns_skyline_prompt}
• BARELY VISIBLE — only the very tips of the tallest 2–3 landmarks peek just slightly above the stadium roofline. Most buildings are completely hidden behind the stadium. The skyline is a subtle background hint, NOT a prominent feature. It adds depth but does not rise high.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREMIUM DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERIOR: Stadium seats packed with supporters (people) in team colors, large jumbotron showing team logo, sponsor banners on interior walls, field with end zone logo visible, floodlights glowing. The interior bowl is visible looking through the open stadium entrance from this ground-level front angle.
FACADE: Sponsor banners and advertisement panels alongside team logos, window glass reflections, structural beams and surface textures
PLATFORM: 3–5 human supporters (people wearing team jerseys, holding team flags) near the entrance — small celebratory figures, clearly human. Flag poles with team flags flying. Trees, shrubs, and light poles at the base. NO mechanical objects, NO ventilators, NO electric fans, NO equipment of any kind on the platform.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOUDS & TOP SILHOUETTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOOK AT THE REFERENCE IMAGE — copy the cloud style and placement exactly:
• Soft white and light grey volumetric clouds sit just above the stadium roofline and skyline tips — exactly as in the reference
• The clouds define the organic top silhouette of the floating island — they are the top edge of the island shape
• Above and around the clouds is pure chroma green (#00FF00) — NO sky color, NO blue, NO gradient. The background outside the island is always pure green.
• The clouds are COMPACT and LOW — they sit just slightly above the skyline, not towering. A thin band of clouds creates the organic irregular top edge. Clouds must NOT grow tall.
• The highest cloud peak must stay well within Zone 3 — clouds must NEVER enter Zone 2 (the gap) or Zone 1 (the marquee). Hard stop at the Zone 3 top boundary.
• Clouds at varied heights across the width — never a smooth arch or dome.
• NO sky visible inside the composition — only clouds, stadium, skyline, and platform."""


def build_scene_prompt(team: TeamData) -> str:
    sky = (team.uptowns_sky_prompt
           or f"Sky in team colors {team.primary_hex} to {team.secondary_hex}, atmospheric")
    return f"""Generate a wide panoramic city skyline background illustration for a collectible sports card.
The provided reference image shows the exact illustration style to match — look at the city buildings visible behind the stadium.

{_STYLE_ANCHOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCENE ASSET — SKY + CITY SKYLINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CITY: {team.uptowns_skyline_prompt}
SKY: {sky}

COMPOSITION:
• Wide panoramic view — the skyline spans the full width of the frame
• Sky and clouds fill the upper ~55% of the image
• City buildings fill the lower ~45%, touching the very bottom edge
• No platform, no stadium, no players — pure city + sky background
• Content reaches all four edges — full bleed, no margins

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• This is a full background — NO chroma green, content fills edge to edge
• Wide landscape 16:9 format"""


# ── Player helpers ─────────────────────────────────────────────────────────────

def _player_facing(side: str) -> str:
    """side='left' → player on left side of card → faces RIGHT toward center."""
    if side == "left":
        return "body and gaze directed to the RIGHT — the player moves and looks toward viewer's right"
    return "body and gaze directed to the LEFT — the player moves and looks toward viewer's left"


def _player_pose(position: str, side: str, pose: str) -> str:
    direction = "right" if side == "left" else "left"
    pos = position.lower()

    if pose == "auto":
        if pos == "qb":                             pose = "throwing"
        elif pos == "rb":                           pose = "rushing"
        elif pos == "wr":                           pose = "route"
        elif pos == "te":                           pose = "rushing"
        elif pos in ("de", "dl", "edge", "olb"):   pose = "speed_rush"
        elif pos == "dt":                           pose = "bull_rush"
        elif pos == "lb":                           pose = "linebacker"
        elif pos in ("cb", "db", "s", "fs", "ss"): pose = "coverage"
        elif pos == "k":                            pose = "kicking"
        else:                                       pose = "athletic"

    descriptions = {
        # ── Offense ───────────────────────────────────────────────────────────
        "throwing":      f"classic QB mid-throw release toward the {direction} — plant foot firmly grounded, hips fully rotated, throwing arm fully extended releasing a tight spiral, non-throwing hand following through naturally, full weight transfer, intense focused eyes downfield",
        "scrambling":    f"QB scrambling at speed toward the {direction} — football tucked under arm, eyes scanning downfield while running, athletic improvisation, body leaning into the run",
        "rushing":       f"explosive full-speed run toward the {direction} — football tucked tight under inside arm, opposite arm driving forward for balance, body leaning aggressively, full stride extension, drive leg pushing powerfully off the ground",
        "route":         f"sharp route-running stride toward the {direction} — no ball, pure speed and athleticism, arms pumping naturally, leaning into the cut, explosive WR acceleration off the break — this is a route runner in full flight, no football",
        "jump_catch":    f"full-extension jump catch toward the {direction} — both arms fully extended overhead at peak of jump, gloved hands reaching for football at fingertips, body fully airborne, eyes locked on the ball, toes pointing down",
        "catching":      f"hands catch toward the {direction} — arms extended forward at chest level, gloved hands cupped together receiving the ball, eyes tracking the football, feet planted, body square to the throw",
        "stiff_arm":     f"powerful stiff-arm toward the {direction} — one arm fully extended straight out as a stiff-arm block, other arm securing the football, body driving forward, aggressive dominant energy",
        "hurdle":        f"explosive hurdle toward the {direction} — one knee driven high, body fully airborne clearing a defender, football secured, face forward and determined",
        # ── Defense ───────────────────────────────────────────────────────────
        "speed_rush":    f"elite speed rush off the edge toward the {direction} — explosive first step, hips low and driving, one arm swiping to beat the block, full acceleration off the line, no ball",
        "bull_rush":     f"devastating bull rush toward the {direction} — both hands driving into the blocker, legs churning powerfully, pad level low, full body power engaged, no ball",
        "pass_rush":     f"explosive pass rush burst toward the {direction} — arms raised and driving, powerful low leverage, maximum first-step acceleration, no ball",
        "linebacker":    f"instinctive linebacker read-and-react toward the {direction} — aggressive forward lean, arms wide and ready to shed, eyes reading the backfield, explosive pre-snap energy, no ball",
        "coverage":      f"elite DB backpedal in man coverage toward the {direction} — hips low, head turned tracking the route, arms out for positioning, explosive defensive back footwork, no ball",
        "press_coverage": f"physical press coverage stance toward the {direction} — hands up and ready to jam at the line, aggressive body position, eyes locked on the receiver, no ball",
        # ── Special ───────────────────────────────────────────────────────────
        "kicking":       f"powerful kick follow-through toward the {direction} — plant foot fully grounded, kicking leg fully extended at maximum height, arms out for balance, eyes following the ball",
        "celebration":   f"celebratory pose toward the {direction} — dynamic, expressive, high-energy football celebration — arms raised, chest out, pure joy and confidence",
        "athletic":      f"explosive athletic action stance toward the {direction} — dynamic power, full energy, premium sports card presence",
    }
    return descriptions.get(pose, descriptions["athletic"])


def _player_ball(position: str, pose: str, ball: str) -> str:
    if ball == "auto":
        if pose in ("throwing", "scrambling"):          ball = "yes"
        elif pose in ("rushing", "stiff_arm", "hurdle"): ball = "yes"
        elif pose in ("catching", "jump_catch"):         ball = "catching"
        else:                                            ball = "no"

    if ball in ("true", "yes"):
        pos = position.lower()
        if pos == "qb":
            return "football firmly gripped in throwing hand — brown leather, white laces clearly visible, classic QB ball grip"
        else:
            return "football tucked securely under arm — brown leather, white laces visible, tight secure carry"
    elif ball in ("catching",):
        return "football arriving at the player's hands — ball clearly visible, laces showing, at the moment of catch, fingertips making contact"
    return "NO football anywhere in the image — hands completely free, arms naturally positioned for the pose"


def _player_visor(visor: str) -> str:
    if visor == "tinted":
        return "dark tinted reflective visor — a dark shield covering the full face opening, eyes and upper face obscured, modern aggressive look"
    elif visor == "none" or visor == "open":
        return "ABSOLUTELY NO VISOR — zero plastic shield on the helmet, the face opening is completely bare, only the metal face mask bars visible, full face and eyes 100% exposed"


def build_player_prompt(
    team: TeamData,
    name: str,
    number: str,
    position: str,
    side: str,          # "left" (faces right) | "right" (faces left)
    pose: str = "auto",
    ball: str = "auto",
    visor: str = "open",
) -> str:
    facing   = _player_facing(side)
    pose_str = _player_pose(position, side, pose)
    ball_str = _player_ball(position, pose if pose != "auto" else position, ball)
    visor_str = _player_visor(visor)

    return f"""Generate a single isolated NFL player illustration for a premium collectible sports card.

The provided reference image IS the exact style guide — match its illustration quality precisely:
bold ink outlines, smooth cel-shaded colors with clean highlight gradients, premium sports card art, highly detailed musculature and uniform.
The reference player faces the SAME direction your player should face — match it exactly.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEAM:   {team.name}
JERSEY: {team.jersey_prompt}
HELMET: {team.helmet_prompt}
PANTS:  {team.pants_prompt}
NUMBER: #{number} in {team.number_style} — large and clearly legible on chest

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POSE & ACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACING: {facing}
POSE:   {pose_str}
BALL:   {ball_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACE — CRITICAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• {visor_str}
• Full face clearly visible — eyes, nose, mouth, skin texture all rendered in high detail
• Determined, intense athletic expression
• Face is the single most detailed part of the illustration — premium portrait quality

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HANDS & ANATOMY — CRITICAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Hands are wearing football gloves — gloves fit tight to the hand, clearly textured
• Fingers are naturally positioned for the pose — closed/gripping when holding the ball, bent naturally when pumping arm
• NEVER splayed fingers, NEVER jazz hands, NEVER outstretched open palms unless catching
• Hand anatomy is correct — proper proportions, no distortion, no extra fingers
• All four limbs fully drawn — no missing arms or legs, no phantom limbs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BODY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Full body — top of helmet to bottom of cleats, ZERO cropping of any body part
• Both feet and cleats fully on screen at the bottom of frame
• Athletic body proportions — muscular, dynamic, powerful — same as the reference
• Uniform details: jersey tucked in, pants fit correctly, sleeves rendered accurately
• Player fills ~85% of frame height — centered horizontally with equal green margin on all sides

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Background: pure flat chroma green (#00FF00), full bleed to all edges
• NOTHING outside the player — no ground shadow, no floor, no gradient, no vignette
• Every single pixel outside the player silhouette is solid #00FF00
• Portrait 3:4 format"""
