// Acceptance checks written from SPEC.md Round 11 (I1 index, I2 show, I3 categories), independently of the
// implementation. Every test plants a temporary root: insight files under runs/x/insight.md and
// .harness-guard/insights/, plus a journal with the failure records the index reads checks from.
import { afterEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { indexMarkdown, insightIndex, loadCategories, showSections } from "../src/insight-index.ts";
import type { CategoryRule, IndexEntry } from "../src/insight-index.ts";
import type { FailureRecord } from "../src/types.ts";

const GUARD_DIR = path.resolve(import.meta.dirname, "..");
const CLI = path.join(GUARD_DIR, "src", "cli.ts");
const SECRET = "SECRET-PLANT-4c1a77";
const roots: string[] = [];

afterEach(() => {
  for (const root of roots.splice(0)) fs.rmSync(root, { recursive: true, force: true });
});

// A root that is a git repository (the CLI resolves the guard root from it), with a journal for the checks.
function box() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-r11-"));
  roots.push(root);
  execFileSync("git", ["init", "-q"], { cwd: root });
  const write = (file: string, text: string) => {
    const absolute = path.join(root, file);
    fs.mkdirSync(path.dirname(absolute), { recursive: true });
    fs.writeFileSync(absolute, text);
    return absolute;
  };
  const failure = (changes: Partial<FailureRecord> = {}): FailureRecord => ({
    kind: "failure",
    id: "F-1a2b3c4d",
    time: "2026-10-16T02:00:00Z",
    session: "s",
    found_by: "guard",
    check: "R12.1-exit",
    input: "codex, answer.md",
    expected: "a non-empty answer file",
    actual: "the answer file was empty",
    engine: "codex",
    harness: "claude-code",
    reason: "the engine call produced no answer",
    evidence: `.harness-guard/evidence/${changes.id ?? "F-1a2b3c4d"}.json`,
    ...changes,
  });
  const journal = (records: FailureRecord[]) => {
    write(".harness-guard/journal.jsonl", `${records.map((record) => JSON.stringify(record)).join("\n")}\n`);
  };
  const cli = (...args: string[]) => spawnSync(process.execPath, [CLI, ...args], {
    cwd: root, encoding: "utf8", timeout: 20_000,
    env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" },
  });
  return { root, write, failure, journal, cli };
}

type Box = ReturnType<typeof box>;

// One failure section whose whys, root cause and options each carry the planted secret.
function sectionBody(options = [`1. [rule] keep the check — evidence: runs/x/evidence-1.md`,
  `2. [check] report the rule id — evidence: runs/x/evidence-2.md`]): string {
  return [
    "Whys:",
    `1. ${SECRET} why one`,
    "2. why two",
    "3. why three",
    "",
    `Source: instruction — ${SECRET}`,
    "",
    `Root cause: ${SECRET} in the wording`,
    "",
    "Options:",
    ...options.map((line, i) => line.includes("[rule]") ? `${line} ${SECRET}` : line),
  ].join("\n");
}

function failureFile(id: string, check = "R12.1-exit", source = "instruction", options?: string[]): string {
  return `## ${id}\n\n${sectionBody(options)}\n`;
}

// The standard planted root: one failure section in runs/x/insight.md and one in .harness-guard/insights/, plus a
// great section, and a journal holding the check of each failure id.
function planted(b: Box = box()) {
  b.write("runs/x/insight.md", `# Insight notes\n\n${failureFile("F-1a2b3c4d", "R12.1-exit")}`);
  b.write(".harness-guard/insights/notes.md", `## F-2b3c4d5e\n\n${sectionBody()}\n\n## great: runs/x/a.md\n\n`
    + `Comparison: it printed the check before the run\n\nCause: the gate ran first\n\nOptions:\n1. [check] keep the order — evidence: runs/x/evidence-3.md\n`);
  b.journal([
    b.failure({ id: "F-1a2b3c4d", check: "R12.1-exit" }),
    b.failure({ id: "F-2b3c4d5e", check: "R12.2-command-error" }),
  ]);
  return b;
}

function rows(b: Box, rules: CategoryRule[] = loadCategories(GUARD_DIR)): IndexEntry[] {
  return insightIndex(b.root, rules);
}

