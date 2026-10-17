thought
Wait, in `withReviewer(base, context.k41)`:
`breaks` has no breaks, so it returns `"needs a reviewer"` instead of `"fail"`!
And what did K4.1 require?
"fails_if: git shows an entry file deleted, a `superseded` entry with no `superseded_by` link, or a `retired` entry with no reason in its `changed:` line."
Level: MUST!
A superseded entry with an empty bullet (`superseded_by:\n  -`) has NO link!
It MUST FAIL!
Instead, it gets `"needs a reviewer"`, exiting 0 instead of exiting 1!
Breaking: `SoT:K4.1` (fails_if: a superseded entry with no superseded_by link), `U2` (a MUST that fails is shown as passing), `R3` (a failing MUST exits 0).
Severity: P1 (wrong answer: exits 0 and gives "needs a reviewer" instead of "fail").
File:line: `memory_check/src/gitrequirements.ts:147`
Input: A staged entry with `status: superseded` and `superseded_by:\n  -` (an empty list item). `memory-check` reports `needs a reviewer` and exits 0 instead of failing `SoT:K4.1` and exiting 1.
Fix in one line: Treat `"-"` (or items trimming to empty) as empty in `linksNothing` or inspect `itemsOf(entry, "superseded_by").length === 0`.

WAIT! Look at `itemsOf` in `gitrequirements.ts`:
Line 271:
```ts
function itemsOf(entry: Entry, key: string): readonly string[] {
  const items = (entry.fields.get(key)?.items ?? []).map((one) => one.replace(/^-\s*/, "").trim());
  return items.filter((one) => one !== "" && one !== "[]" && one !== "none");
}
```
`itemsOf` ALREADY filters out empty items:
`items.filter((one) => one !== "" && one !== "[]" && one !== "none")`!
For `superseded_by:\n  -`:
`one.replace(/^-\s*/, "").trim()` is `""`!
So `itemsOf(entry, "superseded_by")` is `[]`!
If `checkHeader` had used `itemsOf(entry, "superseded_by").length === 0`, it would have caught it!
Instead, `checkHeader` used `linksNothing(entry.fields.get("superseded_by")?.full)`, which gets `"-"` and returns `false`!
That is a crystal clear bug!

WAIT! Look at `checkHeader` for RETIRED entries too:
Line 157-163:
```ts
  if (statusValue === "retired") {
    const changed = entry.fields.get("changed");
    const items = (changed?.items ?? []).filter((item) => item.trim() !== "");
    if (items.length === 0) {
      breaks.push(`${path}:${status?.line ?? 1} — status: retired with no changed: line naming the reason`);
    }
  }
```
Wait! What if an entry is retired with:
```yaml
---
id: 17-10-abc123-2026
kind: decision
status: retired
changed:
  - 2026-10-17T00:00:00Z author created
---
```
Wait, earlier we asked: what is the mechanical check for retired entries?
Notice finding 8 in Codex's review:
"8. [P1] K4.1 passes a mixed git/reviewer requirement... A retired entry retaining only its original 'created' log item also passes as having a retirement reason. Fix: retain mechanical failures, but otherwise return 'needs a reviewer.'"
Because judging whether the text in `changed:` is a valid retirement reason is a human reviewer's judgment (the tool cannot judge the English reason), returning "needs a reviewer" when `items.length > 0` was the agreed design.

WAIT! Look at `tools/memory_index.py` again!
Let's check `tools/memory_index.py` for other defects.
Let's check `parse_header` in `tools/memory_index.py`:
Lines 117-124:
```python
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line[0].isspace():
            continue
        key, separator, value = line.partition(":")
        name = key.strip()
        if separator and name in ("id", "kind", "status"):
            fields[name] = unquote(value)
    return fields, end, None
```
WAIT!
What if a line inside the header has NO colon `:`?
For example:
```yaml
---
id: 14-10-a1b2c3-2026
kind: decision
status: active
invalid header line without colon
---
```
`key, separator, value = line.partition(":")`
`separator` is `""`.
`name` is `"invalid header line without colon"`.
`separator and ...` is `False`.
`parse_header` completely ignores the malformed header line!
Wait, is there a requirement for that?
W1.2b: "Each field is one key: value line... fails_if: a field is missing or laid out otherwise... check: reviewer".
W1.2b is a reviewer check. So tool ignoring it is consistent.

