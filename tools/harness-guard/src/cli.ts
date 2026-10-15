// M5: the command line (SPEC.md M5). `bun src/cli.ts <command>`: the hook adapter reads stdin, and the method's
// steps call lint, result, fail, insight, register, install and doctor. Exit 0 ok, 1 findings, 2 usage.
// Nothing printed here holds a prompt, stdout, stderr or a config value.

import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { doctor, doctorMarkdown } from "./doctor.ts";
import { handleHook } from "./hooks.ts";
import { HARNESSES, installSnippet } from "./install.ts";
import { JournalError, guardRoot, recordFailureFromArgs } from "./journal.ts";
import { checkSection, findInsightFiles, openFailures, parseInsight } from "./insight.ts";
import { RegisterError, coverage, loadRegister, validateRegister } from "./register.ts";
import { checkResult, lintCommand, loadEngines } from "./traps.ts";
import type { EngineCall, Finding, HookEnv } from "./types.ts";

const GUARD_DIR = path.resolve(import.meta.dirname, "..");
const OWN_LINE = ["cli.ts hook", "harness-guard"];

const OK = 0;
const FINDINGS = 1;
const USAGE_EXIT = 2;

const USAGE = [
  "usage: harness-guard <command>",
  "  hook claude                     read a hook payload on stdin",
  "  lint <command…>                 lint one command against the traps",
  "  result --engine E --out FILE [--exit N] [--stderr-file F]",
  "  fail --check --input --expected --actual --reason --evidence [--found-by --engine --harness --session]",
  "  insight [--session S]           list open failures and invalid sections",
  "  register <file>                 validate a register and report its coverage",
  "  install --print <harness>       print the hook settings for a harness",
  "  doctor [--health PATH]          report where the guard is installed",
].join("\n");

class UsageError extends Error {}

// The usage text goes out on stderr, so a caller can read the command's own answer from stdout alone.
function usageError(problem: string): never {
  process.stderr.write(`${problem}\n${USAGE}\n`);
  process.exit(USAGE_EXIT);
}

function out(text: string): void {
  process.stdout.write(text.endsWith("\n") ? text : `${text}\n`);
}

function flagValue(args: string[], flag: string): string | null {
  const at = args.indexOf(flag);
  if (at < 0) return null;
  const value = args[at + 1];
  if (value === undefined || value.startsWith("--")) usageError(`${flag} needs a value`);
  return value;
}

// ---- reading the world ------------------------------------------------------------------------------------------

function readStdin(): string {
  try {
    return fs.readFileSync(0, "utf8");
  } catch {
    return "";
  }
}

// Other processes' command lines, for the concurrent traps. Read for matching only: never printed, never stored.
function runningCommands(): string[] {
  try {
    const lines = execFileSync("ps", ["-eo", "args="], { encoding: "utf8", timeout: 5000, stdio: ["ignore", "pipe", "ignore"] });
    return lines
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line !== "" && !OWN_LINE.some((own) => line.includes(own)));
  } catch {
    return [];
  }
}

function report(findings: Finding[]): number {
  for (const finding of findings) {
    out(`${finding.severity} ${finding.rule}: ${finding.message}${finding.fix === undefined ? "" : ` Fix: ${finding.fix}`}`);
  }
  return findings.some((finding) => finding.severity === "fail") ? FINDINGS : OK;
}

// ---- hook -------------------------------------------------------------------------------------------------------

function hook(args: string[]): number {
  const dialect = args[0];
  if (dialect !== "claude") usageError(`hook: the only protocol is claude (got ${dialect ?? "nothing"})`);
  let payload: unknown;
  try {
    payload = JSON.parse(readStdin());
  } catch {
    usageError("hook: stdin is not one JSON payload");
  }
  const env: HookEnv = { cwd: process.cwd(), running: runningCommands(), now: () => new Date() };
  const result = handleHook(payload, env);
  if (result.stdout !== "") out(result.stdout);
  if (result.stderr !== "") process.stderr.write(result.stderr.endsWith("\n") ? result.stderr : `${result.stderr}\n`);
  return result.exitCode;
}

// ---- lint -------------------------------------------------------------------------------------------------------

function lint(args: string[]): number {
  const command = args.join(" ").trim();
  if (command === "") usageError("lint: needs the command to check");
  return report(lintCommand(command, { repoRoot: guardRoot(process.cwd()), running: runningCommands() }));
}

// ---- result -----------------------------------------------------------------------------------------------------

// The engine's stderr comes from a file when one is named; only the finding reaches stdout.
function stderrFrom(file: string | null): string {
  if (file === null) return "";
  try {
    return fs.readFileSync(path.resolve(process.cwd(), file), "utf8");
  } catch {
    return usageError("result: --stderr-file cannot be read");
  }
}

