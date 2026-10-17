// C5: what the tool looked at. Files are read from the staged state (git index, stage 0) — the view
// `tools/memory_index.py --check` reads — and history from the commits since the first one that touches
// `project-memory/` (`--since` overrides), with the range named in the report. A shallow clone makes every
// history check "could not run", and so does a git command that fails: its empty output is never read as "nothing
// there" (C2). Every call here is read-only, with GIT_OPTIONAL_LOCKS=0.
import { spawnSync } from "node:child_process";
import { git, gitOut, lines } from "./git.ts";

const ENTRIES = "project-memory/entries";
const MEMORY = "project-memory";
const CACHE = "project-memory/.cache";
const COMMIT_MARK = "\u0001";

/** The reasons the git calls one check made failed: what "could not run" answers with (C2). */
export type GitErrors = string[];

/**
 * One read-only git call, and the reason it failed when it did. An empty string with a message in `errors` is never
 * read as "nothing there": a clause that needed the answer and could not get it is "could not run", where the empty
 * output of a failed command used to be taken for a clean result. An `optional` call is one whose question has
 * "nothing there" as an answer — `git rev-parse --verify --quiet`, which exits 1 on a revision that is not there.
 */
function gitRead(root: string, args: readonly string[], errors: GitErrors, optional = false): string {
  const result = git(root, args);
  if (result.code !== 0) {
    const detail = (result.stderr || result.stdout).trim();
    if (!(optional && detail === "")) {
      errors.push(`git ${args.join(" ")} failed: ${detail || `exit ${result.code}`}`);
    }
    return "";
  }
  return result.stdout;
}

export interface SnapshotInfo {
  readonly root: string;
  readonly shallow: boolean;
  /** What the report's first line names for files. */
  readonly filesView: string;
  /** What the report's first line names for history, with the range. Empty when it could not be read. */
  readonly historyView: string;
  readonly range: string | null;
  readonly firstTouching: string | null;
  readonly commitsInRange: number;
  /** The git calls that failed while the snapshot itself was read. */
  readonly errors: readonly string[];
}

export interface StagedEntry {
  readonly name: string;
  readonly path: string;
  readonly sha: string;
  readonly text: string;
}

export interface Rename {
  /** The commit the rename happened in, or null when it is staged and in no commit yet. */
  readonly commit: string | null;
  readonly from: string;
  readonly to: string;
}

export interface Deletion {
  /** The commit the deletion happened in, or null when it is staged and in no commit yet. */
  readonly commit: string | null;
  readonly path: string;
}

/** How a change is named in evidence: a commit of its own, or the staged state. */
export function whereOf(commit: string | null): string {
  return commit === null ? "the staged state" : `commit ${commit.slice(0, 7)}`;
}

/** The first commit that touches `project-memory/`, oldest first. */
function firstTouchingCommit(root: string, errors: GitErrors): string | null {
  const output = gitRead(root, ["log", "--reverse", "--format=%H", "--", MEMORY], errors);
  return lines(output)[0] ?? null;
}

export function snapshotInfo(root: string, since: string | null): SnapshotInfo {
  const errors: GitErrors = [];
  const shallow = gitRead(root, ["rev-parse", "--is-shallow-repository"], errors).trim() === "true";
  const filesView = "the staged state (git index, stage 0), the view `tools/memory_index.py --check` reads";
  const first = since ?? firstTouchingCommit(root, errors);
  if (!first) {
    return {
      root,
      shallow,
      filesView,
      historyView: shallow
        ? `could not run: this is a shallow clone, so the first commit touching ${MEMORY}/ is not here`
        : `no commits touch ${MEMORY}/: no history range to check`,
      range: null,
      firstTouching: null,
      commitsInRange: 0,
      errors,
    };
  }
  // The first commit that touches project-memory/ is inside the range: an entry's first version is its evidence.
  const parent = gitRead(root, ["rev-parse", "--verify", "--quiet", `${first}^`], errors, true).trim();
  const range = parent === "" ? "HEAD" : `${first}^..HEAD`;
  const count = Number(gitRead(root, ["rev-list", "--count", range], errors).trim() || "0");
  const short = gitRead(root, ["rev-parse", "--short", first], errors).trim() || first.slice(0, 7);
  return {
    root,
    shallow,
    filesView,
    historyView: shallow
      ? `${short}..HEAD (${count} commit${count === 1 ? "" : "s"} in a shallow clone: history checks could not run)`
      : `${short}..HEAD (${count} commit${count === 1 ? "" : "s"})`,
    range,
    firstTouching: first,
    commitsInRange: count,
    errors,
  };
}

