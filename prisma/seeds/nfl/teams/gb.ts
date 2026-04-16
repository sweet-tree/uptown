import type { TeamSeed } from "../../types";

export const GB: TeamSeed = {
  abbreviation: "GB",
  name: "Green Bay Packers",
  city: "Green Bay",
  primaryHex: "#203731",
  secondaryHex: "#FFB612",
  stadiumName: "Lambeau Field",
  stadiumPrompt: "Lambeau Field illustrated front-facing — classic circular open-air bowl stadium, dark green and gold exterior, large Packers G logos on the facade panels, snow on the ground, pine trees surrounding the base. The stadium bowl is open at the front — you can see inside the seating bowl, the packed crowd in green and gold, and the field from this front angle.",
  skylinePrompt: "Green Bay winter scene: tall pointed pine trees of dramatically varying heights rise above the stadium — some very tall and narrow, others medium, others short — with snow-covered rooftops of low buildings visible between the trees",
  skyPrompt: "Crisp Wisconsin winter sky — deep steel grey-blue at the top with warm amber stadium glow rising from below. Dramatic grey-white cloud formations at dramatically varied heights: a tall billowing cloud tower rising high on the left, a very tall snow-dusted pine tree spiking sharply at center-left piercing through a low cloud, a wide mid-height cloud bank at center with another tall pine visible through it, and more pine tips at varying heights on the right — each pine and cloud at a distinctly different height. Cold winter air, light snowfall visible. Packers gold warmth glowing from the stadium lights below the clouds.",
  jerseyPrompt: "dark forest green NFL jersey — 'PACKERS' in gold block letters across chest, gold block numbers with white outline on chest and back, gold shoulder panels, green sleeves with gold and white trim bands",
  pantsPrompt: "gold NFL pants with green and white side stripes",
  helmetPrompt: "matte gold helmet, face fully visible through open visor — Packers G logo on both sides (dark green oval with large white letter G centered), white face mask, no center stripe",
  numberStyle: "large gold block numerals with white outline",
  logoPrompt: "Packers G: dark green oval, large white letter G centered, clean bold design",
  cardPlayers: [
    { name: "Jordan Love", number: "10", position: "qb", side: "left",  pose: "throwing", ball: "yes", order: 0 },
    { name: "Jayden Reed", number: "11", position: "wr", side: "right", pose: "route",    ball: "no",  order: 1 },
  ],
};
