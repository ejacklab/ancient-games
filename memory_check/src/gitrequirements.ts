// The clauses the tool judges itself, from the staged snapshot or from git history: the entry-name prefix W1.1a
// does not reach, one file per entry (W6.1a), an entry file is never deleted and says what replaced it (K4.1),
// an entry's claim, `source`, `depends_on` and `covers` never change silently (K4.3), and the git half of W1.1a
// and W1.1b (an entry file renamed to another prefix or another id). Every break carries its file and line, or the
// command and its output (C2).
import { nameParts, parseEntry, type Entry } from "./entry.ts";
import { catFileBatch, entryDeletions, entryRenames, firstVersionOf, type SnapshotInfo, type StagedEntry } from "./gitchecks.ts";

export interface ClauseOutcome {
  /** One evidence line per break found. Empty when nothing broke. */
  readonly breaks: readonly string[];
  /** The evidence that says what was checked, when nothing broke. */
  readonly clean: string;
  /** Set when the check could not run: the reason. */
  readonly couldNotRun: string | null;
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
  if (snapshot.shallow) {
    for (const { staged: one, entry } of parsed(staged)) {
      checkHeader(one.path, entry, breaks);
    }
    return {
      breaks,
      clean: "",
      couldNotRun: breaks.length === 0 ? `${SHALLOW}; the superseded_by and retired checks on the snapshot still ran` : null,
    };
  }
  for (const { staged: one, entry } of parsed(staged)) checkHeader(one.path, entry, breaks);
  const deletions = entryDeletions(snapshot.root, snapshot.range);
  for (const deletion of deletions) {
    breaks.push(
      `commit ${short(deletion.commit)} deleted ${deletion.path} — an entry file is never deleted ` +
        "(git log --diff-filter=D --name-status -- project-memory/entries)",
    );
  }
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  return {
    breaks: [],
    clean:
      `${staged.length} staged entry file(s): no status: superseded without superseded_by, no status: retired ` +
      `without a reason in its changed: line; git log --diff-filter=D --name-status -- project-memory/entries ` +
      `(${snapshot.range}) deleted none`,
    couldNotRun: null,
  };
}

function checkHeader(path: string, entry: Entry, breaks: string[]): void {
  const status = entry.fields.get("status");
  const statusValue = status?.full ?? "";
  if (statusValue === "superseded" && (entry.fields.get("superseded_by")?.full ?? "") === "") {
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

/** K4.3: after its first commit an entry only gains lines; its claim, `source` and `depends_on` never change. */
export function checkK43(staged: readonly StagedEntry[], snapshot: SnapshotInfo): ClauseOutcome {
  const withHeader = parsed(staged);
  if (snapshot.shallow) {
    return { breaks: [], clean: "", couldNotRun: SHALLOW };
  }
  const firstVersions = new Map<string, { sha: string; commit: string }>();
  const shas: string[] = [];
  for (const { staged: one } of withHeader) {
    const first = firstVersionOf(snapshot.root, snapshot.range, one.path);
    if (!first) continue;
    firstVersions.set(one.path, first);
    shas.push(first.sha);
  }
  const blobs = catFileBatch(snapshot.root, shas);
  const breaks: string[] = [];
  let compared = 0;
  for (const { staged: one, entry } of withHeader) {
    const first = firstVersions.get(one.path);
    const text = first ? blobs.get(first.sha) : undefined;
    if (!first || text === undefined) continue;
    compared += 1;
    const was = parseEntry(one.name, text);
    if (entry.claim !== was.claim) {
      breaks.push(
        `${one.path}:${entry.claimLine} — the claim changed after commit ${short(first.commit)}: ` +
          `"${truncate(was.claim)}" → "${truncate(entry.claim)}"`,
      );
    }
    for (const key of ["source", "depends_on"] as const) {
      const before = was.fields.get(key)?.full ?? "";
      const after = entry.fields.get(key)?.full ?? "";
      if (before !== after) {
        const line = entry.fields.get(key)?.line ?? was.fields.get(key)?.line ?? 1;
        breaks.push(`${one.path}:${line} — ${key} changed after commit ${short(first.commit)}: "${truncate(before)}" → "${truncate(after)}"`);
      }
    }
    const coversBefore = was.fields.get("covers")?.full ?? "";
    const coversAfter = entry.fields.get("covers")?.full ?? "";
    const changedBefore = (was.fields.get("changed")?.items ?? []).length;
    const changedAfter = (entry.fields.get("changed")?.items ?? []).length;
    if (coversBefore !== coversAfter && changedAfter <= changedBefore) {
      const line = entry.fields.get("covers")?.line ?? was.fields.get("covers")?.line ?? 1;
      breaks.push(`${one.path}:${line} — covers changed after commit ${short(first.commit)} with no changed: line added`);
    }
  }
  if (breaks.length > 0) return { breaks, clean: "", couldNotRun: null };
  return {
    breaks: [],
    clean:
      `${compared} entry file(s) compared with their first version in ${snapshot.range}: claim, source, depends_on ` +
      "unchanged, and every covers change has a changed: line",
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
  const renames = entryRenames(snapshot.root, snapshot.range);
  const prefixBreaks: string[] = [];
  const idBreaks: string[] = [];
  const skipped: string[] = [];
  for (const rename of renames) {
    const from = nameParts(rename.from.slice(rename.from.lastIndexOf("/") + 1));
    const to = nameParts(rename.to.slice(rename.to.lastIndexOf("/") + 1));
    const commit = `commit ${short(rename.commit)} renamed ${rename.from} → ${rename.to}`;
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
  const how = `git log -M --name-status -- project-memory/entries (${snapshot.range}): ${renames.length} rename(s)`;
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