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
    scanned.push(`${file}:1-${text.split("\n").length}`); // the lines the scan covered, so a pass names file and line (C2)
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
      `${files.length} session-start file(s) scanned (${scanned.join(", ") || "none present"}): no line of any of ` +
      "them opens a file under project-memory/.cache/. A hook outside the repository is not visible here.",
    couldNotRun: null,
  };
}
