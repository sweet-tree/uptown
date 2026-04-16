export { auth as proxy } from "@/auth";

export const config = {
  matcher: [
    /*
     * Match all request paths except static assets and images.
     * (API auth is allowed inside `authorized`; other `/api/*` require a session.)
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
