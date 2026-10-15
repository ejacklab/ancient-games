// M1: trap catalogue, engine-call recognition, result check (SPEC.md M1).
// Never prints raw stdout, stderr, prompts or catalogue values: only ids, counts and fixed phrases.

import * as fs from "node:fs";
import * as path from "node:path";
import type { EngineCall, EngineSpec, Finding, LintContext, ResultInput, Trap } from "./types.ts";

const DATA_DIR = path.join(import.meta.dirname, "..", "data");
const SPECIAL_PATHS = new Set(["/dev/null", "/dev/stdin", "/dev/stdout", "/dev/stderr"]);

type Entry = Record<string, unknown>;

// ---- catalogue ---------------------------------------------------------------------------------------------------

function isEntry(value: unknown): value is Entry {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function nonEmptyString(value: unknown): boolean {
  return typeof value === "string" && value.trim() !== "";
}

function validRegex(source: unknown): boolean {
  if (typeof source !== "string") return false;
  try {
    new RegExp(source);
    return true;
  } catch {
    return false;
  }
}

function matches(source: string, text: string): boolean {
  try {
    return new RegExp(source).test(text);
  } catch {
    return false;
  }
}

// A problem names the entry by position and the field, never by value: catalogue text is not reportable.
function trapProblem(index: number, detail: string): string {
  return `traps: entry ${index} ${detail}`;
}

function checkTrap(entry: unknown, index: number): string | null {
  if (!isEntry(entry)) return trapProblem(index, "is not an object");
  if (!nonEmptyString(entry.id)) return trapProblem(index, "has no id");
  if (entry.status !== "approved" && entry.status !== "proposed") {
    return trapProblem(index, "has a status outside approved|proposed");
  }
  if (entry.applies !== "command" && entry.applies !== "result") {
    return trapProblem(index, "has an applies outside command|result");
  }
  if (!nonEmptyString(entry.engine)) return trapProblem(index, "has no engine");
  for (const field of ["why", "fix", "source"]) {
    if (!nonEmptyString(entry[field])) return trapProblem(index, `has no ${field}`);
  }
  for (const field of ["command", "unless", "stderr"]) {
    if (entry[field] !== undefined && !validRegex(entry[field])) {
      return trapProblem(index, `has a ${field} that is not a regex source`);
    }
  }
  if (entry.applies === "command" && entry.command === undefined) {
    return trapProblem(index, "is a command trap with no command regex");
  }
  if (entry.applies === "result" && entry.stderr === undefined && entry.output_empty !== true) {
    return trapProblem(index, "is a result trap with no stderr regex and no output_empty");
  }
  return null;
}

function engineProblem(index: number, detail: string): string {
  return `engines: entry ${index} ${detail}`;
}

function checkEngine(entry: unknown, index: number): string | null {
  if (!isEntry(entry)) return engineProblem(index, "is not an object");
  if (!nonEmptyString(entry.name)) return engineProblem(index, "has no name");
  if (!validRegex(entry.command)) return engineProblem(index, "has no command regex source");
  if (entry.output_flags !== undefined) {
    const flags = entry.output_flags;
    if (!Array.isArray(flags) || flags.some((flag) => !nonEmptyString(flag))) {
      return engineProblem(index, "has output_flags that are not all non-empty strings");
    }
  }
  if (entry.stdout_is_answer !== undefined && typeof entry.stdout_is_answer !== "boolean") {
    return engineProblem(index, "has a stdout_is_answer that is not a boolean");
  }
  if (entry.status_from_out_dir !== undefined && typeof entry.status_from_out_dir !== "boolean") {
    return engineProblem(index, "has a status_from_out_dir that is not a boolean");
  }
  if (entry.silent_failures !== undefined) {
    const failures = entry.silent_failures;
    const bad = !Array.isArray(failures)
      || failures.some((failure) => !isEntry(failure) || !nonEmptyString(failure.text) || !nonEmptyString(failure.status));
    if (bad) return engineProblem(index, "has a silent_failures entry without text and status");
  }
  return null;
}

// Reads a catalogue file. A missing or unparseable file yields no entries and one problem.
function readCatalogue(file: string): { traps?: unknown[]; engines?: unknown[]; problems: string[] } {
  let parsed: unknown;
  try {
    parsed = Bun.YAML.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return { problems: [`catalogue ${path.basename(file)}: cannot be read or parsed`] };
  }
  if (!isEntry(parsed)) return { problems: [`catalogue ${path.basename(file)}: is not a mapping`] };
  const result: { traps?: unknown[]; engines?: unknown[]; problems: string[] } = { problems: [] };
  if (parsed.traps !== undefined) {
    if (Array.isArray(parsed.traps)) result.traps = parsed.traps;
    else result.problems.push(`catalogue ${path.basename(file)}: traps is not a list`);
  }
  if (parsed.engines !== undefined) {
    if (Array.isArray(parsed.engines)) result.engines = parsed.engines;
    else result.problems.push(`catalogue ${path.basename(file)}: engines is not a list`);
  }
  if (result.traps === undefined && result.engines === undefined) {
    result.problems.push(`catalogue ${path.basename(file)}: has neither traps nor engines`);
  }
  return result;
}

export function loadTraps(file: string = path.join(DATA_DIR, "traps.yaml")): Trap[] {
  const catalogue = readCatalogue(file);
  const traps: Trap[] = [];
  for (const [index, entry] of (catalogue.traps ?? []).entries()) {
    if (checkTrap(entry, index) === null) traps.push(entry as unknown as Trap);
  }
  return traps;
}

export function loadEngines(file: string = path.join(DATA_DIR, "engines.yaml")): EngineSpec[] {
  const catalogue = readCatalogue(file);
  const engines: EngineSpec[] = [];
  for (const [index, entry] of (catalogue.engines ?? []).entries()) {
    if (checkEngine(entry, index) === null) engines.push(entry as unknown as EngineSpec);
  }
  return engines;
}

export function catalogueProblems(file?: string): string[] {
  const files = file === undefined ? [path.join(DATA_DIR, "traps.yaml"), path.join(DATA_DIR, "engines.yaml")] : [file];
  const problems: string[] = [];
  for (const one of files) {
    const catalogue = readCatalogue(one);
    problems.push(...catalogue.problems);
    for (const [index, entry] of (catalogue.traps ?? []).entries()) {
      const problem = checkTrap(entry, index);
      if (problem !== null) problems.push(problem);
    }
    for (const [index, entry] of (catalogue.engines ?? []).entries()) {
      const problem = checkEngine(entry, index);
      if (problem !== null) problems.push(problem);
    }
  }
  return problems;
}

// ---- engine-call recognition --------------------------------------------------------------------------------------

function unquote(value: string): string {
  const text = value.trim();
  if (text.length >= 2) {
    const first = text[0];
    if ((first === '"' || first === "'") && text.endsWith(first)) return text.slice(1, -1);
  }
  return text;
}

function escapeRegex(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// The value after a flag: "-o FILE", "-o=FILE", "--out FILE", "--out=FILE".
function outputFromFlags(command: string, flags: string[] | undefined): string | null {
  for (const flag of flags ?? []) {
    const pattern = new RegExp(
      `(?:^|\\s)${escapeRegex(flag)}(?:=+\\s*|\\s+)("[^"]*"|'[^']*'|[^\\s]+)`,
    );
    const found = command.match(pattern);
    if (found) return unquote(found[1] ?? "");
  }
  return null;
}

// The target of a stdout redirect "> FILE" or ">> FILE"; a "2>" is not one.
function outputFromRedirect(command: string): string | null {
  const pattern = /(^|[^0-9&])>{1,2}\s*("[^"]*"|'[^']*'|[^\s|;&]+)/g;
  let found: string | null = null;
  for (const match of command.matchAll(pattern)) found = unquote(match[2] ?? "");
  return found;
}

// Quote-aware tokenising: a quoted path with spaces stays one token, without its quotes.
function tokens(command: string): string[] {
  const found: string[] = [];
  let current = "";
  let quote: string | null = null;
  for (const char of command) {
    if (quote !== null) {
      if (char === quote) quote = null;
      else current += char;
      continue;
    }
    if (char === '"' || char === "'") {
      quote = char;
      continue;
    }
    if (/\s/.test(char)) {
      if (current !== "") found.push(current);
      current = "";
      continue;
    }
    current += char;
  }
  if (current !== "") found.push(current);
  return found;
}

// True when the command ends with a shell "&" outside quotes.
function endsBackground(command: string): boolean {
  const bare = command.replace(/"[^"]*"|'[^']*'/g, " ");
  const trimmed = bare.trimEnd();
  return trimmed.endsWith("&") && !trimmed.endsWith("&&");
}

export function recognizeEngineCall(command: string, engines?: EngineSpec[]): EngineCall | null {
  const specs = engines ?? loadEngines();
  for (const spec of specs) {
    if (!validRegex(spec.command) || !matches(spec.command, command)) continue;
    const fromFlag = outputFromFlags(command, spec.output_flags);
    const fromRedirect = outputFromRedirect(command);
    const outputFile = fromFlag ?? fromRedirect;
    const isWrapper = spec.status_from_out_dir === true;
    return {
      engine: spec.name,
      outputFile,
      stdoutIsAnswer: spec.stdout_is_answer === true && fromRedirect === null,
      statusFile: isWrapper && outputFile !== null ? path.join(outputFile, "status.json") : null,
      background: endsBackground(command),
    };
  }
  return null;
}

// ---- command lint -------------------------------------------------------------------------------------------------

function hasPathOutsideRepo(command: string, repoRoot: string): boolean {
  const root = path.resolve(repoRoot);
  for (const token of tokens(command)) {
    if (!token.startsWith("/") || SPECIAL_PATHS.has(token)) continue;
    const resolved = path.resolve(token);
    if (resolved !== root && !resolved.startsWith(root + path.sep)) return true;
  }
  return false;
}

function trapHits(command: string, trap: Trap, ctx: LintContext): boolean {
  const commandRegex = trap.command;
  if (typeof commandRegex !== "string" || !validRegex(commandRegex)) return false;
  if (!matches(commandRegex, command)) return false;
  if (trap.unless !== undefined && matches(trap.unless, command)) return false;

  // background and concurrent are alternatives: one of them is enough; every other condition must hold.
  const alternatives: boolean[] = [];
  if (trap.background === true) alternatives.push(ctx.background === true || endsBackground(command));
  if (trap.concurrent === true) alternatives.push(ctx.running.some((line) => matches(commandRegex, line)));
  if (alternatives.length > 0 && !alternatives.some(Boolean)) return false;

  if (trap.paths_outside_repo === true && !hasPathOutsideRepo(command, ctx.repoRoot)) return false;
  return true;
}

export function lintCommand(command: string, ctx: LintContext, traps: Trap[] = loadTraps()): Finding[] {
  const findings: Finding[] = [];
  for (const trap of traps) {
    if (trap.status !== "approved" || trap.applies !== "command") continue;
    if (!trapHits(command, trap, ctx)) continue;
    findings.push({ rule: `trap:${trap.id}`, severity: "fail", message: trap.why, fix: trap.fix, ref: trap.source });
  }
  return findings;
}

// ---- result check -------------------------------------------------------------------------------------------------

function resolveFrom(cwd: string, file: string): string {
  return path.resolve(cwd, file);
}

function hasContent(file: string): boolean {
  try {
    return /\S/.test(fs.readFileSync(file, "utf8"));
  } catch {
    return false;
  }
}

function failedStatusEntries(statusFile: string): { keys: string[]; unreadable: boolean } {
  let parsed: unknown;
  try {
    parsed = JSON.parse(fs.readFileSync(statusFile, "utf8"));
  } catch {
    return { keys: [], unreadable: true };
  }
  if (!isEntry(parsed)) return { keys: [], unreadable: true };
  const keys: string[] = [];
  for (const [key, value] of Object.entries(parsed)) {
    if (isEntry(value) && value.ok === false) keys.push(key);
  }
  return { keys, unreadable: false };
}

export function checkResult(input: ResultInput, traps: Trap[] = loadTraps()): Finding[] {
  const findings: Finding[] = [];
  const { call, cwd, exitCode, stdout, stderr, interrupted } = input;

  if (exitCode !== null && exitCode !== 0) {
    findings.push(
      exitCode === 124
        ? { rule: "R12.1-timeout", severity: "fail", message: `the engine call hit its timeout (exit 124)`, fix: "raise the timeout or run the work in smaller steps" }
        : { rule: "R12.1-exit", severity: "fail", message: `the engine call exited with code ${exitCode}`, fix: "read the engine's stderr, fix the cause, run the call again" },
    );
  }
  if (interrupted) {
    findings.push({ rule: "R12.1-interrupted", severity: "fail", message: "the engine call was interrupted before it finished", fix: "run the call again to completion before using its result" });
  }

  const outputFile = call.outputFile === null ? null : resolveFrom(cwd, call.outputFile);
  const fileMissing = outputFile !== null && !fs.existsSync(outputFile);
  const fileEmpty = outputFile !== null && !fileMissing && !hasContent(outputFile);

  // With a status file the wrapper's own status is the output check.
  if (call.statusFile === null) {
    if (fileMissing) {
      findings.push({ rule: "R12.1-missing-output", severity: "fail", message: "the engine call reported no output file and none exists", fix: "give the engine an output flag it can write, then run it again" });
    } else if (fileEmpty) {
      findings.push({ rule: "R12.1-empty-output", severity: "fail", message: "the output file exists but holds no answer", fix: "treat the call as failed; re-run on an engine that can do the task" });
    } else if (outputFile === null && call.stdoutIsAnswer && !/\S/.test(stdout)) {
      findings.push({ rule: "R12.1-empty-output", severity: "fail", message: "the engine call answered nothing on stdout", fix: "treat the call as failed; re-run on an engine that can do the task" });
    }
  }

  const answerEmpty = outputFile !== null ? fileMissing || fileEmpty : call.statusFile === null && call.stdoutIsAnswer && !/\S/.test(stdout);
  for (const trap of traps) {
    if (trap.status !== "approved" || trap.applies !== "result") continue;
    if (trap.engine !== "any" && trap.engine !== call.engine) continue;
    if (trap.output_empty === true && answerEmpty) {
      findings.push({ rule: `trap:${trap.id}`, severity: "fail", message: trap.why, fix: trap.fix, ref: trap.source });
      continue;
    }
    if (trap.stderr !== undefined && matches(trap.stderr, stderr)) {
      findings.push({ rule: `trap:${trap.id}`, severity: "fail", message: trap.why, fix: trap.fix, ref: trap.source });
    }
  }

  const spec = loadEngines().find((engine) => engine.name === call.engine);
  for (const failure of spec?.silent_failures ?? []) {
    if (!stderr.includes(failure.text)) continue;
    findings.push({
      rule: `R12.1-silent-${failure.status}`,
      severity: "fail",
      message: `the engine reported a silent failure (${failure.status}) while answering`,
      fix: "treat the call as failed; check the engine's own health and run it again",
    });
  }

  if (call.statusFile !== null) {
    const statusFile = resolveFrom(cwd, call.statusFile);
    if (!fs.existsSync(statusFile)) {
      findings.push({ rule: "R12.1-missing-status", severity: "fail", message: "the wrapper reported no status file and none exists", fix: "run the wrapper again and check that it wrote its output folder" });
    } else {
      const entries = failedStatusEntries(statusFile);
      if (entries.unreadable) {
        findings.push({ rule: "R12.1-wrapped-fail", severity: "fail", message: "the wrapper status file is not a JSON object of entries", fix: "treat the call as failed; check the wrapper wrote its status file" });
      }
      for (const key of entries.keys) {
        findings.push({
          rule: "R12.1-wrapped-fail",
          severity: "fail",
          message: `wrapper status entry "${key}" did not report ok`,
          fix: "read that entry's own report, fix the cause, run the wrapper again",
        });
      }
    }
  }

  return findings;
}