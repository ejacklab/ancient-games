// Acceptance expectations come from SPEC.md, Round 18 (L1–L6 and every Fails-if of that round), read together with
// the round's own behaviours: the lessons store beside the guard, the PreToolUse holds of Rounds 13 and 15, and the
// deny of M5. Each early return of handlePreToolUse gets a case of its own.
import { afterEach, beforeEach, describe, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { LESSON_HOLD, handleHook } from "../src/hooks.ts";
import { checkLessons, factsFor, isTestFile, lessonLine, lessonsFor, matches, parseLesson, readLessons, shownFolder, takeUnshown } from "../src/lessons.ts";
import { readJournal } from "../src/journal.ts";
import type { HookEnv, HookResult } from "../src/types.ts";

const CLI = path.join(import.meta.dirname, "..", "src", "cli.ts");
const time = "2026-10-17T15:00:00.000Z";
const session = "round18-crossed-session";
const otherSession = "round18-crossed-other";

let root: string;   // a temporary git root, the guard's guardRoot
let store: string;  // a temporary lessons store
let env: HookEnv;

function write(file: string, text: string): string {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text);
  return file;
}

function lesson(slug: string, front: string[], body: string): string {
  return write(path.join(store, `${slug}.md`), `---\n${front.join("\n")}\n---\n\n${body}\n`);
}

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "hg18c-"));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  store = fs.mkdtempSync(path.join(os.tmpdir(), "hg18s-"));
  env = { cwd: root, running: [], now: () => new Date(time), lessons: store };
  // A project fact for one file in one folder (L2), and prose that readers must ignore.
  write(path.join(root, "fixes.md"), "a fix, read by a clean grep\n");
  write(path.join(root, "work", "LESSONS.md"), [
    "Notes for the folder, in prose, which no reader uses.",
    "- `alpha.ts` — alpha parses the flag before it writes.",
    "- `beta.ts` — beta writes last.",
    "- not-a-fact.ts — this line has no backticks, so it is prose too.",
  ].join("\n") + "\n");
  write(path.join(root, "other", "LESSONS.md"), "- `alpha.ts` — a fact in another folder is not this file's.\n");
  lesson("edit-any-code", ["agents: [all]", "kinds: [code-edit]", "from: runs/x/insight.md#F-00000001"],
    "Name the thing you change before you change it.");
  lesson("any-test-file", ["agents: [all]", "kinds: [test]", "from: runs/x/insight.md#F-00000002"],
    "A test run that fails is a failure, even when the pipe hides the exit.");
  lesson("engine-call-rule", ["agents: [claude-main]", "kinds: [engine-call]", "commands: [grep]", "from: runs/x/insight.md#F-00000003"],
    "Feed an engine from a file, not from a heredoc.");
  lesson("brief-rule", ["agents: [all]", "kinds: [brief]", "from: runs/x/insight.md#F-00000004"],
    "List the unclear spots before dispatching work.");
  lesson("scoped-path", ["agents: [all]", "kinds: [engine-call]", "paths: [src/scoped/**]", "from: runs/x/insight.md#F-00000005"],
    "This path's rules live in its own folder.");
  lesson("opencode-only", ["agents: [opencode]", "kinds: [code-edit, brief]", "from: runs/x/insight.md#F-00000006"],
    "A lesson for another agent type only.");
  lesson("already-checked", ["agents: [all]", "kinds: [code-edit]", "enforced_by: test/round18-crossed.test.ts",
    "from: runs/x/insight.md#F-00000007"], "The line count must match the reported count.");
});

afterEach(() => {
  fs.rmSync(root, { recursive: true, force: true });
  fs.rmSync(store, { recursive: true, force: true });
});

// ---- payload helpers -----------------------------------------------------------------------------------------------

function pre(tool: string, input: Record<string, unknown>, id = session): Record<string, unknown> {
  return { hook_event_name: "PreToolUse", session_id: id, cwd: root, tool_name: tool, tool_input: input };
}

function run(payload: Record<string, unknown>, id = session): HookResult {
  return handleHook({ ...payload, session_id: id }, env);
}

