// C5: what the tool looked at. Files are read from the staged state (git index, stage 0) — the view
// `tools/memory_index.py --check` reads — and history from the commits since the first one that touches
// `project-memory/` (`--since` overrides), with the range named in the report. A shallow clone makes every
// history check "could not run". Every call here is read-only, with GIT_OPTIONAL_LOCKS=0.
import { spawnSync } from "node:child_process";
import { git, gitOut, lines } from "./git.ts";

const ENTRIES = "project-memory/entries";
const MEMORY = "project-memory";
const CACHE = "project-memory/.cache";

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
}

export interface StagedEntry {
  readonly name: string;
  readonly path: string;
  readonly sha: string;
  readonly text: string;
}

export interface Rename {
  readonly commit: string;
  readonly from: string;
  readonly to: string;
}

export interface Deletion {
  readonly commit: string;
  readonly path: string;
}

/** The first commit that touches `project-memory/`, oldest first. */
function firstTouchingCommit(root: string): string | null {
  const output = gitOut(root, ["log", "--reverse", "--format=%H", "--", MEMORY]);
  const first = lines(output)[0];
  return first ?? null;
}

export function snapshotInfo(root: string, since: string | null): SnapshotInfo {
  const shallow = gitOut(root, ["rev-parse", "--is-shallow-repository"]) === "true";
  const filesView = "the staged state (git index, stage 0), the view `tools/memory_index.py --check` reads";
  const first = since ?? firstTouchingCommit(root);
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
    };
  }
  // The first commit that touches project-memory/ is inside the range: an entry's first version is its evidence.
  const parent = gitOut(root, ["rev-parse", "--verify", "--quiet", `${first}^`]);
  const range = parent === "" ? "HEAD" : `${first}^..HEAD`;
  const count = Number(gitOut(root, ["rev-list", "--count", range]) || "0");
  const short = gitOut(root, ["rev-parse", "--short", first]) || first.slice(0, 7);
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
  };
}

/** The staged entry files and their staged bytes: `git ls-files -s`, then one `cat-file --batch`. */
export function stagedEntries(root: string): StagedEntry[] {
  const raw = gitOut(root, ["ls-files", "-s", "-z", "--", ENTRIES]);
  const wanted: { name: string; path: string; sha: string }[] = [];
  for (const record of raw.split("\0")) {
    if (record === "") continue;
    const [meta, path] = record.split("\t");
    if (!meta || !path) continue;
    const fields = meta.trim().split(/\s+/);
    if (fields.length < 3 || fields[2] !== "0") continue; // not stage 0: a tree without conflicts has no other
    wanted.push({ name: path.slice(ENTRIES.length + 1), path, sha: fields[1] ?? "" });
  }
  const blobs = catFileBatch(root, wanted.map((entry) => entry.sha));
  return wanted.map((entry) => ({ ...entry, text: blobs.get(entry.sha) ?? "" }));
}

/** One `git cat-file --batch` for many blobs; missing blobs come back absent, not as an error. */
export function catFileBatch(root: string, shas: readonly string[]): Map<string, string> {
  const blobs = new Map<string, string>();
  const wanted = [...new Set(shas.filter((sha) => sha !== ""))];
  if (wanted.length === 0) return blobs;
  const result = spawnSync("git", ["cat-file", "--batch"], {
    cwd: root,
    encoding: "buffer",
    input: Buffer.from(`${wanted.join("\n")}\n`, "ascii"),
    env: { ...process.env, GIT_OPTIONAL_LOCKS: "0" },
  });
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

/** `--name-status` output of a range: the renames and the deletions of the entry files. */
function nameStatus(root: string, range: string | null): { renames: Rename[]; deletions: Deletion[] } {
  const args = ["log", ...(range ? [range] : []), "--format=%x01%H", "-M", "--name-status", "--", ENTRIES];
  const renames: Rename[] = [];
  const deletions: Deletion[] = [];
  let commit = "";
  for (const line of lines(gitOut(root, args))) {
    if (line.startsWith("\u0001")) {
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

export function entryRenames(root: string, range: string | null): Rename[] {
  return nameStatus(root, range).renames;
}

export function entryDeletions(root: string, range: string | null): Deletion[] {
  return nameStatus(root, range).deletions;
}

/** The merge commits in the range with their parents: `git log --format=%H %P`, the commits with two parents or more. */
export function mergeCommits(root: string, range: string | null): { commit: string; parents: string[] }[] {
  const args = ["log", ...(range ? [range] : []), "--format=%H %P"];
  const merges: { commit: string; parents: string[] }[] = [];
  for (const line of lines(gitOut(root, args))) {
    const parts = line.split(" ").filter((one) => one !== "");
    if (parts.length > 2) merges.push({ commit: parts[0] ?? "", parents: parts.slice(1) });
  }
  return merges;
}

/** The entry files a revision holds: `git ls-tree -r --name-only <rev> -- project-memory/entries`. */
export function entryFilesAt(root: string, rev: string): string[] {
  return lines(gitOut(root, ["ls-tree", "-r", "--name-only", rev, "--", ENTRIES]));
}

/** The blob id a revision holds for a path, or an empty string when it holds none. */
export function blobIdAt(root: string, rev: string, path: string): string {
  return gitOut(root, ["rev-parse", "--verify", "--quiet", `${rev}:${path}`]);
}

/** The commit that added a file, and the blob id of that first version. */
export function firstVersionOf(
  root: string,
  range: string | null,
  path: string,
): { commit: string; sha: string } | null {
  const args = ["log", ...(range ? [range] : []), "--diff-filter=A", "--format=%H", "--", path];
  const commits = lines(gitOut(root, args));
  const commit = commits[commits.length - 1];
  if (!commit) return null;
  const sha = gitOut(root, ["rev-parse", `${commit}:${path}`]);
  return sha === "" ? null : { commit, sha };
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