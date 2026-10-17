// C6, the first version: of CACHES.md's Core requirements only B2.2 (the cache folder is ignored by git) and Rd1
// (no start hook or instruction opens a cache file) are checked. Rd1's scan reads the session-start surface —
// the harness settings, the git hooks, the instruction files — and never opens a file under
// `project-memory/.cache/` itself (Rd1, R2).
import { existsSync, readFileSync } from "node:fs";
import { cacheIsIgnored, sessionStartFiles } from "./gitchecks.ts";
import type { ClauseOutcome } from "./gitrequirements.ts";

const CACHE_REFERENCE = /(?:\bproject-memory\/)?\.cache\/[^\s`"')]*/;
const OPENS = /\b(read|open|load|cat|head|tail|less|more|sqlite3|query|search|grep|rg|glob|import|attach|select|list)\b/i;
const NEGATED = /\b(never|no|not|avoid|without|don'?t|do not|nothing)\b/i;

export function checkB22(root: string): ClauseOutcome {
  const result = cacheIsIgnored(root);
  if (result.ignored) {
    return {
      breaks: [],
      clean: `${result.command} → exit 0, ${result.output}`,
      couldNotRun: null,
    };
  }
  return {
    breaks: [
      `${result.command} → exit ${result.code}${result.output === "" ? ", no output" : `, ${result.output}`}: ` +
        "no ignore rule reports project-memory/.cache",
    ],
    clean: "",
    couldNotRun: null,
  };
}

export function checkRd1(root: string): ClauseOutcome {
  const files = sessionStartFiles(root).filter((file) => existsSync(file));
  const scanned: string[] = [];
  const breaks: string[] = [];
  for (const file of files) {
    let text = "";
    try {
      text = readFileSync(file, "utf8");
    } catch {
      scanned.push(`${file} (unreadable)`);
      continue;
    }
    scanned.push(file);
    text.split("\n").forEach((line, offset) => {
      if (!CACHE_REFERENCE.test(line)) return;
      if (!OPENS.test(line)) return;
      if (NEGATED.test(line)) return; // an instruction not to read a cache is not an instruction to read it
      breaks.push(`${file}:${offset + 1} — "${line.trim()}"`);
    });
  }
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null, notes: [`scanned: ${scanned.join(", ") || "nothing"}`] };
  return {
    breaks: [],
    clean:
      `${scanned.length} session-start file(s) scanned (${scanned.join(", ") || "none present"}): ` +
      "no line opens a file under project-memory/.cache/. A hook outside the repository is not visible here.",
    couldNotRun: null,
  };
}