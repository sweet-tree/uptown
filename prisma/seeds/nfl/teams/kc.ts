import type { TeamSeed } from "../../types";

export const KC: TeamSeed = {
  abbreviation: "KC",
  name: "Kansas City Chiefs",
  city: "Kansas City",
  primaryHex: "#E31837",
  secondaryHex: "#FFB81C",
  stadiumName: "GEHA Field at Arrowhead Stadium",
  stadiumPrompt: "Arrowhead Stadium illustrated front-facing — distinctive arrowhead-shaped roofline, red brick exterior, Chiefs arrowhead logos on the facade panels, trees and parking lot surrounding",
  skylinePrompt: "Kansas City skyline: the Liberty Memorial obelisk tower (tall, slender stone needle) dominates center as the tallest landmark, flanked by downtown office towers of varying heights — some tall glass buildings, some shorter brick — Missouri River glimpsed at the base",
  skyPrompt: "Vivid amber and crimson Chiefs sunset sky — deep red-orange at the horizon fading to rich gold above. Dramatic volumetric clouds at dramatically varied heights: a towering golden cloud pillar rising very high on the left, the Liberty Memorial obelisk needle piercing sharply upward at center-left through a lower cloud bank, a wide mid-height cloud formation at center-right, and a smaller scattered group low on the right — each formation at a distinctly different height. Warm cinematic golden-hour light illuminates the cloud bases from below. Rich, saturated, premium Chiefs red and gold throughout.",
  jerseyPrompt: "red NFL jersey — 'CHIEFS' in white block letters across chest, white block numbers with red outline on chest and back, white shoulder panels, red sleeves with white and gold trim bands",
  pantsPrompt: "white NFL pants with red and gold side stripes",
  helmetPrompt: "red helmet, face fully visible through open visor — Chiefs arrowhead logo on both sides (solid red arrowhead with white outline), white face mask, no center stripe",
  numberStyle: "large white block numerals with red outline",
  logoPrompt: "Chiefs arrowhead: solid red arrowhead pointing right, white outline, bold clean design",
  cardPlayers: [
    { name: "Patrick Mahomes", number: "15", position: "qb", side: "left",  pose: "throwing", ball: "yes", order: 0 },
    { name: "Travis Kelce",    number: "87", position: "te", side: "right", pose: "rushing",  ball: "yes", order: 1 },
  ],
};
