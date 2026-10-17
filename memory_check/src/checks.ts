// C1, C2, C4, C6: every requirement of both guidelines gets one of the five results, with its evidence. The
// decision each record gets is named here, once: the nine `tool` records are `tools/memory_index.py --check`'s
// (C3), the clauses that tool does not reach are checked from the staged snapshot or from git history, and every
// record whose check needs a reviewer is "needs a reviewer" — never a pass and never a fail.
import { checkB22, checkRd1 } from "./cachechecks.ts";
import {
  type ClauseOutcome,
  checkEntryPrefixes,
  checkK41,
  checkK43,
  checkMerges,
  checkOneEntryPerFile,
  checkRenames,
} from "./gitrequirements.ts";
import {
  type SnapshotInfo,
  type UnstagedMemory,
  stagedEntries,
  stagedMemoryPaths,
  snapshotInfo,
  unstagedMemoryFiles,
} from "./gitchecks.ts";
import type { Guidelines, Level, SotRecord } from "./guidelines.ts";
import { type IndexToolRun, indexChecksNotReached, runMemoryIndex, toolFailedToStart } from "./indextool.ts";
import { agentsMdMissing, findLocations, type Location } from "./locations.ts";

export type Verdict = "pass" | "fail" | "needs a reviewer" | "not applicable" | "could not run";

export interface RequirementResult {
  /** `SoT:<id>`, `CACHES:<id>`, or the tool's own requirement id (F1, F2, F3). */
  readonly id: string;
  readonly level: string;
  readonly verdict: Verdict;
  /** Why: the file and line, the command and its output, or the reason there is none. Never empty. */
  readonly evidence: string;
  /** The record's own `fails_if`, quoted from the guideline. */
  readonly failsIf: string;
}

export interface CheckRun {
  readonly root: string;
  readonly snapshot: SnapshotInfo;
  /** R1: the files under `project-memory/` changed but not staged, so not checked (C5). */
  readonly unstaged: UnstagedMemory;
  readonly locations: readonly Location[];
  readonly results: readonly RequirementResult[];
  readonly indexTool: IndexToolRun;
  readonly notes: readonly string[];
  readonly guidelines: Guidelines;
  readonly exitCode: number;
}

/**
 * The records whose subject lives outside `project-memory/` (user and agent memory in the home folder). They keep
 * their result when `project-memory/` is absent; every other record is "not applicable" (C4).
 */
const OUTSIDE_PROJECT_MEMORY = new Set(["W3.5a", "W3.5b", "Rd1.1"]);

/**
 * The clauses `tools/memory_index.py --check` reaches only after every entry parsed: it prints no size line and
 * compares no index until then (`check_index`, tools/memory_index.py:494). A run that stopped before that checked
 * none of them, which is "could not run", never a pass (C2, C3).
 */
const AFTER_ENTRIES = new Set(["K6.1a", "K6.2", "Rd3.1a"]);

/** Why a record is "needs a reviewer". Every record that is not decided has its own reason, cited. */
const REVIEWER_REASON: Record<string, string> = {
  "W2.1b":
    "check: git — whether a commit changed code under a new decision needs that diff read against the entries " +
    "(design-decisions.md 6; research-q/compare.md, Where they agree)",
  "W4.2":
    "its fails_if ends \"with no written reason\", which no tool can see (research-q/compare.md, Where they agree)",
  "W5.1":
    "check: git; reviewer — whether a commit embodies a new decision, or a session writes what it learned, is " +
    "judged (design-decisions.md 6)",
  "W6.1b": "two agent sessions writing one journal file is not visible in git history (design-decisions.md 6)",
  "W6.2": "an edit lost without a conflict cannot be shown by git (design-decisions.md 6)",
  "K1.1":
    "check: git; reviewer — whether a commit changed the behaviour an entry governs needs that entry read " +
    "(design-decisions.md 6)",
  "K5.1":
    "its fails_if ends \"with no written reason\", and raw notes kept elsewhere are not in the repository " +
    "(research-q/compare.md, Where they agree)",
  "W3.5a": "check: reviewer — whether the project holds user memory or agent memory is the owner's call (F1 reports the locations; it does not judge what is in them)",
  "W3.5b": "check: reviewer — where user and agent memory live, and whether a reason is written, is the owner's",
  "Rd1.1": "check: reviewer — user and agent memory live in the home folder, and whether that layout has a written reason is the owner's",
};

