import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Native / Node-only deps: keep them external so Vercel loads prebuilds correctly.
  serverExternalPackages: ["argon2", "@prisma/client", "prisma"],
};

export default nextConfig;
