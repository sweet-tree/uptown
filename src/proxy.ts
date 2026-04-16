export { auth as proxy } from "@/auth";

export const config = {
  matcher: [
    /*
     * Exclude:
     * - NextAuth routes (handled by route.ts; avoids subtle proxy+session interactions in prod)
     * - Static / image assets
     * Other `/api/*` still hit the proxy so `authorized` can enforce sessions.
     */
    "/((?!api/auth|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