function reasons(result: HookResult): string[] {
  if (result.stdout === "") return [];
  const parsed = JSON.parse(result.stdout) as { hookSpecificOutput?: { permissionDecisionReason?: string } };
  return (parsed.hookSpecificOutput?.permissionDecisionReason ?? "").split("\n");
}

function hold(result: HookResult): string[] {
  expect(result.exitCode).toBe(0);
  expect(result.stderr).toBe("");
  expect(JSON.parse(result.stdout).hookSpecificOutput.permissionDecision).toBe("deny");
  const lines = reasons(result);
  expect(lines[0]).toBe(LESSON_HOLD);
  return lines.slice(1);
}

function cli(args: string[]): { exitCode: number | null; out: string } {
  const result = spawnSync(process.execPath, [CLI, ...args], { cwd: root, encoding: "utf8", timeout: 20000 });
  return { exitCode: result.status, out: `${result.stdout}${result.stderr}` };
}

// ---- L1 a lesson file ----------------------------------------------------------------------------------------------

describe("L1 a lesson file", () => {
  test("a file with front matter, the required keys and a body parses into its fields, defaults filled", () => {
    const parsed = parseLesson(lesson("parse-me", [
      "agents: [claude-main, codex]", "kinds: [test, code-edit]", "paths: [src/**, test/**]",
      "commands: [bun]", "from: runs/x/insight.md#F-1a2b3c4d", "enforced_by: a check",
    ], "The body is the lesson text."));
    expect(parsed).toMatchObject({
      slug: "parse-me", agents: ["claude-main", "codex"], kinds: ["test", "code-edit"],
      paths: ["src/**", "test/**"], commands: ["bun"], from: "runs/x/insight.md#F-1a2b3c4d",
      enforcedBy: "a check", text: "The body is the lesson text.",
    });
  });

  test("paths, commands and enforced_by default to empty", () => {
    const parsed = parseLesson(lesson("bare", ["agents: [all]", "kinds: [brief]", "from: memory.md"], "Just a text."));
    expect(parsed).toMatchObject({ paths: [], commands: [], enforcedBy: "" });
  });

  test("each broken shape is reported with its reason, never silently dropped", () => {
    const cases: [string, string, string, RegExp][] = [
      ["Bad_Name", "agents: [all]\nkinds: [brief]\nfrom: memory.md", "Some text.", /slug/],
      ["no-front-matter", "", "Some text.", /front matter/],
      ["empty-agents", "agents: []\nkinds: [brief]\nfrom: memory.md", "Some text.", /agents/],
      ["unknown-agent", "agents: [gemini]\nkinds: [brief]\nfrom: memory.md", "Some text.", /unknown agent gemini/],
      ["empty-kinds", "agents: [all]\nkinds: []\nfrom: memory.md", "Some text.", /kinds/],
      ["unknown-kind", "agents: [all]\nkinds: [proof]\nfrom: memory.md", "Some text.", /unknown kind proof/],
      ["no-from", "agents: [all]\nkinds: [brief]", "Some text.", /from/],
      ["empty-body", "agents: [all]\nkinds: [brief]\nfrom: memory.md", "   \n", /lesson text/],
      ["bad-paths", "agents: [all]\nkinds: [brief]\npaths: src/a\nfrom: memory.md", "Some text.", /paths/],
      ["bad-yaml", "agents: [all\nkinds:", "Some text.", /YAML/],
    ];
    for (const [slug, front, body, reason] of cases) {
      const file = slug === "no-front-matter"
        ? write(path.join(store, `${slug}.md`), "agents: [all]\n")
        : write(path.join(store, `${slug}.md`), `---\n${front}\n---\n\n${body}`);
      const parsed = parseLesson(file) as { file: string; reason: string };
      expect(parsed.reason).toMatch(reason);
      expect(parsed.file).toBe(file);
    }
  });

  test("readLessons skips an invalid file and checkLessons names it with its reason (Fails-if)", () => {
    const broken = write(path.join(store, "broken.md"), "no front matter here\n");
    const slugs = readLessons(store).map((entry) => entry.slug);
    expect(slugs).toContain("edit-any-code");
    expect(slugs).not.toContain("broken");
    expect(slugs).toEqual([...slugs].sort());
    const invalid = checkLessons(store);
    expect(invalid).toEqual([{ file: broken, reason: "no front matter between two --- lines" }]);
  });

  test("a store that is not there reads as empty rather than throwing", () => {
    expect(readLessons(path.join(root, "no-such-store"))).toEqual([]);
    expect(checkLessons(path.join(root, "no-such-store"))).toEqual([]);
  });
});

