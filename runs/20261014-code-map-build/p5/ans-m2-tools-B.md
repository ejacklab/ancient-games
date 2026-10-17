Answers to Q1–Q10 follow. All paths are relative to the repo root. I only read files and changed nothing. I did not run the `harness-guard` criteria or deadline commands from the hook: you limited me to Read, Grep and Glob and I had no shell. I did not read `@opencode/schema/permission`, so the `Rule`, `Reply` and `Request` shapes are inferred from how the code uses them.

## Q1. Rule evaluation, and what happens when nothing matches
- `evaluate` is at `packages/core/src/permission.ts:87-97`. It flattens the rulesets and takes `findLast`, so the last rule whose action and resource both match wins (`:89-91`).
- Matching uses `Wildcard.match` (`packages/core/src/util/wildcard.ts:3-14`). `*` becomes `.*`, `?` becomes `.`, and a trailing ` *` becomes optional.
- **When no rule matches**, it returns `{ action, resource: "*", effect: "ask" }` (`permission.ts:92-95`). The default is to ask.
- The service wraps this in `evaluateInput` (`permission.ts:173-189`):
  - Any denied resource short-circuits to deny, checked before saved approvals (`:175`, `:165-167`).
  - Saved approvals are appended as `allow` rules (`:148-156`, `:176`).
  - The effect is `ask` if any resource asks, otherwise `allow` (`:177-178`).
  - A plugin hook, `hooks.trigger("permission","evaluate")`, can then change the effect (`:179-188`).
- An agent that cannot be resolved falls back to deny-all (`missingAgentPermissions`, `:19`, `:162`).

## Q2. Where the Permission service is declared and implemented
- **Declared:**
  - The `Interface` (`close`, `ask`, `assert`, `reply`, `get`, `forSession`, `list`) is at `permission.ts:103-111`.
  - The service tag is `class Service extends Context.Service<…>()("@opencode/Permission")` at `:113`.
- **Implemented:**
  - The `layer` is at `:121-341`: `ask` at `:223-229`, `assert` at `:231-263`, `reply` at `:265-325`.
  - It is assembled with `Service.of({ ask, assert, reply, get, forSession, list, close })` at `:339`.
  - The node, with its dependencies, is at `:343-347`.
- The file re-exports itself as the `Permission` namespace (`:1`).
- Test stubs also implement the interface (`packages/core/test/plugin/fixture.ts:60-71`, `packages/core/test/lib/permission.ts:4-5`).

## Q3. What calls `Permission.assert`
Every receiver is the injected service, obtained by `yield* Permission.Service`.

| Caller | Line |
|---|---|
| `tool/mcp.ts` | `:51` (service at `:32`) |
| `tool/plugin/mcp-resource.ts` | `:36`, `:65` |
| `tool/plugin/write.ts` | `:78` |
| `tool/plugin/edit.ts` | `:275` |
| `tool/plugin/patch.ts` | `:196` |
| `tool/plugin/shell.ts` | `:138` |
| `tool/plugin/webfetch.ts` | `:124` |
| `tool/plugin/websearch.ts` | `:49` |
| `tool/plugin/subagent.ts` | `:139` |
| `tool/plugin/glob.ts` | `:68` |
| `tool/plugin/grep.ts` | `:87` |
| `tool/plugin/skill.ts` | `:51` |
| `tool/plugin/question.ts` | `:64` |
| `tool/plugin/opencode.ts` | `:192` |
| `file-access.ts` (shared helper) | `:135` (external directory), `:154` (read) |
| `plugin/host.ts` (plugin-facing `assert`) | `:439` |

- All paths in the table are under `packages/core/src/`.
- `permission.ts` itself does not call `assert`.
- A grep for point-free uses of `assert` found nothing else in `packages/core/src`.
- The read tool reaches `assert` only through `FileAccess` (`read.ts:55`, `read.ts:66`).
- I did not check which other tools also go through `FileAccess`.
- I did not confirm that each of these call sites is reachable at runtime.

