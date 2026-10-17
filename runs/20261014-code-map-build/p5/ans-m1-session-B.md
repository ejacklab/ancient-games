Everything below comes from reading and grepping at commit 6dc4d4e. I ran no tests, so "reach" in Q8 means static reachability. All paths are relative to the repository root, and `core/` abbreviates `packages/core/`.

I did not run the harness-guard criteria and deadline commands. They need Bash, and you limited me to Read, Grep and Glob.

## Q1. Where SessionRunner is defined and where `drain` is implemented
- **Service:** it is defined at `core/src/session/runner/index.ts:42`. The class is `Service extends Context.Service<…>()("@opencode/SessionRunner")`. The namespace export is at `index.ts:1`.
- **Interface:** `Interface.drain` is declared at `index.ts:31-40`. It takes `{sessionID, force, continuation?, promotable?}` and returns `Effect<DrainResult, RunError>`.
- **Implementation:** the only one is `const drain = Effect.fn("SessionRunner.drain")` at `core/src/session/runner/llm.ts:57`.
  - It is provided by `Service.of({ drain })` at `llm.ts:387`.
  - It sits inside `Layer.effect(Service, …)` (`llm.ts:41-43`).
  - The node is `SessionRunnerLLM.node` (`llm.ts:391`), wired in at `core/src/instance.ts:108`.
  - Test stubs also implement the interface (see Q3).

## Q2. The maximum-steps prompt
- **Defined:** the `MAX_STEPS_PROMPT` constant is at `core/src/session/runner/max-steps.ts:1-16`. It is imported at `llm.ts:33`.
- **Applied:** it is applied in `runStep` (`llm.ts:209`).
  - `stepLimitReached` is `loaded.agent.info.steps !== undefined && step >= loaded.agent.info.steps` (`llm.ts:226`).
  - When it is true, `Message.assistant(MAX_STEPS_PROMPT)` is appended to the transcript (`llm.ts:240-241`).
  - `toolChoice` is also set to `"none"` (`llm.ts:244`).
- **Enforced in the attempt:** `core/src/session/runner/step.ts:92-93` makes `executeTool` return `Tool.Error("Tools are disabled after the maximum agent steps")` when `toolChoice` is `none`. `step.ts:281` forces `needsContinuation` to false in the same case.
- **Not established:** I did not trace how `agent.info.steps` is set. `core/src/config/plugin/agent.ts:120` and `core/src/v1/config/agent.ts:59` look relevant, but I did not read them.

## Q3. What calls `SessionRunner.drain`
- **Production, one call site:** `core/src/session/execution.ts:95-96`. It is `SessionRunner.Service.use((runner) => runner.drain({sessionID, force, continuation, promotable}))`, inside the local `drain` at `execution.ts:87`.
  - It runs under `instances.provide(session)` (`execution.ts:98`).
  - It re-calls itself for `Moved` and `Reloaded` results (`execution.ts:107-108`).
- **Who reaches that local `drain`:** `execution.ts:117` passes it as the coordinator's `drain` option. `core/src/session/run-coordinator.ts:75` (`loop`) calls it. The coordinator is exposed as `resume` and `wake` (`execution.ts:171-172`).
- **Not a call:** `core/src/session/move.ts:107` only obtains `SessionRunner.Service` as a probe. It never calls `drain`.
- **Tests:**
  - `core/test/session-runner.test.ts:443` reimplements the execution drain loop. Direct calls are at lines 945, 989, 1342, 1474, 1502, 2177, 4131, 4155, 4260, 4277, 4298 and 5215.
  - `core/test/session-runner-recorded.test.ts:118` also calls it.
  - Stubs that implement `drain` without calling it: `core/test/session-move.test.ts:61`, `core/test/session-execution.test.ts:1364` and `core/test/location-activity.test.ts:46`.
- **Limit:** I searched `packages/` only, not the rest of the repository.

## Q4. What calls `SessionStep.attempt`
- **Production:** `core/src/session/runner/llm.ts:248` (`steps.attempt({...})` in `runStep`). `steps` comes from `SessionStep.make` at `llm.ts:53`.
- **Test:** `core/test/session-step.test.ts:102`, with `steps` built from `SessionStep.make` at line 52.
- **Script:** `core/script/benchmark-snapshot-session.ts:142`, with `steps` from `SessionStep.make` at line 125.

