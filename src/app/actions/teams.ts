"use server";

import { getPrisma } from "@/lib/db";
import { requireUser } from "@/lib/require-user";
import type { TeamWithPlayers } from "@/lib/types";

const rosterOrder = [{ name: "asc" as const }, { id: "asc" as const }];

export async function getSports() {
  await requireUser();
  const prisma = getPrisma();
  return prisma.sport.findMany({
    where: { active: true },
    orderBy: { name: "asc" },
  });
}

export async function getTeams(sportSlug: string): Promise<TeamWithPlayers[]> {
  await requireUser();
  const prisma = getPrisma();
  return prisma.team.findMany({
    where: { sport: { slug: sportSlug.toLowerCase() }, active: true },
    include: {
      cardPlayers: { orderBy: { order: "asc" } },
      rosterEntries: { orderBy: rosterOrder },
      sport: true,
    },
    orderBy: { name: "asc" },
  }) as Promise<TeamWithPlayers[]>;
}

export async function getTeamByAbbr(
  abbreviation: string,
  sportSlug = "nfl",
): Promise<TeamWithPlayers> {
  await requireUser();
  const prisma = getPrisma();
  const team = await prisma.team.findFirst({
    where: {
      abbreviation: abbreviation.toUpperCase(),
      sport: { slug: sportSlug.toLowerCase() },
    },
    include: {
      cardPlayers: { orderBy: { order: "asc" } },
      rosterEntries: { orderBy: rosterOrder },
      sport: true,
    },
  });
  if (!team) throw new Error(`Team not found: ${abbreviation} (${sportSlug})`);
  return team as TeamWithPlayers;
}
