I'll read the brief first.
# 老子 (Laozi) — which requirements are MUST, which SHOULD, which guidance

## Answer

MUST only where failing destroys a record nothing else keeps, or puts a secret or another person's private state into a committed repo, or is one of the four Read-side bounds that now stand where EJ's removed K2 stood — that gives **17 of 46 ids, plus 7 ids that carry a MUST clause inside a SHOULD**, and SHOULD where the requirement is a shape or an order and another method serves equally well. Conditional on the one thing I was not told: **if no reviewer is ever assigned for the judged checks, the judged MUSTs (Rd2.1, Rd2.3, Rd4.1, Rd5.3, Rd6.1 and about five more) drop to SHOULD**, and the design then has exactly one gate — `tools/memory_index.py --check`.

| Id | Level | Reason (one line) |
|---|---|---|
| W1.1 | SHOULD for the name and id form; **MUST for "kind and id never change"** | The name is a shape a tool rebuilds, but a changed kind or id leaves an old entry unidentifiable to anyone following its links. |
| W1.2 | SHOULD | Spelling the header and listing the keys is one way to hold the same facts; only the `changed:` and `done:` values inside it are gated elsewhere (W4.2, W5.3). |
| W1.3 | SHOULD for `**Why:**` / `**How to apply:**`; **MUST for one claim per entry** | The two section labels are a reading aid, but two claims in one file cannot be superseded one at a time under K4.3, and that loss is permanent. |
| W2.1 | SHOULD | The definitions tell a writer which kind to pick; a wrong `kind` is a field a later `changed:` line can correct. |
| W2.2 | SHOULD for the three definitions; **MUST for labelling a guess a guess** | An unlabelled guess is read later as a fact and governs code, and nothing downstream can tell it was ever a guess. |
| W3.1 | SHOULD | Writing what the code already says is advice about what is worth writing; the duplicate goes with the entry's own history and nothing is lost but effort. |
| W3.2 | MUST | A credential written into a committed entry has left; deleting the file does not recall it. |
| W3.3 | MUST | Another agent's private state or a transcript copied into a shared repo leaves its owner for good, and the entry no longer says whose words they were. |
| W3.4 | SHOULD | Calling work "verified" when it is implemented is a claim about evidence a reader can check and a new entry can correct. |
| W3.5 | MUST | User and agent memory belong in the home folder; once written into a repo, every clone carries them and the project cannot give them back. |
| W3.6 | SHOULD | Linking to a document instead of copying it is a maintenance choice; a copy goes stale, it is not lost. |
| W4.1 | SHOULD | No owner and no approval is a default EJ may reverse with the reason written down; the one part that must not go is Rd5.3, which has its own row. |
| W4.2 | SHOULD for "every change adds one line"; **MUST for "earlier lines are never edited"** | The added line repeats what git keeps, but editing an earlier line destroys the only record of who changed what, when. |
| W4.3 | guidance | It says which files lean on git history and nothing else; no input fails against it. |
| W5.1 | MUST for the state of unfinished work before a handoff or interruption; SHOULD for "before the code" | Context that ends with the session takes the state with it and nothing else holds it, whereas writing it before the code is K1.1's order — a method. |
| W5.2 | SHOULD | A lesson missed at the end of a task is still in the journal, so what is lost is when it was noticed, not the note. |
| W5.3 | SHOULD | `done:` points at evidence `runs/` and the commit already hold, so its absence costs an unfinished-looking decision; the mismatch sentence belongs to Rd5.3, which is a gate. |
| W6.1 | MUST | Two claims in one shared file cannot be changed or superseded separately, and one `changed:` line cannot name both authors — the record is lost, not untidy. |
| W6.2 | SHOULD | A branch or worktree per agent is one way to make two edits meet; the damage is caught by W4.2's `changed:` line, and the price is that the writer must read the conflict. |
| W6.3 | MUST for "keeps both sides; nobody chooses between two claims"; SHOULD for the two sentences that defer to K6.3 and Rd5.3 | Dropping one side of a merge is the one edit that destroys a claim with no trace that it existed; the reporting sentences are already gated by the rows they point to. |
| K1.1 | SHOULD | Entry-before-code is an order, and the design already answers for the gap: Rd5 catches the mismatch when the decision is read, which is why EJ removed K2 and relied on that. |
| K4.1 | MUST | Deleting an entry takes the link that said which entry replaced it; git keeps the bytes, not the succession. |
| K4.2 | MUST | It forbids the cheapest and most destructive tidy — dropping an entry for being old — and it is free, because K4.1's check already sees any deletion. |
| K4.3 | MUST | A rewritten claim destroys the only record of what was believed and when, and it is the one edit that turns a merge conflict into a loss. |
| K5.1 | SHOULD for the two paths; **MUST for "appended to and never edited"** | Where the journal sits is a layout, but editing an earlier line destroys the raw note that K5.2 exists to rescue. |
| K5.2 | SHOULD | Skipping the read leaves the journal in place, so the next read still finds the notes; what is lost is timeliness. |
| K6.1 | SHOULD | A hand-edited `INDEX.md` fails the K6.2 check that already exists, so a second gate is not needed to keep it true. |
| K6.2 | MUST | `INDEX.md` is what a fresh session reads (Rd2.1), and `tools/memory_index.py --check` is the check that exists today — the one cheap and complete gate here. |
| K6.3 | SHOULD | A hand-merged `INDEX.md` fails the same check; conflict markers are removable without loss, and the doc already calls that part judged. |
| Rd1.1 | SHOULD | The paths are a layout; a project that files things elsewhere pays in wrong instructions, not in lost records. |
| Rd1.2 | MUST | This is the promise that a clone alone carries the memory; an entry living only in one agent's store is gone for everyone else and no check sees it. |
| Rd2.1 | MUST | Work begun before the four files arrive is work done on memory nobody read, and the check sits at the start of the session where it is cheapest. |
| Rd2.2 | guidance | It is a timing table for later reads; reading a journal early costs context, not a record. |
| Rd2.3 | MUST | The list is the ceiling that keeps a session inside Rd3.1's limit, its last item is a safety bound, and nothing in it is a method. |
| Rd3.1 | MUST | If `INDEX.md` does not fit, Rd2.1 cannot be satisfied at the start of every session, so the bound has to stop the entry that would push it over; the figure itself comes from measurement, not from this level. |
| Rd4.1 | MUST | Editing a covered file without reading the decisions that cover it is how code and memory part company, and afterwards nothing shows that it happened. |
| Rd4.2 | guidance | grep and the cache are two ways to find text; a third way loses nothing. |
| Rd4.3 | guidance | `git blame` and `git log -S` are the tools that answer "why"; naming them is advice, and no input fails against it. |
| Rd4.4 | SHOULD | Reading a superseded entry by link is the default that keeps a stale claim out of the working context; another way costs context, not a record. |
| Rd4.5 | SHOULD | Naming the agent and the tool is attribution; getting it wrong leaves a private rule looking like a project one, which a reader can still correct. |
| Rd5.1 | MUST | This is the check that now carries what the removed K2 carried: acting on a stale entry is the one way memory changes behaviour silently. |
| Rd5.2 | MUST | Memory text outranking standing instructions is a hijack with no downstream signal, and the standing instruction is the higher authority by definition. |
| Rd5.3 | MUST | A reader who settles a mismatch writes an unchecked claim into the record of truth; report-and-wait is what stops whoever noticed last from deciding. |
| Rd5.4 | guidance | It names two cases that are not mismatches, so it can fail nothing; it is there to stop Rd5.3 being applied too widely. |
| Rd5.5 | guidance | It says what Rd5.3 cannot catch, so it binds no reader; a statement about a rule's reach is not the rule. |
| Rd6.1 | MUST | It is the one requirement under which the design can be said to work at all, and a handoff that cannot be resumed does not go ahead. |

