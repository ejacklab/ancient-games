Every claim below was checked against the source. The tool failed in places, and I say where under each answer. I did not write the harness-guard criteria or deadline files, because they would change files and you said not to. Paths are relative to the repository root, so the code-map's `src/...` becomes `packages/core/src/...`.

**Q1 — Rule evaluation and the no-match case**
- `evaluate(action, resource, ...rulesets)` is at `packages/core/src/permission.ts:87-97`.
  - It flattens the rulesets and takes the last rule whose action and resource both match (`findLast`, `:89-91`).
  - Matching uses `Wildcard.match` (`packages/core/src/util/wildcard.ts:3-14`).
- With no match it returns a synthetic rule `{action, resource: "*", effect: "ask"}` (`permission.ts:91-95`).
- Related cases:
  - A session whose agent can't be resolved gets `missingAgentPermissions`, which is deny `*` `*` (`:19`, `:162`).
  - `evaluateInput` (`:173-189`) returns deny if any resource is denied by the configured rules. Otherwise it is "ask" if any resource evaluates to ask, else "allow". A plugin hook can then override the effect (`:179-188`).
- The code-map `find "permission rule evaluation"` returned nothing, and `where` on `src/permission.ts:87` also failed. I read the file directly.

**Q2 — Where the Permission service is declared and implemented**
- Declared:
  - The `Interface` (`close`, `ask`, `assert`, `reply`, `get`, `forSession`, `list`) is at `permission.ts:103-111`.
  - `class Service extends Context.Service<...>("@opencode/Permission")` is at `:113`.
- Implemented:
  - `layer` (`:121-341`) holds `ask` (`:223-229`), `assert` (`:231-263`) and `reply` (`:265-325`).
  - It is returned by `Service.of({...})` at `:339`.
  - `node` is at `:343-347`.
- Not established: the `Request`, `Reply`, `Event`, `Rule` and `Ruleset` types come from `@opencode/schema/permission` (`:5`), which I did not open.
- Code-map `where Permission.Service` returned no matches.

**Q3 — What calls `Permission.assert`**
- The code-map `callers packages/core/src/permission.ts:231` gave 18 call sites, and a grep for `permission.assert(` agrees. The plain name `where Permission.assert` resolved to the wrong symbol, `context.permission.assert` in `plugin/host.ts:438`, so I used the `file:line` form.
- Shared helpers: `FileAccess.authorizeExternal` (`file-access.ts:135`) and `authorizeRead` (`:154`).
- Plugin host: `plugin/host.ts:439`.
- Tools:
  - `tool/mcp.ts:51`
  - `tool/plugin/edit.ts:275`
  - `glob.ts:68`
  - `grep.ts:87`
  - `mcp-resource.ts:36` and `:65`
  - `opencode.ts:192`
  - `patch.ts:196`
  - `question.ts:63`
  - `shell.ts:138`
  - `skill.ts:51`
  - `subagent.ts:138`
  - `webfetch.ts:124`
  - `websearch.ts:49`
  - `write.ts:78`
- The read tool has no direct call. It reaches `assert` only through `authorizeRead`.

**Q4 — What calls the runtime `execute` (`tool/runtime.ts:29`)**
- In `src`, the only caller is `executeTool` (`packages/core/src/tool.ts:113`, call at `:119`), per the code-map.
- `executeTool` is called from the code-mode executor (`tool.ts:242`) and from the snapshot's `execute` (`tool.ts:263`, calls at `:278` and `:280`).
- Tests also call it directly: `test/tool-execute.test.ts:67` and others, and `test/tool-schema.test.ts`/`test/plugin/module.test.ts` import it. The code-map did not list these.

**Q5 — What `Permission.assert` calls (`permission.ts:231-263`)**
- Direct calls:
  - `evaluateInput` (`:234`, defined `:173`).
  - `create` (`:246`, defined `:204`) and `request` (`:191`).
  - `relevant` (`:239`, defined `:169`).
  - `new BlockedError` (`:238`).
  - `Deferred.await` (`:247`).
  - `Effect.die` (`:233` when closed, `:253` for a decline).
  - `pending.delete` (`:256`).
- `evaluateInput` in turn calls:
  - `configured` (`:174`), which calls `sessions.get` (`:159`, `session/store.ts:95`), `agents.resolve` (`:161`, `agent.ts:94`) and `merge` (`:162`).
  - `denied` (`:175`).
  - `savedRules` (`:176`).
  - `evaluate` (`:166`, `:177`).
  - `hooks.trigger` (`:179`, `plugin/hooks.ts:88`).
- The code-map's callee list for `evaluateInput` omitted `evaluate`, which is called inside a `.map` callback; I added it by reading.

**Q6 — Call chain down from the write tool to agent resolution**
- The code-map `chain` for `tool/plugin/write.ts:65` shows this path (every hop is at least 3 levels):
  - `write.ts:72` calls `authorizeExternal` (`file-access.ts:125`).
  - `file-access.ts:135` calls `Permission.assert` (`permission.ts:231`).
  - `:234` calls `evaluateInput` (`:173`).
  - `:174` calls `configured` (`:158`).
  - `:161` calls `agents.resolve` (`agent.ts:94`).
- `authorizeExternal` returns early for paths inside the location (`file-access.ts:134`). In that case the write tool's own assert reaches agent resolution directly: `write.ts:78` → `permission.ts:231` → `:173` → `:158` → `agent.ts:94`.

