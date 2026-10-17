// Acceptance expectations: SPEC.md Round 13 N3 as amended — a read is not held when an earlier, completed segment
// writes its exact file by a stdout redirect (`>`, `>>`, `&>`, `&>>`), whatever that segment's command word
// (F-cc665076). Every deny is cross-checked against bash's own answer, so no expectation here is copied from the
// parser under test.
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync, spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import type { HookEnv } from "../src/types.ts";

let root: string;
let env: HookEnv;

beforeEach(() => {
  root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "hg-round13-reader-writes-")));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  fs.mkdirSync(path.join(root, "notes"));
  fs.mkdirSync(path.join(root, "other"));
  fs.mkdirSync(path.join(root, "runs/20261016-four-experts-what-counts-as-change"), { recursive: true });
  fs.writeFileSync(path.join(root, "a"), "x\n");
  env = { cwd: root, running: [], now: () => new Date("2026-10-17T05:00:00.000Z") };
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

// The deny reason when the command is held, null when it may run.
function held(command: string): string | null {
  const result = handleHook({ hook_event_name: "PreToolUse", session_id: "s13-reader-writes", cwd: root,
    tool_name: "Bash", tool_input: { command } }, env);
  expect(result.exitCode).toBe(0);
  if (result.stdout.trim() === "") return null;
  const output = JSON.parse(result.stdout).hookSpecificOutput;
  return output?.permissionDecision === "deny" ? String(output.permissionDecisionReason) : null;
}

// bash's own answer, asked in the same fixture — an expected result computed by another method than the rule's.
function shell(command: string): { status: number | null; stderr: string } {
  const result = spawnSync("bash", ["-c", command], { cwd: root, encoding: "utf8" });
  expect(result.error).toBeUndefined();
  return { status: result.status, stderr: result.stderr };
}
function runsInShell(command: string): void {
  expect(shell(command).status).toBe(0);
}
function failsInShell(command: string): void {
  const result = shell(command);
  expect(result.status !== 0 || result.stderr.includes("No such file")).toBe(true);
}

// F-cc665076 as it was denied, with the repository and `$S` written out: no `$` is left in it, so nothing here
// depends on the separate defect that a read after an unknowable `cd &&` is checked (checked:
// runs/20261017-read-missing-false-hold/cd-after-and.txt). It is only ever shown to the hook, never run.
const OUTPUT = "runs/20261016-four-experts-what-counts-as-change/five-picks-final-tests-on-old.txt";
function plantedCommand(redirect: boolean): string {
  const old = path.join(root, "scratchpad/old-guard");
  const guard = path.join(old, ".claude/skills/workflow-design/guard");
  const tests = path.join(guard, "test");
  const run = `TMPDIR=${old}/tmp BUN_RUNTIME_TRANSPILER_CACHE_PATH=0 bun test test/round16-expect-run.test.ts test/round14-criteria-code.test.ts 2>&1 | grep -E "^\\((pass|fail)\\)"${redirect ? ` > ${root}/${OUTPUT}` : ""}`;
  return `S=${old} && rm -rf ${old} && mkdir -p ${old}/tmp && cd ${root}`
    + ` && git archive f4afcdd .claude/skills/workflow-design/guard | tar -x -C ${old}`
    + ` && cp ${root}/.claude/skills/workflow-design/guard/test/round16-expect-run.test.ts`
    + ` ${root}/.claude/skills/workflow-design/guard/test/round14-criteria-code.test.ts ${tests}/`
    + ` && cd ${guard} && ${run}; cat ${root}/${OUTPUT}`;
}

test("new: F-cc665076's planted command runs — its finished grep redirect wrote the file the last cat reads", () => {
  const command = plantedCommand(true);
  expect(command).not.toContain("$");
  expect(fs.existsSync(path.join(root, OUTPUT))).toBe(false);
  expect(held(command)).toBeNull();
});

test("pin: the same command without the redirect is held, and the reason names the .txt the test names", () => {
  const command = plantedCommand(false);
  expect(command).not.toContain("$");
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("five-picks-final-tests-on-old.txt");
});

// ---- new: each output operator, from a reader

for (const operator of [">", ">>", "&>", "&>>"]) {
  test(`new: a reader's ${operator} into F lets a later cat of F run`, () => {
    const command = `grep x a ${operator} notes/out.md; cat notes/out.md`;
    expect(held(command)).toBeNull();
    runsInShell(command);
    expect(fs.readFileSync(path.join(root, "notes/out.md"), "utf8")).toBe("x\n");
  });
}

