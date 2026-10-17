I answered all ten, but the code-map tool alone only fully answered Q4 and Q5. I got the rest by reading and grepping files, and each answer says which.

**Q1. Where LLMClient is defined, and its live layer**
- The service is `class LLMClientService extends Context.Service<…>()("@opencode/LLMClient")` at `packages/ai/src/route/client.ts:261`. `Service` is an alias for it at `:262-263`, and its method shape (`compact`, `stream`, `generate`) is `Interface` at `:177-181`.
- The layer is `layer: Layer.Layer<Service, never, RequestExecutor.Service>` at `packages/ai/src/route/client.ts:657-685`. It builds `stream` from `streamRequestWith({ http: executor })` and sets `generate` and `compact` too. It is exported as `LLMClient.layer` at `:689-696`.
- There is no layer named "live". `layer` is the real one. A test implementation is provided at `packages/ai/src/testing.ts:227` and `:249`.
- Tool: `where LLMClient` found `:261`. I found the layer by reading.

**Q2. Anthropic provider ID, default base URL, API-key auth**
- **ID:** `ProviderID.make("anthropic")` at `packages/ai/src/providers/anthropic.ts:13`.
- **Default base URL:** `https://api.anthropic.com/v1` is `DEFAULT_BASE_URL` at `packages/ai/src/protocols/anthropic-messages.ts:37`. It is applied with `baseURL ?? AnthropicMessages.DEFAULT_BASE_URL` at `packages/ai/src/providers/anthropic.ts:44`.
- **API-key auth** (`packages/ai/src/providers/anthropic.ts:32-37`):
  - An explicit `auth` wins.
  - Otherwise it uses the `apiKey` option, then the `ANTHROPIC_API_KEY` config variable, and sends it as the `x-api-key` header.
  - `authToken` is the alternative: a bearer token (`:65`). Passing both `apiKey` and `authToken` throws (`:59-63`).
- The route itself has `Auth.none` (`packages/ai/src/protocols/anthropic-messages.ts:1671`). The facade injects auth through `AnthropicCompatible.configure` (`packages/ai/src/providers/anthropic-compatible.ts:47-52`).
- Tool: `find` with the description returned no matches, so I read the files.

**Q3. What uses the LLMClient service**
- **Inside `packages/ai`:**
  - `packages/ai/src/llm.ts:45` and `:54` (`LLM.generate` and `LLM.stream` call `LLMClient.generate` and `LLMClient.stream`).
  - `packages/ai/src/llm.ts:132` (`generateObject` calls `LLMClient.generate`).
  - The helpers `stream`, `generate` and `compact` (`packages/ai/src/route/client.ts:618-648`) and `streamRequest` (`:650-655`) do `yield* Service`.
  - `packages/ai/src/ai-client.ts:12` puts `LLMClient.layer` into `AIClient.layerWith`.
  - `packages/ai/src/testing.ts:227` provides a test client.
  - It is re-exported at `packages/ai/src/index.ts:2,11-12` and `packages/ai/src/route/index.ts:1,9-10`.