// ---- L2 a project fact ---------------------------------------------------------------------------------------------

describe("L2 a project fact", () => {
  test("only the lines naming that file in its own folder are its facts", () => {
    expect(factsFor(path.join(root, "work", "alpha.ts"))).toEqual([
      { file: path.join(root, "work", "alpha.ts"), fact: "alpha parses the flag before it writes." },
    ]);
    expect(factsFor(path.join(root, "work", "beta.ts")).map((fact) => fact.fact)).toEqual(["beta writes last."]);
  });

  test("prose lines are ignored, and a file the LESSONS.md does not name has no fact", () => {
    expect(factsFor(path.join(root, "work", "not-a-fact.ts"))).toEqual([]);
    expect(factsFor(path.join(root, "work", "LESSONS.md"))).toEqual([]);
    expect(factsFor(path.join(root, "work", "never-heard-of.ts"))).toEqual([]);
  });

  test("a fact in another folder does not reach a file of the same name (Fails-if)", () => {
    expect(factsFor(path.join(root, "other", "alpha.ts"))).toEqual([
      { file: path.join(root, "other", "alpha.ts"), fact: "a fact in another folder is not this file's." },
    ]);
    expect(factsFor(path.join(root, "other", "alpha.ts"))).not.toEqual(factsFor(path.join(root, "work", "alpha.ts")));
  });

  test("a folder with no LESSONS.md has no facts", () => {
    expect(factsFor(path.join(root, "nowhere", "gamma.ts"))).toEqual([]);
  });
});

// ---- L3 which lessons match ----------------------------------------------------------------------------------------

describe("L3 which lessons match", () => {
  const byslug = (result: ReturnType<typeof lessonsFor>) => result.lessons.map((entry) => entry.slug);

  test("isTestFile counts a test or tests segment, .test., _test. and a test_ name", () => {
    for (const file of ["test/a.ts", "tests/b.ts", "src/deep/tests/c.ts", "src/d.test.ts", "pkg/e_test.go", "pkg/test_f.py"]) {
      expect(isTestFile(file)).toBe(true);
    }
    for (const file of ["src/a.ts", "src/latest/b.ts", "src/testing.ts", "src/atest.ts", "tester.ts"]) {
      expect(isTestFile(file)).toBe(false);
    }
  });

  test("agents all or the agent itself, and never another agent's lesson", () => {
    const query = { agent: "claude-main", paths: ["work/alpha.ts"], root };
    expect(byslug(lessonsFor(store, query))).toContain("edit-any-code");
    expect(byslug(lessonsFor(store, query))).not.toContain("opencode-only");
    expect(byslug(lessonsFor(store, { agent: "opencode", paths: ["work/alpha.ts"], root }))).toContain("opencode-only");
  });

  test("a test file matches a test lesson; any other file matches a code-edit lesson", () => {
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: ["pkg/x.test.ts"], root }))).toContain("any-test-file");
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: ["pkg/x.test.ts"], root }))).not.toContain("edit-any-code");
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: ["src/a.ts"], root }))).toContain("edit-any-code");
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: ["src/a.ts"], root }))).not.toContain("any-test-file");
  });

  test("a path glob matches by its path relative to the git root", () => {
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: ["src/scoped/deep/a.ts"], root }))).toContain("scoped-path");
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: ["src/other/deep/a.ts"], root }))).not.toContain("scoped-path");
    expect(byslug(lessonsFor(store, { agent: "claude-main", paths: [path.join(root, "src/scoped/deep/a.ts")], root }))).toContain("scoped-path");
  });

  test("a command word matches, and a kind given matches", () => {
    expect(byslug(lessonsFor(store, { agent: "claude-main", commands: ["grep"], root }))).toContain("engine-call-rule");
    expect(byslug(lessonsFor(store, { agent: "claude-main", commands: ["ls"], root }))).not.toContain("engine-call-rule");
    expect(byslug(lessonsFor(store, { agent: "claude-main", kinds: ["brief"], root }))).toContain("brief-rule");
    expect(byslug(lessonsFor(store, { agent: "claude-main", kinds: ["command"], root }))).not.toContain("brief-rule");
  });

  test("a lesson with enforced_by is given as its pointer, else as its text and slug", () => {
    const query = { agent: "claude-main", paths: ["src/scoped/a.ts"], root };
    const found = lessonsFor(store, query).lessons;
    expect(lessonLine(found.find((entry) => entry.slug === "edit-any-code")!)).toBe(
      "- Name the thing you change before you change it. (edit-any-code)");
    expect(lessonLine(found.find((entry) => entry.slug === "already-checked")!)).toBe(
      "- already-checked: enforced by test/round18-crossed.test.ts");
  });

  test("matches is the single decision; no query at all matches nothing", () => {
    const only = readLessons(store).find((entry) => entry.slug === "brief-rule")!;
    expect(matches(only, { agent: "claude-main", root })).toBe(false);
    expect(matches(only, { agent: "codex", kinds: ["brief"], root })).toBe(true);
    expect(lessonsFor(store, { agent: "claude-main", root })).toEqual({ lessons: [], facts: [] });
  });
});

