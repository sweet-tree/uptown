"use client";

import { useState, useEffect, useMemo, useCallback } from "react";
import { signOut, useSession } from "next-auth/react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { buildPlayerPrompt, buildBackgroundPrompt } from "@/lib/prompt-engine";
import { getPrompt, setPrompt, deletePrompt, getGenerations } from "@/app/actions/prompts";
import { getTeams } from "@/app/actions/teams";
import type { TeamWithPlayers } from "@/lib/types";
import { PromptInspector } from "@/components/prompt-inspector";
import { TeamPicker } from "@/components/team-picker";
import { RosterCombobox } from "@/components/roster-combobox";

type Tab = "player" | "background";
type Side = "left" | "right";
type ModelTier = "flash" | "pro";
type Status = "idle" | "loading" | "done" | "error";

interface GeneratedAsset {
  dataUrl: string;
  label: string;
  path: string;
}

export default function Dashboard() {
  const qc = useQueryClient();
  const { data: session, status: sessionStatus } = useSession();

  const [selectedAbbr, setSelectedAbbr] = useState("DAL");
  const [tab, setTab] = useState<Tab>("player");
  const [model, setModel] = useState<ModelTier>("flash");
  const [status, setStatus] = useState<Status>("idle");
  const [genError, setGenError] = useState("");
  const [assets, setAssets] = useState<GeneratedAsset[]>([]);
  const [previewAsset, setPreviewAsset] = useState<GeneratedAsset | null>(null);

  const [side, setSide] = useState<Side>("left");
  const [playerOverride, setPlayerOverride] = useState("");
  const [numberOverride, setNumberOverride] = useState("");
  const [poseOverride, setPoseOverride] = useState("");
  const [ballOverride, setBallOverride] = useState<"auto" | "yes" | "no">("auto");

  const [promptDraft, setPromptDraft] = useState("");
  const [promptInspectorOpen, setPromptInspectorOpen] = useState(false);

  const {
    data: teams = [],
    isError: teamsError,
    error: teamsQueryError,
    isPending: teamsLoading,
  } = useQuery<TeamWithPlayers[]>({
    queryKey: ["teams", "nfl"],
    queryFn: () => getTeams("nfl"),
    staleTime: Infinity,
    // Avoid calling server actions before session is known — `redirect()` from
    // `requireUser()` during a prefetch/RSC path can surface as a 500 on Vercel.
    enabled: sessionStatus === "authenticated",
  });

  const team = teams.find((t) => t.abbreviation === selectedAbbr) ?? teams[0];

  const leftDefault = team?.cardPlayers.find((p) => p.side === "left");
  const rightDefault = team?.cardPlayers.find((p) => p.side === "right");

  const promptKey =
    tab === "background" ? `background:${selectedAbbr}` : `player:${selectedAbbr}:${side}`;

  const { data: promptData, isLoading: promptLoading } = useQuery({
    queryKey: ["prompt", promptKey],
    queryFn: () => getPrompt(promptKey),
    enabled: promptInspectorOpen && sessionStatus === "authenticated",
  });

  const saveMutation = useMutation({
    mutationFn: (text: string) => setPrompt(promptKey, text),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["prompt", promptKey] }),
  });

  const resetMutation = useMutation({
    mutationFn: () => deletePrompt(promptKey),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["prompt", promptKey] });
      if (!team) return;
      const spec = team?.cardPlayers.find((p) => p.side === side);
      const defaultText = promptKey.startsWith("background")
        ? buildBackgroundPrompt(team)
        : buildPlayerPrompt(
            team,
            spec?.name ?? "Player",
            spec?.number ?? "0",
            spec?.position ?? "qb",
            side,
            spec?.pose ?? "auto",
            spec?.ball ?? "auto",
          );
      setPromptDraft(defaultText);
    },
  });

  const closePromptInspector = useCallback(() => {
    if (promptData && promptDraft !== promptData.text) {
      if (!window.confirm("Discard changes to this prompt?")) return;
    }
    saveMutation.reset();
    resetMutation.reset();
    setPromptInspectorOpen(false);
  }, [promptData, promptDraft, saveMutation, resetMutation]);

  useEffect(() => {
    if (!promptInspectorOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        closePromptInspector();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [promptInspectorOpen, closePromptInspector]);

  useEffect(() => {
    if (!promptInspectorOpen || promptLoading) return;
    if (promptData) setPromptDraft(promptData.text);
  }, [promptInspectorOpen, promptKey, promptData, promptLoading]);

  const { data: history } = useQuery({
    queryKey: ["generations", selectedAbbr],
    queryFn: () => getGenerations(selectedAbbr),
    enabled: sessionStatus === "authenticated",
  });

  const resolvedSummary = useMemo(() => {
    if (!team) return "—";
    if (tab === "background") {
      return `Background plate · ${team.name} (${selectedAbbr})`;
    }
    const spec = team.cardPlayers.find((p) => p.side === side);
    const name = playerOverride.trim() || spec?.name || "Player";
    const num = numberOverride.trim() || spec?.number || "0";
    const pos = (spec?.position || "qb").toUpperCase();
    const pose = poseOverride.trim() || spec?.pose || "auto";
    const ball = ballOverride !== "auto" ? ballOverride : (spec?.ball ?? "auto");
    return `${name} · #${num} · ${pos} · pose ${pose} · ball ${ball} · ${side} slot · ${selectedAbbr}`;
  }, [team, tab, side, selectedAbbr, playerOverride, numberOverride, poseOverride, ballOverride]);

  async function generate() {
    setStatus("loading");
    setGenError("");
    try {
      let res: Response;
      if (tab === "background") {
        res = await fetch("/api/generate/background", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ team: selectedAbbr, model }),
        });
      } else {
        const payload: Record<string, string> = {
          team: selectedAbbr,
          side,
          model,
          ...(playerOverride.trim() ? { player: playerOverride.trim() } : {}),
          ...(numberOverride.trim() ? { number: numberOverride.trim() } : {}),
          ...(poseOverride.trim() ? { pose: poseOverride.trim() } : {}),
          ...(ballOverride !== "auto" ? { ball: ballOverride } : {}),
        };
        res = await fetch("/api/generate/player", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
      }

      const data = await res.json();
      if (!data.ok) throw new Error(data.error ?? "Unknown error");

      const label =
        tab === "background"
          ? `${selectedAbbr} BG`
          : `${(data.player ?? playerOverride) || side} #${data.number ?? numberOverride}`;

      const asset: GeneratedAsset = { dataUrl: data.dataUrl, label, path: data.path };
      setAssets((prev) => [asset, ...prev]);
      setPreviewAsset(asset);
      setStatus("done");
      qc.invalidateQueries({ queryKey: ["generations", selectedAbbr] });
    } catch (err) {
      setGenError(err instanceof Error ? err.message : String(err));
      setStatus("error");
    }
  }

  const isGenerating = status === "loading";

  return (
    <div className="box-border flex h-dvh min-h-0 overflow-hidden bg-[#050506] p-2 sm:p-3">
      <div className="flex min-h-0 min-w-0 flex-1 overflow-hidden rounded-2xl border border-[var(--border)] shadow-[0_24px_80px_rgba(0,0,0,0.55)]">
      <aside className="flex w-[292px] shrink-0 flex-col border-r border-[var(--border)] bg-[var(--sidebar)]">
        <div className="border-b border-[var(--border)] px-5 pb-4 pt-5">
          <div className="ds-aside-stack">
            <div className="ds-brand-title">UPTOWNS</div>
            <div className="ds-brand-sub">Card generator</div>
          </div>
          {session?.user ? (
            <div className="mt-3 flex min-w-0 items-center justify-between gap-2 border-t border-[var(--border-subtle)] pt-3">
              <span className="min-w-0 truncate text-[var(--text-xs)] text-[var(--text-secondary)]">
                {session.user.email}
              </span>
              <button
                type="button"
                className="ds-btn-secondary ds-btn-toolbar shrink-0"
                onClick={() => void signOut({ callbackUrl: "/login" })}
              >
                Sign out
              </button>
            </div>
          ) : null}
        </div>

        <div className="border-b border-[var(--border)] px-5 pb-4 pt-4">
          <div className="ds-aside-stack flex flex-col gap-2">
            <div className="ds-overline">Sport</div>
            <button
              type="button"
              className="w-full rounded-[var(--radius-md)] bg-[var(--accent)] px-4 py-2 text-sm font-bold tracking-wide text-white shadow-[0_1px_0_rgba(255,255,255,0.1)_inset] transition-[filter] hover:brightness-110"
            >
              NFL
            </button>
          </div>
        </div>

        <div className="flex min-h-0 flex-1 flex-col px-5 pb-5 pt-4">
          <div className="ds-aside-stack flex min-h-0 flex-1 flex-col">
            <TeamPicker
              teams={teams}
              selectedAbbr={selectedAbbr}
              onSelect={setSelectedAbbr}
              loading={teamsLoading}
              error={
                teamsError
                  ? teamsQueryError instanceof Error
                    ? teamsQueryError
                    : new Error(teamsQueryError != null ? String(teamsQueryError) : "Failed to load teams")
                  : null
              }
            />
          </div>
        </div>
      </aside>

      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="flex min-h-[3.5rem] shrink-0 items-center gap-3 border-b border-[var(--border)] px-6 py-3">
          <span
            className="size-2.5 shrink-0 rounded-full ring-2 ring-[var(--border)]"
            style={{ backgroundColor: team?.primaryHex ?? "#666" }}
            aria-hidden
          />
          <div className="flex min-w-0 flex-col gap-0.5 sm:flex-row sm:items-baseline sm:gap-3">
            <span className="truncate text-lg font-bold tracking-tight text-[var(--text)]">
              {team?.name ?? "…"}
            </span>
            <span className="truncate text-sm font-medium text-[var(--muted)]">{team?.stadiumName}</span>
          </div>
          <div className="ml-auto">
            <ModelToggle value={model} onChange={setModel} />
          </div>
        </header>

        <div className="flex min-h-0 min-w-0 flex-1 overflow-hidden">
          <div className="flex w-[min(360px,36vw)] min-w-[300px] max-w-[400px] shrink-0 flex-col border-r border-[var(--border)] bg-[var(--sidebar)]">
            <div className="flex shrink-0 border-b border-[var(--border)] px-5 pb-2 pt-4">
              {(["player", "background"] as Tab[]).map((t) => (
                <button
                  key={t}
                  type="button"
                  data-active={tab === t ? "true" : "false"}
                  onClick={() => setTab(t)}
                  className="ds-tab"
                >
                  {t}
                </button>
              ))}
            </div>

            <div className="ds-form-stack flex min-h-0 flex-1 flex-col overflow-y-auto px-5 py-6">
              {tab === "player" && (
                <>
                  <div className="ds-soft-panel ds-lane-gutter">
                    <div className="flex flex-col gap-6">
                      <div className="ds-field">
                        <Label>Slot</Label>
                        <div className="flex gap-2">
                          {(["left", "right"] as Side[]).map((s) => (
                            <ToggleBtn key={s} active={side === s} onClick={() => setSide(s)}>
                              {s === "left" ? "← Left" : "Right →"}
                            </ToggleBtn>
                          ))}
                        </div>
                      </div>

                      <InfoCard>
                        <div className="ds-field">
                          <div className="ds-overline">Default {side} player</div>
                          {(side === "left" ? leftDefault : rightDefault) ? (
                            <div className="space-y-1">
                              <div className="text-base font-bold leading-snug text-[var(--text)]">
                                {(side === "left" ? leftDefault : rightDefault)?.name}
                              </div>
                              <div className="text-sm leading-relaxed text-[var(--muted)]">
                                #{(side === "left" ? leftDefault : rightDefault)?.number} ·{" "}
                                {(side === "left" ? leftDefault : rightDefault)?.position?.toUpperCase()} ·{" "}
                                {(side === "left" ? leftDefault : rightDefault)?.pose ?? "auto"}
                              </div>
                            </div>
                          ) : (
                            <div className="text-sm text-[var(--muted)]">No default set</div>
                          )}
                        </div>
                      </InfoCard>

                      {(team?.rosterEntries?.length ?? 0) > 0 && team && (
                        <RosterCombobox
                          entries={team.rosterEntries}
                          cardPlayers={team.cardPlayers}
                          onPick={(r, slotSide) => {
                            setPlayerOverride(r.name);
                            setNumberOverride(r.number);
                            setSide(slotSide);
                          }}
                        />
                      )}
                    </div>
                  </div>

                  <div className="ds-soft-panel ds-lane-gutter">
                    <div className="flex flex-col gap-6">
                      <div className="ds-field">
                        <Label>Override player name</Label>
                        <Input value={playerOverride} onChange={setPlayerOverride} placeholder="e.g. CeeDee Lamb" />
                      </div>
                      <div className="ds-field">
                        <Label>Override jersey #</Label>
                        <Input value={numberOverride} onChange={setNumberOverride} placeholder="e.g. 88" />
                      </div>
                      <div className="ds-field">
                        <Label>Pose</Label>
                        <select
                          value={poseOverride}
                          onChange={(e) => setPoseOverride(e.target.value)}
                          className="ds-select"
                        >
                          <option value="">auto</option>
                          {POSES.map((p) => (
                            <option key={p} value={p}>
                              {p}
                            </option>
                          ))}
                        </select>
                      </div>
                      <div className="ds-field">
                        <Label>Ball</Label>
                        <div className="flex gap-2">
                          {(["auto", "yes", "no"] as const).map((b) => (
                            <ToggleBtn key={b} active={ballOverride === b} onClick={() => setBallOverride(b)}>
                              {b}
                            </ToggleBtn>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {tab === "background" && (
                <>
                  <div className="ds-soft-panel ds-lane-gutter">
                    <InfoCard className="border-0 bg-transparent p-0 shadow-none">
                      <div className="mb-2 text-base font-semibold text-[var(--text)]">Background plate</div>
                      <p className="text-sm leading-relaxed text-[var(--muted)]">
                        Stadium + skyline + sky floating island on chroma green. Sandwich layout applied automatically.
                      </p>
                    </InfoCard>
                  </div>
                </>
              )}
            </div>

            <div className="shrink-0 border-t border-[var(--border)] bg-[var(--bg-elevated)] px-5 py-4 shadow-[0_-1px_0_rgba(255,255,255,0.04)_inset]">
              <div className="ds-lane-gutter ds-footer-actions">
                <button
                  type="button"
                  className="ds-btn-secondary ds-btn-toolbar min-w-0"
                  onClick={() => setPromptInspectorOpen(true)}
                >
                  Edit prompt
                </button>
                <button
                  type="button"
                  className="ds-btn-primary ds-btn-toolbar min-w-0"
                  onClick={generate}
                  disabled={isGenerating}
                >
                  {isGenerating ? "Generating…" : `Generate ${tab === "background" ? "background" : "player"}`}
                </button>
              </div>
              {status === "error" && (
                <div className="ds-lane-gutter mt-3 text-sm font-medium leading-snug text-[var(--danger)]">
                  {genError}
                </div>
              )}
            </div>
          </div>

          <div className="flex min-w-0 flex-1 flex-col overflow-hidden">
            <div
              role="presentation"
              onClick={() => {
                if (promptInspectorOpen) closePromptInspector();
              }}
              className={`relative flex flex-1 items-center justify-center overflow-hidden p-5 sm:p-6 ${
                previewAsset ? "bg-[var(--preview-bg)]" : "bg-[var(--panel)]"
              } ${promptInspectorOpen ? "cursor-zoom-out" : "cursor-default"}`}
            >
              {!previewAsset && !isGenerating && (
                <div className="pointer-events-none max-w-md px-8 py-6 text-center">
                  <div className="mb-2 text-5xl opacity-[0.18]">🏟</div>
                  <div className="text-base font-semibold text-[var(--text)]">No asset yet</div>
                  <p className="mt-2 text-sm leading-relaxed text-[var(--muted)]">
                    {promptInspectorOpen ? "Click here to close the prompt editor" : "Configure controls and generate"}
                  </p>
                </div>
              )}
              {previewAsset && (
                <>
                  {/* eslint-disable-next-line @next/next/no-img-element -- data URL preview */}
                  <img
                    src={previewAsset.dataUrl}
                    alt={previewAsset.label}
                    className="max-h-full max-w-full object-contain p-4"
                  />
                  <div className="pointer-events-none absolute bottom-4 right-4 rounded-md bg-black/75 px-2.5 py-1 font-mono text-xs text-[var(--muted)]">
                    {previewAsset.path}
                  </div>
                </>
              )}
              {isGenerating && (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-black/70 backdrop-blur-[2px]">
                  <Spinner />
                  <div className="text-base font-semibold text-white">
                    Gemini {model === "pro" ? "3 Pro" : "2.5 Flash"} generating…
                  </div>
                  <div className="text-sm text-[var(--muted)]">Usually 30–90 seconds</div>
                </div>
              )}
            </div>

            <div
              className="shrink-0 border-t border-[var(--border)] bg-[var(--sidebar)]"
              onClick={(e) => e.stopPropagation()}
            >
              {assets.length > 0 && (
                <div className="flex items-center gap-2 overflow-x-auto border-b border-[var(--border)] px-5 py-3">
                  <div className="ds-overline shrink-0 pr-1">Session</div>
                  {assets.map((a, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => setPreviewAsset(a)}
                      className={`h-14 w-14 shrink-0 overflow-hidden rounded-lg border-2 bg-black p-0 transition-colors ${
                        previewAsset === a ? "border-[var(--accent)]" : "border-[var(--border)] hover:border-[var(--muted-faint)]"
                      }`}
                    >
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={a.dataUrl} alt={a.label} className="size-full object-cover" />
                    </button>
                  ))}
                </div>
              )}

              {history && history.length > 0 && (
                <div className="max-h-[120px] overflow-y-auto px-5 py-3">
                  <div className="ds-overline mb-2">DB history ({history.length})</div>
                  <div className="flex flex-col gap-2">
                    {history.slice(0, 8).map((g) => (
                      <div
                        key={g.id}
                        className="flex items-start justify-between gap-3 rounded-md bg-[var(--panel)] px-3 py-3 text-sm leading-snug text-[var(--muted)] ring-1 ring-[var(--border-subtle)]"
                      >
                        <span className="min-w-0 flex-1">
                          {g.type === "player"
                            ? `${g.playerName ?? "?"} #${g.number ?? "?"} (${g.side})`
                            : `${g.team} background`}
                        </span>
                        <span className="shrink-0 font-semibold text-[var(--accent)]">{g.model}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {promptInspectorOpen && (
            <PromptInspector
              promptKey={promptKey}
              promptDraft={promptDraft}
              setPromptDraft={setPromptDraft}
              promptData={promptData}
              promptLoading={promptLoading}
              resolvedSummary={resolvedSummary}
              savePending={saveMutation.isPending}
              resetPending={resetMutation.isPending}
              saveSuccess={saveMutation.isSuccess}
              resetSuccess={resetMutation.isSuccess}
              onSave={() => saveMutation.mutate(promptDraft)}
              onReset={() => resetMutation.mutate()}
              onClose={closePromptInspector}
            />
          )}
        </div>
      </main>
      </div>
    </div>
  );
}

function Label({ children }: { children: React.ReactNode }) {
  return <div className="ds-overline">{children}</div>;
}

function InfoCard({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <div className={["ds-panel-card p-5", className].filter(Boolean).join(" ")}>{children}</div>;
}

function ToggleBtn({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button type="button" data-active={active ? "true" : "false"} onClick={onClick} className="ds-toggle">
      {children}
    </button>
  );
}

function Input({
  value,
  onChange,
  placeholder,
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
}) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="ds-input"
    />
  );
}

function ModelToggle({ value, onChange }: { value: ModelTier; onChange: (v: ModelTier) => void }) {
  return (
    <div className="ds-model-toggle">
      {(["flash", "pro"] as ModelTier[]).map((m) => (
        <button key={m} type="button" data-on={value === m ? "true" : "false"} onClick={() => onChange(m)}>
          {m === "flash" ? "Flash" : "Pro"}
        </button>
      ))}
    </div>
  );
}

function Spinner() {
  return <div className="ds-spinner" aria-hidden />;
}

const POSES = [
  "throwing",
  "scrambling",
  "rushing",
  "route",
  "jump_catch",
  "catching",
  "stiff_arm",
  "hurdle",
  "speed_rush",
  "bull_rush",
  "pass_rush",
  "linebacker",
  "coverage",
  "press_coverage",
  "kicking",
  "celebration",
  "athletic",
];
