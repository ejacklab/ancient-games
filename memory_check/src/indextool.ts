// C3: the index and entry-format checks are `tools/memory_index.py --check`, run from the checked project's root
// and parsed. This file never judges those clauses itself — it maps each of the tool's own messages to the
// requirement id the message belongs to, and every result it gives carries the command and its output as evidence.
import { spawnSync } from "node:child_process";
import { MEMORY_INDEX_PY } from "./guidelines.ts";

export interface IndexToolRun {
  /** The command as it was run, for evidence. */
  readonly command: string;
  readonly code: number;
  readonly stdout: readonly string[];
  readonly stderr: readonly string[];
  /** Requirement id (SoT id, no prefix) -> the lines of the tool that found the break. */
  readonly findings: ReadonlyMap<string, readonly string[]>;
  /** `INDEX.md: 12/200 lines, 900/24000 bytes`, when the tool printed it. */
  readonly sizeLine: string | null;
  /** The tool's own over-limit failure (it prints this only after the index matched). */
  readonly overLimit: boolean;
  /** `project-memory/INDEX.md ... does not match what these entries build`. */
  readonly mismatch: boolean;
  /** `nothing to check: no project-memory/ in ...`. */
  readonly noMemory: boolean;
  /** `nothing to check: HEAD names no commit yet ...`. */
  readonly unbornHead: boolean;
  readonly upToDate: boolean;
  /** The index the entries build was measured against the size limits: the tool printed its size line. */
  readonly measured: boolean;
  /** The index was compared with what the entries build: the tool printed its size line and then judged it. */
  readonly compared: boolean;
  /** python itself failed: a traceback, an exit code no check of a memory uses, or no python3 at all. */
  readonly crashed: boolean;
  /** Problems the tool stopped on that name no requirement id: a check this tool cannot report either way. */
  readonly unmapped: readonly string[];
  /** Tool messages that name no requirement id: reported as notes, never dropped. */
  readonly notes: readonly string[];
}

const SIZE_LINE = /^INDEX\.md: (\d+)\/(\d+) lines, (\d+)\/(\d+) bytes/;

/** The index the tool judges, as it names itself (`INDEX_PATH`, tools/memory_index.py:40). */
const INDEX_NAME = "project-memory/INDEX.md";
const UP_TO_DATE = new RegExp(`^${INDEX_NAME.replace(/\//g, "\\/")} in .+ is up to date$`);
const MISMATCH = new RegExp(`${INDEX_NAME.replace(/\//g, "\\/")} in .+ does not match`);
const OVER_LIMIT = new RegExp(`${INDEX_NAME.replace(/\//g, "\\/")} in .+ is over the limit`);

/** A per-file problem as memory_index.py prints it: `<file name>: <problem>` (`tools/memory_index.py:385`). */
const PER_FILE = /^([^:]+): (.+)$/;

/** Which requirement each of memory_index.py's own problems belongs to. Order matters: longer patterns first. */
function idOfProblem(problem: string): string | null {
  if (/^kind .* is not one of/.test(problem)) return "W1.1a";
  if (/^kind .* does not match the/.test(problem)) return "W1.1a";
  if (/^id .* is not in the form/.test(problem)) return "W1.1b";
  if (/^(empty id|duplicate id)/.test(problem)) return "W1.1b";
  if (/^(no header|header is not closed)/.test(problem)) return "W1.2a";
  if (/^(no \*\*Why:\*\* line|empty claim)/.test(problem)) return "W1.3a";
  if (/^status .* is not one of/.test(problem)) return "W4.1b";
  if (/^unresolved conflict marker/.test(problem)) return "K6.3a";
  return null;
}

