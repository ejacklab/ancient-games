// R2, U3: the warning — one line per MUST that fails or could not run, and for a missing AGENTS.md, with ids and file
// names, never entry text; nothing else; empty when there are none. `--warn` prints it; the session-start hook that
// also prints it is a harness change R2 leaves to the owner (R12.3), and no file under project-memory/.cache/ is ever
// opened here (Rd1): nothing in the run reads a cache file, only whether the folder is there.
//
// The lines are built from three things and nothing else: the requirement id, the category that id stands for, and the
// file names in the evidence. No evidence prose and no part of an entry is ever copied into them, because the
// evidence quotes the entry — a claim, a source — and a warning is read in a session's first lines (R2).
import type { StagedEntry } from "./gitchecks.ts";
import type { CheckRun, RequirementResult, Verdict } from "./checks.ts";

/** The file names in an evidence line, and nothing else of the entry: no claim, no body, no text. An entry file is
 *  its bare file name, and a name with a space or a non-ASCII character in it was cut short (C12, A5). An entry path
 *  the evidence itself holds is named too, whole to its `.md`: an entry a staged or committed deletion names is in no
 *  staged state, so naming entries through the staged paths alone loses the file name R2 asks the warning to hold. */
const FILE_NAME = /(project-memory\/INDEX\.md|AGENTS\.md|project-memory\/entries\/[^\s]*\.md)/g;

/** What each id's failure is about, in words of the guideline rather than of the entry. */
const CATEGORY: Record<string, string> = {
  "SoT:W1.1a": "an entry's kind does not match its name, or its name was renamed",
  "SoT:W1.1b": "an entry's id is malformed, or was renamed",
  "SoT:W1.2a": "an entry's header block is missing or not closed",
  "SoT:W1.3a": "an entry has no claim or no Why",
  "SoT:W4.1b": "an entry's status is not one of active, superseded, retired",
  "SoT:K4.1": "an entry file was deleted, superseded without a link, or retired without a reason",
  "SoT:K4.3": "an entry's claim, source, depends_on or covers changed without the log line for it",
  "SoT:K6.1a": "INDEX.md does not match what the entries build",
  "SoT:K6.2": "the index has a line for an entry that is not active, or none for one that is",
  "SoT:K6.3a": "an entry holds an unresolved conflict marker",
  "SoT:Rd3.1a": "INDEX.md is over its size limit",
  "SoT:W6.1a": "one file holds more than one entry",
  "SoT:W6.3a": "a merge dropped what one side wrote",
};

const GENERIC: Record<Verdict, string> = {
  fail: "a clause of the guideline memory needs",
  "could not run": "a clause of the guideline memory could not be checked",
  pass: "",
  "needs a reviewer": "",
  "not applicable": "",
};

/** How each verdict the warning holds is said, in words of the guideline rather than of the entry. */
const SAYS: Record<Verdict, string> = {
  fail: "fails",
  "could not run": "could not run",
  pass: "",
  "needs a reviewer": "",
  "not applicable": "",
};

function filesIn(evidence: string, entries: readonly StagedEntry[]): string[] {
  const found = [...evidence.matchAll(FILE_NAME)].map((match) => match[1]!);
  // An entry is named by its full path, matched on the bare name the findings carry — the path it has in the staged
  // state, so a name with a space or a non-ASCII character in it is named whole (C12, A5).
  for (const one of entries) {
    if (evidence.includes(one.name)) found.push(one.path);
  }
  return [...new Set(found)];
}

function warningFor(result: RequirementResult, entries: readonly StagedEntry[]): string {
  const files = filesIn(result.evidence, entries);
  const where = files.length === 0 ? "" : ` — files: ${files.join(", ")}`;
  return `memory-check: ${result.id} ${SAYS[result.verdict]} — ${CATEGORY[result.id] ?? GENERIC[result.verdict]}${where}`;
}

export function renderWarning(run: CheckRun): string {
  // F1 failing is the missing AGENTS.md, which has its own line below: one line per thing, not two.
  // U3 wins over a narrower hook: a MUST that could not run is in the warning too, or a check that never
  // finished would read as a clean session.
  const lines = run.results
    .filter(
      (result) =>
        result.id !== "F1" &&
        result.level === "MUST" &&
        (result.verdict === "fail" || result.verdict === "could not run"),
    )
    .map((result) => warningFor(result, run.stagedEntries));
  const missingAgents = run.results.find((result) => result.id === "F1" && result.verdict === "fail");
  if (missingAgents) {
    lines.push(`memory-check: AGENTS.md is missing — file: ${run.root}/AGENTS.md (it is required, F1)`);
  }
  return lines.join("\n");
}