import { PrismaClient } from "../generated/prisma/client";
import { PrismaNeon } from "@prisma/adapter-neon";
import { getDatabaseUrl } from "./database-url";

function createPrismaClient() {
  const adapter = new PrismaNeon({
    connectionString: getDatabaseUrl(),
  });
  return new PrismaClient({ adapter });
}

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

/** Every delegate this app uses from PrismaClient — stale globals after `prisma generate` drop methods. */
const DELEGATE_CHECKS = [
  ["sport", "findMany"],
  ["team", "findMany"],
  ["rosterEntry", "findMany"],
  ["cardPlayer", "findMany"],
  ["prompt", "findUnique"],
  ["generation", "findMany"],
  ["user", "findUnique"],
] as const;

function delegatesHealthy(client: PrismaClient | undefined): boolean {
  if (!client) return false;
  const c = client as unknown as Record<string, Record<string, unknown> | undefined>;
  for (const [model, method] of DELEGATE_CHECKS) {
    const delegate = c[model];
    if (typeof delegate?.[method] !== "function") return false;
  }
  return true;
}

/**
 * Returns a PrismaClient that matches the generated schema.
 * In development, clears a cached `globalThis.prisma` when delegates are missing
 * (common after `prisma generate` while Next dev keeps a hot-reloaded module graph).
 */
export function getPrisma(): PrismaClient {
  const g = globalForPrisma;
  if (process.env.NODE_ENV !== "production" && g.prisma && !delegatesHealthy(g.prisma)) {
    void g.prisma.$disconnect().catch(() => {});
    g.prisma = undefined;
  }
  if (!g.prisma) {
    g.prisma = createPrismaClient();
  }
  return g.prisma;
}
