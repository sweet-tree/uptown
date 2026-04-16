import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Native / Node-only deps: keep them external so Vercel loads prebuilds correctly.
  serverExternalPackages: ["argon2", "@prisma/client", "prisma"],
  /**
   * `fileToInlineData("assets/...")` reads repo JPEGs; NFT tracing does not pick up `assets/` by default,
   * so Vercel lambdas had ENOENT. Keys are picomatch'd against normalized app routes (e.g. `/app/api/...`).
   */
  outputFileTracingIncludes: {
    "**/api/generate/*": ["./assets/**/*"],
  },
};

export default nextConfig;
