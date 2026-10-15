// Acceptance expectations: SPEC.md S4, M3, and Round 3 C5/C6.
import { afterEach, beforeEach, describe, expect, spyOn, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { answered, checkGreatSection, checkSection, greatAnswered, parseInsight } from "../src/insight.ts";
import type { Finding, InsightSection } from "../src/types.ts";

const pathFile = "runs/task/success-path.yaml";
const failureId = "F-1a2b3c4d";
const secret = "SECRET-PLANT-7f3a9c";
let folder: string;

beforeEach(() => {
  folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-round5-insight-"));
});

afterEach(() => {
  fs.rmSync(folder, { recursive: true, force: true });
});

function writeFixture(file: string, text: string): void {
  const absolute = path.join(folder, file);
  fs.mkdirSync(path.dirname(absolute), { recursive: true });
  fs.writeFileSync(absolute, text);
}

function greatOptions(count = 1, kind = "check"): string {
  return Array.from({ length: count }, (_, index) =>
    `${index + 1}. [${kind}] retain measured validation — evidence: runs/task/measurements.md`,
  ).join("\n");
}

function greatSection(body = `Comparison: fewer retries than the parent\nCause: validation ran before dispatch\nOptions:\n${greatOptions()}`, file = pathFile): string {
  return `## great: ${file}\n\n${body}\n`;
}

function failureSection(): string {
  return `## ${failureId}\n
Whys:
1. The output was empty.
2. The call had no stdin redirect.
3. The instruction omitted the input check.
Source: instruction
Root cause: the call template omitted the redirect
Options:
1. [rule] add the redirect — evidence: runs/task/command-counts.json
2. [check] check stdin — evidence: runs/task/replay-counts.json
`;
}

function parseSingleSection(text: string): ReturnType<typeof parseInsight>[number] {
  const sections = parseInsight(text);
  expect(sections).toHaveLength(1);
  return sections[0]!;
}

function expectFail(findings: Finding[], rule: string): void {
  expect(findings).toContainEqual(expect.objectContaining({ rule, severity: "fail" }));
}

const invalidGreatBodies: [string, string, string][] = [
  ["no comparison", `Cause: early validation\nOptions:\n${greatOptions()}`, "R12.7-great-comparison"],
  ["empty comparison", `Comparison:\nCause: early validation\nOptions:\n${greatOptions()}`, "R12.7-great-comparison"],
  ["blank comparison", `Comparison:   \nCause: early validation\nOptions:\n${greatOptions()}`, "R12.7-great-comparison"],
  ["no cause", `Comparison: fewer retries\nOptions:\n${greatOptions()}`, "R12.7-great-cause"],
  ["empty cause", `Comparison: fewer retries\nCause:\nOptions:\n${greatOptions()}`, "R12.7-great-cause"],
  ["blank cause", `Comparison: fewer retries\nCause:   \nOptions:\n${greatOptions()}`, "R12.7-great-cause"],
  ["no options label", "Comparison: fewer retries\nCause: early validation", "R12.7-great-options"],
  ["zero options", "Comparison: fewer retries\nCause: early validation\nOptions:", "R12.7-great-options"],
  ["four options", `Comparison: fewer retries\nCause: early validation\nOptions:\n${greatOptions(4)}`, "R12.7-great-options"],
  ["missing kind", "Comparison: fewer retries\nCause: early validation\nOptions:\n1. retain validation — evidence: runs/task/counts.json", "R12.7-great-options"],
  ["unknown kind", `Comparison: fewer retries\nCause: early validation\nOptions:\n${greatOptions(1, "policy")}`, "R12.7-great-options"],
  ["failure-only config-advice kind", `Comparison: fewer retries\nCause: early validation\nOptions:\n${greatOptions(1, "config-advice")}`, "R12.7-great-options"],
  ["missing evidence", "Comparison: fewer retries\nCause: early validation\nOptions:\n1. [check] retain validation", "R12.7-great-options"],
  ["empty evidence", "Comparison: fewer retries\nCause: early validation\nOptions:\n1. [check] retain validation — evidence:   ", "R12.7-great-options"],
  ["one invalid item among valid options", `Comparison: fewer retries\nCause: early validation\nOptions:\n${greatOptions(2)}\n3. [tool] retain replay`, "R12.7-great-options"],
];

describe("Round 5 S4 great section validation", () => {
  test.each([[1], [2], [3]])("accepts %s numbered options without failure-only fields", (count) => {
    const section = parseSingleSection(greatSection(
      `Comparison: fewer retries\nCause: early validation\nOptions:\n${greatOptions(count)}`,
    ));
    expect(section.ids).toEqual([]);
    expect(section.options).toHaveLength(count);
    expect(checkGreatSection(section)).toEqual([]);
  });

  test.each([["rule"], ["check"], ["tool"]])("accepts [%s] options", (kind) => {
    const section = parseSingleSection(greatSection(
      `Comparison: fewer retries\nCause: early validation\nOptions:\n${greatOptions(1, kind)}`,
    ));
    expect(section.options[0]!.kind).toBe(kind);
    expect(section.options[0]!.evidence).toBe("runs/task/measurements.md");
    expect(checkGreatSection(section)).toEqual([]);
  });

  test.each(invalidGreatBodies)("rejects %s and does not count its path as answered", (_name, body, rule) => {
    const text = greatSection(body);
    expectFail(checkGreatSection(parseSingleSection(text)), rule);
    writeFixture("runs/task/insight-invalid.md", text);
    expect(greatAnswered(folder).has(pathFile)).toBe(false);
  });

  test("reports comparison, cause and options defects together", () => {
    const findings = checkGreatSection(parseSingleSection(greatSection("Options:")));
    for (const rule of ["R12.7-great-comparison", "R12.7-great-cause", "R12.7-great-options"]) {
      expectFail(findings, rule);
    }
  });

  test("C6 blank lines and indented evidence continuations apply to great options", () => {
    const section = parseSingleSection(greatSection(`Comparison: fewer retries
Cause: early validation
Options:

1. [rule] retain validation
   evidence: runs/task/rule-counts.json
2. [tool] retain replay
   evidence: runs/task/replay-counts.json
Summary: the list has ended
3. [policy] this is outside the options list`));
    expect(section.options).toHaveLength(2);
    expect(section.options.map((option) => option.evidence)).toEqual([
      "runs/task/rule-counts.json", "runs/task/replay-counts.json",
    ]);
    expect(checkGreatSection(section)).toEqual([]);
  });
});

describe("Round 5 S4 separation from failure sections", () => {
  test.each([[false], [true]])("mixed document keeps sections apart (great first: %s)", (greatFirst) => {
    const text = greatFirst
      ? `${greatSection()}\n${failureSection()}`
      : `${failureSection()}\n${greatSection()}`;
    const sections = parseInsight(text);
    expect(sections).toHaveLength(2);
    const failure: InsightSection = sections[greatFirst ? 1 : 0]!;
    const great = sections[greatFirst ? 0 : 1]!;
    expect(failure.ids).toEqual([failureId]);
    expect(failure.whys).toHaveLength(3);
    expect(failure.options).toHaveLength(2);
    expect(checkSection(failure)).toEqual([]);
    expect(great.ids).toEqual([]);
    expect(great.options).toHaveLength(1);
    expect(checkGreatSection(great)).toEqual([]);
    const insightFile = "runs/task/insight-mixed.md";
    writeFixture(insightFile, text);
    expect([...greatAnswered(folder)]).toEqual([pathFile]);
    expect([...answered(folder)]).toEqual([[failureId, insightFile]]);
  });

  test("a failure section carrying great labels is never read as a great section", () => {
    writeFixture("runs/task/insight-failure.md", `${failureSection()}\nComparison: fewer retries\nCause: early validation\n`);
    expect(greatAnswered(folder).size).toBe(0);
    expect(answered(folder).has(failureId)).toBe(true);
  });

  test("a great heading containing a failure id in its path still has empty ids", () => {
    const file = `runs/${failureId}/success-path.yaml`;
    const section = parseSingleSection(greatSection(undefined, file));
    expect(section.ids).toEqual([]);
    writeFixture("runs/task/insight-great.md", greatSection(undefined, file));
    expect([...greatAnswered(folder)]).toEqual([file]);
    expect(answered(folder).size).toBe(0);
  });

  test("adjacent great sections cannot borrow missing cause or comparison", () => {
    writeFixture("runs/task/insight-adjacent.md",
      greatSection(`Comparison: fewer retries\nOptions:\n${greatOptions()}`, pathFile)
      + greatSection(`Cause: early validation\nOptions:\n${greatOptions()}`, "runs/other/success-path.yaml"));
    expect(greatAnswered(folder).size).toBe(0);
  });
});

describe("Round 5 S4 greatAnswered discovery", () => {
  test("an empty root has no answered paths", () => {
    expect(greatAnswered(folder)).toEqual(new Set<string>());
  });

  test.each([
    ["runs/insight.md"],
    ["runs/task/nested/insight-success.md"],
    [".harness-guard/insights/notes.md"],
  ])("finds a valid great section in %s", (file) => {
    writeFixture(file, greatSection());
    expect(greatAnswered(folder)).toEqual(new Set([pathFile]));
  });

  test("ordinary Markdown outside insight discovery does not answer paths", () => {
    writeFixture("runs/task/notes.md", greatSection());
    writeFixture("insight.md", greatSection());
    writeFixture(".harness-guard/notes.md", greatSection());
    expect(greatAnswered(folder).size).toBe(0);
  });

  test("deduplicates paths and includes each valid section across files", () => {
    const otherPath = "runs/other/success-path-alternative.yaml";
    writeFixture("runs/task/insight-a.md", greatSection());
    writeFixture(".harness-guard/insights/notes.md", greatSection() + greatSection(undefined, otherPath));
    expect(greatAnswered(folder)).toEqual(new Set([pathFile, otherPath]));
  });

  test("an invalid section does not hide a later valid answer for the same path", () => {
    writeFixture("runs/task/insight-a-invalid.md", greatSection("Options:"));
    writeFixture("runs/task/insight-b-valid.md", greatSection());
    expect(greatAnswered(folder)).toEqual(new Set([pathFile]));
  });

  test("a valid section answers only its heading's path", () => {
    writeFixture("runs/task/insight-one.md", greatSection());
    expect(greatAnswered(folder).has("runs/other/success-path.yaml")).toBe(false);
  });

  test("planted command, prompt and output text is absent from diagnostics, prints and new files", () => {
    const text = greatSection(`Comparison: prompt ${secret}\nCause: output ${secret}\nOptions:\n1. [${secret}] command ${secret}`);
    const insightFile = "runs/task/insight-secret.md";
    writeFixture(insightFile, text);
    const log = spyOn(console, "log").mockImplementation(() => {});
    const error = spyOn(console, "error").mockImplementation(() => {});
    const warn = spyOn(console, "warn").mockImplementation(() => {});
    try {
      const findings = checkGreatSection(parseSingleSection(text));
      const paths = greatAnswered(folder);
      expect(JSON.stringify(findings)).not.toContain(secret);
      expect(JSON.stringify([...paths])).not.toContain(secret);
      for (const calls of [log.mock.calls, error.mock.calls, warn.mock.calls]) {
        expect(JSON.stringify(calls)).not.toContain(secret);
      }
      expectFail(findings, "R12.7-great-options");
      expect(paths.size).toBe(0);
      expect(fs.readFileSync(path.join(folder, insightFile), "utf8")).toBe(text);
      for (const file of fs.readdirSync(folder, { recursive: true, encoding: "utf8" })) {
        const absolute = path.join(folder, file);
        if (file !== insightFile && fs.statSync(absolute).isFile()) {
          expect(fs.readFileSync(absolute, "utf8")).not.toContain(secret);
        }
      }
    } finally {
      log.mockRestore();
      error.mockRestore();
      warn.mockRestore();
    }
  });
});
