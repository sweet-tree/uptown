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
  if ("message" in value && !("user" in value)) {
    return null;
  }
  if (!("expires" in value)) {
    return null;
  }
  return value as Session;
}
