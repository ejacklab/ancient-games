status: done

1. **medium** — `.claude/skills/workflow-design/guard/src/insight-index.ts` patch line 1091 (`optionKinds: section.options.map(...)`) printed by patch line 1121 (`indexMarkdown`).
   **Wrong:** the index prints each option's bracket text verbatim. A section that mislabels an option leaks that text into the index, breaking the "the author's text is never printed" guarantee (SPEC Round 11, patch lines 898/906).
   **Input:** an insight section with `Options:\n1. [the root cause is SECRET-x] keep it — evidence: e\n2. [check] y — evidence: e` → `insight index` prints `SECRET-x` in the `options` column (probed).
   **Fix:** allow-list the kinds already defined in `insight.ts` (`OPTION_KINDS` = rule/check/tool/config-advice; `GREAT_OPTION_KINDS` = rule/check/tool) and print `-` for anything else, instead of `option.kind`.

2. **medium** — `insight-index.ts` patch line 1037 `const HEADING_RE = /^##\s+(.*)$/;`, used by `headings()` (patch lines 1101–1116) and `showSections` (patch line 1139).
   **Wrong:** it is stricter than the section rule in `insight.ts:17` (`/^##(?!#)\s*(.*)$/`), which `parseInsight` uses to build the index. For a heading written `##F-1a2b3c4d` (no space), `parseInsight` opens a section but `headings()` does not, so `heads[i]` shifts: the section's own `Category:` override and its title are attached to the wrong section, and `show --category` misses a section the index lists (SPEC I2 fails-if "misses one that does").
   **Input (probed):** `##F-1a2b3c4d — a spec brief\n\n<valid body>Category: spec\n\n## F-2b3c4d5e …` → first entry `category: "-"` (override dropped) and `insight show --category spec` prints nothing.
   **Fix:** share one heading predicate with `insight.ts` (or use `/^##(?!#)\s*(.*)$/`) in both `headings()` and `showSections`.

3. **medium** — `.claude/skills/six-experts/scripts/six_experts.py` patch line 810 (`sid = next(s for s in answers if ... and CJK_RUN.search(answers[s]))`).
   **Wrong:** `check --sabotage` crashes with an unhandled `StopIteration` whenever no answer contains a 4+ character Chinese run, instead of reporting the advertised "≥ 2 failures" (SKILL §2). This is the common case for an English/Claude-only run and is untested.
   **Input (probed):** a run folder with one English answer and no CJK → `six_experts.py check <dir> --sabotage` → `StopIteration` traceback.
   **Fix:** if no CJK run exists, fall back to another mutation (a bogus `#99` item cite, or a changed item number) or print "no quoted Chinese to alter" and exit non-zero. (Secondary crash path: `new RegExp(re)` in `categorize` is unguarded, so a malformed `titles` regex in `insight-categories.yaml` takes down `insight index`; `loadCategories` catches only parse errors.)

4. **medium** — `six_experts.py` patch lines 673–683 (`hand_to_caller`), model set at patch line 674.
   **Wrong:** under `--claude-by-caller` — the mode SKILL §1 tells you to use inside Claude Code — both seats get `"model": "caller's choice"` and the `CALLER` line carries no model, so nothing pins Dave and Dario to the same `SEAT_MODEL`. The D2 decision ("the same Claude model … removes the tool confound", SKILL table; plan round 3) is not enforced exactly where a Dave-vs-Dario comparison is actually run.
   **Input:** `six_experts.py run "…" --only dave,dario --claude-by-caller` → the two `CALLER` lines are identical and name no model; `status.json` says `caller's choice` for each.
   **Fix:** put the model on the `CALLER` line (e.g. `use model claude-sonnet-5-5`) and record it in `status.json`, or refuse a two-seat comparison in caller mode.

5. **low** — `six_experts.py` patch line 420 and patch line 436.
   **Wrong:** the module docstring still says "ask four experts and Dave (the control)" and "Dave claude Opus 5.5 — the control", contradicting the code (six seats, Dario as the plain control, Dave on `SEAT_MODEL` `claude-sonnet-5-5`). Patch lines 21–24 are also now false for Dario ("Each expert gets its own list … decide through its numbered rules"; "check verifies each expert cited … item numbers").
   **Fix:** update the docstring to six seats, Dario the plain control, Dave/Dario on Sonnet 5.5.

6. **low** — `.claude/skills/six-experts/SKILL.md` patch lines 81–85, 61, 130–132.
   **Wrong:** (a) §2 still says `check` requires "every answer" to "cite at least one item" and match Chinese against "its list", but Dario is exempt; (b) the `--only` id list omits `dario`; (c) the note "linked into `~/.claude/skills` and `~/.agents/skills`" is false in this environment — both symlinks still point at `…/ancient-games/.claude/skills/four-experts`, so the skill is not reachable under the new name (plan round 4's "the links move" was not done).
   **Fix:** correct the §2 wording and id list; move `~/.claude/skills/four-experts` and `~/.agents/skills/four-experts` to `six-experts`.

7. **low** — `six_experts.py` patch line 420 is the live-code residue of the old name (see #5); `docs/METHOD_CHANGELOG.md:31–35` (outside the patch) still names the `four-experts` skill and "the four experts" in the 2026-10-16 entries, and there is no changelog entry for the rename itself.
   **Fix:** add the rename entry and use the current name; keep only the historical run-folder paths (`runs/20261013-four-experts-*`), which are correctly untouched.

8. **low** — checks that cannot fail:
   - `.claude/skills/workflow-design/guard/test/round11-insight-index.test.ts:279–280`: `expect(rows(b, shipped).every((e) => e.category === "-" || shipped.some((r) => r.id === e.category))).toBe(true)` is tautological — `categorize` can only return `"-"` or one of the same `shipped` ids — so it asserts nothing.
   - `tests/test_six_experts.py:273–276`: the test that Dario is "not judged on … Chinese" appends `中文`, a 2-character run, while `CJK_RUN` needs 4+, so the Chinese half cannot trip the check even if the `PLAIN` early-return were removed.
   **Fix:** assert something that can change (e.g. every shipped id places at least one planted section; use a 4+ character run and call `check_one` on a non-plain seat).

Areas checked clean:

- **Dario's brief carries nothing beyond the question and the answer's shape:** Checked and found nothing — `assets/brief-plain.md` holds only the question, the answer shape and the five headings; the runner writes it through the `sid in PLAIN` branch before any list/identity/insight append (patch lines 224–227, 642–645).
- **A way two opencode experts could still overlap:** Checked and found nothing — `opencode_busy()` (patch lines 701–702) is checked both in the launch loop and before draining `waiting`, the failing-Linus path re-checks it before `launch` (patch lines 754–758), and a process stays in `procs` until its exit is reaped, so no second opencode call can start while one is live.

The other areas above were **not** clean: "code that does not do what the skill/plan/SPEC says" (#2, #4, #5, #6), "text from insight sections reaching the index" (#1), "a crash path" (#3), and "a reference still pointing at the old four-experts name in live code" (#5, #6, #7).