WAIT! Look at `read_claim` in `tools/memory_index.py`:
Lines 135-145:
```python
def read_claim(body: list[str]) -> tuple[str, bool]:
    """Return the claim (the body up to `**Why:**`, blank lines dropped, whitespace runs collapsed) and whether
    a `**Why:**` line was found."""
    parts: list[str] = []
    has_why = False
    for line in body:
        if line.startswith(WHY):
            has_why = True
            break
        parts.append(" ".join(line.split()))
    return " ".join(part for part in parts if part), has_why
```
WAIT! Look at line 140:
`if line.startswith(WHY):`
What if the body has a code block or markdown quote that starts with `**Why:**`?
Wait, `WHY = "**Why:**"`.
What if `**Why:**` is followed by text on the same line, e.g. `**Why:** Because reasons`?
`line.startswith(WHY)` is True.
What if `**Why:**` is on its own line: `**Why:**`?
`line.startswith(WHY)` is True.
What if `**Why:**` is NOT at the start of the line, e.g. `# Heading\n**Why:** reason`? It matches.

WAIT! Look at `check_content` in `tools/memory_index.py`:
Lines 148-171:
```python
def check_content(entry: Entry) -> None:
    if not entry.tracked:
        entry.errors.append("not known to git, git add it first")
    problems: list[str] = []
    if entry.kind not in KINDS:
        problems.append(f"kind {entry.kind!r} is not one of {' / '.join(KINDS)}")
    elif PREFIX_KIND.get(entry.name[:1]) != entry.kind:
        problems.append(f"kind {entry.kind!r} does not match the {entry.name[:1]}- file prefix")
    if not entry.has_why:
        problems.append(f"no {WHY} line")
    if not entry.claim:
        problems.append("empty claim")
    if entry.is_active:
        entry.errors.extend(problems)
    else:
        entry.warnings.extend(problems)
```
WAIT!
What if an entry is `status: active`, and:
`kind` is empty:
`entry.kind not in KINDS` (since `"" not in KINDS`):
`problems.append("kind '' is not one of decision / fact / lesson / observation / hypothesis")`.
In `memory_check/src/indextool.ts:51`:
`if (/^kind .* is not one of/.test(problem)) return "W1.1a";`
That matches.

