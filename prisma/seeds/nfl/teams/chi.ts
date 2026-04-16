import type { TeamSeed } from "../../types";

export const CHI: TeamSeed = {
  abbreviation: "CHI",
  name: "Chicago Bears",
  city: "Chicago",
  primaryHex: "#0B162A",
  secondaryHex: "#C83803",
  stadiumName: "Soldier Field",
  stadiumPrompt: "Soldier Field illustrated front-facing — iconic neoclassical stone columns flanking both sides of the modern bowl, Bears C logos on the facade panels, Lake Michigan visible behind",
  skylinePrompt: "Chicago skyline: Willis Tower (Sears Tower) dominates center-left — tallest building with two slim antenna towers at the top. John Hancock Center with distinctive X-bracing stands to the right at second height. Shorter skyscrapers at many varying heights fill the rest. Lake Michigan shoreline at the base.",
  skyPrompt: "Dramatic Chicago dusk sky — deep navy blue at the top fading to vivid burnt orange and amber from the city glow near the horizon. Dramatic clouds at dramatically varied heights: Willis Tower's twin steel antenna tips pierce sharply upward through a low cloud bank at center — the antennas are the absolute highest point, far above everything else. John Hancock's X-braced silhouette clears a wider cloud bank at the right at a distinctly lower height. A tall billowing cloud formation rises high on the left. Navy blue sky visible between formations. Bears navy and orange throughout — cinematic Chicago dusk energy.",
  jerseyPrompt: "navy blue NFL jersey — 'BEARS' in orange block letters across chest, orange block numbers with white outline on chest and back, navy shoulder panels, navy sleeves with orange and white trim bands",
  pantsPrompt: "navy blue NFL pants with orange and white side stripes",
  helmetPrompt: "navy blue helmet, face fully visible through open visor — Bears C logo on both sides (bold orange letter C with navy outline), navy face mask, no center stripe",
  numberStyle: "large orange block numerals with white outline",
  logoPrompt: "Bears C: bold orange letter C, navy outline, classic Chicago Bears design",
  cardPlayers: [
    { name: "Caleb Williams", number: "18", position: "qb", side: "left",  pose: "throwing", ball: "yes", order: 0 },
    { name: "DJ Moore",       number: "2",  position: "wr", side: "right", pose: "route",    ball: "no",  order: 1 },
  ],
};