// ---- P1: every section once --------------------------------------------------------------------------------------

test("P1 Fails-if: a section is missing from the index or listed twice — every planted section appears once", () => {
  const b = planted();
  const entries = rows(b);
  const listed = entries.map((entry) => `${entry.file}#${entry.ids.join(",") || entry.kind}`);
  expect(listed).toContain("runs/x/insight.md#F-1a2b3c4d");
  expect(listed).toContain(path.join(".harness-guard", "insights", "notes.md") + "#F-2b3c4d5e");
  expect(listed).toContain(path.join(".harness-guard", "insights", "notes.md") + "#great");
  expect(new Set(listed).size).toBe(listed.length);
  expect(entries.filter((e) => e.file === "runs/x/insight.md")).toHaveLength(1);
  // I1 row fields: ids, kind, the journal's check per id, the Source first word, the options' kinds.
  const first = entries.find((e) => e.ids.includes("F-1a2b3c4d"))!;
  expect(first).toEqual({
    file: "runs/x/insight.md",
    ids: ["F-1a2b3c4d"],
    kind: "failure",
    checks: ["R12.1-exit"],
    source: "instruction",
    optionKinds: ["rule", "check"],
    category: expect.any(String),
  });
  const second = entries.find((e) => e.ids.includes("F-2b3c4d5e"))!;
  expect(second.checks).toEqual(["R12.2-command-error"]);
  // A great section has no ids and takes its kinds from its own options.
  const great = entries.find((e) => e.kind === "great")!;
  expect(great.ids).toEqual([]);
  expect(great.optionKinds).toEqual(["check"]);
});

test("P1 Fails-if: a section is missing from the index — an id with no journal record still gets a row, with check -", () => {
  const b = box();
  b.write("runs/x/insight.md", failureFile("F-3c4d5e6f", "R12.9-nothing"));
  b.journal([]);
  const entries = rows(b);
  expect(entries).toHaveLength(1);
  expect(entries[0]!.checks).toEqual(["-"]);
});

// ---- P2: the index prints no author text ---------------------------------------------------------------------------

test("P2 Fails-if: the index prints any whys, root-cause or option text — the planted secret is in no row, JSON or table", () => {
  const b = planted();
  const entries = rows(b);
  expect(JSON.stringify(entries)).not.toContain(SECRET);
  expect(indexMarkdown(entries)).not.toContain(SECRET);
  const result = b.cli("insight", "index");
  expect(result.status).toBe(0);
  expect(result.stdout).not.toContain(SECRET);
  expect(b.cli("insight", "index", "--json").stdout).not.toContain(SECRET);
});

// ---- P3: show --category -------------------------------------------------------------------------------------------

test("P3 Fails-if: show prints a section that does not match, or misses one that does — --category prints only the matching", () => {
  const b = planted();
  // A rule set of its own so the planted file shapes are placed exactly where the test says.
  const rules: CategoryRule[] = [
    { id: "tool", name: "an engine behaved other than expected", sources: ["tool"] },
    { id: "spec", name: "a spec was unclear", sources: ["instruction"], titles: ["spec", "brief"] },
  ];
  b.write("runs/x/insight.md", failureFile("F-1a2b3c4d — a spec question", "R12.1-exit", "instruction")
    + `\n## F-4d5e6f70\n\n${sectionBody().replace(/Source: instruction/, "Source: tool")}\n`);
  const entries = rows(b, rules);
  const tool = entries.filter((entry) => entry.category === "tool");
  const spec = entries.filter((entry) => entry.category === "spec");
  expect(tool.map((entry) => entry.ids[0])).toEqual(["F-4d5e6f70"]);
  expect(spec.map((entry) => entry.ids[0])).toEqual(["F-1a2b3c4d"]);

  const printed = showSections(b.root, entries, { categories: ["tool"], refs: [] });
  expect(printed).toContain("<!-- ");
  expect(printed).toContain("F-4d5e6f70");
  expect(printed).not.toContain("F-1a2b3c4d"); // a section that does not match
  expect(printed).not.toContain("great:"); // the great section has no rule here either

  const viaCli = b.cli("insight", "show", "--category", "tool");
  expect(viaCli.status).toBe(0);
  expect(viaCli.stdout).toContain("F-4d5e6f70");
  expect(viaCli.stdout).not.toContain("F-1a2b3c4d");

  // Two categories at once: both sides, each exactly once.
  const both = b.cli("insight", "show", "--category", "tool", "--category", "spec");
  expect(both.stdout.match(/F-4d5e6f70/g)).toHaveLength(1);
  expect(both.stdout.match(/F-1a2b3c4d/g)).toHaveLength(1);
});

