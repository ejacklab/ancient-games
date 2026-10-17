// M3: insight gate (SPEC.md M3). An insight file answers a logged failure with a section per failure id:
// whys, the source the whys end at, a root cause and options. Only ids, counts, sources, kinds and paths are
// read out; the author's own text stays in the file.
// Round 5, S4: the same file may hold great-success sections (`## great: <path file>`) — comparison, cause and
// options — kept apart from failure sections (their ids are empty).

import * as fs from "node:fs";
import * as path from "node:path";
import { failuresFor } from "./journal.ts";
import type { FailureRecord, Finding, InsightOption, InsightSection } from "./types.ts";

const GUARD_DIR = ".harness-guard";
const INSIGHT_DIR = path.join(GUARD_DIR, "insights");
const RUNS_DIR = "runs";

const ID_RE = /F-[0-9a-f]{8}/g;
const HEADING_RE = /^##(?!#)\s*(.*)$/;
const NUMBER_RE = /^\s*\d+[.)]\s+/;
const WHYS_RE = /^\s*whys\s*:/i;
const SOURCE_RE = /^\s*source\s*:/i;
const CAUSE_RE = /^\s*root\s+cause\s*:/i;
const OPTIONS_RE = /^\s*options\s*:/i;
const KIND_RE = /^\[([^\]]*)\]/;
const EVIDENCE_RE = /evidence\s*:\s*(.*)$/i;

const SOURCES = ["instruction", "check", "tool", "config"];
const OPTION_KINDS = ["rule", "check", "tool", "config-advice"];

// Round 5, S4: great-success sections.
const GREAT_HEADING_RE = /^great\s*:\s*(.*)$/i;
const COMPARISON_RE = /^\s*comparison\s*:/i;
const GREAT_CAUSE_RE = /^\s*cause\s*:/i;
const GREAT_OPTION_KINDS = ["rule", "check", "tool"];

// The last why ending at a person is a shape, not a word list the spec fixes: a heuristic, so it only warns.
const PERSON_RE = /\bforgot\b|\bcareless\b|\bi missed\b|\bthe model was wrong\b/i;

function isLabel(line: string): boolean {
  return WHYS_RE.test(line) || SOURCE_RE.test(line) || CAUSE_RE.test(line) || OPTIONS_RE.test(line);
}

function isGreatLabel(line: string): boolean {
  return COMPARISON_RE.test(line) || GREAT_CAUSE_RE.test(line) || OPTIONS_RE.test(line);
}

// A great section is an InsightSection with no ids (types.ts is fixed and has no fields for the path file, the
// comparison or the cause), so those three ride on this local extension.
export interface GreatSection extends InsightSection {
  great: string; // the path file named in the heading, as written (surrounding backticks or quotes removed)
  comparison: string | null;
  cause: string | null;
}

export function isGreatSection(s: InsightSection): s is GreatSection {
  return s.ids.length === 0 && typeof (s as Partial<GreatSection>).great === "string";
}

// Under .harness-guard/insights/ every *.md counts, whatever its name (round 3, C5); under runs/** only insight*.md.
function isInsightName(name: string): boolean {
  return name.startsWith("insight") && name.endsWith(".md");
}

function isGuardInsightName(name: string): boolean {
  return name.endsWith(".md");
}

function readDirSafe(dir: string): fs.Dirent[] {
  try {
    return fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return [];
  }
}

// ---- discovery ---------------------------------------------------------------------------------------------------

export function findInsightFiles(root: string): string[] {
  const found: string[] = [];

  for (const entry of readDirSafe(path.join(root, INSIGHT_DIR))) {
    if (entry.isFile() && isGuardInsightName(entry.name)) found.push(path.join(INSIGHT_DIR, entry.name));
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
      if (parts[0] === RUNS_DIR && isInsightName(name)) found.push(childRelative);
    }
  };
  walk(path.join(root, RUNS_DIR), RUNS_DIR);

  return found.sort();
}

// ---- parsing -----------------------------------------------------------------------------------------------------

function labelText(line: string, labelRe: RegExp): string {
  return line.replace(labelRe, "").trim();
}

// The numbered list after a label (round 3, C6): blank lines are skipped until the first item, an indented line
// continues the item above it, and the list ends at the next unindented line that is not an item — which includes
// the next label and the next heading.
function numberedItems(lines: string[], from: number): string[] {
  const items: string[] = [];
  let index = from;
  while (index < lines.length) {
    const line = lines[index]!;
    if (line.trim() === "") {
      index += 1;
      continue;
    }
    if (!NUMBER_RE.test(line)) break;
    let item = line.replace(NUMBER_RE, "").trim();
    index += 1;
    while (index < lines.length) {
      const next = lines[index]!;
      if (next.trim() === "" || !/^\s/.test(next)) break;
      item = `${item} ${next.trim()}`;
      index += 1;
    }
    items.push(item);
  }
  return items;
}

