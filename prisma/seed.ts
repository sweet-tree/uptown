import { config } from "dotenv";
config({ path: ".env.local" });
config({ path: ".env" });

import { argon2id, hash } from "argon2";
import { PrismaClient } from "../src/generated/prisma/client";
import { PrismaNeon } from "@prisma/adapter-neon";
import { getDatabaseUrl } from "../src/lib/database-url";
import { seedNFL } from "./seeds/nfl/index";
import { seedNBA } from "./seeds/nba/index";

async function main() {
  const adapter = new PrismaNeon({
    connectionString: getDatabaseUrl(),
  });
  const prisma = new PrismaClient({ adapter });

  console.log("Seeding sports catalog...\n");

  await seedNFL(prisma);
  await seedNBA(prisma);

  const seedEmail = process.env.AUTH_SEED_EMAIL?.trim().toLowerCase();
  const seedPassword = process.env.AUTH_SEED_PASSWORD;
  if (seedEmail && seedPassword) {
    const passwordHash = await hash(seedPassword, { type: argon2id });
    await prisma.user.upsert({
      where: { email: seedEmail },
      create: { email: seedEmail, passwordHash, name: "Admin" },
      update: { passwordHash },
    });
    console.log(`\nSeeded credentials user: ${seedEmail}`);
  }

  await prisma.$disconnect();
  console.log("\nDone.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