## Q5. What `SessionStep.attempt` calls
It is defined at `step.ts:73`. In rough order:
- **Snapshots:** `snapshots.capture()` (`:76`, `:237`) and `snapshots.files` (`:243`).
- **Publisher:** `createLLMEventPublisher` (`:77`) and its methods: `publish`, `streamed`, `flush`, `startAssistant`, `failAssistant`, `failTool`, `failUnsettledTools`, `failIncompleteTools`, `publishStepFailure`, `toolExecution`, `progress` and `record`.
- **Model stream:** `llm.stream(...)` (`:107`).
- **Tools:** `input.prepared.executeTool` (`:94`) then `toolOutput.truncate` (`:127`).
- **Injected callbacks:** `input.recoverOverflow` (`:159`) and `input.retry` (`:192`).
- **Helpers:**
  - `isContextOverflowFailure` (`:114`, `:158`)
  - `SessionRunnerRetry.isRetryable` (`:195`)
  - `isInterruptedStream` (`:196`)
  - `classifyToolExits` (`:153`)
  - `toSessionError` (`:130`, `:181`, `:220`)
  - `SessionUsage.calculateCost` (`:247`)
- **Events and errors:** `bus.publish(SessionEvent.Step.Ended)` (`:251`) and `new StepFailedError` (`:280`).

## Q6. Call chain down, from SessionExecution to a tool's own `execute`
1. `execution.ts:87` calls `runner.drain` at `execution.ts:95-96`.
2. `llm.ts:57` runs `runStep(next.context, step)` (`llm.ts:194`, defined at `:209`).
3. That calls `steps.attempt` (`llm.ts:248`).
4. Inside it, `step.ts:94` calls `input.prepared.executeTool`. The local wrapper is at `step.ts:91`, and the call is forked at `step.ts:125-133`.
5. `prepared.executeTool` is `core/src/session/model-request.ts:404`, which calls `tools.execute(...)` (`:405`).
   - `tools` is `input.tools` (`model-request.ts:242`).
   - That is `loaded.tools` (`llm.ts:236`), which comes from `registry.snapshot(permissions)` (`core/src/session/context.ts:134`). `registry` is `Tool.Service` (`context.ts:91`).
6. `Snapshot.execute` at `core/src/tool.ts:263` calls `executeTool(tool, …)` (`tool.ts:280`). For the code-mode `execute` tool, it calls `executeTool(codeModeTool, …)` (`tool.ts:278`) instead.
7. `Tool.execute` (`tool.ts:113`) calls `execute(tool, input, context)` (`tool.ts:119`).
8. `core/src/tool/runtime.ts:29` calls **`tool.execute(decoded, context)`** (`runtime.ts:37`). This is the tool's own function.

On the code-mode path, `core/src/codemode/tool.ts:235` wraps each inner tool's `execute`. I did not follow that further.

## Q7. Call chain up, from `SessionRunnerRetry.policy` to the session runner
`policy` is defined at `core/src/session/runner/retry.ts:64`. It has two callers.

- **Chain A, the step retry:**
  1. `retry.ts:96` (`SessionRunnerRetry.make`) calls `policy`.
  2. `llm.ts:212` (`runStep`) calls `make`.
  3. `llm.ts:194` (`drain`) calls `runStep`.
  4. `drain` is the runner's implementation (`llm.ts:387`).
  - The returned `decide` is used at `llm.ts:256`, passed as `input.retry`. `step.ts:192` invokes it.
- **Chain B, compaction:**
  1. `core/src/session/compaction.ts:398` (`deliver`) calls `policy` directly.
  2. `compaction.ts:309` and `:371` call `deliver` from `compact` (`:205`).
  3. `llm.ts:220` and `llm.ts:127` call `compaction.compact` from `runStep` and `drain`.

## Q8. Which tests reach `SessionRunnerRetry.policy`
- **Direct calls:**
  - `core/test/session-runner-retry.test.ts:29` (tests at `:36` and `:42`).
  - `core/test/plugin/provider-chatgpt.test.ts:301` and `:363`.
- **Through the real runner (Chain A):** `core/test/session-runner.test.ts` builds the real `SessionRunnerLLM.node` (`:429`).
  - Retry scenarios include `:5448-5474`, `:5524`, `:5542`, `:5565`, `:5580`, `:6054` and `:6094`.
  - `:6135` ("does not retry non-eligible…") reaches it too. `input.retry` is called whenever there is an LLM failure that is not a context overflow (`step.ts:189-199`), eligible or not.
