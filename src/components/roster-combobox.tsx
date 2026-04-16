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
import { IconChevronsUpDown } from "@/components/ui/icons";

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
    <Field className="ds-field min-w-0">
      <Label className="ds-overline">Roster</Label>
      <Combobox
        onChange={(row: RosterEntry | null) => {
          if (!row) return;
          const card = resolveCardPlayerForRoster(cardPlayers, row);
          const slot: "left" | "right" = card?.side === "right" ? "right" : "left";
          onPick(row, slot);
        }}
        onClose={() => setQuery("")}
      >
        <div className="relative min-w-0">
          <div className="ds-combobox-trigger" style={{ minHeight: COMBO_TRIGGER_MIN_PX }}>
            <ComboboxInput
              autoComplete="off"
              displayValue={() => ""}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search players…"
              className="ds-combobox-input"
            />
            <ComboboxButton type="button" className="ds-combobox-chevron-btn">
              <IconChevronsUpDown className="size-4 opacity-90" />
            </ComboboxButton>
          </div>
          <ComboboxOptions
            portal
            modal={false}
            transition
            anchor={{ to: "bottom start", gap: 6 }}
            style={{ maxHeight: ROSTER_LIST_MAX_PX }}
            className="ds-combobox-options-panel z-[90] w-[var(--input-width)] empty:invisible outline-none data-[closed]:opacity-0 motion-safe:data-[closed]:translate-y-0.5 motion-safe:transition data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
          >
            {filtered.map((r) => {
              const card = resolveCardPlayerForRoster(cardPlayers, r);
              return (
                <ComboboxOption
                  key={r.id}
                  value={r}
                  className="ds-combobox-option-row ds-combobox-option-row--dense ds-combobox-option-row--split"
                >
                  <span className="ds-combobox-option-row__grow ds-combobox-option-row__pick">
                    <span className="font-mono-code text-xs font-medium text-[var(--text)]">#{r.number}</span>
                    <span> {r.name}</span>
                  </span>
                  <span className="ds-combobox-option-row__meta">
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
