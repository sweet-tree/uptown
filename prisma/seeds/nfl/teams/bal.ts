import type { TeamSeed } from "../../types";

export const BAL: TeamSeed = {
  abbreviation: "BAL",
  name: "Baltimore Ravens",
  city: "Baltimore",
  primaryHex: "#241773",
  secondaryHex: "#9E7C0C",
  stadiumName: "M&T Bank Stadium",
  stadiumPrompt: "M&T Bank Stadium illustrated front-facing — brick and steel exterior with arched windows, dark purple and gold banners on the facade, Ravens shield logos on the building panels, trees and landscaping at the base",
  skylinePrompt: "Baltimore skyline: the tall cylindrical Baltimore World Trade Center tower centered (tallest, distinctive rounded top), flanked by shorter rectangular downtown office buildings stepping down at varying heights on both sides, Inner Harbor waterfront at the base",
  skyPrompt: "Rich purple and gold dusk sky over Baltimore — deep royal purple at the top fading to warm amber and gold near the horizon from the Inner Harbor glow below. Dramatic volumetric clouds at dramatically varied heights: a tall billowing formation high on the left, the Baltimore World Trade Center's distinctive cylindrical top piercing through lower clouds at center, and a wide lower cloud bank on the right — each at a different height, creating a richly irregular silhouette. Deep purple sky visible in gaps between formations. Cinematic, premium, Ravens colors throughout.",
  jerseyPrompt: "deep purple NFL jersey — 'RAVENS' in white block letters across chest, white block numbers with thick black outline on chest and back, white shoulder stripes, purple sleeves with black and gold trim bands",
  pantsPrompt: "black NFL pants with purple and gold side stripes",
  helmetPrompt: "glossy purple helmet, face fully visible through open visor — Ravens shield logo on both sides (black raven head on purple and gold shield with letter B), black face mask, thin gold center stripe",
  numberStyle: "large white block numerals with thick black outline, collegiate style",
  logoPrompt: "Ravens shield: black raven head facing left, purple and gold shield, bold letter B, gold trim border",
  cardPlayers: [
    { name: "Lamar Jackson", number: "8",  position: "qb", side: "left",  pose: "throwing", ball: "yes", order: 0 },
    { name: "Derrick Henry", number: "22", position: "rb", side: "right", pose: "rushing",  ball: "yes", order: 1 },
  ],
};