const DEFAULT_REVIEWER_REASON =
  "its check is the project owner (or someone they name): the tool does not judge it, and never reports it as " +
  "passing or failing (C1, U4)";

export interface CheckOptions {
  readonly root: string;
  readonly home: string;
  readonly since: string | null;
  /** The report file this run will write, or null when it prints to stdout: F3's evidence. */
  readonly out: string | null;
  readonly guidelines: Guidelines;
}

export function runChecks(options: CheckOptions): CheckRun {
  const { root, home, since, guidelines } = options;
  const snapshot = snapshotInfo(root, since);
  // R1: named in the report, because no check reads the working tree (C5).
  const unstaged = unstagedMemoryFiles(root);
  const locations = findLocations(root, home);
const snapshotGitErrors: string[] = [];
  // C5: the snapshot this run reports on is the staged state, so its presence is the staged state's presence. The
  // working tree is what F1 names, and a staged-but-deleted memory is still memory the checks must judge. The read
  // that says whether any memory is staged keeps its own reasons: a read that failed is never read as "there is no
  // memory", which would make every record "not applicable" and the run exit 0 (E-1, C2).
  const memoryPathErrors: string[] = [];
  const projectMemory = stagedMemoryPaths(root, memoryPathErrors).length > 0;
  const stagedRead: StagedRead = { failed: memoryPathErrors.length > 0, reason: memoryPathErrors.join("; ") || null };
  snapshotGitErrors.push(...memoryPathErrors);
  const cachePresent = locations.some((one) => one.name === "project-memory/.cache/" && one.present);
  const staged = projectMemory ? stagedEntries(root, snapshotGitErrors) : [];
  const indexTool = runMemoryIndex(root);
  const notes: string[] = [];
  if (snapshotGitErrors.length > 0) notes.push(`the staged state could not be read: ${snapshotGitErrors.join("; ")}`);

  const renames = checkRenames(snapshot);
  const prefixes = checkEntryPrefixes(staged);
  const onePerFile = checkOneEntryPerFile(staged);
  const k41 = checkK41(staged, snapshot);
  const k43 = checkK43(staged, snapshot);
  const merges = checkMerges(snapshot);
  for (const outcome of [renames.prefixes, renames.ids, prefixes, onePerFile, k41, k43, merges]) {
    for (const note of outcome.notes ?? []) notes.push(note);
  }

  const results: RequirementResult[] = [];

  // --- the tool's own requirements (F1-F3) -------------------------------------------------------------------------

  const missingAgentsMd = agentsMdMissing(root);
  results.push({
    id: "F1",
    level: "MUST",
    verdict: missingAgentsMd ? "fail" : "pass",
    evidence: missingAgentsMd
      ? `${root}/AGENTS.md does not exist: AGENTS.md is required (F1)`
      : `${root}/AGENTS.md exists; ${locations.filter((one) => one.present).length} of ${locations.length} named locations present, ` +
        `${locations.filter((one) => !one.present).length} absent. This table is the working tree; every verdict below reads the ` +
        "staged state (C5)",
    failsIf:
      "a named location exists and is not found, one is reported that does not exist, or a missing AGENTS.md is not a failure",
  });
  results.push({
    id: "F2",
    level: "MUST",
    verdict: "pass",
    evidence: `project ${root} is the root of a git repository (git rev-parse --show-toplevel in it)`,
    failsIf: "a given path is ignored, or a path that is not a git root is checked instead of being a usage error",
  });
  results.push({
    id: "F3",
    level: "MUST",
    verdict: "pass",
    evidence:
      `this run created, changed and deleted nothing; it wrote ${options.out ? `only ${options.out}` : "nothing"}; ` +
      "every git call ran with GIT_OPTIONAL_LOCKS=0",
    failsIf: "a run changes, creates or deletes any file, ignored files included, other than the report",
  });

  // --- the records of SOURCE_OF_TRUTH_REQUIREMENTS.yaml ----------------------------------------------------------

  const context: SotContext = { projectMemory, stagedRead, indexTool, prefixes, onePerFile, k41, k43, merges, renames };
  for (const record of guidelines.sot) {
    results.push(sotResult(record, context));
  }

  // --- the Core requirements of CACHES.md --------------------------------------------------------------------------

  for (const record of guidelines.caches) {
    results.push(cachesResult(record.id, record.failsIf, cachePresent, root));
  }

  return {
    root,
    snapshot,
    unstaged,
    locations,
    results,
    indexTool,
    notes,
    guidelines,
    exitCode: exitCodeOf(results),
  };
}

