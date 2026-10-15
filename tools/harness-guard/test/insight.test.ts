import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { answered, checkSection, findInsightFiles, openFailures, parseInsight } from "../src/insight.ts";
import type { FailureRecord, Finding, InsightOption, InsightSection } from "../src/types.ts";

const secret = "SECRET-PLANT-7f3a9c";
const first = "F-1a2b3c4d";
const second = "F-2b3c4d5e";
const third = "F-3c4d5e6f";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-"));
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

// ---- fixtures ------------------------------------------------------------------------------

function writeFile(name: string, text: string): string {
  const file = path.join(folder, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function whysList(count: number): string {
  return Array.from({ length: count }, (_, i) => `${i + 1}. why ${i + 1} of the fixture chain`).join("\n");
}

function optionsList(count: number): string {
  const kinds = ["rule", "check", "tool", "config-advice"];
  return Array.from(
    { length: count },
    (_, i) => `${i + 1}. [${kinds[i % kinds.length]}] option ${i + 1} of the fixture chain — evidence: runs/20260101/evidence-${i + 1}.md`,
  ).join("\n");
}

interface Body {
  whys?: number;
  source?: string | null;
  rootCause?: string | null;
  options?: string;
  labels?: { whys: string; source: string; rootCause: string; options: string };
}

// The body of one insight section, in the shape SPEC.md M3 describes.
function body(changes: Body = {}): string {
  const labels = changes.labels ?? { whys: "Whys:", source: "Source:", rootCause: "Root cause:", options: "Options:" };
  const lines = [labels.whys, whysList(changes.whys ?? 4)];
  if (changes.source !== null) lines.push("", `${labels.source} ${changes.source ?? "instruction"}`);
  if (changes.rootCause !== null) lines.push("", `${labels.rootCause} ${changes.rootCause ?? "the check was only prose"}`);
  lines.push("", labels.options, changes.options ?? optionsList(2));
  return lines.join("\n");
}

function document(heading: string, sections: string[] = [body()]): string {
  return ["# Insight notes", ...sections.map((text) => `## ${heading}\n\n${text}\n`)].join("\n");
}

function insightSection(changes: Partial<InsightSection> = {}): InsightSection {
  return {
    ids: [first],
    whys: ["why one of the fixture chain", "why two of the fixture chain", "why three of the fixture chain",
      "why four of the fixture chain"],
    source: "instruction",
    rootCause: "the check was only prose",
    options: [
      { kind: "rule", text: "name the check as a numbered step", evidence: "runs/20260101/step.md" },
      { kind: "check", text: "report the rule id in the report", evidence: "runs/20260101/report.md" },
    ],
    ...changes,
  };
}

function option(changes: Partial<InsightOption> = {}): InsightOption {
  return { kind: "rule", text: "name the check as a numbered step", evidence: "runs/20260101/step.md", ...changes };
}

function failure(changes: Partial<FailureRecord> = {}): FailureRecord {
  const id = changes.id ?? first;
  const evidence = `.harness-guard/evidence/${id}.json`;
  writeFile(path.join(".harness-guard", "evidence", `${id}.json`), JSON.stringify({ rule: "R12.1-exit", lengths: { stdout: 0 } }));
  return {
    kind: "failure",
    id,
    time: "2026-10-15T09:00:00Z",
    session: "s1",
    found_by: "guard",
    check: "R12.1-exit",
    input: "codex, output file answer.md",
    expected: "a non-empty answer file",
    actual: "the answer file was empty",
    engine: "codex",
    harness: "claude-code",
    reason: "the engine call produced no answer",
    evidence,
    ...changes,
  };
}

function writeJournal(records: unknown[]): void {
  const lines = records.map((record) => JSON.stringify(record)).join("\n");
  writeFile(path.join(".harness-guard", "journal.jsonl"), `${lines}\n`);
}

function gitRoot(): string {
  fs.mkdirSync(path.join(folder, ".harness-guard", "insights"), { recursive: true });
  fs.writeFileSync(path.join(folder, "marker.txt"), "fixture");
  const result = Bun.spawnSync(["git", "init", "--quiet", folder], { stdout: "ignore", stderr: "ignore" });
  if (result.exitCode !== 0) throw new Error("git init failed in the temporary folder");
  return folder;
}

// ---- assertions ---------------------------------------------------------------------------

function expectFailure(findings: Finding[], rule: string): void {
  expect(findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
}

function expectNoSecret(action: () => unknown): void {
  const printed: string[] = [];
  const spies = [
    spyOn(console, "log").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "warn").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(console, "error").mockImplementation((...args) => { printed.push(JSON.stringify(args)); }),
    spyOn(process.stdout, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
    spyOn(process.stderr, "write").mockImplementation((chunk) => { printed.push(String(chunk)); return true; }),
  ];
  let output: unknown;
  try {
    output = action();
  } finally {
    for (const spy of spies) spy.mockRestore();
  }
  expect(JSON.stringify(output)).not.toContain(secret);
  expect(printed.join("\n")).not.toContain(secret);
  const state = path.join(folder, ".harness-guard");
  if (fs.existsSync(state)) {
    for (const name of fs.readdirSync(state, { recursive: true, encoding: "utf8" })) {
      const file = path.join(state, name);
      if (fs.statSync(file).isFile()) expect(fs.readFileSync(file, "utf8")).not.toContain(secret);
    }
  }
}

describe("insight file discovery", () => {
  test("find: insight files under runs/ and .harness-guard/insights/ are found as relative paths", () => {
    const root = gitRoot();
    writeFile(path.join("runs", "20260101", "insight-first.md"), document(first));
    writeFile(path.join("runs", "20260101", "runs", "insight-nested.md"), document(second));
    writeFile(path.join(".harness-guard", "insights", "insight-third.md"), document(third));
    const found = findInsightFiles(root);
    expect(found).toContain(path.join("runs", "20260101", "insight-first.md"));
    expect(found).toContain(path.join("runs", "20260101", "runs", "insight-nested.md"));
    expect(found).toContain(path.join(".harness-guard", "insights", "insight-third.md"));
    for (const file of found) {
      expect(path.isAbsolute(file)).toBe(false);
      expect(fs.existsSync(path.join(root, file))).toBe(true);
    }
  });

  test("find: the returned paths are sorted", () => {
    const root = gitRoot();
    const written = ["h", "c", "a", "e", "g", "b", "d", "f"];
    for (const letter of written) writeFile(path.join("runs", "20260101", `insight-${letter}.md`), document(first));
    expect(findInsightFiles(root)).toEqual(
      ["a", "b", "c", "d", "e", "f", "g", "h"].map((letter) => path.join("runs", "20260101", `insight-${letter}.md`)),
    );
  });

  test("find: files outside the two insight patterns are ignored", () => {
    const root = gitRoot();
    writeFile(path.join("runs", "20260101", "insight-kept.md"), document(first));
    writeFile(path.join("runs", "20260101", "notes.md"), document(second));
    writeFile(path.join("runs", "20260101", "insight.txt"), document(third));
    writeFile(path.join(".harness-guard", "insights", "notes.md"), document(third));
    writeFile(path.join("src", "insight.ts"), "// not an insight\n");
    writeFile(path.join("runs", "20260101", "insight-log", "deep.md"), document(third));
    expect(findInsightFiles(root)).toEqual([path.join("runs", "20260101", "insight-kept.md")]);
  });

  test("find: a root with no insight files returns an empty list without throwing", () => {
    const root = gitRoot();
    writeFile(path.join("runs", "20260101", "notes.md"), "nothing to see");
    expect(findInsightFiles(root)).toEqual([]);
  });
});

describe("insight parsing", () => {
  test("parse: a complete document becomes one section with its labelled parts", () => {
    const sections = parseInsight(document(`${first} — short title`));
    expect(sections).toHaveLength(1);
    expect(sections[0].ids).toEqual([first]);
    expect(sections[0].whys).toHaveLength(4);
    expect(sections[0].source).toBe("instruction");
    expect(sections[0].rootCause).toBe("the check was only prose");
    expect(sections[0].options).toHaveLength(2);
    expect(sections[0].options.map((each: InsightOption) => each.kind)).toEqual(["rule", "check"]);
    expect(sections[0].options.map((each: InsightOption) => each.evidence)).toEqual([
      "runs/20260101/evidence-1.md",
      "runs/20260101/evidence-2.md",
    ]);
  });

  test("parse: a heading naming two failure ids yields both ids", () => {
    const sections = parseInsight(document(`${first}, ${second} — one run, two failures`));
    expect(sections).toHaveLength(1);
    expect(sections[0].ids).toEqual([first, second]);
  });

  test("parse: heading text after the ids is not read as an id", () => {
    const sections = parseInsight(document(`${first} — why the second gate never ran`));
    expect(sections[0].ids).toEqual([first]);
  });

  test("parse: the labels are matched case-insensitively at the start of a line", () => {
    const labels = { whys: "whys:", source: "SOURCE:", rootCause: "Root CAUSE:", options: "options:" };
    const sections = parseInsight(document(first, [body({ labels })]));
    expect(sections[0].whys).toHaveLength(4);
    expect(sections[0].source).toBe("instruction");
    expect(sections[0].rootCause).toBe("the check was only prose");
    expect(sections[0].options).toHaveLength(2);
  });

  test("parse: a root cause on the next non-empty line is read", () => {
    const section = `${body().replace(/Root cause:.*\n/, "Root cause:\n\nthe check was only prose\n")}`;
    const sections = parseInsight(document(first, [section]));
    expect(sections[0].rootCause).toBe("the check was only prose");
    expect(checkSection(sections[0])).toEqual([]);
  });

  test("parse: an option without evidence text is kept with empty evidence", () => {
    const options = ["1. [rule] name the check as a numbered step", "2. [check] report the rule id — evidence: runs/20260101/report.md"].join("\n");
    const sections = parseInsight(document(first, [body({ options })]));
    expect(sections[0].options).toHaveLength(2);
    expect(sections[0].options[0].kind).toBe("rule");
    expect(sections[0].options[0].evidence).toBe("");
    expect(sections[0].options[1].evidence).toBe("runs/20260101/report.md");
  });

  test("parse: a section ends where the next heading starts, and a heading with no id opens none", () => {
    const text = `${document(first)}\n## Summary of the run\n\nFree prose, ${second} is mentioned here.\n`;
    const sections = parseInsight(text);
    expect(sections).toHaveLength(1);
    expect(sections[0].whys).toHaveLength(4);
    expect(sections[0].options).toHaveLength(2);
    expect(checkSection(sections[0])).toEqual([]);
  });

  test("parse: two heading sections are parsed separately", () => {
    const text = `${document(first)}\n## ${second} — second failure\n\n${body({ whys: 2, source: null, rootCause: null, options: optionsList(4) })}\n`;
    const sections = parseInsight(text);
    expect(sections).toHaveLength(2);
    expect(sections[0].ids).toEqual([first]);
    expect(sections[1].ids).toEqual([second]);
    expect(sections[1].whys).toHaveLength(2);
    expect(sections[1].source).toBeNull();
    expect(sections[1].rootCause).toBeNull();
    expect(sections[1].options).toHaveLength(4);
  });

  test("parse: a heading with no failure id opens no section", () => {
    const sections = parseInsight(`# Insight notes\n\n## Summary of the run\n\nFree prose, ${first} is mentioned here.\n`);
    expect(sections).toEqual([]);
  });

  test("parse: text before the first heading belongs to no section", () => {
    const sections = parseInsight(`Prose mentioning ${second} before any heading.\n\n${document(first)}`);
    expect(sections).toHaveLength(1);
    expect(sections[0].ids).toEqual([first]);
  });

  test.each(["", "\n\n", "# Insight notes\n\nno ids here\n"])("parse: text %j holds no sections", (text) => {
    expect(parseInsight(text)).toEqual([]);
  });
});

describe("section checks", () => {
  test("check: a valid section has no findings", () => {
    expect(checkSection(insightSection())).toEqual([]);
  });

  test.each([3, 6])("check: %s whys is accepted", (count) => {
    expect(checkSection(insightSection({ whys: whysList(count).split("\n") }))).toEqual([]);
  });

  test.each([0, 2, 7])("check: %s whys fails R12.3-whys-count", (count) => {
    expectFailure(checkSection(insightSection({ whys: whysList(count).split("\n") })), "R12.3-whys-count");
  });

  test("check: no source fails R12.3-source", () => {
    expectFailure(checkSection(insightSection({ source: null })), "R12.3-source");
  });

  test("check: an unknown source fails R12.3-source", () => {
    expectFailure(checkSection(insightSection({ source: "policy" })), "R12.3-source");
  });

  test("check: an empty source fails R12.3-source", () => {
    expectFailure(checkSection(insightSection({ source: "" })), "R12.3-source");
  });

  test.each(["instruction", "check", "tool", "config"])("check: source %s is accepted", (source) => {
    expect(checkSection(insightSection({ source }))).toEqual([]);
  });

  test("check: no root cause fails R12.3-root-cause", () => {
    expectFailure(checkSection(insightSection({ rootCause: null })), "R12.3-root-cause");
  });

  test("check: an empty root cause fails R12.3-root-cause", () => {
    expectFailure(checkSection(insightSection({ rootCause: "" })), "R12.3-root-cause");
  });

  test.each([2, 3])("check: %s options is accepted", (count) => {
    const options = Array.from({ length: count }, (_, i) => option({ kind: "check", evidence: `runs/20260101/e-${i}.md` }));
    expect(checkSection(insightSection({ options }))).toEqual([]);
  });

  test.each([0, 1, 4])("check: %s options fails R12.3-options-count", (count) => {
    const options = Array.from({ length: count }, (_, i) => option({ evidence: `runs/20260101/e-${i}.md` }));
    expectFailure(checkSection(insightSection({ options })), "R12.3-options-count");
  });

  test("check: an option with no kind fails R12.3-option-kind", () => {
    const findings = checkSection(insightSection({ options: [option({ kind: "" }), option()] }));
    expectFailure(findings, "R12.3-option-kind");
    expect(findings).not.toContainEqual(expect.objectContaining({ rule: "R12.3-options-count" }));
  });

  test("check: an option with no evidence fails R12.3-option-evidence", () => {
    const findings = checkSection(insightSection({ options: [option({ evidence: "" }), option()] }));
    expectFailure(findings, "R12.3-option-evidence");
    expect(findings).not.toContainEqual(expect.objectContaining({ rule: "R12.3-option-kind" }));
  });

  test("check: an option with neither kind nor evidence reports both rules", () => {
    const findings = checkSection(insightSection({ options: [option({ kind: "", evidence: "" }), option()] }));
    expectFailure(findings, "R12.3-option-kind");
    expectFailure(findings, "R12.3-option-evidence");
  });

  test("check: every defect in a section is reported, each as a fail", () => {
    const findings = checkSection(insightSection({
      whys: whysList(2).split("\n"),
      source: null,
      rootCause: null,
      options: [option({ kind: "", evidence: "" })],
    }));
    for (const rule of ["R12.3-whys-count", "R12.3-source", "R12.3-root-cause", "R12.3-options-count", "R12.3-option-kind",
      "R12.3-option-evidence"]) expectFailure(findings, rule);
    for (const finding of findings) {
      expect(finding.severity).toBe("fail");
      expect(finding.message.length).toBeGreaterThan(0);
    }
  });

  test.each([
    ["forgot", "the model forgot the step"],
    ["careless", "the run was careless about the step"],
    ["I missed", "I missed the trap in the catalogue"],
    ["the model was wrong", "the model was wrong about the guard"],
  ])("check: a last why ending at the person (%s) warns and is labelled a heuristic", (_name, why) => {
    const whys = [...insightSection().whys.slice(0, 3), why];
    const findings = checkSection(insightSection({ whys }));
    const heuristic = findings.filter((finding: Finding) => finding.rule === "R12.3-why-ends-at-person");
    expect(heuristic).toHaveLength(1);
    expect(heuristic[0].severity).toBe("warn");
    expect(heuristic[0].message.toLowerCase()).toContain("heuristic");
    expect(heuristic[0].message).toContain(why);
  });

  test("check: a person-shaped why that is not the last one does not warn", () => {
    const whys = ["the model was wrong about the guard", ...insightSection().whys.slice(1, 4)];
    expect(checkSection(insightSection({ whys }))).toEqual([]);
  });

  test("check: the person heuristic never turns a valid section into a fail", () => {
    const findings = checkSection(insightSection({ whys: [...insightSection().whys.slice(0, 3), "I missed the step"] }));
    expect(findings.filter((finding: Finding) => finding.severity === "fail")).toEqual([]);
  });

  test("check: planted secret text never appears in findings, prints or guard files", () => {
    expectNoSecret(() => {
      const findings = checkSection(insightSection({
        whys: [`the log held the key ${secret}`, "the step skipped it"],
        rootCause: `the value ${secret} was pasted into the run`,
        options: [option({ kind: "", evidence: "" }), option({ text: secret })],
      }));
      expectFailure(findings, "R12.3-whys-count");
      expectFailure(findings, "R12.3-option-kind");
      expectFailure(findings, "R12.3-option-evidence");
      return findings;
    });
  });
});

describe("answered failures", () => {
  test("answered: a valid section answers its failure and gives the relative path", () => {
    const root = gitRoot();
    const file = path.join("runs", "20260101", "insight-gate.md");
    writeFile(file, document(first));
    const result = answered(root);
    expect(result.size).toBe(1);
    expect(result.get(first)).toBe(file);
  });

  test("answered: a section with fail findings does not answer its failure", () => {
    const root = gitRoot();
    writeFile(path.join("runs", "20260101", "insight-gate.md"), document(first, [body({ whys: 2 })]));
    expect(answered(root).has(first)).toBe(false);
  });

  test("answered: a warning-only section still answers its failure", () => {
    const root = gitRoot();
    const text = document(first, [body().replace("4. why 4 of the fixture chain", "4. I missed the step in the chain")]);
    writeFile(path.join("runs", "20260101", "insight-gate.md"), text);
    expect(answered(root).get(first)).toBe(path.join("runs", "20260101", "insight-gate.md"));
  });

  test("answered: the first file in sorted order that answers wins", () => {
    const root = gitRoot();
    const broken = path.join("runs", "20260101", "insight-a-broken.md");
    const valid = path.join("runs", "20260101", "insight-b-valid.md");
    const later = path.join("runs", "20260102", "insight-c-valid.md");
    writeFile(broken, document(first, [body({ options: optionsList(4) })]));
    writeFile(valid, document(first));
    writeFile(later, document(first));
    expect(answered(root).get(first)).toBe(valid);
  });

  test("answered: a section naming two failures answers both", () => {
    const root = gitRoot();
    writeFile(path.join("runs", "20260101", "insight-pair.md"), document(`${first}, ${second} — one run, two failures`));
    const result = answered(root);
    expect(result.get(first)).toBe(path.join("runs", "20260101", "insight-pair.md"));
    expect(result.get(second)).toBe(path.join("runs", "20260101", "insight-pair.md"));
  });

  test("answered: a failure with no insight file is not answered", () => {
    const root = gitRoot();
    writeFile(path.join("runs", "20260101", "notes.md"), document(first));
    expect(answered(root).has(first)).toBe(false);
    expect(answered(root).size).toBe(0);
  });

  test("answered: a root with no insight files yields an empty map", () => {
    const root = gitRoot();
    expect(answered(root).size).toBe(0);
  });
});

describe("open failures", () => {
  test("open: a failure with no insight file is open", () => {
    const root = gitRoot();
    writeJournal([failure()]);
    expect(openFailures(root, null).map((record: FailureRecord) => record.id)).toEqual([first]);
  });

  test("open: a failure answered by a valid section is not open", () => {
    const root = gitRoot();
    writeJournal([failure()]);
    writeFile(path.join("runs", "20260101", "insight-gate.md"), document(first));
    expect(openFailures(root, null)).toEqual([]);
  });

  test.each([
    ["2 whys", body({ whys: 2 })],
    ["7 whys", body({ whys: 7 })],
    ["no source", body({ source: null })],
    ["an unknown source", body({ source: "policy" })],
    ["no root cause", body({ rootCause: null })],
    ["1 option", body({ options: optionsList(1) })],
    ["4 options", body({ options: optionsList(4) })],
    ["an option with no kind", body({ options: "1. name the check as a step — evidence: runs/20260101/step.md\n2. [check] report the rule id — evidence: runs/20260101/report.md" })],
    ["an option with no evidence", body({ options: "1. [rule] name the check as a step\n2. [check] report the rule id — evidence: runs/20260101/report.md" })],
  ])("open: a section with %s leaves its failure open", (_name, section) => {
    const root = gitRoot();
    writeJournal([failure()]);
    writeFile(path.join("runs", "20260101", "insight-gate.md"), document(first, [section]));
    expect(openFailures(root, null).map((record: FailureRecord) => record.id)).toEqual([first]);
  });

  test("open: a section answering two failures closes both", () => {
    const root = gitRoot();
    writeJournal([failure({ id: first }), failure({ id: second })]);
    writeFile(path.join("runs", "20260101", "insight-pair.md"), document(`${first}, ${second} — one run, two failures`));
    expect(openFailures(root, null)).toEqual([]);
  });

  test("open: one section never answers a failure it does not name", () => {
    const root = gitRoot();
    writeJournal([failure({ id: first }), failure({ id: second })]);
    writeFile(path.join("runs", "20260101", "insight-gate.md"), document(first));
    expect(openFailures(root, null).map((record: FailureRecord) => record.id)).toEqual([second]);
  });

  test("open: the session filter returns only that session's open failures", () => {
    const root = gitRoot();
    writeJournal([failure({ id: first, session: "s1" }), failure({ id: second, session: "s2" })]);
    writeFile(path.join("runs", "20260101", "insight-gate.md"), document(first));
    expect(openFailures(root, "s1").map((record: FailureRecord) => record.id)).toEqual([]);
    expect(openFailures(root, "s2").map((record: FailureRecord) => record.id)).toEqual([second]);
    expect(openFailures(root, null).map((record: FailureRecord) => record.id)).toEqual([second]);
  });

  test("open: the session filter still leaves an unanswered failure open", () => {
    const root = gitRoot();
    writeJournal([failure({ id: first, session: "s1" })]);
    expect(openFailures(root, "s1").map((record: FailureRecord) => record.id)).toEqual([first]);
  });

  test("open: records that are not failures are never open", () => {
    const root = gitRoot();
    writeJournal([
      { kind: "touched", time: "2026-10-15T09:00:00Z", session: "s1", path: "runs/20260101/plan.register.yaml" },
      { kind: "guard_error", time: "2026-10-15T09:00:00Z", session: "s1", message: "a guard bug" },
    ]);
    expect(openFailures(root, null)).toEqual([]);
  });

  test("open: a root with no journal yields no open failures", () => {
    const root = gitRoot();
    expect(openFailures(root, null)).toEqual([]);
  });
});