/** Split long prompts on heavy horizontal rule lines (matches player/background prompt templates). */
export function splitPromptSections(text: string): string[] {
  const lines = text.split("\n");
  const chunks: string[][] = [];
  let cur: string[] = [];
  for (const line of lines) {
    if (/^━{12,}\s*$/.test(line)) {
      if (cur.length) chunks.push(cur);
      cur = [line];
    } else {
      cur.push(line);
    }
  }
  if (cur.length) chunks.push(cur);
  return chunks.length ? chunks.map((c) => c.join("\n")) : [text];
}
