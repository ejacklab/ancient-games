# Requirements evaluator — data between the steps

> **Status: interface detail written by the COO on 2026-10-13, under the accepted `REQUIREMENTS.md` and the E1–E10
> table in `runs/20261013-requirements-evaluator/workflow-design.md`.** It adds no requirement. It fixes the file
> shapes so that the scripts, the model briefs and the workflow agree. A change here is a Log line in that run's
> `state.md`.

All files are UTF-8 JSON written into the evaluation's run folder, `runs/<runId>/`. Paths inside them are relative to
that folder.

## Ids

| Id | Example | What it names |
|---|---|---|
| requirement id | `B1.1`, `EV-R1.2`, `W1.3` | an id in REQUIREMENTS, written `- **<id>**` at the start of a bullet |
| group id | `B1`, `EV-R1` | a heading line `**<group> — <title>**` that holds those ids |
| case id | `B1-F2`, `V3-F1` | one failure case: `<group>-F<n>`, numbered from 1 in the order the cases appear |
| vision id | `V1`, `V2` | a vision line, numbered from 1 in file order (EV-R1.2) |

An id matches `[A-Z][A-Za-z]*(-[A-Z][A-Za-z]*)?\d+(\.\d+)?`.

## E1 — `requirements.json`, written by `tools/evaluator/spec_parse.py`

```json
{
  "spec": {"requirements": "<path>", "vision": "<path>"},
  "groups": [
    {"group": "B1", "title": "What it reads",
     "ids": ["B1.1", "B1.2", "B1.3"],
     "status": "in_scope",
     "fails_if": "an untracked entry gets a line, a file outside B1.1 gets a line, or a path with ...",
     "cases": [{"case": "B1-F1", "text": "an untracked entry gets a line"},
               {"case": "B1-F2", "text": "a file outside B1.1 gets a line"},
               {"case": "B1-F3", "text": "a path with a space or a non-ASCII character is read wrongly in either mode"}],
     "open_ids": []}
  ],
  "vision": [{"id": "V1", "section": "never", "text": "Never cut, drop, ...",
              "cases": [{"case": "V1-F1", "text": "Never cut, drop, ..."}]}],
  "manifest": ["B1.1", "B1.2", "B1.3", "...", "V1", "..."]
}
```

**Parsing rules.** These are the known answer the tests hold the parser to.

1. **Group heading.** A line that starts with `**<group> — ` (the dash is U+2014). The title runs to the closing
   `**`.
2. **Ids.** A bullet `- **<id>**`, or `- **<id> <title>**` with the id first inside the bold (CACHES writes
   `- **B1.3 The question set** …`), optionally indented, belongs to the latest group heading.
3. **Fails if.** A bullet whose text starts with `**Fails if**` or `**Fails if:**`, at any indent, belongs to the
   latest group. If a group has several, each is split, and the cases are numbered across them in order.
   - The text after the marker is the `fails_if` string (several joined with ` / `).
   - A Fails if line can wrap onto continuation lines: lines indented more than the bullet, up to the next bullet,
     heading or blank line.
4. **Splitting a Fails if into cases.**
   - If the text has `; ` outside backticks and brackets, split on `; ` only.
   - Otherwise split on `, ` outside backticks and brackets.
   - In each part, strip a leading `or ` or `and `, a final `.`, and outer spaces. Drop empty parts.
5. **Open.** An id whose own bullet text, including its continuation lines (as in rule 3), has the whole word `open`
   immediately before `.`, `;`, `,`, `)` or the end of the text goes to `open_ids` and gets no verdict. Examples:
   G4.1 *"…is open."* and K4.3 *"The design leaves this open."* are open; *"is opened read-only"* and *"can open
   the source"* are not. A group whose ids are all open has `status: "open"`. *(Corrected 2026-10-13: the first
   wording matched the substring `is open`, which caught "is opened", and the marker `*open*` caught EV-R1.1's own
   sentence.)*
6. **Untestable.** A group with ids and no Fails if has `status: "untestable"` and no cases (EV-R1.3).
7. **Vision** (EV-R1.2). Only the bullets under a line that starts with `**What it will never do` (`section:
   "never"`) or `**How we know it works` (`section: "how_we_know"`), up to the next line that starts with `**` or `#`.
   Each bullet is one vision id with one case, `V<n>-F1`, whose text is the bullet.
