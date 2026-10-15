Reviewed `d7a1390`; both script copies are identical. No files were edited.

**My reading:** AC2 and AC5 still do not hold. The original secret leak and malformed-mode crashes are fixed, but filesystem errors still crash the report, and one new help snippet leaves its finding `absent`.

## 1. Round-1 defects and weak tests

Line references below point to the current implementation.

| Round-1 defect | Status | Evidence |
|---|---|---|
| 1. Arbitrary hook names leak secrets | **Fixed** | [harness_health.py:304](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:304) uses an event whitelist. Both planted tokens stayed out of Markdown and JSON in my replay. |
| 2. Malformed mode types crash | **Fixed** | String guards at [line 274](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:274) and [line 350](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:350). Lists and objects now produce `unknown`. |
| 3. Permission modes falsely imply human approval | **Fixed** | [Line 276](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:276): `auto` and `dontAsk` produce `absent`; `bogus` produces `unknown`. |
| 4. Malformed deny lists count as configured | **Partly** | [Line 247](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:247) rejects null, numeric and empty entries, but still counts strings Claude skips; see defect 2 below. |
| 5. Empty or disabled hooks say `present` | **Partly** | Empty handlers and `disableAllHooks=true` now produce `absent`. [Line 298](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:298) still accepts invalid handler types; see defect 3. |
| 6. Absolute paths escape formatting | **Partly** | [Line 107](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:107) formats external directories symbolically, and caught read errors print only exception names. Uncaught filesystem checks still expose paths; see defect 1. |
| 7. Non-UTF-8 Codex config crashes | **Fixed** | [Line 333](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:333) catches `ValueError`, including `UnicodeDecodeError`. My replay returned `unknown`. |
| 8. Self-test violates no-write requirement | **Not fixed** | [Line 420](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:420) creates directories; lines 423 and 425 write settings. The docstring now acknowledges these writes. |
| 9. Help claims exceed emitted instructions | **Fixed** | [Line 410](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:410) prints application instructions. The [method text:106](/home/smoke01/dev/ancient-games-harness-health/docs/WORKFLOW_DESIGN_METHOD.md:106) limits the snippet claim to settings fixes. |

| Round-1 weak test | Status | Evidence |
|---|---|---|
| Secret test misses alphabetic tokens | **Fixed** | [test_harness_health.py:161](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:161) tests both token forms in both output formats. |
| Snippet test supplies missing instructions and skips findings | **Partly** | [Line 208](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:208) checks printed instructions. Its fixture misses the new disabled-hooks snippet. The merge helper at line 179 replaces lists, whereas the printed instructions say to append items. |
| No-write test misses filesystem changes | **Partly** | [Line 78](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:78) now records directories and permissions; line 223 invokes self-test. It still checks only fake home and project trees after execution, missing temporary writes elsewhere. |
| Covered-script test accepts broken scripts | **Not fixed** | [Line 231](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:231) still creates empty scripts and accepts `covered`. The new implementation docstring explicitly acknowledges that this proves existence only. |
| Instruction-file test never asserts `present` | **Fixed** | [Line 144](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:144) now asserts `present`. |

## 2. New defects introduced or still present

1. **Medium — inaccessible directories crash the report and expose absolute paths.**  
   Filesystem checks occur outside error handlers at [harness_health.py:163](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:163), line 118 and line 330.

   A live run with `CLAUDE_CONFIG_DIR=/root/.claude` and `--harness codex` exited **1**, printed **zero stdout bytes**, and ended with:

   ```text
   PermissionError: [Errno 13] Permission denied: '/root/.claude/CLAUDE.md'
   ```

   A direct check using `CODEX_HOME=/root/.codex` likewise raised `PermissionError` for `/root/.codex/config.toml`.

