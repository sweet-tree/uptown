/**
 * Vercel + Neon injects `DATABASE_URL` (pooled). Local / Neon docs sometimes use
 * `POSTGRES_PRISMA_URL` for the same pooler string. Accept both so production works.
 */
export function getDatabaseUrl(): string {
  const url =
    process.env.POSTGRES_PRISMA_URL?.trim() ||
    process.env.DATABASE_URL?.trim() ||
    process.env.POSTGRES_URL?.trim();
  if (!url) {
    throw new Error(
      "Missing database connection string. Set DATABASE_URL (Vercel Neon default) or POSTGRES_PRISMA_URL.",
    );
  }
  return url;
}
