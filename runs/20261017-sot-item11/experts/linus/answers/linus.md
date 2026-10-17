# Linus Torvalds — Merge, kit, and reader limits

## Answer

- **A — Keep the explicit correction; do not resurrect the stale path.** Replace W6.3a with: “Keep both sides’ `changed:` lines and links, and every still-valid `covers` path; an explicit committed removal or replacement, recorded with its own `changed:` line, wins over an unchanged opposite branch and is not resurrected.” Change `fails_if` accordingly: a merge fails if it loses a `changed:` line, link, or retained valid path, or restores a path explicitly removed or replaced without preserving the correcting `changed:` line.

- **B — Include the executable dependencies in the kit.** Extend the kit list to include `tools/memory_index.py` and `docs/index-md/`, including its requirements and design; a project lacking either is non-compliant, and a missing checker must fail the check rather than silently skip `check: tool`.

- **C — Use one owner-maintained, machine-readable limits file.** Add `docs/memory-system/reader-limits.yaml` to the kit, with one record per agent, installed version, start path, scope, metric and unit, limit or unknown value, basis (`interim`, `documented`, or `measured`), repository-local evidence, and measurement date; move the existing 200-line/24,000-byte example into one `interim` record, make Rd3.1a, Rd3.1b, and `docs/index-md/` reference it, and make missing or malformed configuration an error.

- **D — Count agents that actually load `INDEX.md` at session start.** Replace “agents that work on the project” with “every agent/version/configuration on which this project loads `INDEX.md` at session start”; an agent merely working in the repository does not constrain the file unless it receives it through a start-file path, and absence of a published limit remains `unknown`, not unlimited.

- **E — Change the tool in its own run and measure before retiring the interim value.** Measure now on every owner-declared installed engine, version, profile, and load path, recording the first observable truncation, skip, or omission with repository-local evidence; remeasure when the engine, configuration, or instruction chain changes, and do not treat documented figures or code inspection as engine measurements.

## How I decided

1. “Do both” is appropriate when neither approach is known to be better, but K4.3 establishes that an explicit path correction has meaning; retain its history in `changed:` while treating `covers` as corrected data (**my #8**, **my #9**).
2. A merge must explain the durable record and why an apparently conflicting change exists, rather than hiding that decision in an automatic union (**my #11**, **my #12**).
3. A checker that is not shipped with the requirements is not part of the repeatable design; it is merely a claim that somebody once had such a tool (**my #2**, **my #19**).
4. The project owner, who knows the supported readers and their operational details, should select that matrix; putting it in structured data lets the checker consume the same facts that reviewers inspect (**my #4**, **my #6**, **my #9**).
5. The governing population should be the actual load path being constrained, not an irrelevant list of every tool used near the repository (**my #10**, **my #13**).
6. Tool support needs real code and boundary tests, while any claimed replacement for the interim example needs measured evidence and stated costs (**my #2**, **my #18**, **my #19**).
7. Separating implementation from measurement keeps each change reversible and independently checkable (**my #5**, **my #13**).
8. **Proposed change to the pattern:** add an outcome criterion that every declared engine/version/load path demonstrably loads the intended portion, then execute inventory, measurement, configuration, and implementation as separate timestamped pieces (**my reading**, supported by **my #2**, **my #18**, and **my #19**).

## What I need to know

- Which agents, exact installed versions, profiles, and session-start paths are officially supported, including whether `INDEX.md` participates in a shared instruction-chain budget?
- What merge rule is required when both branches independently remove, replace, or re-add the same path? This does not change the untouched-side case, but it changes the complete merge grammar.

## Costs and risks

- **A:** A mistaken explicit removal can hide a still-valid path. The independent `changed:` line and merge fixture make the decision visible and reviewable (**my #5**, **my #11**, **my #18**).
- **B:** Consumers must carry and version more files, and incomplete installations fail closed. That is bootstrap work, but accepting an uncheckable kit would make the requirements unverifiable (**my #2**, **my #13**, **my #19**).
- **C:** Owner-maintained limits can become stale as engines change, while schema handling adds code. Versioning, evidence dates, and review of the basis field are the price (**my #7**, **my #9**, **my #18**).
- **D:** A wrong load-path inventory could omit an affected reader. Reject unknown configurations rather than treating them as harmless (**my #7**, **my #16**, **my #18**).
- **E:** Boundary measurements require an engine/version/configuration matrix and consume time; combined instruction chains need more than an `INDEX.md`-only test. Running this as separate pieces limits rework but delays retiring the interim example (**my #5**, **my #13**, **my #18**, **my #19**).

## How we would know I was right

- A merge fixture where one branch corrects a path and the other leaves it unchanged produces the correction, preserves both sides’ `changed:` lines and links, and does not restore the stale path.
- A clean project missing `tools/memory_index.py` or required `docs/index-md/` files fails the kit/tool check explicitly.
- Config tests cover missing fields, unknown values, each supported metric, per-file versus shared scope, and combined instruction-chain accounting; a reviewer can identify the evidence and date that changed an entry from `interim` to `measured`.
- For each declared engine/version/load path, fixtures immediately below, at, and above the observed boundary produce the recorded load result. The generated `INDEX.md` passes every applicable measured constraint, and the real project instruction chain demonstrably retains the intended index content.