function result(args: string[]): number {
  const engine = flagValue(args, "--engine");
  const outFile = flagValue(args, "--out");
  if (engine === null || outFile === null) usageError("result: needs --engine and --out");
  const spec = loadEngines().find((each) => each.name === engine);
  if (spec === undefined) usageError(`result: ${engine} is not an engine in the catalogue`);

  const exitText = flagValue(args, "--exit");
  let exitCode: number | null = null;
  if (exitText !== null) {
    exitCode = Number(exitText);
    if (!Number.isInteger(exitCode)) usageError("result: --exit needs a whole number");
  }

  const call: EngineCall = {
    engine: spec.name,
    outputFile: outFile,
    stdoutIsAnswer: spec.stdout_is_answer === true,
    statusFile: spec.status_from_out_dir === true ? path.join(outFile, "status.json") : null,
    background: false,
  };
  const findings = checkResult({ call, cwd: process.cwd(), exitCode, stdout: "", stderr: stderrFrom(flagValue(args, "--stderr-file")), interrupted: false });
  return report(findings);
}

// ---- fail -------------------------------------------------------------------------------------------------------

function fail(args: string[]): number {
  const record = recordFailureFromArgs(guardRoot(process.cwd()), args);
  out(`${record.id} appended to .harness-guard/journal.jsonl`);
  return OK;
}

// ---- insight ----------------------------------------------------------------------------------------------------

// Open failures and the sections that failed their checks: ids, rule ids and paths only.
function insight(args: string[]): number {
  const session = flagValue(args, "--session");
  const root = guardRoot(process.cwd());
  const open = openFailures(root, session);
  const openIds = new Set(open.map((record) => record.id));

  for (const relative of findInsightFiles(root)) {
    let sections;
    try {
      sections = parseInsight(fs.readFileSync(path.join(root, relative), "utf8"));
    } catch {
      out(`warn ${relative}: cannot be read or parsed`);
      continue;
    }
    for (const section of sections) {
      const rules = checkSection(section).filter((finding) => finding.severity === "fail").map((finding) => finding.rule);
      if (rules.length === 0) continue;
      for (const id of section.ids) {
        if (openIds.has(id)) out(`fail ${id}: ${relative}: ${rules.join(", ")}`);
      }
    }
  }

  for (const record of open) {
    out(`open ${record.id}: ${record.check}: no valid insight section answers it`);
  }
  if (open.length === 0) out("no open failures");
  return open.length === 0 ? OK : FINDINGS;
}

// ---- register ---------------------------------------------------------------------------------------------------

// Rule ids and counts only: the register's own text never enters the output.
function register(args: string[]): number {
  const file = args[0];
  if (file === undefined || file.startsWith("--")) usageError("register: needs the register file");
  let loaded;
  try {
    loaded = loadRegister(path.resolve(process.cwd(), file));
  } catch (error) {
    if (error instanceof RegisterError) usageError(error.message);
    throw error;
  }
  const counts = coverage(loaded);
  const findings = [...validateRegister(loaded), ...counts.findings];
  for (const finding of findings) out(`${finding.severity} ${finding.rule}`);
  out(`coverage: ${counts.covered}/${counts.total} units, ${counts.percent}% (target ${counts.target}%)`);
  return findings.some((finding) => finding.severity === "fail") ? FINDINGS : OK;
}

// ---- install ----------------------------------------------------------------------------------------------------

function install(args: string[]): number {
  if (args[0] !== "--print") usageError("install: only --print is supported; the guard never writes a harness's settings");
  const harness = args[1];
  if (harness === undefined) usageError("install: --print needs a harness");
  if (!HARNESSES.includes(harness as (typeof HARNESSES)[number])) usageError(`install: unknown harness ${harness}`);
  out(installSnippet(harness as (typeof HARNESSES)[number], GUARD_DIR));
  return OK;
}

// ---- doctor -----------------------------------------------------------------------------------------------------

function doctorCommand(args: string[]): number {
  const report = doctor({ home: os.homedir(), projectRoot: guardRoot(process.cwd()), healthScript: flagValue(args, "--health") });
  out(doctorMarkdown(report));
  return OK;
}

// ---- dispatch ---------------------------------------------------------------------------------------------------

function run(args: string[]): number {
  const command = args[0];
  const rest = args.slice(1);
  switch (command) {
    case "hook": return hook(rest);
    case "lint": return lint(rest);
    case "result": return result(rest);
    case "fail": return fail(rest);
    case "insight": return insight(rest);
    case "register": return register(rest);
    case "install": return install(rest);
    case "doctor": return doctorCommand(rest);
    case undefined: return usageError("no command given");
    case "help":
    case "--help": return usageError("help is the usage text above");
    default: return usageError(`unknown command ${command}`);
  }
}

try {
  process.exit(run(process.argv.slice(2)));
} catch (error) {
  if (error instanceof UsageError || error instanceof JournalError) usageError(error.message);
  process.stderr.write("harness-guard: an internal error was caught; the guard is failing open\n");
  process.exit(FINDINGS);
}