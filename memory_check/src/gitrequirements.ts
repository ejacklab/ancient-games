// The clauses the tool judges itself, from the staged snapshot or from git history: the entry-name prefix W1.1a
// does not reach, one file per entry (W6.1a), an entry file is never deleted and says what replaced it (K4.1),
// an entry's claim, `source`, `depends_on` and `covers` never change silently (K4.3), a merge keeps what both sides
// wrote (W6.3a), and the git half of W1.1a and W1.1b (an entry file renamed to another prefix or another id). Every
// break carries its file and line, or the command and its output (C2).
import { nameParts, parseEntry, type Entry } from "./entry.ts";
import {
  blobIdAt,
  catFileBatch,
  commitsOf,
  entryDeletions,
  entryFilesAt,
  entryRenames,
  entriesDroppedByMerges,
  hasParent,
  mergeCommits,
  textAt,
  type GitErrors,
  type SnapshotInfo,
  type StagedEntry,
  whereOf,
} from "./gitchecks.ts";

export interface ClauseOutcome {
  /** One evidence line per break found. Empty when nothing broke. */
  readonly breaks: readonly string[];
  /** The evidence that says what was checked, when nothing broke. */
  readonly clean: string;
  /** Set when the check could not run: the reason. */
  readonly couldNotRun: string | null;
  /** Things the scan could not decide either way: a reviewer's, never a pass and never a fail (C2). */
  readonly unresolved?: readonly string[];
  /** Things a reader should know that are not breaks (a name not in the W1.1c form, for instance). */
  readonly notes?: readonly string[];
}

const SHALLOW = "this is a shallow clone, so the history this clause needs is not here (C5)";

function short(sha: string): string {
  return sha.slice(0, 7);
}

function truncate(text: string, limit = 90): string {
  const one = text.replace(/\s+/g, " ").trim();
  return one.length <= limit ? one : `${one.slice(0, limit - 1)}…`;
}

function parsed(staged: readonly StagedEntry[]): { staged: StagedEntry; entry: Entry }[] {
  return staged
    .map((one) => ({ staged: one, entry: parseEntry(one.name, one.text) }))
    .filter((one) => one.entry.headerEndLine > 0);
}

/** A git call of the snapshot itself failed: every history clause that needed it could not run. */
function snapshotErrors(snapshot: SnapshotInfo, errors: GitErrors): string[] {
  return [...snapshot.errors, ...errors];
}

/** W1.1a's clause memory_index.py does not check: it only reads `^[DFLOH]-` names, so it never sees another name. */
export function checkEntryPrefixes(staged: readonly StagedEntry[]): ClauseOutcome {
  const breaks: string[] = [];
  for (const one of staged) {
    if (!one.name.endsWith(".md")) continue;
    if (!/^[DFLOH]-/.test(one.name)) {
      breaks.push(`${one.path}:1 — the prefix "${one.name.slice(0, 1)}" is not one of D F L O H`);
    }
  }
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  return {
    breaks: [],
    clean: `${staged.length} staged file(s) under project-memory/entries/, every name's prefix is one of D F L O H`,
    couldNotRun: null,
  };
}

/** W6.1a's mechanical clause: one file holds one entry. */
export function checkOneEntryPerFile(staged: readonly StagedEntry[]): ClauseOutcome {
  const breaks: string[] = [];
  for (const { staged: one, entry } of parsed(staged)) {
    if (entry.idLines.length > 1) {
      breaks.push(`${one.path}:${entry.idLines[1]} — a second id: line; one file holds one entry`);
    } else if (entry.headerBlocks > 1) {
      breaks.push(`${one.path}:${entry.headerEndLine} — a second --- header block; one file holds one entry`);
    }
  }
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  return {
    breaks: [],
    clean: `${staged.length} staged entry file(s), each with one header block and one id:`,
    couldNotRun: null,
  };
}