/** Every path under `project-memory/` in the staged state: the snapshot itself (C5). */
export function stagedMemoryPaths(root: string, errors: GitErrors): string[] {
  const raw = gitRead(root, ["ls-files", "-z", "--cached", "--", MEMORY], errors);
  return raw.split("\0").filter((record) => record !== "");
}

/** The staged entry files and their staged bytes: `git ls-files -s`, then one `cat-file --batch`. */
export function stagedEntries(root: string, errors: GitErrors): StagedEntry[] {
  const raw = gitRead(root, ["ls-files", "-s", "-z", "--", ENTRIES], errors);
  const wanted: { name: string; path: string; sha: string }[] = [];
  for (const record of raw.split("\0")) {
    if (record === "") continue;
    const [meta, path] = record.split("\t");
    if (!meta || !path) continue;
    const fields = meta.trim().split(/\s+/);
    if (fields.length < 3 || fields[2] !== "0") continue; // not stage 0: a tree without conflicts has no other
    wanted.push({ name: path.slice(ENTRIES.length + 1), path, sha: fields[1] ?? "" });
  }
  const blobs = catFileBatch(root, wanted.map((entry) => entry.sha), errors);
  return wanted.map((entry) => ({ ...entry, text: blobs.get(entry.sha) ?? "" }));
}

/** One `git cat-file --batch` for many blobs; missing blobs come back absent, not as an error. */
export function catFileBatch(root: string, shas: readonly string[], errors: GitErrors): Map<string, string> {
  const blobs = new Map<string, string>();
  const wanted = [...new Set(shas.filter((sha) => sha !== ""))];
  if (wanted.length === 0) return blobs;
  const result = spawnSync("git", ["cat-file", "--batch"], {
    cwd: root,
    encoding: "buffer",
    input: Buffer.from(`${wanted.join("\n")}\n`, "ascii"),
    env: { ...process.env, GIT_OPTIONAL_LOCKS: "0" },
  });
  if (result.status !== 0) {
    errors.push(`git cat-file --batch failed: ${result.stderr?.toString().trim() || `exit ${result.status}`}`);
    return blobs;
  }
  const buffer = result.stdout ?? Buffer.alloc(0);
  let position = 0;
  while (position < buffer.length) {
    const newline = buffer.indexOf(0x0a, position);
    if (newline < 0) break;
    const header = buffer.subarray(position, newline).toString("ascii").split(" ");
    position = newline + 1;
    if (header.length < 3) continue; // "<sha> missing"
    const size = Number(header[2]);
    blobs.set(header[0] ?? "", buffer.subarray(position, position + size).toString("utf8"));
    position += size + 1;
  }
  return blobs;
}

function readNameStatus(raw: string): { renames: Rename[]; deletions: Deletion[] } {
  const renames: Rename[] = [];
  const deletions: Deletion[] = [];
  let commit: string | null = null;
  for (const line of lines(raw)) {
    if (line.startsWith(COMMIT_MARK)) {
      commit = line.slice(1);
      continue;
    }
    const fields = line.split("\t");
    if (fields[0]?.startsWith("R") && fields.length === 3) {
      renames.push({ commit, from: fields[1] ?? "", to: fields[2] ?? "" });
    } else if (fields[0]?.startsWith("D") && fields.length === 2) {
      deletions.push({ commit, path: fields[1] ?? "" });
    }
  }
  return { renames, deletions };
}

/** The renames and deletions of the entry files in a range of commits (`git log -M --name-status`). */
function committedNameStatus(root: string, range: string | null, errors: GitErrors): { renames: Rename[]; deletions: Deletion[] } {
  const args = ["log", ...(range ? [range] : []), "--format=%x01%H", "-M", "--name-status", "--", ENTRIES];
  return readNameStatus(gitRead(root, args, errors));
}

/**
 * The renames and deletions of the entry files in the staged diff (`git diff --cached -M --name-status`): a
 * deletion or rename that is staged is in no commit yet, and history alone would never show it (K4.1, W1.1).
 */
function stagedNameStatus(root: string, errors: GitErrors): { renames: Rename[]; deletions: Deletion[] } {
  if (gitRead(root, ["rev-parse", "--verify", "--quiet", "HEAD"], errors, true).trim() === "") {
    return { renames: [], deletions: [] }; // nothing is staged against: no commit names a previous state
  }
  return readNameStatus(gitRead(root, ["diff", "--cached", "-M", "--name-status", "--", ENTRIES], errors));
}

/** Every rename of an entry file, committed or staged. */
export function entryRenames(root: string, range: string | null, errors: GitErrors): Rename[] {
  return [...committedNameStatus(root, range, errors).renames, ...stagedNameStatus(root, errors).renames];
}

