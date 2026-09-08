# Tool-interface prior art: what the world has built and measured

**Domain:** software engineering — how an agent framework should present its tool interface to an
LLM so the model forms correct calls.

**Framing of this document:** external evidence only. Two sibling investigations cover internal
measurement and the contrarian case; neither is attempted here. Where this document says
"no measurement found", that is a claim about the public literature as of 2026-09-08, not a claim
that no effect exists.

**Grounding.** Written against `ancient_games/hybrid/cli.py` (`tools_schema`, `DATACLASSES`,
`ENUMS`, `NOTES`), `ancient_games/hybrid/tools/*.py`, `ancient_games/hybrid/invariants.py`, and the
53 declined/refused `tool_call` events under `ablation/runs/**`. Re-extract those with:

```python
import json, glob
for p in glob.glob('ablation/runs/**/*.jsonl', recursive=True):
    for ln in open(p):
        e = json.loads(ln) if ln.strip() else {}
        if e.get('event') == 'tool_call' and e.get('reason'):
            print(e.get('tool'), e['reason'][:150])
```

The dispatch's classification is taken as given: 29 SEMANTIC (55%), 17 ARG-SHAPE/ENUM (32%),
6 name-slot (11%). One observation from re-reading the raw reasons is load-bearing for the
recommendations below and is stated here because it changes what "semantic" means:

> **16 of the 53 declines (30% of all declines, 55% of the "semantic" class) carry a reason that
> names nothing at all** — `internal-error: False` (x9), `internal-error: True` (x6),
> `internal-error: 'no'` (x1), across `gate` (10), `prove` (5) and `corroborate` (1). These are
> `str(exception)` of an exception constructed with a bare value, emitted by
> `_shared.internal_error()`. They are not "constraints a type system cannot express"; they are
> constraints the interface *declined to express to the caller at all*.

**Verified, not eyeballed.** An earlier draft of this document said 13; that was a miscount off a
truncated terminal listing. The figure 16 is the agreement of two independent detectors run over the
journals — the regex `^(internal-error|invalid-args): (True|False|None|'[^']*')$` and a content
heuristic (`startswith("internal-error: ")` and length < 30 and not containing `must be`). They
select the identical 16 events; the symmetric difference is empty.

Distinguish these two failure modes throughout. The literature has a lot to say about the second
one and comparatively little about the first.

---

## Terminology used below

- **Shape** — types, required-ness, enum membership of a single call, decidable from the call alone.
- **Semantics / precondition** — a constraint referring to something outside the call: session
  state, a prior call, the identity of the caller, the value set established earlier in the run.
- **Affordance** — a legal action *in the current state*. Turning a precondition into an affordance
  makes its violation an absence rather than an error.

---

## 1. What the major interfaces actually specify, and what they deliberately omit

Verdict up front: **none of the seven expresses preconditions or call ordering.** Two of seven ship
"currently unavailable" as a first-class concept, and they do it in opposite ways.

| Interface | Carries per-call shape | Preconditions / ordering | "Unavailable right now" as a first-class concept |
|---|---|---|---|
| Anthropic tool use | `name`, `description`, `input_schema` (JSON Schema); `strict: true` for guaranteed conformance | none in the schema | no — but the tool *list* is per-request, so the caller can omit tools; `tool_choice` forces/forbids calling |
| OpenAI function calling / Structured Outputs | JSON Schema, `strict: true` | none | no |
| MCP | `name`, `title`, `description`, `inputSchema`, `outputSchema`, `annotations` | none | **yes, indirectly**: `tools.listChanged` capability + `notifications/tools/list_changed`; the server re-publishes a different tool list |
| LSP | request params typed by the meta-model | none for ordering; capabilities are negotiated at `initialize` | **yes, explicitly**: `CodeAction.disabled: { reason: string }`, plus `client/registerCapability` / `unregisterCapability` for runtime add/remove |
| OpenAPI 3.1 | JSON Schema per operation; `readOnly`/`writeOnly`; `deprecated` | **no.** `Link` objects describe *possible* transitions only | no |
| GraphQL | introspection: full type graph, `description`, `isDeprecated` + `deprecationReason` | none | no (deprecation is not availability) |
| gRPC server reflection | protobuf `FileDescriptor`s only — no prose, no constraints | none | no |

### The two designs worth reading closely

**LSP `CodeAction.disabled` — "show it, say why".** The spec's own doc comment (quoted verbatim
via `lsp-types`, which copies it):

> "Marks that the code action cannot currently be applied. Clients should follow the following
> guidelines regarding disabled code actions: Disabled code actions are not shown in automatic
> lightbulb code action menu. Disabled actions are shown as faded out in the code action menu when
> the user request a more specific type of code action, such as refactorings. If the user has a
> keybinding that auto applies a code action and only a disabled code actions are returned, the
> client should show the user an error message with `reason` in the editor. @since 3.16.0"

This is the single closest prior art to the ancient-games problem: an interface that (a) knows the
action is illegal in the current state, (b) does not silently hide it, (c) carries a machine-readable
*reason* string alongside the action, and (d) prescribes different presentation depending on whether
the consumer is browsing or committing. LSP 3.16 shipped this rather than dropping disabled actions
from the list, because dropping them destroys discoverability — the user then cannot learn *why*
the refactoring is unavailable. That trade-off applies identically to an LLM caller.

**MCP `listChanged` — "hide it, republish".** The spec:

> "When the list of available tools changes, servers that declared the `listChanged` capability
> **SHOULD** send a notification: `notifications/tools/list_changed`."

MCP discussion #643 asked for "dynamic tool exposure based on server state" as a *new* capability;
a maintainer replied that "MCP does support a ToolListChangedNotification which enables the Client
to dynamically update it's tool list based on MCP Server state." So: the spec supports it, the
mechanism is republication of the whole list, and the community had to be told it exists. The
discussion is open; no maintainer discussion of the client-cache or model-confusion trade-offs
appears in it.

