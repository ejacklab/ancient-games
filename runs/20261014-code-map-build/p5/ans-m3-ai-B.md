All ten answers are below, with paths relative to the repository root. I only read and searched; no files were changed and no tests were run. I did not run the harness-guard criteria and deadline commands the hook suggested, because you limited me to Read, Grep and Glob and told me not to change any file.

## Q1 — Where LLMClient is defined
- The service class is `LLMClientService extends Context.Service<…>()("@opencode/LLMClient")` at `packages/ai/src/route/client.ts:261`. The aliases `Service` are at `:262-263`, and its interface (`compact`, `stream`, `generate`) is at `:177-181`.
- The live layer is `export const layer: Layer.Layer<Service, never, RequestExecutor.Service>` at `packages/ai/src/route/client.ts:657-685`. It builds `Service.of({ stream, generate: generateWith(stream), compact })` at `:679-683`.
- The `LLMClient` namespace object bundling `Service`, `layer`, `stream`, `generate`, `compact` and `canCompact` is at `client.ts:689-696`. It is re-exported at `packages/ai/src/route/index.ts:1` and `packages/ai/src/index.ts:2`.
- `packages/ai/src/testing.ts:224-229` is a second, test-only provider of the same tag.

## Q2 — Anthropic provider ID, base URL and auth
- **ID:** `ProviderID.make("anthropic")` at `packages/ai/src/providers/anthropic.ts:13`. The route also hard-codes `provider: "anthropic"` at `packages/ai/src/protocols/anthropic-messages.ts:1665`.
- **Default base URL:** `DEFAULT_BASE_URL = "https://api.anthropic.com/v1"` at `anthropic-messages.ts:37`. It is applied at `providers/anthropic.ts:44` (`baseURL ?? AnthropicMessages.DEFAULT_BASE_URL`) and in the route endpoint at `anthropic-messages.ts:1668-1670`.
- **API-key auth:** `providers/anthropic.ts:32-37`. It uses an explicit `auth` if given. Otherwise it takes the `apiKey` option, falls back to the `ANTHROPIC_API_KEY` config, and sends it as the `x-api-key` header.
- **Auth-token alternative:** `Auth.bearer(authToken)` at `anthropic.ts:65`. Combining `apiKey` and `authToken` throws at `:59-63`.
- The route's own default is `Auth.none` (`anthropic-messages.ts:1671`). The provider overrides it through `AnthropicCompatible.configure` (`anthropic.ts:41-46`; `anthropic-compatible.ts:47-52`).

## Q3 — What uses the LLMClient service
**Inside `packages/ai/src`:**
- `route/client.ts:618-655` has static accessors (`stream`, `generate`, `compact`, `streamRequest`) that do `yield* Service`.
- `llm.ts:45` and `:54` (`LLM.generate`/`LLM.stream`) call them, and `llm.ts:132` is `generateObject`'s call.
- `ai-client.ts:12` merges `LLMClient.layer` into the combined `layerWith`.
- `promise.ts:68` builds its runtime on `AIClient.layerWith`, so its `llm.generate`/`llm.stream` (`:139-142`) reach the service that way.
- `testing.ts:227` and `:248-250` provide `LLMClient.Service` as a test double.

**Outside the module, in `packages/core/src` (each does `yield* LLMClient.Service`):**
- `session/runner/step.ts:69`, which calls `llm.stream` at `:107`.
- `session/compaction.ts:189`, which calls `llm.compact` (trigger) at `:359` and `llm.stream` at `:511`.
- `session/title.ts:43`, which calls `llm.stream` at `:74`.
- `session/generate.ts:32`, which calls `llm.generate` at `:69`.
- `generate.ts:36` and `session.ts:250`.
- The live layer is registered at `effect/app-node-platform.ts:27`.

I did not read the surrounding logic in `generate.ts`, `session.ts` or `plugin/internal.ts`.

## Q4 — What calls `prepareRequest`
`prepareRequest` is private, defined at `packages/ai/src/route/client.ts:555`. A grep across `packages` finds three call sites, all in that file:
- `compile` at `:575`.
- The layer's `compact`, trigger branch, at `:673`.
- The layer's `compact`, endpoint branch, at `:675`.

`compile` (`:574`) is called by `compileRequest` (`:591`) and `streamRequestWith` (`:605`).

