import { NextRequest, NextResponse } from "next/server";
import { ai, MODELS, fileToInlineData, saveImage, extractImageBase64 } from "@/lib/gemini";
import { getTeamByAbbr } from "@/app/actions/teams";
import { buildPlayerPrompt } from "@/lib/prompt-engine";
import { getPrisma } from "@/lib/db";
import { saveGeneration } from "@/app/actions/prompts";
import type { GeneratePlayerRequest } from "@/lib/types";

export const maxDuration = 120;

export async function POST(req: NextRequest) {
  try {
    const body: GeneratePlayerRequest = await req.json();
    const { team: teamAbbr, side, player, number, pose, ball, model = "flash" } = body;

    const team = await getTeamByAbbr(teamAbbr);

    let resolvedName: string;
    let resolvedNumber: string;
    let resolvedPosition: string;
    let resolvedPose = pose ?? "auto";
    let resolvedBall = ball ?? "auto";

    if (player) {
      const fromCard = team.cardPlayers.find(
        (p) => p.name.toLowerCase() === player.toLowerCase(),
      );
      if (fromCard) {
        resolvedName     = fromCard.name;
        resolvedNumber   = fromCard.number;
        resolvedPosition = fromCard.position;
        if (!pose) resolvedPose = fromCard.pose;
        if (!ball) resolvedBall = fromCard.ball;
      } else {
        const fromRoster = team.rosterEntries.find(
          (p) => p.name.toLowerCase() === player.toLowerCase(),
        );
        if (!fromRoster) {
          return NextResponse.json(
            { ok: false, error: `Player "${player}" not found for ${teamAbbr}` },
            { status: 400 },
          );
        }
        resolvedName     = fromRoster.name;
        resolvedNumber   = fromRoster.number;
        resolvedPosition = fromRoster.position;
      }
    } else if (number) {
      const fromCard = team.cardPlayers.find((p) => p.number === number);
      if (fromCard) {
        resolvedName     = fromCard.name;
        resolvedNumber   = fromCard.number;
        resolvedPosition = fromCard.position;
      } else {
        const fromRoster = team.rosterEntries.find((p) => p.number === number);
        if (!fromRoster) {
          return NextResponse.json(
            { ok: false, error: `#${number} not found for ${teamAbbr}` },
            { status: 400 },
          );
        }
        resolvedName     = fromRoster.name;
        resolvedNumber   = fromRoster.number;
        resolvedPosition = fromRoster.position;
      }
    } else {
      const spec = team.cardPlayers.find((p) => p.side === side);
      if (!spec) {
        return NextResponse.json({ ok: false, error: `No default ${side} player for ${teamAbbr}` }, { status: 400 });
      }
      resolvedName     = spec.name;
      resolvedNumber   = spec.number;
      resolvedPosition = spec.position;
      if (!pose) resolvedPose = spec.pose;
      if (!ball) resolvedBall = spec.ball;
    }

    const promptKey = `player:${teamAbbr.toUpperCase()}:${side}`;
    const storedPrompt = await getPrisma().prompt.findUnique({ where: { key: promptKey } });
    const prompt = storedPrompt?.text ?? buildPlayerPrompt(
      team, resolvedName, resolvedNumber, resolvedPosition,
      side, resolvedPose, resolvedBall,
    );

    const refPath = side === "left" ? "assets/player_ref_left.jpg" : "assets/player_ref_right.jpg";
    const refPart = fileToInlineData(refPath);

    const response = await ai.models.generateContent({
      model: MODELS[model],
      contents: [{ role: "user", parts: [{ text: prompt }, refPart] }],
    });

    const base64 = extractImageBase64(response);
    if (!base64) {
      const textPart = response.candidates?.[0]?.content?.parts?.find((p: { text?: string }) => p.text);
      return NextResponse.json({ ok: false, error: textPart?.text ?? "No image in response" }, { status: 500 });
    }

    const slug = resolvedName.toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/(^_|_$)/g, "");
    const filename = `${teamAbbr.toLowerCase()}_${slug}_${side}_raw.jpg`;
    const outPath  = `output/players/${filename}`;
    saveImage(base64, outPath);

    await saveGeneration({
      team: teamAbbr.toUpperCase(),
      type: "player",
      side,
      playerName: resolvedName,
      number: resolvedNumber,
      pose: resolvedPose,
      model,
      imagePath: outPath,
    });

    return NextResponse.json({
      ok: true,
      path: outPath,
      dataUrl: `data:image/jpeg;base64,${base64}`,
      player: resolvedName,
      number: resolvedNumber,
      position: resolvedPosition,
      promptKey,
      usedCustomPrompt: !!storedPrompt,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    return NextResponse.json({ ok: false, error: msg }, { status: 500 });
  }
}