export function runMemoryIndex(root: string): IndexToolRun {
  const args = ["--check"];
  const result = spawnSync("python3", [MEMORY_INDEX_PY, ...args], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, GIT_OPTIONAL_LOCKS: "0" },
  });
  const code = result.status ?? -1;
  const stdout = (result.stdout ?? "").split("\n").filter((line) => line.trim() !== "");
  const stderr = (result.stderr ?? "").split("\n").filter((line) => line.trim() !== "");
  const command = `python3 ${MEMORY_INDEX_PY} --check   (in ${root})`;

  const findings = new Map<string, string[]>();
  const notes: string[] = [];
  const unmapped: string[] = [];
  let sizeLine: string | null = null;
  let overLimit = false;
  let mismatch = false;
  let noMemory = false;
  let unbornHead = false;
  let upToDate = false;

  const add = (id: string, line: string): void => {
    const bucket = findings.get(id) ?? [];
    bucket.push(line);
    findings.set(id, bucket);
  };

  for (const line of [...stdout, ...stderr]) {
    const message = line.trim();
    if (SIZE_LINE.test(message)) {
      sizeLine = message;
      continue;
    }
    if (/^nothing to check: no project-memory\//.test(message)) {
      noMemory = true;
      continue;
    }
    if (/^nothing to check: HEAD names no commit/.test(message)) {
      unbornHead = true;
      continue;
    }
    if (UP_TO_DATE.test(message)) {
      upToDate = true;
      continue;
    }
    if (MISMATCH.test(message)) {
      mismatch = true;
    }
    if (OVER_LIMIT.test(message)) {
      // The index's own size limit: the clause memory_index.py judges (Rd3.1a), reported as its own failure.
      overLimit = true;
      add("Rd3.1a", message);
      continue;
    }
    // The two index clauses share memory_index.py's one comparison: K6.1a and K6.2 are reported together (C3).
    if (/INDEX\.md in .* does not match what these entries build/.test(message)) {
      add("K6.1a", message);
      add("K6.2", message);
      continue;
    }
    const perFile = PER_FILE.exec(message);
    const problem = perFile ? perFile[2]! : message;
    const id = idOfProblem(problem);
    // memory_index.py calls a content problem in an inactive entry a warning and exits 0 on it, so one old entry
    // never blocks the build (its B2.5). W1.1a's fails_if names no status, and an entry whose kind does not match
    // its prefix breaks it whatever the entry's status is: that warning is a break here (C6). Every other warning
    // stays a note, so a clause the tool only warns about is never reported as a break (C3).
    const warned = /\(warning\)$/.test(message);
    if (id && (!warned || id === "W1.1a")) {
      for (const one of id.split(",")) add(one, message);
      continue;
    }
    // A problem the tool stopped on that names no requirement id: it is not a pass and not a fail here — it is a
    // check that could not run (C2, C3). Diff lines and fix hints arrive only after the size line, once the entries
    // were read, so they are never mistaken for one.
    if (!warned && sizeLine === null && !noMemory && !unbornHead && code !== 0) {
      unmapped.push(message);
      continue;
    }
    // Everything else the tool printed: a per-file warning, a diff line, a fix hint. Not a finding of a
    // requirement id, but never dropped.
    notes.push(message);
  }

  // The tool measures the index only after every entry parsed, so a size line means the entry checks all ran.
  const measured = sizeLine !== null;
  return {
    command,
    code,
    stdout,
    stderr,
    findings,
    sizeLine,
    overLimit,
    mismatch,
    noMemory,
    unbornHead,
    upToDate,
    measured,
    compared: measured && (upToDate || mismatch),
    crashed: code === -1 || (code !== 0 && code !== 1) || stderr.some((line) => /Traceback \(most recent call last\)/.test(line)),
    unmapped,
    notes,
  };
}

/** Whether the tool could not be run at all: no python3, or a crash of its own. */
export function toolFailedToStart(run: IndexToolRun): boolean {
  return run.crashed;
}

/** Why the index clauses did not run: the tool had no snapshot, or it stopped on the entries before comparing. */
export function indexChecksNotReached(run: IndexToolRun): string {
  if (run.noMemory || run.unbornHead) {
    return `memory_index.py had no snapshot to compare (${run.stdout.join(" ")}): the index clauses did not run (C2)`;
  }
  const stopped = [...run.stdout, ...run.stderr].filter((line) => line.trim() !== "" && !SIZE_LINE.test(line.trim()));
  return (
    `memory_index.py stopped at its entry checks and never compared ${INDEX_NAME}, so the index clauses did not ` +
    `run (C2): ${stopped.slice(0, 4).join(" | ") || `exit ${run.code}`}`
  );
}

