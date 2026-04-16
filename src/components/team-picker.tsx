"use client";

import { useMemo, useState } from "react";
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  Field,
  Label,
} from "@headlessui/react";
import type { TeamWithPlayers } from "@/lib/types";
import { COMBO_TRIGGER_MIN_PX, TEAM_LIST_MAX_PX } from "@/components/picker-dimensions";
import { IconChevronsUpDown } from "@/components/ui/icons";

function teamMatchesQuery(t: TeamWithPlayers, q: string): boolean {
  const s = q.trim().toLowerCase();
  if (!s) return true;
  return (
    t.abbreviation.toLowerCase().includes(s) ||
    t.name.toLowerCase().includes(s) ||
    t.city.toLowerCase().includes(s)
  );
}

export function TeamPicker({
  teams,
  selectedAbbr,
  onSelect,
  loading,
  error,
}: {
  teams: TeamWithPlayers[];
  selectedAbbr: string;
  onSelect: (abbr: string) => void;
  loading: boolean;
  error: Error | null;
}) {
  const [query, setQuery] = useState("");
  const selected = useMemo(
    () => teams.find((t) => t.abbreviation === selectedAbbr) ?? null,
    [teams, selectedAbbr],
  );

  const filtered = useMemo(
    () => teams.filter((t) => teamMatchesQuery(t, query)),
    [teams, query],
  );

  if (loading) {
    return (
      <div className="min-w-0 py-3 text-sm leading-relaxed text-[var(--muted)]">
        Loading teams…
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-w-0 py-3 text-[11px] leading-snug text-[var(--danger)]">
        Could not load teams. Run{" "}
        <code className="font-mono-code text-[10px]">npx prisma generate</code>, restart the dev server, then refresh.
        {error.message ? ` (${error.message})` : ""}
      </div>
    );
  }

  return (
    <Field className="ds-field min-h-0 flex-1">
      <Label className="ds-overline">Teams</Label>
      <Combobox
        value={selected}
        by={(a, b) => a?.abbreviation === b?.abbreviation}
        onChange={(t: TeamWithPlayers | null) => {
          if (t) onSelect(t.abbreviation);
        }}
        onClose={() => setQuery("")}
      >
        <div className="relative min-w-0">
          <div className="ds-combobox-trigger" style={{ minHeight: COMBO_TRIGGER_MIN_PX }}>
            <ComboboxInput
              autoComplete="off"
              displayValue={(t: TeamWithPlayers | null) => (t ? `${t.abbreviation} · ${t.name}` : "")}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search teams…"
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
            style={{ maxHeight: TEAM_LIST_MAX_PX }}
            className="ds-combobox-options-panel z-[100] w-[var(--input-width)] empty:invisible outline-none data-[closed]:opacity-0 motion-safe:data-[closed]:translate-y-0.5 motion-safe:transition data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
          >
            {filtered.map((t) => (
              <ComboboxOption key={t.abbreviation} value={t} className="ds-combobox-option-row">
                <span
                  className="size-2 shrink-0 rounded-full ring-1 ring-black/20"
                  style={{ backgroundColor: t.primaryHex }}
                  aria-hidden
                />
                <span className="ds-combobox-option-row__grow">
                  <span className="ds-combobox-option-row__primary">{t.abbreviation}</span>
                  <span className="ds-combobox-option-row__secondary">{t.name}</span>
                </span>
              </ComboboxOption>
            ))}
          </ComboboxOptions>
        </div>
      </Combobox>
    </Field>
  );
}
