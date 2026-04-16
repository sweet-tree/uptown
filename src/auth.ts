/**
 * Do not statically import `@/lib/db` here: keep Prisma on the Node path (credentials `authorize` only).
 */
import NextAuth, { CredentialsSignin } from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { normalizeAuthUrlEnvVars } from "@/lib/auth-url-env";

normalizeAuthUrlEnvVars();

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

        const { getPrisma } = await import("@/lib/db");
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
    jwt({ token, user }) {
      if (user) {
        token.sub = user.id;
        token.email = user.email;
        token.name = user.name;
      }
      return token;
    },
    session({ session, token }) {
      // JWT: `session.user` is often empty on first paint; never gate on `if (session.user)`.
      if (typeof token.sub === "string" && token.sub.length > 0) {
        session.user = {
          ...session.user,
          id: token.sub,
          email:
            typeof token.email === "string"
              ? token.email
              : (session.user?.email ?? ""),
          name:
            typeof token.name === "string"
              ? token.name
              : (session.user?.name ?? null),
        };
      }
      return session;
    },
  },
});
