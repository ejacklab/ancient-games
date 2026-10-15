// M5: doctor (SPEC.md M5). Reports, per harness, whether the guard is installed and whether it answers — without
// printing a settings value, a config line or the health script's own text.

import { spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as path from "node:path";
import { handleHook } from "./hooks.ts";
import type { DoctorHarness, DoctorReport } from "./types.ts";

const MARK = "harness-guard";

// A command the catalogue denies: the probe's answer is whether the handler denies it in-process.
const PROBE_COMMAND = "codex exec probe";

export interface DoctorOptions {
  home: string;
  projectRoot: string;
  healthScript?: string | null;
  run?: (argv: string[]) => { code: number; stdout: string };
}

// ---- harness files -----------------------------------------------------------------------------------------------

function listDir(dir: string): string[] {
  try {
    return fs.readdirSync(dir).map((name) => path.join(dir, name)).filter((file) => {
      try {
        return fs.statSync(file).isFile();
      } catch {
        return false;
      }
    });
  } catch {
    return [];
  }
}

interface Files {
  // A missing file is simply not there; an unreadable or unparseable one makes the answer unknown.
  files: string[];
}

const HARNESS_FILES: Record<string, (opts: DoctorOptions) => Files> = {
  "claude-code": (opts) => ({
    files: [
      path.join(opts.home, ".claude", "settings.json"),
      path.join(opts.projectRoot, ".claude", "settings.json"),
      path.join(opts.projectRoot, ".claude", "settings.local.json"),
    ],
  }),
  codex: (opts) => ({
    files: [
      path.join(opts.home, ".codex", "hooks.json"),
      path.join(opts.home, ".codex", "config.toml"),
    ],
  }),
  qwen: (opts) => ({ files: [path.join(opts.home, ".qwen", "settings.json")] }),
  opencode: (opts) => ({
    files: [
      ...listDir(path.join(opts.home, ".config", "opencode", "plugin")),
      ...listDir(path.join(opts.home, ".config", "opencode", "plugins")),
      ...listDir(path.join(opts.projectRoot, ".opencode", "plugin")),
      ...listDir(path.join(opts.projectRoot, ".opencode", "plugins")),
    ],
  }),
};

// A settings value is a hook command only when its key says so: an unrelated value naming the guard is not an install.
function jsonCommands(value: unknown, found: string[] = []): string[] {
  if (Array.isArray(value)) {
    for (const item of value) jsonCommands(item, found);
    return found;
  }
  if (typeof value !== "object" || value === null) return found;
  for (const [key, item] of Object.entries(value as Record<string, unknown>)) {
    if (typeof item === "string" && key.toLowerCase().endsWith("command")) found.push(item);
    else jsonCommands(item, found);
  }
  return found;
}

const TEXT_COMMAND = /(?:^|[\s;{])["']?([\w.$-]*command)["']?\s*[:=]\s*"([^"]*)"|(?:^|[\s;{])["']?([\w.$-]*command)["']?\s*[:=]\s*'([^']*)'/gi;

function textCommands(source: string): string[] {
  const found: string[] = [];
  for (const match of source.matchAll(TEXT_COMMAND)) found.push(match[2] ?? match[4] ?? "");
  return found;
}

// A TOML check without a TOML parser: brackets and quotes have to close.
function structurallyComplete(source: string): boolean {
  let depth = 0;
  for (let i = 0; i < source.length; i++) {
    const char = source[i]!;
    if (char === '"' || char === "'") {
      const close = source.indexOf(char, i + 1);
      if (close < 0) return false;
      i = close;
      continue;
    }
    if (char === "#") {
      while (i < source.length && source[i] !== "\n") i++;
      continue;
    }
    if (char === "[" || char === "{") depth += 1;
    if (char === "]" || char === "}") depth -= 1;
    if (depth < 0) return false;
  }
  return depth === 0;
}

// A settings file that does not parse cannot be read as a hook list: the answer is unknown, not absent.
function readState(file: string): "installed" | "absent" | "unknown" | null {
  let raw: string;
  try {
    raw = fs.readFileSync(file, "utf8");
  } catch (error) {
    return (error as NodeJS.ErrnoException).code === "ENOENT" ? null : "unknown";
  }
  if (file.endsWith(".json")) {
    let parsed: unknown;
    try {
      parsed = JSON.parse(raw);
    } catch {
      return "unknown";
    }
    return jsonCommands(parsed).some((command) => command.includes(MARK)) ? "installed" : "absent";
  }
  if (file.endsWith(".toml") && !structurallyComplete(raw)) return "unknown";
  return textCommands(raw).some((command) => command.includes(MARK)) ? "installed" : "absent";
}

function guardState(opts: DoctorOptions, harness: string): { guard: DoctorHarness["guard"]; note: string } {
  const source = HARNESS_FILES[harness];
  if (source === undefined) return { guard: "unknown", note: "no files are known for this harness" };
  const { files } = source(opts);
  let installed = 0;
  let absent = 0;
  let unknown = 0;
  for (const file of files) {
    const state = readState(file);
    if (state === "installed") installed += 1;
    else if (state === "absent") absent += 1;
    else if (state === "unknown") unknown += 1;
  }
  const seen = installed + absent + unknown;
  if (installed > 0) return { guard: "installed", note: `${installed} of ${seen} read file(s) carry a ${MARK} hook` };
  if (unknown > 0) return { guard: "unknown", note: `${unknown} file(s) exist but cannot be read or parsed` };
  return { guard: "absent", note: `no ${MARK} hook found in ${seen} read file(s)` };
}

// ---- does the guard answer ---------------------------------------------------------------------------------------

// One probe for every row: a PreToolUse payload on a catalogued trap must deny.
function answers(opts: DoctorOptions): boolean {
  const result = handleHook(
    { hook_event_name: "PreToolUse", session_id: "doctor", tool_name: "Bash", tool_input: { command: PROBE_COMMAND } },
    { cwd: opts.projectRoot, running: [], now: () => new Date(0) },
  );
  if (result.exitCode !== 0 || result.stdout === "") return false;
  try {
    const output = JSON.parse(result.stdout) as { hookSpecificOutput?: { permissionDecision?: string } };
    return output.hookSpecificOutput?.permissionDecision === "deny";
  } catch {
    return false;
  }
}

// ---- harness health ----------------------------------------------------------------------------------------------

function defaultRun(argv: string[]): { code: number; stdout: string } {
  const result = spawnSync(argv[0] ?? "", argv.slice(1), { encoding: "utf8", timeout: 30000 });
  return { code: result.status ?? -1, stdout: result.stdout ?? "" };
}

// The summary is a count or the kind of failure, never the script's own text.
function health(opts: DoctorOptions): DoctorReport["health"] {
  const script = opts.healthScript;
  if (script === undefined || script === null || script === "") return null;
  const run = opts.run ?? defaultRun;
  let result: { code: number; stdout: string };
  try {
    result = run(["python3", script, "--json"]);
  } catch (error) {
    return { ok: false, summary: `the health script could not run (${error instanceof Error ? error.name : "Error"})` };
  }
  if (result.code !== 0) return { ok: false, summary: `the health script exited with code ${result.code}` };
  let parsed: unknown;
  try {
    parsed = JSON.parse(result.stdout);
  } catch {
    return { ok: false, summary: "the health script did not print parsable JSON" };
  }
  const findings: unknown = (parsed as { findings?: unknown }).findings;
  const count = Array.isArray(findings) ? findings.length : 0;
  return { ok: true, summary: `${count} findings` };
}

// ---- report ------------------------------------------------------------------------------------------------------

export function doctor(opts: DoctorOptions): DoctorReport {
  const answer = answers(opts);
  const harnesses: DoctorHarness[] = Object.keys(HARNESS_FILES).map((harness) => {
    const state = guardState(opts, harness);
    return { harness, guard: state.guard, answers: answer, note: state.note };
  });
  return { harnesses, health: health(opts) };
}

export function doctorMarkdown(report: DoctorReport): string {
  const lines = ["# harness-guard doctor", "", "| harness | guard | answers | note |", "| --- | --- | --- | --- |"];
  for (const row of report.harnesses) {
    const note = row.note.replace(/\|/g, "\\|");
    lines.push(`| ${row.harness} | ${row.guard} | ${row.answers === null ? "not checked" : row.answers ? "yes" : "no"} | ${note} |`);
  }
  if (report.health === null) {
    lines.push("", "harness health: not checked (no harness_health.py path given)");
  } else {
    lines.push("", `harness health: ${report.health.ok ? "ok" : "failed"} — ${report.health.summary}`);
  }
  return `${lines.join("\n")}\n`;
}