/** R3: 0 when no MUST fails or could not run, 1 when one does. CACHES.md gives its requirements no level, so they
 *  cannot gate the exit code; the report says so. */
function exitCodeOf(results: readonly RequirementResult[]): number {
  return results.some(
    (result) => result.level === "MUST" && (result.verdict === "fail" || result.verdict === "could not run"),
  )
    ? 1
    : 0;
}

interface SotContext {
  readonly projectMemory: boolean;
  /** Whether the staged read that decided `projectMemory` worked, and why it did not when it did not (E-1). */
  readonly stagedRead: StagedRead;
  readonly indexTool: IndexToolRun;
  readonly prefixes: ClauseOutcome;
  readonly onePerFile: ClauseOutcome;
  readonly k41: ClauseOutcome;
  readonly k43: ClauseOutcome;
  readonly merges: ClauseOutcome;
  readonly renames: { prefixes: ClauseOutcome; ids: ClauseOutcome };
}

/** The read every SoT record about project memory is judged on: did it work? */
interface StagedRead {
  readonly failed: boolean;
  readonly reason: string | null;
}

function sotResult(record: SotRecord, context: SotContext): RequirementResult {
  const level: Level = record.level;
  const base = { id: `SoT:${record.id}`, level, failsIf: record.failsIf };
  if (!context.projectMemory && !OUTSIDE_PROJECT_MEMORY.has(record.id)) {
    // E-1: the read that would have found the memory failed, so its absence says nothing about this record (C2).
    if (context.stagedRead.failed && level !== "guidance") {
      return {
        ...base,
        verdict: "could not run",
        evidence:
          `the staged state this record is judged on could not be read (${context.stagedRead.reason}), so whether ` +
          "this memory is there is unknown, not absent (C2, E-1)",
      };
    }
    return {
      ...base,
      verdict: "not applicable",
      evidence:
        "project-memory/ is absent from the staged state this run checked (git ls-files -s -z -- " +
        "project-memory; F1 names what the working tree holds), so the memory this record is about is absent (C4)",
    };
  }
  if (level === "guidance") {
    return { ...base, verdict: "not applicable", evidence: "guidance: nothing to check (check: none)" };
  }
  return decidedByTool(record, context) ?? {
    ...base,
    verdict: "needs a reviewer",
    evidence: REVIEWER_REASON[record.id] ?? DEFAULT_REVIEWER_REASON,
  };
}

