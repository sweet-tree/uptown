import { GoogleGenAI } from "@google/genai";
import fs from "fs";
import os from "os";
import path from "path";

let genaiClient: GoogleGenAI | undefined;

/** Lazy init so missing `GEMINI_API_KEY` does not crash unrelated routes at import time. */
export function getGenAI(): GoogleGenAI {
  if (!genaiClient) {
    const apiKey = process.env.GEMINI_API_KEY?.trim();
    if (!apiKey) {
      throw new Error("GEMINI_API_KEY is not set");
    }
    genaiClient = new GoogleGenAI({ apiKey });
  }
  return genaiClient;
}

export const MODELS = {
  flash: "gemini-2.5-flash-image",
  pro: "gemini-3-pro-image-preview",
} as const;

export type ModelTier = keyof typeof MODELS;

/** Resolve a path relative to the repo root (same as Next.js cwd) */
export function workspacePath(...segments: string[]): string {
  return path.resolve(process.cwd(), ...segments);
}

/** Vercel serverless FS is read-only outside `/tmp`; keep logical paths for DB, write under tmp there. */
function writeRootDir(): string {
  return process.env.VERCEL === "1" ? path.join(os.tmpdir(), "uptowns-writes") : process.cwd();
}

/** Load a file from the workspace as a base64 part for Gemini */
export function fileToInlineData(filePath: string, mimeType = "image/jpeg") {
  const abs = path.isAbsolute(filePath)
    ? filePath
    : resolveReadableAsset(workspacePath(filePath), filePath);
  const data = fs.readFileSync(abs).toString("base64");
  return { inlineData: { data, mimeType } };
}

/** Prefer repo `assets/`; fall back to `public/generate-refs/<basename>` after tracing/cdn layout. */
function resolveReadableAsset(resolvedFromCwd: string, originalRelative: string): string {
  if (fs.existsSync(resolvedFromCwd)) {
    return resolvedFromCwd;
  }
  const base = path.basename(originalRelative.replace(/\\/g, "/"));
  const underPublic = workspacePath("public", "generate-refs", base);
  if (fs.existsSync(underPublic)) {
    return underPublic;
  }
  return resolvedFromCwd;
}

/** Save base64 image to disk, returns the absolute path */
export function saveImage(base64: string, outPath: string): string {
  const abs = path.isAbsolute(outPath) ? outPath : path.resolve(writeRootDir(), outPath);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, Buffer.from(base64, "base64"));
  return abs;
}

/** Extract the first image part from a Gemini response */
export function extractImageBase64(
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  response: any
): string | null {
  for (const part of response.candidates?.[0]?.content?.parts ?? []) {
    if (part.inlineData?.data) return part.inlineData.data as string;
  }
  return null;
}