## Q4. What calls the tool runtime's `execute` (`tool/runtime.ts:29`)
- In `src`, the only caller is `executeTool`, in `packages/core/src/tool.ts:119`. It is imported at `tool.ts:18` and defined as `Effect.fn("Tool.execute")` at `:113`.
- `executeTool` is itself called from `tool.ts:242` (code-mode inner tools), `:278` (the code-mode `execute` tool) and `:280` (a direct tool).
- `codemode/tool.ts:14` and `plugin/tool-input-repair.ts:5` import `runtime.ts` but take only `definition` and `normalizedName`, not `execute`.
- Tests that call it directly are `packages/core/test/tool-schema.test.ts:10`, `packages/core/test/tool-execute.test.ts:4` and `packages/core/test/plugin/module.test.ts:15`.
- My search was for the import strings `tool/runtime` and `./runtime.js` across `packages/`. I did not look for dynamic imports.

## Q5. What `Permission.assert` calls (`permission.ts:231-263`)
- If the service is closed, it dies with `DeclinedError` (`:233`).
- `evaluateInput` (`:234`, defined at `:173`) then calls:
  - `configured` (`:174`, defined at `:158`), which calls `sessions.get` (`:159`), `agents.resolve` (`:161`) and `merge` (`:162`).
  - `denied`, which calls `evaluate` (`:175`, `:166`).
  - `savedRules`, which calls `saved.list` (`:176`, `:149`).
  - `evaluate` again (`:177`).
  - `hooks.trigger("permission","evaluate")` (`:179`).
- If the effect is `deny`, it fails with `BlockedError`, using `relevant()` to select the rules (`:237-244`).
- If the effect is `allow`, it returns (`:245`).
- If the effect is `ask`:
  - `request()` and `create()` run at `:246`.
  - `create` records the request in `pending` (`:215`) and calls `bus.publish(Permission.Event.Asked)` (`:216-218`).
  - It then does `Deferred.await` (`:247`).
  - A `DeclinedError` is converted to a defect with `Effect.die` (`:253`).
  - The pending entry is deleted afterward (`:254-258`).

## Q6. Call chain down, from the write tool to agent resolution
1. `write.ts:78`: `permission.assert({…, agent: context.agent})`. The tool's `execute` closure starts at `:64`.
2. `permission.ts:231`: `assert`.
3. `permission.ts:234`: `evaluateInput` (defined at `:173`).
4. `permission.ts:174`: `configured` (defined at `:158`).
5. `permission.ts:161`: `agents.resolve(agentID ?? session.agent)`.
6. `agent.ts:94-97`: `resolve` returns `state.get().agents.get(ID.make(id))` when an id is given, otherwise `selectedDefault()` (`:76-86`).

- The write tool reaches the same chain a second time. `write.ts:72` calls `access.authorizeExternal`, which calls `file-access.ts:135`, which calls `permission.assert`. This only fires when the target is external (`file-access.ts:134`).
- If the agent is not found, the permissions fall back to deny-all (`permission.ts:162`).

## Q7. Call chain up, from `Permission.assert` in the write tool to the session step
1. `write.ts:78`: the `assert` call.
2. `tool/runtime.ts:37`: `tool.execute(decoded, context)`.
3. `tool.ts:119`: `executeTool`, called at `tool.ts:280` from `Snapshot.execute` (`:263`) after the `beforeExecute` hook (`:271`).
4. `session/model-request.ts:405`: `tools.execute({...call, definitions: hooked})`, inside `Prepared.executeTool` (`:404`). It recovers declines as failures at `:406-417`.
5. `session/runner/step.ts:94`: `input.prepared.executeTool(...)`, inside the local `executeTool` (`:91`).
6. `step.ts:126`: this is run for each non-provider-executed `tool-call` event in `SessionStep.attempt` (`:73`, event check at `:122`).
7. `session/runner/llm.ts:248`: `steps.attempt({…, prepared})`. The `prepared` value comes from `context.request.primary` at `llm.ts:234`.

- The tool snapshot used above comes from `session/context.ts:134` (`registry.snapshot(permissions)`) and is passed in at `llm.ts:238`.
- I did not trace what calls the `llm.ts` loop above line 248.

