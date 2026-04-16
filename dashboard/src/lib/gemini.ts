import { GoogleGenAI } from "@google/genai";
import fs from "fs";
import path from "path";

export const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! });

export const MODELS = {
  flash: "gemini-2.5-flash-image",
  pro: "gemini-3-pro-image-preview",
} as const;

export type ModelTier = keyof typeof MODELS;

/** Resolve a path relative to the workspace root (two levels up from dashboard/) */
export function workspacePath(...segments: string[]): string {
  return path.resolve(process.cwd(), "..", ...segments);
}

/** Load a file from the workspace as a base64 part for Gemini */
export function fileToInlineData(filePath: string, mimeType = "image/jpeg") {
  const abs = path.isAbsolute(filePath) ? filePath : workspacePath(filePath);
  const data = fs.readFileSync(abs).toString("base64");
  return { inlineData: { data, mimeType } };
}

/** Save base64 image to disk, returns the absolute path */
export function saveImage(base64: string, outPath: string): string {
  const abs = path.isAbsolute(outPath) ? outPath : workspacePath(outPath);
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
