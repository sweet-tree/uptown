import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { serverSessionOrNull } from "@/lib/server-session";

/**
 * Server-side protection for `/` (this route group). Avoids NextAuth `auth` as `proxy`, which
 * repeatedly hit fragile `getSession`/RSC paths on Vercel. Public routes stay outside this group.
 */
export default async function DashboardLayout({ children }: { children: React.ReactNode }) {
  let raw: unknown;
  try {
    raw = await auth();
  } catch {
    raw = null;
  }
  const session = serverSessionOrNull(raw);
  if (!session?.user?.id) {
    redirect("/login");
  }
  return children;
}