## How I decided

1. **My #2** — 知足不辱，知止不殆, 禍莫大於不知足 — sets the size of the answer before the answer itself. The scarce thing here is the word MUST: RFC 2119 §6 says it is *"used with care and sparingly."* So my first question was never "what does W1.1 mean" but "how many gates can this project afford to keep". Answer: few, and know where to stop.
2. **My #1** — 損之又損，以至於無為 — is the order of work. I first read every requirement as MUST, because the document's own `**Fails if**` lines make them all look like gates, and then took the MUSTs away one at a time.
3. **My #4** — 為者敗之，執者失之 — is the test I used when removing them. A `Fails if` clause is the *way* a requirement is checked; acting on it and gripping it turns a check into a gate and loses the requirement. The brief's own rule says the same: *"A safety bound earns MUST. A method does not."* (my reading of the application; the quoted words are `quoted`, ch. 64 and ch. 29.)
4. **My #11** — 反者道之動，弱者道之用, 正言若反 — caught the requirement that reads most permissive. W4.1 ("anyone may change any entry, there is no owner and no approval") sounds like a permission; it is the thing EJ removed twice, and what keeps it standing is the Rd5.3 exception inside it, which is its own row.
5. **My #13** — 善有果而已,果而不得已, 其事好還 — decided the borderline cases. Things tend to come back: a requirement nothing can check cheaply becomes a thing everyone ignores, and an ignored MUST is worse than a SHOULD because it still looks binding. So for each candidate MUST I asked whether a check exists today (`tools/memory_index.py`) or a person is at a named moment; if neither, the level drops unless the loss is unrecoverable.
6. **My #19** — 以深為根，以約為紀, 苟免於咎 — set the size of each deviation. Restraint is the rule and the duty is to escape blame, not to pass every gate: that is why an overridable default (SHOULD) with the reason written down is the right size for a shape or an order, and a stopping gate (MUST) is right only where blame and loss are both unrecoverable.
7. **My #17** — 三十輖共一轂，當其無，有車之用; 故有之以為利，無之以為用 — put the level on the operative sentence and not on the prose around it. The words do not say to remove anything; that would be an application. So W4.3 (which files rely on git) and Rd5.5 (what Rd5.3 cannot catch) are the shape of the vessel, not a requirement in it: guidance. (my reading of the use; the words are `quoted`, ch. 11.)
8. **My #12** — 將欲廢之，必固興之 — is what I ran before every demotion: name the case that breaks. The cases that broke through were deleting by age (K4.2), an unlabelled guess (W2.2), a secret written once (W3.2), a context that ended mid-task (W5.1), and a reader who quietly fixed a mismatch (Rd5.3). Those stayed MUST. The case that broke the rest — a shape, an order, a place to put things — is a case another method answers.
9. **My #3** — 功遂身退，天之道; 功成而弗居 — is the precedent already in the document: EJ withdrew K2 and K3 when their work was done, and the numbers were not reused. So a rule can be withdrawn, and W5.3's `done:`, W6.2's branch rule and W3.6's script rule were demoted on that precedent, with their prices named below.
10. **My #8** — 知不知上，不知知病 — is the label on the whole answer. n=0: no run has used this memory, so every row is a reading, not a measurement. I say which rows move the moment a lint over `entries/` exists (W1, W2) and which row is decided by measurement rather than by me (Rd3.1).
11. **My #9** — 江海所以能為百谷王者，以其善下之; 是以聖人處上而民不重 — kept the reviewer load small. The Read-side MUSTs put a person between the agent and its work, which is the opposite of W4.1; I therefore hold them to four checks (Rd2.1, Rd4.1, Rd5.1, Rd5.3) and push everything else down a level.
12. **My #10** — 我有三寶，持而保之。一曰慈，二曰儉，三曰不敢為天下先 — names what this answer is built on (my reading of the application): nothing private in a shared repo (W3.2, W3.3, W3.5), nothing lost (K4), and memory not made the centre of the design — which is why I add no owner, no approval gate and no fixed number of my own. 今舍慈且勇，舍儉且廣，舍後且先，死矣: give up one of the three while keeping the other two and the design starts losing things quietly.
13. **My #6** — 為之於未有，治之於未亂 — with **my #7** — 民之從事，常於幾成而敗之，慎終如始，則無敗事 — sets when to do this and when to look again. Levels are cheapest to assign now, at n=0, before the lint exists; but the failure of a document like this comes at the end, in the rows nobody revisits, so the W1 and W2 rows are to be re-read once the tool can check them.