- **Through compaction (Chain B):**
  - `session-runner.test.ts:2654`, `:2700` and `:2756`.
  - `core/test/session-native-compaction.test.ts:307-326`, which uses the real `SessionCompaction.node` (`:39`).
- **Does not reach it:** `core/test/session-step.test.ts:118-119` stubs `retry`. `core/test/plugin/provider-snowflake-cortex.test.ts:156` triggers the hook only.
- **Not established:** whether `session-runner-recorded.test.ts` ever hits a retry. It builds the real runner (`:97`), but I did not check for a failing request.

## Q9. How `SessionStep.attempt` decides its outcome after the stream ends
This is `step.ts:141-283`, in order. It is not one decision.
1. It captures the stream `Exit` (`:143`), plus `streamFailure` and `streamInterrupted` (`:144-145`).
2. If the stream was interrupted before the start snapshot existed, it fails with the stream's cause and records nothing (`:147-148`).
3. It awaits the tool fibers and classifies their exits (`:149-153`).
4. **Compacted:** if no output has started, the failure is a context overflow, and `recoverOverflow` returns true, it returns `Compacted` (`:156-167`).
5. It then publishes any held overflow failure and builds `llmFailure`. An "unknown" finish on a successful stream becomes an `incomplete-stream` AIError (`:169-181`).
6. **RecoverFull:** this needs `recoverContinuation`, a Transport failure with `retry-full` or `rotate-and-retry-full`, and no output started (`:182-188`).
7. It asks `input.retry`, which is the runner's `retry.decide`. The proposed value is `isRetryable(llmFailure) || (outputStarted && isInterruptedStream(llmFailure))` (`:189-199`).
8. **Retry:** if the decision is retry and no output has started, it starts the assistant and returns `Retry` (`:200-204`).
9. Otherwise it settles durable state: it fails the assistant, fails declined, interrupted and missing-result tools, and publishes the step failure or `Step.Ended` (`:205-261`).
10. **Continue:** if the decision was retry, output had started, and there were no declines and no tool interrupt, it returns `Continue` (`:263-271`).
11. These cases fail or interrupt instead of returning an `Outcome`:
    - a stream failure (`:273`)
    - a tool decline: `Completed({needsContinuation: true})` if the location closed, otherwise `Effect.interrupt` (`:274-277`)
    - a tool defect or interrupt (`:278-279`)
    - a recorded failure, which raises `StepFailedError` (`:280`)
12. **Completed or OutputLimit:** `needsContinuation` is `toolChoice !== "none" && record.needsContinuation` (`:281`). A `length` finish gives `OutputLimit` (`:282`). Anything else gives `Completed` (`:283`).

`publisher.record()` builds a fresh object on each call (`publish-llm-event.ts:653`). That is why `recorded` at `:170` and `record` at `:234` can differ.

## Q10. How Retry and Continue differ
- **Shape:** the two have identical payloads, `{error, decision}` (`step.ts:34-38`).
- **When each is returned:**
  - `Retry` is returned before any output, at `step.ts:200-204`.
  - `Continue` is returned after output has started, at `step.ts:263-271`.
- **What the attempt does first:**
  - `Retry` only calls `startAssistant` and returns, so nothing is settled.
  - `Continue` comes after `failAssistant`, tool settlement and `Step.Ended` or the step failure (`:205-261`). The partial output is persisted.
- **What the runner does next (`llm.ts:275-289`):**
  - `Retry` only runs `retry.wait` (`:275-279`). It keeps the same `assistantMessageID` and resends the same request.
  - `Continue` runs `retry.wait`, publishes a `SessionEvent.Synthetic` with `CONTINUE_AFTER_INCOMPLETE_STREAM` (`:287`, text at `:35-36`), and creates a new `assistantMessageID` (`:288`).
- **Shared accounting:** both go through the one `retry` object per `runStep` (`llm.ts:212`), so they use the same retry schedule.
- **Test evidence:** `session-runner.test.ts:6013` has the comment "A transparent retry keeps the assistant identity; a partial continuation starts a new one". The test at `:5991` is titled "shares retry accounting and assistant identity across transparent retries and partial continuations".