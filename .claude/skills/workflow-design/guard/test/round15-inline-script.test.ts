// Acceptance expectations come from SPEC.md Round 15, P1–P4 (a program read from a heredoc).
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
  root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "hg-round15-")));
  execFileSync("git", ["init", "--quiet"], { cwd: root });
  fs.mkdirSync(path.join(root, "runs/run"), { recursive: true });
  env = { cwd: root, running: [], now: () => new Date("2026-10-17T06:00:00.000Z") };
});
afterEach(() => fs.rmSync(root, { recursive: true, force: true }));

// The deny reason when the command is held, null when it may run.
function held(command: string): string | null {
  const result = handleHook({ hook_event_name: "PreToolUse", session_id: "s15", cwd: root, tool_name: "Bash",
    tool_input: { command } }, env);
  expect(result.exitCode).toBe(0);
  if (result.stdout.trim() === "") return null;
  const output = JSON.parse(result.stdout).hookSpecificOutput;
  return output?.permissionDecision === "deny" ? String(output.permissionDecisionReason) : null;
}

// ---- the planted repeat (R12.3)

// F-d1444d01's command: its shape, with the Python program exactly as written (the search string doubled the
// backslash, so it held a backslash and an n, never a newline).
const F_D1444D01 = String.raw`cd ROOT/runs/run && cat >> decisions.md <<'EOF'

Built as guard Round 13 and ` + "`tools/git-hooks/pre-commit`" + String.raw`, commit 6794ea0.
EOF
python3 - <<'EOF'
from pathlib import Path
p = Path("success-path.yaml")
t = p.read_text(encoding="utf-8")
step = '''  - did: "2026-10-17: guard Round 13 (read-missing holds) and the pre-commit export hook"
    engine: "claude"
    model: "claude-opus-5-5"
    check: "planted repeats of F-e82a6f58 and F-4981093a held"
decisions:'''
assert t.count("\\ndecisions:") == 1
p.write_text(t.replace("\\ndecisions:", "\\n" + step, 1), encoding="utf-8")
EOF
cd ROOT && bun cli.ts path check runs/run/success-path.yaml 2>&1 | tail -1`;

test("F-d1444d01's command, a Python program in a quoted heredoc holding a backslash, is held", () => {
  const reason = held(F_D1444D01.replaceAll("ROOT", root));
  expect(reason).toContain("inline-script");
  expect(reason).toContain("python3");
  expect(reason).toContain("<<EOF");
  expect(reason).toContain("a backslash");
  expect(reason).toContain("Write tool");
});

// ---- P1–P2: what is held

test("an interpreter reading its program from a quoted heredoc with a backslash is held", () => {
  expect(held("python3 <<'EOF'\nprint(\"a\\nb\")\nEOF")).toContain("python3");
  expect(held("node - <<'JS'\nconsole.log(\"a\\tb\")\nJS")).toContain("node");
  expect(held("timeout 60 python3 -u - arg <<'EOF'\nimport re\nprint(re.sub(r\"\\s\", \"\", \"a b\"))\nEOF")).toContain("python3");
  expect(held("cd runs && PYTHONPATH=. python - <<\"PY\"\nprint(\"\\\\\")\nPY")).toContain("<<PY");
  expect(held("python3 - <<-EOF\n\tprint(\"a\\nb\")\n\tEOF")).toContain("a backslash");
});

test("a program whose opener follows a multi-line quoted string is held (found by the replay)", () => {
  const command = 'git commit -q -m "subject\n\nCo-Authored-By: A <a@example.invalid>" && git log -1; python3 - <<\'EOF\'\nprint("a\\nb")\nEOF';
  expect(held(command)).toContain("python3");
});

test("an unquoted heredoc program is held for a $ or a backtick as well", () => {
  expect(held("python3 - <<EOF\nprint(\"$HOME\")\nEOF")).toContain("a $");
  expect(held("python3 <<EOF\nprint(\"`date`\")\nEOF")).toContain("a backtick");
  expect(held("python3 - <<EOF\nprint(\"a\\nb\")\nEOF")).toContain("a backslash");
});

// ---- P3: what is not held

test("a heredoc program with no backslash, $ or backtick runs", () => {
  expect(held("python3 - <<'EOF'\nimport json\nprint(json.dumps({\"a\": 1}))\nEOF")).toBeNull();
  expect(held("python3 - <<'EOF'\nprint(\"$HOME is not expanded here\")\nEOF")).toBeNull();
  expect(held("python3 - <<EOF\nprint(1)\nEOF")).toBeNull();
});

test("a heredoc fed as data to a script, a module or -c runs", () => {
  expect(held("python3 build.py <<'EOF'\nline one\\n\nEOF")).toBeNull();
  expect(held("python3 -m json.tool <<'EOF'\n{\"a\": \"b\\n\"}\nEOF")).toBeNull();
  expect(held("python3 -c 'import sys; print(sys.stdin.read())' <<'EOF'\n\\n\nEOF")).toBeNull();
  expect(held("node script.js <<'EOF'\n\\t\nEOF")).toBeNull();
});

test("a script file run, a heredoc written to a file, and an opener inside another heredoc's body run", () => {
  expect(held("python3 runs/run/script.py")).toBeNull();
  expect(held("cat > runs/run/s.py <<'EOF'\nprint(\"a\\nb\")\nEOF")).toBeNull();
  expect(held("cat > runs/run/brief.md <<'EOF'\npython3 - <<'X'\nprint(\"\\n\")\nX\nEOF")).toBeNull();
  expect(held("echo 'python3 - <<EOF' | wc -c")).toBeNull();
});

test("a << inside a program's body is not another opener: one program, one hold", () => {
  const reason = held("python3 - <<'EOF'\nflags = 1<<x\nprint(\"a\\nb\")\nEOF");
  expect(reason?.split("inline-script:").length).toBe(2);
});

// ---- P4: a hold writes no record

test("a held program writes nothing to the journal", () => {
  held("python3 - <<'EOF'\nprint(\"\\n\")\nEOF");
  expect(readJournal(root).records).toEqual([]);
});
