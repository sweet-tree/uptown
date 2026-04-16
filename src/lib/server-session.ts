import type { Session } from "next-auth";

/**
 * When Auth.js config validation fails, `auth()` can resolve to a JSON error body
 * (`{ message: string }`) instead of a session. Passing that into `SessionProvider`
 * can crash the tree in production.
 */
export function serverSessionOrNull(value: unknown): Session | null {
  if (!value || typeof value !== "object") {
    return null;
  }
  const o = value as Record<string, unknown>;
  // Auth.js misconfiguration responses look like `{ message: "..." }` without a session shape.
  if (typeof o.message === "string" && o.user === undefined && o.expires === undefined) {
    return null;
  }
  return value as Session;
}