// ---- L4 lessons for and lessons check ------------------------------------------------------------------------------

describe("L4 the CLI", () => {
  test("lessons for prints - <text> (<slug>) per lesson and - <file>: <fact> per fact, exit 0", () => {
    const result = cli(["lessons", "for", "--agent", "claude-main", "--kinds", "brief", "--paths", "work/alpha.ts", "--dir", store]);
    expect(result.exitCode).toBe(0);
    const lines = result.out.trim().split("\n");
    expect(lines).toEqual([
      "- already-checked: enforced by test/round18-crossed.test.ts",
      "- List the unclear spots before dispatching work. (brief-rule)",
      "- Name the thing you change before you change it. (edit-any-code)",
      "- work/alpha.ts: alpha parses the flag before it writes.",
    ]);
  });

  test("the kind filter, the command filter and the path filter each cut the list", () => {
    const briefOnly = cli(["lessons", "for", "--agent", "claude-main", "--kinds", "brief", "--dir", store]);
    expect(briefOnly.exitCode).toBe(0);
    expect(briefOnly.out.trim().split("\n")).toEqual(["- List the unclear spots before dispatching work. (brief-rule)"]);

    const byCommand = cli(["lessons", "for", "--agent", "claude-main", "--commands", "grep", "--dir", store]);
    expect(byCommand.out.trim().split("\n")).toEqual(["- Feed an engine from a file, not from a heredoc. (engine-call-rule)"]);

    const byPath = cli(["lessons", "for", "--agent", "claude-main", "--paths", "pkg/a.test.ts", "--dir", store]);
    expect(byPath.out.trim().split("\n")).toEqual([
      "- A test run that fails is a failure, even when the pipe hides the exit. (any-test-file)",
    ]);
  });

  test("nothing matching prints nothing and exits 0", () => {
    const result = cli(["lessons", "for", "--agent", "dsh", "--kinds", "command", "--dir", store]);
    expect(result.exitCode).toBe(0);
    expect(result.out).toBe("");
  });

  test("an unknown agent or kind is a usage error (exit 2), never exit 0 (Fails-if)", () => {
    for (const args of [
      ["lessons", "for", "--agent", "gemini", "--dir", store],
      ["lessons", "for", "--agent", "all", "--dir", store],
      ["lessons", "for", "--agent", "claude-main", "--kinds", "proof", "--dir", store],
      ["lessons", "for", "--dir", store],
    ]) {
      const result = cli(args);
      expect(result.exitCode).toBe(2);
      expect(result.out).not.toBe("");
    }
  });

  test("lessons check reports each invalid file with its reason and exits 1; a clean store exits 0", () => {
    const broken = write(path.join(store, "broken.md"), "agents: [all]\n");
    const bad = cli(["lessons", "check", "--dir", store]);
    expect(bad.exitCode).toBe(1);
    expect(bad.out.trim()).toBe(`${broken}: no front matter between two --- lines`);

    fs.rmSync(broken);
    const clean = cli(["lessons", "check", "--dir", store]);
    expect(clean.exitCode).toBe(0);
    expect(clean.out.trim()).toBe(`lessons ok: ${readLessons(store).length} in ${store}`);
  });
});