/** K4.1: an entry file is never deleted; a superseded entry says what replaced it; a retired entry gives its reason. */
export function checkK41(staged: readonly StagedEntry[], snapshot: SnapshotInfo): ClauseOutcome {
  const breaks: string[] = [];
  for (const { staged: one, entry } of parsed(staged)) {
    checkHeader(one.path, entry, breaks);
  }
  const errors: GitErrors = [];
  if (!snapshot.shallow) {
    for (const deletion of entryDeletions(snapshot.root, snapshot.range, errors)) {
      breaks.push(
        `${whereOf(deletion.commit)} deleted ${deletion.path} — an entry file is never deleted ` +
          "(git log --diff-filter=D --name-status -- project-memory/entries, and git diff --cached --name-status)",
      );
    }
    // A merge holds no diff of its own against one parent by default: every parent is compared with its result, so
    // the whole entry one side added cannot vanish in a merge without a name here (K4.1).
    for (const dropped of entriesDroppedByMerges(snapshot.root, snapshot.range, errors)) {
      breaks.push(
        `commit ${short(dropped.merge)} holds ${dropped.path}, which parent ${short(dropped.parent)} held and the ` +
          `merge result does not — an entry file is never deleted (git ls-tree -r ${dropped.parent} vs ` +
          `${short(dropped.merge)} -- project-memory/entries)`,
      );
    }
  }
  const couldNotRun = [...snapshotErrors(snapshot, errors)];
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  if (couldNotRun.length > 0) return { breaks: [], clean: "", couldNotRun: reasons(couldNotRun) };
  if (snapshot.shallow) {
    return {
      breaks: [],
      clean: "",
      couldNotRun: `${SHALLOW}; the superseded_by and retired checks on the staged state still ran`,
    };
  }
  return {
    breaks: [],
    clean:
      `${staged.length} staged entry file(s): no status: superseded without superseded_by, no status: retired ` +
      `without a reason in its changed: line; git log --diff-filter=D --name-status and git diff --cached ` +
      `--name-status -- project-memory/entries (${snapshot.range}) deleted none, and no merge dropped an entry`,
    couldNotRun: null,
  };
}

/** What "could not run" says: the git calls that failed, named (C2). */
function reasons(errors: readonly string[]): string {
  const first = errors[0] ?? "";
  const more = errors.length > 1 ? ` … (${errors.length - 1} more failed call(s))` : "";
  return `a git command failed, so this clause could not run (C2): ${first}${more}`;
}

/** A field that says "nothing here": an empty value, or the empty list the format's own examples use. */
function linksNothing(value: string | undefined): boolean {
  const one = (value ?? "").replace(/\s+/g, " ").trim().toLowerCase();
  return one === "" || one === "[]" || one === "- none" || one === "none" || one === "(none)";
}

function checkHeader(path: string, entry: Entry, breaks: string[]): void {
  const status = entry.fields.get("status");
  const statusValue = status?.full ?? "";
  if (statusValue === "superseded" && linksNothing(entry.fields.get("superseded_by")?.full)) {
    breaks.push(`${path}:${status?.line ?? 1} — status: superseded with no superseded_by link`);
  }
  if (statusValue === "retired") {
    const changed = entry.fields.get("changed");
    const items = (changed?.items ?? []).filter((item) => item.trim() !== "");
    if (items.length === 0) {
      breaks.push(`${path}:${status?.line ?? 1} — status: retired with no changed: line naming the reason`);
    }
  }
}

/** One version of an entry: a revision that holds it, or the staged state. */
interface Version {
  readonly where: string;
  readonly text: string;
  readonly entry: Entry;
}

/**
 * K4.3: after its first commit an entry only gains lines; its claim, `source` and `depends_on` never change, and
 * every change to `covers` has a `changed:` line of its own. Every transition inside the range is compared, not
 * only the two ends: a claim rewritten and then restored is a break like any other, and one `changed:` line from
 * long ago does not excuse a later `covers` edit.
 */
export function checkK43(staged: readonly StagedEntry[], snapshot: SnapshotInfo): ClauseOutcome {
  const withHeader = parsed(staged);
  if (snapshot.shallow) {
    return { breaks: [], clean: "", couldNotRun: SHALLOW };
  }
  const errors: GitErrors = [];
  const breaks: string[] = [];
  const comparedAt: string[] = [];
  let transitions = 0;

  for (const { staged: one } of withHeader) {
    const { baseline, versions } = versionsOf(snapshot, one, errors);
    for (const [index, version] of versions.entries()) {
      const before = index === 0 ? baseline : versions[index - 1]!.text;
      if (before === null) continue; // the entry did not exist: its first version is not a change of a claim
      transitions += 1;
      comparedAt.push(`${one.path}:${version.entry.claimLine}`);
      for (const breakLine of transitionBreaks(one.path, parseEntry(one.name, before), version)) breaks.push(breakLine);
    }
  }
  const couldNotRun = snapshotErrors(snapshot, errors);
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  if (couldNotRun.length > 0) return { breaks: [], clean: "", couldNotRun: reasons(couldNotRun) };
  return {
    breaks: [],
    clean:
      `${withHeader.length} staged entry file(s) compared over ${transitions} transition(s) in ` +
      `${snapshot.range}, each from the version before it (git log --format=%H -- <entry file>): claim at ` +
      `${comparedAt.join(", ") || "no transition"}, source and depends_on unchanged, and every covers change has a ` +
      "changed: line of its own",
    couldNotRun: null,
  };
}