WAIT! What if `entry.name` has a prefix that is NOT in `PREFIX_KIND`?
Say `X-something.md`.
Wait! Earlier we saw:
If a file in `project-memory/entries/` is `X-something.md` or `R-something.md`:
In `memory_index.py`:
`ENTRY_NAME = re.compile(r"[DFLOH]-[^/]+\.md")`
`is_entry_path` returns `False`!
So `memory_index.py` NEVER ADDS IT TO `entries`!
In `snapshot_memory`:
`wanted = [path for path in sorted(paths) if is_entry_path(path)]`
`X-something.md` is NOT in `wanted`!
Now what happens in `working_tree_entries` (write mode)?
Lines 397-420:
```python
def working_tree_entries(repo: Path) -> list[Entry]:
    tracked, untracked = working_tree_paths(repo)
...
```
And what is `working_tree_paths`?
Lines 321-327:
```python
def working_tree_paths(repo: Path) -> tuple[list[str], list[str]]:
    tracked = set(split_nul(git(["ls-files", "-z", "--cached", "--", ENTRIES_DIR], cwd=repo)))
    others = set(
        split_nul(git(["ls-files", "-z", "--others", "--exclude-standard", "--", ENTRIES_DIR], cwd=repo))
    )
    return sorted(p for p in tracked if is_entry_path(p)), sorted(p for p in others - tracked if is_entry_path(p))
```
LOOK AT LINE 327:
`sorted(p for p in tracked if is_entry_path(p))`!
`sorted(p for p in others - tracked if is_entry_path(p))`!
IT FILTERS WITH `is_entry_path(p)`!
So ANY file in `project-memory/entries/` whose name does not start with `[DFLOH]-` is SILENTLY FILTERED OUT by `memory_index.py` in BOTH write mode and check mode!
It is NEVER parsed!
It NEVER produces an error in `memory_index.py`!
NOW:
What requirement does `memory_index.py` purport to check?
In `docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`:
"W1.1a (MUST)
Each entry is one file. The prefix is one letter per kind (W2): `D-` decision, `F-` fact, `L-
status: done

## Findings

1. **[P1] Unborn HEAD skips staging area check — [tools/memory_index.py:483](file:///home/smoke01/dev/ancient-games/tools/memory_index.py#L483).**
   - **Broken requirement / use case:** SoT:K6.1a, SoT:K6.2, U2 (*my reading*).
   - **Input that shows it:** An initial repository state where `HEAD` is unborn (e.g. a fresh `git init` before the first commit) with malformed entries or an unsynchronized `project-memory/INDEX.md` staged. Running `python3 tools/memory_index.py --check` outputs `"nothing to check: HEAD names no commit yet, so the staging area holds no snapshot"` and exits 0 instead of checking the staged snapshot and exiting 1.
   - **Fix:** Restrict `if head_is_unborn(repo):` so it only returns early when checking `rev` (or `rev == "HEAD"`), allowing staged checks (`rev is None`) to proceed to `snapshot_memory`.

2. **[P1] Early return on index mismatch suppresses Rd3.1a size check — [tools/memory_index.py:499](file:///home/smoke01/dev/ancient-games/tools/memory_index.py#L499).**
   - **Broken requirement / use case:** SoT:Rd3.1a, U2 (*my reading*).
   - **Input that shows it:** An active entry corpus whose generated index exceeds `MAX_LINES` (200) or `MAX_BYTES` (24,000) and whose staged `project-memory/INDEX.md` is simultaneously out of date (`current != rendered`). Running `python3 tools/memory_index.py --check` returns 1 immediately at line 502, never evaluating `over_limit(rendered)` at line 503, thereby failing to report that `INDEX.md` exceeds its limit.
   - **Fix:** Evaluate and record `over_limit(rendered)` before or alongside returning on `current != rendered`.

3. **[P1] SessionStart harness hook opening cache is evaluated as allowed on-demand read — [memory_check/src/cachechecks.ts:38](file:///home/smoke01/dev/ancient-games/memory_check/src/cachechecks.ts#L38).**
   - **Broken requirement / use case:** CACHES:Rd1, C6, U2 (*my reading*).
   - **Input that shows it:** A project with `.claude/settings.json` defining a `SessionStart` hook command opening the cache (e.g. `"hooks": { "SessionStart": [{ "matcher": ".*", "command": "cat project-memory/.cache/index.sqlite" }] }`). Because `checkRd1` evaluates each line in isolation against `SESSION_START` regex, the command line lacks startup keywords, setting `reading.atStart` to `false` and reporting `CACHES:Rd1` as `pass`.
   - **Fix:** Maintain `SessionStart` block context when parsing JSON/settings files rather than testing lines in isolation with `SESSION_START`.

4. **[P1] Empty bullet in superseded_by passes as valid link — [memory_check/src/gitrequirements.ts:147](file:///home/smoke01/dev/ancient-games/memory_check/src/gitrequirements.ts#L147).**
   - **Broken requirement / use case:** SoT:K4.1, U2, R3 (*my reading*).
   - **Input that shows it:** A staged entry with `status: superseded` and `superseded_by:\n  -` (an empty list bullet). In `parseEntry`, `entry.fields.get("superseded_by")?.full` is `"-"`, for which `linksNothing("-")` returns `false`, causing `checkHeader` to log no break and `runChecks` to return `needs a reviewer` (exit 0) instead of `fail` (exit 1).
   - **Fix:** Verify `itemsOf(entry, "superseded_by").length === 0` or include `"-"` in `linksNothing` empty forms.

5. **[P2] Entry names with whitespace or non-ASCII characters are truncated in warnings — [memory_check/src/warn.ts:12](file:///home/smoke01/dev/ancient-games/memory_check/src/warn.ts#L12).**
   - **Broken requirement / use case:** R2, U3 (*my reading*).
   - **Input that shows it:** An entry whose filename contains whitespace or non-ASCII characters (e.g. `project-memory/entries/D-17-10-abc123-2026-time check.md`) that triggers a failing MUST. `FILE_NAME` regex `[\w.\-]+` stops before the space, printing `files: project-memory/entries/D-17-10-abc123-2026-time` in `memory-check --warn`.
   - **Fix:** Update `FILE_NAME` regex to match valid entry paths containing spaces and UTF-8 characters up to `.md`.

## Checked and found nothing

- **F1 & F2 (Location and Project Root):** Git toplevel resolution, project path validation, and working-tree memory location enumeration adhere to `REQUIREMENTS.md` F1/F2.
- **F3 (Read-Only Guarantee):** All Git executions specify `GIT_OPTIONAL_LOCKS=0`, and the tool writes only to `--out` when explicitly instructed.
- **C1 & R1 (Coverage and Formatting):** Bundled YAML and Markdown guidelines are parsed with SHA-256 version hashes, mapping all requirement records and levels without omissions.
- **C4 & C6 (Absent Memory & Cache Invariants):** Projects lacking `project-memory/` or `project-memory/.cache/` consistently resolve affected records to `not applicable`.
- **C5 (Snapshot & Range Scoping):** First-commit discovery on `project-memory/` and `--since` revision bounds correctly delineate historical commit transitions.
- **K4.3 (Immutable Header Properties):** Historical step-by-step verification catches claim, `source`, and `depends_on` modifications, as well as `covers` adjustments without matching `changed:` entries.
- **W6.3a (Merge Preservation):** Merge commits are checked against each parent to ensure union retention of `covers`, links, and `changed:` audit lines.