test("P3 Fails-if: show misses one that does match — a great section is printed whole for its category", () => {
  const b = box();
  b.write("runs/x/insight.md", `## great: runs/x/a.md\n\nComparison: printed first\n\nCause: the gate ran first\n\n`
    + `Options:\n1. [check] keep the order — evidence: runs/x/e.md\n`);
  b.journal([]);
  const entries = rows(b);
  const printed = showSections(b.root, entries, { categories: entries.map((entry) => entry.category), refs: [] });
  expect(printed).toContain("Comparison: printed first");
  expect(printed).toContain("Options:");
});

// ---- P4: refs, usage, no match -------------------------------------------------------------------------------------

test("P4 I2: show <file>#<id> prints that section only; a file with no id prints its sections", () => {
  const b = planted();
  const entries = rows(b, [{ id: "any", name: "everything", kinds: ["failure", "great"] }]);
  const one = showSections(b.root, entries, {
    categories: [], refs: [`${path.join(".harness-guard", "insights", "notes.md")}#F-2b3c4d5e`],
  });
  expect(one).toContain("F-2b3c4d5e");
  expect(one).not.toContain("runs/x/insight.md");
  expect(one.match(/Whys:/g)).toHaveLength(1);
  expect(b.cli("insight", "show", `${path.join(".harness-guard", "insights", "notes.md")}#F-2b3c4d5e`).stdout)
    .toContain("F-2b3c4d5e");
});

test("P4 I2: show with neither --category nor a ref is a usage error (2) and prints nothing", () => {
  const b = planted();
  const result = b.cli("insight", "show");
  expect(result.status).toBe(2);
  expect(result.stderr).toContain("--category"); // the usage error goes to stderr
  expect(result.stdout).toBe("");
});

test("P4 I2: show that matches nothing says so", () => {
  const b = planted();
  const result = b.cli("insight", "show", "--category", "no-such-category");
  expect(result.status).toBe(0);
  expect(result.stdout.trim()).toBe("no matching insight sections");
});

// ---- P5: categories ------------------------------------------------------------------------------------------------

test("P5 I3: a section takes the first rule whose every given condition matches", () => {
  const b = box();
  b.write("runs/x/insight.md",
    `## F-1a2b3c4d — a bun test read wrongly\n\n${sectionBody()}\n\n`
    + `## F-2b3c4d5e — a quota setting\n\n${sectionBody().replace(/Source: instruction/, "Source: config")}\n\n`
    + `## F-3c4d5e6f\n\n${sectionBody().replace(/Source: instruction/, "Source: instruction")}\n`);
  b.journal([b.failure({ id: "F-1a2b3c4d", check: "R11.9-index" }), b.failure({ id: "F-3c4d5e6f", check: "R12.1-exit" })]);
  const rules: CategoryRule[] = [
    { id: "test", name: "a test failed or was read wrongly", sources: ["instruction"], checks: ["^R11\\."] },
    { id: "instruction", name: "anything from an instruction", sources: ["instruction"] },
  ];
  const entries = rows(b, rules);
  const byId = new Map(entries.map((entry) => [entry.ids[0], entry.category]));
  expect(byId.get("F-1a2b3c4d")).toBe("test"); // both conditions hold: the first rule wins
  expect(byId.get("F-2b3c4d5e")).toBe("-"); // no rule matches
  expect(byId.get("F-3c4d5e6f")).toBe("instruction"); // the first rule's checks do not match, the second does
  const config: CategoryRule[] = [{ id: "config", name: "the environment", sources: ["config"] }];
  expect(rows(b, config).find((entry) => entry.ids[0] === "F-2b3c4d5e")!.category).toBe("config");
});

