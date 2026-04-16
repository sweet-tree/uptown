export interface TeamSeed {
  abbreviation: string;
  name: string;
  city: string;
  primaryHex: string;
  secondaryHex: string;
  stadiumName: string;
  stadiumPrompt: string;
  skylinePrompt: string;
  skyPrompt: string;
  jerseyPrompt: string;
  pantsPrompt: string;
  helmetPrompt: string;
  numberStyle: string;
  logoPrompt: string;
  cardPlayers: CardPlayerSeed[];
}

export interface CardPlayerSeed {
  name: string;
  number: string;
  position: string;
  side: "left" | "right";
  pose?: string;
  ball?: string;
  order?: number;
}