## Q5 — What `prepareRequest` calls
`client.ts:555-572`, in order:
1. `resolveRequestOptions` (`:556`, defined `:265-280`). It calls `normalizeToolHistory`, `LLMRequest.update`, and `mergeGenerationOptions`, `mergeProviderOptions` and `mergeHttpOptions` over the route, model and request defaults.
2. `LLMRequest.update`, `LLMRequest.input` and `sanitizeSurrogates` (`:557`).
3. A local `dedupe` of tools (`:559-562`).
4. `ToolSchemaProjection.tools` (`:565`).
5. `applyEffortUpdates` (`:564`), then `applyCachePolicy` (`:563`).
6. `resolved.model.route.headers?.(...)` (`:568`).
7. `mergeHttpOptions` with `new HttpOptions` (`:571`).

I did not open the implementations of the imported helpers.

## Q6 — Call chain down, from the layer's `stream` to protocol parsing
This is the Anthropic route.
1. `layer` sets `stream = streamRequestWith({ http: executor })` (`client.ts:661`) and exposes it at `:680`.
2. `streamRequestWith` (`:602-608`) calls `compile` (`:605`), then `route.streamPrepared` (`:606`).
3. `compile` (`:574-587`) calls `prepareRequest`, then `route.body.from` (`:578`). That is the protocol's body builder, `fromRequest` (`anthropic-messages.ts:1599`). It then calls `route.prepareTransport` (`:579`), which runs `transport.prepare` (`client.ts:413-422`).
4. The Anthropic `prepare` adds beta headers (`anthropic-messages.ts:1622-1640`). It delegates to `httpJson.prepare` (`route/transport/http.ts:85-99`), which calls `jsonRequestParts` (`:52-70`) to render the URL and apply auth.
5. `streamPrepared` (`client.ts:423`) calls `transport.execute` (`:426`). That is `httpJson.execute` (`http.ts:100-141`), which calls `runtime.http.execute` (`:116`) and then `framing.frame` (`:125`).
6. The Anthropic framing is `Framing.sseEvents(SSE_EVENTS)` (`anthropic-messages.ts:54`), which runs `sseFraming` (`route/framing.ts:36-78`).
7. Each frame goes through `decodeEvent` (`client.ts:361-372`, used at `:447`). That decodes `Protocol.jsonEvent(AnthropicEvent)` (`anthropic-messages.ts:1602`; `route/protocol.ts:86`).
8. `protocol.stream.initial(request)` (`client.ts:458`) is `anthropic-messages.ts:1603-1610`. `protocol.stream.step(state, event)` (`client.ts:461`) is `step` at `anthropic-messages.ts:1529`.
9. `step` dispatches to `onMessageStart`, `onContentBlockStart`, `onContentBlockDelta` (`:1318`), `onContentBlockStop` (`:1386`), `onMessageDelta` (`:1421`), `onMessageStop` (`:1457`) and `onError` (`:1494`).
10. The Anthropic protocol sets no `terminal` or `onHalt` (`:1595-1614`), so `client.ts:455` and `:474` skip those branches.

## Q7 — Call chain up, from `requireTerminalEvent` to the session step
1. `requireTerminalEvent` (`client.ts:341`) is called only at `client.ts:484`, inside `streamPrepared` (`:423-501`).
2. `streamPrepared` is called at `client.ts:606` from `streamRequestWith`. That is the `stream` the layer exposes (`:661`, `:680`).
3. The step reaches it through `llm = yield* LLMClient.Service` (`packages/core/src/session/runner/step.ts:69`) and `llm.stream(...)` (`step.ts:107`), inside `SessionStep.attempt` (`:73`).
4. `SessionRunner.runStep` calls `steps.attempt(...)` (`packages/core/src/session/runner/llm.ts:248`; `runStep` is defined at `:209`).
5. `SessionRunner.drain` calls `runStep` (`llm.ts:194`; `drain` is defined at `:57`).

`streamPrepared` has one other caller, `packages/ai/src/protocols/utils/responses-checkpoint.ts:113`, used by trigger compaction. `packages/core/src/aisdk.ts:412` defines its own `streamPrepared`. I did not trace either further.

## Q8 — Which tests reach `compileRequest`
- `compileRequest` is `client.ts:590`, marked "@internal Test-only projection… not exported from package barrels". `route/index.ts` does not export it. It is reachable only through the `./*` wildcard export in `packages/ai/package.json:20`.
- A grep for `compileRequest` finds no use in `packages/ai/src` besides its definition, so only tests call it.
- By direct import, **57 test files** reach it: 53 in `packages/ai/test` and 4 in `packages/core/test` (`session-runner.test.ts:21`, `aisdk.test.ts:25`, `plugin/provider-chatgpt.test.ts:7`, `model-resolver.test.ts:4`).
- The dedicated file is `packages/ai/test/compile.test.ts` (import at `:15`, calls at `:65`, `:94`, `:119`, `:173`, `:458`).
- The other files in `packages/ai/test` are `adapter.test.ts`, `cache-policy.test.ts`, `effort-updates.test.ts`, `tool-schema-projection.test.ts` and about 45 under `test/provider/`. Examples are `anthropic-messages.test.ts`, `openai-chat.test.ts`, `openai-responses.test.ts` and `bedrock-converse.test.ts`.
- That count comes from a grep of the import lines. I did not run the tests.
- Tests that call `LLMClient.generate` or `stream` (for example `compile.test.ts:192`) reach the private `compile`, but not `compileRequest`.

