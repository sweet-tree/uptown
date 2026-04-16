import NextAuth, { CredentialsSignin } from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { getPrisma } from "@/lib/db";

/** Trim whitespace; strip trailing slashes (Auth.js expects a canonical origin). */
function normalizeAuthUrlEnv() {
  for (const key of ["AUTH_URL", "NEXTAUTH_URL"] as const) {
    const raw = process.env[key];
    if (!raw) continue;
    const cleaned = raw.trim().replace(/\/+$/, "");
    if (cleaned) {
      process.env[key] = cleaned;
    }
  }
}

normalizeAuthUrlEnv();

class InvalidCredentials extends CredentialsSignin {
  code = "invalid_credentials";
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  trustHost: true,
  secret: process.env.AUTH_SECRET?.trim() || process.env.NEXTAUTH_SECRET?.trim(),
  pages: { signIn: "/login" },
  session: { strategy: "jwt", maxAge: 14 * 24 * 60 * 60 },
  providers: [
    Credentials({
      id: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const email =
          typeof credentials?.email === "string" ? credentials.email.trim().toLowerCase() : "";
        const password = typeof credentials?.password === "string" ? credentials.password : "";
        if (!email || !password) {
          throw new InvalidCredentials();
        }

        const prisma = getPrisma();
        const user = await prisma.user.findUnique({ where: { email } });
        if (!user) {
          throw new InvalidCredentials();
        }

        const { verify } = await import("argon2");
        const ok = await verify(user.passwordHash, password).catch(() => false);
        if (!ok) {
          throw new InvalidCredentials();
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name ?? undefined,
        };
      },
    }),
  ],
  callbacks: {
    authorized({ auth, request }) {
      const path = request.nextUrl.pathname;
      if (path.startsWith("/login")) {
        return true;
      }
      if (path.startsWith("/api/auth")) {
        return true;
      }
      if (path.startsWith("/api/health")) {
        return true;
      }

      // App Router flight / prefetch requests must not get an HTML redirect from the proxy.
      // In production that often surfaces as an endless reload while the router retries RSC.
      const isFlightOrPrefetch =
        request.headers.get("RSC") === "1" ||
        request.headers.get("Next-Router-Prefetch") === "1";
      if (!auth?.user && isFlightOrPrefetch && !path.startsWith("/api/")) {
        return true;
      }

      return !!auth?.user;
    },
    jwt({ token, user }) {
      if (user) {
        token.sub = user.id;
        token.email = user.email;
        token.name = user.name;
      }
      return token;
    },
    session({ session, token }) {
      if (session.user && token.sub) {
        session.user.id = token.sub;
        if (typeof token.email === "string") {
          session.user.email = token.email;
        }
        if (typeof token.name === "string") {
          session.user.name = token.name;
        }
      }
      return session;
    },
  },
});
