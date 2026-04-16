import type { TeamData } from "./types";

const STYLE_ANCHOR = `Match the exact illustration style visible in the provided reference image:
• Semi-realistic sports card illustration — NOT flat cartoon
• Bold consistent ink outlines with even line weight throughout
• Multi-value shading — visible light, midtone, and shadow on every surface
• Detailed fabric texture on jerseys, 3D volumetric helmet with reflective sheen
• Rich architectural detail on the stadium, window detail on skyline buildings`;

function playerFacing(side: "left" | "right"): string {
  return side === "left"
    ? "body and gaze directed to the RIGHT — the player moves and looks toward viewer's right"
    : "body and gaze directed to the LEFT — the player moves and looks toward viewer's left";
}

function playerPose(position: string, side: "left" | "right", pose: string): string {
  const direction = side === "left" ? "right" : "left";
  const pos = position.toLowerCase();

  if (pose === "auto") {
    if (pos === "qb")                              pose = "throwing";
    else if (pos === "rb")                         pose = "rushing";
    else if (pos === "wr")                         pose = "route";
    else if (pos === "te")                         pose = "rushing";
    else if (["de", "dl", "edge", "olb"].includes(pos)) pose = "speed_rush";
    else if (pos === "dt")                         pose = "bull_rush";
    else if (pos === "lb")                         pose = "linebacker";
    else if (["cb", "db", "s", "fs", "ss"].includes(pos)) pose = "coverage";
    else if (pos === "k")                          pose = "kicking";
    else                                           pose = "athletic";
  }

  const descriptions: Record<string, string> = {
    throwing:      `classic QB mid-throw release toward the ${direction} — plant foot firmly grounded, hips fully rotated, throwing arm fully extended releasing a tight spiral, non-throwing hand following through naturally, full weight transfer, intense focused eyes downfield`,
    scrambling:    `QB scrambling at speed toward the ${direction} — football tucked under arm, eyes scanning downfield while running, athletic improvisation, body leaning into the run`,
    rushing:       `explosive full-speed run toward the ${direction} — football tucked tight under inside arm, opposite arm driving forward for balance, body leaning aggressively, full stride extension, drive leg pushing powerfully off the ground`,
    route:         `sharp route-running stride toward the ${direction} — no ball, pure speed and athleticism, arms pumping naturally, leaning into the cut, explosive WR acceleration off the break — this is a route runner in full flight, no football`,
    jump_catch:    `full-extension jump catch toward the ${direction} — both arms fully extended overhead at peak of jump, gloved hands reaching for football at fingertips, body fully airborne, eyes locked on the ball, toes pointing down`,
    catching:      `hands catch toward the ${direction} — arms extended forward at chest level, gloved hands cupped together receiving the ball, eyes tracking the football, feet planted, body square to the throw`,
    stiff_arm:     `powerful stiff-arm toward the ${direction} — one arm fully extended straight out as a stiff-arm block, other arm securing the football, body driving forward, aggressive dominant energy`,
    hurdle:        `explosive hurdle toward the ${direction} — one knee driven high, body fully airborne clearing a defender, football secured, face forward and determined`,
    speed_rush:    `elite speed rush off the edge toward the ${direction} — explosive first step, hips low and driving, one arm swiping to beat the block, full acceleration off the line, no ball`,
    bull_rush:     `devastating bull rush toward the ${direction} — both hands driving into the blocker, legs churning powerfully, pad level low, full body power engaged, no ball`,
    pass_rush:     `explosive pass rush burst toward the ${direction} — arms raised and driving, powerful low leverage, maximum first-step acceleration, no ball`,
    linebacker:    `instinctive linebacker read-and-react toward the ${direction} — aggressive forward lean, arms wide and ready to shed, eyes reading the backfield, explosive pre-snap energy, no ball`,
    coverage:      `elite DB backpedal in man coverage toward the ${direction} — hips low, head turned tracking the route, arms out for positioning, explosive defensive back footwork, no ball`,
    press_coverage:`physical press coverage stance toward the ${direction} — hands up and ready to jam at the line, aggressive body position, eyes locked on the receiver, no ball`,
    kicking:       `powerful kick follow-through toward the ${direction} — plant foot fully grounded, kicking leg fully extended at maximum height, arms out for balance, eyes following the ball`,
    celebration:   `celebratory pose toward the ${direction} — dynamic, expressive, high-energy football celebration — arms raised, chest out, pure joy and confidence`,
    athletic:      `explosive athletic action stance toward the ${direction} — dynamic power, full energy, premium sports card presence`,
  };

  return descriptions[pose] ?? descriptions.athletic;
}