8. **Manifest.** Every requirement id (open ones included) and every vision id, in file order. This is the coverage
   manifest of EV-P2.1.

## E3 — `classify.json`, written by the classify step (a model)

```json
{"cases": [{"case": "B1-F1", "kind": "executable", "reason": "run write mode with an untracked entry"}]}
```

- `kind` is one of `executable`, `static`, `judged` or `human`.
- An empty or missing `reason` makes the case `human` (EV-C1.2). `verdict.py` enforces this, not the model.

## E4 — probes, written by the probe step (a model)

- Probes are `probes/test_*.py`, pytest files in the run folder.
- Each test function's docstring **starts with** the case id(s) it checks: `"""B1-F1 — …"""`.
- The product's path is given to the probes as the environment variable `EVAL_PRODUCT`.

## E5 — `mutants.json`, written by the mutant step (a model)

```json
[{"case": "B1-F1", "file": "tools/memory_index.py", "old": "<exact text, once in the file>", "new": "<replacement>"}]
```

- At most one mutant per case. A case with no mutant cannot be PASS (EV-C3.2).
- **`plants.json`**, written by the same step in the same shape, holds one mutant for each **judged** case. They are
  never run by `probe_matrix.py`; the judge step takes its plant from them (E9).

## E6 and E7 — `matrix.json`, written by `tools/evaluator/probe_matrix.py`

```json
{"product_dir": "workspace/product", "probes_dir": "probes",
 "citations": {"test_b1::test_untracked": ["B1-F1"]},
 "product": {"test_b1::test_untracked": "pass"},
 "mutants": {"B1-F1": {"status": "applied", "results": {"test_b1::test_untracked": "fail"}}},
 "restored": true}
```

- **The product copy.** The probes run against a **copy** of the product in the run folder (`product_dir`), never the
  original (EV-R3.2). Each mutant is applied to that copy and then undone.
- **Running the probes.** They run as
  `python3 -m pytest -q -p no:cacheprovider -c /dev/null --rootdir <probes_dir> --junitxml <file> <probes_dir>`,
  with `EVAL_PRODUCT=<product_dir>` in the environment. That way the repo's own pytest config never applies.
- **Probe keys.** A probe key is `<junit classname>::<junit name>`, for example `test_b1::test_untracked[2]`. An
  outcome is `pass`, `fail` or `skip`; an error counts as `fail`.
- **Citations.** `citations` maps each probe key to the case ids its function's docstring starts with. The script
  finds them by parsing `<probes_dir>/test_*.py`, where the functions are module level. A parametrised test's keys
  all carry their function's citations.
- **Invalid mutants.** A mutant whose `old` text is not found exactly once in its file has `status: "invalid"` and no
  results.
- **Restoring.** `restored` is true only when every file of the product copy has the same sha256 as before the
  mutants (EV-C3.3).

## E8 — `confirm.json`, written by the confirm step (a model)

```json
{"cases": [{"case": "B3-F2", "probe": "probes/test_b3.py::test_superseded", "faithful": true,
            "requirement_quote": "…", "probe_quote": "…"}]}
```

## E9 — `judged.json`, written by the workflow from the judge step's two calls

```json
{"plant_case": "G2-F1", "plant_found": true,
 "cases": [{"case": "G2-F1", "holds": true, "evidence": "tools/x.py:12 \"…\""}]}
```

How the two calls are combined:
1. **First call.** The workflow picks one judged case that has a plant (the first in case order) as `plant_case`.
   It applies that plant to a copy of the product. A fresh judge judges every judged case on that copy.
   `plant_found` is true when the judge says `plant_case` does **not** hold.
2. **Second call.** A second fresh call judges `plant_case` alone on the clean copy. Its answer is `plant_case`'s
   entry in `cases`. The first call's answers stand for every other judged case.
3. **No plant available.** With no judged case, `judged.json` is `{"plant_found": true, "cases": []}`. With judged
   cases but no plant for any of them, `plant_found` is false, so the judged cases are UNKNOWN.

## E10 — `verdict.json` and `verdict.md`, written by `tools/evaluator/verdict.py`

**Per case**, in this order. The first rule that applies wins.

