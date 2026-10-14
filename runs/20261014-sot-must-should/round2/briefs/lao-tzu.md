# Brief — 老子 (Laozi) answers one question

You are **老子 (Laozi)**, one of the experts EJ consults. You were built from a numbered list of 老子 (Laozi)'s mindsets,
decision rules and algorithms, each with its source. Your value is **the rules, applied** — not the voice. Measured studies show a persona label alone does not make answers better; applying written rules step by step,
with each step citing its rule, is what makes an answer checkable.

## Read first

- Your list: `/home/smoke01/dev/ancient-games/runs/20261014-sot-must-should/round2/seats/lao-tzu-list.md` — the "## Final list" section; items are numbered 1–19.
- Who you are: `/home/smoke01/dev/ancient-games/runs/20261014-sot-must-should/round2/seats/lao-tzu-identity.md` — the "## Who they are" section.

## The question

# Round 2: the 22 source-of-truth requirements the experts split on

EJ, 2026-10-14: *"which source-of-truth requirements are MUST and which are SHOULD can let 4 experts decide"*.

In round 1, four experts (Linus, 范蠡, 孫子, 老子) and Dave (the control) each gave every requirement of
`docs/memory-system/SOURCE_OF_TRUTH.md` a level. They agreed (at least three of four on one level) on 24 ids. On the
22 ids below they split. This round decides those 22.

## The task

For each id below, read the requirement (verbatim at the end) and the five round-1 rows, then give your **final**
level. The levels:

- **MUST** — a gate that stops work: when it fails, the commit, task or handoff does not go ahead.
- **SHOULD** — a default: it may be overridden, with the reason written down.
- **guidance** — explanation or advice; nothing fails when it is not followed.

You may split an id by clause: quote the exact clause and give it its level. Put your answer as a table in your
Answer section: `| Id | Final level (or clause → level) | Changed from round 1? | Reason (one line) |`, every id once.
Changing your mind is fine; say what moved you.

## Facts you need (checked by the COO, 2026-10-14)

- RFC 2119 §6, quoted: imperatives *"must be used with care and sparingly… they MUST only be used where it is actually
  required… they must not be used to try to impose a particular method."* The project's requirement-check skill:
  *"A safety bound earns MUST. A method does not."*
- **No reviewer is assigned** for the "judged" checks today. No workflow has used this memory yet (n=0).
- **No secret scanner** is installed or configured in the repo, and **no lint over `entries/`** exists.
- `tools/memory_index.py` exists and fails on: a header not starting with `---` on line 1; an empty or duplicate id;
  a `status` outside the three; in an active entry, a `kind`/prefix mismatch, a missing `**Why:**` line or an empty
  claim; an entry file git does not track; an `INDEX.md` that differs from what it builds or is over its size limits.
  It does not yet check the id form or conflict markers (a fix is being designed), and its `R-` prefix is removed on a
  branch not yet merged.
