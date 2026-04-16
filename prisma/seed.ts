import { config } from "dotenv";
config({ path: ".env.local" });
config({ path: ".env" });

import { PrismaClient } from "../src/generated/prisma/client";
import { PrismaNeon } from "@prisma/adapter-neon";
import { seedNFL } from "./seeds/nfl/index";
import { seedNBA } from "./seeds/nba/index";

async function main() {
  const adapter = new PrismaNeon({
    connectionString: process.env.POSTGRES_PRISMA_URL!,
  });
  const prisma = new PrismaClient({ adapter });

  console.log("Seeding sports catalog...\n");

  await seedNFL(prisma);
  await seedNBA(prisma);

  await prisma.$disconnect();
  console.log("\nDone.");
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
