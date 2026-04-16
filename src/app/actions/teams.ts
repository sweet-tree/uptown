"use server";

import { prisma } from "@/lib/db";
import type { Team, CardPlayer, Sport } from "../../generated/prisma/client";

export type TeamWithPlayers = Team & { cardPlayers: CardPlayer[]; sport: Sport };

export async function getSports() {
  return prisma.sport.findMany({
    where: { active: true },
    orderBy: { name: "asc" },
  });
}

export async function getTeams(sportSlug: string): Promise<TeamWithPlayers[]> {
  return prisma.team.findMany({
    where: { sport: { slug: sportSlug.toLowerCase() }, active: true },
    include: { cardPlayers: { orderBy: { order: "asc" } }, sport: true },
    orderBy: { name: "asc" },
  }) as Promise<TeamWithPlayers[]>;
}

export async function getTeamByAbbr(
  abbreviation: string,
  sportSlug = "nfl",
): Promise<TeamWithPlayers> {
  const team = await prisma.team.findFirst({
    where: {
      abbreviation: abbreviation.toUpperCase(),
      sport: { slug: sportSlug.toLowerCase() },
    },
    include: { cardPlayers: { orderBy: { order: "asc" } }, sport: true },
  });
  if (!team) throw new Error(`Team not found: ${abbreviation} (${sportSlug})`);
  return team as TeamWithPlayers;
}
