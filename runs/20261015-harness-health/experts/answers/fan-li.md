# 范蠡 (Fan Li) — Harness Health Extension

## Answer
Build harness health as an independent companion script (`harness_health.py`) that examines the defensive preparations of designated engines without mutating their configurations, reports objective measurements without invented numeric thresholds, and provides non-destructive, copy-pasteable configuration snippets when settings tilt toward vulnerability. If a target engine lacks internal guardrails, do not force an artificial pass; adapt the workflow design by strengthening external Guard gates and read-only constraints.

## How I decided

1. **Examine defensive preparations before engaging (my #18).**
   Readiness is fundamentally the examination of defense: 「審備則可以戰乎？」王曰：「巧。」 (`quoted`). Before dispatching autonomous agents into codebases, we must ascertain whether defensive measures are close-knit and unbreachable.

2. **Divide labor between inventory and health evaluation (my #14, addressing U4).**
   「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也。」 (`quoted`). Let each component perform what it is built for. `readiness.py` is the established inventory inspector (probing binary paths, versions, logins, and environment facts); `harness_health.py` must live as a separate companion script dedicated to evaluating security posture, configuration integrity, and alignment with the ten requirements. Overloading `readiness.py` with normative policy checks conflates inventory with governance.

3. **Separate harness-level capability from run-level execution (my #14, addressing U7).**
   Say who is responsible for what. Requirements 2 (tool design), 3 (task structure), and 7 (recovery/retries), along with parts of 5 (independent verifiers) and 8 (human gates), are properties governed by the workflow method and its run-time gates (`design_gate.py`, `feature_gate.py`, `dispatch.py`), not static attributes of harness configuration files. `harness_health.py` should inspect static harness capabilities (e.g. hook registration, CLI flags, sandbox support) and explicitly mark run-level disciplines as "enforced by workflow method" rather than inventing redundant probes.

4. **Scope verdicts to engines designated for action (my #1, addressing U1).**
   「夫聖人隨時以行，是謂守時。天時不作，弗為人客；人事不起，弗為之始。」 (`quoted`). Do not initiate conflict where no campaign is planned. The script should list all detected harnesses as broad inventory, but the health verdict and gate checks must evaluate only the engine(s) designated for the specific workflow (configurable via `--harness`). Demanding perfection from unused harnesses on the host machine halts valid work for no purpose.

5. **Provide humble advice and ready snippets, never auto-fix (my #13 and #15, addressing U2).**
   「夫勇者，逆德也；兵者，凶器也；爭者，事之末也。陰謀逆德，好用凶器，始於人者，人之所卒也；淫佚之事，上帝之禁也，先行此者，不利。」 (`quoted`). A script that unilaterally modifies a developer's environment or global configuration files (`~/.claude/settings.json`, `~/.codex/config.toml`) initiates reckless aggression and will eventually destroy working setups. Instead, steady what is tilting through humble, transparent guidance (my #15: 「卑辭尊禮…又身與之市」 [`quoted`]): provide exact file paths, describe the diagnosed gap, and emit ready-to-apply configuration patches or CLI commands for the human to review and apply.

6. **Measure what is there without inventing thresholds (my #3, addressing U3).**
   「時不至，不可彊生；事不究，不可彊成。自若以處，以度天下，待其來者而正之，因時之所宜而定之。」 (`quoted`). When a standard has not been established by EJ, completion cannot be forced. Where a requirement possesses a concrete binary reality (e.g. a `deny` list exists, a sandbox flag is declared, a hook is installed), report a concrete status (`verified` or `MISSING`). Where a requirement is a quantitative continuum (e.g. instruction file length for R1, number of MCP tools for R2), measure and report the exact number ("自若以處，以度天下") without inventing an arbitrary pass/fail cutoff.

7. **Compensate for internal harness weakness with external workflow firmness (my #12, addressing U5).**
   「彼來從我，固守勿與。若將與之，必因天地之災…宜為人主，安徐而重固；陰節不盡，柔而不可迫。」…「今其來也，剛彊而力疾，王姑待之。」 (`quoted`). If an engine lacks sandbox isolation or strict permissions, do not pretend it is safe. Treat it as a defender whose yin is not yet full: keep the workflow "calm, slow, heavy and firm" by elevating Guard stage approval requirements, enforcing read-only tool constraints, or restricting that engine to non-destructive analysis nodes. Method 3.1 should incorporate an explicit "Harness health condition → Workflow design adjustment" table.

8. **Do not speculate on unverified configuration schemas (my #7 and #9, addressing U6).**
   「未可也。蠡聞之，上帝不考，時反是守，彊索者不祥。…王無蚤圖。夫吳，君王之吳也，王若蚤圖之，其事又將未可知也。」 (`quoted`) and 「逆節萌生。天地未形，而先為之征，其事是以不成，雜受其刑。王姑待之。」 (`quoted`). Campaigning before form has taken shape leads to collective failure. Where configuration paths, keys, and schemas for specific engines (`dsh`, `opencode`, `agy`) have not been verified against installed versions, mark them honestly as `unknown` with the reason stated. Never speculate or write brittle regex parsers for unverified formats.

9. **New unclear spot N1 — Precedence of local versus user-level configurations (my reading).**
   When both user-level (`~/.claude/settings.json`) and project-level (`.claude/settings.json`) files exist, which governs the health assessment? My reading: project-level settings take precedence if present; if absent, user-level settings define the baseline. This prevents false alarms in shared repositories.

10. **New unclear spot N2 — Intake failure policy: hard abort versus adaptive mitigation (my reading).**
    Does a failed health condition on a selected engine abort workflow intake (exit 1), or does it emit workflow adjustments (U5) and continue? My reading: it should only exit 1 if `--strict` or a mandatory flag is passed; by default, it should complete with exit 0, emit the remediation snippet, and record the necessary Guard compensations in the design.

11. **Concrete design specification (my reading, synthesized from my #3, #14, #15, #18).**
    - **Location**: `.claude/skills/workflow-design/scripts/harness_health.py`, executable standalone and importable by `.claude/workflows/intake.js`.
    - **Requirement Checks**:
      - *R1 (Clear context)*: Measure line counts of instruction files (`CLAUDE.md`, `AGENTS.md`) and report active skills; report raw values without arbitrary thresholds.
      - *R2 (Well-designed tools)*: Verify dispatcher engine adapters pass required containment flags (e.g. read-only, schema validation).
      - *R3 (Task structure)*: Verify engine CLI supports structured output / json schema.
      - *R4 (State/memory)*: Verify progress storage and checkpoint directories exist and are writable.
      - *R5 (Independent verification)*: Verify at least two distinct engine types are installed and verified, ensuring reviewer != builder.
      - *R6 (Guardrails/permissions)*: Inspect `permissions.deny` in `settings.json` and sandbox flags in `config.toml`.
      - *R7 (Recovery/retries)*: Verify dispatch adapter timeout and retry bounds are defined.
      - *R8 (Human gates)*: Verify approval policies and confirmation prompts are active in engine settings.
      - *R9 (Observability)*: Verify logging hooks, token tracking, and `events.jsonl` output mechanisms.
      - *R10 (Feedback loop)*: Verify pre-prompt and post-turn hooks (e.g. `UserPromptSubmit`) are registered.
    - **Output**: Clean Markdown or `--json` table adhering to the `readiness.py` conventions (`verified`, `reported`, `unknown`, `MISSING`), accompanied by a "Required Workflow Adaptations" section.
    - **Help**: A "Remediation Snippets" section outputting exact file targets and valid, copy-pasteable JSON/TOML blocks.

12. **Build order with verifiable failure checks (my #2 and #18).**
    Regulate affairs by tangible ground realities (my #2: 「節事者與地」 [`quoted`]). Every step must demonstrate that its check can fail:
    - *Step 1: Core probe runner and parser skeleton.* Test on verified configs (`claude`, `codex`).
      *Check that can fail (Sabotage)*: Plant a corrupted, malformed JSON file; verify parser catches it cleanly, returns `unknown` with error detail, and does not crash.
    - *Step 2: Security and guardrail checks (R6, R8).* Implement permission deny list and sandbox probes.
      *Check that can fail (Sabotage)*: Plant an empty `permissions.allow` with no `deny` entries; verify output reports `MISSING` on deny list and emits warning.
    - *Step 3: Objective measurements (R1, R9, R10).* Implement context line counter and hook inspectors.
      *Check that can fail (Sabotage)*: Remove hook configuration; verify hook status drops to `MISSING` and line count accurately reflects an empty file.
    - *Step 4: Help snippet generator.* Implement remediation formatting for missing keys.
      *Check that can fail (Sabotage)*: Run generator against planted failures; verify generated snippet is syntactically valid JSON/TOML and that target configuration files remain completely unmodified (hash check).
    - *Step 5: Engine scoping and design effect generator (U1, U5).* Implement `--harness` filtering and adaptation table output.
      *Check that can fail (Sabotage)*: Specify a non-existent harness with `--harness fake_engine --require`; verify script exits 1 with explicit missing engine error.
    - *Step 6: Pytest test suite (`tests/test_harness_health.py`).* End-to-end unit tests with isolated mock environments.
      *Check that can fail (Sabotage)*: Introduce an intentional assertion inversion; verify pytest detects failure immediately.

## What I need to know

1. If EJ intends instruction file length (R1) to trigger an explicit warning, what is their preferred line count or token budget? (If EJ provides a number, we alert on it; if not, we report only the measured line count).
2. If a selected engine fails health checks during intake, should the workflow design halt immediately with exit 1, or should it proceed by applying stricter external Guard constraints (N2)?
3. Are the configuration file locations and key names for `dsh`, `opencode`, and `agy` documented and stable on this system? (If provided, we probe them; if not, they remain `unknown`).

## Costs and risks

- **Risk of missed vulnerabilities through non-speculation (from my #7 and #9):** Keeping unverified configuration keys as `unknown` prevents false assumptions, but may leave uninspected risks if a harness uses non-standard security keys.
- **Cost of manual remediation over auto-fix (from my #13 and #15):** Requiring the human to review and apply config snippets takes human time, though it avoids the severe risk of corrupting user configuration files.
- **Cost of maintaining two companion scripts (from my #14):** Keeping `readiness.py` as inventory and `harness_health.py` as health evaluation requires maintaining two CLI interfaces and test suites rather than one combined script.
- **Cost of unthresholded reporting (from my #3):** Reporting numbers without pass/fail thresholds places the cognitive burden of evaluating sizing and context budgets on the workflow designer.

## How we would know I was right

Run `python3 .claude/skills/workflow-design/scripts/harness_health.py` against the host machine:
1. It executes without modifying or creating any files in `~/.claude`, `~/.codex`, or the project root (verified by `git status` and SHA-256 hashes of config files remaining identical before and after execution).
2. It correctly identifies the real state of `~/.claude/settings.json` (reporting `permissions.allow` as present, `permissions.deny` as `MISSING`, and `UserPromptSubmit` hook as `verified`), outputting a valid, copy-pasteable JSON snippet to configure `permissions.deny`.
3. In `tests/test_harness_health.py`, every planted defect across mock configurations triggers a distinct, reproducible test failure, confirming that no check gives a false pass.
