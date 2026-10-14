# 范蠡 (Fan Li) — Source-of-truth memory levels

## Answer
I recommend assigning MUST strictly to structural defenses, irreversible data-loss boundaries, capacity ceilings, and plan-integrity gates; assigning SHOULD to procedural defaults and authoring methods that allow reasoned adaptation; and classifying definitions, scope boundaries, and epistemic limits as guidance. If tooling does not yet exist to automate a check, imposing a hard gate forces growth before its season and breeds contention.

| Id | Level | Reason (one line) |
| :--- | :--- | :--- |
| W1.1 | MUST | Structural defense against merge collisions and broken references across uncoordinated branches (my #18). |
| W1.2 | MUST | Machine-readable frontmatter is the defensive foundation for index generation and automated tracking (my #18). |
| W1.3 | Split: MUST / SHOULD | One claim per entry is MUST to prevent semantic merge collisions (my #18); specific body headings (**Why:**, **How to apply:**) are SHOULD method defaults. |
| W2.1 | guidance | Definitions of decision and fact explain terms; the timing gate is enforced under W5.1 and K1.1 (my reading). |
| W2.2 | guidance | Semantic definitions of entry kinds guide writers and do not constitute a blocking gate by themselves (my reading). |
| W3.1 | SHOULD | Avoids redundant code/test duplication and overflow (my #2), but is an editorial default rather than a catastrophic hazard. |
| W3.2 | MUST | Absolute security boundary where secret leakage incurs immediate harm and disaster (my #4, #18). |
| W3.3 | MUST | Safety bound preventing unmanageable context bloat and private state contamination (my #10, #18). |
| W3.4 | MUST | Prohibits false completion claims that induce premature downstream commitments (my #2, #9). |
| W3.5 | MUST | Boundary defense keeping project scope separate from personal or agent-specific memory (my #14, #18). |
| W3.6 | SHOULD | Prevents redundant documentation drift (my #2), but linking versus copying is an editorial default. |
| W4.1 | MUST | Architectural rule barring ownership bottlenecks and permission contention (my #13, #14). |
| W4.2 | MUST | Audit trail requirement ensuring chronological accountability for every change (my #18). |
| W4.3 | guidance | Clarifies that non-entry files rely on git history rather than internal change logs (my reading). |
| W5.1 | MUST | Timing gate preventing state loss at handoffs and ungrounded code changes (my #4, #5). |
| W5.2 | SHOULD | Default sequencing to synthesize non-critical lessons at task end, overridable if needed earlier (my #3). |
| W5.3 | MUST | Closes the loop on build decisions with verified evidence before a task is deemed complete (my #4, #18). |
| W6.1 | MUST | Structural defense eliminating concurrent write contention and file clobbering (my #13, #18). |
| W6.2 | MUST | Workspace isolation ensuring concurrent work surfaces conflicts safely in git (my #18). |
| W6.3 | MUST | Non-destructive merge contract preserving history and referring ambiguities to EJ (my #5, #18). |
| K1.1 | MUST | The recorded decision governs execution; altering code before the entry breaks intentional control (my #5). |
| K4.1 | MUST | Absolute ban on deletion prevents irreversible loss of institutional history (my #18). |
| K4.2 | guidance | Establishes that memory validity is event-driven via Rd5 verification rather than expired by calendar age (my reading). |
| K4.3 | MUST | Claim immutability preserves historical truth and prevents semantic merge conflicts (my #5, #18). |
| K5.1 | SHOULD | Default storage layout for session raw notes, overridable if a workflow has an alternate scratch area (my #3). |
| K5.2 | MUST | Gate ensuring raw session notes are distilled into durable entries before task handoff (my #4, #6). |
| K6.1 | MUST | Machine generation guarantees index consistency and forbids unverified manual edits (my #18). |
| K6.2 | MUST | Verified mechanical gate keeping the index synchronized with entry changes in every commit (my #18). |
| K6.3 | MUST | Prevents corrupted index state by requiring programmatic regeneration over manual conflict resolution (my #18). |
| Rd1.1 | MUST | Fixed repository topography required for tools and incoming agents to locate memory reliably (my #18). |
| Rd1.2 | MUST | Zero-external-dependency requirement ensuring memory is fully readable from a fresh clone alone (my #3, #18). |
| Rd2.1 | MUST | Mandatory startup orientation ensuring an agent takes the measure of the field before acting (my #3, #18). |
| Rd2.2 | SHOULD | Default reading schedule to conserve startup context, overridable when specific background is needed (my #1, #3). |
| Rd2.3 | MUST | Absolute safety bound against context window exhaustion and security contamination (my #10, #18). |
| Rd3.1 | MUST | Hard capacity ceiling preventing index size from exceeding the strictest agent limit (my #2, #10). |
| Rd4.1 | MUST | Requires reading covering decisions before editing code to prevent architectural regressions (my #5, #18). |
| Rd4.2 | guidance | Recommended search method for finding entries; the lookup mechanism does not gate work (my reading). |
| Rd4.3 | guidance | Recommended investigative heuristics for tracing intent and line history (my reading). |
| Rd4.4 | SHOULD | Default navigation discipline to avoid obsolete guidance, overridable during historical audits (my #3). |
| Rd4.5 | MUST | Provenance requirement preventing private agent opinions from masquerading as verified project memory (my #14, #18). |
| Rd5.1 | MUST | Verification gate requiring claims to be cross-checked against code before action (my #1, #12). |
| Rd5.2 | MUST | Precedence rule preserving standing instructions over historical memory (my #8). |
| Rd5.3 | MUST | Constitutional boundary requiring code-entry discrepancies to be reported to EJ rather than settled unilaterally (my #5, #6, #14). |
| Rd5.4 | guidance | Clarifying exemptions defining what does not constitute a mismatch under Rd5.3 (my reading). |
| Rd5.5 | guidance | Explains the epistemic limitations of code-based verification (my reading). |
| Rd6.1 | MUST | Verification gate proving handoff state is sufficient for autonomous continuation without re-asking settled questions (my #18). |

## How I decided

1. **Examine defensive preparations first (my #18).** In my list, I asked: 「審備則可以戰乎？」 (`quoted`, #18). Defensive preparations that cannot be broken into earn MUST. Structural rules that prevent branch collisions, clobbering, and broken references (W1.1, W1.2, W6.1, W6.2, W6.3, K6.1, K6.2, K6.3, Rd1.1, Rd1.2) must be hard gates; if any fails, downstream work cannot stand.
2. **Contention is the last of affairs (my #13).** In my words: 「夫勇者，逆德也；兵者，凶器也；爭者，事之末也」 (`quoted`, #13). Creating blocking gates where defaults suffice causes unnecessary friction among agents and people. Rules concerning editorial cleanliness and documentation duplication (W3.1, W3.6, K5.1, Rd4.4) must be SHOULD defaults, overridable with stated reasons rather than blocking halts.
3. **While the time has not come, growth cannot be forced (my #3).** In my words: 「時不至，不可彊生；事不究，不可彊成」 (`quoted`, #3). Today no lint over `entries/` exists and no product has used this memory (n=0). Forcing rigid structural styling (such as the subheadings in W1.3) as an absolute blocking gate before tooling exists forces completion before its time. Hence W1.3 splits: atomic claims earn MUST to preserve merge safety, while internal section headings remain SHOULD.
4. **The plan does not shift (my #5).** In my words: 「夫謀之廊廟，失之中原，其可乎？…天節固然，唯謀不遷」 (`quoted`, #5). Decisions planned at court must not be discarded on the field. Changing code without updating governing entries (K1.1, W5.1) or unilaterally altering a contradicted decision entry without EJ's decision (Rd5.3) destroys intentional governance. These are MUST gates.
5. **Turning at the extreme, and stopping (my #10; and my #2).** In my words: 「善用兵者，贏縮以為常，四時以為紀，無過天極，究數而止」 (`quoted`, #10), and 「天道盈而不溢」 (`quoted`, #2). Index sizes and context dumps must not exceed natural agent capacity. Strict bounds that prevent context exhaustion (Rd2.3, Rd3.1, W3.3) are protective MUST gates.
6. **Say who is better at what, and honour the boundaries (my #14; and my #6).** In my words: 「四封之內，百姓之事，蠡不如種也。四封之外，敵國之制，立斷之事，種亦不如蠡也」 (`quoted`, #14), and 「君行制，臣行意」 (`quoted`, #6). Mechanized tasks belong to tools (`memory_index.py`), while decisions on policy belong to EJ. W4.1 correctly forbids approval bottlenecks (MUST), and Rd5.3 preserves the ruler's prerogative to settle contradictions (MUST).
7. **Cross-check human affairs with Heaven and Earth (my #1; and my #12).** In my words: 「夫人事必將與天地相參，然後乃可以成功」 (`quoted`, #1), and 「又觀其民之饑飽勞逸以參之」 (`quoted`, #12). Acting on memory without verifying it against real code, tests, or commits invites defeat. Rd5.1 must be a MUST gate before taking action.
8. **Distinguish rules from definitions and limits (my reading).** Statements that clarify meanings (W2.1, W2.2), define non-entry storage scopes (W4.3), explain invalidation concepts (K4.2), or establish epistemic boundaries (Rd5.4, Rd5.5) do not evaluate actions and cannot fail; they are guidance.

## What I need to know

1. If EJ plans to enforce all entry formatting with an automated pre-commit script before the first run, the section headings in W1.3 could become machine-enforced; if checks remain human-reviewed or n=0, enforcing them as MUST will stall work on trivial styling disputes.
2. If multi-agent teams share a single central branch rather than distinct branches or worktrees, the collision avoidance in W6.2 would require additional branch-locking doctrine, though W1.1 and W6.1 remain necessary in either case.

## Costs and risks

1. **Risk of minor narrative drift:** Classifying documentation duplication (W3.1, W3.6) and session wrap-up timing (W5.2) as SHOULD relies on reviewer vigilance; careless reviewers may let bloated entries accumulate until pruned (from my #2 on steadying what tilts).
2. **Cost of mandatory verification checks:** Making Rd4.1 (reading covering entries) and Rd5.1 (cross-checking against code) hard MUST gates imposes real latency on agent startup and tool execution, which is the price of preventing ungrounded actions (from my #18 on examining preparations).
3. **Risk of handoff blockages:** Holding fresh sessions strictly accountable to Rd6.1 will surface deficient task summaries immediately, stopping work whenever departing agents fail to record state diligently (from my #4 on not slackening when finishing).

## How we would know I was right

A measurable test on the first multi-agent run (n=1): track all halted commits, tasks, and handoffs. If every halt is triggered by genuine merge collisions, index desynchronization, ungrounded code edits, or credential leaks (MUST gates functioning as structural defenses), while agents proceed smoothly without failing on editorial formatting or search heuristics (SHOULD and guidance preventing artificial friction), then the levels were assigned correctly. If tasks routinely abort over cosmetic Markdown headings, MUST was over-extended; if uncoordinated agents silently overwrite claims or act on hallucinated memory, MUST was under-applied.
