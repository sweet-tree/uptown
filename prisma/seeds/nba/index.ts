import type { PrismaClient } from "../../src/generated/prisma/client";

export async function seedNBA(prisma: PrismaClient) {
  await prisma.sport.upsert({
    where: { slug: "nba" },
    update: { name: "NBA", active: false },
    create: { slug: "nba", name: "NBA", active: false },
  });
  console.log("NBA: placeholder seeded (no teams yet).");
}
