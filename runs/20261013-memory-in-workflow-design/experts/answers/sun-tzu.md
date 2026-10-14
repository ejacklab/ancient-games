# 孫子 (Sun Tzu) — does the agent know memory by itself, and should the method be told?

## Answer

**Q1: No — not by the model's own judgement.** The reads that happen are the ones the harness forces; every read left to the model is *not measured* or measured poor (report §1 "Across the tools", §2 "Where the evidence is thin"). The report's "partly" is the harness working, not the agent knowing.

**Q2: Partly — yes, one change to §4, but not by adding details of how agents use memory.** Replace §4's project-memory paragraph (L494–510) with a pointer to `docs/memory-system/SOURCE_OF_TRUTH.md`, and in that same paragraph write the half neither earlier expert put into his proposal: the *negative* half — memory reaches a node by brief, import or start hook, never as a request to read it, and the node's brief names what it must **not** receive; no verifier gets a worker's reasoning or an entry that carries it. Conditional: if SoT will not be built before the next workflow that needs project memory, keep §4's three files marked "until SoT is built" and change only that sentence (范蠡's interim, report §6.2).

## How I decided

1. The question is a reckoning before a commitment. My #1, `quoted`: 「多算勝，少算不勝，而況於無算乎？」 — "More wins, fewer does not, how much less none at all?" The report has done that reckoning on the tools (T1–T9) and the evidence (E1–E12). Its own count is thin exactly where the question sits.

2. My #1's comparison is between two sides. Here the sides are the **design** (what the harness loads) and the **model** (what it chooses mid-task). The report's own tables separate them: T1–T8 are harness or documented behaviour, T9 and Codex memories are *not measured* (report §1, §4). That split decides Q1.

3. My #4, `quoted`: 「故曰：知彼知己，百戰不殆；不知彼而知己，一勝一負；不知彼不知己，每戰必殆。」 We know the loading side; we do not know the choosing side (report §2, Q1). "One win, one loss" is the report's "partly" — and it is not the model that is doing the knowing.

4. My #2, `quoted`: 「昔之善戰者，先為不可勝，以待敵之可勝。不可勝在己，可勝在敵。」 What reaches a node through its brief, an import or a hook is in our hands. Whether the model opens an optional file is the other side's. So the method cannot be built on "the agent will use memory well"; it can only be built on the part we own. Same item, second half: 「無恃其不來，恃吾有以待之；無恃其不攻，恃吾有所不可攻也。」

5. My #12, `quoted`: 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 This is my reason for Q2 being *partly*, not *yes*. "How agents use memory" is 責於人 — demanding good memory judgement from the model. The method's lever is 勢: which file, which scope, which engine, what is loaded at start. §4 should set the position, not describe the agent's mind.

6. My #13, `quoted`: 「途有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受。」 O6 (Linus) and O7 (范蠡) both say what a node **must read**. Neither says what it **must not be given**. The report's M13 and 范蠡's own last cost both name the verifier blind spot, and §4 already applies that principle to a worker's notes (L484–485) but not to project memory. That omission is the road not taken, and it is what I add.

7. My #3, `quoted`: 「凡用兵之法，全國為上，破國次之」 and 「不戰而屈人之兵，善之善者也。」 A per-node copy of SoT's rules is a second, broken copy of one accepted design; the pointer keeps it whole. My #8, `quoted`: 「故兵聞拙速，未睹巧之久也」 — the small fast form beats the perfect long one. So I side with 范蠡's pointer against Linus's per-node contract (§5, O6 vs O7), for a different reason than his: one whole copy, not his "timing".

8. My #16, `quoted`: 「約束不明，申令不熟，將之罪也；既已明而不如法者，吏士之罪也。」 A delivery sentence that is written but not checked is care that cannot command. This is why the one change must carry both halves in one paragraph: delivery, and the denial. It is also where I partly correct O7's smallest form — a sentence about loading without the denial clause is half an order.

9. My #5, `quoted`: 「非利不動，非得不用，非危不戰」; and my #6, `quoted`: 「是故智者之慮，必雜於利害，雜於利而務可信也，雜於害而患可解也。」 The advantage of *more* memory detail is not established: E4's developer-file gain has p=21%, E10's gain is on tasks selected because injection helped (v1 correction, §2), and no study measures auto memory (§7 Q1). The part that does not depend on that unmeasured gain is deterministic delivery and explicit denial. I change only that part.

10. My #15, `quoted`: 「愛民，可煩也」 — "loving the people, he can be harried." A designer who gives every node every memory it might want hands the difficulty a handle; the report's E7 is that handle. So the direction of the change is to narrow, never widen. This agrees with 范蠡's rule but stands on a different item than the one he cited.

11. My #17, `quoted`: 「故策之而知得失之計，作之而知動靜之理，形之而知死生之地，角之而知有餘不足之處。」 The way to learn the other side is to act on it. Linus's matched-task test (§6.1, report §7 Q9) is that probe, and my #11, `quoted` — 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也」 — says the count must come from the engines' own records and from our own runs, not from vendor numbers (E8, E12 are *unproven*) or from studies on other models (E5 is GPT-4o-mini).

12. Therefore the one change, in one place: **§4**. Its project-memory paragraph becomes a pointer to `SOURCE_OF_TRUTH.md` plus one sentence with two halves — *a node's memory arrives by brief, import or hook and never as a request to read it; the brief names what the node must not receive, and no verifier gets a worker's reasoning or an entry that carries it.* The pointer is Linus's and 范蠡's; the denial half is mine.

## What I need to know

1. **Will `SOURCE_OF_TRUTH.md` be built before the next designed workflow that needs project memory?** If yes, the pointer leads somewhere. If no, 范蠡's interim applies and the pointer alone is a plan with fewer 算 than it looks (my #1; F1).
2. **Do your workflows use Codex, agy or opencode nodes, or Claude only?** If non-Claude nodes are used, M14 bites and the delivery half matters now; if not, it is cheap insurance.
3. **Will you accept a matched-task test, and may it run before the change is written?** If yes, run Linus's test narrowed to delivery (§6.2) before enlarging anything; if no, the delivery-and-denial change still stands, because it constrains what reaches a node and needs no new evidence.
4. **Whose is the memory this node needs — task, project, agent, or user?** §4 and SoT treat these differently, and the answer changes what the brief names and what it denies. I was not given this per node.

## Costs and risks

- **Brief preparation, input tokens and checking time; amount *not measured*** (Linus, §6.1; O6 cost). From my #5: I am moving with the advantage only partly established, and from my #6: the harm side is that time spent on unneeded contracts is not recovered.
- **The denial clause is carried by the designer, not enforced by the method** — 范蠡's cost that "the method will not prompt for it" stands unless it becomes a line in the node's fields. From my #16: an order written and not checked is the general's fault if a verifier later receives reasoning. This is M13, still *not measured*.
- **Until SoT is built, the pointer leads to nothing** (F1, §6.2). From my #1: a store without entries is closer to 無算 than to 多算.
- **Removing §4's three files may strip the only concrete instruction an existing run uses.** That is why 范蠡's interim is the fallback, not a compromise.
- **Narrowing can omit a needed entry** — 范蠡's last cost, that "some nodes' memory needs go unstated". From my #13: the road not taken has a price; the denial half raises it deliberately.
- **Built-in memory keeps running beside the design** (T2, T3, T6; O4 left open). My change does not touch it. From my #4 and #10: that is an unknown left on the board, not a settled front.

## How we would know I was right

- **On the next designed workflow that needs project memory:** every must-read memory reaches its node by brief, import or hook (visible in the design files), no node brief asks the model to read an optional file, and no verifier brief names a worker's reasoning file or a reasoning-bearing entry. This is close to 范蠡's first test (§6.2, "grep the next three design files"), widened by the denial check.
- **The delivered-versus-ask-only comparison** (Linus's test, narrowed to one variable by 范蠡): on matched repository tasks, count missed reads, memory mistakes, tokens and elapsed time. My #17: probe, then read the signs.
- **A fresh-session handoff** (SoT Rd6.1): a fresh session with only a clone and a task id names the next step from `state.md` and does not ask EJ a question the record already answers. If it cannot, the delivery half failed.
- **I am wrong if:** the next three design files still cite §4's three files; or a verifier receives reasoning; or a node misses an entry its task needed while its brief said nothing either way. And if no Codex/agy/opencode node ever breaks a rule that only Claude auto memory or `CLAUDE.md` held (范蠡's trigger, §7 Q11), then for Claude-only work the pointer plus delivery was already enough, and the denial half was the only part worth keeping.
