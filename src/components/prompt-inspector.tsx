"use client";

import { splitPromptSections } from "@/lib/prompt-sections";

export interface PromptInspectorProps {
  promptKey: string;
  promptDraft: string;
  setPromptDraft: (v: string) => void;
  promptData: { text: string; isCustom: boolean } | undefined;
  promptLoading: boolean;
  resolvedSummary: string;
  savePending: boolean;
  resetPending: boolean;
  saveSuccess: boolean;
  resetSuccess: boolean;
  onSave: () => void;
  onReset: () => void;
  onClose: () => void;
}

export function PromptInspector({
  promptKey,
  promptDraft,
  setPromptDraft,
  promptData,
  promptLoading,
  resolvedSummary,
  savePending,
  resetPending,
  saveSuccess,
  resetSuccess,
  onSave,
  onReset,
  onClose,
}: PromptInspectorProps) {
  const sections = splitPromptSections(promptDraft);

  return (
    <aside
      className="prompt-inspector"
      style={{
        width: 400,
        maxWidth: "42vw",
        flexShrink: 0,
        display: "flex",
        flexDirection: "column",
        borderLeft: "1px solid var(--border)",
        background: "var(--sidebar)",
        boxShadow: "-8px 0 24px rgba(0,0,0,0.35)",
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "12px 14px",
          borderBottom: "1px solid var(--border)",
          flexShrink: 0,
        }}
      >
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 10, color: "var(--muted)", letterSpacing: "0.08em", textTransform: "uppercase" }}>
            Prompt override
          </div>
          <div style={{ fontSize: 11, fontFamily: "ui-monospace, monospace", color: "var(--text)", marginTop: 4, wordBreak: "break-all" }}>
            {promptKey}
          </div>
        </div>
        {promptData?.isCustom && (
          <span
            style={{
              fontSize: 10,
              fontWeight: 700,
              background: "#92400e",
              color: "#fde68a",
              padding: "3px 8px",
              borderRadius: 4,
              letterSpacing: "0.06em",
              flexShrink: 0,
            }}
          >
            CUSTOM
          </span>
        )}
        <button
          type="button"
          onClick={onClose}
          aria-label="Close prompt editor"
          style={{
            width: 32,
            height: 32,
            borderRadius: 6,
            border: "1px solid var(--border)",
            background: "var(--panel)",
            color: "var(--muted)",
            cursor: "pointer",
            fontSize: 18,
            lineHeight: 1,
            flexShrink: 0,
          }}
        >
          ×
        </button>
      </div>

      <div
        style={{
          padding: "10px 14px",
          borderBottom: "1px solid var(--border)",
          background: "rgba(108,99,255,0.08)",
          flexShrink: 0,
        }}
      >
        <div style={{ fontSize: 9, color: "var(--muted)", letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: 4 }}>
          Effective generation context
        </div>
        <div style={{ fontSize: 12, color: "var(--accent)", fontWeight: 600, lineHeight: 1.45 }}>{resolvedSummary}</div>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "10px 12px", display: "flex", flexDirection: "column", gap: 8 }}>
        <div style={{ fontSize: 10, color: "var(--muted)", letterSpacing: "0.06em", textTransform: "uppercase" }}>
          Sections (fold for readability; edits are one full prompt)
        </div>
        {sections.map((block, i) => (
          <details
            key={i}
            open={i < 4}
            style={{
              border: "1px solid var(--border)",
              borderRadius: 8,
              background: "var(--panel)",
              overflow: "hidden",
            }}
          >
            <summary
              style={{
                padding: "8px 10px",
                cursor: "pointer",
                fontSize: 11,
                fontWeight: 600,
                color: "var(--text)",
                listStyle: "none",
              }}
            >
              {sectionTitle(block, i)}
            </summary>
            <div
              style={{
                margin: 0,
                padding: "0 10px 10px",
                fontSize: 10,
                lineHeight: 1.55,
                color: "var(--muted)",
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
                fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
                borderTop: "1px solid var(--border)",
              }}
              dangerouslySetInnerHTML={{ __html: highlightPreview(block) }}
            />
          </details>
        ))}
      </div>

      <div style={{ padding: "10px 12px", borderTop: "1px solid var(--border)", flexShrink: 0 }}>
        <div style={{ fontSize: 10, color: "var(--muted)", marginBottom: 6, letterSpacing: "0.06em", textTransform: "uppercase" }}>
          Full prompt (editable)
        </div>
        {promptLoading ? (
          <div style={{ color: "var(--muted)", fontSize: 12 }}>Loading…</div>
        ) : (
          <textarea
            value={promptDraft}
            onChange={(e) => setPromptDraft(e.target.value)}
            spellCheck={false}
            style={{
              width: "100%",
              minHeight: 200,
              maxHeight: 320,
              resize: "vertical",
              background: "#0c0c12",
              border: "1px solid var(--border)",
              borderRadius: 8,
              color: "#e4e4ef",
              fontSize: 11,
              padding: 12,
              outline: "none",
              fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
              lineHeight: 1.55,
              tabSize: 2,
            }}
          />
        )}
        <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
          <button
            type="button"
            onClick={onSave}
            disabled={savePending || promptLoading}
            style={{
              flex: 1,
              padding: "10px 0",
              border: "none",
              borderRadius: 8,
              background: "var(--accent)",
              color: "#fff",
              fontWeight: 700,
              fontSize: 12,
              cursor: savePending || promptLoading ? "not-allowed" : "pointer",
              opacity: savePending || promptLoading ? 0.6 : 1,
            }}
          >
            {savePending ? "Saving…" : "Save override"}
          </button>
          <button
            type="button"
            onClick={onReset}
            disabled={resetPending || promptLoading || !promptData?.isCustom}
            style={{
              flex: 1,
              padding: "10px 0",
              border: "1px solid var(--border)",
              borderRadius: 8,
              background: "var(--panel)",
              color: promptData?.isCustom ? "var(--danger)" : "var(--muted)",
              fontWeight: 600,
              fontSize: 12,
              cursor: promptData?.isCustom && !resetPending ? "pointer" : "not-allowed",
            }}
          >
            {resetPending ? "Resetting…" : "Reset"}
          </button>
        </div>
        {(saveSuccess || resetSuccess) && (
          <div style={{ marginTop: 8, color: "var(--success)", fontSize: 11 }}>
            {resetSuccess ? "Restored default prompt." : "Saved to database."}
          </div>
        )}
      </div>
    </aside>
  );
}

function sectionTitle(block: string, index: number): string {
  const lines = block.split("\n").filter((l) => l.trim());
  const afterRule = lines.find((l) => !/^━/.test(l));
  if (afterRule && afterRule.length < 48) return afterRule.trim();
  return `Section ${index + 1}`;
}

/** Lightweight read-only highlights inside folded previews (escape + wrap). */
function highlightPreview(text: string): string {
  const esc = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return esc
    .replace(/(#[0-9]{1,2}\b)/g, '<span style="color:#a5b4fc;font-weight:700">$1</span>')
    .replace(/(\bTEAM:|\bJERSEY:|\bHELMET:|\bPANTS:|\bNUMBER:|\bPOSE:|\bFACING:|\bBALL:)/g, '<span style="color:#86efac;font-weight:700">$1</span>')
    .replace(/(\b[A-Z][A-Z\s]{2,20}:)/g, '<span style="color:#fcd34d;font-weight:600">$1</span>');
}
