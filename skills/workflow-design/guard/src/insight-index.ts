// Round 11 (SPEC.md; plan A Part C step 9, plan B round 2): what was learned, listed — one line per insight section
// with its ids, the failure's check, the source the whys end at, the options' kinds and its category. The index never
// prints the author's text; `show` prints whole sections, for an expert who loads them on purpose.

import * as fs from "node:fs";
import * as path from "node:path";
import { findInsightFiles, isGreatSection, parseInsight } from "./insight.ts";
import { readJournal } from "./journal.ts";
import type { InsightSection } from "./types.ts";

export interface IndexEntry {
  file: string; // root-relative
  ids: string[]; // failure ids; empty for a great section
  kind: "failure" | "great";
  checks: string[]; // the journal's check per id ("-" when the journal has no record of it)
  source: string; // the Source line's first word, or "-"
  optionKinds: string[];
  category: string; // the category id, or "-" when no rule places it
}

// A category is placed by the first rule that matches; categories are data (data/insight-categories.yaml).
export interface CategoryRule {
  id: string;
  name: string;
  sources?: string[]; // a Source first word
  checks?: string[]; // regexes over the failure's check
  kinds?: ("failure" | "great")[];
  titles?: string[]; // case-insensitive regexes over the section's heading (used to place it, never printed)
}

// The same heading rule as insight.ts, so the index and the sections it names never fall out of step (review #2).
const HEADING_RE = /^##(?!#)\s*(.*)$/;
// Only known option kinds are printed; anything else in the brackets is the author's text (review #1).
const OPTION_KINDS = new Set(["rule", "check", "tool", "config-advice"]);
const ID_RE = /F-[0-9a-f]{8}/g;

function firstWord(text: string | null): string {
  const match = text === null ? null : /^[A-Za-z-]+/.exec(text.trim());
  return match === null ? "-" : match[0];
}

// A malformed regex in the categories file matches nothing instead of breaking the index (review #3).
function matches(re: string, text: string, flags = ""): boolean {
  try {
    return new RegExp(re, flags).test(text);
  } catch {
    return false;
  }
}

export function categorize(entry: Omit<IndexEntry, "category">, rules: CategoryRule[], title = "", own: string | null = null): string {
  // The writer's own `Category:` line wins when it names a known category.
  if (own !== null && rules.some((rule) => rule.id === own)) return own;
  for (const rule of rules) {
    if (rule.titles !== undefined && !rule.titles.some((re) => matches(re, title, "i"))) continue;
    if (rule.kinds !== undefined && !rule.kinds.includes(entry.kind)) continue;
    if (rule.sources !== undefined && !rule.sources.includes(entry.source)) continue;
    if (rule.checks !== undefined && !entry.checks.some((check) => rule.checks!.some((re) => matches(re, check)))) continue;
    return rule.id;
  }
  return "-";
}

export function loadCategories(guardDir: string): CategoryRule[] {
  const file = path.join(guardDir, "data", "insight-categories.yaml");
  try {
    const parsed = Bun.YAML.parse(fs.readFileSync(file, "utf8")) as { categories?: CategoryRule[] };
    return Array.isArray(parsed?.categories) ? parsed.categories : [];
  } catch {
    return [];
  }
}

export function insightIndex(root: string, rules: CategoryRule[]): IndexEntry[] {
  const checkOf = new Map<string, string>();
  for (const record of readJournal(root).records) if (record.kind === "failure") checkOf.set(record.id, record.check);
  const entries: IndexEntry[] = [];
  for (const file of findInsightFiles(root)) {
    let sections: InsightSection[];
    let heads: { title: string; own: string | null }[];
    try {
      const text = fs.readFileSync(path.join(root, file), "utf8");
      sections = parseInsight(text);
      heads = headings(text);
    } catch {
      continue;
    }
    sections.forEach((section, i) => {
      const head = heads[i] ?? { title: "", own: null };
      const kind = isGreatSection(section) ? "great" : "failure";
      const base: Omit<IndexEntry, "category"> = {
        file,
        ids: section.ids,
        kind,
        checks: section.ids.map((id) => checkOf.get(id) ?? "-"),
        source: firstWord(section.source),
        optionKinds: section.options.map((option) => (OPTION_KINDS.has(option.kind) ? option.kind : "-")),
      };
      entries.push({ ...base, category: categorize(base, rules, head.title, head.own) });
    });
  }
  return entries;
}

// Each section's heading and its own `Category:` line, in file order — the same order parseInsight returns (a
// heading opens a section only when it has a failure id or starts with "great:").
function headings(text: string): { title: string; own: string | null }[] {
  const out: { title: string; own: string | null }[] = [];
  let current: { title: string; own: string | null } | null = null;
  for (const line of text.split(/\r?\n/)) {
    const heading = HEADING_RE.exec(line);
    if (heading) {
      const title = heading[1]!.trim();
      current = (title.match(ID_RE) ?? []).length > 0 || /^great\s*:/i.test(title) ? { title, own: null } : null;
      if (current !== null) out.push(current);
      continue;
    }
    const own = /^Category:\s*([a-z-]+)/i.exec(line);
    if (current !== null && own !== null) current.own = own[1]!.toLowerCase();
  }
  return out;
}

export function indexMarkdown(entries: IndexEntry[]): string {
  const lines = ["| file | ids | kind | check | source | options | category |", "|---|---|---|---|---|---|---|"];
  for (const e of entries) {
    lines.push(`| ${e.file} | ${e.ids.join(", ") || "-"} | ${e.kind} | ${e.checks.join(", ") || "-"} | ${e.source} | ${e.optionKinds.join(", ") || "-"} | ${e.category} |`);
  }
  return lines.join("\n");
}

// The whole text of each section that matches: by category, or by `<file>#<id>`. For an expert that loads insights.
export function showSections(root: string, entries: IndexEntry[], want: { categories: string[]; refs: string[] }): string {
  const chosen = entries.filter((e) => want.categories.includes(e.category)
    || want.refs.some((ref) => { const [file, id] = ref.split("#"); return e.file === file && (id === undefined || e.ids.includes(id)); }));
  const out: string[] = [];
  const byFile = new Map<string, IndexEntry[]>();
  for (const e of chosen) byFile.set(e.file, [...(byFile.get(e.file) ?? []), e]);
  for (const [file, list] of byFile) {
    const text = fs.readFileSync(path.join(root, file), "utf8").split(/\r?\n/);
    let block: string[] = [];
    let keep = false;
    const flush = () => { if (keep && block.length > 0) out.push(`<!-- ${file} -->`, ...block, ""); block = []; };
    for (const line of text) {
      const heading = HEADING_RE.exec(line);
      if (heading) {
        flush();
        const ids: string[] = heading[1]!.match(ID_RE) ?? [];
        const great = /^great\s*:/i.test(heading[1]!.trim());
        keep = list.some((e) => (e.kind === "great" ? great : e.ids.some((id) => ids.includes(id))));
      }
      if (keep) block.push(line);
    }
    flush();
  }
  return out.join("\n");
}