/**
 * The text an entry had before the range started (null when it was not there at all), and every version inside it —
 * the last of which is the staged state, the view the whole run reports on.
 */
function versionsOf(
  snapshot: SnapshotInfo,
  one: StagedEntry,
  errors: GitErrors,
): { baseline: string | null; versions: Version[] } {
  const commits = commitsOf(snapshot.root, snapshot.range, one.path, errors);
  const first = commits[0];
  const baseline =
    first !== undefined && hasParent(snapshot.root, first, errors) ? textAt(snapshot.root, `${first}^`, one.path, errors) : null;
  const versions: Version[] = [];
  for (const commit of commits) {
    const text = textAt(snapshot.root, commit, one.path, errors);
    if (text !== null) versions.push({ where: `commit ${short(commit)}`, text, entry: parseEntry(one.name, text) });
  }
  versions.push({ where: "the staged state", text: one.text, entry: parseEntry(one.name, one.text) });
  return { baseline, versions };
}

/** The breaks one transition — one version to the next — makes: K4.3's three immutable things, each with its line. */
function transitionBreaks(path: string, before: Entry, after: Version): string[] {
  const breaks: string[] = [];
  const where = after.where;
  if (after.entry.claim !== before.claim) {
    breaks.push(
      `${path}:${after.entry.claimLine} — the claim changed in ${where}: ` +
        `"${truncate(before.claim)}" → "${truncate(after.entry.claim)}"`,
    );
  }
  for (const key of ["source", "depends_on"] as const) {
    const was = before.fields.get(key)?.full ?? "";
    const now = after.entry.fields.get(key)?.full ?? "";
    if (was !== now) {
      const line = after.entry.fields.get(key)?.line ?? before.fields.get(key)?.line ?? 1;
      breaks.push(`${path}:${line} — ${key} changed in ${where}: "${truncate(was)}" → "${truncate(now)}"`);
    }
  }
  const coversBefore = before.fields.get("covers")?.full ?? "";
  const coversAfter = after.entry.fields.get("covers")?.full ?? "";
  if (coversBefore === coversAfter) return breaks;
  // One covers change, one changed: line: the line this very transition added, not one an earlier commit added.
  const added = (after.entry.fields.get("changed")?.items ?? []).filter(
    (item) => item.trim() !== "" && !(before.fields.get("changed")?.items ?? []).includes(item),
  );
  if (added.length === 0) {
    const line = after.entry.fields.get("covers")?.line ?? before.fields.get("covers")?.line ?? 1;
    breaks.push(`${path}:${line} — covers changed in ${where} with no changed: line naming it`);
  }
  return breaks;
}

/** The header fields and the log line a merge must keep from both sides (W6.3a). */
const KEPT_ON_BOTH_SIDES = ["covers", "supersedes", "superseded_by", "depends_on", "changed"] as const;

/** The items of one header field, with the empty list forms read as no items. */
function itemsOf(entry: Entry, key: string): readonly string[] {
  const items = (entry.fields.get(key)?.items ?? []).map((one) => one.replace(/^-\s*/, "").trim());
  return items.filter((one) => one !== "" && one !== "[]" && one !== "none");
}

/**
 * W6.3a's git half: a merge keeps both sides. For every merge in the range and every parent, each `covers` path,
 * link and `changed:` line the parent holds must be in the merge result. A file the merge does not hold is left to
 * K4.1's deletion clause, so one break is reported once.
 */
