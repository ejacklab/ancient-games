// Round 6, K1 (SPEC.md "K1 Criteria files"): the criteria a task is scored against — a YAML file written before the
// work, one item per thing the result must get right, each marked met or not met with evidence at the end. The guard
// reads ids, marks and counts out of it; the request and the criterion text stay in the file.

import * as fs from "node:fs";
import * as path from "node:path";
import { units } from "./register.ts";
import type { Criterion, CriteriaFile, Finding, Register, Score } from "./types.ts";

const GUARD_DIR = ".harness-guard";
const CRITERIA_DIR = path.join(GUARD_DIR, "criteria");
const RUNS_DIR = "runs";
const REQUEST_CHARS = 120;

export class CriteriaError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "CriteriaError";
  }
}

// ---- loading ----------------------------------------------------------------------------------------------------

function isEntry(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

// A value that counts as written: a string with something in it. Blank and non-strings do not.
function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function list(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

// A criterion read defensively: an item that is not a mapping names nothing, and names no mark either.
function criterion(value: unknown): Criterion {
  if (!isEntry(value)) return { id: "", text: "", met: null };
  return {
    id: text(value.id),
    text: text(value.text),
    met: value.met === true || value.met === false ? value.met : null,
    evidence: text(value.evidence),
  };
}

// The items of a criteria file, whatever YAML shape the file holds; the position is counted from zero, as written.
function items(c: CriteriaFile): Criterion[] {
  return list(c?.items).map(criterion);
}

// The id a finding may name. A missing id is named by its position, so no item text ever reaches a message.
function idOf(item: Criterion, index: number): string {
  return item.id === "" ? `items[${index}]` : item.id;
}

function marked(item: Criterion): boolean {
  return item.met === true || item.met === false;
}

export function loadCriteria(file: string): CriteriaFile {
  const name = path.basename(file);
  let parsed: unknown;
  try {
    parsed = Bun.YAML.parse(fs.readFileSync(file, "utf8"));
  } catch {
    // The parser's own message would carry the source line, so the diagnostic stays generic.
    throw new CriteriaError(`criteria ${name}: cannot be read or parsed`);
  }
  if (!isEntry(parsed) || parsed.criteria !== 1) {
    throw new CriteriaError(`criteria ${name}: has no numeric "criteria: 1" marker`);
  }
  return parsed as unknown as CriteriaFile;
}

export function isCriteriaFile(file: string): boolean {
  const name = path.basename(file);
  if (!name.endsWith(".yaml")) return false;
  // Any .yaml in .harness-guard/criteria/ counts too, as the reminder offers that folder with any name (COO, round 6).
  return name.startsWith("criteria") || path.basename(path.dirname(file)) === "criteria" && path.basename(path.dirname(path.dirname(file))) === ".harness-guard";
}

// ---- discovery --------------------------------------------------------------------------------------------------

function readDirSafe(dir: string): fs.Dirent[] {
  try {
    return fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return [];
  }
}

// Under .harness-guard/criteria/ every *.yaml counts, whatever its name; under runs/** only criteria*.yaml.
function isGuardName(name: string): boolean {
  return name.endsWith(".yaml");
}

export function findCriteriaFiles(root: string): string[] {
  const found: string[] = [];

  for (const entry of readDirSafe(path.join(root, CRITERIA_DIR))) {
    if (entry.isFile() && isGuardName(entry.name)) found.push(path.join(CRITERIA_DIR, entry.name));
  }

  const walk = (dir: string, relative: string): void => {
    for (const entry of readDirSafe(dir)) {
      const childRelative = path.join(relative, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === ".git" || entry.name === "node_modules" || childRelative === GUARD_DIR) continue;
        walk(path.join(dir, entry.name), childRelative);
        continue;
      }
      if (!entry.isFile()) continue;
      const parts = childRelative.split(path.sep);
      const name = parts[parts.length - 1]!;
      if (parts[0] === RUNS_DIR && isCriteriaFile(name)) found.push(childRelative);
    }
  };
  walk(path.join(root, RUNS_DIR), RUNS_DIR);

  return found.sort();
}

// ---- checks -----------------------------------------------------------------------------------------------------

function fail(rule: string, message: string, fix: string): Finding {
  return { rule, severity: "fail", message, fix, ref: "SPEC.md K1" };
}

export function checkCriteria(c: CriteriaFile): Finding[] {
  const findings: Finding[] = [];
  const list_ = items(c);

  if (list_.length === 0) {
    findings.push(
      fail("R12.7-criteria-empty", "the criteria file has no items", "items: - id: C1  — one item per thing the result must get right."),
    );
  }

  const seen = new Set<string>();
  list_.forEach((item, index) => {
    const id = idOf(item, index);
    if (item.id === "" || item.text === "") {
      findings.push(
        fail("R12.7-criterion-text", `item ${id}: no id or no text`, `items: - id: ${item.id === "" ? "C1" : item.id}\n    text: <one thing the result must get right>.`),
      );
    } else if (seen.has(item.id)) {
      findings.push(fail("R12.7-criterion-text", `item ${id} at items[${index}]: the id is used twice`, "give every criterion its own id."));
    } else {
      seen.add(item.id);
    }
    // A mark without evidence says nothing, so it is not a score (R12.7: a result is the share met).
    if (marked(item) && item.evidence === "") {
      findings.push(fail("R12.7-criterion-evidence", `item ${id}: marked met ${String(item.met)} with no evidence`, `met: true|false with evidence: <a path or a fact>.`));
    }
  });

  return findings;
}

// ---- score ------------------------------------------------------------------------------------------------------

// One decimal, as every count in the guard is.
function round1(value: number): number {
  return Math.round(value * 10) / 10;
}

export function score(c: CriteriaFile): Score {
  const list_ = items(c);
  const total = list_.length;
  // An item with no mark counts as neither met nor not met: it is reported as unmarked, never as a zero.
  const met = list_.filter((item) => item.met === true).length;
  const unmarked = list_.filter((item) => !marked(item)).map(idOf);
  return {
    met,
    total,
    percent: total === 0 ? null : round1((met / total) * 100),
    unmarked,
  };
}

// ---- building ----------------------------------------------------------------------------------------------------

// The criteria of a register's units: one item per thing the result must get right, none of them marked yet.
export function fromRegister(r: Register, session: string, request: string): CriteriaFile {
  return {
    criteria: 1,
    session,
    request: cut(request),
    items: units(r).map(({ id, text: unitText }) => ({ id, text: unitText })),
  };
}

// A request is a few words: cut so a whole prompt can never travel into a file the guard writes.
function cut(request: string): string {
  return text(request).slice(0, REQUEST_CHARS);
}

function plain(value: string): boolean {
  return /^[A-Za-z0-9_][A-Za-z0-9 _./-]*$/.test(value);
}

// A YAML scalar: plain when it can be, quoted otherwise, so a request with a colon in it still parses.
function scalar(value: string): string {
  return plain(value) ? value : JSON.stringify(value);
}

// The skeleton for a new criteria file: two placeholder items the agent replaces. The file holds nothing but the
// session, the request and the placeholders — no command text, no output.
export function skeleton(session: string, request: string): string {
  return [
    "# The criteria this request will be scored on. Write it before the work, mark each item at the end.",
    "# Replace the two placeholder items with one item per thing the result must get right.",
    "criteria: 1",
    `session: ${scalar(session)}`,
    `request: ${scalar(cut(request))}`,
    "items:",
    "  - id: C1",
    '    text: ""   # one thing the result must get right',
    "    met: null  # true | false at the end, never while the work runs",
    '    evidence: ""',
    "  - id: C2",
    '    text: ""',
    "    met: null",
    '    evidence: ""',
    "",
  ].join("\n");
}