// ---- L5 and L6 the hook gives them by holding the call once --------------------------------------------------------

describe("L5 and L6 the hook", () => {
  test("a Write holds the matching lessons and that file's facts, all in one hold", () => {
    const lines = hold(run(pre("Write", { file_path: "work/alpha.ts" })));
    expect(lines).toContain("- Name the thing you change before you change it. (edit-any-code)");
    expect(lines).toContain("- work/alpha.ts: alpha parses the flag before it writes.");
  });

  test("Edit and MultiEdit are held the same way", () => {
    expect(hold(run(pre("Edit", { file_path: "work/alpha.ts" })))).toContain("- work/alpha.ts: alpha parses the flag before it writes.");
    expect(hold(run(pre("MultiEdit", { file_path: "work/beta.ts" })))).toContain("- work/beta.ts: beta writes last.");
  });

  test("a test file is given the test lesson, not the code-edit one", () => {
    const lines = hold(run(pre("Write", { file_path: "pkg/x.test.ts" })));
    expect(lines).toContain("- A test run that fails is a failure, even when the pipe hides the exit. (any-test-file)");
    expect(lines).not.toContain("- Name the thing you change before you change it. (edit-any-code)");
  });

  test("a Bash call is matched by the command words of its segments", () => {
    expect(hold(run(pre("Bash", { command: "grep -n fix fixes.md" })))).toContain(
      "- Feed an engine from a file, not from a heredoc. (engine-call-rule)");
  });

  test("a lesson that does not match the call is not given, and a matching one is not missed (Fails-if)", () => {
    const lines = hold(run(pre("Write", { file_path: "work/alpha.ts" })));
    expect(lines).not.toContain("- List the unclear spots before dispatching work. (brief-rule)");
    expect(lines).not.toContain("- This path's rules live in its own folder. (scoped-path)");
    expect(lines).not.toContain("- A lesson for another agent type only. (opencode-only)");
    expect(lines).toContain("- Name the thing you change before you change it. (edit-any-code)");
  });

  test("a project's own fact never reaches an edit of a file of another name or folder (Fails-if)", () => {
    expect(hold(run(pre("Write", { file_path: "work/never-heard-of.ts" })))).not.toContain(
      "- work/never-heard-of.ts: alpha parses the flag before it writes.");
    const elsewhere = hold(run(pre("Write", { file_path: "other/alpha.ts" })));
    expect(elsewhere).toContain("- other/alpha.ts: a fact in another folder is not this file's.");
    expect(elsewhere).not.toContain("- other/alpha.ts: alpha parses the flag before it writes.");
  });

  test("the retry after a hold runs, and the same lesson is not given twice in a session (Fails-if)", () => {
    const first = run(pre("Write", { file_path: "work/alpha.ts" }));
    expect(hold(first).length).toBeGreaterThan(0);
    const retry = run(pre("Write", { file_path: "work/alpha.ts" }));
    expect(retry).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    // A different call of the same session gets only what it has not been given.
    expect(hold(run(pre("Bash", { command: "grep -n fix fixes.md" })))).toEqual([
      "- Feed an engine from a file, not from a heredoc. (engine-call-rule)",
    ]);
  });

  test("another session is given them again", () => {
    hold(run(pre("Write", { file_path: "work/alpha.ts" })));
    expect(hold(run(pre("Write", { file_path: "work/alpha.ts" }), otherSession)).length).toBeGreaterThan(0);
  });

  test("the shown keys are written under the git root, per session, and takeUnshown records before it returns", () => {
    expect(takeUnshown(root, "s-a", ["lesson:x", "fact:a"])).toEqual(["lesson:x", "fact:a"]);
    expect(takeUnshown(root, "s-a", ["lesson:x", "fact:a", "fact:a"])).toEqual([]);
    expect(takeUnshown(root, "s-a", [])).toEqual([]);
    expect(takeUnshown(root, "s-b", ["lesson:x"])).toEqual(["lesson:x"]);
    // Changed after the crossed review (findings 2 and 3): one marker file per key under the git root, not one JSON
    // file. Written by opencode against the JSON form; the expectation changed, not the calls.
    const marks = (session: string) => fs.readdirSync(shownFolder(root, session))
      .map((name) => fs.readFileSync(path.join(shownFolder(root, session), name), "utf8").trim()).sort();
    expect(shownFolder(root, "s-a").startsWith(path.join(root, ".harness-guard", "lessons-shown"))).toBe(true);
    expect(marks("s-a")).toEqual(["fact:a", "lesson:x"]);
    expect(marks("s-b")).toEqual(["lesson:x"]);
  });

  test("a hold writes no journal record", () => {
    hold(run(pre("Write", { file_path: "work/alpha.ts" })));
    const journalFile = path.join(root, ".harness-guard", "journal.jsonl");
    expect(fs.existsSync(journalFile)).toBe(false);
    expect(readJournal(root).records).toEqual([]);
  });

  test("a hook without a store gives nothing at all (Fails-if)", () => {
    const bare: HookEnv = { cwd: root, running: [], now: () => new Date(time) };
    for (const payload of [
      pre("Write", { file_path: "work/alpha.ts" }),
      pre("Bash", { command: "grep -n fix fixes.md" }),
      pre("Edit", { file_path: "pkg/x.test.ts" }),
    ]) {
      expect(handleHook(payload, bare)).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    }
  });

  test("an invalid lesson file in the store does not break the hook (Fails-if)", () => {
    write(path.join(store, "broken.md"), "no front matter\n");
    expect(hold(run(pre("Write", { file_path: "work/alpha.ts" })))).toContain(
      "- Name the thing you change before you change it. (edit-any-code)");
  });
});

