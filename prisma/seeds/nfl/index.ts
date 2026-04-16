import type { PrismaClient } from "../../src/generated/prisma/client";
import { BAL } from "./teams/bal";
import { KC }  from "./teams/kc";
import { DAL } from "./teams/dal";
import { GB }  from "./teams/gb";
import { CHI } from "./teams/chi";
import { LV }  from "./teams/lv";
import type { TeamSeed } from "../types";

export const NFL_TEAMS: TeamSeed[] = [BAL, KC, DAL, GB, CHI, LV];

export async function seedNFL(prisma: PrismaClient) {
  const sport = await prisma.sport.upsert({
    where: { slug: "nfl" },
    update: { name: "NFL", active: true },
    create: { slug: "nfl", name: "NFL", active: true },
  });

  for (const t of NFL_TEAMS) {
    const team = await prisma.team.upsert({
      where: { sportId_abbreviation: { sportId: sport.id, abbreviation: t.abbreviation } },
      update: {
        name: t.name, city: t.city,
        primaryHex: t.primaryHex, secondaryHex: t.secondaryHex,
        stadiumName: t.stadiumName,
        stadiumPrompt: t.stadiumPrompt, skylinePrompt: t.skylinePrompt, skyPrompt: t.skyPrompt,
        jerseyPrompt: t.jerseyPrompt, pantsPrompt: t.pantsPrompt, helmetPrompt: t.helmetPrompt,
        numberStyle: t.numberStyle, logoPrompt: t.logoPrompt,
      },
      create: {
        abbreviation: t.abbreviation, sportId: sport.id,
        name: t.name, city: t.city,
        primaryHex: t.primaryHex, secondaryHex: t.secondaryHex,
        stadiumName: t.stadiumName,
        stadiumPrompt: t.stadiumPrompt, skylinePrompt: t.skylinePrompt, skyPrompt: t.skyPrompt,
        jerseyPrompt: t.jerseyPrompt, pantsPrompt: t.pantsPrompt, helmetPrompt: t.helmetPrompt,
        numberStyle: t.numberStyle, logoPrompt: t.logoPrompt,
      },
    });

    // Re-seed card players (delete + recreate for clean state)
    await prisma.cardPlayer.deleteMany({ where: { teamId: team.id } });
    await prisma.cardPlayer.createMany({
      data: t.cardPlayers.map((p) => ({
        teamId: team.id,
        name: p.name, number: p.number, position: p.position,
        side: p.side, pose: p.pose ?? "auto", ball: p.ball ?? "auto",
        order: p.order ?? 0,
      })),
    });

    console.log(`  ✓ ${t.abbreviation} — ${t.name}`);
  }

  console.log(`NFL: ${NFL_TEAMS.length} teams seeded.`);
}