/** The clauses the tool decides for a record, or null when it decides none of them. */
function decidedByTool(record: SotRecord, context: SotContext): RequirementResult | null {
  const base = { id: `SoT:${record.id}`, level: record.level as Level, failsIf: record.failsIf };
  const run = context.indexTool;
  const toolEvidence = `${run.command} → exit ${run.code}${outputOf(run)}`;

  if (record.checks.includes("tool")) {
    if (toolFailedToStart(run)) {
      return {
        ...base,
        verdict: "could not run",
        evidence: `${run.command} could not be run: ${run.stderr.join(" ") || `exit ${run.code}`}`,
      };
    }
    // Rd3.1a's limit is checked by memory_index.py after it compared the index; when it stopped earlier that clause
    // did not run. Its own size line is reported, not judged here a second way (C3).
    if (record.id === "Rd3.1a" && run.mismatch && !run.overLimit && overLimitSize(run.sizeLine)) {
      return {
        ...base,
        verdict: "could not run",
        evidence:
          `${toolEvidence} — memory_index.py printed ${run.sizeLine} and then stopped at the K6 index comparison, ` +
          "before its limit check; nothing is judged here a second way (C3)",
      };
    }
    const findings = run.findings.get(record.id) ?? [];
    const mine = myClauseOf(record, context);
    const breaks = [...findings, ...(mine?.breaks ?? [])];
    if (breaks.length > 0) return { ...base, verdict: "fail", evidence: `${toolEvidence}; ${breaks.join("; ")}` };
    if (mine?.couldNotRun) return { ...base, verdict: "could not run", evidence: `${toolEvidence}; ${mine.couldNotRun}` };
    // E-1: this run's own staged read found memory and memory_index.py says it has no snapshot to check it — an
    // unborn HEAD, or object ids it does not read. One of the two reads is wrong about the same files, so no clause
    // the tool checks ran: "could not run", never a pass (C2, C3).
    if ((run.noMemory || run.unbornHead) && context.projectMemory) {
      return {
        ...base,
        verdict: "could not run",
        evidence:
          "git ls-files --cached -- project-memory found memory in the staged state this run checked, but " +
          `${indexChecksNotReached(run)}`,
      };
    }
    // The clauses memory_index.py only reaches after every entry parsed: not reaching them is never a pass (C2).
    if (AFTER_ENTRIES.has(record.id) && !run.compared) {
      return { ...base, verdict: "could not run", evidence: `${toolEvidence}; ${indexChecksNotReached(run)}` };
    }
    // The tool stopped on a problem that names no requirement id: it could not judge this clause either way (C2).
    if (run.unmapped.length > 0) {
      return {
        ...base,
        verdict: "could not run",
        evidence:
          `${toolEvidence}; memory_index.py stopped on problems that name no requirement id, so this clause did ` +
          `not run: ${run.unmapped.slice(0, 4).join(" | ")}`,
      };
    }
    if (record.checks.includes("reviewer")) {
      return {
        ...base,
        verdict: "needs a reviewer",
        evidence: `${toolEvidence}; the tool found no break in the clause it checks — ${DEFAULT_REVIEWER_REASON}`,
      };
    }
    return { ...base, verdict: "pass", evidence: `${toolEvidence}${mine ? `; ${mine.clean}` : ""}` };
  }

  switch (record.id) {
    case "K4.1":
      // C2: a record checked by the tool and by a reviewer fails when the tool finds a break, else needs a reviewer.
      return withReviewer(base, context.k41);
    case "K4.3":
      return fromOutcome(base, context.k43);
    case "W6.3a": {
      // C2: checked by the tool and by a reviewer — a break the tool finds fails, else it stays the reviewer's.
      if (context.merges.breaks.length > 0) {
        return { ...base, verdict: "fail", evidence: context.merges.breaks.join("; ") };
      }
      if (context.merges.couldNotRun) {
        return { ...base, verdict: "could not run", evidence: context.merges.couldNotRun };
      }
      return {
        ...base,
        verdict: "needs a reviewer",
        evidence:
          `${context.merges.clean}; whether the two entries that supersede one go unreported (the other half of ` +
          "W6.3a) is judged with the project owner (C2: checked by the tool and by a reviewer)",
      };
    }
    case "W6.1a":
      if (context.onePerFile.breaks.length > 0) {
        return { ...base, verdict: "fail", evidence: context.onePerFile.breaks.join("; ") };
      }
      if (context.onePerFile.couldNotRun) {
        return { ...base, verdict: "could not run", evidence: context.onePerFile.couldNotRun };
      }
      return {
        ...base,
        verdict: "needs a reviewer",
        evidence:
          `${context.onePerFile.clean}; whether a commit adds an entry to an existing file is judged with the ` +
          "project owner (C2: checked by the tool and by a reviewer)",
      };
    default:
      return null;
  }
}

/** The clause this tool judges itself for a record the tool also runs, or undefined when it judges none. */
function myClauseOf(record: SotRecord, context: SotContext): ClauseOutcome | undefined {
  switch (record.id) {
    case "W1.1a":
      return {
        breaks: [...context.prefixes.breaks, ...context.renames.prefixes.breaks],
        clean: `${context.prefixes.clean}; ${context.renames.prefixes.clean}`,
        couldNotRun: context.renames.prefixes.couldNotRun,
        notes: context.renames.prefixes.notes,
      };
    case "W1.1b":
      return context.renames.ids;
    case "K4.1":
      return context.k41;
    case "K4.3":
      return context.k43;
    case "W6.1a":
      return context.onePerFile;
    default:
      return undefined;
  }
}

