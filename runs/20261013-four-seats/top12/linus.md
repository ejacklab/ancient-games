I'll read that brief first.
# Linus Torvalds — top 12, reviewed

## Review of the top 10

1. **Keep**, and it is correctly first — the "name of the game is to avoid having to make a decision" sentence is the doc's headline and the strongest evidence for it. But note it is one half of a single mechanism whose other half is #2; they only separate because one answers *who decides* and the other *what commitment is allowed*.
2. **Keep**, ranked 2 — reversibility is the test that #1 uses, and the paragraph makes that explicit ("the key difference between a big decision and a small one is whether you can fix your decision afterwards"). The "can't we just do both?" fallback is a *tactic*, not the rule; it is quoted twice in the item and reads as a second thing.
3. **Change → widen into a mindset** — as written it is only a manager tactic. The sentences around it in §1 and §3 ("admitting up-front that you don't have a friggin' clue", "we're not the sharpest knife around") make it a standing attitude. Widening matters because the top 10 contains **no mindset at all** — all ten are triggered rules.
4. **Change → add the size cap** — "If you cannot condense your patch set into a smaller set of patches, then only post say 15 or so at a time and wait for review and integration" is missing, and it is the only quantitative rule in the three documents: it is what makes the loop bounded. As an algorithm the item should read split → order → build at every point → cap the batch.
5. **Keep** — solid, well quoted, correctly ranked among the acceptance rules. Its first quote (resubmission hygiene) is the weaker half; the weight is in "quantify" plus "describe the expected downsides".
6. **Drop** — its strong form is contradicted two sections later in the same file: checkpatch "should be viewed as a guide, not as a replacement for human judgment" and "You should be able to justify all violations that remain in your patch". Its second quote is about his own inbox rather than about work, and the MIME/shabby-formatting material is 2003-era etiquette with little transfer value. Salvage: fold the mechanical test into item 12, and note the one real exception it contains (a move-only patch must not be edited in the same patch).
7. **Keep** — quote is verbatim (including the `-avoid-`). It is really two rules (route to the owner; keep the arbiter's queue small) but they belong together. Ranked 8 only because it is about kernel structure rather than judgement — though it is the most directly transferable dispatch rule he has.
8. **Keep, strengthened** — "burn the GNU standards" is the famous line and the weakest evidence of the rule. §9 carries the real principle: the emacs defaults "are worse than random typing", "an infinite number of monkeys typing into GNU emacs would never make a good program", and "remember: `indent` is not a fix for bad programming".
9. **Change → merge into item 12** — it is three rules with three triggers (naming, comments, function size) and fails one-thing. The transferable half — "do just one thing", "a human brain can generally easily keep track of about 7 different things", "maybe you'd like to understand what you did 2 weeks from now" — survives inside item 12; naming and comments are enforced by the same single filter.
10. **Change → split into two** (items 5 and 6) — "be blunt" and "take the blame for someone else" are different acts with different triggers: one is how you deliver a no, the other whose name carries the cost. Merged, a reader cannot tell which applies when a rejection is correct *and* unpopular. Also fix the quote: the file says "**There's** one thing people hate…", not "There is one thing" (the quote check caught this).

## What the top 10 missed

- **A standing attitude at all.** The top 10 has none. The docs are saturated with one: everyone is fallible and you are no exception, so uncertainty is announced in advance rather than concealed.
- **How he finds the decision-maker, not just how he refuses to be one.** §3 "People II — the Good Kind" is a whole method the list skips: find whoever is better than you at this thing, coast, say "Sounds like a good idea - go wild", and — the part that is easy to miss — *expertise is local, so prod lightly and do not push hard*.
- **The artifact that survives.** The top 10 talks about patch justification but not the commit log, which is the thing that has to stand alone for a reader with no memory of the discussion.
- **The one big decision he does take.** `management-style.rst` says avoid big decisions; the documented release process says he personally opens a ~2-week merge window per cycle, merges at scale, and then only fixes until release. Read alone, the top 10 implies he never decides anything. He decides once per cycle, on a schedule, with a named owner — which is the most transferable rule on this list.
- **The thing he got backwards in the top 10:** the style gate is a guide, not an oracle; a violation you can justify may stay, and moving code is never combined with editing it.

## Top 12

1. **Never make the technical decision yourself — hand it to whoever wrote the code.**
   - **Kind:** decision rule
   - **In plain English:** when a maintainer brings you a choice between two designs, refuse the binary and push it back down to the person who knows the details; your own judgement is not the input that matters.
   - **Their words:** "The name of the game is to **avoid** having to make a decision. In particular, if somebody tells you 'choose (a) or (b), we really need you to decide on this', you're in trouble as a manager. The people you manage had better know the details better than you, so if they come to you for a technical decision, you're screwed."
     → English original; operative sense: being asked to choose proves you are the wrong person to choose.
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions" — https://docs.kernel.org/process/management-style.html
   - **Label:** `quoted`
   - **From:** top-10 #1 (kept)

2. **Only take decisions you can undo; make every big decision into two small ones.**
   - **Kind:** decision rule
   - **In plain English:** the test for a decision is not its size but whether you can back it out; if you can always undo it, then being wrong is cheap and the decision was never big. Never commit to something you cannot walk back.
   - **Their words:** "It helps to realize that the key difference between a big decision and a small one is whether you can fix your decision afterwards. Any decision can be made small by just always making sure that if you were wrong (and you **will** be wrong), you can always undo the damage later by backtracking. Suddenly, you get to be doubly managerial for making **two** inconsequential decisions - the wrong one **and** the right one." … "Thus the key to avoiding big decisions becomes to just avoiding to do things that can't be undone. Don't get ushered into a corner from which you cannot escape."
     → English original; operative sense: reversibility is the whole criterion, and admitting you will be wrong is assumed, not exceptional.
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions"
   - **Label:** `quoted`
   - **From:** top-10 #2 (kept)

3. **Nobody is above suspicion and you are not above it either: say "I don't know" before you act, and sell doubt rather than confidence.**
   - **Kind:** mindset
   - **In plain English:** a standing attitude applied to yourself first — announce in advance that a decision is preliminary and may be wrong, reserve the right to change your mind visibly, and prefer leaving people thinking twice over giving them your assurance.
   - **Their words:** "Happily, both of these reasons can be mitigated effectively by just admitting up-front that you don't have a friggin' clue, and telling people ahead of the fact that your decision is purely preliminary, and might be the wrong thing. You should always reserve the right to change your mind, and make people very **aware** of that." … "The best thing you can do as a manager is not to instill confidence, but rather a healthy dose of critical thinking on what they do. […] Make them at least think twice before they embark on a big endeavor." … "we should also admit that we're not the sharpest knife around, and that there will be other people that are less of an idiot than you are."
     → English original; operative sense: uncertainty is cheap to state and expensive to hide; your job is to make people doubt, not believe you.
   - **Source:** `Documentation/process/management-style.rst` §1, §3 "People II - the Good Kind"
   - **Label:** `quoted`
   - **From:** top-10 #3 (changed)

4. **Actively recruit the people who are better than you at the thing, then coast; expertise is local, so prod lightly.**
   - **Kind:** decision rule
   - **In plain English:** find whoever understands the area better than you do, make them the decision-maker, and do the job of saying "sounds like a good idea — go wild" or "that sounds good, but what about X?"; never push hard in a direction, because being sharp in one area does not transfer to another.
   - **Their words:** "Some people react badly to smart people. Others take advantage of them. Make sure that you, as a kernel maintainer, are in the second group. Suck up to them, because they are the people who will make your job easier. In particular, they'll be able to make your decisions for you, which is what the game is all about." … "So when you find somebody smarter than you are, just coast along. Your management responsibilities largely become ones of saying 'Sounds like a good idea - go wild', or 'That sounds good, but what about xxx?'." … "One thing to look out for is to realize that greatness in one area does not necessarily translate to other areas. […] just don't push too hard."
     → English original; operative sense: the top 10 had only the refusal; this is the positive move that replaces the refusal, plus its limit.
   - **Source:** `Documentation/process/management-style.rst` §3 "People II - the Good Kind"
   - **Label:** `quoted`
   - **From:** new

5. **Take the blame yourself, in public; deliver the correction in private.**
   - **Kind:** decision rule
   - **In plain English:** when something breaks, take the fall openly — it buys you the authority to manage — then tell the person who actually caused it privately, because that is also how you learn who can fix it next time.
   - **Their words:** "Which brings us to the best way of taking the blame: do it for someone else. You'll feel good for taking the fall, they'll feel good about not getting blamed, and the person who lost their whole 36GB porn-collection because of your incompetence will grudgingly admit that you at least didn't try to weasel out of it." … "Then make the developer who really screwed up (if you can find them) know **in private** that they screwed up. Not just so they can avoid it in the future, but so that they know they owe you one. And, perhaps even more importantly, they're also likely the person who can fix it."
     → English original; operative sense: public blame is the price of the role and should be paid first, in cash, without excuse.
   - **Source:** `Documentation/process/management-style.rst` §4 "Placing blame"
   - **Label:** `quoted`
   - **From:** top-10 #10 (changed — split, this half)

6. **Be blunt, never sanctimonious: no politeness that hides the problem, no public name-calling, and apologise when you slipped.**
   - **Kind:** decision rule
   - **In plain English:** deliver a rejection directly and without softening — politeness ends up hiding the problem and "nobody can hear you being subtle" — but the insult must not be sanctimonious and never public; the two rules that matter are "don't call people d*ckheads" and "learn how to apologize", because alienating someone is irreversible and the rejection is not.
   - **Their words:** "There's just a few simple rules here: (1) don't call people d*ckheads (at least not in public) (2) learn how to apologize when you forgot rule (1)." … "There's one thing people hate even more than being called 'd*ckhead', and that is being called a 'd*ckhead' in a sanctimonious voice." … "Similarly, don't be too polite or subtle about things. Politeness easily ends up going overboard and hiding the problem, and as they say, 'On the internet, nobody can hear you being subtle'. Use a big blunt object to hammer the point in, because you can't really depend on people getting your point otherwise." … "It turns out that alienating people is fairly easy, and un-alienating them is hard. Thus 'alienating' immediately falls under the heading of 'not reversible'."
     → English original; operative sense: bluntness is required, sanctimony is fatal, and the relationship is the irreversible part.
   - **Source:** `Documentation/process/management-style.rst` §2 "People", §5 "Things to avoid"
   - **Label:** `quoted`
   - **From:** top-10 #10 (changed — split, this half; quote corrected)

7. **Take the one big irreversible decision, once per cycle, at a scheduled moment — then take only fixes until it ships.**
   - **Kind:** algorithm
   - **In plain English:** steps: collect and stage changes before the cycle → open a roughly two-week merge window and merge everything that is ready at scale → close the window and cut -rc1 → accept only bug fixes for the next six to ten weeks, releasing -rc kernels weekly → release final. A feature that missed the window waits for the next cycle.
   - **Their words:** "The merge window lasts for approximately two weeks. At the end of this time, Linus Torvalds will declare that the window is closed and release the first of the 'rc' kernels." … "The -rc1 release is the signal that the time to merge new features has passed, and that the time to stabilize the next kernel has begun." … "Over the next six to ten weeks, only patches which fix problems should be submitted to the mainline." … "As a general rule, if you miss the merge window for a given feature, the best thing to do is to wait for the next development cycle."
     → English original, but **not his words** — the kernel's own documentation describing his practice in the third person.
   - **Source:** `Documentation/process/2.Process.rst` §"The Merge Window" (and `howto.rst` for the cycle) — https://docs.kernel.org/process/2.Process.html
   - **Label:** `attributed` (the project's description of his practice; no first-person source found)
   - **From:** new

8. **Route work to the owner of the code and keep the top arbiter's queue small.**
   - **Kind:** decision rule
   - **In plain English:** a patch belongs to the subsystem maintainer named in MAINTAINERS; the final arbiter's address is listed so people can *avoid* it, because very few patches go through him directly. He stays the exception path, not the default path.
   - **Their words:** "Linus Torvalds is the final arbiter of all changes accepted into the Linux kernel. His e-mail address is <torvalds@linux-foundation.org>. He gets a lot of e-mail, and, at this point, very few patches go through Linus directly, so typically you should do your best to -avoid- sending him e-mail."
     → English original; operative sense: the escalation address is published precisely to be avoided.
   - **Source:** `Documentation/process/submitting-patches.rst` §"Select the recipients for your patch" — https://docs.kernel.org/process/submitting-patches.html
   - **Label:** `quoted`
   - **From:** top-10 #7 (kept)

9. **The commit message is permanent documentation, written for a competent stranger who has forgotten the discussion.**
   - **Kind:** algorithm
   - **In plain English:** steps: one-line summary of at most ~70–75 characters naming what changes *and* why it may be necessary, in imperative mood; body wrapped at 75 columns explaining the problem, the user-visible impact and the reasoning; tags below; anything version-specific goes *after* the `---` marker so the permanent record stays clean. The test is the reader months or years later, searching the log.
   - **Their words:** "the ``summary`` must be no more than 70-75 characters, and it must describe both what the patch changes, as well as why the patch might be necessary." … "The explanation body will be committed to the permanent source changelog, so should make sense to a competent reader who has long since forgotten the immediate details of the discussion that might have led to this patch." … "The text should be written in such detail so that when read weeks, months or even years later, it can give the reader the needed details to grasp the reasoning for **why** the patch was created." … "The body of the explanation, line wrapped at 75 columns, which will be copied to the permanent changelog to describe this patch."
     → English original; operative sense: the log is the only thing that survives the people who wrote it, so it is written for a stranger.
   - **Source:** `Documentation/process/submitting-patches.rst` §"The canonical patch format" → "Subject Line", "Explanation Body", "Commentary"
   - **Label:** `quoted`
   - **From:** new

10. **One logical change per patch; the tree must build and run after every patch in the series; never post more than about fifteen without review.**
    - **Kind:** algorithm
    - **In plain English:** steps: split a mixed change into one logical change per patch (bug fix apart from performance work, API change apart from the driver that uses it); keep a single change across many files in one patch; order the series so the kernel builds and runs at every point, because `git bisect` will cut anywhere; note any dependency; if the series cannot be condensed, send ~15 patches and wait.
    - **Their words:** "Solve only one problem per patch. If your description starts to get long, that's a sign that you probably need to split up your patch." … "take special care to ensure that the kernel builds and runs properly after each patch in the series. Developers using git bisect to track down a problem can end up splitting your patch series at any point; they will not thank you if you introduce bugs in the middle." … "If you cannot condense your patch set into a smaller set of patches, then only post say 15 or so at a time and wait for review and integration."
      → English original; operative sense: every intermediate state must be valid, and the batch size is capped on purpose.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Describe your changes" and §"Separate your changes"
    - **Label:** `quoted`
    - **From:** top-10 #4 (changed — added the batch cap and the bisect reason)

11. **The justification must stand alone: quantify the claimed win and state your own costs.**
    - **Kind:** decision rule
    - **In plain English:** a patch that only makes sense to people already in the thread is not acceptable — resend the full description, not "this is v2"; if you claim a performance or size improvement, give numbers; and name the downsides you expect, so the reviewer can weigh cost against benefit.
    - **Their words:** "When you submit or resubmit a patch or patch series, include the complete patch description and justification for it. Don't just say that this is version N of the patch (series). […] the patch (series) and its description should be self-contained." … "Quantify optimizations and trade-offs. If you claim improvements in performance, memory consumption, stack footprint, or binary size, include numbers that back them up. But also describe non-obvious costs. […] Describe the expected downsides of your optimization so that the reviewer can weigh costs against benefits."
      → English original; operative sense: the claim must survive without the thread, and it must come with its own downside attached.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Describe your changes"
    - **Label:** `quoted`
    - **From:** top-10 #5 (kept)

12. **One filter for all code: can the people who must maintain it still read and grep it in two weeks? No external standard has authority, and no formatter is a fix.**
    - **Kind:** decision rule
    - **In plain English:** the only test is maintainability by whoever has to keep it, so conventions are his own rather than GNU's or a tool's; the mechanical consequences are descriptive names, comments that say what and not how, and functions that do one thing and stay small. Where the checker and his judgement disagree, his judgement wins — but he must be able to justify every violation left standing.
    - **Their words:** "Coding style is very personal, and I won't **force** my views on anybody, but this is what goes for anything that I have to be able to maintain, and I'd prefer it for most other things too. Please at least consider the points made here." … "First off, I'd suggest printing out a copy of the GNU coding standards, and NOT read it. Burn them, it's a great symbolic gesture." … "the defaults it uses are less than desirable (in fact, they are worse than random typing - an infinite number of monkeys typing into GNU emacs would never make a good program)" … "remember: `indent` is not a fix for bad programming." … "Functions should be short and sweet, and do just one thing. […] A human brain can generally easily keep track of about 7 different things, anything more and it gets confused. You know you're brilliant, but maybe you'd like to understand what you did 2 weeks from now." … "NEVER try to explain HOW your code works in a comment: […] Generally, you want your comments to tell WHAT your code does, not HOW."
      → English original; operative sense: one filter (maintainability), expressed as conventions he owns, with tools subordinate to it.
    - **Source:** `Documentation/process/coding-style.rst` opening, §4 "Naming", §6 "Functions", §8 "Commenting", §9 "You've made a mess of it" — plus `submitting-patches.rst` §"Style-check your changes" for the checker-is-a-guide exception: "the style checker should be viewed as a guide, not as a replacement for human judgment" / "You should be able to justify all violations that remain in your patch" — https://docs.kernel.org/process/coding-style.html
    - **Label:** `quoted`
    - **From:** top-10 #8 and #9 (changed — merged into one filter; the checker's subordination is now stated)

## Gaps

- **Nothing here is sourced from outside the kernel's own documentation, and that is a hard limit in this environment, not a choice.** `lore.kernel.org` returns 403 (Anubis proof-of-work); `groups.google.com` returns 429; the Wayback Machine has **no** snapshot of the 1991 `comp.os.minix` announcement; no general web search is reachable. So there is **no** item from the NFS "I'M A COMPLETE IDIOT" mail, the `[GIT PULL]` rants, the 2.6.12/3.0 release announcements, the 2007 Git talk's "10 rules", the 2018 Code-of-Conduct apology, or the "just a hobby" announcement. The research's largest gap is real and I could not close it. Anyone wanting his actual decision-making *in the act*, the mails are the corpus and this list is not.
- **My list leans harder on the least verifiable source than the research's did.** Six of twelve items come from `management-style.rst`, whose authorship is still asserted rather than proven by commit — the same caveat the research recorded, and it now matters more, not less. Treat those six as his words on the strength of attribution only.
- **Item 7 is not in his words.** It is the kernel's documentation (`2.Process.rst`, third person, other authors) describing his release practice. Labelled `attributed`; no first-person source was found. Without item 7, items 1–2 over-read as "he never decides anything", which is false.
- **`stable-api-nonsense.rst` is Greg Kroah-Hartman's, not Torvalds's.** It must not be used as evidence for the famous "the kernel has no stable in-kernel API" position; that rule is widely attributed to him and I could not source it in his own words.
- **The canonical patch format's original statement is unverified.** `submitting-patches.rst` cites Linus's 2005 mail (`Pine.LNX.4.58.0504071023190.28951@ppc970.osdl.org`) as the source of §"The canonical patch format"; I could not open it (lore blocked). Item 9's rules therefore carry the same later-editor risk the research flagged for `coding-style.rst` §10+.
- **Provenance discipline inherited unchanged:** only `coding-style.rst` §1–§9 and the opening are used (§22 and later chapters excluded, per the research's own authorship finding); the CoC file in the tree is Contributor Covenant text, not his, so nothing from it is used.
- **Quote verification:** I re-checked every quote I reuse against the files I fetched, and the only defect found is the one the quote check already flagged — "There is one thing" should be "There's one thing". No other rewording found in the reused material.
