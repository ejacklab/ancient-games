// Reproduces each review finding on the current code: one hook call per input, the journal records it leaves.
// Run: bun runs/20261017-round17-crossed/probe.ts
import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { handleHook } from "../../.claude/skills/workflow-design/guard/src/hooks.ts";
import { readJournal } from "../../.claude/skills/workflow-design/guard/src/journal.ts";

type Case = { id: string; event: "PostToolUse" | "PostToolUseFailure"; command: string; exit?: number; output?: string; stdout?: string };

const cases: Case[] = [
  { id: "1", event: "PostToolUseFailure", command: "pytest -q && bun /guard/src/cli.ts insight", exit: 1, output: "collection error" },
  { id: "2", event: "PostToolUseFailure", command: "pytest -q | grep missing", exit: 1, output: "" },
  { id: "3", event: "PostToolUseFailure", command: "false && pytest test/a.py", exit: 1, output: "" },
  { id: "4", event: "PostToolUse", command: "pytest -q | (cat)", stdout: "3 failed, 2 passed" },
  { id: "5", event: "PostToolUseFailure", command: "bun test a.test.ts; pytest b.py", exit: 2, output: "no tests ran" },
  { id: "7", event: "PostToolUseFailure", command: "pytest; echo '3 errors' >&2; false", exit: 1, output: "3 errors" },
];

for (const c of cases) {
  const folder = fs.mkdtempSync(path.join(os.tmpdir(), "hg-probe-"));
  execFileSync("git", ["init", "--quiet"], { cwd: folder });
  const base = { hook_event_name: c.event, session_id: "probe", cwd: folder, tool_name: "Bash", tool_input: { command: c.command } };
  const payload = c.event === "PostToolUseFailure"
    ? { ...base, error: `Exit code ${c.exit}\n${c.output}`, is_interrupt: false }
    : { ...base, tool_response: { stdout: c.stdout, stderr: "", interrupted: false } };
  handleHook(payload, { cwd: folder, running: [], now: () => new Date("2026-10-17T11:30:00.000Z") });
  const kept = readJournal(folder).records.filter((r) => r.kind === "failure" || r.kind === "warning")
    .map((r) => `${r.kind} ${(r as { check: string }).check} input=${(r as { input?: string }).input} actual=${(r as { actual?: string }).actual}`);
  console.log(`finding ${c.id}: ${c.command}\n  -> ${kept.length ? kept.join("; ") : "nothing recorded"}`);
  fs.rmSync(folder, { recursive: true, force: true });
}
