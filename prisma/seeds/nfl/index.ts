import path from "node:path";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import type { PrismaClient } from "../../src/generated/prisma/client";
import type { TeamSeed } from "../types";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const nflJsonPath = path.join(__dirname, "nfl-full.generated.json");

type NflSeedFile = { teams: TeamSeed[]; meta: Record<string, unknown> };

const { teams: NFL_TEAMS } = JSON.parse(readFileSync(nflJsonPath, "utf8")) as NflSeedFile;

export { NFL_TEAMS };

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

    await prisma.cardPlayer.deleteMany({ where: { teamId: team.id } });
    if (t.cardPlayers.length) {
      await prisma.cardPlayer.createMany({
        data: t.cardPlayers.map((p) => ({
          teamId: team.id,
          name: p.name, number: p.number, position: p.position,
          side: p.side, pose: p.pose ?? "auto", ball: p.ball ?? "auto",
          order: p.order ?? 0,
        })),
      });
    }

    await prisma.rosterEntry.deleteMany({ where: { teamId: team.id } });
    if (t.roster?.length) {
      await prisma.rosterEntry.createMany({
        data: t.roster.map((r, idx) => {
          const n = Number.parseInt(r.number, 10);
          const base = Number.isFinite(n) ? n : 0;
          return {
            teamId: team.id,
            name: r.name,
            number: r.number,
            position: r.position,
            sortOrder: base * 100 + idx,
          };
        }),
      });
    }

    console.log(`  ✓ ${t.abbreviation} — ${t.name}`);
  }

  console.log(`NFL: ${NFL_TEAMS.length} teams seeded.`);
}
