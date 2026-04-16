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
      <div className="px-3.5 py-3 text-xs text-[var(--muted)]">
        Loading teams…
      </div>
    );
  }

  if (error) {
    return (
      <div className="px-3.5 py-3 text-[11px] leading-snug text-[var(--danger)]">
        Could not load teams. Run{" "}
        <code className="text-[10px]">npx prisma generate</code>, restart the dev server, then refresh.
        {error.message ? ` (${error.message})` : ""}
      </div>
    );
  }

  return (
    <Field className="flex min-h-0 flex-col gap-1.5 px-3.5 pb-2">
      <Label className="text-[10px] font-medium uppercase tracking-widest text-[var(--muted)]">
        Teams
      </Label>
      <Combobox
        value={selected}
        by={(a, b) => a?.abbreviation === b?.abbreviation}
        onChange={(t: TeamWithPlayers | null) => {
          if (t) onSelect(t.abbreviation);
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
              displayValue={(t: TeamWithPlayers | null) =>
                t ? `${t.abbreviation} · ${t.name}` : ""
              }
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search teams…"
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
            style={{ maxHeight: TEAM_LIST_MAX_PX }}
            className="z-[100] w-[var(--input-width)] overflow-y-auto overscroll-y-contain rounded-lg border border-[var(--border)] bg-[var(--panel)] py-1 shadow-xl outline-none empty:invisible data-[closed]:opacity-0 motion-safe:data-[closed]:translate-y-0.5 motion-safe:transition data-[enter]:duration-100 data-[leave]:duration-75 data-[enter]:ease-out data-[leave]:ease-in"
          >
            {filtered.map((t) => (
              <ComboboxOption
                key={t.abbreviation}
                value={t}
                className="group flex min-h-[48px] cursor-pointer items-center gap-2 px-2.5 py-2 text-left text-sm data-focus:bg-[rgba(108,99,255,0.14)] data-selected:bg-[rgba(108,99,255,0.1)]"
              >
                <span
                  className="size-2 shrink-0 rounded-full ring-1 ring-black/10"
                  style={{ backgroundColor: t.primaryHex }}
                />
                <span className="min-w-0 flex-1">
                  <span className="block font-semibold text-[var(--text)]">{t.abbreviation}</span>
                  <span className="block truncate text-xs text-[var(--muted)]">{t.name}</span>
                </span>
              </ComboboxOption>
            ))}
          </ComboboxOptions>
        </div>
      </Combobox>
    </Field>
  );
}