function parseOption(item: string): InsightOption {
  let rest = item;
  let kind = "";
  const kindMatch = KIND_RE.exec(rest);
  if (kindMatch) {
    kind = kindMatch[1]!.trim();
    rest = rest.slice(kindMatch[0].length).trim();
  }
  let text = rest;
  let evidence = "";
  const evidenceMatch = EVIDENCE_RE.exec(rest);
  if (evidenceMatch) {
    evidence = evidenceMatch[1]!.trim();
    text = rest.slice(0, evidenceMatch.index).trim().replace(/[\s—–:,-]+$/, "");
  }
  return { kind, text, evidence };
}

// A label's text: on the same line, or the next non-empty line when that is not another label or a list item.
function labelValue(lines: string[], at: number, labelRe: RegExp, isAnyLabel: (line: string) => boolean): string | null {
  const sameLine = labelText(lines[at]!, labelRe);
  if (sameLine !== "") return sameLine;
  for (let i = at + 1; i < lines.length; i++) {
    const line = lines[i]!;
    if (line.trim() === "") continue;
    if (isAnyLabel(line) || NUMBER_RE.test(line)) return null;
    return line.trim();
  }
  return null;
}

function parseRootCause(lines: string[], at: number): string | null {
  return labelValue(lines, at, CAUSE_RE, isLabel);
}

function parseSection(ids: string[], body: string[]): InsightSection {
  let whys: string[] = [];
  let source: string | null = null;
  let rootCause: string | null = null;
  let options: InsightOption[] = [];

  for (let i = 0; i < body.length; i++) {
    const line = body[i]!;
    if (WHYS_RE.test(line)) whys = numberedItems(body, i + 1);
    else if (SOURCE_RE.test(line)) source = labelText(line, SOURCE_RE);
    else if (CAUSE_RE.test(line)) rootCause = parseRootCause(body, i);
    else if (OPTIONS_RE.test(line)) options = numberedItems(body, i + 1).map(parseOption);
  }

  return { ids, whys, source, rootCause, options };
}

function parseGreatSection(great: string, body: string[]): GreatSection {
  let comparison: string | null = null;
  let cause: string | null = null;
  let options: InsightOption[] = [];

  for (let i = 0; i < body.length; i++) {
    const line = body[i]!;
    if (COMPARISON_RE.test(line)) comparison = labelValue(body, i, COMPARISON_RE, isGreatLabel);
    else if (GREAT_CAUSE_RE.test(line)) cause = labelValue(body, i, GREAT_CAUSE_RE, isGreatLabel);
    else if (OPTIONS_RE.test(line)) options = numberedItems(body, i + 1).map(parseOption);
  }

  return { ids: [], whys: [], source: null, rootCause: null, options, great, comparison, cause };
}

