// Expectations: SPEC.md Round 13 N1–N4 and the tests-codex brief's amendment.
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

function held(command: string): string | null {
  const result = handleHook({ hook_event_name: "PreToolUse", session_id: "s13-reader-writes", cwd: root,
    tool_name: "Bash", tool_input: { command } }, env);
  expect(result.exitCode).toBe(0);
  if (result.stdout.trim() === "") return null;
  const output = JSON.parse(result.stdout).hookSpecificOutput;
  return output?.permissionDecision === "deny" ? String(output.permissionDecisionReason) : null;
}

function shellSucceeds(command: string): void {
  const result = spawnSync("bash", ["-c", command], { cwd: root, encoding: "utf8" });
  expect(result.error).toBeUndefined();
  expect(result.status).toBe(0);
}

function shellFindsMissing(command: string): void {
  const result = spawnSync("bash", ["-c", command], { cwd: root, encoding: "utf8" });
  expect(result.error).toBeUndefined();
  expect(result.status !== 0 || result.stderr.includes("No such file")).toBe(true);
}

// These two commands are inspected by the hook only, never executed.
function plantedCommand(redirect: boolean): string {
  const scratch = path.join(root, "scratchpad/old-guard");
  const output = path.join(root, "runs/20261016-four-experts-what-counts-as-change/five-picks-final-tests-on-old.txt");
  return `S=${scratch} && rm -rf ${scratch} && mkdir -p ${scratch}/tmp && cd ${root} && git archive f4afcdd .claude/skills/workflow-design/guard | tar -x -C ${scratch} && cp .claude/skills/workflow-design/guard/test/round16-expect-run.test.ts .claude/skills/workflow-design/guard/test/round14-criteria-code.test.ts ${scratch}/.claude/skills/workflow-design/guard/test/ && cd ${scratch}/.claude/skills/workflow-design/guard && TMPDIR=${scratch}/tmp BUN_RUNTIME_TRANSPILER_CACHE_PATH=0 bun test test/round16-expect-run.test.ts test/round14-criteria-code.test.ts 2>&1 | grep -E "^\\((pass|fail)\\)"${redirect ? ` > ${output}` : ""}; cat ${output}`;
}

test("new: F-cc665076's completed grep redirect permits the planted final cat", () => {
  const command = plantedCommand(true);
  expect(command).not.toContain("$");
  expect(fs.existsSync(path.join(root, "runs/20261016-four-experts-what-counts-as-change/five-picks-final-tests-on-old.txt"))).toBe(false);
  expect(held(command)).toBeNull();
});

test("pin: F-cc665076's twin without the redirect holds the final cat", () => {
  const command = plantedCommand(false);
  expect(command).not.toContain("$");
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("five-picks-final-tests-on-old.txt");
});

for (const operator of [">", ">>", "&>", "&>>"]) {
  test(`new: a completed reader's ${operator} writes the later read's exact file`, () => {
    const command = `grep x a ${operator} notes/out.md; cat notes/out.md`;
    expect(held(command)).toBeNull();
    shellSucceeds(command);
    expect(fs.readFileSync(path.join(root, "notes/out.md"), "utf8")).toBe("x\n");
  });
}

test("new: a cat heredoc writes a file read on a later line", () => {
  const command = "cat > notes/out.md <<'EOF'\nx\nEOF\ncat notes/out.md";
  expect(held(command)).toBeNull();
  shellSucceeds(command);
});

test("new: a writer after cd resolves its redirect in that folder", () => {
  const command = "cd notes && grep x ../a > out.md; cd ..; cat notes/out.md";
  expect(held(command)).toBeNull();
  shellSucceeds(command);
});

for (const reader of ["cat a", "head -n 1 a", "sed -n 1p a"]) {
  test(`new: ${reader} can write the later read's file across &&`, () => {
    const command = `${reader} > notes/out.md && cat notes/out.md`;
    expect(held(command)).toBeNull();
    shellSucceeds(command);
  });
}

test("new: a completed writer before || supplies the following read", () => {
  const command = "grep x a > notes/out.md || true; cat notes/out.md";
  expect(held(command)).toBeNull();
  shellSucceeds(command);
});

for (const [label, command, missing] of [
  ["same base name in another folder", "grep x a > other/out.md; cat notes/out.md", "notes/out.md"],
  ["target only contains the read name", "grep x a > notes/out.md.bak; cat notes/out.md", "notes/out.md"],
  ["reader redirects elsewhere then rereads its missing operand", "grep -c x notes/missing.md > notes/count.txt; cat notes/missing.md", "notes/missing.md"],
  ["writing reader has a missing input", "grep x missing.txt > F; cat F", "missing.txt"],
  ["earlier read without a redirect proves nothing", "cat notes/missing.md; cat notes/missing.md", "notes/missing.md"],
  ["redirect into a missing parent makes no file", "grep x a > absent/out.md; cat absent/out.md", "absent/out.md"],
  ["input redirect supplies no output file", "grep x a < a; cat notes/out.md", "notes/out.md"],
  ["stderr copy supplies no output file", "grep x a 2>&1; cat notes/out.md", "notes/out.md"],
  ["stdout copy supplies no output file", "grep x a >&2; cat notes/out.md", "notes/out.md"],
  ["descriptor close supplies no output file", "grep x a >&-; cat notes/out.md", "notes/out.md"],
]) {
  test(`pin: ${label} is held`, () => {
    const reason = held(command);
    expect(reason).toContain("read-missing");
    expect(reason).toContain(missing);
    shellFindsMissing(command);
  });
}

test("pin: an input redirect from the read file makes no file", () => {
  const command = "grep x a < notes/in.md; cat notes/in.md";
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("notes/in.md");
  shellFindsMissing(command);
});

test("pin: a stderr redirect to the read file is not covered", () => {
  const command = "grep x a 2> notes/err.md; cat notes/err.md";
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("notes/err.md");
});

test("pin: a stdout descriptor copy names no file", () => {
  const command = "grep x a >&2; cat '&2'";
  const reason = held(command);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("&2");
});

for (const [label, command] of [
  ["writer in the read's pipeline", "grep x a > F | cat F"],
  ["background writer", "grep x a > F & cat F"],
]) {
  test(`pin: ${label} is not a completed write`, () => {
    const reason = held(command);
    expect(reason).toContain("read-missing");
    expect(reason).toContain("F");
  });
}

for (const [label, command] of [
  ["handled read followed by ||", "grep x a > notes/out.md; cat notes/out.md || true"],
  ["probe with stderr suppressed and a later segment", "grep x a > notes/out.md; cat notes/out.md 2>/dev/null; true"],
  ["subshell cd before the read", "grep x a > notes/out.md; (cd notes); cat notes/out.md"],
  ["shell-resolved dollar path", "grep x a > $PWD/notes/out.md; cat $PWD/notes/out.md"],
]) {
  test(`pin: reader redirect preserves the exemption for a ${label}`, () => {
    expect(held(command)).toBeNull();
    shellSucceeds(command);
  });
}
