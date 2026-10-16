// Acceptance expectations come from SPEC.md Round 13, N1–N4 (a read of a file that is not there).
import { afterEach, beforeEach, expect, test } from "bun:test";
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../src/hooks.ts";
import { readJournal } from "../src/journal.ts";
import type { HookEnv } from "../src/types.ts";

let root: string;
let env: HookEnv;

beforeEach(() => {
  root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "hg-round13-")));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  // The folders as they were when the two failures happened.
  for (const file of [
    ".claude/skills/four-experts/assets/questions/time-boxed-decision.md",
    "runs/20261015-four-experts-speed/DIGEST.md",
    "runs/20261015-four-experts-speed/research.md",
    "tasks/b1q3id6pc.output",
    "notes/present.md",
  ]) {
    fs.mkdirSync(path.join(root, path.dirname(file)), { recursive: true });
    fs.writeFileSync(path.join(root, file), "x\n");
  }
  fs.mkdirSync(path.join(root, "runs/trial-mcode/retry"), { recursive: true });
  env = { cwd: root, running: [], now: () => new Date("2026-10-17T05:00:00.000Z") };
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

// The deny reason when the command is held, null when it may run.
function held(command: string): string | null {
  const result = handleHook({ hook_event_name: "PreToolUse", session_id: "s13", cwd: root, tool_name: "Bash",
    tool_input: { command } }, env);
  expect(result.exitCode).toBe(0);
  if (result.stdout.trim() === "") return null;
  const output = JSON.parse(result.stdout).hookSpecificOutput;
  return output?.permissionDecision === "deny" ? String(output.permissionDecisionReason) : null;
}

// ---- the planted repeats (R12.3: a check is shown failing on a planted repeat before it is trusted)

test("F-e82a6f58's command, a listing and a read of a guessed file, is held", () => {
  const reason = held("ls .claude/skills/four-experts/assets/questions/ && cat .claude/skills/four-experts/assets/questions/time-boxed-decision.md && ls runs/20261015-four-experts-speed/ && head -60 runs/20261015-four-experts-speed/question.md");
  expect(reason).toContain("read-missing");
  expect(reason).toContain("runs/20261015-four-experts-speed/question.md");
});

test("F-4981093a's command, a status read and reads of an answer never written, is held — 2>/dev/null did not save it", () => {
  const reason = held(`cat ${root}/tasks/b1q3id6pc.output; cd ${root}/runs/trial-mcode/retry && head -c 300 linus.md 2>/dev/null; echo; grep -c "^## " linus.md 2>/dev/null`);
  expect(reason).toContain("read-missing");
  expect(reason).toContain("linus.md");
});

// ---- N2: what is missing

test("a missing file after a value flag, a sed script or a cd is held", () => {
  expect(held("head -n 5 notes/missing.md")).toContain("notes/missing.md");
  expect(held("sed -n 1,60p notes/missing.md")).toContain("notes/missing.md");
  expect(held("cd notes && cat missing.md")).toContain("missing.md");
  expect(held("grep -rn pattern notes/missing")).toContain("notes/missing");
});

test("a file present in the root but not in the folder a cd moved to is held", () => {
  expect(held("cd tasks && cat notes/present.md")).toContain("notes/present.md");
});

// ---- N3: what is not held

test("a read of an existing file runs", () => {
  expect(held("cat notes/present.md")).toBeNull();
  expect(held("head -n 5 notes/present.md && sed -n 1,5p notes/present.md")).toBeNull();
  expect(held("cd notes && grep -c x present.md")).toBeNull();
});

test("a read whose file an earlier segment names, or that is followed by ||, runs", () => {
  expect(held("[ -f notes/new.md ] && cat notes/new.md")).toBeNull();
  expect(held("some-engine -o notes/new.md && head notes/new.md")).toBeNull();
  expect(held("cat notes/new.md || echo none yet")).toBeNull();
});

test("a write, a heredoc body, a pattern, a script and a path the shell decides are not reads", () => {
  expect(held("cat > notes/new.md <<'EOF'\nhead -5 notes/missing.md\nEOF")).toBeNull();
  expect(held('grep -c "notes/missing.md" notes/present.md')).toBeNull();
  expect(held("grep -e missing.md notes/present.md")).toBeNull();
  expect(held("sed -n '/missing.md/p' notes/present.md")).toBeNull();
  expect(held("cat $D/missing.md && head notes/*.md")).toBeNull();
});

test("a probe — stderr to /dev/null and an exit that cannot end the command — runs", () => {
  expect(held("cat .claude/settings.json 2>/dev/null; ls notes")).toBeNull();
  expect(held('grep -n -A4 "\\[pytest\\]" notes/present.md pytest.ini setup.cfg 2>/dev/null | head')).toBeNull();
  expect(held("cat notes/missing.md 2>/dev/null")).toContain("notes/missing.md"); // its exit is the command's
  expect(held("cat notes/missing.md 2>/dev/null && echo read")).toContain("notes/missing.md");
});

test("a folder an earlier writing command names may be filled there; a listing does not fill it", () => {
  expect(held("python3 build.py structure in.txt && head -30 structure/symbols.md")).toBeNull();
  expect(held("ls notes/ && head notes/question.md")).toContain("notes/question.md");
});

test("an escaped quote inside a pattern does not split the command", () => {
  expect(held('grep -n "kind: \\"" notes/present.md; grep -n "return null;\\|return x" notes/present.md | head -5')).toBeNull();
  expect(held('grep -n "kind: \\"" notes/missing.md')).toContain("notes/missing.md");
});

test("a cd inside a ( … ) subshell is not taken as the folder of what follows", () => {
  expect(held("cd notes && (echo x) 2>&1 | (cd .. && tee log.txt); cat present.md")).toBeNull();
});

test("a reader with no file operand runs", () => {
  expect(held("ls notes | grep missing")).toBeNull();
  expect(held("echo x | head -1")).toBeNull();
  expect(held("cat - < notes/present.md")).toBeNull();
});

test("~/ is the home folder", () => {
  const home = process.env.HOME;
  process.env.HOME = path.join(root, "notes");
  try {
    expect(held("cat ~/present.md")).toBeNull();
    expect(held("cat ~/missing.md")).toContain("~/missing.md");
    expect(held("cd ~ && cat present.md")).toBeNull();
    expect(held("cd ~/ && head -3 present.md")).toBeNull();
  } finally {
    process.env.HOME = home;
  }
});

// ---- N4: a hold writes no record

test("a held read writes nothing to the journal", () => {
  held("head notes/missing.md");
  expect(readJournal(root).records).toEqual([]);
});
