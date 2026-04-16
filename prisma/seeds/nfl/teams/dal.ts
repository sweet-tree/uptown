import type { TeamSeed } from "../../types";

export const DAL: TeamSeed = {
  abbreviation: "DAL",
  name: "Dallas Cowboys",
  city: "Dallas",
  primaryHex: "#003594",
  secondaryHex: "#869397",
  stadiumName: "AT&T Stadium",
  stadiumPrompt: "AT&T Stadium illustrated front-facing — massive domed silver roof, Cowboys star centered on the facade, glass and steel exterior, Cowboys helmet logos on the building panels",
  skylinePrompt: "Dallas skyline: Reunion Tower with its distinctive spherical globe top is the most recognizable landmark (mid-height, iconic shape), flanked by tall glass skyscrapers including the Bank of America Plaza and Renaissance Tower at varying heights, deep indigo sky",
  skyPrompt: "Vivid Texas noon sky — deep Cowboys navy-blue at the top fading to bright cerulean and warm gold at the horizon. Large dramatic white cumulus clouds at dramatically varied heights: a massive towering cloud column rising very high on the right with Reunion Tower's globe visible just beside it, a wide mid-height cloud bank at center, and lower scattered clouds on the left with Dallas skyline towers poking through at varying heights. Bright, vivid, cinematic Texas sunshine — warm golden light on every cloud surface. Bold contrast, premium collector card atmosphere.",
  jerseyPrompt: "white home NFL jersey — 'COWBOYS' in navy blue block letters across chest, navy blue numbers with silver metallic outline on chest and back, blue shoulder stripe panels, white sleeves with navy trim",
  pantsPrompt: "silver metallic NFL pants with navy and white side stripes",
  helmetPrompt: "high-gloss silver metallic helmet, face fully visible through open visor — iconic blue five-pointed star centered on both sides, blue face mask, no center stripe",
  numberStyle: "large white block numerals with silver metallic outline",
  logoPrompt: "Cowboys star: large blue five-pointed star, white outline, centered on silver helmet panel",
  cardPlayers: [
    { name: "Dak Prescott", number: "4",  position: "qb", side: "left",  pose: "throwing", ball: "yes", order: 0 },
    { name: "CeeDee Lamb",  number: "88", position: "wr", side: "right", pose: "route",    ball: "no",  order: 1 },
  ],
};
