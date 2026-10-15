// M1: trap catalogue, engine-call recognition, result check (SPEC.md M1).
// Never prints raw stdout, stderr, prompts or catalogue values: only ids, counts and fixed phrases.

import * as fs from "node:fs";
import * as path from "node:path";
import type { EngineCall, EngineSpec, Finding, LintContext, ResultInput, Segment, Trap } from "./types.ts";

const DATA_DIR = path.join(import.meta.dirname, "..", "data");
const SPECIAL_PATHS = new Set(["/dev/null", "/dev/stdin", "/dev/stdout", "/dev/stderr"]);
const HELP_WORDS = new Set(["--help", "-h", "--version", "-V"]);
const ASSIGNMENT = /^[A-Za-z_][A-Za-z0-9_]*=/;
const DURATION = /^\d+(?:\.\d+)?(?:h\d+)?[smhd]?$/;
const TIMEOUT_VALUE_OPTIONS = new Set(["-s", "--signal", "-k", "--kill-after"]);
const SIMPLE_WRAPPERS = new Set(["nohup", "time", "exec", "command"]);

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

// ---- segments and the command word --------------------------------------------------------------------------------

interface Word {
  text: string; // the word as written, quotes kept
  start: number;
}

// Quote-aware words with their offsets, so a stripped command can start where a wrapper ended.
function words(text: string): Word[] {
  const found: Word[] = [];
  let start = -1;
  let quote: string | null = null;
  const close = (end: number) => {
    if (start >= 0) found.push({ text: text.slice(start, end), start });
    start = -1;
  };
  for (let i = 0; i < text.length; i++) {
    const char = text[i]!;
    if (quote !== null) {
      if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"') {
      quote = char;
      if (start < 0) start = i;
      continue;
    }
    if (/\s/.test(char)) {
      close(i);
      continue;
    }
    if (start < 0) start = i;
  }
  close(text.length);
  return found;
}

function unquote(value: string): string {
  const text = value.trim();
  if (text.length >= 2) {
    const first = text[0];
    if ((first === '"' || first === "'") && text.endsWith(first)) return text.slice(1, -1);
  }
  return text;
}

function hasHelpWord(text: string): boolean {
  return words(text).some((word) => HELP_WORDS.has(unquote(word.text)));
}

// The heredoc a line opens: "<<WORD", "<<'WORD'", "<<"WORD"" or "<<-WORD" at a word boundary.
function heredocIn(line: string): { word: string; tabs: boolean } | null {
  const found = line.match(/(?:^|\s)<<(-?)(?:'([^']*)'|"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*))/);
  if (found === null) return null;
  const word = found[2] ?? found[3] ?? found[4] ?? "";
  return word === "" ? null : { word, tabs: found[1] === "-" };
}

// Heredoc bodies carry data, not commands: the opening line stays, the body and its delimiter go.
function dropHeredocBodies(command: string): string {
  const kept: string[] = [];
  let open: { word: string; tabs: boolean } | null = null;
  for (const line of command.split("\n")) {
    if (open !== null) {
      const body = open.tabs ? line.replace(/^\t+/, "") : line;
      if (body.trimEnd() === open.word) open = null;
      continue;
    }
    kept.push(line);
    open = heredocIn(line);
  }
  return kept.join("\n");
}

type Token = { kind: "text"; text: string } | { kind: "sep"; sep: string };

// Simple commands, keeping their own redirections. A "&" of a redirection (2>&1, >&2, &>file) is not a separator.
function tokenize(command: string): Token[] {
  const tokens: Token[] = [];
  let current = "";
  let quote: string | null = null;
  const flush = () => {
    tokens.push({ kind: "text", text: current });
    current = "";
  };
  const separate = (sep: string) => {
    flush();
    tokens.push({ kind: "sep", sep });
  };
  for (let i = 0; i < command.length; i++) {
    const char = command[i]!;
    if (quote !== null) {
      current += char;
      if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"') {
      quote = char;
      current += char;
      continue;
    }
    if (char === "\n" || char === ";" || char === "(" || char === ")") {
      separate(char);
      continue;
    }
    if (char === "|") {
      if (command[i + 1] === "|") {
        separate("||");
        i++;
      } else separate("|");
      continue;
    }
    if (char === "&") {
      const next = command[i + 1];
      const previous = current[current.length - 1];
      if (next === "&") {
        separate("&&");
        i++;
        continue;
      }
      if (next !== ">" && previous !== ">" && previous !== "&") {
        separate("&");
        continue;
      }
    }
    current += char;
  }
  flush();
  return tokens;
}

export function segments(command: string): Segment[] {
  const tokens = tokenize(dropHeredocBodies(command));
  // A separator next to a command, skipping the empty text between two separators.
  const separator = (index: number, step: number): string | null => {
    for (let i = index + step; i >= 0 && i < tokens.length; i += step) {
      const token = tokens[i]!;
      if (token.kind === "text" && token.text.trim() === "") continue;
      return token.kind === "sep" ? token.sep : null;
    }
    return null;
  };
  const parts: Segment[] = [];
  // Commands inside a "( … )" group share the group's background status.
  const groups: number[][] = [];
  for (const [index, token] of tokens.entries()) {
    if (token.kind === "sep") {
      if (token.sep === "(") groups.push([]);
      if (token.sep === ")") {
        const group = groups.pop();
        if (group !== undefined && separator(index + 1, 1) === "&") {
          for (const member of group) parts[member]!.background = true;
        }
      }
      continue;
    }
    const text = token.text.trim();
    const before = separator(index, -1);
    const after = separator(index, 1);
    if (text === "") continue;
    const position = parts.length;
    parts.push({ text, background: after === "&", piped: before === "|" });
    // A command inside nested groups is inside each of them.
    for (const group of groups) group.push(position);
  }
  return parts;
}