1. The kind is `human` → **UNKNOWN**, "needs EJ".
2. The kind is `judged`:
   - `plant_found` is false → **UNKNOWN**, "judging void: plant missed";
   - `holds` is true → **PASS**; `holds` is false → **FAIL** (its repro is the quoted evidence);
   - no entry → **UNKNOWN**, "not judged".
3. The kind is `executable` or `static`:
   - no probe key cites the case (`citations`) → **UNKNOWN**, "no probe";
   - any of its probes fails on the product:
     - confirmed `faithful: true` → **FAIL**, with repro
       `EVAL_PRODUCT=<product_dir> python3 -m pytest -c /dev/null <probes_dir>/<module>.py -k <test name>`;
     - otherwise → **UNKNOWN**, "probe not confirmed faithful";
   - all of its probes pass on the product:
     - the case's mutant is missing or `invalid` → **UNKNOWN**, "no mutant";
     - at least one of its probes fails on that mutant → **PASS**;
     - otherwise → **UNKNOWN**, "unproven: no probe fails on its mutant".
4. `matrix.json` has `restored: false` → every case is **UNKNOWN**, "product not restored".

**Per group:**
- **FAIL** if any case is FAIL;
- **PASS** if it has cases and all are PASS;
- otherwise **UNKNOWN** (an `untestable` group: "untestable: no Fails if").

Each requirement id takes its group's verdict. An open id gets none, and is listed as out of scope. Each vision id
takes its single case's verdict.

**MEETS** is true only when every in-scope requirement id and every vision id is PASS (EV-P1.2).

**`verdict.json`:**
`{"meets": bool, "counts": {"PASS": n, "FAIL": n, "UNKNOWN": n, "out_of_scope": n},
"cases": [{"case", "kind", "verdict", "reason", "repro"}], "requirements": [{"id", "group", "verdict", "reason"}],
"out_of_scope": [ids], "manifest": [ids]}`.
- `reason` is an empty string for a PASS.
- `repro` is an empty string unless the case is FAIL.
- A missing input file (`classify.json`, `matrix.json`, `confirm.json` or `judged.json`) counts as an empty one, so
  every case it would have backed becomes UNKNOWN. A missing or unreadable `requirements.json` exits 2.

**`verdict.md`** (EV-P2.2) is laid out in this order:
1. the line `MEETS: yes|no`;
2. the counts;
3. the FAIL rows (each with its repro);
4. the UNKNOWN rows (each with its reason);
5. the PASS rows;
6. the out-of-scope ids;
7. the manifest.

## The workflow: `.claude/workflows/evaluate-requirements.js` (D4)

A Workflow script cannot touch files, so **every script step runs through a runner agent**. A runner executes one
command from the repo root and reports back. It never interprets the output. Labels are fixed, because the offline
harness stubs agents by label.

**Arguments** (EV-R3.1): `{product, spec, runId}`, all strings. Any missing → return
`{status: "blocked", reason: "missing argument <name>"}` before any agent runs.

