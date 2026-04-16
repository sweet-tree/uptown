import { PrismaClient } from "../generated/prisma/client";
import { PrismaNeon } from "@prisma/adapter-neon";

function createPrismaClient() {
  const adapter = new PrismaNeon({
    connectionString: process.env.POSTGRES_PRISMA_URL!,
  });
  return new PrismaClient({ adapter });
}

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

function rosterDelegateMissing(client: PrismaClient | undefined): boolean {
  if (!client) return true;
  const d = (client as unknown as { rosterEntry?: { findMany?: unknown } }).rosterEntry;
  return typeof d?.findMany !== "function";
}

/**
 * After `prisma generate`, Next dev can keep a stale PrismaClient on `globalThis`
 * that predates new models — delegates like `rosterEntry` are then undefined.
 * In development, drop that cache so the next import gets a fresh client.
 */
function getPrisma(): PrismaClient {
  const g = globalForPrisma;
  if (process.env.NODE_ENV !== "production" && g.prisma && rosterDelegateMissing(g.prisma)) {
    void g.prisma.$disconnect().catch(() => {});
    g.prisma = undefined;
  }
  if (!g.prisma) {
    g.prisma = createPrismaClient();
  }
  return g.prisma;
}

export const prisma = getPrisma();
