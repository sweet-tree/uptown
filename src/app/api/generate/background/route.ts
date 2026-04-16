import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/auth";
import {
  getGenAI,
  MODELS,
  fileToInlineData,
  saveImage,
  extractImageBase64,
  imageGenerateConfig,
} from "@/lib/gemini";
import { getTeamByAbbr } from "@/app/actions/teams";
import { buildBackgroundPrompt } from "@/lib/prompt-engine";
import { getPrisma } from "@/lib/db";
import { saveGeneration } from "@/app/actions/prompts";
import type { GenerateBackgroundRequest } from "@/lib/types";

export const maxDuration = 120;

export async function POST(req: NextRequest) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ ok: false, error: "Unauthorized" }, { status: 401 });
    }

    const body: GenerateBackgroundRequest = await req.json();
    const { team: teamAbbr, model = "flash" } = body;

    const team = await getTeamByAbbr(teamAbbr);

    // Check for prompt override in DB
    const promptKey = `background:${teamAbbr.toUpperCase()}`;
    const storedPrompt = await getPrisma().prompt.findUnique({ where: { key: promptKey } });
    const prompt = storedPrompt?.text ?? buildBackgroundPrompt(team);

    const styleRef = fileToInlineData("assets/uptowns_sticker_ref.jpg");

    const response = await getGenAI().models.generateContent({
      model: MODELS[model],
      contents: [{ role: "user", parts: [{ text: prompt }, styleRef] }],
      config: imageGenerateConfig(model, {
        aspectRatio: "16:9",
        flashImageSize: "2K",
        proImageSize: "4K",
      }),
    });

    const base64 = extractImageBase64(response);
    if (!base64) {
      const textPart = response.candidates?.[0]?.content?.parts?.find((p: { text?: string }) => p.text);
      return NextResponse.json({ ok: false, error: textPart?.text ?? "No image in response" }, { status: 500 });
    }

    const filename = `${teamAbbr.toLowerCase()}_background_raw.jpg`;
    const outPath  = `output/backgrounds/${filename}`;
    saveImage(base64, outPath);

    await saveGeneration({
      team: teamAbbr.toUpperCase(),
      type: "background",
      model,
      imagePath: outPath,
    });

    return NextResponse.json({
      ok: true,
      path: outPath,
      dataUrl: `data:image/jpeg;base64,${base64}`,
      promptKey,
      usedCustomPrompt: !!storedPrompt,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return NextResponse.json({ ok: false, error: msg }, { status: 500 });
  }
}