## Q8. Which tests reach `Permission.reply`
These use the real service:
- `packages/core/test/permission.test.ts` builds the real `Permission.node` (`:27-32`). It calls `reply` at `:292` (once), `:303` (reject), `:331` and `:377` (always), and also at `:584`, `:690` and `:709`.
- `packages/core/test/tool-shell.test.ts:282`, in `runPermissionCommand` (`:260-290`). It looks real because it reads `Asked` events from the bus and a real `PermissionSaved` (`:270`, `:301`), but I did not read its layer setup.
- `packages/server/test/session-instances.test.ts:317-320` posts `/permission/:id/reply` and expects 204. This goes through the handler at `packages/server/src/handlers/permission.ts:77-82`, which calls `permission.reply` at `:81`, and the test then checks the request is gone (`:328`).
- The 404 case at `session-instances.test.ts:297-300` is probably rejected by `requireOwnedRequest` before `reply` runs. I did not read that function.

These do not reach the real `reply`:
- Stubs and mocks: `packages/core/test/plugin/fixture.ts:66`, `packages/core/test/fixture/policy.ts:43`, `packages/core/test/plugin/host.ts:114`, `packages/core/test/lib/permission.ts` (used by `tool-write.test.ts:44`), and `packages/core/test/plugin/permission-assert.test.ts:16-36`.
- Client-side tests that talk to a fake HTTP server: `packages/cli/test/acp/permission.test.ts:156` and `packages/tui/test/cli/tui/data.test.tsx:2441`, `:2481`.
- I found no test calling the plugin host's `reply` (`plugin/host.ts:427`).

## Q9. What `Permission.reply` does (`permission.ts:265-325`)
1. The whole body runs uninterruptibly (`:266`).
2. It looks up the pending request. If it is missing, it fails with `NotFoundError` (`:268-269`).
3. It publishes `Replied` (`:270-274`).
4. **Reject** (`:276-297`):
   - It fails the deferred with `CorrectedError{feedback}` if a message was given, otherwise `DeclinedError` (`:277-280`).
   - It deletes the entry (`:281`).
   - It does the same for every other pending request in the same session: publish `Replied` with reject, fail with the same error, delete (`:282-295`). The comment at `:289` says feedback applies to the whole batch.
   - It then returns.
5. **Once or always:**
   - If the reply is `always` and the request has `save` entries, it calls `saved.add` (`:299-305`).
   - It then succeeds the deferred and deletes the entry (`:306-307`).
6. If the reply is not `always`, or there is nothing to save, it returns (`:308`).
7. **Always with saved entries:**
   - It re-runs `evaluateInput` on every remaining pending request, in any session, using that request's agent (`:310-313`).
   - A session that no longer exists is skipped (`:312`).
   - A request is auto-approved only if its effect is now `allow` (`:314`). Auto-approval publishes `Replied: always`, succeeds the deferred and deletes the entry (`:315-321`).

On the `assert` side, a `DeclinedError` becomes a defect (`:253`) and a `CorrectedError` stays typed. The reply literals `once`, `always` and `reject` come from the code and tests, since I did not read the schema.

## Q10. How the read and write tools differ in their permission checks
**Same:**
- Both check `external_directory` first, then their own action.
- Both pass `save: ["*"]` (`write.ts:81`, `file-access.ts:157`).

**Different:**
- **Gating name.** Write sets `options.permission: "edit"` (`write.ts:59`). Read sets only `{ codemode: false }` (`read.ts:42`). `tool.ts:231` uses `options.permission ?? name`, so write is gated as `edit` and read as `read`.
- **Action.** Write asserts `edit` directly in the tool (`write.ts:78-86`). Read has no `assert` of its own and calls `access.authorizeRead` (`read.ts:55`), which asserts `read` (`file-access.ts:154-159`).
- **External check.** Write always calls `authorizeExternal([target])` (`write.ts:72`). Read's external check lives inside `authorizeRead` (`file-access.ts:153`). It is skipped for the filename-recovery retry when the sibling file is in the same directory (`read.ts:66`, `file-access.ts:150-153`). Write has no such path.
- **Metadata.** Write sends `metadata: { files: [preview] }`, a diff preview (`write.ts:77`, `:82`). Read sends no metadata.
- **Order.** Write reads the current file contents (`write.ts:73`) to build the preview before asking for `edit`. Nothing is written before the check passes (`write.ts:87`). Read asks before reading.
- **Error wrapping.** Write wraps every error as `ToolFailure("Unable to write …")` (`write.ts:95`). Read passes a `ToolFailure` through unchanged and maps other errors to specific messages (`read.ts:121-131`).