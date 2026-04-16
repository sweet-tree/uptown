export type Sport = "nfl" | "soccer" | "hockey" | "baseball";

export interface RosterPlayer {
  name: string;
  number: string;
  position: string;
}

export interface PlayerSpec {
  name: string;
  number: string;
  position: string;
  side: "left" | "right";
  pose?: string;
  ball?: string;
}

export interface TeamData {
  name: string;
  city: string;
  abbreviation: string;
  sport: Sport;
  primaryHex: string;
  secondaryHex: string;
  stadiumName: string;
  uptownsStadiumPrompt: string;
  uptownsSkylinePrompt: string;
  uptownsSkyPrompt: string;
  jerseyPrompt: string;
  pantsPrompt: string;
  helmetPrompt: string;
  numberStyle: string;
  logoPrompt: string;
  cardPlayers: PlayerSpec[];
  roster: Record<string, RosterPlayer>;
}

export type GenerateType = "background" | "player";
export type ModelTier = "flash" | "pro";

/** Dashboard copy for each tier — keep aligned with `MODELS` in `src/lib/gemini.ts`. */
export const MODEL_TIER_DISPLAY: Record<ModelTier, string> = {
  flash: "3.1 Flash",
  pro: "3 Pro",
};

export interface GeneratePlayerRequest {
  team: string;
  side: "left" | "right";
  player?: string;
  number?: string;
  pose?: string;
  ball?: string;
  model?: ModelTier;
}

export interface GenerateBackgroundRequest {
  team: string;
  model?: ModelTier;
}

export interface GenerateResponse {
  ok: boolean;
  path?: string;
  dataUrl?: string;
  error?: string;
}

// ── DB model shapes ──────────────────────────────────────────────────────────
import type { Team, CardPlayer, Sport as SportModel, RosterEntry } from "../generated/prisma/client";

export type TeamWithPlayers = Team & {
  cardPlayers: CardPlayer[];
  rosterEntries: RosterEntry[];
  sport: SportModel;
};