2. **Medium — a skipped deny rule still produces `present`.**  
   [Line 247](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:247) counts every nonempty string. Input:

   ```json
   {"permissions":{"deny":["mcp__github__create_issue(foo)"]}}
   ```

   My replay produced `present`, `1 in user`. Claude’s documentation says settings-file `mcp__` rules containing parentheses are skipped. [Permission-rule documentation](https://code.claude.com/docs/en/permissions#match-by-input-parameter).

3. **Medium — invalid hook handlers still produce `present`.**  
   [Line 298](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:298) checks `command` but ignores `type`. Input:

   ```json
   {"hooks":{"Stop":[{"hooks":[{"type":"bogus","command":"true"}]}]}}
   ```

   My replay produced `present`, `events: Stop`. Omitting `type` also produces `present`, although the documented schema requires a recognized type. [Hook-handler fields](https://code.claude.com/docs/en/hooks#common-fields).

4. **Medium — valid prompt hooks now produce `absent`.**  
   The same [command-only check:298](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:298) rejects this configured hook:

   ```json
   {"hooks":{"Stop":[{"hooks":[{"type":"prompt","prompt":"Check completion"}]}]}}
   ```

   My replay produced `absent`. This is a regression from round 1; prompt handlers use `prompt` instead of `command`. [Prompt-hook configuration](https://code.claude.com/docs/en/hooks#prompt-hook-configuration).

5. **Medium — the new disabled-hooks snippet does not always fix its finding.**  
   [Line 307](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:307) emits `{"disableAllHooks":false}` for input `{"disableAllHooks":true}`, even when no hooks exist. Applying that snippet as instructed leaves the hooks finding **`absent → absent`**. This directly fails AC5.

6. **Medium — self-test still writes files.**  
   [Line 418](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/harness_health.py:418) creates a temporary tree; lines 423 and 425 write settings files. Concrete invocation: `harness_health.py --self-test`. Cleanup does not satisfy the unchanged “never write a file” requirement.

## 3. Verdict per criterion AC1–AC7

| Criterion | Verdict | Evidence |
|---|---|---|
| AC1 | **Cannot tell** | `dsh` and `opencode` remain listed at [readiness.py:40](/home/smoke01/dev/ancient-games-harness-health/.claude/skills/workflow-design/scripts/readiness.py:40). I could not execute the prior readiness tests. |
| AC2 | **Does not hold** | The inaccessible-directory run prints no requirement rows and exposes an absolute path in stderr. Ordinary machine output prints ten rows. |
| AC3 | **Holds** | The tests contain absent/present assertions for all nine absent-capable checks: the [Claude cases:99](/home/smoke01/dev/ancient-games-harness-health/tests/test_harness_health.py:99), Codex cases at line 125, and engine/instruction cases at line 135. This is a coverage finding, not a claim that I executed those tests. |
| AC4 | **Holds for the planted values checked** | Both `SECRET-PLANT-7f3a9c` and `SecretPlantToken` were absent from Markdown and JSON in my adversarial replay. |
| AC5 | **Does not hold** | Six existing setting snippets flipped their findings in my independent in-memory application. The disabled-hooks snippet failed on the no-hooks input, and self-test still writes files. |
| AC6 | **Cannot tell** | **1,024 tests collected** independently. Test execution stopped before tests began because no writable temporary directory exists. The brief reports the builder’s **1,024 passed**; I could not reproduce that result. |
| AC7 | **Holds** | Both the live machine run and [saved output](/home/smoke01/dev/ancient-games/runs/20261015-harness-health/evidence/harness-health-this-machine.md) show Claude deny rules absent, Codex’s two top-level keys unset, and `dsh` and `opencode` installed. |

## 4. What I did not check

I did not execute the test suite, apply snippets to disk, rerun mutation checks, launch model tasks, measure quota usage, or verify harness enforcement.

The parsing, rendering and snippet probes were checks I wrote using mocked reads and version commands. They establish this script’s behavior, not installed-harness enforcement. The inaccessible-directory crash was reproduced with the live CLI.