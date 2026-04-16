import { NextResponse } from "next/server";

/** No auth — use on Vercel to confirm env wiring (booleans only, no secrets). */
export async function GET() {
  const hasAuthUrl = !!(process.env.AUTH_URL ?? process.env.NEXTAUTH_URL);
  const hasAuthSecret = !!(process.env.AUTH_SECRET ?? process.env.NEXTAUTH_SECRET);
  const hasDb = !!process.env.POSTGRES_PRISMA_URL;

  return NextResponse.json({
    ok: true,
    env: { hasAuthUrl, hasAuthSecret, hasDb },
  });
}