**Q7 — Call chain up from `Permission.assert` in the write tool to the session step**
- The code-map `chain` up from `write.ts:65` is empty, because `execute` is a callback passed to `editor.add` (`write.ts:55-64`). The links from `tool.ts:119` up to the step are partly my reading, as marked below.
- The chain, from the assert upward:
  1. `write.ts:78` is inside the write `execute` (`:64-65`).
  2. It is called by `tool.execute(decoded, context)` in `tool/runtime.ts:37`.
  3. That is `execute` (`runtime.ts:29`), called by `executeTool` (`tool.ts:119`). The code-map confirms this link.
  4. Next is the snapshot `execute` (`tool.ts:263`, calls `executeTool` at `:280`). The code-map confirms this link.
  5. That is called by `tools.execute({...call, definitions})` in `session/model-request.ts:404-405` (my reading).
  6. That is called by `input.prepared.executeTool` in `session/runner/step.ts:91-94`. It runs inside a forked tool fiber at `step.ts:125-133` in `SessionStep.attempt` (`:73`). The code-map confirms the `step.ts:126` → `:91` link.
  7. `SessionStep.attempt` is called as `steps.attempt` at `session/runner/llm.ts:248`, inside `SessionRunner.runStep` (`:209`). `runStep` is called from the step loop at `:194`.
- Not verified: that `tools` at `model-request.ts:405` is the `Tool` snapshot. I inferred it from `input.tools` (`:242`) and the matching `definitions` argument. The code-map returned no callers for `tool.ts:263` or `model-request.ts:404`, because those calls go through interface types.

**Q8 — Tests that reach `Permission.reply`**
- The code-map `tests` command returned 0 for both `reply` and `assert`. It says it reports static links, not coverage, and it missed these. A grep for `.reply(` found them.
- `packages/core/test/permission.test.ts`, all calling the real service:
  - "resolves an asked permission once" (`:284`, reply at `:292`).
  - "defects when an asked permission is declined" (`:299`, reply "reject" at `:303`).
  - "stores and removes saved resources for a project" (`:317`, reply "always" at `:331`).
  - "skips pending auto-approval after always for configured deny" and "…for missing Session" (generated at `:349-350`, reply at `:377`).
  - The shell-scanner tests "`${fixture.name}: ${scenario.name}`" (`:560`, reply "once" at `:584`) and "…always allow from native/legacy…" (`:675`, replies at `:690` and `:709`).
- `packages/core/test/tool-shell.test.ts:282`: `runPermissionCommand` calls `permission.reply`, using `permissionIt` (`:165`), which does not replace the Permission node. It is called throughout the "ShellTool scanner permissions" tests (`:293` onward). I did not work out which of its callers pass non-empty reply lists.
- Not real calls: stubs named `reply` at `test/plugin/permission-assert.test.ts:29`, `test/plugin/fixture.ts:66`, `test/plugin/host.ts:114` and `test/fixture/policy.ts:43`. Those don't run `Permission.reply`.

**Q9 — What `Permission.reply` does (`permission.ts:265-325`)**
1. The whole body is uninterruptible (`:266`). It looks up the pending request by `requestID`. If none exists it fails with `NotFoundError` (`:268-269`).
2. It publishes `Permission.Event.Replied` (`:270-274`).
3. On "reject" (`:276-297`):
   - It fails the request's deferred with `CorrectedError` if a message was given, else `DeclinedError`, and removes it from pending (`:277-281`).
   - It does the same for every other pending request in the same session, publishing "reject" for each (`:282-295`). The comment says the feedback applies to the whole batch.
   - It then returns.
4. Otherwise, on "once" or "always":
   - On "always" with a non-empty `save`, it stores the rule with `saved.add` (`:299-305`).
   - It resolves the deferred and removes the request from pending (`:306-307`).
5. On "always" with `save`, it re-evaluates every other pending request across all sessions (`:310-311`). A session that is no longer found is skipped (`:312`). A request that now evaluates to "allow" is published as "always", resolved and removed (`:314-321`). Requests that still evaluate to ask or deny stay pending, which the tests at `:350-385` cover.
- A "reject" without a message becomes a defect inside `assert` (`:253`). A "reject" with a message stays a typed `CorrectedError`.

**Q10 — How the read and write tools differ in their permission checks**
- **Write** (`tool/plugin/write.ts`):
  - It declares `options.permission: "edit"` (`:59`).
  - It calls `access.authorizeExternal` (`:72`), which asks for `external_directory` only if the target is outside the location.
  - It computes a diff preview and calls `permission.assert` itself with action "edit", `resources: [target.resource]`, `save: ["*"]` and `metadata: { files: [preview] }` (`:77-86`). That happens before the write (`:87`).
- **Read** (`tool/plugin/read.ts`):
  - It declares no `permission` option (`:42`). `Tool.snapshot` falls back to the tool name "read" when deciding whether the tool is wholly disabled (`tool.ts:231`).
  - It never calls `permission.assert` directly. It calls `access.authorizeRead` (`:55`, and `:66` for the recovered filename).
  - `authorizeRead` (`file-access.ts:144-161`) checks `external_directory` first, except for a sibling recovery, which shares the directory approval (`:153`). It then asserts action "read" with `save: ["*"]` and no metadata (`:154-159`).
- The two tools use different actions ("edit" vs "read"). Write attaches a diff preview and read attaches none.