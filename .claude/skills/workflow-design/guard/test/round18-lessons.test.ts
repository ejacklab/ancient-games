// Acceptance expectations come from SPEC.md, Round 18 (L1–L5): agent lessons and project facts.
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { LESSON_HOLD, handleHook } from "../src/hooks.ts";
import { checkLessons, isTestFile, readLessons } from "../src/lessons.ts";
import type { HookEnv } from "../src/types.ts";

const CLI = path.resolve(import.meta.dirname, "../src/cli.ts");
let root: string;
let store: string;
let env: HookEnv;

beforeEach(() => {
  root = fs.mkdtempSync(path.join(os.tmpdir(), "hg-lessons-"));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  store = path.join(root, "store");
  fs.mkdirSync(store);
  env = { cwd: root, running: [], now: () => new Date("2026-10-17T15:30:00.000Z"), lessons: store };
});

afterEach(() => {
  fs.rmSync(root, { recursive: true, force: true });
});

function lesson(slug: string, front: string, body = `Lesson text of ${slug}.`): void {
  fs.writeFileSync(path.join(store, `${slug}.md`), `---\n${front}\nfrom: runs/x/insight.md#F-1\n---\n${body}\n`);
}

function write(file: string, text: string): string {
  const absolute = path.join(root, file);
  fs.mkdirSync(path.dirname(absolute), { recursive: true });
  fs.writeFileSync(absolute, text);
  return absolute;
}

function pre(tool: string, input: Record<string, unknown>, session = "s1") {
  return handleHook({ hook_event_name: "PreToolUse", session_id: session, cwd: root, tool_name: tool, tool_input: input }, env);
}

function context(result: { stdout: string }): string {
  if (result.stdout === "") return "";
  const out = JSON.parse(result.stdout).hookSpecificOutput;
  expect(out.permissionDecision).toBe("deny");
  expect(out.permissionDecisionReason.split("\n")[0]).toBe(LESSON_HOLD);
  return out.permissionDecisionReason;
}

function cli(...args: string[]) {
  return spawnSync(process.execPath, [CLI, ...args], {
    cwd: root, encoding: "utf8", env: { ...process.env, BUN_RUNTIME_TRANSPILER_CACHE_PATH: "0" },
  });
}

// ---- L1

test("L1: a valid lesson is read with its fields and text", () => {
  lesson("a-lesson", "agents: [all]\nkinds: [test]\npaths: [\"**/*.ts\"]\ncommands: [git]");
  expect(readLessons(store)).toEqual([{ slug: "a-lesson", agents: ["all"], kinds: ["test"], paths: ["**/*.ts"],
    commands: ["git"], from: "runs/x/insight.md#F-1", enforcedBy: "", text: "Lesson text of a-lesson." }]);
});

test.each([
  ["Bad_Name", "agents: [all]\nkinds: [test]", "x", "slug"],
  ["no-agents", "kinds: [test]", "x", "agents"],
  ["empty-agents", "agents: []\nkinds: [test]", "x", "agents"],
  ["odd-agent", "agents: [gpt]\nkinds: [test]", "x", "unknown agent gpt"],
  ["no-kinds", "agents: [all]", "x", "kinds"],
  ["odd-kind", "agents: [all]\nkinds: [deploy]", "x", "unknown kind deploy"],
  ["bad-paths", "agents: [all]\nkinds: [test]\npaths: 3", "x", "paths"],
  ["no-text", "agents: [all]\nkinds: [test]", "  ", "no lesson text"],
])("L1: %s is skipped by readers and reported by check", (slug, front, body, reason) => {
  lesson(slug, front, body);
  lesson("good", "agents: [all]\nkinds: [test]");
  expect(readLessons(store).map((l) => l.slug)).toEqual(["good"]);
  const bad = checkLessons(store);
  expect(bad).toHaveLength(1);
  expect(bad[0]!.reason).toContain(reason);
});

test("L1: a file with no front matter or no from is invalid", () => {
  fs.writeFileSync(path.join(store, "plain.md"), "just text\n");
  fs.writeFileSync(path.join(store, "nofrom.md"), "---\nagents: [all]\nkinds: [test]\n---\ntext\n");
  expect(readLessons(store)).toEqual([]);
  expect(checkLessons(store).map((b) => b.reason).sort()).toEqual(
    ["from: the insight or memory it came from", "no front matter between two --- lines"]);
});

// ---- L3

test.each([
  ["src/test/a.ts", true], ["tests/b.py", true], ["src/x.test.ts", true], ["pkg/y_test.go", true],
  ["test_z.py", true], ["src/hooks.ts", false], ["latest/a.ts", false], ["src/contest.ts", false],
])("L3: %s is a test file: %p", (file, expected) => {
  expect(isTestFile(file)).toBe(expected);
});

// ---- L5 through the hook, L2 facts

test("L5: a Write gets the matching lessons and the file's project facts once per session", () => {
  lesson("for-code", "agents: [all]\nkinds: [code-edit]");
  lesson("for-tests", "agents: [all]\nkinds: [test]");
  lesson("for-opencode", "agents: [opencode]\nkinds: [code-edit]");
  lesson("for-yaml", "agents: [claude-main]\nkinds: [brief]\npaths: [\"conf/*.yaml\"]");
  const file = write("src/hooks.ts", "x");
  write("src/LESSONS.md", "# notes\n- `hooks.ts` — keep the exemption narrow.\n- `other.ts` — not this one.\n");
  const first = context(pre("Write", { file_path: file, content: "y" }));
  expect(first).toContain("Lesson text of for-code. (for-code)");
  expect(first).toContain("- src/hooks.ts: keep the exemption narrow.");
  expect(first).not.toContain("for-tests");
  expect(first).not.toContain("for-opencode");
  expect(first).not.toContain("for-yaml");
  expect(first).not.toContain("not this one");
  expect(pre("Edit", { file_path: file, old_string: "x", new_string: "z" }).stdout).toBe("");
  expect(context(pre("Edit", { file_path: file }, "s2"))).toContain("(for-code)");
});