// A wrapper word that leads a segment: its name, with any path and quotes removed.
function wrapperName(text: string): string {
  return path.basename(unquote(text));
}

// The index after "timeout" with its options and duration.
function afterTimeout(list: Word[], index: number): number {
  let i = index + 1;
  while (i < list.length) {
    const word = unquote(list[i]!.text);
    if (!word.startsWith("-")) break;
    i++;
    if (word === "--") return i; // the options end here: no duration follows
    if (!word.includes("=") && TIMEOUT_VALUE_OPTIONS.has(word) && i < list.length) i++;
  }
  if (i < list.length && DURATION.test(unquote(list[i]!.text))) i++;
  return i;
}

// The index after "env" with its options and assignments.
function afterEnv(list: Word[], index: number): number {
  let i = index + 1;
  while (i < list.length) {
    const word = unquote(list[i]!.text);
    if (word === "-i" || word.startsWith("-u=")) {
      i++;
      continue;
    }
    if (word === "-u") {
      i += 2;
      continue;
    }
    if (ASSIGNMENT.test(word)) {
      i++;
      continue;
    }
    break;
  }
  return i;
}

// The index after the first standalone "--" of a runlog.py wrapper.
function afterRunlog(list: Word[], index: number): number {
  for (let i = index; i < list.length; i++) {
    if (unquote(list[i]!.text) === "--") return i + 1;
  }
  return list.length;
}

// Leading wrappers are not the command word: strip them, and return the rest as written.
function stripWrappers(text: string): string {
  const list = words(text);
  let i = 0;
  while (i < list.length) {
    const raw = list[i]!.text;
    const name = wrapperName(raw);
    if (raw === "--") {
      i++;
      continue;
    }
    if (ASSIGNMENT.test(raw) || SIMPLE_WRAPPERS.has(name)) {
      i++;
      continue;
    }
    if (name.endsWith("runlog.py")) {
      const after = afterRunlog(list, i);
      if (after > i) {
        i = after;
        continue;
      }
      break;
    }
    if (name === "python" || name === "python3") {
      const next = list[i + 1];
      if (next !== undefined && wrapperName(next.text).endsWith("runlog.py")) {
        i = afterRunlog(list, i + 1);
        continue;
      }
      break;
    }
    if (name === "timeout") {
      i = afterTimeout(list, i);
      continue;
    }
    if (name === "env") {
      i = afterEnv(list, i);
      continue;
    }
    break;
  }
  const command = list[i];
  return command === undefined ? text : text.slice(command.start).trim();
}

// ---- engine-call recognition --------------------------------------------------------------------------------------

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

export function recognizeEngineCall(command: string, engines?: EngineSpec[]): EngineCall | null {
  const specs = engines ?? loadEngines();
  for (const part of segments(command)) {
    // A help or version word means the segment starts no session.
    if (hasHelpWord(part.text)) continue;
    const text = stripWrappers(part.text);
    for (const spec of specs) {
      if (!matches(spec.command, text)) continue;
      const fromFlag = outputFromFlags(text, spec.output_flags);
      const fromRedirect = outputFromRedirect(text);
      const outputFile = fromFlag ?? fromRedirect;
      return {
        engine: spec.name,
        outputFile,
        stdoutIsAnswer: spec.stdout_is_answer === true && fromRedirect === null,
        statusFile: spec.status_from_out_dir === true && outputFile !== null ? path.join(outputFile, "status.json") : null,
        background: part.background,
      };
    }
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

// A trap's regex is anchored to the command word; another process's line carries wrappers, so read it unanchored.
function unanchored(source: string): string {
  return source.replace(/^\^/, "");
}

function trapHits(part: Segment, trap: Trap, ctx: LintContext): boolean {
  const commandRegex = trap.command;
  if (typeof commandRegex !== "string" || !validRegex(commandRegex)) return false;
  if (hasHelpWord(part.text)) return false;
  const text = stripWrappers(part.text);
  if (!matches(commandRegex, text)) return false;
  if (trap.unless !== undefined && matches(trap.unless, text)) return false;
  if (trap.unless_piped === true && part.piped) return false;

  // background and concurrent are alternatives: one of them is enough; every other condition must hold.
  const alternatives: boolean[] = [];
  if (trap.background === true) alternatives.push(ctx.background === true || part.background);
  if (trap.concurrent === true) alternatives.push(ctx.running.some((line) => matches(unanchored(commandRegex), line)));
  if (alternatives.length > 0 && !alternatives.some(Boolean)) return false;

  if (trap.paths_outside_repo === true && !hasPathOutsideRepo(text, ctx.repoRoot)) return false;
  return true;
}

export function lintCommand(command: string, ctx: LintContext, traps: Trap[] = loadTraps()): Finding[] {
  const parts = segments(command);
  const findings: Finding[] = [];
  for (const trap of traps) {
    if (trap.status !== "approved" || trap.applies !== "command") continue;
    if (!parts.some((part) => trapHits(part, trap, ctx))) continue;
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

  // A wrapper writes a folder, so its own status file says whether the answer is empty.
  const answerEmpty = call.statusFile !== null
    ? false
    : outputFile === null
      ? call.stdoutIsAnswer && !/\S/.test(stdout)
      : fileMissing || fileEmpty;
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