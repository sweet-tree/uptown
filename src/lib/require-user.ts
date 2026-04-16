import { auth } from "@/auth";
import { redirect } from "next/navigation";

/** Use at the start of server actions and route handlers that must not run anonymously. */
export async function requireUser() {
  const session = await auth();
  if (!session?.user?.id) {
    redirect("/login");
  }
  return session;
}