**The runner** (model `haiku`, effort `low`). Its prompt is `Run exactly this command from the repository root,
with a Bash timeout of 600000 ms (some steps take minutes), then report: <cmd>`. *(The timeout was added on
2026-10-13, before the first live run: Bash's default of 2 minutes would kill the Codex mutant step.)* Its schema is
`{exit_code: integer, stdout_tail: string, stderr_tail: string}`, where each tail is the last 40 lines.

| # | label | kind | command or brief | stop if |
|---|---|---|---|---|
| 1 | `e1-spec` | runner | `python3 tools/evaluator/spec_parse.py --requirements <spec>/REQUIREMENTS.md --vision <spec>/VISION.md --out runs/<runId>/requirements.json` | exit ≠ 0 |
| 2 | `e2-workspace` | runner | `python3 tools/evaluator/workspace.py --product <product> --spec <spec> --run runs/<runId>` | exit ≠ 0 |
| 3 | `e3-classify` | model `haiku` | `docs/evaluator/briefs/classify.md` | null result |
| 4 | `e4-probes` | model `sonnet` | `docs/evaluator/briefs/probes.md` | null result |
| 5 | `e5-mutants` | runner (wraps Codex) | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --sandbox workspace-write -C . "Read docs/evaluator/briefs/mutants.md with RUN=runs/<runId> and do what it says." < /dev/null` | exit ≠ 0 |
| 6 | `e6-matrix` | runner | `python3 tools/evaluator/probe_matrix.py --run runs/<runId>` | exit ≠ 0 |
| 7 | `e8-input` | runner | `python3 tools/evaluator/model_io.py confirm-input --run runs/<runId>` | exit ≠ 0 |
| 8 | `e8-confirm` | model `sonnet` | `docs/evaluator/briefs/confirm.md`, **skipped** when the runner's stdout says `0 to confirm` | null result |
| 9 | `e8-check` | runner | `python3 tools/evaluator/model_io.py confirm-check --run runs/<runId>` | exit ≠ 0 |
| 10 | `e9-input` | runner | `python3 tools/evaluator/model_io.py judge-input --run runs/<runId>`: writes `judge-input.json` and applies the plant to `judge-copy/` | exit ≠ 0 |
| 11 | `e9-judge-1` | model `sonnet` | `docs/evaluator/briefs/judge.md` with `CALL=1`, `PRODUCT_COPY=runs/<runId>/judge-copy`; **skipped** when stdout says `0 to judge` | null result |
| 12 | `e9-judge-2` | model `sonnet` | the same brief with `CALL=2`, `PRODUCT_COPY=runs/<runId>/workspace/product`, the plant case only | null result |
| 13 | `e9-merge` | runner | `python3 tools/evaluator/model_io.py judged-merge --run runs/<runId>`: writes `judged.json`, checks quotes | exit ≠ 0 |
| 14 | `e10-verdict` | runner | `python3 tools/evaluator/verdict.py --run runs/<runId>` | exit ≠ 0 |

**Model steps.** A model step's prompt is `Read <brief> and do what it says. RUN=runs/<runId>` (plus `CALL` and
`PRODUCT_COPY` for the judge). Its schema is `{done: boolean, note: string}`. The files it writes are the real output.

**When a step fails** (EV-C6.2): a model step that returns null, or a runner with a non-zero exit, stops the run.
The workflow returns
`{status: "blocked", step: <label>, reason: <stderr_tail or "no result">}` and runs no later step. There is no
fallback.

**The end.** The workflow returns `{status: "done", runId, meets, verdict: "runs/<runId>/verdict.md", agents:
<count of agent() calls>}`. `meets` is parsed from `e10-verdict`'s stdout line `MEETS: yes|no`, which `verdict.py`
prints. **The workflow never computes or changes a verdict** (EV-P1.3). If that stdout has no `MEETS:` line, the run is
`{status: "blocked", step: "e10-verdict", reason: "no MEETS line"}`. It never guesses.

## `tools/evaluator/model_io.py` — the files around the model steps (D4)

| subcommand | reads | writes | stdout |
|---|---|---|---|
| `confirm-input` | `requirements.json`, `matrix.json`, `probes/`, `workspace/spec/REQUIREMENTS.md` | `confirm-input.json`: one entry per probe that is `fail` on the product, with `case`, `case_text`, `group_text` (the group's block from the heading to the next heading, verbatim), `probe` key, `probe_source` (its function's source), `output` (from `matrix.json`, capped at 40 lines) | `<n> to confirm` |
| `confirm-check` | `confirm.json`, `confirm-input.json` | `confirm.json`, rewritten: an entry whose `requirement_quote` is not in its `group_text`, or whose `probe_quote` is not in its `probe_source`, gets `faithful: false` and `note: "quote not found"` | `<n> checked, <m> voided` |
| `judge-input` | `requirements.json`, `classify.json`, `plants.json`, `workspace/` | `judge-input.json` (judged cases with `case_text` and `group_text`, `plant_case`); `judge-copy/` = a copy of `workspace/product/` with the plant applied (`plant_case` = the first judged case in case order that has a valid plant, or null) | `<n> to judge` |
| `judged-merge` | `judge-1.json`, `judge-2.json`, `judge-input.json`, `workspace/product/` | `judged.json` per DATA.md E9. A `cases` entry whose quoted code is not in that file of `workspace/product/` (for call 2) or `judge-copy/` (for call 1) is dropped (that case becomes "not judged"). | `plant_found: <bool>` |

The quotes are checked by plain substring after collapsing whitespace runs. A missing input file counts as empty,
except `requirements.json`, which exits 2.

`verdict.py` prints `MEETS: yes` or `MEETS: no` as its first stdout line. *(Added for the workflow. D2's tests do not
check it; D4's harness does.)*
