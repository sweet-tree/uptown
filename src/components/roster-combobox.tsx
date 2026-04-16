"use client";

import { useMemo, useState } from "react";
import Fuse from "fuse.js";
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  Field,
  Label,
} from "@headlessui/react";
import type { CardPlayer, RosterEntry } from "@/generated/prisma/client";
import { resolveCardPlayerForRoster } from "@/lib/resolve-card-player";
import { COMBO_TRIGGER_MIN_PX, ROSTER_LIST_MAX_PX } from "@/components/picker-dimensions";

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="currentColor" aria-hidden>
      <path
        fillRule="evenodd"
        d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z"
        clipRule="evenodd"
      />
    </svg>
  );
}

export function RosterCombobox({
  entries,
  cardPlayers,
  onPick,
}: {
  entries: RosterEntry[];
  cardPlayers: CardPlayer[];
  onPick: (row: RosterEntry, side: "left" | "right") => void;
}) {
  const [query, setQuery] = useState("");

  const fuse = useMemo(
    () =>
      new Fuse(entries, {
        keys: [
          { name: "name", weight: 0.62 },
          { name: "number", weight: 0.22 },
          { name: "position", weight: 0.16 },
        ],
        threshold: 0.32,
        ignoreLocation: true,
        includeScore: true,
      }),
    [entries],
  );

  const filtered = useMemo(() => {
    const q = query.trim();
    if (!q) return entries;
    return fuse.search(q).map((r) => r.item);
  }, [entries, fuse, query]);

  return (
    <Field className="flex flex-col gap-1.5">
      <Label className="text-[10px] font-medium uppercase tracking-widest text-[var(--muted)]">
        Roster
      </Label>
      <Combobox
        onChange={(row: RosterEntry | null) => {
          if (!row) return;
          const card = resolveCardPlayerForRoster(cardPlayers, row);
          const slot: "left" | "right" = card?.side === "right" ? "right" : "left";
          onPick(row, slot);
        }}
        onClose={() => setQuery("")}
      >
        <div className="relative">
          <div
            className="flex items-center rounded-lg border border-[var(--border)] bg-[var(--panel)] shadow-sm focus-within:border-[var(--accent)] focus-within:ring-1 focus-within:ring-[var(--accent)]"
            style={{ minHeight: COMBO_TRIGGER_MIN_PX }}
          >
            <ComboboxInput
              autoComplete="off"
              displayValue={() => ""}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search players…"
              className="min-w-0 flex-1 border-0 bg-transparent py-2 pl-3 pr-1 text-sm leading-tight text-[var(--text)] placeholder:text-[var(--muted)] focus:outline-none"
            />
            <ComboboxButton className="flex h-full shrink-0 items-center px-2 text-[var(--muted)] hover:text-[var(--text)]">
              <ChevronDown className="size-4" />
            </ComboboxButton>
          </div>
          <ComboboxOptions
            portal
            modal={false}
            transition
            anchor={{ to: "bottom start", gap: 6 }}
            style={{ maxHeight: ROSTER_LIST_MAX_PX }}
            className="z-[90] w-[var(--input-width)] overflow-y-auto overscroll-y-contain rounded-lg border border-[var(--border)] bg-[var(--panel)] py-1 shadow-xl outline-none empty:invisible data-[closed]:opacity-0 motion-safe:data-[closed]:translate-y-0.5 motion-safe:transition data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
          >
            {filtered.map((r) => {
              const card = resolveCardPlayerForRoster(cardPlayers, r);
              return (
                <ComboboxOption
                  key={r.id}
                  value={r}
                  className="group flex min-h-[44px] cursor-pointer items-center justify-between gap-2 px-2.5 py-2 text-left text-sm data-focus:bg-[rgba(108,99,255,0.14)] data-selected:bg-[rgba(108,99,255,0.08)]"
                >
                  <span className="min-w-0 truncate text-[var(--muted)] group-data-focus:text-[var(--text)]">
                    <span className="font-mono text-xs text-[var(--text)]">#{r.number}</span>{" "}
                    {r.name}
                  </span>
                  <span className="shrink-0 text-xs font-semibold uppercase text-[var(--accent)]">
                    {r.position}
                    {card ? ` · ${card.side}` : ""}
                  </span>
                </ComboboxOption>
              );
            })}
          </ComboboxOptions>
        </div>
      </Combobox>
    </Field>
  );
}