## Q9 — How `generateObject` produces a typed object
`packages/ai/src/llm.ts:168-196`, with the core in `runGenerateObject` (`:123-154`).
1. **Input mode decision (`:175`).** If `options` has `schema` (an Effect schema), `makeTool({ parameters: schema, success: Schema.Unknown, execute: () => Effect.void })` is built (`:177-184`). Otherwise it uses `jsonSchema` (raw JSON Schema), and `.object` is `unknown` (`:187-195`; doc at `:161-166`).
2. **Synthetic tool.** `runGenerateObject` builds the request with `request(options)` (`:127`). It forces a tool named `generate_object` via `toDefinitions` and `ToolChoice.named` (`:128-131`). No provider-native JSON mode is used (`:156-160`).
3. **Call.** `LLMClient.generate(generateRequest)` (`:132`).
4. **Decision: tool call present?** It looks for a `toolCall` event named `generate_object` in `response.toolCalls` (`:133-135`). If none is found, it fails with `AIError(InvalidProviderOutputError)` (`:136-141`).
5. **Decode.** `tool._decode(call.input)` (`:142`). For typed mode, `_decode` is `Schema.decodeUnknownEffect(parameters)` (`tool.ts:196`). For dynamic mode it is `Effect.succeed` (`tool.ts:176`), so the caller validates. A decode failure becomes `AIError(InvalidProviderOutputError)` (`llm.ts:143-151`).
6. **Result.** `new GenerateObjectResponse(object, response)` (`:153`), which exposes `.object`, `.events` and `.usage` (`:95-108`).

## Q10 — Anthropic versus OpenAI: routes and auth
**Routes**
- Anthropic has one route: `routes = [AnthropicMessages.route]` (`providers/anthropic.ts:15`). It is HTTP JSON over SSE, endpoint `/messages?beta=true` when the provider is `"anthropic"` (`anthropic-messages.ts:1668`). It sets the `anthropic-version: 2023-06-01` header (`:1673`). Its transport adds `anthropic-beta` headers (`:1616-1661`). It has no `compact` operations (`:1663-1674`).
- OpenAI has two routes: `routes = [OpenAIResponses.route, OpenAIChat.route]` (`providers/openai.ts:27`).
- The default model is Responses (`openai.ts:124`, `model: responses`). Chat is available as `.chat` (`:126`).
- The Responses route is id `openai-responses`, path `/responses` (`open-responses.ts:30`). It uses a WebSocket-capable channel transport, with HTTP fallback when no WebSocket is offered or enabled (`openai-responses.ts:309-316`; `open-responses-channel.ts:138-216`). It has both `compact.endpoint` and `compact.trigger` (`openai-responses.ts:319-322`). Its defaults are `store: false` and `include: ["reasoning.encrypted_content"]` (`:330`).
- The Chat route is id `openai-chat`, path `/chat/completions`. It is HTTP SSE with `[DONE]` framing (`openai-chat.ts:35`, `:1309-1319`).
- OpenAI also exposes image, speech and transcription factories (`openai.ts:118-120`).

**Auth**
- Both routes default to `Auth.none` (`anthropic-messages.ts:1671`, `openai-responses.ts:307`, `openai-chat.ts:1318`). Each provider facade overrides it, and both accept an explicit `auth`.
- Anthropic sends an `x-api-key` header from the `apiKey` option or the `ANTHROPIC_API_KEY` config (`anthropic.ts:32-37`). It also supports `authToken`, sent as a bearer token, mutually exclusive with `apiKey` (`:59-65`).
- OpenAI sends a bearer `Authorization` header from `apiKey` or the `OPENAI_API_KEY` config, through `AuthOptions.bearer` (`openai.ts:81`; `auth-options.ts:51-62`). It adds optional `OpenAI-Organization` and `OpenAI-Project` headers (`openai.ts:146-149`) and `queryParams` (`:94`). It has no `authToken` mode.

## What I could not establish
- I did not read the bodies of the helpers called by `prepareRequest` (Q5), the Anthropic block handlers beyond what is cited (Q6), or the logic around the `LLMClient.Service` consumers in `session.ts`, `generate.ts` and `plugin/internal.ts` (Q3).
- Q8 is a count from import statements. I did not check which assertions in each file depend on `compileRequest`.