function outputOf(run: IndexToolRun): string {
  const all = [...run.stdout, ...run.stderr];
  if (all.length === 0) return ", no output";
  const shown = all.slice(0, 4).join(" | ");
  const more = all.length > 4 ? ` … (${all.length - 4} more line(s) under Notes)` : "";
  return `, output: ${shown}${more}`;
}

/** The size line's own numbers, against the limits memory_index.py prints them with. */
function overLimitSize(sizeLine: string | null): boolean {
  if (sizeLine === null) return false;
  const match = /^INDEX\.md: (\d+)\/(\d+) lines, (\d+)\/(\d+) bytes$/.exec(sizeLine);
  if (!match) return false;
  return Number(match[1]) > Number(match[2]) || Number(match[3]) > Number(match[4]);
}

/** The clause of a CACHES requirement a result stands for, named in its evidence. */
function named(base: { id: string; level: string; failsIf: string }, clause: string, result: RequirementResult): RequirementResult {
  return { ...result, evidence: `clause ${clause}: ${result.evidence}` };
}

/** The one part of the warning the reviewer is asked about: what the tool cleared, and what it cannot judge. */
const MIXED_REVIEWER_REASON =
  "whether the written reason is one the owner accepts is judged (C2: a record the tool and a reviewer both check " +
  "is the reviewer's when the tool finds no break)";

/** A clause the tool judges, where the record also names a reviewer: a break fails, nothing broken is the reviewer's. */
function withReviewer(
  base: { id: string; level: string; failsIf: string },
  outcome: ClauseOutcome,
): RequirementResult {
  const result = fromOutcome(base, outcome);
  if (result.verdict !== "pass") return result;
  return {
    ...result,
    verdict: "needs a reviewer",
    evidence: `${result.evidence}; ${MIXED_REVIEWER_REASON}`,
  };
}

function fromOutcome(
  base: { id: string; level: string; failsIf: string },
  outcome: ClauseOutcome,
): RequirementResult {
  if (outcome.breaks.length > 0) {
    return { ...base, verdict: "fail", evidence: outcome.breaks.join("; ") };
  }
  if (outcome.couldNotRun) return { ...base, verdict: "could not run", evidence: outcome.couldNotRun };
  const unresolved = outcome.unresolved ?? [];
  if (unresolved.length > 0) {
    return {
      ...base,
      verdict: "needs a reviewer",
      evidence:
        `${unresolved.join("; ")} — a line of a session-start file this scan cannot read as an instruction to open ` +
        "a cache file nor as one never to, so it is the reviewer's (C2)",
    };
  }
  return { ...base, verdict: "pass", evidence: outcome.clean };
}

function cachesResult(id: string, failsIf: string, cachePresent: boolean, root: string): RequirementResult {
  const base = { id: `CACHES:${id}`, level: "not stated in CACHES.md", failsIf };
  // C4, C6 as changed: with no cache folder every cache requirement is "not applicable", B2.2 included. The cache
  // folder is named from the working tree and nowhere else: it is git-ignored, so it is in no snapshot.
  if (!cachePresent) {
    return {
      ...base,
      verdict: "not applicable",
      evidence:
        "project-memory/.cache/ is absent in the working tree (F1 names it; a git-ignored folder is in no snapshot), " +
        "so the cache requirements are not applicable (C4, C6)",
    };
  }
  // C6, v1: of the Core requirements only B2 (its clause B2.2) and Rd1 (its clause Rd1.1) are checked.
  if (id === "B2") return named(base, "B2.2", fromOutcome(base, checkB22(root)));
  if (id === "Rd1") return named(base, "Rd1.1", fromOutcome(base, checkRd1(root)));
  return {
    ...base,
    verdict: "needs a reviewer",
    evidence:
      "CACHES.md gives this requirement no level and no check field, and its check is the runtime behaviour of a " +
      "cache tool; only B2.2 and Rd1 are checked in this version (C6, design-decisions.md 7)",
  };
}