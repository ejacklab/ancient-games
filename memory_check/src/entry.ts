// Reading one entry file's header and body: the few fields the tool's own git checks compare (K4.1, K4.3,
// W1.1a, W1.1b, W6.1a). The format clauses W1.1a, W1.1b, W1.2a, W1.3a, W4.1b and K6.3a are not judged here — they
// are `tools/memory_index.py --check`'s, and the tool runs it instead of checking them a second way (C3).

export interface Field {
  /** The value on the `key:` line, whitespace collapsed. */
  readonly value: string;
  /** The value plus every indented or `- ` continuation line under it, as one text. */
  readonly full: string;
  /** The continuation lines under the `key:` (`- ` items, or wrapped values), one per line. */
  readonly items: readonly string[];
  /** The 1-based line the `key:` is on, for evidence. */
  readonly line: number;
}

export interface Entry {
  readonly name: string;
  readonly text: string;
  readonly fields: ReadonlyMap<string, Field>;
  /** The body up to `**Why:**`, whitespace collapsed: the claim. */
  readonly claim: string;
  readonly claimLine: number;
  /** The `id:` lines at top level: more than one means more than one entry in the file (W6.1a). */
  readonly idLines: number[];
  /** The lines that are exactly `---`: more than two means more than one header block (W6.1a). */
  readonly headerBlocks: number;
  readonly headerStartLine: number;
  readonly headerEndLine: number;
}

const WHY = "**Why:**";

function squash(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

/** One pair of surrounding quotes, as memory_index.py's `unquote` strips (tools/memory_index.py:127): a header
 *  scalar written `status: "superseded"` is the status `superseded`, and comparing it unquoted is comparing what
 *  the index checker reads. */
function unquote(value: string): string {
  const first = value[0];
  return value.length >= 2 && first === value[value.length - 1] && (first === '"' || first === "'")
    ? value.slice(1, -1)
    : value;
}

const FENCE = /^\s{0,3}(`{3,}|~{3,})/;

/**
 * The lines that are exactly `---`, as line numbers. A line inside a fenced code block is the entry's own content —
 * a Markdown example of a header is not a second header (W6.1a), so fences are stepped over.
 */
function headerDelimiters(lines: readonly string[]): number[] {
  const found: number[] = [];
  let fence = "";
  for (const [index, line] of lines.entries()) {
    const marker = FENCE.exec(line);
    if (marker) {
      const token = marker[1]!;
      if (fence === "") fence = token[0]!;
      else if (token.startsWith(fence)) fence = "";
      continue;
    }
    if (fence !== "") continue;
    if (line === "---") found.push(index);
  }
  return found;
}

export function parseEntry(name: string, text: string): Entry {
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  const fences = headerDelimiters(lines);
  const start = fences[0] ?? -1;
  const end = fences[1] ?? -1;
  const fields = new Map<string, Field>();
  const idLines: number[] = [];
  if (start === 0 && end > 0) {
    let current: { key: string; value: string; parts: string[]; items: string[]; line: number } | null = null;
    const close = (): void => {
      if (current) {
        fields.set(current.key, {
          value: current.value,
          full: squash(current.parts.join(" ")),
          items: current.items,
          line: current.line,
        });
      }
      current = null;
    };
    for (let index = start + 1; index < end; index++) {
      const line = lines[index] ?? "";
      if (line.trim() === "") continue;
      const indented = /^\s/.test(line);
      if (indented || line.startsWith("- ")) {
        if (current) {
          current.parts.push(line.trim());
          current.items.push(line.trim().replace(/^-\s*/, ""));
        }
        continue;
      }
      const colon = line.indexOf(":");
      if (colon <= 0) continue;
      close();
      const key = line.slice(0, colon).trim();
      const value = unquote(line.slice(colon + 1).trim());
      current = { key, value, parts: value ? [value] : [], items: value ? [value] : [], line: index + 1 };
      if (key === "id") idLines.push(index + 1);
    }
    close();
  }
  const body = lines.slice(end >= 0 ? end + 1 : 0);
  let claim = "";
  let claimLine = (end >= 0 ? end : 0) + 2;
  for (const [offset, line] of body.entries()) {
    if (line.startsWith(WHY)) break;
    if (squash(line) !== "") {
      if (claim === "") claimLine = (end >= 0 ? end : 0) + 2 + offset;
      claim = claim === "" ? squash(line) : `${claim} ${squash(line)}`;
    }
  }
  return {
    name,
    text,
    fields,
    claim,
    claimLine,
    idLines,
    headerBlocks: Math.max(0, Math.floor(fences.length / 2)),
    headerStartLine: start + 1,
    headerEndLine: end + 1,
  };
}

export function fieldValue(entry: Entry, key: string): string {
  return entry.fields.get(key)?.full ?? "";
}

/** The id form of W1.1b, the same one tools/memory_index.py checks (`ID_FORM`, tools/memory_index.py:57). */
const ID_FORM = /\d{2}-\d{2}-[0-9a-z]{6}-\d{4}/;

/** `<prefix>-<id>-<slug>.md` (W1.1c): the prefix is the first letter, the id the W1.1b form in the name. A name
 *  with no id in it has none to compare, and that is W1.1c's (a reviewer's) to say. */
export function nameParts(name: string): { prefix: string; id: string | null } {
  return { prefix: name.slice(0, 1), id: ID_FORM.exec(name)?.[0] ?? null };
}