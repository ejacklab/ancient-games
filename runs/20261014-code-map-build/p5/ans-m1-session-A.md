# Answers to Q1–Q10 (opencode, `packages/core/src/session`, commit 6dc4d4e)

The code-map tool answered Q1, Q3 and Q7 (partly). It could not answer Q4, Q8 or most of Q6, so I filled those from grep and reading the files, and say so in each answer. I did not write the harness-guard criteria or deadline files, because you said not to change any file.

In the answers below, `core/` means `packages/core/`.

## Q1. Where SessionRunner is defined, and where `drain` is implemented
- **Service:** `core/src/session/runner/index.ts:42` declares `class Service extends Context.Service<…>()("@opencode/SessionRunner")`. Its `Interface` is at `index.ts:31-40`, with `drain` declared at `:33`. The `SessionRunner` namespace export is at `:1`.
- **Implementation of `drain`:** `core/src/session/runner/llm.ts:57`, which is `Effect.fn("SessionRunner.drain")` inside the layer started at `llm.ts:41`. The layer exposes it with `Service.of({ drain })` at `llm.ts:387`. The node is `SessionRunnerLLM.node` at `llm.ts:391`, registered at `core/src/instance.ts:108`.
- **Not the implementation:** `core/src/session/execution.ts:87` is SessionExecution's own `drain`, which calls the runner.
- **Tool:** `where SessionRunner.drain` returned both places and flagged the name as ambiguous. I picked `llm.ts:57` because `index.ts:33` declares it and the tool's `callers` output lists `llm.ts:57` as its implementation.

## Q2. The maximum-steps prompt
- **Defined:** the `MAX_STEPS_PROMPT` constant, `core/src/session/runner/max-steps.ts:1-16`.
- **Applied:** in `runStep`, `llm.ts:209`.
  - `llm.ts:226` sets `stepLimitReached = agent.info.steps !== undefined && step >= agent.info.steps`.
  - `llm.ts:240-242` appends `Message.assistant(MAX_STEPS_PROMPT)` to the transcript when the limit is reached.
  - `llm.ts:244` sets `toolChoice: "none"`.
- **Enforced in the attempt:** `core/src/session/runner/step.ts:92-93` returns `Tool.Error("Tools are disabled after the maximum agent steps")` if a tool is called anyway. `step.ts:281` forces `needsContinuation` to false.
- **Not established:** no code-map `find` for this question succeeded. My first call was rejected by the shell, so I located it with grep and by reading the files.

## Q3. What calls `SessionRunner.drain`
- **The only production call site:** `core/src/session/execution.ts:95-96`, `SessionRunner.Service.use((runner) => runner.drain({ sessionID, force, continuation, promotable }))`. Code-map `callers llm.ts:57` returned exactly this one. It found it through the injected `Service`, with the note "via implementation lookup".
- **What reaches that call site:**
  - SessionExecution's `drain` (`execution.ts:87`) calls itself on `Moved` and `Reloaded` (`:107-108`).
  - The `drain` option passed to `SessionRunCoordinator.make` (`execution.ts:117`) calls it.
  - The coordinator invokes that option at `core/src/session/run-coordinator.ts:75`.
  - The coordinator's entry points are `resume`, `wake` and `interrupt` (`execution.ts:150-173`).