Note the difference: **LSP surfaces unavailability with a reason; MCP surfaces it as absence.** No
published measurement compares the two for LLM callers (see §9).

### What "annotations" do and do not buy you

MCP's `annotations` (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) are the
closest any tool protocol comes to declaring behaviour rather than shape. They are advisory, and the
spec is blunt about their trust status:

> "For trust & safety and security, clients **MUST** consider tool annotations to be untrusted
> unless they come from trusted servers."

ancient-games' `MANIFEST["side_effects"]`, `cost`, `participates_in` are the same genre and should be
understood the same way: metadata for routing and display, never a check.

### Where errors go

MCP splits errors deliberately: protocol errors (JSON-RPC, e.g. `-32602` "Unknown tool") vs tool
execution errors (`isError: true` inside a normal result, so the model sees them and can react).
ancient-games already makes the equivalent split — exit code 2 refused/invalid-args vs exit 0 with
`ok:false`. That part is conventional and correct.

**Sources:** [MCP tools spec 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) ·
[MCP discussion #643](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/643) ·
[LSP CodeAction.disabled doc comment](https://docs.rs/lsp-types/latest/lsp_types/struct.CodeAction.html) ·
[LSP 3.17 spec](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/) ·
[Anthropic tool use overview](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview) ·
[OpenAPI 3.1.0 spec](https://spec.openapis.org/oas/v3.1.0.html) ·
[GraphQL introspection spec §4](https://github.com/graphql/graphql-spec/blob/main/spec/Section%204%20--%20Introspection.md) ·
[gRPC reflection](https://grpc.io/docs/guides/reflection/)

---

## 2. Constrained / grammar-guided decoding

**Conclusion for this repo: not available as a lever, and it would not touch the 55% anyway.**

### What it is and what it costs

Constrained decoding masks the logits at each step so that only tokens keeping the output inside a
grammar can be sampled: llama.cpp GBNF, Outlines, guidance, XGrammar, and the vendor features built
on them (OpenAI `strict: true` / Structured Outputs, Anthropic strict tool use).

- **Runtime cost is now negligible.** XGrammar reports "under 40 µs per token for JSON Schema and
  CFG (JSON)", up to 100× lower per-token mask latency than prior engines and up to 80× end-to-end
  serving speedup on H100 for Llama-3.1, achieved by precomputing the >99% of vocabulary tokens
  whose validity is context-independent. XGrammar is the default backend in vLLM and SGLang.
- **Compile cost is per-schema and cached.** OpenAI: "The first request you make with any schema
  will have additional latency as our API processes the schema, but subsequent requests with the
  same schema will not have additional latency."
- **Distributional cost is real and is the underrated one.** Park et al., *Grammar-Aligned Decoding*
  (NeurIPS 2024) show grammar-constrained decoding "can distort the LLM's distribution, leading to
  outputs that are grammatical but appear with likelihoods that are not proportional to the ones
  given by the LLM, and so ultimately are low-quality", and give ASAp, an algorithm that restores
  the correct conditional distribution. Greedy masking is not free even when it is fast.

### What it cannot constrain

1. **Anything outside a regular/context-free language over the output tokens.** "This `claim_id`
   must be one already recorded in this run" is not a property of the string; it is a property of
   the journal.
2. **Cross-field conditionals, in practice.** JSON Schema *can* express a good chunk of these
   (`if`/`then`/`else` since Draft 7, `dependentRequired`, `dependentSchemas` since 2019-09 — see
   §4), but the strict-decoding profiles do not accept them. OpenAI strict mode has historically
   rejected `pattern`, `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`, `multipleOf`,
   `minItems`, `maxItems`; support has been expanding, and the supported set is a moving target you
   must check against current docs rather than assume.
3. **Semantic correctness of values.** OpenAI's own guide: "Structured Outputs can still contain
   mistakes", and warns that "the model can result in hallucinations if the input is completely
   unrelated to the schema". Forcing a value into an enum guarantees it is *a member*, not that it
   is *the right member*. This matters here: `record_check.mechanism` failures were the agent trying
   to describe what it did in a field that only accepts a fixed vocabulary. Constrained decoding
   would have produced a syntactically valid but semantically arbitrary `mechanism`. That is
   strictly worse than a refusal, because the journal would then record a false mechanism.

### Does it degrade reasoning?

Contested, and the contest itself is instructive. Tam et al., *Let Me Speak Freely?*
(EMNLP 2024 Industry) report "a significant decline in LLMs reasoning abilities under format
restrictions" with "stricter format constraints generally lead[ing] to greater performance
degradation". .txt's rebuttal reran the tasks on Llama-3-8B-instruct with matched prompts and got
the opposite sign — GSM8K 0.77 unstructured vs 0.78 structured; Last Letter 0.73 vs 0.77; Shuffle
Object 0.41 vs 0.44 — and identified three methodological problems: prompts differed across
conditions, the paper's "structured" arm was JSON-*mode* (a fine-tuning behaviour with no
constraint engine) rather than constrained decoding, and Claude 3 Haiku was used as the answer
parser. **Treat the "constrained decoding hurts reasoning" claim as unresolved**, and note that
neither side measured tool-call correctness.

### Applicability here

ancient-games does not host the model. The agent is a subagent that emits
`python3 -m ancient_games.hybrid call <tool> '<json>'` into a shell. **There is no logit stream to
mask.** Constrained decoding becomes available only if the framework moves from a CLI surface to
the Messages API tool interface, at which point `strict: true` on the tool definitions is a
one-line adoption. Until then it is not a candidate. This also means the 6 name-slot errors (JSON
where the tool name goes) are *structurally* solvable only by changing the invocation surface —
which is exactly what a real tool-calling API does by separating `name` from `arguments`.

**Sources:** [XGrammar](https://arxiv.org/abs/2411.15100) ·
[Grammar-Aligned Decoding (NeurIPS 2024)](https://arxiv.org/abs/2405.21047) ·
[Let Me Speak Freely? (EMNLP 2024)](https://aclanthology.org/2024.emnlp-industry.91/) ·
[.txt rebuttal, with rerun numbers](https://blog.dottxt.ai/say-what-you-mean.html) ·
[OpenAI Structured Outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs) ·
[OpenAI announcement (100% vs <40% schema-following)](https://openai.com/index/introducing-structured-outputs-in-the-api/)

---

## 3. Dynamic tool availability / affordance filtering

**This is where the strongest measured result in the whole search lives, and it is not the one you
would guess.**

### The strong result: state-machine-gated tool visibility

Wu et al. (Meta), *The Art of Tool Interface Design* (arXiv 2503.21036) introduce **State-Machine
Augmented Generation (SMAG)**:

> "We represent business logic as state machines. The LLM agent orchestrates state transitions to
> precisely follow business logic and is aided by state-dependent instructions."

Mechanically: the state machine is itself a callable tool (instantiate a flow, set slot variables,
trigger transitions); the current flow state is placed in working memory; and crucially the tool
surface is filtered by state —

> "We allow the system prompt...to be conditioned on the current state variables. For
> example...before successful user authentication, we can hide all tools except authentication
> tools."

And they are explicit that this exists because prompt-level policy does not hold:

> "The standard solution is to introduce tools as functions and let LLM orchestrate their use...
> However, this is not reliable as we cannot guarantee that LLM would strictly follow the business
> logic."

**Numbers, on τ-bench retail:** GPT-4o 68.3% → 82.6% (+14.3pp); Llama-3.1-405B 49.6% → 81.9%
(+32.3pp). Ablation on Llama-3.1 attributes **+15.6pp to SMAG alone**, with LLM-powered sub-tools
+10.3pp, multi-function calling +1pp, adaptive context management + prompting +4pp.

This is the closest published analogue to ancient-games' situation: an agent that keeps violating
ordering and policy preconditions expressed in prose, fixed by moving the protocol into
program-enforced state with a state-conditioned tool surface. Note that SMAG buys *both* things at
once — enforcement and visibility — so the ablation does not separate "the check now runs in code"
from "the illegal tool is now absent". That separation is not established anywhere I found.

### The weaker, better-publicised result: tool-count reduction

Anthropic's Tool Search Tool loads tool definitions on demand rather than up front. Reported:
Opus 4 49% → 74%, Opus 4.5 79.5% → 88.1%; ~85% token reduction (~77K → ~8.7K tokens of tool
definitions). Programmatic Tool Calling: 43,588 → 27,297 average tokens (37%), internal knowledge
retrieval 25.6% → 28.5%, GIA 46.5% → 51.2%.

**This is almost certainly irrelevant to ancient-games and should not be cited as support.** These
gains come from catalogues of hundreds to thousands of tools. The best-controlled treatment I found,
*How Many Tools Should an LLM Agent See? A Chance-Corrected Answer* (arXiv 2605.24660), introduces
Bits-over-Random to correct for the fact that showing more tools raises the random-success baseline,
and reports that on MetaTool with N=20 the learned policy settles at K=1.6 tools with no degradation
from the small catalogue. The widely-quoted "78% at 10 tools → 13.62% at 100+ tools" figure comes
from vendor/blog material and I could not trace it to a controlled primary source; **do not use it**.
ancient-games has 18 tools. **Affordance filtering here would have to be justified by precondition
clarity, not by context savings.** If someone proposes it on token-budget grounds, that is
unsupported at this scale.

BFCL v3 does directly measure the neighbouring skill: its "Missing Functions" category tests
"whether the agent can recognize when required tools are unavailable or when no valid tool applies",
alongside Irrelevance Detection (`IrrelAcc`: fraction of no-call cases where the model correctly
abstains). So the field treats "the right tool is absent" as a first-class, separately-scored
competence — evidence that absence is a signal models can act on, though I found no head-to-head of
absence vs a disabled-with-reason listing.

### Robotics precedent

SayCan (arXiv 2204.01691) is the canonical "precondition as affordance" system: a learned value
function per skill answers "if I ask the robot to perform this action right now, will it succeed?",
and the score combines the LLM's usefulness probability with the affordance's success probability;
evaluated zero-shot on 101 real-world kitchen tasks. The architectural lesson transfers cleanly —
**let the environment, not the model, decide what is currently possible** — but the numbers do not,
because SayCan's affordances are learned continuous values over robot skills, not deterministic
predicates over a journal.

### REST's version of the same idea, 25 years earlier

HATEOAS is affordance filtering: the server returns, with each representation, the links
representing the transitions legal *from this state*, so the client need not know the protocol in
advance. This is the design pattern ancient-games would be adopting. Worth knowing that OpenAPI's
static analogue is explicitly weaker — the `Link` Object expresses "a possible design-time link",
and the spec cautions that "the presence of a link does not guarantee the caller's ability to
successfully invoke it". Design-time link lists do not carry preconditions; runtime ones do.

**Sources:** [The Art of Tool Interface Design](https://arxiv.org/abs/2503.21036) ·
[Anthropic advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) ·
[How Many Tools Should an LLM Agent See?](https://arxiv.org/html/2605.24660v1) ·
[BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) ·
[SayCan](https://arxiv.org/abs/2204.01691) ·
[HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) ·
[OpenAPI Link Object](https://spec.openapis.org/oas/v3.1.0.html)

---

## 4. Design by contract, refinement types, and the "set by the callee" problem

### Can a machine-checkable contract carry "field X is set by the callee, never the caller"?

**Yes — three ways, in increasing cost, and the cheapest one is already available.**

**(a) Reject the field if present. Cost: near zero.** The standard vocabulary for this is
OpenAPI/JSON Schema `readOnly`. JSON Schema 2020-12 §9.4: *"If `readOnly` has a value of boolean
true, it indicates that the value of the instance is managed exclusively by the owning authority,
and attempts by an application to modify the value of this property are expected to be ignored or
rejected by that owning authority."* OpenAPI 3.0 sharpens it: a `readOnly` property "MAY be sent as
part of a response but SHOULD NOT be sent as part of the request".

But note what this is: **`readOnly` is an annotation, not an assertion.** JSON Schema places
enforcement on the "owning authority". A validator will not fail a document for containing a
`readOnly` field. So the standard gives you the *vocabulary and the semantics*, and you supply the
check. The check is three lines and it is non-forgeable.

This is directly applicable. `NOTES` currently carries, as free prose the agent must read and obey:

```
"n_required": "set by corroborate — never passed by the caller",
"stakes":     "set by corroborate — never passed by the caller",
"actor":      "set by corroborate from ctx.actor — never passed by the caller",
```

Three constraints that a two-line `if name in args: return invalid_args(...)` converts from a rule
the agent may violate into one it cannot. The companion is `additionalProperties: false` /
Pydantic's `extra='forbid'`: **an unknown field should be an error, not silently dropped.** Silent
acceptance is how a caller learns nothing.

**(b) Cross-field conditionals in the schema itself. Cost: low, if you write your own validator.**
JSON Schema has had this since Draft 7 / 2019-09:
- `dependentRequired` — 2020-12 §6.5.4: *"This keyword specifies properties that are required if a
  specific other property is present."*
- `dependentSchemas` — applies a subschema when a property is present.
- `if` / `then` / `else` — "If `if` is valid, `then` must also be valid (and `else` is ignored.)"

`kind == "executable"` on absence text requiring `closed_world` is exactly `if`/`then`. Note the
awkwardness: expressing it as JSON Schema buys you nothing here unless a validator runs it, and
writing a Draft-2020-12 validator is not a small stdlib project. Writing the predicate in Python is
five lines. **The value of the JSON Schema vocabulary here is as a design checklist and a
serialisation format, not as an execution engine.**

**(c) Full contracts / refinement types. Cost: high, mostly not adoptable.**
- **Eiffel** (`require` / `ensure` / class invariants) is the origin: preconditions are the caller's
  obligation, postconditions the callee's, and violation blames a specific party.
- **Clojure spec** `fdef` is the most instructive design: `:args` (a spec for arguments), `:ret`
  (for the return), and `:fn` (*"a spec of the relationship between args and ret"*). The key
  operational choice: `instrument` "swaps out the fn var with a wrapped version of the fn that tests
  the `:args` spec" — **instrumentation checks preconditions only**, because a precondition failure
  is the caller's bug and is what you want to report at the boundary; `:ret`/`:fn` are checked under
  generative testing (`check`), not on every call. That is precisely the split ancient-games wants:
  argument contracts at the tool boundary, relational contracts in the test suite.
- **Liquid Haskell / refinement types** can express dependent constraints statically but require a
  dependently-typed host language and an SMT solver. Not adoptable in a stdlib-only Python package
  and not worth further evaluation.
- **Pydantic** `model_validator(mode='after')` gives ergonomic cross-field validation and
  `ConfigDict(extra='forbid')` gives (a) — but **Pydantic is a heavy third-party dependency**
  (compiled `pydantic-core`), and `pyproject.toml` declares `dependencies = []`. Adopting it is a
  policy change, not a refactor. Everything Pydantic would buy here is achievable with dataclasses
  plus explicit predicates.

**Measurement:** I found **no controlled study measuring whether contract-style declarations
improve LLM tool-call correctness.** The DbC literature's evidence base is about human developers
and static analysis; do not transfer its claims.

### The runtime-enforcement analogue built for agents

**AgentSpec** (arXiv 2503.18666, ICSE 2026) is a small DSL of `trigger` / `predicate` / `enforce`
rules evaluated at agent runtime: triggers are execution events, predicates are checked when the
trigger fires, and enforcement is one of `user_inspection` (pause for confirmation),
`llm_self_examine` (ask the model to reconsider), or `invoke_action(...)`. Reported: prevents unsafe
executions in "over 90%" of code-agent cases, "eliminates all hazardous actions" in embodied agent
tasks, 100% compliance for autonomous vehicles, overheads "in milliseconds".

Read this as **independent confirmation that ancient-games' architecture is the mainstream answer**:
`invariants.py` (`check_invariants` → `Refusal(invariant, reason)` with a fixed priority
`I4 > I1 > I5 > I2 > I3`) *is* an AgentSpec-shaped runtime enforcer, built before that paper landed.
The one thing AgentSpec has that ancient-games does not is the `enforce` *vocabulary* — a refusal is
not the only response; `user_inspection` and `llm_self_examine` are distinct outcomes. ancient-games
has the raw material for this (the autonomy modes, the deferral queue, `approve`) but does not
currently let an invariant *choose* its enforcement mode.

**Sources:** [JSON Schema Validation 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation) ·
[JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals) ·
[OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0.html) ·
[clojure.spec rationale](https://clojure.org/about/spec) ·
[clojure.spec guide (fdef, instrument)](https://clojure.org/guides/spec) ·
[AgentSpec](https://arxiv.org/abs/2503.18666)

---

## 5. Session types, typestate, and typing the sequence rather than the call

### The prior art

**Typestate** (Strom & Yemini 1986; Aldrich et al., *Typestate-Oriented Programming*, OOPSLA 2009;
Sunshine et al. 2011; *Foundations of Typestate-Oriented Programming*, TOPLAS 2014) makes the legal
operation set a function of the object's current state: "a typestate checker can statically ensure
that an object method is only called when the object is in a state for which the operation is well
defined." In Plaid the typestate *is* the class, and the class changes at runtime.

**Session types** (Honda et al.; multiparty session types) type the communication protocol itself so
that "protocol implementations can be verified by static type-checking". The two lines converge:
Bierhoff & Aldrich's typestates "are based on session types and describe the permitted sequence of
method calls".

The practical, shipped, boring version of this is the **Rust typestate builder** — each method
consumes `self` and returns a differently-typed value, so `build()` simply does not exist until the
required fields are set. The illegal call is not rejected; it is unnameable.

### Does anyone use it for agents?

Only one system I found does it in the strict sense, and it is SMAG (§3) — business logic as a state
machine, tool visibility conditioned on state, code-enforced. Adjacent but weaker:

- **ToolSandbox** (Apple, arXiv 2408.04682) does not *type* the sequence but *builds a world with
  one*: 34 stateful tools across 11 domains with "implicit state dependencies" — sending a message
  requires cellular service, which cannot be enabled in low-battery mode — and when preconditions
  fail "tools raise informative Python exceptions, forcing agents to reason through trial-and-error".
  Their finding is the one that matters here: "complex tasks like State Dependency, Canonicalization
  and Insufficient Information defined in ToolSandbox are challenging even the most capable SOTA
  LLMs". **The state-dependency class is a known-hard, separately-named failure mode in the
  literature.** ancient-games' `corroborate: ctx.actor has no entry for action '<name>'` (4 of the
  53 declines) is textbook state dependency.
- **PDDL-based planning** (LLM+P arXiv 2304.11477; Guan et al., NeurIPS 2023) gives each action an
  explicit `:precondition` and `:effect` and hands the problem to a symbolic planner. The pattern —
  LLM translates intent into a formal representation, a non-LLM component checks preconditions and
  guarantees the plan — is the strongest available argument for *declaring* preconditions in machine
  form rather than prose. Caveat: this literature measures *plan validity*, not *call-argument
  correctness*, and the domain descriptions are human-authored.

### Honest limit

Typestate is a *static* discipline and its guarantees come from the compiler. ancient-games' tool
surface is a CLI reached from a shell; there is no type checker between the model and the call. The
adoptable residue of typestate is therefore not the type system but the **state-conditioned action
set** — which is §3, and which the framework can compute from the journal.

**Sources:** [Typestate-Oriented Programming (Aldrich et al.)](https://www.semanticscholar.org/paper/Typestate-oriented-programming-Aldrich-Sunshine/94a28e918631d698486584a9b73d5420edc92d01) ·
[Foundations of Typestate-Oriented Programming (TOPLAS)](https://dl.acm.org/doi/10.1145/2629609) ·
[Modular session types for objects](https://arxiv.org/pdf/1205.5344) ·
[ToolSandbox](https://arxiv.org/abs/2408.04682) ·
[LLM+P](https://arxiv.org/abs/2304.11477) ·
[Guan et al. NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/f9f54762cbb4fe4dbffdd4f792c31221-Abstract-Conference.html)

---

## 6. Empirical results by interface style

Ordered by how directly each bears on the question. **Numbers are quoted as published; none was
reproduced here.**

### 6.1 Examples beat schema for exactly the class of constraint at issue — vendor-measured

Anthropic's *advanced tool use* engineering post ships a feature ("Tool Use Examples") whose
justification is a verbatim statement of the ancient-games problem:

> "JSON Schema excels at defining structure–types, required fields, allowed enums–but it can't
> express usage patterns: when to include optional parameters, which combinations make sense, or
> what conventions your API expects."

Named gaps: format ambiguity (date conventions), ID naming conventions, when to populate nested
structures, parameter correlations. **Measured: accuracy 72% → 90% on complex parameter handling.**

Caveats to state plainly: this is a vendor number on an unnamed internal benchmark, with no
described protocol, no sample size, no confidence interval, and a commercial interest in the result.
It is nonetheless the *only* number I found that measures the schema-vs-examples axis on the
semantic class directly, and its direction is corroborated by §6.3.

### 6.2 Error-message content, not error-message format, drives recovery

*Structured Feedback Improves Repair in an LLM Agent Loop* (arXiv 2607.14167) compares four feedback
policies on 50 paired TextWorld games × 2 models (880 rows, 2,652 LLM calls):

| Policy | Content |
|---|---|
| `RawDiag` | the original validation error |
| `LocObs` | failure label + location + observed value |
| `SameNL` | location + observed value + **admissible alternatives**, in prose |
| `TypedFields` | same content as `SameNL`, as keyed JSON with a stable failure label |

Results, four-call budget:
- `TypedFields` vs `RawDiag`: **+44pp** on Qwen2.5-Coder-14B (14/50 → 36/50; 95% interval 28–60pp;
  p = 3.15e-5); **+42pp** on Llama-3.1-8B (8/50 → 29/50; p = 3.81e-6).
- `SameNL` vs `RawDiag`: **+42pp for both models** — prose with alternatives is essentially as good.
- `TypedFields` vs `SameNL`: **+2pp / 0pp, both intervals include zero.**
- `LocObs` vs `RawDiag`: near baseline.

Authors' conclusion: "most of the gain comes from the repair values rather than an observed
advantage for the keyed representation", and "the alternatives account for most of the improvement".
Their stated limits: 50 generated TextWorld games, two quantized small models, admissible actions
capped at 12, prompt size measured in words; and "repair policy cannot act on a failure that its
visible validator does not expose".

**This is the most decision-relevant result in the document, and it argues directly against the
candidate on the table.** Emitting JSON Schema is a change of *representation*. The measured lever
is *naming the admissible set*. `TypedFields` vs `SameNL` says the JSON-ification is worth ~0.

Corroborating, weaker: ToolScan (arXiv 2411.13547) reports that "models receiving constructive error
feedback about function names, argument types, and formats demonstrate immediate recovery from
mistakes across subsequent iterations". *Self-Reflective APIs: Structure Beats Verbosity for AI
Agent Recovery* (arXiv 2606.05037) argues the same thesis from API design; I could not extract its
numbers (PDF text extraction failed) and therefore cite no figure from it.

### 6.3 Error taxonomies: the field's categories, and where ancient-games' 53 land

ToolScan characterises seven error patterns: Insufficient API Calls, Incorrect Argument Value
(including omitting necessary arguments), Incorrect Argument Name (hallucinated argument names),
Incorrect Argument Type, Repeated API Calls, Incorrect Function Name (hallucinated function names),
Invalid Format Error. Success rates: GPT-4 0.71 overall, xLAM-8x22b 0.68, Code-Llama-13b 0.54,
Vicuna-13b 0.16; API-tuned models beat chat-tuned models on hallucination categories.

Note the shape of the taxonomy: **it is entirely per-call.** Six of seven categories are shape or
selection errors; none names a precondition or ordering violation. The 55% semantic class in
ancient-games' data is essentially invisible to the dominant error taxonomy in the literature. This
is a real gap, not an oversight on the framework's part.

### 6.4 Ordering/policy compliance is measured, and it is bad

τ-bench (arXiv 2406.12045) evaluates agents against domain API tools *plus written policy
guidelines*, scoring by final database state, and introduces `pass^k` for consistency across trials.
"State-of-the-art function calling agents (like gpt-4o) succeed on less than 50% of the tasks, and
are quite inconsistent (pass^8 less than 25% in retail)"; ~61% on τ-retail and ~35% on τ-airline.
Authors' diagnosis: agents "struggle with complex reasoning over databases, understanding and
following ad-hoc policies, and handling compound requests".

**This is the empirical case against prose preconditions**, and SMAG (§3) is the measured fix on the
same benchmark: 68.3% → 82.6% for GPT-4o.

### 6.5 Interface *format* comparisons

*The Bitter Lesson of Tool Calling* (arXiv 2608.06370) compares programmatic tool calling — the
model writes Python against "typed Python stubs compiled from the benchmark's function schemas" —
against JSON tool calling on BFCL v4 (309 entries). 11 of 14 models matched or exceeded the JSON
baseline; GPT-5.6 family +10.6%; sequential chaining (52 entries, chains of 2–20) Claude Sonnet 5
80.8% → 96.2% and Claude Opus 4.8 80.8% → 94.2%, with an 18.8pp absolute gap at chain lengths ≥12;
parallel fan-out GPT-5 71.9% → 96.9%; under a 128-schema flood PTC +5.5% while JSON degraded 2.3%
and a filesystem-discovery baseline degraded 32.0%.

Relevant because ancient-games' tools *are already typed Python functions*, currently hidden behind
a JSON-over-CLI surface. **But see the veto in §8: PTC hands the agent an interpreter, which is
incompatible with a framework whose premise is that the agent cannot forge its way past a check.**

*Meta-Tool* (arXiv 2604.20148) reports documentation as the dominant ablation factor on InterCode:
removing it drops performance 54.0% → 44.0% (+10pp contribution). Consistent with §6.1.

### 6.6 What was NOT measured anywhere I looked

- **Schema vs docstring vs bespoke prose, held constant.** No study isolates the *serialisation* of
  a tool description with content held constant. §6.2's `TypedFields`-vs-`SameNL` null is the
  nearest thing, and it is on error messages, not tool descriptions, with n=50 games and two small
  quantized models.
- **Hiding an illegal tool vs listing it with a `disabled.reason`.** No measurement found, for LLM
  callers, of the LSP-vs-MCP choice. This is a genuine open question and a cheap experiment.
- **Whether declaring preconditions in a machine-readable form improves calls when the enforcement
  is unchanged.** SMAG changes visibility and enforcement together; nobody separates them.

**Sources:** [Anthropic advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) ·
[Structured Feedback Improves Repair in an LLM Agent Loop](https://arxiv.org/html/2607.14167v1) ·
[ToolScan](https://arxiv.org/abs/2411.13547) ·
[τ-bench](https://arxiv.org/abs/2406.12045) ·
[The Bitter Lesson of Tool Calling](https://arxiv.org/html/2608.06370v1) ·
[Meta-Tool](https://arxiv.org/html/2604.20148) ·
[Self-Reflective APIs](https://arxiv.org/pdf/2606.05037)

---

## 7. Additions the dispatch did not list

### 7.1 Dynamic (session-derived) enums — the cheapest reframing available

Several of the "semantic" declines are not semantic at all. They are **enum errors over a value set
that the session already knows but the schema was authored before**:

```
corroborate  ctx.actor has no entry for action 'delete-dead-helpers' (set at C·3/C·4 or by D)
corroborate  ctx.actor has no entry for action 'delete-helpers'          (×3, varying names)
guard        ...tripwires must be keyed by a hub element of this action (hubs: [])
```

The legal `action` values are exactly `ctx.actor.keys()`. The legal tripwire keys are exactly
`{k for h in hit.hubs for k in hit.tripwire_keys(h)}` — `guard.unmatched_tripwire_keys` already
computes this set in order to report the error. `falsifies` must be a claim_id recorded in the run.
`framings` is keyed by claim_id.

**A schema rendered per-call from the current ctx/journal turns each of these into an ordinary enum
listing.** This is the technique behind both LSP dynamic registration and MCP `listChanged`, applied
at field granularity rather than tool granularity, and it is the mechanism by which §6.2's
"admissible alternatives" become available *before* the failed call rather than after it. Nothing in
the literature names this pattern that I could find — it is the obvious composition of
§3 (affordance filtering) and §6.2 (name the admissible set), but no citation is offered because I
found none.

Cost: `tools_schema()` already takes the loaded tools; it would additionally take `ctx` and the
journal events. `ENUMS` becomes a mapping from field name to a callable over `(ctx, events)`.

### 7.2 The blame question — who is at fault, stated in the message

Eiffel's and Racket's contract systems both carry **blame**: a violated precondition blames the
caller, a violated postcondition blames the callee. ancient-games conflates them:
`_shared.internal_error(e)` emits `internal-error: {e}` for *both* "the caller passed nonsense" and
"the framework broke". The 16 `internal-error: False|True|'no'` declines are caller errors wearing a
callee-error label, with no field name and no admissible set.

The repo has already discovered this fix locally and applied it in one place — `gate.py` now
pre-checks `governance_gated` and returns
`invalid_args("governance_gated", '"none" or an owner-gated registry row id (one of …), never a bool', gg)`,
which is precisely §6.2's `SameNL`/`TypedFields` content: field, admissible set, observed value.
The `_shared.invalid_args(field, accepted, got)` helper is exactly the right shape. **The finding is
that this pattern exists and is under-applied, not that it needs inventing.**

A cheap, non-forgeable structural fix: make it impossible to emit a refusal that names no field —
e.g. `internal_error` refuses to accept an exception whose `str()` is empty or a bare literal, and
the invariant floor's own test asserts that no journalled `reason` matches
`^(internal-error|invalid-args): (True|False|None|'[^']*')$`. That is a test that can independently
fail, which is the standard this repo holds itself to.

---

## 8. What to steal, and what it costs

**Ranking rule, fixed before the table.** Each candidate is scored 0–3 on three axes:

- **(a) Semantic reach** — how much of the 55% class it addresses. 3 = addresses most of it; 0 = none.
- **(b) Adoption cost in a stdlib-only Python package** (`dependencies = []`) — scored so that
  *cheaper is higher*. 3 = under ~50 lines, no new dependency, no new surface; 0 = new heavy
  dependency or a change of invocation architecture.
- **(c) Non-forgeability** — can the agent get past the check by writing something clever?
  3 = the check runs in program code the agent cannot reach; 0 = the agent can bypass it.

Rank by (a) descending, tie-broken by (b) descending. **(c) ≤ 1 is a veto for anything load-bearing:
such a candidate may be adopted as guidance but must never carry an invariant.** This rule was
written before the table was filled in.

| # | Steal | From | a | b | c | Cost, concretely |
|---|---|---|---|---|---|---|
| 1 | **Every refusal names the field and the admissible set** — no reason may be a bare repr; route caller errors through `invalid_args`, never `internal_error`; add a test asserting no journalled reason is a bare literal | Structured Feedback (+44pp/+42pp); Clojure spec `instrument` checks `:args` only; the repo's own `gate.py` fix | 3 | 3 | 3 | ~30 lines across `_shared.py` + the ~8 raise sites, plus one test. No new dependency. Directly attacks the 16 message-less declines and improves recovery on the rest. |
| 2 | **Session-derived enums: render the schema per call from ctx + journal** — `action` ∈ `ctx.actor.keys()`, tripwire keys ∈ computed hub set, `falsifies` ∈ recorded claim_ids | LSP dynamic registration; MCP `listChanged`, applied per-field (§7.1) | 3 | 2 | 3 | `tools_schema(tools)` → `tools_schema(tools, ctx, events)`; `ENUMS` values become callables. ~60–100 lines. Converts ≥5 of the 53 from semantic to enum, and — more importantly — supplies the admissible set *before* the call. |
| 3 | **State-conditioned tool surface: `tools` lists only tools whose loop-level preconditions currently hold, and names the reason for each that does not** | SMAG +15.6pp ablation, τ-bench retail 68.3→82.6 / 49.6→81.9; LSP `CodeAction.disabled.reason`; HATEOAS | 3 | 2 | 3 | `invariants.py` already computes refusals from `(call, ctx, events)`. A `preconditions_now()` that evaluates them for a null call per tool is a modest addition. Attacks `checkpoint-not-cleared` (4), `no-prove-pass` (4), `hard_blocked` (1). **Prefer LSP's show-with-reason over MCP's hide**: at 18 tools there is no context argument for hiding (§3), and hiding destroys the agent's ability to learn the protocol. |
| 4 | **`readOnly` fields become rejected fields** — `n_required`, `stakes`, `actor` refuse when present; plus `additionalProperties: false` semantics (unknown key = error, never silently dropped) | JSON Schema §9.4 `readOnly`; OpenAPI "SHOULD NOT be sent as part of the request"; Pydantic `extra='forbid'` | 2 | 3 | 3 | ~10 lines. Converts three `NOTES` prose rules into checks. Small class, but the cheapest true conversion of prose-to-check in the whole list. |
| 5 | **Worked examples in the tool surface** — one canonical valid call per tool, chosen to show the conventions the types cannot (which optional fields co-occur, what a real `tripwires` map looks like) | Anthropic Tool Use Examples 72%→90%; Meta-Tool documentation ablation +10pp | 2 | 3 | 1 | Pure text; `tools --schema` gains an `example:` line per tool. **(c)=1: advisory only.** Cannot carry an invariant, but it is the cheapest thing with a measured effect on the semantic class. |
| 6 | **Enforcement vocabulary on invariants** — a refusal can resolve to `refuse` / `defer to queue` / `request approval` / `ask the model to re-examine`, rather than only `refuse` | AgentSpec `trigger`/`predicate`/`enforce` (>90% unsafe-execution prevention) | 2 | 1 | 3 | Larger: `Refusal` gains a mode, `loop.step` gains branches, and it touches the autonomy/deferral machinery. Defer until 1–4 land. |
| 7 | **Cross-field conditionals stated explicitly** — `kind == "executable"` on absence text ⇒ `closed_world` required, as a named predicate with its own error | JSON Schema `if`/`then`/`else`, `dependentRequired`; Eiffel `require` | 2 | 3 | 3 | Already partly enforced deeper in; the win is stating it at the boundary with an `invalid_args` message rather than letting it surface later as a gate refusal. |
| 8 | **Emit JSON Schema for the tool surface** *(the candidate on the table)* | MCP/OpenAI/Anthropic `inputSchema` | 1 | 2 | 2 | Addresses the 32% only, and §6.2 measured the format change (`TypedFields` vs `SameNL`) at +2pp/0pp with intervals including zero. **Worth doing for interoperability** — it is the lingua franca, and it is the prerequisite for `strict: true` if the framework ever moves off the CLI — **but it should not be sold as the fix for the declines.** |
| 9 | **Constrained decoding / `strict: true`** | XGrammar, OpenAI/Anthropic strict mode | 0 | 0 | 3 | **Not available**: the framework does not host the model (§2). Would eliminate the 6 name-slot errors and much of the 32% *if* the invocation surface moved from CLI to a tool-calling API. That is an architecture decision, not an interface tweak. |
| 10 | **Programmatic tool calling (typed Python stubs, agent writes code)** | Bitter Lesson of Tool Calling: +18.8pp at chain length ≥12 | 2 | 1 | **0** | **VETOED for the invariant floor.** Handing the agent an interpreter in the run's `cwd` means it can `git commit` directly, write the journal, or otherwise route around `loop.step`. The framework's premise is that it cannot. Viable only inside a sandbox whose only reachable names are the tool stubs — a large piece of work, and the numbers above were not measured under such a sandbox. |

**If only one thing is done: #1.** It is the cheapest, it is fully non-forgeable, it is supported by
the strongest effect size in the literature (+44pp / +42pp, p < 1e-4), and it attacks the largest
single bucket in the local data (16 of 53 declines that name nothing).

**#1 + #2 + #3 together are the SMAG pattern**, arrived at from three different literatures.

---

## 9. What I could NOT establish

Stated as failures, not softened.

1. **No study isolates tool-description serialisation with content held constant.** Nobody has run
   "same information, as JSON Schema vs as bespoke text vs as docstrings" on tool-call accuracy. The
   nearest evidence (§6.2, `TypedFields` vs `SameNL`, +2pp/0pp) is about *error messages*, from 50
   TextWorld games on two quantized ≤14B models. Treat "JSON Schema is a better rendering than the
   current bespoke text" as **unmeasured**, in either direction.
2. **No measurement of hide-vs-disable for LLM callers.** LSP chose show-with-reason; MCP chose
   republish-the-list. Which produces better agent behaviour is, as far as I can find, untested.
   Recommendation #3 picks LSP's side on argument (discoverability, small catalogue), not evidence.
3. **SMAG's +15.6pp cannot be decomposed.** Visibility filtering and code enforcement were adopted
   together. Whether the gain comes from the illegal tool being absent, or from the illegal call
   being blocked, or from state-dependent instructions, is not separable from the published ablation.
4. **No controlled source for "78% at 10 tools → 13.62% at 100+ tools".** It circulates widely; I
   could not trace it to a primary paper with a described protocol. The chance-corrected treatment
   (arXiv 2605.24660) does not support degradation at small catalogue sizes. **Do not cite the 78/13
   figure.**
5. **No measurement of design-by-contract declarations on LLM callers.** The Eiffel/Clojure-spec/
   refinement-type evidence base concerns human developers and static checkers. Its transfer to LLM
   tool calls is an assumption, not a finding.
6. **Could not extract the numbers from two relevant papers.** *Self-Reflective APIs* (arXiv
   2606.05037) and *DisasterBench* (arXiv 2605.27957) both failed PDF text extraction; no HTML
   version was reachable. Their titles and abstracts are on-topic and someone should read them
   properly before this document is treated as complete.
7. **The 72%→90% Tool Use Examples number is a vendor claim** on an undescribed internal benchmark:
   no n, no CI, no protocol, commercial interest. Its *direction* is corroborated by Meta-Tool's
   documentation ablation; its *magnitude* should not be relied on.
8. **Nothing was reproduced here.** Every number in this document is quoted from its source. No
   experiment was run against ancient-games. The one thing measured locally is the extraction of the
   53 decline reasons and the observation that 16 of them name nothing (two independent
   detectors, identical selection) — reproducible with the
   snippet at the top of this file.
9. **`readOnly` as a *validating* constraint could not be confirmed.** JSON Schema 2020-12 §9.4
   describes it as managed-by-owning-authority; I could not find spec text stating it affects
   validation outcomes, and the surrounding literature treats it as an annotation. Recommendation #4
   therefore proposes an explicit rejection check, not reliance on a validator.

---

## Supersedes / conflicts

This document does not supersede any existing finding in `docs/`. It **argues against the framing**
of the JSON-Schema-emission candidate as a fix for the observed declines (see row 8) — that
candidate should be re-scoped to "interoperability and a path to `strict: true`", not "reduces the
53". `docs/ABLATION_1.md` (H2/H4) and `docs/ABLATION_2.md` (H11/H13) were not re-read line by line
and may contain claims this document bears on; that check is not done.
