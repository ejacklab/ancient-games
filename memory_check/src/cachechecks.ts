// C6, the first version: of CACHES.md's Core requirements only B2.2 (the cache folder is ignored by git) and Rd1
// (no start hook or instruction opens a cache file) are checked. Rd1's scan reads the session-start surface —
// the harness settings, the git hooks, the instruction files — and never opens a file under
// `project-memory/.cache/` itself (Rd1, R2).
import { existsSync, readFileSync, readdirSync, type Dirent } from "node:fs";
import path from "node:path";
import { cacheIsIgnored, sessionStartFiles, stagedFiles, type GitErrors } from "./gitchecks.ts";
import type { ClauseOutcome } from "./gitrequirements.ts";

const CACHE_REFERENCE = /(?:\bproject-memory\/)?\.cache\/[^\s`"')]*/;
const OPENS = /\b(read|open|load|cat|head|tail|less|more|sqlite3|query|search|grep|rg|glob|import|attach|select|list)\b/i;
const NEGATED = /\b(never|no|not|avoid|without|don'?t|do not|nothing)\b/i;
/** What ties an instruction to the start of a session: Rd1's subject is the start of one, not any time (C6). */
const SESSION_START =
  /\b(at (?:the |a )?(?:session )?start|start of (?:the |a )?session|session start|on startup|at startup|when (?:a |the )?session (?:begins|starts)|every session|each session)\b/i;
/** Something that reaches the cache without saying so on the line: a run command, a hook or a script. */
const INDIRECT = /\b(script|hook|command|npm|pnpm|bun|yarn|bash|sh|tools\/)\b/i;
const CLAUSE_SPLIT = /[;,]|\bbut\b|\bhowever\b/;

/**
 * What one line says about the cache, and what the tool can decide about it:
 * - `opens` true and `atStart` false: an on-demand read, which CACHES.md allows — nothing to decide (Rd1 is about
 *   the start of a session).
 * - `opens` true, `atStart` true and not negated: an instruction to open a cache file at the start of a session —
 *   a break, with the line's number.
 * - `atStart` true with no verb the tool knows, or with a run command: the instruction is not clear enough to be
 *   called a break, and not clear enough to be cleared — the reviewer's (C2).
 * - `negated` true: an instruction not to read a cache is not an instruction to read it.
 */
interface LineReading {
  readonly atStart: boolean;
  readonly opens: boolean;
  readonly negated: boolean;
  readonly indirect: boolean;
}

function readLine(line: string): LineReading {
  const atStart = SESSION_START.test(line);
  // A clause is judged on its own words: a negation in one clause does not exempt another (a line that both forbids
  // and does the thing is not a clean "never read the cache").
  const clauses = line.split(CLAUSE_SPLIT).filter((clause) => clause.trim() !== "");
  const cacheClauses = clauses.filter((clause) => CACHE_REFERENCE.test(clause));
  const subject = cacheClauses.length > 0 ? cacheClauses.join(" ") : line;
  return {
    atStart,
    opens: OPENS.test(subject),
    negated: cacheClauses.length > 0 ? cacheClauses.every((clause) => NEGATED.test(clause)) : NEGATED.test(line),
    indirect: INDIRECT.test(subject),
  };
}

/** The harness settings files whose `hooks` name their events: a hook is a session-start hook by where it sits. */
const SETTINGS_FILES = new Set([".claude/settings.json", ".claude/settings.local.json"]);
const SESSION_START_EVENT = /^session_?start$/i;

/** Every `command` string under a value, however the hooks nest them. */
function commandsUnder(value: unknown): string[] {
  if (Array.isArray(value)) return value.flatMap(commandsUnder);
  if (value === null || typeof value !== "object") return [];
  return Object.entries(value).flatMap(([key, one]) =>
    key === "command" && typeof one === "string" ? [one] : commandsUnder(one),
  );
}

/**
 * The commands the SessionStart hooks of a harness settings file run. Such a command opens a cache file at the start
 * of a session by being registered there: it says nothing about *when* it runs, so the line-by-line wording test
 * cannot see it, and it was read as an on-demand read (C4, A3).
 */
function sessionStartHookCommands(text: string): string[] {
  let document: unknown;
  try {
    document = JSON.parse(text);
  } catch {
    return []; // not JSON: the line scan above is the whole reading of it
  }
  const hooks = (document as { hooks?: unknown } | null)?.hooks;
  if (hooks === null || typeof hooks !== "object") return [];
  const commands: string[] = [];
  for (const [event, entries] of Object.entries(hooks as Record<string, unknown>)) {
    if (SESSION_START_EVENT.test(event)) commands.push(...commandsUnder(entries));
  }
  return commands;
}

/**
 * C6, the first version: of CACHES.md's Core requirements only B2.2 (the cache folder is ignored by git) and Rd1
 * (no start hook or instruction opens a cache file) are checked. Rd1's scan reads the session-start surface —
 * the harness settings, the git hooks, the instruction files — and never opens a file under
 * `project-memory/.cache/` itself (Rd1, R2). A session-start instruction the scan cannot decide is left to a
 * reviewer, not called a pass and not called a break (C2).
 *
 * C5: a file git knows is read from the staging area, the snapshot this run reports on — a staged instruction that
 * the working tree already dropped is still what the commit says. A file in no staged version (an untracked one, a
 * hook inside `.git/`) has no staged bytes at all, so its working-tree file is what the session reads, and the
 * evidence says which of the two was read.
 */
export function checkRd1(root: string, errors: GitErrors): ClauseOutcome {
  const files = sessionStartFiles(root);
  const staged = stagedFiles(root, files.map((file) => path.relative(root, file)), errors);
  const scanned: string[] = [];
  const breaks: string[] = [];
  const unresolved: string[] = [];
  const unreadable: string[] = [];
  for (const file of files) {
    const fromStage = staged.get(path.relative(root, file));
    if (fromStage === undefined && !existsSync(file)) continue;
    let text: string;
    let from: string;
    if (fromStage !== undefined) {
      text = fromStage;
      from = "the staged state";
    } else {
      from = "the working tree (in no staged version)";
      try {
        text = readFileSync(file, "utf8");
      } catch (error) {
        // E-1: a file the scan could not read is a clause it did not check, not a clause with nothing in it (C2).
        const reason = error instanceof Error ? error.message : String(error);
        scanned.push(`${file} (unreadable)`);
        unreadable.push(`${file} (unreadable: ${reason})`);
        continue;
      }
    }
    // the lines the scan covered, so a pass names file and line (C2)
    scanned.push(`${file}, ${from}:1-${text.split("\n").length}`);
    text.split("\n").forEach((line, offset) => {
      if (!CACHE_REFERENCE.test(line)) return;
      const reading = readLine(line);
      if (!reading.atStart || reading.negated) return; // on demand, or an instruction never to read one
      if (reading.opens && !reading.indirect) {
        breaks.push(`${file}:${offset + 1} — "${line.trim()}"`);
        return;
      }
      // A cache at the start of a session this scan cannot read as an instruction to open one: a reviewer's.
      unresolved.push(
        `${file}:${offset + 1} — "${line.trim()}"${reading.indirect ? " runs something that may open it" : ""}`,
      );
    });
    // A SessionStart hook runs at the start of a session by being registered as one, whatever its command says (C4).
    if (!SETTINGS_FILES.has(path.relative(root, file))) continue;
    sessionStartHookCommands(text).forEach((command, offset) => {
      if (!CACHE_REFERENCE.test(command)) return;
      // A command is not prose: its words are arguments, so the negation rule, which is for instructions, does not
      // read one — `cat <cache> || echo not found` opens the cache and its "not found" is a fallback message.
      const reading = readLine(command);
      const where = `${file} — hooks.SessionStart[${offset}]: "${command.trim()}"`;
      if (reading.opens && !reading.indirect) breaks.push(where);
      else unresolved.push(`${where}${reading.indirect ? " runs something that may open it" : ""}`);
    });
  }
  const scannedNote = [`scanned: ${scanned.join(", ") || "nothing"}`];
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null, notes: scannedNote };
  if (unreadable.length > 0) {
    return {
      breaks: [],
      clean: "",
      couldNotRun:
        `${unreadable.join("; ")}: this scan could not read every session-start file, so it did not cover the ` +
        "whole surface Rd1 is about and cannot call it clean (C2, E-1)",
      notes: scannedNote,
    };
  }
  if (unresolved.length > 0) {
    return {
      breaks: [],
      clean: "",
      couldNotRun: null,
      unresolved,
      notes: scannedNote,
    };
  }
  return {
    breaks: [],
    clean:
      `${scanned.length} session-start file(s) scanned (${scanned.join(", ") || "none present"}): no line of any of ` +
      "them opens a file under project-memory/.cache/ at the start of a session. A hook outside the repository is " +
      "not visible here.",
    couldNotRun: null,
  };
}

/**
 * The ignore files git reads for this repository: every `.gitignore` in the working tree and the repository's own
 * exclude file. Named, never opened — `git check-ignore` decides, and its evidence says where it looked (C2). The
 * walk steps over `.git` and over any `.cache` folder, so nothing under `project-memory/.cache/` is opened (Rd1, R2).
 */
function ignoreRuleFiles(root: string): string[] {
  const files: string[] = [];
  const walk = (folder: string): void => {
    for (const one of listingOf(folder)) {
      if (one.name === ".gitignore") files.push(path.join(folder, one.name));
      else if (one.isDirectory()) walk(path.join(folder, one.name));
    }
  };
  walk(root);
  const exclude = path.join(root, ".git", "info", "exclude");
  if (existsSync(exclude)) files.push(exclude);
  return files;
}

function listingOf(folder: string): Dirent[] {
  try {
    return readdirSync(folder, { withFileTypes: true }).filter((one) => (one.isDirectory() ? one.name !== ".git" && one.name !== ".cache" : one.isFile()));
  } catch {
    return [];
  }
}

export function checkB22(root: string): ClauseOutcome {
  const result = cacheIsIgnored(root);
  const rules = `ignore rules git reads here: ${ignoreRuleFiles(root).join(", ") || "none (no .gitignore, no .git/info/exclude)"}`;
  if (result.ignored) {
    return {
      breaks: [],
      clean: `${result.command} → exit 0, ${result.output}; ${rules}`,
      couldNotRun: null,
    };
  }
  return {
    breaks: [
      `${result.command} → exit ${result.code}${result.output === "" ? ", no output" : `, ${result.output}`}: ` +
        `no ignore rule reports project-memory/.cache; ${rules}`,
    ],
    clean: "",
    couldNotRun: null,
  };
}
