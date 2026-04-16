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
      className="flex w-[min(420px,44vw)] shrink-0 flex-col border-l border-[var(--border)] bg-[var(--sidebar)] shadow-[var(--shadow-float)]"
    >
      <div className="flex shrink-0 items-center gap-3 border-b border-[var(--border)] px-4 py-3">
        <div className="min-w-0 flex-1">
          <div className="ds-overline">Prompt override</div>
          <div className="font-mono-code mt-2 break-all text-xs font-medium leading-snug text-[var(--text)]">
            {promptKey}
          </div>
        </div>
        {promptData?.isCustom && (
          <span className="shrink-0 rounded-md px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-[var(--warning-fg)] [background:var(--warning-bg)]">
            Custom
          </span>
        )}
        <button
          type="button"
          onClick={onClose}
          aria-label="Close prompt editor"
          className="flex size-9 shrink-0 items-center justify-center rounded-lg border border-[var(--border)] bg-[var(--panel)] text-lg leading-none text-[var(--muted)] transition-colors hover:border-[var(--muted-faint)] hover:bg-[var(--panel-hover)] hover:text-[var(--text)]"
        >
          ×
        </button>
      </div>

      <div className="shrink-0 border-b border-[var(--border)] bg-[var(--accent-muted)] px-4 py-3">
        <div className="ds-overline mb-2">Effective generation context</div>
        <p className="text-sm font-semibold leading-relaxed text-[var(--accent)]">{resolvedSummary}</p>
      </div>

      <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-4 py-5 sm:px-5">
        <div className="ds-overline px-[var(--lane-inset)]">Sections (read-only preview; edit full prompt below)</div>
        <div className="flex flex-col gap-2 px-[var(--lane-inset)]">
          {sections.map((block, i) => (
            <details
              key={i}
              open={i < 4}
              className="overflow-hidden rounded-[var(--radius-md)] border border-[var(--border-subtle)] bg-[var(--panel)] shadow-[var(--shadow-panel)]"
            >
              <summary className="cursor-pointer list-none px-4 py-3 text-sm font-semibold text-[var(--text)] marker:hidden [&::-webkit-details-marker]:hidden">
                {sectionTitle(block, i)}
              </summary>
              <div
                className="font-mono-code whitespace-pre-wrap border-t border-[var(--border-subtle)] px-4 pb-3 pt-2 text-xs leading-relaxed text-[var(--muted)] [word-break:break-word]"
                dangerouslySetInnerHTML={{ __html: highlightPreview(block) }}
              />
            </details>
          ))}
        </div>
      </div>

      <div className="shrink-0 border-t border-[var(--border)] px-4 py-5 sm:px-5">
        <div className="ds-overline mb-2 px-[var(--lane-inset)]">Full prompt (editable)</div>
        {promptLoading ? (
          <div className="px-[var(--lane-inset)] text-sm text-[var(--muted)]">Loading…</div>
        ) : (
          <div className="ds-lane-gutter min-w-0">
            <textarea
              value={promptDraft}
              onChange={(e) => setPromptDraft(e.target.value)}
              spellCheck={false}
              className="font-mono-code ds-textarea max-h-[min(40vh,360px)] w-full text-xs [tab-size:2]"
            />
          </div>
        )}
        <div className="mt-3 flex gap-2 px-[var(--lane-inset)]">
          <button
            type="button"
            onClick={onSave}
            disabled={savePending || promptLoading}
            className="ds-btn-primary min-h-[42px] flex-1 text-sm disabled:cursor-not-allowed disabled:opacity-60"
          >
            {savePending ? "Saving…" : "Save override"}
          </button>
          <button
            type="button"
            onClick={onReset}
            disabled={resetPending || promptLoading || !promptData?.isCustom}
            className={`min-h-[42px] flex-1 rounded-[var(--radius-md)] border border-[var(--border)] bg-[var(--panel)] px-3 py-2 text-sm font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${
              promptData?.isCustom ? "text-[var(--danger)] hover:bg-[var(--panel-hover)]" : "text-[var(--muted)]"
            }`}
          >
            {resetPending ? "Resetting…" : "Reset"}
          </button>
        </div>
        {(saveSuccess || resetSuccess) && (
          <div className="mt-3 px-[var(--lane-inset)] text-sm font-medium text-[var(--success)]">
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

function highlightPreview(text: string): string {
  const esc = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return esc
    .replace(/(#[0-9]{1,2}\b)/g, '<span style="color:#a5b4fc;font-weight:700">$1</span>')
    .replace(
      /(\bTEAM:|\bJERSEY:|\bHELMET:|\bPANTS:|\bNUMBER:|\bPOSE:|\bFACING:|\bBALL:)/g,
      '<span style="color:#86efac;font-weight:700">$1</span>',
    )
    .replace(/(\b[A-Z][A-Z\s]{2,20}:)/g, '<span style="color:#fcd34d;font-weight:600">$1</span>');
}