// Run 20261017-agent-lessons insight: subagents' calls carry the parent session id, so the marks are per agent too.
test("L5: each agent of a session gets a lesson once — the main agent and each subagent (agent_id)", () => {
  lesson("for-git", "agents: [all]\nkinds: [command]\ncommands: [git]");
  const call = (agent?: string) => handleHook({ hook_event_name: "PreToolUse", session_id: "s1", cwd: root, tool_name: "Bash",
    tool_input: { command: "git status" }, ...(agent === undefined ? {} : { agent_id: agent, agent_type: "general-purpose" }) }, env);
  expect(context(call("sub-1"))).toContain("(for-git)");
  expect(call("sub-1").stdout).toBe("");
  expect(context(call())).toContain("(for-git)");
  expect(call().stdout).toBe("");
  expect(context(call("sub-2"))).toContain("(for-git)");
});

test("L5: a test file gets test lessons; a path glob matches a non-code file", () => {
  lesson("for-tests", "agents: [claude-main]\nkinds: [test]");
  lesson("for-yaml", "agents: [claude-main]\nkinds: [brief]\npaths: [\"conf/*.yaml\"]");
  expect(context(pre("Write", { file_path: write("test/a.test.ts", "") }))).toContain("(for-tests)");
  expect(context(pre("Write", { file_path: write("conf/app.yaml", "") }))).toContain("(for-yaml)");
});

test("L2: a fact reaches only the file of that name in that folder", () => {
  lesson("unused", "agents: [codex]\nkinds: [test]");
  write("src/LESSONS.md", "- `hooks.ts` — the fact.\n");
  expect(pre("Write", { file_path: write("lib/hooks.ts", "") }).stdout).toBe("");
  expect(context(pre("Write", { file_path: write("src/hooks.ts", "") }))).toContain("the fact.");
});

test("L5: a Bash call gets the lessons of its command words", () => {
  lesson("for-git", "agents: [all]\nkinds: [command]\ncommands: [git]");
  expect(pre("Bash", { command: "ls -la" }).stdout).toBe("");
  expect(context(pre("Bash", { command: "cd sub && timeout 30 git status" }))).toContain("(for-git)");
});

test("L5: a call the guard denies gets the deny alone; its lessons wait for a call that runs", () => {
  lesson("for-cat", "agents: [all]\nkinds: [command]\ncommands: [cat]");
  const denied = JSON.parse(pre("Bash", { command: "cat missing-file.txt" }).stdout).hookSpecificOutput;
  expect(denied.permissionDecision).toBe("deny");
  expect(denied.permissionDecisionReason).not.toContain(LESSON_HOLD);
  expect(denied.permissionDecisionReason).not.toContain("for-cat");
  write("there.txt", "x");
  expect(context(pre("Bash", { command: "cat there.txt" }))).toContain("(for-cat)");
});

test("L5: no store, an unknown tool, or a Write with no path gives nothing", () => {
  lesson("for-code", "agents: [all]\nkinds: [code-edit]");
  expect(pre("Read", { file_path: write("src/a.ts", "") }).stdout).toBe("");
  expect(pre("Write", { content: "x" }).stdout).toBe("");
  env = { ...env, lessons: undefined };
  expect(pre("Write", { file_path: write("src/b.ts", "") }).stdout).toBe("");
});

// Run 20261017-agent-lessons: a hold that carried only an enforced lesson's pointer was noise — its check already acts.
test("L5: an enforced lesson never holds a call; lessons for still lists its pointer", () => {
  lesson("checked", "agents: [all]\nkinds: [code-edit]\nenforced_by: guard Round 13");
  expect(pre("Write", { file_path: write("src/a.ts", "") }).stdout).toBe("");
  const listed = cli("lessons", "for", "--agent", "claude-main", "--kinds", "code-edit", "--dir", store);
  expect(listed.stdout.trim()).toBe("- checked: enforced by guard Round 13");
});

// ---- L4

test("L4: lessons for prints the matching lines and exits 0; nothing when none match", () => {
  lesson("for-tests", "agents: [opencode]\nkinds: [test]");
  const hit = cli("lessons", "for", "--agent", "opencode", "--kinds", "test", "--dir", store);
  expect(hit.status).toBe(0);
  expect(hit.stdout.trim()).toBe("- Lesson text of for-tests. (for-tests)");
  const miss = cli("lessons", "for", "--agent", "codex", "--kinds", "test", "--dir", store);
  expect(miss.status).toBe(0);
  expect(miss.stdout).toBe("");
});

test.each([[["--agent", "gpt"]], [["--agent", "all"]], [["--agent", "opencode", "--kinds", "deploy"]], [[]]])(
  "L4: lessons for %j is a usage error", (args: string[]) => {
    expect(cli("lessons", "for", ...args, "--dir", store).status).toBe(2);
  },
);

test("L4: lessons check exits 1 on an invalid file and 0 when all are valid", () => {
  lesson("good", "agents: [all]\nkinds: [test]");
  expect(cli("lessons", "check", "--dir", store).status).toBe(0);
  lesson("bad", "agents: [all]");
  const result = cli("lessons", "check", "--dir", store);
  expect(result.status).toBe(1);
  expect(result.stdout).toContain("bad.md: kinds");
});