// ---- the early returns of handlePreToolUse ---------------------------------------------------------------------------

describe("handlePreToolUse early returns", () => {
  test("a tool that is not Bash, Write, Edit or MultiEdit is quiet", () => {
    for (const tool of ["Read", "Grep", "Task", "TodoWrite"]) {
      expect(run(pre(tool, { file_path: "work/alpha.ts" }))).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    }
  });

  test("a Write, Edit or MultiEdit with no file_path is quiet", () => {
    for (const tool of ["Write", "Edit", "MultiEdit"]) {
      expect(run(pre(tool, {}))).toEqual({ exitCode: 0, stdout: "", stderr: "" });
      expect(run(pre(tool, { file_path: "" }))).toEqual({ exitCode: 0, stdout: "", stderr: "" });
    }
  });

  test("a Bash call with no command is quiet", () => {
    expect(run(pre("Bash", {}))).toEqual({ exitCode: 0, stdout: "", stderr: "" });
  });

  test("a Bash call the lint denies gets the deny alone, with no lesson lines", () => {
    const result = run(pre("Bash", { command: "codex exec \"do it\"" }));
    const lines = reasons(result);
    expect(lines.length).toBe(1);
    expect(lines[0]).toMatch(/^trap:codex-stdin: /);
    expect(lines[0]).not.toContain(LESSON_HOLD);
  });

  test("a read of a file that is not there is held for that reason alone", () => {
    const result = run(pre("Bash", { command: "grep -rn fix missing.md" }));
    const lines = reasons(result);
    expect(lines.length).toBe(1);
    expect(lines[0]).toMatch(/^read-missing: .*which does not exist yet/);
    expect(lines[0]).not.toContain(LESSON_HOLD);
  });

  test("a program read from an unquoted heredoc is held for that reason alone", () => {
    const command = "python3 - <<'PY'\nprint(\"a\\\\b\")\nPY";
    const result = run(pre("Bash", { command }));
    const lines = reasons(result);
    expect(lines.length).toBe(1);
    expect(lines[0]).toMatch(/^inline-script: python3 reads its program from the <<PY heredoc/);
    expect(lines[0]).not.toContain(LESSON_HOLD);
  });

  test("a denied call's lessons wait: the next clean call is held with them", () => {
    run(pre("Bash", { command: "codex exec \"do it\"" }));
    expect(hold(run(pre("Bash", { command: "grep -n fix fixes.md" })))).toEqual([
      "- Feed an engine from a file, not from a heredoc. (engine-call-rule)",
    ]);
  });
});