- **Outside `packages/ai`** (I found these by grep; they are not in the tool's scope):
  - `packages/core/src/session/runner/step.ts:69`, which calls `llm.stream` at `:107`.
  - `packages/core/src/session/compaction.ts:189`, which calls `llm.compact` at `:359` and `llm.stream` at `:511`.
  - `packages/core/src/session/title.ts:43`, which calls `llm.stream` at `:74`.
  - `packages/core/src/session/generate.ts:32`, which calls `llm.generate` at `:69`.
  - `packages/core/src/generate.ts:36`.
  - `packages/core/src/session.ts:250` and `:422`.
  - `packages/core/src/plugin/internal.ts:131`.
  - `packages/core/src/effect/app-node-platform.ts:27`, where the layer is wired to the request executor.
- Tool: `callers LLMClientService` returned only the declaration.

**Q4. What calls `prepareRequest`** (tool and my reading agree)
- Three call sites in `packages/ai/src/route/client.ts`:
  - `compile` at `:575`. That covers `streamRequestWith` (`:605`) and `compileRequest` (`:591`).
  - The `compact` function in the layer, in the trigger branch at `:673`.
  - The same function, in the endpoint branch at `:675`.

**Q5. What `prepareRequest` calls** (`packages/ai/src/route/client.ts:555-572`)
- `resolveRequestOptions` (`:556`, defined `:265`). It calls `normalizeToolHistory` (`packages/ai/src/tool-history.ts:6`), `mergeGenerationOptions`, `mergeProviderOptions` and `mergeHttpOptions` (`packages/ai/src/schema/options.ts`).
- `LLMRequest.update` (`:557`, `:565`, `:571`; `packages/ai/src/schema/messages.ts:437`) and `LLMRequest.input` (`:557`; `packages/ai/src/schema/messages.ts:418`).
- `sanitizeSurrogates` (`:557`; `packages/ai/src/utils/sanitize.ts:4`).
- The local `dedupe` (`:559`).
- `ToolSchemaProjection.tools` (`:565`; `packages/ai/src/protocols/utils/tool-schema.ts:99`).
- `applyEffortUpdates` (`:564`; `packages/ai/src/effort-updates.ts:16`).
- `applyCachePolicy` (`:563`; `packages/ai/src/cache-policy.ts:173`).
- `route.headers?.(…)` (`:568`). The tool could not resolve it because it depends on the route. For Anthropic it is `anthropic-version` (`packages/ai/src/protocols/anthropic-messages.ts:1673`).
- `mergeHttpOptions` (`:571`; `packages/ai/src/schema/options.ts:94`) and `new HttpOptions` (`:571`, defined outside the repo).

**Q6. Down from the layer's `stream` to protocol parsing**
1. The layer sets `stream = streamRequestWith({ http: executor })` (`packages/ai/src/route/client.ts:661`, defined `:602`).
2. `compile` (`:605`, defined `:574`) calls `prepareRequest` (`:575`), then `route.body.from` (`:578`) and `route.prepareTransport` (`:579`).
3. `route.streamPrepared` (`:606`, defined `:423`) runs `transport.execute` (`:426`) to get frames.
4. Each frame goes through `decodeEvent` (`:447`, defined `:362`), which decodes with `protocol.stream.event`.
5. `protocol.stream.initial` and `protocol.stream.step` (`:458`, `:461`) do the parsing. For Anthropic, `step` is at `packages/ai/src/protocols/anthropic-messages.ts:1529`. It calls `onContentBlockStart` (`:1566`), `onContentBlockDelta` (`:1574`), `onMessageDelta`, `onMessageStop` and `onError` (`:1583`).
6. `requireTerminalEvent` (`:484`) wraps the result.
- The tool's chain reached `compile` and `prepareRequest` but stopped at `route.streamPrepared`, because it is a property call on an interface. Steps 3–6 are my reading of the code.

**Q7. Up from `requireTerminalEvent` to the session step**
- `requireTerminalEvent` (`packages/ai/src/route/client.ts:341`) is called at `:484` inside `streamPrepared` (`:423`).
- `streamPrepared` is called by `streamRequestWith` (`:606`).
- `streamRequestWith` is called by the layer's `stream` (`:661`).
- The layer's `stream` is `llm.stream(...)` at `packages/core/src/session/runner/step.ts:107`, inside `SessionStep.attempt` (`:73`).
- `attempt` is called as `steps.attempt({…})` at `packages/core/src/session/runner/llm.ts:248`, where `steps` comes from `SessionStep.make` (`:53`).
- The tool returned only the first hop (`:484`). The rest is my reading. The step to `llm.stream` crosses a service boundary, so no static tool could follow it.

**Q8. Tests that reach `compileRequest`**
- `compileRequest` is defined at `packages/ai/src/route/client.ts:590`. It is test-only, and no source file calls it.
- 53 test files import it directly, all from `…/src/route/client.js`. Examples are `packages/ai/test/compile.test.ts:15`, `packages/ai/test/cache-policy.test.ts:5`, `packages/ai/test/effort-updates.test.ts:5`, `packages/ai/test/adapter.test.ts:5`, `packages/ai/test/tool-schema-projection.test.ts:8` and `packages/ai/test/provider/anthropic-messages.test.ts:16`.
- The rest are under `packages/ai/test/provider/`: the OpenAI, Gemini, Bedrock, Mistral and Groq tests, plus the `*.recorded.test.ts` files. Two of them, `bedrock-mantle.test.ts:7` and `open-responses-replay.test.ts:6`, also import `LLMClient`.
- Tests that only call `LLMClient.stream`, `LLMClient.generate` or `LLMClient.layer` reach the internal `compile`. They do not reach `compileRequest`.
- **The tool failed here.** `tests compileRequest` returned 0 tests. I did not check why. The count above is from grep.

**Q9. How `generateObject` produces a typed object** (`packages/ai/src/llm.ts:123-196`)
1. **Decision:** `"schema" in options` (`:175`).
   - A typed Effect schema is wrapped by `makeTool({ parameters: schema, success: Schema.Unknown, execute: () => Effect.void })` (`:177-185`). Its `_decode` is `Schema.decodeUnknownEffect(parameters)` (`packages/ai/src/tool.ts:196`).
   - A raw `jsonSchema` is wrapped by `makeTool({ jsonSchema, … })` (`:188-195`). Its `_decode` is the identity (`packages/ai/src/tool.ts:176`), so the object is `unknown` and the caller validates.
2. `runGenerateObject` builds the request (`:127`) and forces a synthetic `generate_object` tool. It sets `tools: toDefinitions(...)` and `toolChoice: ToolChoice.named(...)` (`:128-131`). The tool is never executed.
3. It calls `LLMClient.generate(...)` (`:132`).
4. Decision: it looks for a tool call named `generate_object` in `response.toolCalls` (`:133-135`). If the model did not call it, it fails with `InvalidProviderOutputError` (`:136-141`).
5. It decodes `call.input` with `tool._decode` (`:142`). A decode failure becomes an `AIError` (`:143-151`).
6. It returns `new GenerateObjectResponse(object, response)` (`:153`).
- It avoids provider JSON modes on purpose (doc comment `:156-160`), so it works on every protocol.
- Static types come from the overloads at `:168-173`. The `Schema.Schema.Type<S>` result type in the first overload is what makes the object typed.
- I did not run this.

**Q10. Anthropic vs OpenAI: routes and auth**

| | Anthropic | OpenAI |
|---|---|---|
| Routes | One: `[AnthropicMessages.route]` (`providers/anthropic.ts:15`) | Two: `[OpenAIResponses.route, OpenAIChat.route]` (`providers/openai.ts:27`). The default `model` is Responses (`:124`); `.chat` gives Chat |
| Path | `/messages`, plus `?beta=true` when the provider is `"anthropic"` (`protocols/anthropic-messages.ts:1668`) | `/responses` (`protocols/open-responses.ts:30`) and `/chat/completions` (`protocols/openai-chat.ts:35`) |
| Base URL | `https://api.anthropic.com/v1` (`anthropic-messages.ts:37`) | `https://api.openai.com/v1` (`openai-responses.ts:23`, `openai-chat.ts:34`) |
| Transport | HTTP SSE, with an `anthropic-beta` header computed per body (`anthropic-messages.ts:1616-1661`) | Responses uses a channel transport with an `openai-beta` websocket header (`openai-responses.ts:309-316`). Chat uses `sseWithDone` (`openai-chat.ts:1309`) |
| Fixed headers | `anthropic-version: 2023-06-01` (`:1673`) | None at route level. The facade adds `OpenAI-Organization` and `OpenAI-Project` (`openai.ts:146-149`) |
| Auth | `x-api-key` header from `apiKey` or `ANTHROPIC_API_KEY` (`anthropic.ts:32-37`). Alternative `authToken` as bearer; both together throw (`:59-65`) | `Authorization: Bearer` from `apiKey` or `OPENAI_API_KEY` (`openai.ts:81`; `route/auth-options.ts:51-62`). No `authToken` option |
| How auth is attached | Through `AnthropicCompatible.configure` and `route.with` (`anthropic-compatible.ts:47-52`) | Through `route.with` in `configuredRoute` (`openai.ts:92-95`), with `queryParams` added to the endpoint |
| Other modalities | None | `image`, `speech`, `transcription` (`openai.ts:118-120`) |

- Both protocol routes are defined with `Auth.none` (`anthropic-messages.ts:1671`, `openai-responses.ts:307`, `openai-chat.ts:1318`). The provider facade supplies the real auth.
- I did not read the websocket channel code in detail.

**Not done**
- The harness-guard hook asked me to write a criteria file and record a deadline. You said not to change any file, so I did neither. I changed no files.