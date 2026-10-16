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
// Shell words that lead a segment without being the command word (round 3, C19): loop and branch keywords,
// the negation operator and the brace group.
const SHELL_WORDS = new Set(["do", "then", "else", "elif", "!", "{", "}", "fi", "done"]);

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
    if (char === "\\" && quote !== "'" && i + 1 < text.length) {
      if (start < 0) start = i;
      i++;
      continue;
    }
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

// The heredoc a line opens: "<<WORD", "<<'WORD'", "<<"WORD"" or "<<-WORD", with or without a space before "<<" (C18).
function heredocIn(line: string): { word: string; tabs: boolean } | null {
  const found = line.match(/<<(-?)(?:'([^']*)'|"([^"]*)"|([A-Za-z_][A-Za-z0-9_]*))/);
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

// Simple commands, keeping their own redirections. A "&" of a redirection (2>&1, >&2, &>file) is not a separator,
// and a backtick opens a command substitution whose command is a simple command of its own (C19).
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
    // A backslash keeps the next character, outside quotes and inside double quotes (round 13: `"kind: \""`).
    if (char === "\\" && quote !== "'" && i + 1 < command.length) {
      current += char + command[i + 1]!;
      i++;
      continue;
    }
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
    if (char === "`") {
      separate("`");
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
    if (SHELL_WORDS.has(raw)) {
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

interface ShellWord {
  value: string; // the word as written, quotes kept
  quoted: boolean; // the word is one quoted string
  redirectTarget: boolean; // the word is the target of a redirect, not an argument
  stdout: boolean; // a redirect target of stdout ("> FILE", ">> FILE", "&> FILE")
}

// A redirection operator at the start of a word: ">", ">>", "2>", "2>>", "&>", "<", "<<", ">&2".
const REDIRECT_PREFIX = /^(?:\d*(?:>>?|<{1,2}|>&|<&)|&>>?)/;

function isQuotedWord(raw: string): boolean {
  return raw.length >= 2 && (raw.startsWith("\"") && raw.endsWith("\"") || raw.startsWith("'") && raw.endsWith("'"));
}

// The segment's words, quote-aware: a quoted word stays one word, and the target of a redirect is marked as one
// (the shell writes it, the command does not read it — round 3, C2 and C21).
function shellWords(text: string): ShellWord[] {
  const found: ShellWord[] = [];
  let targetNext = false;
  let targetStdout = false;
  for (const word of words(text)) {
    const quoted = isQuotedWord(word.text);
    const prefix = quoted ? null : REDIRECT_PREFIX.exec(word.text);
    // The word after a bare operator is that operator's target, whatever it looks like.
    if (targetNext && prefix === null) {
      targetNext = false;
      found.push({ value: word.text, quoted, redirectTarget: true, stdout: targetStdout });
      continue;
    }
    targetNext = false;
    if (prefix === null) {
      found.push({ value: word.text, quoted, redirectTarget: false, stdout: false });
      continue;
    }
    const rest = word.text.slice(prefix[0].length);
    const stdout = /^&?>/.test(prefix[0]);
    if (rest !== "") {
      found.push({ value: rest, quoted: false, redirectTarget: true, stdout });
      continue;
    }
    targetNext = true;
    targetStdout = stdout;
  }
  return found;
}

// The value after an output flag, read from the unquoted words of the segment: "-o FILE", "-o=FILE", "--out FILE",
// "--out=FILE". A flag inside a quoted prompt is prompt text (round 3, C2).
function outputFromFlags(command: string, flags: string[] | undefined): string | null {
  if (flags === undefined || flags.length === 0) return null;
  const list = shellWords(command);
  for (const [index, word] of list.entries()) {
    if (word.quoted || word.redirectTarget) continue;
    for (const flag of flags) {
      if (word.value === flag) {
        const next = list[index + 1];
        return next === undefined ? null : unquote(next.value);
      }
      if (word.value.startsWith(`${flag}=`)) return unquote(word.value.slice(flag.length + 1));
    }
  }
  return null;
}

// The target of a stdout redirect "> FILE" or ">> FILE"; a "2>" is not one.
function outputFromRedirect(command: string): string | null {
  let found: string | null = null;
  for (const word of shellWords(command)) {
    if (word.redirectTarget && word.stdout) found = unquote(word.value);
  }
  return found;
}

export function recognizeEngineCall(command: string, engines?: EngineSpec[]): EngineCall | null {
  return engineCallSite(command, process.cwd(), engines)?.call ?? null;
}

// ---- the command word and test runs (round 4, D1) ---------------------------------------------------------------

// The command word of one segment, after the wrappers of M1: what the segment actually runs. A segment that holds
// nothing but a redirect operator names no command.
export function commandWord(segment: string): string | null {
  const stripped = stripWrappers(segment);
  const first = words(stripped)[0];
  if (first === undefined) return null;
  const value = unquote(first.text);
  if (value === "" || REDIRECT_PREFIX.test(value)) return null;
  return value;
}

// The test runners of round 4, D1: the segment's stripped text must be the whole invocation, so `pytest-helper` and a
// prompt naming pytest are not test runs. The label is the runner as the specification writes it.
const TEST_RUNNERS: { label: string; pattern: RegExp }[] = [
  { label: "pytest", pattern: /^pytest(?:\s|$)/ },
  { label: "pytest", pattern: /^python[0-9.]*\s+-m\s+pytest(?:\s|$)/ },
  { label: "bun test", pattern: /^bun\s+test(?:\s|$)/ },
  { label: "npm test", pattern: /^npm\s+test(?:\s|$)/ },
  { label: "npm run test", pattern: /^npm\s+run\s+test(?:\s|$)/ },
  { label: "yarn test", pattern: /^yarn\s+test(?:\s|$)/ },
  { label: "pnpm test", pattern: /^pnpm\s+test(?:\s|$)/ },
  { label: "npx jest", pattern: /^npx\s+jest(?:\s|$)/ },
  { label: "npx vitest", pattern: /^npx\s+vitest(?:\s|$)/ },
  { label: "go test", pattern: /^go\s+test(?:\s|$)/ },
  { label: "cargo test", pattern: /^cargo\s+test(?:\s|$)/ },
];

// The runner of the first segment that is a test run, or null. Later segments count too: `cd work && pytest -q` runs
// the tests.
export function recognizeTestRun(command: string): string | null {
  for (const part of segments(command)) {
    if (hasHelpWord(part.text)) continue;
    const text = stripWrappers(part.text);
    const runner = TEST_RUNNERS.find((entry) => entry.pattern.test(text));
    if (runner !== undefined) return runner.label;
  }
  return null;
}

// Round 12, E2: the paths a test run names — each word of each test-run segment, a pytest `::<node>` suffix dropped,
// resolved in the folder the segment runs in. Flags and words that are no file resolve too; the caller matches.
export function testRunFiles(command: string, cwd: string): string[] {
  const parts = segments(command);
  const found: string[] = [];
  for (const [index, part] of parts.entries()) {
    if (hasHelpWord(part.text)) continue;
    const text = stripWrappers(part.text);
    if (!TEST_RUNNERS.some((entry) => entry.pattern.test(text))) continue;
    const folder = folderBefore(parts, index, cwd);
    for (const word of words(text)) {
      const value = unquote(word.text).replace(/::.*$/, "");
      if (value === "" || value.startsWith("-")) continue;
      found.push(path.resolve(folder, value));
    }
  }
  return found;
}

// ---- reads of files that are not there (round 13) ----------------------------------------------------------------

export interface MissingRead {
  reader: string;
  path: string; // as the command writes it
}

const READERS = new Set(["cat", "head", "grep", "sed"]);
// N1: the short flags whose value is the rest of the word or the next word, and the long ones that take a value.
const VALUE_LETTERS: Record<string, string> = { cat: "", head: "nc", grep: "efmABCdD", sed: "efl" };
const LONG_VALUES = new Set(["--regexp", "--file", "--max-count", "--after-context", "--before-context", "--context",
  "--directories", "--devices", "--include", "--exclude", "--exclude-dir", "--expression", "--line-length", "--lines",
  "--bytes"]);
const PROGRAM_FLAGS = new Set(["e", "f", "--regexp", "--file", "--expression"]);

// N1: the words of a read that name files — not flags, their values, redirects, or grep's pattern and sed's script.
function fileOperands(reader: string, text: string): string[] {
  const values = VALUE_LETTERS[reader] ?? "";
  const operands: string[] = [];
  let programGiven = false;
  let skipNext = false;
  let flagsEnded = false;
  for (const word of shellWords(text).slice(1)) {
    if (word.redirectTarget) continue;
    const value = unquote(word.value);
    if (skipNext) {
      skipNext = false;
      continue;
    }
    if (!flagsEnded && value === "--") {
      flagsEnded = true;
      continue;
    }
    if (!flagsEnded && !word.quoted && value.startsWith("--")) {
      const name = value.split("=")[0]!;
      if (PROGRAM_FLAGS.has(name)) programGiven = true;
      if (!value.includes("=") && LONG_VALUES.has(name)) skipNext = true;
      continue;
    }
    if (!flagsEnded && !word.quoted && value.startsWith("-") && value.length > 1) {
      const letters = value.slice(1);
      if (/^\d+$/.test(letters)) continue; // head -5
      for (const [index, letter] of [...letters].entries()) {
        if ((reader === "grep" || reader === "sed") && PROGRAM_FLAGS.has(letter)) programGiven = true;
        if (values.includes(letter)) {
          if (index === letters.length - 1) skipNext = true;
          break;
        }
      }
      continue;
    }
    operands.push(value);
  }
  if ((reader === "grep" || reader === "sed") && !programGiven) operands.shift();
  return operands.filter((operand) => operand !== "-");
}

// Commands that cannot make a file: an earlier one that names the read's folder is no sign the file was made (N3).
const READ_ONLY = new Set(["ls", "cat", "head", "tail", "grep", "wc", "echo", "printf", "cd", "test", "[", "stat", "pwd", "true"]);

// N3: a read whose stderr goes to /dev/null and whose exit cannot end the command (`;`, a newline or `|` follows) can
// neither print an error nor fail the command — a probe.
function probe(text: string, after: string): boolean {
  const silent = /(?:^|\s)(?:2>\s*\/dev\/null|&>\s*\/dev\/null)(?:\s|$)/.test(text) || /2>&1/.test(text) && />\s*\/dev\/null/.test(text);
  return silent && /^\s*(?:;|\n|\|(?!\|))/.test(after);
}

// N2–N3: the files a command reads that do not exist now, in the folder each read runs in. A file an earlier segment
// names may be made or tested there, a folder an earlier writing command names may be filled there, a read followed
// by `||` handles its own error, and a probe cannot fail; none is reported.
export function missingReads(command: string, cwd: string, exists: (file: string) => boolean = fs.existsSync): MissingRead[] {
  const parts = segments(command);
  const found: MissingRead[] = [];
  const home = process.env.HOME ?? "";
  let cursor = 0;
  for (const [index, part] of parts.entries()) {
    const at = command.indexOf(part.text, cursor);
    const end = at < 0 ? cursor : at + part.text.length;
    cursor = end;
    if (hasHelpWord(part.text)) continue;
    const text = stripWrappers(part.text);
    const reader = wrapperName(words(text)[0]?.text ?? "");
    if (!READERS.has(reader)) continue;
    const after = command.slice(end);
    if (/^\s*\|\|/.test(after) || probe(part.text, after)) continue;
    if (unknownCdBefore(command, Math.max(at, 0)) || /\(\s*cd\s/.test(command.slice(0, Math.max(at, 0)))) continue;
    const folder = folderBefore(parts, index, cwd);
    const before = parts.slice(0, index).map((segment) => ({ text: segment.text, word: wrapperName(words(stripWrappers(segment.text))[0]?.text ?? "") }));
    // An earlier read of the same file proves nothing about it; a command that makes or tests it does.
    const earlier = before.filter((segment) => !READERS.has(segment.word)).map((segment) => segment.text).join("\n");
    const writers = before.filter((segment) => !READ_ONLY.has(segment.word)).map((segment) => segment.text).join("\n");
    for (const operand of fileOperands(reader, text)) {
      if (unknowablePath(operand) || (operand.startsWith("~") && !operand.startsWith("~/"))) continue;
      const resolved = path.resolve(folder, operand.startsWith("~/") ? path.join(home, operand.slice(2)) : operand);
      if (exists(resolved)) continue;
      if (earlier.includes(operand) || earlier.includes(path.basename(operand))) continue;
      const parent = path.dirname(operand);
      if (parent !== "." && writers.includes(parent)) continue;
      found.push({ reader, path: operand });
    }
  }
  return found;
}

// ---- paths the text cannot name (round 4, D3) --------------------------------------------------------------------

// A path the shell decides, not the text: a variable, a command substitution or a glob.
const UNKNOWABLE = /[$`*?\[]/;

function unknowablePath(value: string): boolean {
  return UNKNOWABLE.test(value);
}

// The output the engine segment asks for, when the text does not say which file it is: a stdout redirect or an output
// flag whose target holds a variable, a backtick or a glob character, or is missing because the shell expands it.
function outputPathUnknown(text: string, flags: string[] | undefined): boolean {
  const list = words(text);
  for (const [index, word] of list.entries()) {
    const quoted = isQuotedWord(word.text);
    const prefix = quoted ? null : REDIRECT_PREFIX.exec(word.text);
    if (prefix !== null && /^&?>/.test(prefix[0])) {
      const rest = word.text.slice(prefix[0].length);
      if (rest !== "") return unknowablePath(unquote(rest));
      const next = list[index + 1];
      return next === undefined || unknowablePath(unquote(next.text));
    }
    // An output flag inside a quoted prompt is prompt text (round 3, C2).
    if (quoted) continue;
    for (const flag of flags ?? []) {
      if (word.text === flag) {
        const next = list[index + 1];
        return next === undefined || unknowablePath(unquote(next.text));
      }
      if (word.text.startsWith(`${flag}=`)) return unknowablePath(unquote(word.text.slice(flag.length + 1)));
    }
  }
  return false;
}

// The command split at newlines, `;`, `&&`, `||`, `|` and a single `&` outside quotes, but not at a backtick: a
// `cd `printf work`` stays one piece, so its target is seen as written.
function coarsePieces(command: string): { text: string; start: number }[] {
  const found: { text: string; start: number }[] = [];
  let quote: string | null = null;
  let start = 0;
  const flush = (end: number) => {
    const text = command.slice(start, end);
    if (text.trim() !== "") found.push({ text: text.trim(), start });
    start = end + 1;
  };
  for (let i = 0; i < command.length; i++) {
    const char = command[i]!;
    if (char === "\\" && quote !== "'" && i + 1 < command.length) {
      i++;
      continue;
    }
    if (quote !== null) {
      if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"') {
      quote = char;
      continue;
    }
    if (char === "\n" || char === ";" || char === "|") {
      flush(i);
      continue;
    }
    if (char === "&") {
      const next = command[i + 1];
      const previous = command[i - 1];
      if (next === "&") {
        flush(i);
        i++;
        continue;
      }
      if (next !== ">" && previous !== ">" && previous !== "&") flush(i);
    }
  }
  flush(command.length);
  return found;
}

// A `cd` the text cannot resolve, before the call: the folder the engine writes into is unknown.
function unknownCdBefore(command: string, engineStart: number): boolean {
  for (const piece of coarsePieces(command)) {
    if (piece.start >= engineStart) break;
    const list = words(stripWrappers(piece.text));
    if (list.length < 2 || wrapperName(list[0]!.text) !== "cd") continue;
    if (list.slice(1).some((word) => unknowablePath(unquote(word.text)))) return true;
  }
  return false;
}

// ---- where the call happens ---------------------------------------------------------------------------------------

// The call a command makes, with the folder it runs in, whether it ends the command, and whether the output path and
// the folder are knowable from the text at all. The hook needs all five: paths resolve in the folder the command cd'd
// into, a failing pipeline after the engine is not the engine's exit, and a path the shell decides is not checked.
export interface EngineCallSite {
  call: EngineCall;
  cwd: string; // the folder the engine segment runs in
  endsWithEngine: boolean; // the engine segment is the last segment of the command
  outputKnown: boolean; // the text names the output file
  cwdKnown: boolean; // every cd before the call names a folder
}

export function engineCallSite(command: string, cwd: string, engines?: EngineSpec[]): EngineCallSite | null {
  const specs = engines ?? loadEngines();
  const parts = segments(command);
  for (const [index, part] of parts.entries()) {
    // A help or version word means the segment starts no session.
    if (hasHelpWord(part.text)) continue;
    const text = stripWrappers(part.text);
    for (const spec of specs) {
      if (!matches(spec.command, text)) continue;
      const fromFlag = outputFromFlags(text, spec.output_flags);
      const fromRedirect = outputFromRedirect(text);
      const outputFile = fromFlag ?? fromRedirect;
      return {
        call: {
          engine: spec.name,
          outputFile,
          stdoutIsAnswer: spec.stdout_is_answer === true && fromRedirect === null,
          statusFile: spec.status_from_out_dir === true && outputFile !== null ? path.join(outputFile, "status.json") : null,
          background: part.background,
        },
        cwd: folderBefore(parts, index, cwd),
        endsWithEngine: index === parts.length - 1,
        outputKnown: !outputPathUnknown(text, spec.output_flags),
        // The raw offset of the segment's own text: what stands before it in the command is what can move the folder.
        cwdKnown: !unknownCdBefore(command, command.indexOf(part.text.trim())),
      };
    }
  }
  return null;
}

// The folder a `cd` before the engine segment moved the command into; a relative folder resolves against the last one.
function folderBefore(parts: Segment[], engineIndex: number, cwd: string): string {
  let folder = cwd;
  for (const part of parts.slice(0, engineIndex)) {
    const list = words(stripWrappers(part.text));
    if (list.length < 2 || unquote(list[0]!.text) !== "cd") continue;
    const target = unquote(list[1]!.text);
    if (target === "" || target === "-" || target.startsWith("-")) continue;
    folder = path.resolve(folder, expandHome(list[1]!.text, target));
  }
  return folder;
}

// An unquoted `~` or `~/…` is the home folder, as the shell expands it (round 13: `cd ~/dev/x` resolved as `./~/dev/x`).
function expandHome(raw: string, value: string): string {
  if (raw !== value) return value; // quoted: the shell does not expand it
  if (value === "~") return process.env.HOME ?? value;
  return value.startsWith("~/") ? path.join(process.env.HOME ?? "~", value.slice(2)) : value;
}

// ---- command lint -------------------------------------------------------------------------------------------------

// A path the command reads: an absolute path token of the segment, split on whitespace inside a quoted word too, but
// never the target of a redirect — the shell writes that one, the engine never reads it (round 3, C21).
function hasPathOutsideRepo(command: string, repoRoot: string): boolean {
  const root = path.resolve(repoRoot);
  const candidates: string[] = [];
  for (const word of shellWords(command)) {
    if (word.redirectTarget) continue;
    if (word.quoted) candidates.push(...unquote(word.value).split(/\s+/));
    else candidates.push(word.value);
  }
  for (const candidate of candidates) {
    if (!candidate.startsWith("/") || SPECIAL_PATHS.has(candidate)) continue;
    const resolved = path.resolve(candidate);
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