"use client";

import { useState, useEffect, useMemo, useCallback } from "react";
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

  const [selectedAbbr, setSelectedAbbr]     = useState("DAL");
  const [tab, setTab]                        = useState<Tab>("player");
  const [model, setModel]                    = useState<ModelTier>("flash");
  const [status, setStatus]                  = useState<Status>("idle");
  const [genError, setGenError]              = useState("");
  const [assets, setAssets]                  = useState<GeneratedAsset[]>([]);
  const [previewAsset, setPreviewAsset]      = useState<GeneratedAsset | null>(null);

  const [side, setSide]                      = useState<Side>("left");
  const [playerOverride, setPlayerOverride]  = useState("");
  const [numberOverride, setNumberOverride]  = useState("");
  const [poseOverride, setPoseOverride]      = useState("");
  const [ballOverride, setBallOverride]      = useState<"auto" | "yes" | "no">("auto");

  const [promptDraft, setPromptDraft]        = useState("");
  const [promptInspectorOpen, setPromptInspectorOpen] = useState(false);

  const {
    data: teams = [],
    isError: teamsError,
    error: teamsQueryError,
    isPending: teamsLoading,
  } = useQuery<TeamWithPlayers[]>({
    queryKey: ["teams", "nfl"],
    queryFn:  () => getTeams("nfl"),
    staleTime: Infinity,
  });

  const team = teams.find((t) => t.abbreviation === selectedAbbr) ?? teams[0];

  const leftDefault  = team?.cardPlayers.find((p) => p.side === "left");
  const rightDefault = team?.cardPlayers.find((p) => p.side === "right");

  const promptKey =
    tab === "background"
      ? `background:${selectedAbbr}`
      : `player:${selectedAbbr}:${side}`;

  const { data: promptData, isLoading: promptLoading } = useQuery({
    queryKey: ["prompt", promptKey],
    queryFn: () => getPrompt(promptKey),
    enabled: promptInspectorOpen,
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
          team: selectedAbbr, side, model,
          ...(playerOverride.trim() ? { player: playerOverride.trim() } : {}),
          ...(numberOverride.trim() ? { number: numberOverride.trim() } : {}),
          ...(poseOverride.trim()   ? { pose: poseOverride.trim() }     : {}),
          ...(ballOverride !== "auto" ? { ball: ballOverride }           : {}),
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

  const editPromptBtnStyle: React.CSSProperties = {
    width: "100%",
    padding: "8px 10px",
    borderRadius: 8,
    border: "1px solid var(--border)",
    background: "var(--panel)",
    color: "var(--text)",
    fontWeight: 600,
    fontSize: 12,
    cursor: "pointer",
    textAlign: "left",
  };

  return (
    <div className="flex h-screen overflow-hidden">

      <aside style={{ background: "var(--sidebar)", borderRight: "1px solid var(--border)", width: 236, flexShrink: 0 }} className="flex flex-col">
        <div style={{ padding: "18px 14px 10px", borderBottom: "1px solid var(--border)" }}>
          <div style={{ fontWeight: 800, fontSize: 17, letterSpacing: "-0.03em" }}>UPTOWNS</div>
          <div style={{ fontSize: 10, color: "var(--muted)", marginTop: 2, letterSpacing: "0.08em", textTransform: "uppercase" }}>Card Generator</div>
        </div>

        <div style={{ padding: "10px 14px 6px" }}>
          <div style={{ fontSize: 10, color: "var(--muted)", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 6 }}>Sport</div>
          <button style={{ background: "var(--accent)", color: "#fff", border: "none", borderRadius: 6, padding: "5px 12px", fontSize: 12, fontWeight: 700, cursor: "pointer", width: "100%" }}>NFL</button>
        </div>

        <div className="min-h-0 flex-1 border-t border-[var(--border)] pt-2">
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
      </aside>

      <main style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", minWidth: 0 }}>

        <header style={{ height: 52, display: "flex", alignItems: "center", gap: 12, padding: "0 20px", borderBottom: "1px solid var(--border)", flexShrink: 0 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: team?.primaryHex ?? "#666" }} />
          <span style={{ fontWeight: 700, fontSize: 15 }}>{team?.name ?? "…"}</span>
          <span style={{ color: "var(--muted)", fontSize: 12 }}>{team?.stadiumName}</span>
          <div style={{ marginLeft: "auto", display: "flex", gap: 6, alignItems: "center" }}>
            <ModelToggle value={model} onChange={setModel} />
          </div>
        </header>

        <div style={{ flex: 1, display: "flex", overflow: "hidden", minHeight: 0 }}>

          <div style={{ width: 270, flexShrink: 0, borderRight: "1px solid var(--border)", display: "flex", flexDirection: "column" }}>
            <div style={{ display: "flex", borderBottom: "1px solid var(--border)" }}>
              {(["player", "background"] as Tab[]).map((t) => (
                <button key={t} onClick={() => setTab(t)} style={{
                  flex: 1, padding: "10px 0", border: "none", cursor: "pointer", fontSize: 11, fontWeight: 600,
                  background: tab === t ? "var(--panel)" : "transparent",
                  color: tab === t ? "var(--text)" : "var(--muted)",
                  borderBottom: tab === t ? "2px solid var(--accent)" : "2px solid transparent",
                  textTransform: "capitalize",
                }}>
                  {t}
                </button>
              ))}
            </div>

            <div style={{ flex: 1, overflowY: "auto", padding: 14, display: "flex", flexDirection: "column", gap: 14 }}>

              {tab === "player" && (
                <>
                  <button type="button" onClick={() => setPromptInspectorOpen(true)} style={editPromptBtnStyle}>
                    Edit prompt for this slot…
                  </button>

                  <div>
                    <Label>Slot</Label>
                    <div style={{ display: "flex", gap: 6, marginTop: 5 }}>
                      {(["left", "right"] as Side[]).map((s) => (
                        <ToggleBtn key={s} active={side === s} onClick={() => setSide(s)}>
                          {s === "left" ? "← Left" : "Right →"}
                        </ToggleBtn>
                      ))}
                    </div>
                  </div>

                  <InfoCard>
                    <div style={{ fontSize: 10, color: "var(--muted)", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.08em" }}>Default {side} player</div>
                    {(side === "left" ? leftDefault : rightDefault) ? (
                      <>
                        <div style={{ fontWeight: 700, fontSize: 13 }}>{(side === "left" ? leftDefault : rightDefault)?.name}</div>
                        <div style={{ color: "var(--muted)", fontSize: 11, marginTop: 2 }}>
                          #{(side === "left" ? leftDefault : rightDefault)?.number} · {(side === "left" ? leftDefault : rightDefault)?.position?.toUpperCase()} · {(side === "left" ? leftDefault : rightDefault)?.pose ?? "auto"}
                        </div>
                      </>
                    ) : (
                      <div style={{ color: "var(--muted)", fontSize: 12 }}>No default set</div>
                    )}
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

                  <div>
                    <Label>Override Player Name</Label>
                    <Input value={playerOverride} onChange={setPlayerOverride} placeholder="e.g. CeeDee Lamb" />
                  </div>
                  <div>
                    <Label>Override Jersey #</Label>
                    <Input value={numberOverride} onChange={setNumberOverride} placeholder="e.g. 88" />
                  </div>
                  <div>
                    <Label>Pose</Label>
                    <select value={poseOverride} onChange={(e) => setPoseOverride(e.target.value)} style={{ ...inputStyle, cursor: "pointer" }}>
                      <option value="">auto</option>
                      {POSES.map((p) => <option key={p} value={p}>{p}</option>)}
                    </select>
                  </div>
                  <div>
                    <Label>Ball</Label>
                    <div style={{ display: "flex", gap: 5, marginTop: 5 }}>
                      {(["auto", "yes", "no"] as const).map((b) => (
                        <ToggleBtn key={b} active={ballOverride === b} onClick={() => setBallOverride(b)}>{b}</ToggleBtn>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {tab === "background" && (
                <>
                  <button type="button" onClick={() => setPromptInspectorOpen(true)} style={editPromptBtnStyle}>
                    Edit background prompt…
                  </button>
                  <InfoCard>
                    <div style={{ fontWeight: 600, color: "var(--text)", marginBottom: 4, fontSize: 13 }}>Background Plate</div>
                    <div style={{ color: "var(--muted)", fontSize: 12, lineHeight: 1.5 }}>
                      Stadium + skyline + sky floating island on chroma green. Sandwich layout applied automatically.
                    </div>
                  </InfoCard>
                </>
              )}
            </div>

            <div style={{ padding: 14, borderTop: "1px solid var(--border)" }}>
              <button onClick={generate} disabled={isGenerating} style={{ width: "100%", padding: "11px 0", border: "none", borderRadius: 8, background: isGenerating ? "var(--border)" : "var(--accent)", color: isGenerating ? "var(--muted)" : "#fff", fontWeight: 700, fontSize: 13, cursor: isGenerating ? "not-allowed" : "pointer" }}>
                {isGenerating ? "Generating…" : `Generate ${tab === "background" ? "Background" : "Player"}`}
              </button>
              {status === "error" && <div style={{ marginTop: 8, color: "var(--danger)", fontSize: 11 }}>{genError}</div>}
            </div>
          </div>

          <div style={{ flex: 1, display: "flex", flexDirection: "column", overflow: "hidden", minWidth: 0 }}>
            <div
              role="presentation"
              onClick={() => { if (promptInspectorOpen) closePromptInspector(); }}
              style={{
                flex: 1,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: previewAsset ? "#0d0d14" : "var(--panel)",
                position: "relative",
                overflow: "hidden",
                cursor: promptInspectorOpen ? "zoom-out" : "default",
              }}
            >
              {!previewAsset && !isGenerating && (
                <div style={{ textAlign: "center", color: "var(--muted)", pointerEvents: "none" }}>
                  <div style={{ fontSize: 40, marginBottom: 10, opacity: 0.25 }}>🏟</div>
                  <div style={{ fontSize: 14, fontWeight: 600, color: "var(--text)" }}>No asset yet</div>
                  <div style={{ fontSize: 12, marginTop: 3 }}>
                    {promptInspectorOpen ? "Click here to close prompt editor" : "Configure and hit Generate"}
                  </div>
                </div>
              )}
              {previewAsset && (
                <>
                  <img src={previewAsset.dataUrl} alt={previewAsset.label} style={{ maxWidth: "100%", maxHeight: "100%", objectFit: "contain", pointerEvents: "none" }} />
                  <div style={{ position: "absolute", bottom: 10, right: 10, background: "rgba(0,0,0,0.7)", borderRadius: 5, padding: "3px 8px", fontSize: 10, color: "#999", pointerEvents: "none" }}>
                    {previewAsset.path}
                  </div>
                </>
              )}
              {isGenerating && (
                <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", background: "rgba(0,0,0,0.65)", gap: 10 }}>
                  <Spinner />
                  <div style={{ color: "#fff", fontSize: 13, fontWeight: 600 }}>Gemini {model === "pro" ? "3 Pro" : "2.5 Flash"} generating…</div>
                  <div style={{ color: "var(--muted)", fontSize: 11 }}>30–90 seconds</div>
                </div>
              )}
            </div>

            <div style={{ borderTop: "1px solid var(--border)", background: "var(--sidebar)" }} onClick={(e) => e.stopPropagation()}>
              {assets.length > 0 && (
                <div style={{ display: "flex", gap: 6, padding: "8px 10px", overflowX: "auto", alignItems: "center", borderBottom: "1px solid var(--border)" }}>
                  <div style={{ fontSize: 10, color: "var(--muted)", flexShrink: 0, textTransform: "uppercase", letterSpacing: "0.06em" }}>Session</div>
                  {assets.map((a, i) => (
                    <button key={i} type="button" onClick={() => setPreviewAsset(a)} style={{ flexShrink: 0, height: 60, width: 60, border: `2px solid ${previewAsset === a ? "var(--accent)" : "var(--border)"}`, borderRadius: 5, overflow: "hidden", cursor: "pointer", padding: 0, background: "#000" }}>
                      <img src={a.dataUrl} alt={a.label} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
                    </button>
                  ))}
                </div>
              )}

              {history && history.length > 0 && (
                <div style={{ padding: "8px 12px", maxHeight: 100, overflowY: "auto" }}>
                  <div style={{ fontSize: 10, color: "var(--muted)", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 4 }}>
                    DB History ({history.length})
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
                    {history.slice(0, 8).map((g) => (
                      <div key={g.id} style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "var(--muted)" }}>
                        <span>
                          {g.type === "player" ? `${g.playerName ?? "?"} #${g.number ?? "?"} (${g.side})` : `${g.team} background`}
                        </span>
                        <span style={{ color: "var(--accent)", fontWeight: 600 }}>{g.model}</span>
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
  );
}

function Label({ children }: { children: React.ReactNode }) {
  return <div style={{ fontSize: 10, color: "var(--muted)", letterSpacing: "0.08em", textTransform: "uppercase" }}>{children}</div>;
}

function InfoCard({ children }: { children: React.ReactNode }) {
  return <div style={{ background: "var(--panel)", border: "1px solid var(--border)", borderRadius: 7, padding: 11 }}>{children}</div>;
}

function ToggleBtn({ active, onClick, children }: { active: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button type="button" onClick={onClick} style={{
      flex: 1, padding: "6px 0", border: `1px solid ${active ? "var(--accent)" : "var(--border)"}`,
      borderRadius: 6, cursor: "pointer", background: active ? "rgba(108,99,255,0.2)" : "transparent",
      color: active ? "var(--accent)" : "var(--muted)", fontWeight: 600, fontSize: 12,
    }}>
      {children}
    </button>
  );
}

function Input({ value, onChange, placeholder }: { value: string; onChange: (v: string) => void; placeholder?: string }) {
  return (
    <input value={value} onChange={(e) => onChange(e.target.value)} placeholder={placeholder} style={{ ...inputStyle, marginTop: 4 }} />
  );
}

function ModelToggle({ value, onChange }: { value: ModelTier; onChange: (v: ModelTier) => void }) {
  return (
    <div style={{ display: "flex", border: "1px solid var(--border)", borderRadius: 6, overflow: "hidden", fontSize: 11 }}>
      {(["flash", "pro"] as ModelTier[]).map((m) => (
        <button type="button" key={m} onClick={() => onChange(m)} style={{
          padding: "4px 11px", border: "none", cursor: "pointer", fontWeight: 700,
          background: value === m ? "var(--accent)" : "transparent",
          color: value === m ? "#fff" : "var(--muted)",
        }}>
          {m === "flash" ? "Flash" : "Pro"}
        </button>
      ))}
    </div>
  );
}

function Spinner() {
  return (
    <div style={{ width: 32, height: 32, borderRadius: "50%", border: "3px solid rgba(255,255,255,0.1)", borderTop: "3px solid var(--accent)", animation: "spin 0.8s linear infinite" }} />
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%", padding: "7px 9px", background: "var(--panel)",
  border: "1px solid var(--border)", borderRadius: 6, color: "var(--text)",
  fontSize: 12, outline: "none",
};

const POSES = [
  "throwing", "scrambling", "rushing", "route", "jump_catch", "catching",
  "stiff_arm", "hurdle", "speed_rush", "bull_rush", "pass_rush",
  "linebacker", "coverage", "press_coverage", "kicking", "celebration", "athletic",
];
