// C6, the first version: of CACHES.md's Core requirements only B2.2 (the cache folder is ignored by git) and Rd1
// (no start hook or instruction opens a cache file) are checked. Rd1's scan reads the session-start surface —
// the harness settings, the git hooks, the instruction files — and never opens a file under
// `project-memory/.cache/` itself (Rd1, R2).
import { existsSync, readFileSync, readdirSync, type Dirent } from "node:fs";
import path from "node:path";
import { cacheIsIgnored, sessionStartFiles } from "./gitchecks.ts";
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

/**
 * C6, the first version: of CACHES.md's Core requirements only B2.2 (the cache folder is ignored by git) and Rd1
 * (no start hook or instruction opens a cache file) are checked. Rd1's scan reads the session-start surface —
 * the harness settings, the git hooks, the instruction files — and never opens a file under
 * `project-memory/.cache/` itself (Rd1, R2). A session-start instruction the scan cannot decide is left to a
 * reviewer, not called a pass and not called a break (C2).
 */
export function checkRd1(root: string): ClauseOutcome {
  const files = sessionStartFiles(root).filter((file) => existsSync(file));
  const scanned: string[] = [];
  const breaks: string[] = [];
  const unresolved: string[] = [];
  for (const file of files) {
    let text = "";
    try {
      text = readFileSync(file, "utf8");
    } catch {
      scanned.push(`${file} (unreadable)`);
      continue;
    }
    scanned.push(`${file}:1-${text.split("\n").length}`); // the lines the scan covered, so a pass names file and line (C2)
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
  }
  const scannedNote = [`scanned: ${scanned.join(", ") || "nothing"}`];
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null, notes: scannedNote };
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
      `${files.length} session-start file(s) scanned (${scanned.join(", ") || "none present"}): no line of any of ` +
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