- **Not a caller:** `core/src/session/move.ts:107` only resolves `SessionRunner.Service` to check availability. It never calls `drain`.
- **Test callers** (found by grep, because the tool's project covers `src` only):
  - `core/test/session-runner.test.ts`: `:443`, `:945`, `:989`, `:1342`, `:1474`, `:1502`, `:2177`, `:4131`, `:4155`, `:4260`, `:4277`, `:4298`, `:5215`.
  - `core/test/session-runner-recorded.test.ts:118`.
  - `session-move.test.ts:61`, `session-execution.test.ts:1364` and `location-activity.test.ts:46` only install stub Services. They are not callers.

## Q4. What calls `SessionStep.attempt`
- **The tool found nothing:** `callers SessionStep.attempt` said "no definition found", and `callers step.ts:73` said "empty". `attempt` is reached through the object returned by `SessionStep.make` (`step.ts:288`) and bound as `steps` at `llm.ts:53`, which the tool does not follow.
- **Callers found by grep and reading:**
  - `core/src/session/runner/llm.ts:248`, `steps.attempt({...})` inside `runStep`. This is the only call in `src`.
  - `core/test/session-step.test.ts:102`.
  - `core/script/benchmark-snapshot-session.ts:142`.
- **Limit:** this was text matching, so a call through some other alias would be missed.

## Q5. What `SessionStep.attempt` calls (`step.ts:73-286`)
Code-map `callees step.ts:73` listed the resolved ones, and I read the rest.
- **Snapshots:** `snapshots.capture()` (`:76`, `:237`; defined at `core/src/snapshot.ts:128`, with a no-op variant at `:230`) and `snapshots.files` (`:242`).
- **Event publisher:** `createLLMEventPublisher` (`:77`, defined at `publish-llm-event.ts:105`). Its methods are `publish`, `hasStarted`, `record`, `flush`, `streamed`, `startAssistant`, `failAssistant`, `failTool`, `failUnsettledTools`, `failIncompleteTools`, `publishStepFailure`, `toolExecution`, `progress` and `hasProviderError`. The tool resolved only `publish` (`:637`), `hasStarted` (`:651`) and `record` (`:653`).
- **Provider stream and tools:** `llm.stream` (`:107`, from `@opencode/ai`) and `input.prepared.executeTool` (`:94`), followed by `toolOutput.truncate` (`:127`).
- **Local helpers:** `classifyToolExits` (`:153`, defined at `:298`), `isInterruptedStream` (`:196`, defined at `:291`), `toSessionError` (`:181`, `:220`; defined at `core/src/session/to-session-error.ts:28`) and `SessionUsage.calculateCost` (`:247`; defined at `core/src/session/usage.ts:22`).
- **Callbacks supplied by the runner:**
  - `input.retry` (`:192`) → `retry.decide` at `llm.ts:255-263`.
  - `input.recoverOverflow` (`:159`) → `compaction.compact` at `llm.ts:265-270`.
  - `input.isLocationClosed` (`:210`, `:275`).
- **Events and errors:** `bus.publish(SessionEvent.Step.Ended)` (`:251`), `SessionRunnerRetry.isRetryable` (`:195`), and the constructors `AIError`, `InvalidProviderOutputError` and `StepFailedError`.
- **Limit:** the tool marks Effect, Stream and Fiber calls "outside the repository", and I did not expand those.

## Q6. Call chain down, from SessionExecution to a tool's own `execute`
The tool's `chain execution.ts:87` stopped at `SessionRunner.Service.use` (`execution.ts:95`), which it treats as unresolved. It followed only `store.get`. I traced the rest by reading.

1. `SessionExecution` `drain`, `execution.ts:87`, called from the coordinator at `:117`.
2. `runner.drain` through the Service, `execution.ts:95-96`, which lands in `SessionRunnerLLM` `drain`, `llm.ts:57`.
3. `runStep`, called at `llm.ts:194` and defined at `:209`.
4. `steps.attempt`, called at `llm.ts:248` and defined at `step.ts:73`.
5. The local `executeTool`, called at `step.ts:126` and defined at `:91`, which calls `input.prepared.executeTool` at `:94`.
6. `Prepared.executeTool`, `core/src/session/model-request.ts:404`, which calls `tools.execute(...)` at `:405`. `tools` is a `Tool.Snapshot` (`model-request.ts:77`, `:242`).
7. `Snapshot.execute`, `core/src/tool.ts:263`, which calls `executeTool` at `tool.ts:280`. That function is defined at `tool.ts:113`, with the span name `Tool.execute`. The `execute` code-mode tool takes a branch at `:277-278`.
8. `execute` in `core/src/tool/runtime.ts:29`, called from `tool.ts:119`.
9. `tool.execute(decoded, context)` at `runtime.ts:37`. This is the tool's own function. It is typed at `packages/schema/src/tool.ts:99`, and a concrete example is `core/src/tool/plugin/patch.ts:85`.

## Q7. Call chain up, from `SessionRunnerRetry.policy` to the session runner
`policy` is at `core/src/session/runner/retry.ts:64`. There are two paths up. The tool found the second one, and I added the first by reading.

- **A (the tool did not link this one up):**
  1. `policy` is called inside `make`, `retry.ts:94-96`.
  2. `make` is called from `runStep` at `llm.ts:212`.
  3. `runStep` is called from the runner's `drain` at `llm.ts:194`, which is `llm.ts:57`.
  4. Above that is `execution.ts:95`, as in Q3.
  - The decision it produces is used at `llm.ts:255-263` and `step.ts:192`.
- **B (from the tool):**
  1. `policy` is called in `deliver`, `core/src/session/compaction.ts:384`, at `:398`.
  2. `deliver` is called from `summarize` (`:272`, call at `:309`) and from `compactNatively` (`:324`, call at `:371`).
  3. Both are called from `compact` (`:205`, calls at `:232-233`).
  4. `compact` is reached through the service method at `compaction.ts:664`.
  5. That service method is called from `llm.ts:220` (`runStep`), `llm.ts:127` (manual compaction in `advanceToStep`) and `llm.ts:267` (`recoverOverflow`).
  6. All three sit under `drain`, `llm.ts:57`.

## Q8. Which tests reach `SessionRunnerRetry.policy`
- **Tool result:** 0 tests. `tsconfig.json` includes only `src` (`packages/core/tsconfig.json:16`), so tests are outside its program. `tsconfig.tests.json` also gave 0. This answer comes from grep and reading.
- **Direct calls to `policy`:**
  - `core/test/session-runner-retry.test.ts:29` (the two tests at `:36` and `:42`).
  - `core/test/plugin/provider-chatgpt.test.ts:301` and `:363`.
- **Through the real runner:** `runStep` calls `SessionRunnerRetry.make` at `llm.ts:212`, which calls `policy`, so any test that runs the real `SessionRunnerLLM` drain reaches it.
  - `core/test/session-runner.test.ts` builds that node at `:429` and `:486`. It has retry scenarios, for example `:5450-5469`, `:5565`, `:5580` and `:5991`.
  - `core/test/session-runner-recorded.test.ts` builds it at `:97` and `:148`. I did not check that it drives a retry.
- **Through compaction (`compaction.ts:398`):** `core/test/session-native-compaction.test.ts` builds `SessionCompaction.node` (`:39`) and registers a retry hook that asserts on retries (`:309-324`).
- **Not verified:** `session-compaction.test.ts:87` builds the compaction node, but I did not confirm it reaches `deliver`. `config/compaction.test.ts` builds the node, and I did not confirm it runs compaction. Other tests that build the full instance (`instance.ts:108`) were not enumerated.
- **Not reaching `policy`:** `aisdk.test.ts` and `session-error.test.ts` use only `isRetryable`. `session-step.test.ts` does not import `SessionRunnerRetry`.

## Q9. How `SessionStep.attempt` decides its outcome after the stream ends (`step.ts:143-283`)
1. **Cancelled before it started:** if the stream was interrupted before the start snapshot existed, it fails with that cause and records nothing (`:147-148`).
2. **Wait for tools:** otherwise it marks the stream as streamed (`:149`), interrupts tools if the stream was interrupted (`:150`), waits for the tool fibers (`:151-152`), and classifies the results into `{interrupted, declines, failure}` (`:153`, `:298-321`).
3. **Context overflow, no output yet:** if the provider rejected the request as too long, nothing was written, and `recoverOverflow` (compaction) succeeds, the outcome is `Compacted` (`:155-167`).
4. **Derive the failure:**
   - A successful stream whose finish reason is "unknown" becomes an `incomplete-stream` `AIError` (`:171-179`).
   - `llmFailure` is the stream's `AIError` or that synthetic one (`:180`).
   - `llmError` is its session form, unless the provider failure was already recorded (`:181`).
5. **Transport recovery:** if `recoverContinuation` is set, the transport recovery is `retry-full` or `rotate-and-retry-full`, and no output started, the outcome is `RecoverFull` (`:182-188`).
6. **Retry decision:** for a non-overflow failure, `input.retry(...)` is asked whether to retry, with the proposal `isRetryable(llmFailure) || (outputStarted && isInterruptedStream(llmFailure))` (`:189-199`). That call goes to `policy`.
7. **Retry before output:** if the decision is to retry and no output started, the outcome is `Retry` (`:200-204`).
8. **Settle:** otherwise it:
   - fails the assistant message with `llmError` (`:205`);
   - fails declined tools (`:207-215`);
   - computes `interrupted` and the tool failure, and fails the unsettled tools (`:216-224`);
   - fails the assistant with `STEP_INTERRUPTED` if interrupted (`:225`);
   - marks tools that never returned a result as `RESULT_MISSING` (`:227-232`);
   - publishes `Step.Failed` or `Step.Ended` with usage and a snapshot diff (`:234-261`).
9. **Return ladder (in order):**
   - `Continue` if a retry was decided, output started, there were no declines, and tools were not interrupted (`:263-271`).
   - Fail with the stream's cause if the stream failed (`:273`).
   - On a decline, `Completed{needsContinuation:true}` if the location is closed, otherwise interrupt (`:274-277`).
   - Fail with the tool or joined cause if tools were interrupted and failed (`:278-279`).
   - `StepFailedError` if `record.failure` is set (`:280`).
   - `OutputLimit` if the finish reason is `length` (`:282`).
   - Otherwise `Completed{needsContinuation}`, where `needsContinuation` is false when `toolChoice` is `none` (`:281`, `:283`).

## Q10. How the Retry and Continue outcomes differ
They have the same payload (`{error, decision}`, `step.ts:34-38`) and both pass through `retry.wait` in the runner. The differences are when they are produced and what happens next.

| | **Retry** | **Continue** |
|---|---|---|
| **Produced when** | A retry is decided and no output started (`step.ts:200-204`). | A retry is decided and output had already started, with no declines and no interrupted tools (`:263-271`). |
| **Step settlement** | Returns early. It only calls `startAssistant()` so the retry state shows on the existing assistant (`:201-203`). It never reaches `failAssistant` or the `Step.Failed`/`Step.Ended` publication. | Runs the whole settlement first. `failAssistant` (`:205`) sets the failure, `publishStepFailure` is called (`:249`), and the partial assistant message is durably failed. |
| **Runner reaction** (`llm.ts:275-289`) | Only `retry.wait`. | `retry.wait`, then publishes a `SessionEvent.Synthetic` with "The previous response was interrupted. Continue from where you left off…" (`llm.ts:35-36`, `:287`). |
| **Assistant identity** | Kept (`assistantMessageID` unchanged). | New (`llm.ts:288`). |

- **Shared retry accounting:** both draw from the same retry allowance. `core/test/session-runner.test.ts:5991` ("shares retry accounting and assistant identity across transparent retries and partial continuations") has the comment at `:6013`: "A transparent retry keeps the assistant identity; a partial continuation starts a new one."