export function checkMerges(snapshot: SnapshotInfo): ClauseOutcome {
  const root = snapshot.root;
  if (snapshot.shallow) return { breaks: [], clean: "", couldNotRun: SHALLOW };
  const errors: GitErrors = [];
  const merges = mergeCommits(root, snapshot.range, errors);
  const breaks: string[] = [];
  const comparedAt: string[] = [];
  let compared = 0;
  for (const merge of merges) {
    const merged = new Set(entryFilesAt(root, merge.commit, errors));
    for (const parent of merge.parents) {
      const paths = entryFilesAt(root, parent, errors).filter((path) => merged.has(path));
      const mergedShas = paths.map((path) => blobIdAt(root, merge.commit, path, errors));
      const parentShas = paths.map((path) => blobIdAt(root, parent, path, errors));
      const blobs = catFileBatch(root, [...mergedShas, ...parentShas], errors);
      for (const [offset, path] of paths.entries()) {
        const after = blobs.get(mergedShas[offset] ?? "");
        const before = blobs.get(parentShas[offset] ?? "");
        if (after === undefined || before === undefined || after === before) continue;
        compared += 1;
        const result = parseEntry(path, after);
        const side = parseEntry(path, before);
        const line = result.fields.get("changed")?.line ?? 1;
        comparedAt.push(`${path}:${line}`);
        for (const key of KEPT_ON_BOTH_SIDES) {
          const kept = itemsOf(result, key);
          for (const item of itemsOf(side, key)) {
            if (kept.includes(item)) continue;
            breaks.push(
              `${path}:${result.fields.get(key)?.line ?? line} — merge ${short(merge.commit)} holds no ${key} ` +
                `"${truncate(item)}" that parent ${short(parent)} holds (git show ${merge.commit}:${path})`,
            );
          }
        }
      }
    }
  }
  const couldNotRun = snapshotErrors(snapshot, errors);
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  if (couldNotRun.length > 0) return { breaks: [], clean: "", couldNotRun: reasons(couldNotRun) };
  return {
    breaks: [],
    clean:
      `${merges.length} merge commit(s) in ${snapshot.range} (git log --format=%H %P), ${compared} parent(s) of an ` +
      `entry file compared with the merge result${compared === 0 ? "" : ` (${comparedAt.join(", ")})`}: every ` +
      "covers path, link and changed: line either side holds is in the merge result",
    couldNotRun: null,
  };
}

/** The git half of W1.1a and W1.1b: an entry file renamed to another prefix, or to another id. */
export function checkRenames(
  snapshot: SnapshotInfo,
): { prefixes: ClauseOutcome; ids: ClauseOutcome } {
  if (snapshot.shallow) {
    const couldNotRun = SHALLOW;
    return {
      prefixes: { breaks: [], clean: "", couldNotRun },
      ids: { breaks: [], clean: "", couldNotRun },
    };
  }
  const errors: GitErrors = [];
  const renames = entryRenames(snapshot.root, snapshot.range, errors);
  const prefixBreaks: string[] = [];
  const idBreaks: string[] = [];
  const skipped: string[] = [];
  for (const rename of renames) {
    const from = nameParts(rename.from.slice(rename.from.lastIndexOf("/") + 1));
    const to = nameParts(rename.to.slice(rename.to.lastIndexOf("/") + 1));
    const commit = `${whereOf(rename.commit)} renamed ${rename.from} → ${rename.to}`;
    if (from.prefix !== to.prefix) {
      prefixBreaks.push(`${commit} — the prefix changed from ${from.prefix} to ${to.prefix}; an entry's kind never changes`);
    }
    if (from.id === null || to.id === null) {
      skipped.push(`${commit} — the name is not <prefix>-<id>-<slug>.md, so no id was compared (W1.1c is a reviewer's)`);
      continue;
    }
    if (from.id !== to.id) {
      idBreaks.push(`${commit} — the id changed from ${from.id} to ${to.id}; an id never changes`);
    }
  }
  const how =
    `git log -M --name-status and git diff --cached -M --name-status -- project-memory/entries ` +
    `(${snapshot.range}): ${renames.length} rename(s)`;
  const couldNotRun = snapshotErrors(snapshot, errors);
  if (couldNotRun.length > 0) {
    const why = reasons(couldNotRun);
    return {
      prefixes: { breaks: [], clean: "", couldNotRun: why, notes: skipped },
      ids: { breaks: [], clean: "", couldNotRun: why, notes: skipped },
    };
  }
  const prefixes: ClauseOutcome =
    prefixBreaks.length > 0
      ? { breaks: prefixBreaks, clean: "", couldNotRun: null, notes: skipped }
      : { breaks: [], clean: how, couldNotRun: null, notes: skipped };
  const ids: ClauseOutcome =
    idBreaks.length > 0
      ? { breaks: idBreaks, clean: "", couldNotRun: null, notes: skipped }
      : { breaks: [], clean: `${how}; no id changed in a rename`, couldNotRun: null, notes: skipped };
  return { prefixes, ids };
}