test("P5 I3: a section's own Category: line overrides every rule", () => {
  const b = box();
  b.write("runs/x/insight.md", `## F-1a2b3c4d — a quota setting\n\n${sectionBody()}\nCategory: spec\n\n`
    + `## F-2b3c4d5e — a quota setting\n\n${sectionBody().replace(/Source: instruction/, "Source: config")}\n`
    + "Category: no-such-category\n");
  b.journal([b.failure({ id: "F-1a2b3c4d", check: "R12.1-exit" }), b.failure({ id: "F-2b3c4d5e", check: "R12.1-exit" })]);
  const rules: CategoryRule[] = [
    { id: "config", name: "the environment", sources: ["config"] },
    { id: "spec", name: "a spec was unclear", sources: ["instruction"] },
  ];
  const entries = rows(b, rules);
  expect(entries.find((entry) => entry.ids[0] === "F-1a2b3c4d")!.category).toBe("spec"); // the config rule would not win
  expect(entries.find((entry) => entry.ids[0] === "F-2b3c4d5e")!.category).toBe("config"); // an unknown id falls back
});

test("P5 Fails-if: a category rule with no matching section breaks the index — every section is still listed", () => {
  const b = planted();
  const rules: CategoryRule[] = [
    { id: "never", name: "matches nothing", sources: ["nothing-like-this"], titles: ["no such title"], kinds: ["great"] },
    { id: "spec", name: "a spec was unclear", sources: ["instruction"] },
  ];
  const entries = rows(b, rules);
  expect(entries.map((entry) => entry.ids.join(",") || entry.kind).sort())
    .toEqual(["F-1a2b3c4d", "F-2b3c4d5e", "great"].sort());
  expect(entries.every((entry) => entry.category !== "never")).toBe(true);
  expect(indexMarkdown(entries)).not.toContain("never");
  // The shipped data file is read and every id it names is usable.
  const shipped = loadCategories(GUARD_DIR);
  expect(shipped.length).toBeGreaterThan(0);
  expect(shipped.map((rule) => rule.id)).toContain("spec");
  // Review #8: every shipped category places at least one planted section of its own kind.
  b.write("runs/y/insight.md", ["config", "tool", "check", "instruction"].map((source, n) =>
    `## F-${String(n).padStart(8, "9")} — a ${source === "check" ? "test suite" : source === "instruction" ? "spec" : source} case\n\n`
    + sectionBody().replace(/Source: instruction/, `Source: ${source}`) + "\n").join("\n")
    + `## F-99999994 — a guard alarm\n\n${sectionBody().replace(/Source: instruction/, "Source: check")}\n`
    + `## F-99999995 — my command chain\n\n${sectionBody()}\n`);
  const placed = new Set(rows(b, shipped).map((entry) => entry.category));
  for (const rule of shipped) expect(placed.has(rule.id)).toBe(true);
});

// ---- P6: the CLI in a temporary git root ---------------------------------------------------------------------------

test("P6 I1: insight index --json gives one object per section, with the file, ids, kind, checks, source, kinds, category", () => {
  const b = planted();
  const result = b.cli("insight", "index", "--json");
  expect(result.status).toBe(0);
  const parsed = JSON.parse(result.stdout) as { sections: IndexEntry[] };
  expect(parsed.sections).toHaveLength(3);
  expect(parsed.sections.map((entry) => entry.file)).toContain("runs/x/insight.md");
  for (const entry of parsed.sections) {
    expect(Object.keys(entry).sort())
      .toEqual(["category", "checks", "file", "ids", "kind", "optionKinds", "source"]);
  }
  expect(parsed.sections.find((entry) => entry.ids.includes("F-2b3c4d5e"))!.checks).toEqual(["R12.2-command-error"]);
});

test("P6 I1: the markdown table has one header row and one row per section, with the journal's check", () => {
  const b = planted();
  const result = b.cli("insight", "index");
  expect(result.status).toBe(0);
  const lines = result.stdout.trim().split("\n");
  expect(lines[0]).toBe("| file | ids | kind | check | source | options | category |");
  expect(lines).toHaveLength(5); // a header, a separator and one row per section
  expect(lines.some((line) => line.includes("R12.2-command-error"))).toBe(true);
  expect(lines.some((line) => line.includes("F-2b3c4d5e"))).toBe(true);
  expect(lines.some((line) => line.includes("| great |"))).toBe(true);
});