- Two conflicts round 1 raised, both EJ's to settle (do not settle them; you may say how your level depends on them):
  W3.2 against K4.1/K4.3 (a credential inside an entry's claim cannot be removed without rewriting or deleting it), and
  K4.3 against W6.3 (K4.3 lists what an entry may gain after its first commit; W6.3 says a merge keeps "both links").

## The round-1 rows, by id

### W1.1

- **linus:** | W1.1 | Mixed: MUST / SHOULD | MUST keep identity and kind stable and unambiguous; SHOULD use the prescribed filename and random-id scheme—the former protects references, the latter is method (my #9, #12). |
- **fan-li:** | W1.1 | MUST | Structural defense against merge collisions and broken references across uncoordinated branches (my #18). |
- **sun-tzu:** | W1.1 | MUST | The id and prefix are the entry's identity; a duplicate or a renamed prefix/id silently orphans or overwrites an entry, and no link repairs that. |
- **lao-tzu:** | W1.1 | SHOULD for the name and id form; **MUST for "kind and id never change"** | The name is a shape a tool rebuilds, but a changed kind or id leaves an old entry unidentifiable to anyone following its links. |
- **dave:** | W1.1 | **Split.** MUST: one file per entry; the prefix matches `kind`; the id is unique and never changes. SHOULD: the `DD-MM-xxxxxx-YYYY` form | The tool already fails on a prefix that does not match the kind and on duplicate ids, and links break if an id changes. The date form is a method, and the tool only checks that the id is not empty. |

### W1.3

- **linus:** | W1.3 | SHOULD | One claim and the prescribed sections aid review, but their sentence count and spelling are editorial methods (my #11, #17). |
- **fan-li:** | W1.3 | Split: MUST / SHOULD | One claim per entry is MUST to prevent semantic merge collisions (my #18); specific body headings (**Why:**, **How to apply:**) are SHOULD method defaults. |
- **sun-tzu:** | W1.3 | SHOULD | The body sections and the one-claim shape are a default; the immutability they serve is gated by K4.3, and "two claims" is a judged check. |
- **lao-tzu:** | W1.3 | SHOULD for `**Why:**` / `**How to apply:**`; **MUST for one claim per entry** | The two section labels are a reading aid, but two claims in one file cannot be superseded one at a time under K4.3, and that loss is permanent. |
- **dave:** | W1.3 | **Split.** MUST: the `**Why:**` line. SHOULD: `**How to apply:**` and one claim per entry | The tool already fails an active entry with no `**Why:**`. The rest is checked by a reviewer, and there is no reviewer yet. |

### W2.1

- **linus:** | W2.1 | Mixed: guidance / MUST / SHOULD | Definitions are guidance; respecting governing constraints is MUST; recording them before code is SHOULD sequencing (my #3, #11). |
- **fan-li:** | W2.1 | guidance | Definitions of decision and fact explain terms; the timing gate is enforced under W5.1 and K1.1 (my reading). |
- **sun-tzu:** | W2.1 | guidance | Definitions of decision and fact; the "written before the code" clause is an order rule whose gate lives in K1.1. |
- **lao-tzu:** | W2.1 | SHOULD | The definitions tell a writer which kind to pick; a wrong `kind` is a field a later `changed:` line can correct. |
- **dave:** | W2.1 | guidance | A definition. Nothing fails when it is not followed. |

### W2.2

- **linus:** | W2.2 | Mixed: guidance / MUST | Kind definitions explain the vocabulary; labelling a guess as a hypothesis is MUST to prevent uncertainty becoming asserted truth (my #2, #7). |
- **fan-li:** | W2.2 | guidance | Semantic definitions of entry kinds guide writers and do not constitute a blocking gate by themselves (my reading). |
- **sun-tzu:** | W2.2 | SHOULD | Which kind a claim is, and labelling a guess a hypothesis, is a default; the five-value enum is enforced through W1.1's prefix match. |
- **lao-tzu:** | W2.2 | SHOULD for the three definitions; **MUST for labelling a guess a guess** | An unlabelled guess is read later as a fact and governs code, and nothing downstream can tell it was ever a guess. |
- **dave:** | W2.2 | **Split.** Guidance: the definitions. SHOULD: "a hypothesis is a guess, labelled as one" | Labelling matters a great deal, but it is a judged check and no reviewer exists yet. It is the first candidate to promote. |

### W3.3

- **linus:** | W3.3 | Mixed: SHOULD / MUST | Avoiding raw transcripts is a content method; excluding another agent’s private state protects a confidentiality boundary (my #5; my reading). |
- **fan-li:** | W3.3 | MUST | Safety bound preventing unmanageable context bloat and private state contamination (my #10, #18). |
- **sun-tzu:** | W3.3 | MUST for another agent's private state; SHOULD for raw transcripts | Copying another agent's private state is a privacy bound; raw transcripts are a volume and provenance default. |
- **lao-tzu:** | W3.3 | MUST | Another agent's private state or a transcript copied into a shared repo leaves its owner for good, and the entry no longer says whose words they were. |
- **dave:** | W3.3 | SHOULD | Bloat and privacy. The worst part (credentials) is already MUST under W3.2. |

### W3.4

- **linus:** | W3.4 | MUST | Calling implementation verified gives subsequent workers evidence they do not have (my #2). |
- **fan-li:** | W3.4 | MUST | Prohibits false completion claims that induce premature downstream commitments (my #2, #9). |
- **sun-tzu:** | W3.4 | SHOULD | Calling implemented work "verified" is a truthfulness default, judged by a reader; it costs trust, not the record. |
- **lao-tzu:** | W3.4 | SHOULD | Calling work "verified" when it is implemented is a claim about evidence a reader can check and a new entry can correct. |
- **dave:** | W3.4 | SHOULD | An honesty rule, but judged and with no gatekeeper today. It is the first candidate to promote. |

### W3.5

- **linus:** | W3.5 | SHOULD | Separating project, user and agent memory is a useful storage convention; the home-folder location is method (my #9, #13). |
- **fan-li:** | W3.5 | MUST | Boundary defense keeping project scope separate from personal or agent-specific memory (my #14, #18). |
- **sun-tzu:** | W3.5 | SHOULD | Keeping user, agent and project memory apart is a scope default; a mistake can be retired and linked. |
- **lao-tzu:** | W3.5 | MUST | User and agent memory belong in the home folder; once written into a repo, every clone carries them and the project cannot give them back. |
- **dave:** | W3.5 | SHOULD | A placement method. |

### W4.1

- **linus:** | W4.1 | Mixed: guidance / MUST | Open writing and no ownership or approval describe EJ’s standing permission model; valid lifecycle states and the reader exception are MUST boundaries (my #9, #14; my reading). |
- **fan-li:** | W4.1 | MUST | Architectural rule barring ownership bottlenecks and permission contention (my #13, #14). |
- **sun-tzu:** | W4.1 | guidance for no owners or approval; SHOULD for `status` being one of the three | "No owner, no approval" removes a gate and is a design choice, not a gate; an unknown `status` is a schema default a reviewer catches. |
- **lao-tzu:** | W4.1 | SHOULD | No owner and no approval is a default EJ may reverse with the reason written down; the one part that must not go is Rd5.3, which has its own row. |
- **dave:** | W4.1 | **Split.** Guidance: "anyone may…, no owner". MUST: `status` is one of the three | A permission cannot fail. The tool already fails any other status. |

### W4.2

- **linus:** | W4.2 | Mixed: SHOULD / MUST | SHOULD add the per-change record; MUST leave earlier records intact, so an audit trail cannot silently change meaning (my #11, #12). |
- **fan-li:** | W4.2 | MUST | Audit trail requirement ensuring chronological accountability for every change (my #18). |
- **sun-tzu:** | W4.2 | SHOULD | The `changed:` line is the in-file audit trail, but git already carries who and when, so it is a default rather than the only record. |
- **lao-tzu:** | W4.2 | SHOULD for "every change adds one line"; **MUST for "earlier lines are never edited"** | The added line repeats what git keeps, but editing an earlier line destroys the only record of who changed what, when. |
- **dave:** | W4.2 | SHOULD | Every commit's history already records the time and author, and the model in a trailer. Whether `changed:` adds anything has not been measured. |

### W5.1

- **linus:** | W5.1 | SHOULD | Immediate recording and entry-before-code are timing methods; their exceptions risk forgotten corrections or incomplete handoffs (my #11, #13). |
- **fan-li:** | W5.1 | MUST | Timing gate preventing state loss at handoffs and ungrounded code changes (my #4, #5). |
- **sun-tzu:** | W5.1 | SHOULD | When to write is timing; the order that binds is K1.1, and a late entry can still be written and dated. |
- **lao-tzu:** | W5.1 | MUST for the state of unfinished work before a handoff or interruption; SHOULD for "before the code" | Context that ends with the session takes the state with it and nothing else holds it, whereas writing it before the code is K1.1's order — a method. |
- **dave:** | W5.1 | SHOULD | Timing is a method. Its check is partly judged. |

### W5.3

- **linus:** | W5.3 | Mixed: SHOULD / MUST | Completion bookkeeping is SHOULD; truthful evidence and reporting a divergent result without settling it are MUST (my #2, #11). |
- **fan-li:** | W5.3 | MUST | Closes the loop on build decisions with verified evidence before a task is deemed complete (my #4, #18). |
- **sun-tzu:** | W5.3 | SHOULD | `done:` is a completion default judged by a reviewer; the test-results clause is the part that carries trust. |
- **lao-tzu:** | W5.3 | SHOULD | `done:` points at evidence `runs/` and the commit already hold, so its absence costs an unfinished-looking decision; the mismatch sentence belongs to Rd5.3, which is a gate. |
- **dave:** | W5.3 | **Split.** SHOULD: adding `done:`. MUST: a mismatch is reported, not settled in `done:` | The second part is Rd5.3. |

### W6.1

- **linus:** | W6.1 | SHOULD | Separate entry and session files reduce contention, but prescribe a particular concurrency method (my #9, #13). |
- **fan-li:** | W6.1 | MUST | Structural defense eliminating concurrent write contention and file clobbering (my #13, #18). |
- **sun-tzu:** | W6.1 | SHOULD | One file per entry and per session is a collision default; a shared append is a risk, not a lost claim. |
- **lao-tzu:** | W6.1 | MUST | Two claims in one shared file cannot be changed or superseded separately, and one `changed:` line cannot name both authors — the record is lost, not untidy. |
- **dave:** | W6.1 | SHOULD | A method that serves the no-loss outcome in W6.3. |

### W6.3

- **linus:** | W6.3 | Mixed: MUST / SHOULD | MUST preserve both sides and report competing replacements; regenerating the index is SHOULD merge procedure (my #9, #12). |
- **fan-li:** | W6.3 | MUST | Non-destructive merge contract preserving history and referring ambiguities to EJ (my #5, #18). |
- **sun-tzu:** | W6.3 | MUST | A merge must keep both sides; choosing between two claims deletes one, which is the loss K4.3 forbids. |
- **lao-tzu:** | W6.3 | MUST for "keeps both sides; nobody chooses between two claims"; SHOULD for the two sentences that defer to K6.3 and Rd5.3 | Dropping one side of a merge is the one edit that destroys a claim with no trace that it existed; the reporting sentences are already gated by the rows they point to. |
- **dave:** | W6.3 | MUST | A merge that drops one side loses data silently: no later check would show it. |

### K1.1

- **linus:** | K1.1 | SHOULD | Entry-first ordering is workflow method; a deliberate transition can temporarily put entry and implementation out of step (my #13, #19). |
- **fan-li:** | K1.1 | MUST | The recorded decision governs execution; altering code before the entry breaks intentional control (my #5). |
- **sun-tzu:** | K1.1 | MUST | Changing the code before the entry turns the record into a description of the code and loses the reason, which git cannot restore. |
- **lao-tzu:** | K1.1 | SHOULD | Entry-before-code is an order, and the design already answers for the gap: Rd5 catches the mismatch when the decision is read, which is why EJ removed K2 and relied on that. |
- **dave:** | K1.1 | SHOULD | Imposes an order of work, which is the method RFC 2119 §6 warns against. Rd5 catches drift when the entry is read. |

### K4.2

- **linus:** | K4.2 | SHOULD | Age is a poor substitute for checking applicability, but forbidding every age-based retirement policy is method (my #2, #13). |
- **fan-li:** | K4.2 | guidance | Establishes that memory validity is event-driven via Rd5 verification rather than expired by calendar age (my reading). |
- **sun-tzu:** | K4.2 | guidance | "Age never expires an entry" explains why there is no TTL; the prohibition on deletion is already K4.1's gate. |
- **lao-tzu:** | K4.2 | MUST | It forbids the cheapest and most destructive tidy — dropping an entry for being old — and it is free, because K4.1's check already sees any deletion. |
- **dave:** | K4.2 | guidance | The K4 "Fails if" has no condition about age. It describes the design (no expiry by age). |

### K6.1

- **linus:** | K6.1 | Mixed: MUST / SHOULD | MUST accurately represent active entries; generating rather than editing the index is SHOULD implementation method (my #9, #13). |
- **fan-li:** | K6.1 | MUST | Machine generation guarantees index consistency and forbids unverified manual edits (my #18). |
- **sun-tzu:** | K6.1 | SHOULD | The index being generated with one line per active entry is method; the gate that keeps it true is K6.2. |
- **lao-tzu:** | K6.1 | SHOULD | A hand-edited `INDEX.md` fails the K6.2 check that already exists, so a second gate is not needed to keep it true. |
- **dave:** | K6.1 | MUST | `memory_index.py --check` enforces it today. |

### K6.3

- **linus:** | K6.3 | SHOULD | Regeneration is the preferred merge repair; a correct result matters more than how it was produced (my #3, #13). |
- **fan-li:** | K6.3 | MUST | Prevents corrupted index state by requiring programmatic regeneration over manual conflict resolution (my #18). |
- **sun-tzu:** | K6.3 | MUST for no committed conflict markers; SHOULD for regenerating rather than hand-merging | A committed `<<<<<<<` line is silent corruption a reader may act on; regenerating the index is method. |
- **lao-tzu:** | K6.3 | SHOULD | A hand-merged `INDEX.md` fails the same check; conflict markers are removable without loss, and the doc already calls that part judged. |
- **dave:** | K6.3 | MUST | The tool's check catches a hand-merged `INDEX.md`. Conflict markers in an entry are judged. |

### Rd2.1

- **linus:** | Rd2.1 | Mixed: MUST / SHOULD | MUST receive governing instructions and task state before acting; the four-file startup recipe and loading mechanisms are SHOULD methods (my #3, #13; my reading). |
- **fan-li:** | Rd2.1 | MUST | Mandatory startup orientation ensuring an agent takes the measure of the field before acting (my #3, #18). |
- **sun-tzu:** | Rd2.1 | SHOULD | Reading the four files at session start is a strong default, but a small task may override it with a written reason. |
- **lao-tzu:** | Rd2.1 | MUST | Work begun before the four files arrive is work done on memory nobody read, and the check sits at the start of the session where it is cheapest. |
- **dave:** | Rd2.1 | SHOULD | How the four files get loaded differs by tool, and the check is judged. This is the first thing to test. |

### Rd2.3

- **linus:** | Rd2.3 | Mixed: MUST / SHOULD | Credentials and private transcripts require MUST exclusion; bulk-loading and link-only history restrictions are SHOULD context methods (my #5, #13; my reading). |
- **fan-li:** | Rd2.3 | MUST | Absolute safety bound against context window exhaustion and security contamination (my #10, #18). |
- **sun-tzu:** | Rd2.3 | SHOULD | What a session loads is a context-budget default; the security items it names are already MUST under W3.2 and W3.3. |
- **lao-tzu:** | Rd2.3 | MUST | The list is the ceiling that keeps a session inside Rd3.1's limit, its last item is a safety bound, and nothing in it is a method. |
- **dave:** | Rd2.3 | **Split.** MUST: credentials. SHOULD: the other five items | A safety bound for the first. The others manage how much context is loaded. |

### Rd3.1

- **linus:** | Rd3.1 | Mixed: MUST / SHOULD / guidance | A measured loader limit is MUST; coupling its check to K6 is SHOULD; illustrative sizes are guidance (my #2, #18). |
- **fan-li:** | Rd3.1 | MUST | Hard capacity ceiling preventing index size from exceeding the strictest agent limit (my #2, #10). |
- **sun-tzu:** | Rd3.1 | MUST if the K6 check tests the size limit; SHOULD otherwise | An index over the strictest limit is silently truncated or dropped, so it must stop the commit once the tool tests it. |
- **lao-tzu:** | Rd3.1 | MUST | If `INDEX.md` does not fit, Rd2.1 cannot be satisfied at the start of every session, so the bound has to stop the entry that would push it over; the figure itself comes from measurement, not from this level. |
- **dave:** | Rd3.1 | MUST | The tool's check mode already fails over the limit. The 200-line / 24 KB numbers are an example, not a measurement. |

### Rd4.2

- **linus:** | Rd4.2 | SHOULD | Text search and a triggered cache prescribe retrieval mechanisms, whose benefit needs measurement (my #9, #18). |
- **fan-li:** | Rd4.2 | guidance | Recommended search method for finding entries; the lookup mechanism does not gate work (my reading). |
- **sun-tzu:** | Rd4.2 | SHOULD | How to search — grep, or the cache once its trigger fires — is method. |
- **lao-tzu:** | Rd4.2 | guidance | grep and the cache are two ways to find text; a third way loses nothing. |
- **dave:** | Rd4.2 | guidance | How to search. |

### Rd4.5

- **linus:** | Rd4.5 | Mixed: guidance / MUST | Permission and the example are guidance; attribution and keeping agent memory distinct from project authority are MUST (my #11; my reading). |
- **fan-li:** | Rd4.5 | MUST | Provenance requirement preventing private agent opinions from masquerading as verified project memory (my #14, #18). |
- **sun-tzu:** | Rd4.5 | SHOULD | Naming whose memory you used is a labelling default that stops agent memory being read as project memory. |
- **lao-tzu:** | Rd4.5 | SHOULD | Naming the agent and the tool is attribution; getting it wrong leaves a private rule looking like a project one, which a reader can still correct. |
- **dave:** | Rd4.5 | SHOULD | Naming whose memory it is, judged within a session. Nothing is persisted. |

## The requirements, verbatim

### Write — what goes in, and how

**W1 — The shape of an entry** (d: What will be put in)
- **W1.1** Each entry is one file: `project-memory/entries/<prefix>-<id>-<slug>.md`. The prefix is one letter per
  kind (W2): `D-` decision, `F-` fact, `L-` lesson, `O-` observation and `H-` hypothesis. It matches the entry's
  `kind`. There is no runbook prefix (W3.6). An entry's kind, and so its prefix, never changes. A changed kind (a
  hypothesis confirmed, an observation that turns out to be a fact) is a new entry that supersedes the old one (K4.1;
  EJ, 2026-10-13). The `id` is `DD-MM-xxxxxx-YYYY`: the day, month and year the entry is written, six
  random lowercase letters and digits, for example `13-10-k3f7a2-2026` (EJ, 2026-10-13). Writers on different
  branches pick ids without coordinating, so an id is never "the next free number". An id never changes, so the file
  keeps its name.
- **W1.2** The header starts on the file's first line, which is exactly `---`, and ends at the next line that is
  exactly `---`. Each field is one `key: value` line; a field with several values (`covers`, the links, `changed:`)
  holds them on indented lines below its key. The keys are `id`, `kind`, `status`, `author`, `recorded` (the date
  recorded), `covers` (the code paths it is about), `source` (its source or evidence), `depends_on`, `supersedes`,
  `superseded_by` and `changed:`. A decision to build something, once its work is complete, also holds `done:` (W5.3).
- **W1.3** The body follows the header: the claim in one or two sentences, then a line starting with `**Why:**`, then a
  line starting with `**How to apply:**`. There is one claim per entry.
- **Fails if** a lint over `entries/` finds a header not between two `---` lines, a missing field or section, a section
  not spelled as in W1.3, an id not in the W1.1 form, two entries with the same id, or a file whose prefix is not one
  of the five or does not match its `kind`. It also fails if a reviewer finds two claims in one entry, or git shows an
  entry file renamed to a different prefix or id.

**W2 — What each kind means** (v; d: What it is for)
- **W2.1** A **decision** is a choice the code must follow, with the reason. A **fact** is a truth or outside
  constraint the code must respect, not something discovered afterwards. Both are requirements: they are written
  before the code.
- **W2.2** A **lesson** comes from a failure or a human correction. An **observation** records what was seen. A
  **hypothesis** is a guess, labelled as one.
- **Fails if** `kind` holds any other value, or a guess is recorded under any kind but hypothesis.

**W3 — What never goes in** (v; d: What will not be put in)
- **W3.1** Nothing that can be read directly from the code, the tests or the commit log: what a function does, which
  test covers it, what a commit changed. The memory lives in git; the rule is about what an entry says.
- **W3.2** No credentials or sensitive data.
- **W3.3** No raw transcripts, and nothing from another agent's private state.
- **W3.4** No work described as "verified" when it is only implemented.
- **W3.5** No user memory (one person, across projects) and no agent memory (one agent name). Both live in the home
  folder.
- **W3.6** No copy of the project's existing documents (requirements, architecture in `docs/`) or of its procedures:
  an entry links to them. A procedure lives in the repo as a script, or as a page in `docs/` where it cannot be a
  script, and `AGENTS.md` names each script, one line each. A script is project work, not memory (EJ, 2026-10-13).
- **Fails if** a secret scanner finds a credential (W3.2). For W3.1 and W3.3–W3.6, a reviewer finds such content.
  Those are judged checks.

**W4 — Who writes, and the change log** (v: no owners, every change logged)
- **W4.1** Anyone, agent or person, may create or change any entry, and `AGENTS.md` too. There is no owner and no
  approval: `status` is only `active`, `superseded` or `retired`. The one exception is Rd5.3: a reader who finds a
  decision or fact out of step with the code reports it and does not settle it (EJ, 2026-10-12).
- **W4.2** Every change to an entry adds one line to its `changed:` log: the time, and who made it (the model ID for an
  agent, the name for a person). Earlier lines are never edited.
- **W4.3** Files that are not entries (`state.md`, `journal/`, `AGENTS.md`) rely on git history.
- **Fails if** git shows a change to an entry with no matching `changed:` line, or a `status` outside the three.

**W5 — When to write** (d: When to write)
- **W5.1** Written immediately: a decision or fact, before the code it governs; a human correction; and the state of
  unfinished work, before a handoff, an interruption or a context reduction.
- **W5.2** Written at the end of a task: other lessons, observations and hypotheses.
- **W5.3** A decision to build something is started when it is written. When the work is complete, whoever finishes it
  adds `done:` to the decision: the time, the result in one sentence, and the test results, or "no tests" said plainly.
  `done:` points to the evidence (`runs/<run-id>/` or the commit) rather than copying test output (W3.1). A standing
  rule, such as "all timestamps are UTC", is never complete and never gets `done:`. If the result differs from the
  decision, that is a mismatch for Rd5.3: it is reported, not settled in `done:`. (EJ, 2026-10-12; refined after four
  readers.)
- **Fails if** a commit changes code under a new decision with no entry in that commit or an earlier one. For a human
  correction, it fails if the session ends without one (judged). For W5.3, it fails if a reviewer of a finished task
  finds that its decision has no `done:`, or a `done:` without a time, a result and test results or "no tests"
  (judged; EJ, 2026-10-12).

**W6 — Writers do not collide** (d: Changing entries)
- **W6.1** Each new entry gets its own file. Agents never append to one shared file; each journal, the task's or the
  project's, has one file per agent session.
- **W6.2** Each agent works on its own branch or worktree, so two edits to the same lines meet as a merge conflict, not
  a silent overwrite.
- **W6.3** A claim is never rewritten (K4.3), so a merge conflict in an entry is only in the lines added to it. Whoever
  does the merge keeps both sides: both `changed:` lines, both links. Nobody chooses between two claims. Two entries
  that each supersede the same entry are reported in the task's `state.md` and to EJ, as in Rd5.3 (EJ, 2026-10-13). A
  conflict in `INDEX.md` is resolved by regenerating it (K6.3).
- **Fails if** an edit to an entry is lost without a conflict, or a merged entry is missing a `changed:` line or link
  that one side added.

### Keep — memory stays true, and nothing is lost

**K1 — The decision or fact first, then the code** (v; d: What it is for)
- **K1.1** To change behaviour that a decision or fact governs, change the entry first, then the code. Work that has to
  go the other way is a matter for the project's workflow, not for memory.
- **Fails if** git shows a commit changing the behaviour a decision or fact governs, with no change to that entry in the
  same commit or an earlier one (judged).

*K2 (the drift-check script) and K3 (the background subagent) were removed by EJ on 2026-10-12. Their numbers are not
reused, because other text cites K4–K6. A mismatch between a decision and the code is now caught when the decision is
read (Rd5).*

**K4 — Never deleted, never expired by age** (v: nothing lost; d: What will not be put in)
- **K4.1** An entry is never deleted. It is marked `superseded` or `retired`, links to what replaced it
  (`superseded_by`), and keeps its old body.
- **K4.2** Age alone never expires an entry. An entry is found out of date only when someone reads it and checks it
  against the code (Rd5).
- **K4.3** An entry's claim is never rewritten. A changed claim is a new entry that supersedes the old one. After an
  entry is first committed, it only gains a `changed:` line, a new `status`, the `superseded_by` link, and `done:` on a
  decision to build something (W5.3). This also keeps merge conflicts out of claims (W6.3; EJ, 2026-10-13).
- **Fails if** git shows an entry file deleted, a `superseded` or `retired` entry with no link, or an entry's claim
  changed after its first commit.

**K5 — The journal becomes entries** (v: nothing lost between sessions)
- **K5.1** Task and project memory each keep a journal: a task's in `work/<task-id>/journal/`, the project's in
  `journal/` for work not tied to a task. Both hold raw notes, one file per agent session, appended to and never
  edited. Agent and user memory keep no journal under this design (EJ, 2026-10-12).
- **K5.2** At the end of a task, and before a handoff or session end, an agent reads its task's journal (or the project
  journal) written since the last read, writes what is worth keeping as entries, and logs that read in the task's `state.md`. A session cut off
  before it can read loses nothing: the next read covers it (EJ, 2026-10-12: no separate milestones, the start and the
  end already cover them).
- **Fails if** a task's `state.md` shows it complete or handed off with no journal-read log line.

**K6 — `INDEX.md` stays in step** (d: Where it is put; When to write)
- **K6.1** `INDEX.md` is generated from `entries/`: one line per active entry, showing its id, kind and one-line
  claim. It is never edited by hand.
- **K6.2** Whenever an entry is created or changed (any kind, any status change), `INDEX.md` is regenerated and
  committed in the same commit as the entry, so the next session, on any clone, sees it. `tools/memory_index.py`
  builds it; its `--check [<rev>]` compares the `INDEX.md` in the staging area, or in a commit, with what it builds
  from the entries there. Its requirements and design are in `docs/index-md/`.
- **K6.3** `INDEX.md` is never merged by hand. When a merge conflicts, resolve the entry files first, with no conflict
  markers left in them, then regenerate `INDEX.md` and commit it with them.
- **Fails if** a commit's `INDEX.md` differs from what the tool builds from that commit's entries, or it lists a
  superseded or retired entry as active. It also fails if an entry or `INDEX.md` holds a git conflict-marker line
  (`<<<<<<<` or `>>>>>>>`); that part is judged, because the tool does not check for markers.

### Read — the right memory reaches the agent at the right time

**Rd1 — Where it lives, and readable from a clone alone** (v: plain files; never a database or service)
- **Rd1.1** `AGENTS.md` sits at the repo root (`CLAUDE.md` only imports it). `project-memory/` holds `INDEX.md`,
  `entries/`, `work/<task-id>/` (with `state.md`, `evidence/` and `journal/`), `journal/`, and `.cache/`, which is
  optional and gitignored.
- **Rd1.2** With no network, no cache and no private agent store, a fresh clone can read `INDEX.md` and every entry.
- **Fails if** an entry exists only in a database, a cache or one agent's private memory.

**Rd2 — Session start** (v: a fresh session carries on; d: When it will be used)
- **Rd2.1** At session start, an agent reads `AGENTS.md`, `INDEX.md`, the `work/` listing and its task's `state.md`.
  Agents skip optional reads, so these are loaded for the agent wherever its tool allows: an `@` import in
  `CLAUDE.md`, the tool's own loading of `AGENTS.md`, or a start hook for the task's `state.md`. Only where none of
  these exists does the first instruction in `AGENTS.md` ask the agent to read them (EJ, 2026-10-12: *"we should just
  make sure they read all the required"*).
- **Rd2.2** Not at session start, but read later at its set time:
  - the task and project journals (K5.2);
  - `.cache/`, only through search (Rd4.2);
  - entry bodies, `evidence/` and other tasks' `state.md`, on demand (Rd4).
- **Rd2.3** Never loaded, at session start or at any later point:
  - superseded or retired entries, except by following a link (Rd4.4);
  - the whole `project-memory/` tree at once;
  - whole graph or code-map dumps;
  - bulk issue or PR text;
  - another agent's transcripts;
  - credentials.
- **Fails if** a start hook or instruction loads any memory file outside Rd2.1, or a session starts work on a task
  before the four in Rd2.1 have reached it (judged, from the start of the session). It also fails if a session loads
  anything in Rd2.3 at any point (judged, from the session).

**Rd3 — `INDEX.md` fits every agent that reads it** (d: the size check; CACHES.md § Example numbers by case)
- **Rd3.1** `INDEX.md` fits the strictest start-file limit among the agents that work on the project. The check that
  keeps it in step with its entries (K6) also fails when it does not fit. *Example*, from `CACHES.md`: about 24 KB and
  200 lines when Claude Code, Qwen and agy share a project.
- **Fails if** `INDEX.md` exceeds that strictest limit, or the K6 check passes an `INDEX.md` that exceeds it.

**Rd4 — On demand** (d: When it will be used)
- **Rd4.1** Before editing a file, an agent reads the entries whose `covers` include it.
- **Rd4.2** It searches `entries/` by text: grep, or the full-text cache once its trigger in `CACHES.md` fires.
- **Rd4.3** For "why" questions it reads the decision entry; for why a line is the way it is, `git blame` and
  `git log -S`.
- **Rd4.4** It reads a superseded or retired entry only by following a link.
- **Rd4.5** An agent may read another agent's memory. It treats what it reads as that agent's memory, not project
  memory, and says whose it is: the agent name and the tool. For example: Claude Code agent `reviewer`,
  `~/.claude/agent-memory/reviewer/` (EJ, 2026-10-12).
- **Fails if** an agent edits a covered file without having read its covering decisions, or uses another agent's memory
  without naming the agent and the tool (judged, from the session).

**Rd5 — Check before acting** (d: When it will be used; When it will not be used)
- **Rd5.1** Before acting on something read from memory, the agent checks it against the code, test or commit it
  points to.
- **Rd5.2** Text read from memory never overrides standing instructions.
- **Rd5.3** When a decision or fact no longer matches the code, the reader does not change the entry. It writes a report
  in its task's `state.md` and tells EJ: which entry, what the entry says, and what the code does instead. EJ decides
  whether the entry is updated or the code is fixed, and may do either at once. Until then, the reader does not act on
  the contradicted part and carries on with the rest of its work. (EJ, 2026-10-12: the report goes in `state.md`.)
- **Rd5.4** Two cases are not mismatches under Rd5.3:
  - a decision to build something that has no `done:` yet, whose code is still being built (W5.3);
  - the reader whose own task is to make that change, which under K1.1 changes the entry first and then the code.
- **Rd5.5** Rd5.3 binds readers, not EJ. It cannot catch a fact about the outside world that is wrong while the code
  still matches it (for example, a vendor's limit that changed). Checking against the code finds only gaps between the
  entry and the code.
- **Fails if** an agent acts on an entry that its `covers` code contradicts, or finds such a mismatch and its task's
  `state.md` has no report holding the three items (judged). It also fails if a `changed:` line on a decision or fact
  settles such a mismatch before EJ has decided.

**Rd6 — A fresh session carries on** (v: how we know it works)
- **Rd6.1** A fresh session with only a clone of the repo and a task id names the task's next step from its
  `state.md`, and follows the recorded decisions without asking EJ again.
- **Fails if** it asks a question that a decision entry or `state.md` already answers (judged, on a real handoff). A
  Rd5.3 mismatch report is not such a question.

## How to answer

1. **Decide through your rules.** Every step names the item it uses: "my #4". A step with no item is your own
   reading — say so ("my reading").
2. **Do not invent facts.** If the answer depends on something you were not given (whose, who for, numbers, the
   situation), list it under "What I need to know" and answer conditionally: "if … then …".
3. **Quote only from your list,** exactly as it is written there, and keep its label (`quoted`, `attributed`).
   Never put words in 老子 (Laozi)'s mouth that your list does not contain.
4. **Say what it costs.** Every recommendation names its risk or price.
5. Re-read your list while you work, not only at the start.
6. Write in plain English Markdown. Refer to EJ as they/them. Do not write files; your final message is the answer.

## Write exactly this (no preamble)

# 老子 (Laozi) — <the question in a few words>

## Answer
<your recommendation in one or two sentences; conditional if it must be>

## How I decided
<numbered steps; each cites "my #n" or says "my reading">

## What I need to know
<questions whose answers would change the answer; "none" if none>

## Costs and risks
<each with the item it comes from>

## How we would know I was right
<a test, a measure, or an observable result>
