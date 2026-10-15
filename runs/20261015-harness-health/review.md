Reviewed commit `cb808f1`; no files were edited. **My reading:** the change does not meet AC2–AC5. It leaks an alphabetic planted token, crashes on malformed mode fields, and reports several unsupported `present` findings.

## 1. Verdict per criterion

| Criterion | Verdict | Evidence |
|---|---|---|
| AC1 | **Cannot tell** | `dsh` and `opencode` are added at [readiness.py:40](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/readiness.py:40). The 26 readiness tests collect, but I could not run them successfully in this sandbox. |
| AC2 | **Does not hold** | Lists or objects in mode fields crash before any rows print. External config directories and instruction-file read errors can print absolute paths; see defects below. The ordinary machine run prints ten rows. |
| AC3 | **Does not hold** | The project-instruction check can say `absent`, but existing files produce `measured`, never `present`, at [harness_health.py:136](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:136). Its test checks that the absent finding disappears at [test_harness_health.py:136](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:136). The other absent-capable checks have both cases. |
| AC4 | **Does not hold** | With `{"hooks":{"SecretPlantToken":[{"command":"true"}]}}`, the planted token appears in both Markdown and JSON. |
| AC5 | **Does not hold** | `--self-test` creates directories and writes settings files at [harness_health.py:378](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:378). All six nonempty snippets flipped their findings in an in-memory replay using the implementation author’s helper; that does not establish their correctness under the printed instructions or actual harness behavior. |
| AC6 | **Cannot tell** | The full suite collects **1013 tests**. Execution stops before tests start with `FileNotFoundError: No usable temporary directory found`, because the sandbox is read-only. The saved baseline records 994 passes; the run state reports 1013 passes, which I could not independently reproduce. |
| AC7 | **Holds** | The live machine run reports Claude deny rules `absent`, Codex’s two top-level keys `not set`, and both `dsh` and `opencode` installed. The [saved output](/home/smoke01/dev/ancient-games/runs/20261015-harness-health/evidence/harness-health-this-machine.md) contains the same required findings. |

## 2. Defects

Both copies of `harness_health.py` are identical; these findings apply to both.

1. **High — arbitrary hook names leak configuration strings.**  
   [harness_health.py:268](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:268) accepts any alphabetic event name and prints it at line 271. Input `{"hooks":{"SecretPlantToken":[{"command":"true"}]}}` prints `events: SecretPlantToken` in both output formats. An alphabetic filter does not establish that a string is a recognized event or safe to disclose.

2. **Medium — malformed mode types crash the entire report.**  
   [harness_health.py:251](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:251) and [harness_health.py:305](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:305) perform set membership without checking types. Concrete inputs:
   - Claude: `{"permissions":{"defaultMode":[]}}` or `defaultMode: {}`.
   - Codex: `sandbox_mode = []`, `approval_policy = []`, or either key assigned `{}`.

   Each raises `TypeError: unhashable type`. A mocked CLI replay produced zero stdout bytes before crashing. Selection happens after gathering at line 402, so a malformed unselected harness can also break `--harness codex`.

3. **High — permission mode gives false reassurance about human approval.**  
   [harness_health.py:244](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:244) treats everything except `bypassPermissions` as `present`, including `"bogus"` and `"dontAsk"`. The former is unrecognized; the latter suppresses approval prompts by denying calls that would prompt. `auto` also runs without routine human prompts. These results do not support the line’s stated human-approval interpretation. [Claude’s permission-mode documentation](https://code.claude.com/docs/en/permissions#permission-modes) describes those behaviors.

4. **Medium — nonempty malformed deny lists count as configured deny rules.**  
   [harness_health.py:207](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:207) checks only list type and nonemptiness. `{"permissions":{"deny":[null]}}` produces `present`, with `1 in user`, although it contains no tool/path rule.

5. **Medium — hooks can say `present` with no runnable or enabled hook.**  
   [harness_health.py:268](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:268) accepts `{"hooks":{"Stop":[{"hooks":[]}]}}`. It also ignores `disableAllHooks`: a valid Stop hook alongside `"disableAllHooks":true` still produces `present`. Both were reproduced in memory. [Claude’s hook documentation](https://code.claude.com/docs/en/hooks#disable-or-remove-hooks) confirms that this setting disables configured hooks.

6. **Medium — absolute paths escape the path formatter.**  
   [harness_health.py:90](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:90) returns the absolute path when it falls outside home and cwd. For example, `CODEX_HOME=/opt/shared` exposes `/opt/shared/config.toml`. Separately, line 134 prints the raw `OSError`; an instruction-file `PermissionError` exposes its absolute filename even when the formatted proof is relative.

7. **Medium — non-UTF-8 Codex configuration crashes.**  
   [harness_health.py:291](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:291) reads text, but its exception handler excludes `UnicodeDecodeError`. A config containing byte `0xff` raises that exception instead of returning `unknown`.

8. **Medium — the no-write claim excludes an advertised execution path.**  
   [harness_health.py:378](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:378) creates temporary directories and writes two configurations during `--self-test`. Cleanup does not satisfy “never writes a file.”

9. **Low — help claims exceed what is emitted.**  
   [harness_health.py:274](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:274) emits an empty snippet for absent hooks. Engine and instruction-file help also lack snippets, despite the blanket file/key/snippet claim in the docstring and [method documentation:105](/home/smoke01/dev/ancient-games-harness-health/docs/WORKFLOW_DESIGN_METHOD.md:105). JSON merge instructions exist in the test helper, but are not printed to the person applying the snippets.

## 3. Tests that would pass on a broken script

- **`test_hh_03_planted_secret_never_printed`**, [line 151](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:151): its token contains hyphens and digits, so the hook-name regex rejects it. The same output code leaks an alphabetic token. I reproduced both outcomes.
- **`test_hh_04_every_snippet_flips_its_finding`**, [line 188](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:188): skips empty snippets and supplies its own JSON merge procedure. It can pass while absent findings have no snippet and printed application instructions are incomplete.
- **`test_hh_05_no_file_changes`**, [line 202](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:202): checks file contents only under fake home and cwd. It misses empty-directory creation, permission changes, writes elsewhere, and `--self-test`.
- **`test_hh_06_covered_goes_missing_without_its_script`**, [line 213](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:213): explicitly uses empty backing scripts and accepts `verified / covered`. It proves file existence, not that the claimed gates, logging, or recovery work.
- **`test_hh_02_engine_kinds_and_instruction_file`**, [line 127](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:127): never asserts `present` for the instruction-file check, leaving AC3’s stated requirement unchecked.

## 4. What I did not check

I could not execute the test suite or apply snippets to disk under the read-only sandbox. I did not launch model tasks, measure quota consumption, verify harness enforcement, or rerun the saved mutation checks.

The adversarial probes were checks I wrote using mocked file reads and version commands. They establish the script’s parsing and rendering behavior; they do not independently establish how installed harnesses interpret those configurations.