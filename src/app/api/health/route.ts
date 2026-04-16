import { NextResponse } from "next/server";

/** No auth — use on Vercel to confirm env wiring (booleans only, no secrets). */
export async function GET() {
  const hasAuthUrl = !!(process.env.AUTH_URL ?? process.env.NEXTAUTH_URL);
  const hasAuthSecret = !!(process.env.AUTH_SECRET ?? process.env.NEXTAUTH_SECRET);
  const hasPostgresPrismaUrl = !!process.env.POSTGRES_PRISMA_URL;
  const hasDatabaseUrl = !!process.env.DATABASE_URL;
  const hasPostgresUrl = !!process.env.POSTGRES_URL;

  let dbResolved = false;
  try {
    const { getDatabaseUrl } = await import("@/lib/database-url");
    getDatabaseUrl();
    dbResolved = true;
  } catch {
    dbResolved = false;
  }

  return NextResponse.json({
    ok: true,
    env: {
      hasAuthUrl,
      hasAuthSecret,
      hasPostgresPrismaUrl,
      hasDatabaseUrl,
      hasPostgresUrl,
      dbResolved,
    },
  });
}