test("P6 I1: an empty root indexes to no rows and show says nothing matched", () => {
  const b = box();
  b.journal([]);
  expect(rows(b)).toEqual([]);
  expect(indexMarkdown([]).split("\n")).toHaveLength(2);
  expect(b.cli("insight", "index").stdout.trim().split("\n")).toHaveLength(2);
  expect(b.cli("insight", "show", "--category", "spec").stdout.trim()).toBe("no matching insight sections");
});
// COO, after mutant IM1 survived: the override must beat a rule that would place the section elsewhere.
test("I3: a config section marked `Category: spec` is spec, not config", () => {
  const b = box();
  b.write("runs/x/insight.md", `## F-3c4d5e6f — a quota setting\n\n${sectionBody().replace(/Source: instruction/, "Source: config")}\nCategory: spec\n`);
  b.journal([b.failure({ id: "F-3c4d5e6f", check: "R12.1-exit" })]);
  const rules: CategoryRule[] = [
    { id: "config", name: "the environment", sources: ["config"] },
    { id: "spec", name: "a spec was unclear", sources: ["instruction"] },
  ];
  expect(rows(b, rules).find((entry) => entry.ids[0] === "F-3c4d5e6f")!.category).toBe("spec");
});

// COO, after the dsh review (runs/20261016-six-experts/nodes/review.result.md).
test("review 1: an option label that is not a known kind never reaches the index", () => {
  const b = box();
  b.write("runs/x/insight.md", `## F-4d5e6f70 — a case\n\n${sectionBody([`1. [the cause is ${SECRET}] keep — evidence: e`, "2. [check] y — evidence: e"])}\n`);
  b.journal([b.failure({ id: "F-4d5e6f70", check: "R12.1-exit" })]);
  const entries = rows(b);
  expect(entries[0]!.optionKinds).toEqual(["-", "check"]);
  expect(indexMarkdown(entries)).not.toContain(SECRET);
});

test("review 2: a heading with no space after ## keeps its override and is shown", () => {
  const b = box();
  b.write("runs/x/insight.md", `##F-5e6f7081 — a quota setting\n\n${sectionBody().replace(/Source: instruction/, "Source: config")}\nCategory: spec\n\n`
    + `## F-6f708192 — another\n\n${sectionBody().replace(/Source: instruction/, "Source: tool")}\n`);
  b.journal([b.failure({ id: "F-5e6f7081", check: "R12.1-exit" }), b.failure({ id: "F-6f708192", check: "R12.1-exit" })]);
  const entries = rows(b);
  expect(entries.find((e) => e.ids[0] === "F-5e6f7081")!.category).toBe("spec");
  expect(entries.find((e) => e.ids[0] === "F-6f708192")!.category).toBe("tool");
  expect(showSections(b.root, entries, { categories: ["spec"], refs: [] })).toContain("F-5e6f7081");
});

test("review 3: a malformed regex in a category rule matches nothing instead of breaking the index", () => {
  const b = planted();
  const rules: CategoryRule[] = [{ id: "broken", name: "x", titles: ["([unclosed"] }, { id: "spec", name: "s", sources: ["instruction"] }];
  expect(() => rows(b, rules)).not.toThrow();
  expect(rows(b, rules).some((e) => e.category === "broken")).toBe(false);
});

// COO, after the trial: insights written by test agents inside an experiment's own folders are not the project's.
test("the index reads runs/<run>/insight*.md and .harness-guard/insights/, not insight files nested deeper", () => {
  const b = box();
  b.write("runs/x/insight.md", `## F-7a8b9c0d — top\n\n${sectionBody()}\n`);
  b.write("runs/x/e4/runs2/B3/insight.md", `## F-8b9c0d1e — nested\n\n${sectionBody()}\n`);
  b.write(".harness-guard/insights/g.md", `## F-9c0d1e2f — guard dir\n\n${sectionBody()}\n`);
  b.journal([]);
  const ids = rows(b).flatMap((e) => e.ids).sort();
  expect(ids).toEqual(["F-7a8b9c0d", "F-9c0d1e2f"]);
});
