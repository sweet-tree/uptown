import type { CardPlayer, RosterEntry } from "@/generated/prisma/client";

/**
 * Map a roster row to a card slot when jersey numbers collide (e.g. many "0" placeholders).
 */
export function resolveCardPlayerForRoster(
  cardPlayers: CardPlayer[],
  roster: Pick<RosterEntry, "name" | "number">,
): CardPlayer | undefined {
  const norm = (s: string) => s.trim().toLowerCase().replace(/\s+/g, " ");
  const rName = norm(roster.name);
  const num = roster.number.trim();

  if (num === "" || num === "0") {
    return cardPlayers.find((c) => norm(c.name) === rName);
  }

  const sameNum = cardPlayers.filter((c) => c.number.trim() === num);
  if (sameNum.length === 0) return undefined;
  if (sameNum.length === 1) return sameNum[0];
  return sameNum.find((c) => norm(c.name) === rName) ?? sameNum[0];
}