## What I need to know

1. **Who is the reviewer for a judged check, and are they assigned or hoped for?** If nobody is assigned at a named moment, the judged MUSTs cannot be gates — they become SHOULD, the writer has no one to stop them, and the design rests on `memory_index.py --check` alone.
2. **What is the measured strictest start-file limit for Rd3.1, per agent?** If one line per active entry (K6.1) cannot fit that limit at the growth rate real entries arrive, then the *shape* is what must change — retire entries from `INDEX.md` sooner — and the bound stays where it is. The bound is a MUST; the one-line-per-entry shape is not, and I cannot tell which fails first without the measurement.
3. **Will the W1 and W2 rows carry MUST now, with the gate waiting for a lint that does not exist, or SHOULD until it exists?** If MUST now, then W1.1, W1.2, W1.3 and W2.1 become the requirements with no way to fail today, and the honest thing is to write the expected lint output down beside them.
4. **Does any product keep `project-memory/` outside the repo, or uncommitted, for any period?** If so, K4.1, K4.3 and Rd1.2 lose their basis — git would be holding the record only sometimes — and their level changes with the answer.

## Costs and risks

- **A smaller MUST set means some failures are caught later, by a reader, or not at all.** That is the price of 知止不殆 (my #2) and of少則得 (my #14): a careless writer is not stopped at the commit.
- **Marking the format SHOULD means a second writer may choose another shape**, and the lint must then accept two shapes. The cost of refusing to impose a method is a tool that has to be generous — RFC 2119 §6's point, which I accept here (my #4).
- **K4.1 and K4.3 against Rd3.1.** Never delete, never rewrite, one line per active entry: entries accumulate and the index grows toward the measured ceiling. The only exit the design offers is retire-with-link, which costs a writer per old entry. These two bounds pull against each other and the pull shows up in Rd3.1's measurement (my #2: know where to stop).
- **Every judged MUST spends a reviewer's attention on every commit, and judged MUSTs are the ones most likely to be ignored** — my #13: 事好還, things tend to come back. An ignored MUST is worse than a SHOULD because it keeps looking binding while binding nothing (my reading).
- **Rd5.3 puts a decision with EJ.** That is one person, and W4.1 removed concentration elsewhere in the same document. If EJ is unavailable, the mismatch reports queue (my #9: put yourself behind — the ones above carry the weight of the ones below).
- **Nothing here was measured.** n=0, per my #8: I do not know that I know. The W1/W2 rows and Rd3.1 are the ones I would expect to move first.

## How we would know I was right

- **The first 20 real commits.** Count how many MUSTs actually stopped a commit, and how many SHOULDs were overridden with a reason written down. If fewer than 2 of 20 commits are stopped by a MUST, the level is decoration and the word has gone back to meaning "advice" (少則得). If nearly every commit is stopped, the level is too low and the work will route around it — the workaround, not the failure, is the signal (my #12: about to abolish it, first raise it — watch for someone who starts saying "the shape requires").
- **Three real handoffs (Rd6.1).** Count the questions asked that a decision entry or a `state.md` already answered. One or more means the read-side MUSTs were not met in practice, whatever level they carry. A Rd5.3 mismatch report does not count.
- **One sentence to watch for:** an agent refusing a change because "the entry format requires it". That is a method being treated as a bound, my #4's 為者敗之, and it means the level is wrong (my reading).
- **Re-read at:** the first 20 commits, or the day the lint over `entries/` exists, whichever comes first — with the W1, W2 and Rd3.1 rows re-decided then, and n=0 recorded until then (my #7: the failure of this document comes at the end).