test("new: any command word may write the file a later read takes — here cat itself, across &&", () => {
  const command = "cat a > notes/out.md && cat notes/out.md";
  expect(held(command)).toBeNull();
  runsInShell(command);
});

test("new: a heredoc write leaves a file a cat reads on a later line", () => {
  const command = "cat > notes/out.md <<'EOF'\nx\nEOF\ncat notes/out.md";
  expect(held(command)).toBeNull();
  runsInShell(command);
});

test("new: a writer after a cd writes the file in the folder it runs in", () => {
  const command = "cd notes && grep x ../a > out.md; cat out.md";
  expect(held(command)).toBeNull();
  runsInShell(command);
  expect(fs.readFileSync(path.join(root, "notes/out.md"), "utf8")).toBe("x\n");
});

// ---- pin: the write must be the same file, finished, and one the text can know

for (const [label, command] of [
  ["a target in another folder with the same base name", "grep x a > other/out.md; cat notes/out.md"],
  ["a target whose name only contains the read's name", "grep x a > notes/out.md.bak; cat notes/out.md"],
  ["an input redirect", "grep x a < a; cat notes/out.md"],
  ["a stderr copy", "grep x a 2>&1; cat notes/out.md"],
  ["a stdout copy", "grep x a >&2; cat notes/out.md"],
  ["a descriptor close", "grep x a >&-; cat notes/out.md"],
]) {
  test(`pin: ${label} is no write of the file the read takes`, () => {
    const reason = held(command);
    expect(reason).toContain("read-missing");
    expect(reason).toContain("notes/out.md");
    failsInShell(command);
  });
}

test("pin: a reader that redirects elsewhere is still held on its own missing operand", () => {
  const command = "grep -c x notes/missing.md > notes/count.txt; cat notes/missing.md";
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("notes/missing.md");
  failsInShell(command);
});

test("pin: a writer that reads a missing input is held on that input, not excused by its own redirect", () => {
  const command = "grep x missing.txt > notes/out.md; cat notes/out.md";
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("missing.txt");
  failsInShell(command);
});

test("pin: a writer in the read's own pipeline has not finished", () => {
  const reason = held("grep x a > notes/out.md | cat notes/out.md");
  expect(reason).toContain("read-missing");
  expect(reason).toContain("notes/out.md");
});

test("pin: a writer sent to the background may not have finished", () => {
  const reason = held("grep x a > notes/out.md & cat notes/out.md");
  expect(reason).toContain("read-missing");
  expect(reason).toContain("notes/out.md");
});

test("pin: an earlier read of the file, with no redirect to it, still proves nothing", () => {
  const command = "cat notes/missing.md; cat notes/missing.md";
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("notes/missing.md");
  failsInShell(command);
});

// ---- the other N3 exemptions, each fed a reader that redirects

test("pin: a read followed by || is not held, though nothing wrote its file", () => {
  expect(held("cat notes/out.md")).toContain("notes/out.md"); // the same read without the redirect
  expect(held("grep x a > notes/out.md; cat notes/out.md || true")).toBeNull();
  runsInShell("grep x a > notes/out.md; cat notes/out.md || true");
});

test("pin: a probe is not held, though nothing wrote its file", () => {
  expect(held("cat notes/out.md")).toContain("notes/out.md");
  const command = "grep x a > notes/out.md; cat notes/out.md 2>/dev/null; true";
  expect(held(command)).toBeNull();
  runsInShell(command);
});

test("pin: a cd inside ( … ) before the read is not held", () => {
  expect(held("cat notes/out.md")).toContain("notes/out.md");
  const command = "grep x a > notes/out.md; (cd notes); cat notes/out.md";
  expect(held(command)).toBeNull();
  runsInShell(command);
});

test("pin: a path holding $ is still not checked, on either side of the redirect", () => {
  const known = "grep x a > notes/out.md; cat $PWD/notes/out.md";
  expect(held(known)).toBeNull();
  // The writer's target is text the shell decides, so it proves nothing; bash would succeed, and the guard holds on
  // purpose because it cannot know where `$PWD` points. Only the hold is asserted.
  expect(held("grep x a > $PWD/notes/out.md; cat notes/out.md")).toContain("notes/out.md");
  runsInShell(known);
});