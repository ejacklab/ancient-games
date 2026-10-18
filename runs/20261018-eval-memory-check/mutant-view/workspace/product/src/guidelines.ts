// The guidelines the tool checks against: its own copy of the two kit files (C1), loaded and parsed here.
// The copy under `guidelines/` is verbatim; the version printed in the report is its content hash, so a report
// names the exact text its results came from.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";

export const FOLDER = path.resolve(import.meta.dirname, "..");
export const GUIDELINES_DIR = path.join(FOLDER, "guidelines");
export const SOT_YAML = path.join(GUIDELINES_DIR, "SOURCE_OF_TRUTH_REQUIREMENTS.yaml");
export const CACHES_MD = path.join(GUIDELINES_DIR, "CACHES.md");
export const MEMORY_INDEX_PY = path.resolve(import.meta.dirname, "../../tools/memory_index.py");

export type Level = "MUST" | "SHOULD" | "guidance";

export interface SotRecord {
  readonly id: string;
  readonly level: Level;
  /** The `check` field, split: `tool`, `git`, `reviewer`, `secret scanner`, `none`. */
  readonly checks: readonly string[];
  readonly failsIf: string;
  readonly text: string;
  readonly category: string;
}

export interface CachesRecord {
  readonly id: string;
  readonly title: string;
  readonly failsIf: string;
}

export interface Guidelines {
  readonly sot: readonly SotRecord[];
  readonly caches: readonly CachesRecord[];
  /** Content hash of both kit files: the version the report prints. */
  readonly version: string;
}

function readText(file: string): string {
  return readFileSync(file, "utf8");
}

function squash(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

function hashOf(file: string): string {
  return createHash("sha256").update(readFileSync(file)).digest("hex").slice(0, 12);
}

/** `Bun.YAML.parse` needs no dependency; the records under `categories[].groups[].requirements[]` are one shape. */
function loadSot(file: string): SotRecord[] {
  const document = Bun.YAML.parse(readText(file)) as {
    categories?: {
      title?: string;
      groups?: { requirements?: Record<string, unknown>[] }[];
    }[];
  };
  const records: SotRecord[] = [];
  for (const category of document.categories ?? []) {
    for (const group of category.groups ?? []) {
      for (const requirement of group.requirements ?? []) {
        const id = String(requirement["id"] ?? "");
        const level = String(requirement["level"] ?? "") as Level;
        const check = String(requirement["check"] ?? "none");
        if (!id) continue;
        records.push({
          id,
          level,
          checks: check.split(";").map((part) => part.trim()).filter(Boolean),
          failsIf: squash(String(requirement["fails_if"] ?? "")),
          text: squash(String(requirement["text"] ?? "")),
          category: String(category.title ?? ""),
        });
      }
    }
  }
  return records;
}

const HEADING = /^\*\*((?:B|K|Rd)\d+) — (.+?)\*\*.*$/;
const FAILS_IF = /^\s*-?\s*\*+Fails if\*+\s*(.+)$/;

/**
 * `CACHES.md` § Core requirements: each requirement is a bold heading, with its Fails-if line inside it. The
 * requirement is the heading, so the sub-bullets (B1.1, K1.2, ...) are not ids of their own.
 */
function loadCaches(file: string): CachesRecord[] {
  const records: CachesRecord[] = [];
  let current: { id: string; title: string; failsIf: string } | null = null;
  let heading = false;
  for (const line of readText(file).split("\n")) {
    if (/^## /.test(line)) {
      if (current) records.push(current);
      current = null;
      heading = false;
    }
    const match = HEADING.exec(line);
    if (match) {
      if (current) records.push(current);
      current = { id: match[1]!, title: squash(match[2]!), failsIf: "" };
      heading = true;
      continue;
    }
    if (!heading || !current) continue;
    const fails = FAILS_IF.exec(line);
    if (fails) current.failsIf = `${current.failsIf} ${squash(fails[1]!)}`.trim();
  }
  if (current) records.push(current);
  return records;
}

export function loadGuidelines(): Guidelines {
  return {
    sot: loadSot(SOT_YAML),
    caches: loadCaches(CACHES_MD),
    version: `SOURCE_OF_TRUTH_REQUIREMENTS.yaml ${hashOf(SOT_YAML)}, CACHES.md ${hashOf(CACHES_MD)}`,
  };
}