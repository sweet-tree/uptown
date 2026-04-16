"use server";

import { prisma } from "@/lib/db";
import type { TeamWithPlayers } from "@/lib/types";

export async function getSports() {
  return prisma.sport.findMany({
    where: { active: true },
    orderBy: { name: "asc" },
  });
}

export async function getTeams(sportSlug: string): Promise<TeamWithPlayers[]> {
  return prisma.team.findMany({
    where: { sport: { slug: sportSlug.toLowerCase() }, active: true },
    include: {
      cardPlayers: { orderBy: { order: "asc" } },
      rosterEntries: { orderBy: { sortOrder: "asc" } },
      sport: true,
    },
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
    include: {
      cardPlayers: { orderBy: { order: "asc" } },
      rosterEntries: { orderBy: { sortOrder: "asc" } },
      sport: true,
    },
  });
  if (!team) throw new Error(`Team not found: ${abbreviation} (${sportSlug})`);
  return team as TeamWithPlayers;
}
