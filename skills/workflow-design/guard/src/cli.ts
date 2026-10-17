// M5: the command line (SPEC.md M5). `bun src/cli.ts <command>`: the hook adapter reads stdin, and the method's
// steps call lint, result, fail, insight, register, install and doctor. Exit 0 ok, 1 findings, 2 usage.
// Nothing printed here holds a prompt, stdout, stderr or a config value.

import { execFileSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { CriteriaError, checkCriteria, fromRegister, loadCriteria, score, skeleton as criteriaSkeleton } from "./criteria.ts";
import { doctor, doctorMarkdown } from "./doctor.ts";
import { handleHook } from "./hooks.ts";
import { HARNESSES, installSnippet } from "./install.ts";
import { JournalError, guardRoot, newFailureId, recordFailureFromArgs } from "./journal.ts";
import { checkSection, findInsightFiles, openFailures, parseInsight } from "./insight.ts";
import { WarningError, dismiss, settleAsFailure, warnings } from "./warnings.ts";
import { indexMarkdown, insightIndex, loadCategories, showSections } from "./insight-index.ts";
import { ExpectError, declareRed, runRed } from "./expect.ts";
import { DeadlineError, deadlineEnd, deadlineStatus, endDeadline, readDeadlines, startDeadline } from "./deadline.ts";
import { PathError, checkPath, parents, skeleton } from "./paths.ts";
import { rates, ratesMarkdown } from "./rates.ts";
import { RegisterError, coverage, loadRegister, validateRegister } from "./register.ts";
import { checkResult, lintCommand, loadEngines } from "./traps.ts";
import type { EngineCall, Finding, HookEnv } from "./types.ts";

const GUARD_DIR = path.resolve(import.meta.dirname, "..");

const OK = 0;
const FINDINGS = 1;
const USAGE_EXIT = 2;

const USAGE = [
  "usage: harness-guard <command>",
  "  hook claude                     read a hook payload on stdin",
  "  lint <command…>                 lint one command against the traps",
  "  result --engine E --out FILE [--exit N] [--stderr-file F]",
  "  fail --check --input --expected --actual --reason --evidence [--found-by --engine --harness --session]",
  "  insight [--session S] [--json]  list open failures and invalid sections",
  "  insight index [--json]          every insight section: ids, check, source, option kinds, category (no text)",
  "  insight show --category C | <file>#<id>   the chosen sections, whole (for an expert that loads them)",
  "  expect-fail --tests FILE [--session S]   before a planned red run: the next test run naming FILE must fail",
  "  expect-fail --run COMMAND --out FILE [--session S]   run a planned red run: the guard runs it and records the result",
  "  warning <W-id> fail|dismiss --reason TEXT   settle a warning the guard could not judge",
  "  warnings [--session S]          every warning and how it was settled",
  "  deadline start --minutes N [--run DIR]   record the owner's time limit (a clock line after every Bash or file-write call)",
  "  deadline status | wait | end   time used and left, workers' progress; wait = a background timer to the deadline; end = the task is done",
  "  register <file>                 validate a register and report its coverage",
  "  install --print <harness>       print the hook settings for a harness",
  "  doctor [--health PATH] [--json] report where the guard is installed",
  "  rates [--session S] [--json]    success and failure counts per check and engine",
  "  path new [--session S] [--out F]  print or write a success-path skeleton",
  "  path check <file>               check a success-path file",
  "  path parents <category>         list the path files of a category",
  "  criteria new [--session S] [--request TEXT] [--from-register FILE] [--code] [--out F]",
  "                                  print or write a criteria file; --code adds the tests item",
  "  criteria score <file>           score a criteria file: met/total and the unmarked ids",
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
// Only this process and the one that started it are dropped, by pid (round 3, C17): a text match would drop any
// other process whose line happens to name this package.
function runningCommands(): string[] {
  const own = new Set<number>([process.pid, process.ppid]);
  try {
    const lines = execFileSync("ps", ["-eo", "pid=,args="], { encoding: "utf8", timeout: 5000, stdio: ["ignore", "pipe", "ignore"] });
    return lines
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line !== "")
      .filter((line) => {
        const pid = Number(line.split(/\s+/)[0]);
        return Number.isFinite(pid) && !own.has(pid);
      })
      .map((line) => line.replace(/^\d+\s+/, ""));
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
  const raw = readStdin();
  let payload: unknown;
  try {
    payload = JSON.parse(raw);
  } catch {
    // A payload that is not one JSON object is not a usage error: the guard says so in one line and lets the call
    // through, because a blocking exit here would freeze the agent (round 3, C11).
    process.stderr.write(raw.trim() === ""
      ? "harness-guard: hook: stdin was empty; nothing to check\n"
      : "harness-guard: hook: stdin is not one JSON payload; nothing to check\n");
    return OK;
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

// ---- deadline (round 10) ----------------------------------------------------------------------------------------

function deadlineCommand(args: string[]): number {
  const [verb] = args;
  const root = guardRoot(process.cwd());
  if (verb === "start") {
    if (args.includes("--marks")) usageError("deadline start: --marks was removed with the percent marks; the clock shows after every call");
    const minutesText = flagValue(args, "--minutes");
    const minutes = minutesText === null ? Number.NaN : Number(minutesText);
    try {
      const deadline = startDeadline(root, { minutes, run: flagValue(args, "--run") }, new Date());
      const end = new Date(deadlineEnd(deadline));
      out(`${deadline.id}: ${deadline.minutes} min, deadline ${end.toTimeString().slice(0, 5)}; a clock line after every Bash or file-write call`);
      return OK;
    } catch (error) {
      if (error instanceof DeadlineError) usageError(`deadline start: ${error.message}`);
      throw error;
    }
  }
  if (verb === "status") {
    const status = deadlineStatus(root, flagValue(args, "--session"), new Date());
    if (status === null) {
      process.stderr.write("no deadline: record one with deadline start --minutes N\n");
      return USAGE_EXIT;
    }
    out([status.line, ...status.workers.map((w) => `  ${w}`)].join("\n"));
    return status.up ? FINDINGS : OK;
  }
  if (verb === "wait") {
    // --mark went with the 50/80/100% marks (run 20261017-workflows, experts-decide mark-q, accepted by EJ): asking for it
    // fails loudly, never waits silently to the deadline.
    if (args.includes("--mark")) usageError("deadline wait: --mark was removed with the percent marks; wait runs to the deadline");
    const session = flagValue(args, "--session");
    const status = deadlineStatus(root, session, new Date());
    if (status === null) usageError("deadline wait: no deadline");
    const at = Date.parse(status.deadline.start) + status.deadline.minutes * 60_000;
    const wait = at - Date.now();
    if (wait > 0) Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, wait);
    // The deadline may be ended while wait sleeps, when a run finishes early (run 20261017-insight-placement).
    const after = readDeadlines(root).find((d) => d.id === status.deadline.id);
    if (after?.ended !== undefined) {
      out(`${status.deadline.id} ended before its deadline`);
      return OK;
    }
    out(deadlineStatus(root, session, new Date())?.line ?? `${status.deadline.id}: no open deadline`);
    return OK;
  }
  if (verb === "end") {
    const ended = endDeadline(root, flagValue(args, "--session"), new Date());
    if (ended === null) {
      process.stderr.write("no deadline to end\n");
      return USAGE_EXIT;
    }
    out(`${ended.id} ended`);
    return OK;
  }
  return usageError("deadline: start --minutes N [--run DIR] | status | wait | end");
}

// ---- warnings (round 9) -----------------------------------------------------------------------------------------

// Settle one warning: the agent's judgement, with a one-line reason. Ids and the reason only are printed.
function warningCommand(args: string[]): number {
  const [id, verb] = args;
  if (id === undefined || !/^W-[0-9a-f]{8}$/.test(id)) usageError("warning: give a warning id (W-xxxxxxxx)");
  if (verb !== "fail" && verb !== "dismiss") usageError("warning: say fail or dismiss");
  const reason = flagValue(args, "--reason");
  if (reason === null) usageError("warning: --reason is required");
  const root = guardRoot(process.cwd());
  try {
    if (verb === "fail") {
      const record = settleAsFailure(root, id, reason, new Date(), newFailureId);
      out(`${id} logged as ${record.id}: an insight is required before you stop`);
    } else {
      dismiss(root, id, reason, new Date());
      out(`${id} dismissed: the reason is kept for the project owner`);
    }
  } catch (error) {
    if (error instanceof WarningError) {
      process.stderr.write(`${error.message}\n`);
      return FINDINGS;
    }
    throw error;
  }
  return OK;
}

// ---- expect-fail (round 12, E1) ----------------------------------------------------------------------------------

// The session is the harness's own when it gives one, so a declaration matches the hook's runs of the same session.
function expectFail(args: string[]): number {
  const session = flagValue(args, "--session") ?? (process.env.CLAUDE_CODE_SESSION_ID?.trim() || "none");
  const command = flagValue(args, "--run");
  if (command !== null) return expectRun(command, flagValue(args, "--out"), session);
  const file = flagValue(args, "--tests");
  if (file === null) usageError("expect-fail: needs --tests FILE or --run COMMAND --out FILE");
  try {
    const record = declareRed(guardRoot(process.cwd()), path.resolve(process.cwd(), file), session, new Date());
    out(`expect-fail ${record.id}: the next test run naming ${record.file} must fail (session ${record.session})`);
  } catch (error) {
    if (error instanceof ExpectError) usageError(error.message);
    throw error;
  }
  return OK;
}

// Round 16, X1–X4: the guard runs the red run itself; 0 when it failed as planned, 1 when it passed (logged).
function expectRun(command: string, outFile: string | null, session: string): number {
  if (outFile === null) usageError("expect-fail --run: needs --out FILE (the run's whole output goes there)");
  const harness = process.env.CLAUDE_CODE_SESSION_ID?.trim() ? "claude-code" : "none";
  let run;
  try {
    run = runRed(guardRoot(process.cwd()), command, process.cwd(), outFile, session, harness, () => new Date());
  } catch (error) {
    if (error instanceof ExpectError) usageError(error.message);
    throw error;
  }
  const tail = fs.readFileSync(path.resolve(guardRoot(process.cwd()), run.out), "utf8").trimEnd().split("\n").slice(-15);
  out(tail.join("\n"));
  if (run.record.kind === "red") {
    out(`expect-fail --run: ${run.runner} exited ${run.exit ?? "on a signal"} — the red step, recorded (${run.record.declared.join(", ")}); whole output in ${run.out}`);
    return OK;
  }
  out(`expect-fail --run: ${run.runner} exited 0 — no test failed: ${run.record.id} logged (R12.2-red-passed); whole output in ${run.out}`);
  return FINDINGS;
}

// Every warning with how it was settled, so the project owner can read the dismissals and overrule them.
function warningsCommand(args: string[]): number {
  const rows = warnings(guardRoot(process.cwd()), flagValue(args, "--session"));
  const lines = ["| warning | check | input | settled |", "|---|---|---|---|"];
  for (const { warning, settled } of rows) {
    const state = settled.state === "open" ? "open" : settled.state === "failure" ? `failure ${settled.failure}`
      : `dismissed: ${settled.reason.replace(/\|/g, "\\|")}`;
    lines.push(`| ${warning.id} | ${warning.check} | ${warning.input} | ${state} |`);
  }
  out(lines.join("\n"));
  return rows.some((row) => row.settled.state === "open") ? FINDINGS : OK;
}

// ---- insight ----------------------------------------------------------------------------------------------------

// Open failures and the sections that failed their checks: ids, rule ids and paths only.
function insight(args: string[]): number {
  // Round 11: `insight index` lists what was learned (no author text); `insight show` prints chosen sections whole.
  if (args[0] === "index" || args[0] === "show") {
    const root = guardRoot(process.cwd());
    const categoriesFile = flagValue(args, "--categories");  // another scheme, for a comparison (default: data/insight-categories.yaml)
    const guardDir = path.resolve(import.meta.dirname, "..");
    const entries = insightIndex(root, categoriesFile === null ? loadCategories(guardDir) : loadCategories(guardDir, path.resolve(categoriesFile)));
    if (args[0] === "index") {
      out(args.includes("--json") ? JSON.stringify({ sections: entries }) : indexMarkdown(entries));
      return OK;
    }
    const categories: string[] = [];
    const refs: string[] = [];
    for (let i = 1; i < args.length; i++) {
      if (args[i] === "--category") categories.push(args[++i] ?? usageError("--category needs a value"));
      else if (args[i] === "--categories") i++;
      else refs.push(args[i]!);
    }
    if (categories.length === 0 && refs.length === 0) usageError("insight show: --category C or <file>#<id>");
    out(showSections(root, entries, { categories, refs }) || "no matching insight sections");
    return OK;
  }
  const session = flagValue(args, "--session");
  const json = args.includes("--json");
  const root = guardRoot(process.cwd());
  const open = openFailures(root, session);
  const openIds = new Set(open.map((record) => record.id));
  const invalid: { id: string; file: string; rules: string[] }[] = [];
  const unreadable: string[] = [];

  for (const relative of findInsightFiles(root)) {
    let sections;
    try {
      sections = parseInsight(fs.readFileSync(path.join(root, relative), "utf8"));
    } catch {
      unreadable.push(relative);
      if (!json) out(`warn ${relative}: cannot be read or parsed`);
      continue;
    }
    for (const section of sections) {
      const rules = checkSection(section).filter((finding) => finding.severity === "fail").map((finding) => finding.rule);
      if (rules.length === 0) continue;
      for (const id of section.ids) {
        if (!openIds.has(id)) continue;
        invalid.push({ id, file: relative, rules });
        if (!json) out(`fail ${id}: ${relative}: ${rules.join(", ")}`);
      }
    }
  }

  if (json) {
    // Round 7 (J3): the same facts as the text form, for harness_health.py.
    out(JSON.stringify({ open: open.map((record) => ({ id: record.id, check: record.check })), invalid, unreadable }));
    return open.length === 0 ? OK : FINDINGS;
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
  out(args.includes("--json") ? JSON.stringify(report) : doctorMarkdown(report)); // Round 7 (J1)
  return OK;
}

// ---- rates (round 5, S2) ---------------------------------------------------------------------------------------

function ratesCommand(args: string[]): number {
  const rows = rates(guardRoot(process.cwd()), flagValue(args, "--session"));
  out(args.includes("--json") ? JSON.stringify({ rows }) : ratesMarkdown(rows)); // Round 7 (J2)
  return OK;
}

// ---- path (round 5, S3) -----------------------------------------------------------------------------------------

function pathNew(args: string[]): number {
  const root = guardRoot(process.cwd());
  const session = flagValue(args, "--session") ?? "none";
  const outFile = flagValue(args, "--out");
  let yaml: string;
  try {
    yaml = skeleton(root, session, outFile === null ? undefined : path.resolve(process.cwd(), outFile));
  } catch (error) {
    if (error instanceof PathError) usageError(error.message);
    throw error;
  }
  if (outFile === null) out(yaml);
  else out(`skeleton written to ${outFile}`);
  return OK;
}

function pathCheck(args: string[]): number {
  const file = args[0];
  if (file === undefined || file.startsWith("--")) usageError("path check: needs the path file");
  const root = guardRoot(process.cwd());
  let checked;
  try {
    checked = checkPath(root, path.relative(root, path.resolve(process.cwd(), file)));
  } catch (error) {
    if (error instanceof PathError) usageError(error.message);
    throw error;
  }
  const code = report(checked.findings);
  out(`better: ${checked.better === null ? "n/a" : checked.better}; gain: ${checked.gainPercent === null ? "n/a" : `${checked.gainPercent}%`}; repeated failures: ${checked.repeatedFailures.length === 0 ? "none" : checked.repeatedFailures.join(", ")}`);
  return code;
}

function pathParents(args: string[]): number {
  const category = args[0];
  if (category === undefined || category.startsWith("--")) usageError("path parents: needs a category");
  const lines = ["| file | measures | better |", "|---|---|---|"];
  for (const entry of parents(guardRoot(process.cwd()), category)) {
    const measures = Object.entries(entry.measures).map(([name, value]) => `${name}=${value}`).join(", ");
    lines.push(`| ${entry.file} | ${measures} | ${entry.better === null ? "n/a" : entry.better} |`);
  }
  out(lines.join("\n"));
  return OK;
}

function pathCommand(args: string[]): number {
  const sub = args[0];
  const rest = args.slice(1);
  switch (sub) {
    case "new": return pathNew(rest);
    case "check": return pathCheck(rest);
    case "parents": return pathParents(rest);
    default: return usageError(`path: needs new, check or parents (got ${sub ?? "nothing"})`);
  }
}

// ---- criteria (round 6, K3) ------------------------------------------------------------------------------------

// The text of a new criteria file: the skeleton, or one item per unit of a register. Written only inside the root.
function criteriaNew(args: string[]): number {
  const root = guardRoot(process.cwd());
  const session = flagValue(args, "--session") ?? "none";
  const request = flagValue(args, "--request") ?? "";
  const registerFile = flagValue(args, "--from-register");
  const outFile = flagValue(args, "--out");
  // Round 14, Q2: the request changes code, so the file carries the standard tests item.
  const code = args.includes("--code");

  let yaml: string;
  if (registerFile === null) {
    yaml = criteriaSkeleton(session, request, code);
  } else {
    let loaded;
    try {
      loaded = loadRegister(path.resolve(process.cwd(), registerFile));
    } catch (error) {
      if (error instanceof RegisterError) usageError(error.message);
      throw error;
    }
    yaml = Bun.YAML.stringify(fromRegister(loaded, session, request, code), null, 2);
  }

  if (outFile === null) {
    out(yaml);
    return OK;
  }
  const base = path.resolve(root);
  const target = path.resolve(process.cwd(), outFile);
  if (target !== base && !target.startsWith(base + path.sep)) usageError("criteria new: --out must be inside the root");
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, yaml.endsWith("\n") ? yaml : `${yaml}\n`, "utf8");
  out(`criteria written to ${outFile}`);
  return OK;
}

// Rule ids, counts and criterion ids only: the request and the criterion text never enter the output.
function criteriaScore(args: string[]): number {
  const file = args[0];
  if (file === undefined || file.startsWith("--")) usageError("criteria score: needs the criteria file");
  let loaded;
  try {
    loaded = loadCriteria(path.resolve(process.cwd(), file));
  } catch (error) {
    if (error instanceof CriteriaError) usageError(error.message);
    throw error;
  }
  const findings = checkCriteria(loaded);
  for (const finding of findings) out(`${finding.severity} ${finding.rule}: ${finding.message}`);
  const result = score(loaded);
  out(`score: ${result.met}/${result.total} (${result.percent === null ? "n/a" : `${result.percent}%`})`);
  out(`unmarked: ${result.unmarked.length === 0 ? "none" : result.unmarked.join(", ")}`);
  return findings.some((finding) => finding.severity === "fail") || result.unmarked.length > 0 ? FINDINGS : OK;
}

function criteriaCommand(args: string[]): number {
  const sub = args[0];
  const rest = args.slice(1);
  switch (sub) {
    case "new": return criteriaNew(rest);
    case "score": return criteriaScore(rest);
    default: return usageError(`criteria: needs new or score (got ${sub ?? "nothing"})`);
  }
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
    case "warning": return warningCommand(rest);
    case "expect-fail": return expectFail(rest);
    case "deadline": return deadlineCommand(rest);
    case "warnings": return warningsCommand(rest);
    case "register": return register(rest);
    case "install": return install(rest);
    case "doctor": return doctorCommand(rest);
    case "rates": return ratesCommand(rest);
    case "path": return pathCommand(rest);
    case "criteria": return criteriaCommand(rest);
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