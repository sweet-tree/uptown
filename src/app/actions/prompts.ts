"use server";

import { prisma } from "@/lib/db";
import { buildPlayerPrompt, buildBackgroundPrompt } from "@/lib/prompt-engine";
import { getTeamByAbbr } from "./teams";


export interface PromptResult {
  text: string;
  isCustom: boolean;
}

export interface GenerationInput {
  team: string;
  type: "player" | "background";
  side?: string;
  playerName?: string;
  number?: string;
  pose?: string;
  model: string;
  imagePath: string;
}

// ── Prompt CRUD ────────────────────────────────────────────────────────────────

export async function getPrompt(key: string): Promise<PromptResult> {
  const stored = await prisma.prompt.findUnique({ where: { key } });
  if (stored) return { text: stored.text, isCustom: true };

  const [type, teamAbbr, side] = key.split(":");
  const team = await getTeamByAbbr(teamAbbr);

  let text: string;
  if (type === "background") {
    text = buildBackgroundPrompt(team);
  } else {
    const spec = side
      ? team.cardPlayers.find((p) => p.side === side)
      : team.cardPlayers[0];
    text = buildPlayerPrompt(
      team,
      spec?.name ?? "Player",
      spec?.number ?? "0",
      spec?.position ?? "qb",
      (side ?? "left") as "left" | "right",
      spec?.pose ?? "auto",
      spec?.ball ?? "auto",
    );
  }

  return { text, isCustom: false };
}

export async function setPrompt(key: string, text: string): Promise<void> {
  await prisma.prompt.upsert({
    where: { key },
    update: { text },
    create: { key, text },
  });
}

export async function deletePrompt(key: string): Promise<void> {
  await prisma.prompt.deleteMany({ where: { key } });
}

// ── Generation history ─────────────────────────────────────────────────────────

export async function saveGeneration(data: GenerationInput): Promise<void> {
  await prisma.generation.create({ data });
}

export async function getGenerations(team: string) {
  return prisma.generation.findMany({
    where: { team: team.toUpperCase() },
    orderBy: { createdAt: "desc" },
    take: 50,
  });
}

export async function getAllGenerations() {
  return prisma.generation.findMany({
    orderBy: { createdAt: "desc" },
    take: 100,
  });
}