/** Every deletion of an entry file, committed or staged. */
export function entryDeletions(root: string, range: string | null, errors: GitErrors): Deletion[] {
  return [...committedNameStatus(root, range, errors).deletions, ...stagedNameStatus(root, errors).deletions];
}

/** The merge commits in the range with their parents: `git log --format=%H %P`, the commits with two parents or more. */
export function mergeCommits(root: string, range: string | null, errors: GitErrors): { commit: string; parents: string[] }[] {
  const args = ["log", ...(range ? [range] : []), "--format=%H %P"];
  const merges: { commit: string; parents: string[] }[] = [];
  for (const line of lines(gitRead(root, args, errors))) {
    const parts = line.split(" ").filter((one) => one !== "");
    if (parts.length > 2) merges.push({ commit: parts[0] ?? "", parents: parts.slice(1) });
  }
  return merges;
}

/** The entry files a revision holds: `git ls-tree -r --name-only <rev> -- project-memory/entries`. */
export function entryFilesAt(root: string, rev: string, errors: GitErrors): string[] {
  return lines(gitRead(root, ["ls-tree", "-r", "--name-only", rev, "--", ENTRIES], errors));
}

/** The blob id a revision holds for a path, or an empty string when it holds none. */
export function blobIdAt(root: string, rev: string, path: string, errors: GitErrors): string {
  return gitRead(root, ["rev-parse", "--verify", "--quiet", `${rev}:${path}`], errors, true).trim();
}

/** Whether a revision has a parent commit: a root commit has none, and nothing was there before it. */
export function hasParent(root: string, rev: string, errors: GitErrors): boolean {
  return gitRead(root, ["rev-parse", "--verify", "--quiet", `${rev}^`], errors, true).trim() !== "";
}

/** The commits in the range that changed a path, oldest first: `git log --format=%H -- <path>`, reversed. */
export function commitsOf(root: string, range: string | null, path: string, errors: GitErrors): string[] {
  const args = ["log", ...(range ? [range] : []), "--format=%H", "--", path];
  return lines(gitRead(root, args, errors)).reverse();
}

/** The text a revision holds for a path, or null when it holds none. */
export function textAt(root: string, rev: string, path: string, errors: GitErrors): string | null {
  const sha = blobIdAt(root, rev, path, errors);
  if (sha === "") return null;
  return catFileBatch(root, [sha], errors).get(sha) ?? null;
}

/**
 * The entry files a merge holds that one of its parents held and it does not: the whole entry a side added, lost in
 * the merge result. `git log --diff-filter=D` never shows it, because a merge has no diff of its own against one
 * parent by default, so every parent is compared with the result here (K4.1).
 */
export function entriesDroppedByMerges(
  root: string,
  range: string | null,
  errors: GitErrors,
): { merge: string; parent: string; path: string }[] {
  const dropped: { merge: string; parent: string; path: string }[] = [];
  for (const merge of mergeCommits(root, range, errors)) {
    const merged = new Set(entryFilesAt(root, merge.commit, errors));
    for (const parent of merge.parents) {
      for (const path of entryFilesAt(root, parent, errors)) {
        if (!merged.has(path)) dropped.push({ merge: merge.commit, parent, path });
      }
    }
  }
  return dropped;
}

/** B2.2: `git check-ignore` on the cache folder, and the output as evidence either way. */
export function cacheIsIgnored(root: string): { ignored: boolean; command: string; code: number; output: string } {
  const result = git(root, ["check-ignore", "-v", CACHE]);
  const output = (result.stdout + result.stderr).trim();
  return {
    ignored: result.code === 0,
    command: `git check-ignore -v project-memory/.cache   (in ${root})`,
    code: result.code,
    output,
  };
}

/**
 * Rd1: the session-start surface a hook or an instruction can live in — the harness settings' hooks, the git
 * hooks the repository uses, and the instruction files. Each file that exists is read; nothing under
 * `project-memory/.cache/` is ever opened (R2, Rd1).
 */
export function sessionStartFiles(root: string): string[] {
  const candidates = [
    "AGENTS.md",
    "CLAUDE.md",
    ".claude/settings.json",
    ".claude/settings.local.json",
    ".claude/CLAUDE.md",
    ".codex/AGENTS.md",
    ".gemini/GEMINI.md",
    ".github/copilot-instructions.md",
  ];
  const files = candidates.map((candidate) => `${root}/${candidate}`);
  const hooksPath = gitOut(root, ["config", "--get", "core.hooksPath"]);
  const hookDir = hooksPath !== "" ? `${root}/${hooksPath}` : `${root}/.git/hooks`;
  for (const hook of ["pre-commit", "prepare-commit-msg", "post-commit", "post-checkout", "commit-msg", "pre-push"]) {
    files.push(`${hookDir}/${hook}`);
  }
  return files;
}