function unquote(text: string): string {
  return text.trim().replace(/^[`"']+|[`"']+$/g, "").trim();
}

export function parseInsight(text: string): InsightSection[] {
  const lines = text.split(/\r?\n/);
  const sections: InsightSection[] = [];
  let ids: string[] = [];
  let great: string | null = null;
  let body: string[] = [];

  const flush = (): void => {
    if (great !== null) sections.push(parseGreatSection(great, body));
    else if (ids.length > 0) sections.push(parseSection(ids, body));
    ids = [];
    great = null;
    body = [];
  };

  for (const line of lines) {
    const heading = HEADING_RE.exec(line);
    if (heading) {
      flush();
      // A heading that starts with "great:" is a great-success section, never a failure section (S4).
      const greatHeading = GREAT_HEADING_RE.exec(heading[1]!.trim());
      if (greatHeading) great = unquote(greatHeading[1]!);
      else ids = heading[1]!.match(ID_RE) ?? [];
      continue;
    }
    if (ids.length > 0 || great !== null) body.push(line);
  }
  flush();
  return sections;
}

// The first word of the Source line decides (round 3, C7); the rest of the line is the author's detail.
function isKnownSource(source: string): boolean {
  const first = /^[A-Za-z-]+/.exec(source.trim());
  return first !== null && SOURCES.includes(first[0]);
}

// ---- checks ------------------------------------------------------------------------------------------------------

function fail(rule: string, message: string, fix: string): Finding {
  return { rule, severity: "fail", message, fix, ref: "SPEC.md M3" };
}

export function checkSection(s: InsightSection): Finding[] {
  const findings: Finding[] = [];

  if (s.whys.length < 3 || s.whys.length > 6) {
    findings.push(fail("R12.3-whys-count", `Whys: ${s.whys.length} items, 3 to 6 needed`, "number the whys 1. to 6."));
  }
  if (s.source === null || !isKnownSource(s.source)) {
    findings.push(fail("R12.3-source", `Source: ${s.source === null ? "missing" : "unknown"}`, `Source: one of ${SOURCES.join(", ")}.`));
  }
  if (s.rootCause === null || s.rootCause.trim() === "") {
    findings.push(fail("R12.3-root-cause", "Root cause: missing or empty", "Root cause: the changeable source, in one line of text."));
  }
  if (s.options.length < 2 || s.options.length > 3) {
    findings.push(fail("R12.3-options-count", `Options: ${s.options.length} items, 2 or 3 needed`, "list 2 or 3 fix options."));
  }

  s.options.forEach((each, index) => {
    const kind = each.kind.trim().toLowerCase();
    if (kind === "" || !OPTION_KINDS.includes(kind)) {
      findings.push(fail("R12.3-option-kind", `Option ${index + 1}: kind is missing or not one of ${OPTION_KINDS.join(", ")}`, `start the option with [${OPTION_KINDS[0]}] or another listed kind.`));
    }
    if (each.evidence.trim() === "") {
      findings.push(fail("R12.3-option-evidence", `Option ${index + 1}: no evidence`, "end the option with evidence: <path or fact>."));
    }
  });

  const lastWhy = s.whys[s.whys.length - 1];
  if (lastWhy !== undefined && PERSON_RE.test(lastWhy)) {
    findings.push({
      rule: "R12.3-why-ends-at-person",
      severity: "warn",
      message: `Heuristic: the last why reads as ending at the person — "${lastWhy}". A why that ends at a person names no source to change.`,
      fix: "end the whys at the instruction, check, tool or config that let it happen.",
      ref: "SPEC.md M3",
    });
  }

  return findings;
}

// Round 5, S4: a great-success section needs a comparison, a cause and 1 to 3 options, each of kind rule, check or
// tool and holding evidence. Kind and evidence problems are R12.7-great-options: S4 names no rule of their own.
function failGreat(rule: string, message: string, fix: string): Finding {
  return { rule, severity: "fail", message, fix, ref: "SPEC.md Round 5 S4" };
}

export function checkGreatSection(s: InsightSection): Finding[] {
  const great = s as Partial<GreatSection>;
  const findings: Finding[] = [];

  if (typeof great.comparison !== "string" || great.comparison.trim() === "") {
    findings.push(failGreat("R12.7-great-comparison", "Comparison: missing or empty", "Comparison: what this success did better than, and by how much."));
  }
  if (typeof great.cause !== "string" || great.cause.trim() === "") {
    findings.push(failGreat("R12.7-great-cause", "Cause: missing or empty", "Cause: why it went well, in one line of text."));
  }
  if (s.options.length < 1 || s.options.length > 3) {
    findings.push(failGreat("R12.7-great-options", `Options: ${s.options.length} items, 1 to 3 needed`, "list 1 to 3 options that keep what worked."));
  }
  s.options.forEach((each, index) => {
    const kind = each.kind.trim().toLowerCase();
    if (kind === "" || !GREAT_OPTION_KINDS.includes(kind)) {
      findings.push(failGreat("R12.7-great-options", `Option ${index + 1}: kind is missing or not one of ${GREAT_OPTION_KINDS.join(", ")}`, `start the option with [${GREAT_OPTION_KINDS[0]}] or another listed kind.`));
    }
    if (each.evidence.trim() === "") {
      findings.push(failGreat("R12.7-great-options", `Option ${index + 1}: no evidence`, "end the option with evidence: <path or fact>."));
    }
  });

  return findings;
}

// ---- answered failures -------------------------------------------------------------------------------------------

function hasFail(findings: Finding[]): boolean {
  return findings.some((finding) => finding.severity === "fail");
}

function readInsight(root: string, relative: string): InsightSection[] {
  try {
    return parseInsight(fs.readFileSync(path.join(root, relative), "utf8"));
  } catch {
    return [];
  }
}

export function answered(root: string): Map<string, string> {
  const answers = new Map<string, string>();
  for (const relative of findInsightFiles(root)) {
    for (const section of readInsight(root, relative)) {
      if (hasFail(checkSection(section))) continue;
      for (const id of section.ids) if (!answers.has(id)) answers.set(id, relative);
    }
  }
  return answers;
}

// Path files answered by a valid great section, as root-relative paths (an absolute heading path inside the root is
// made relative to it), so they compare with the relative paths path-file discovery returns.
export function greatAnswered(root: string): Set<string> {
  const files = new Set<string>();
  for (const relative of findInsightFiles(root)) {
    for (const section of readInsight(root, relative)) {
      if (!isGreatSection(section) || section.great === "") continue;
      if (hasFail(checkGreatSection(section))) continue;
      const named = path.isAbsolute(section.great) ? path.relative(root, section.great) : section.great;
      files.add(path.normalize(named));
    }
  }
  return files;
}

// R12.2: a failure is what the evaluator judges wrong against the product's vision, use cases and requirements, or a
// correction from the owner. What the guard's own checks see is evidence, kept in the journal, never asking for an
// insight by itself.
export const JUDGES = new Set(["evaluator", "owner"]);

export function isJudged(record: FailureRecord): boolean {
  return JUDGES.has(record.found_by);
}

export function openFailures(root: string, session: string | null): FailureRecord[] {
  const answers = answered(root);
  return failuresFor(root, session).filter((record) => isJudged(record) && !answers.has(record.id));
}