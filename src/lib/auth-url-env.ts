/**
 * NextAuth's `reqWithEnvURL` does `new URL(process.env.AUTH_URL ?? NEXTAUTH_URL)` with no try/catch.
 * A malformed value (missing scheme, quotes, typo) makes every `/api/auth/*` route return HTTP 500.
 * With `trustHost: true`, omitting both vars is fine; invalid strings must not reach NextAuth.
 */
export function normalizeAuthUrlEnvVars(): void {
  for (const key of ["AUTH_URL", "NEXTAUTH_URL"] as const) {
    const raw = process.env[key];
    if (!raw) continue;
    const cleaned = raw.trim().replace(/\/+$/, "");
    if (!cleaned) {
      delete process.env[key];
      continue;
    }
    try {
      const u = new URL(cleaned);
      if ((u.protocol !== "http:" && u.protocol !== "https:") || !u.hostname) {
        delete process.env[key];
        continue;
      }
      process.env[key] = cleaned;
    } catch {
      delete process.env[key];
    }
  }
}

/** Whether an optional AUTH_URL / NEXTAUTH_URL is safe for NextAuth (or unset = OK with trustHost). */
export function authUrlEnvOk(): { hasAuthUrl: boolean; authUrlOk: boolean } {
  const raw = (process.env.AUTH_URL ?? process.env.NEXTAUTH_URL)?.trim();
  if (!raw) {
    return { hasAuthUrl: false, authUrlOk: true };
  }
  try {
    const u = new URL(raw);
    const ok = (u.protocol === "http:" || u.protocol === "https:") && !!u.hostname;
    return { hasAuthUrl: true, authUrlOk: ok };
  } catch {
    return { hasAuthUrl: true, authUrlOk: false };
  }
}