function playerBall(position: string, pose: string, ball: string): string {
  if (ball === "auto") {
    if (["throwing", "scrambling"].includes(pose))       ball = "yes";
    else if (["rushing", "stiff_arm", "hurdle"].includes(pose)) ball = "yes";
    else if (["catching", "jump_catch"].includes(pose))  ball = "catching";
    else                                                 ball = "no";
  }

  if (ball === "true" || ball === "yes") {
    return position.toLowerCase() === "qb"
      ? "football firmly gripped in throwing hand — brown leather, white laces clearly visible, classic QB ball grip"
      : "football tucked securely under arm — brown leather, white laces visible, tight secure carry";
  }
  if (ball === "catching") {
    return "football arriving at the player's hands — ball clearly visible, laces showing, at the moment of catch, fingertips making contact";
  }
  return "NO football anywhere in the image — hands completely free, arms naturally positioned for the pose";
}

function playerVisor(visor: string): string {
  if (visor === "tinted") {
    return "dark tinted reflective visor — a dark shield covering the full face opening, eyes and upper face obscured, modern aggressive look";
  }
  return "ABSOLUTELY NO VISOR — zero plastic shield on the helmet, the face opening is completely bare, only the metal face mask bars visible, full face and eyes 100% exposed";
}

export function buildPlayerPrompt(
  team: TeamData,
  name: string,
  number: string,
  position: string,
  side: "left" | "right",
  pose = "auto",
  ball = "auto",
  visor = "open",
): string {
  const facing   = playerFacing(side);
  const poseStr  = playerPose(position, side, pose);
  const ballStr  = playerBall(position, pose !== "auto" ? pose : position, ball);
  const visorStr = playerVisor(visor);

  return `Generate a single isolated NFL player illustration for a premium collectible sports card.

The provided reference image IS the exact style guide — match its illustration quality precisely:
bold ink outlines, smooth cel-shaded colors with clean highlight gradients, premium sports card art, highly detailed musculature and uniform.
The reference player faces the SAME direction your player should face — match it exactly.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PLAYER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEAM:   ${team.name}
JERSEY: ${team.jerseyPrompt}
HELMET: ${team.helmetPrompt}
PANTS:  ${team.pantsPrompt}
NUMBER: #${number} in ${team.numberStyle} — large and clearly legible on chest

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POSE & ACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACING: ${facing}
POSE:   ${poseStr}
BALL:   ${ballStr}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FACE — CRITICAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• ${visorStr}
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
• Portrait 3:4 format`;
}

export function buildBackgroundPrompt(team: TeamData): string {
  return `Generate a background plate illustration for a collectible sports card, using the provided reference image as the exact composition and style guide.

${STYLE_ANCHOR}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CANVAS LAYOUT — TOP TO BOTTOM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Background: pure chroma green (#00FF00) everywhere outside the drawn elements.

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
• ${team.uptownsStadiumPrompt}
• "${team.stadiumName}" clearly lettered on the EXTERIOR facade wall — large visible signage on the outside of the building, never on glass, never inside
• ${team.logoPrompt} prominently on the facade panels
• Large and dominant — fills ~78% of the canvas width, front-facing and symmetrical
• Facade details, signage, and architecture clearly visible

SKYLINE:
• ${team.uptownsSkylinePrompt}
• BARELY VISIBLE — only the very tips of the tallest 2–3 landmarks peek just slightly above the stadium roofline. Most buildings are completely hidden behind the stadium. The skyline is a subtle background hint, NOT a prominent feature. It adds depth but does not rise high.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREMIUM DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INTERIOR: Stadium seats packed with supporters in team colors, large jumbotron showing team logo, sponsor banners on interior walls, field with end zone logo visible, floodlights glowing.
FACADE: Sponsor banners and advertisement panels alongside team logos, window glass reflections, structural beams and surface textures
PLATFORM: 3–5 human supporters (people wearing team jerseys, holding team flags) near the entrance — small celebratory figures. Flag poles with team flags flying. Trees, shrubs, and light poles at the base. NO mechanical objects, NO ventilators, NO fans.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOUDS & TOP SILHOUETTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Soft white and light grey volumetric clouds sit just above the stadium roofline — exactly as in the reference
• The clouds define the organic top silhouette of the floating island
• Above and around the clouds is pure chroma green (#00FF00) — NO sky color, NO blue, NO gradient
• Clouds are COMPACT and LOW — a thin band creating the organic irregular top edge
• Clouds at varied heights across the width — never a smooth arch or dome`;
}
