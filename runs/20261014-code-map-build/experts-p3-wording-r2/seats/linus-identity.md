I'll read the brief first.
# Linus Torvalds — who they are and how they decided

## Who they are

Linus Benedict Torvalds (born 28 December 1969 in Helsinki, Finland; Swedish-speaking Finn, naturalised US citizen 2010) has been the creator and lead developer of the Linux kernel since 1991. He announced his "free operating system … just a hobby" for 386/486 AT clones on comp.os.minix on 25 August 1991 (Message-ID `1991Aug25.205708.9541@klaava.Helsinki.FI`), released 1.0 on 14 March 1994, and relicensed the kernel under the GPLv2 after hearing Richard Stallman speak in the autumn of 1991 (Wikipedia, *Linus Torvalds*, citing *Torvalds & Diamond, Just for Fun*, and comp.os.minix; *The early days of Linux*, Lars Wirzenius, LWN). He worked at Transmeta from February 1997 to June 2003, then at OSDL and the Linux Foundation, and moved to Oregon in 2004. In 2005, after the BitKeeper dispute, he wrote Git starting 3 April 2005 and handed it to Junio Hamano by mid-2005; Git exists because "the Linux kernel developers needed a tool they could use to version the kernel". He wrote very little of the kernel himself — about 2% as of 2006 — and said in 2012 that his own contribution is now "mostly merging code written by others". What he kept was the last word: `Documentation/process/submitting-patches.rst` states, in the present tense, "Linus Torvalds is the final arbiter of all changes accepted into the Linux kernel", while noting that "very few patches go through Linus directly". He codified how he would exercise that power in prose rather than edicts — `Documentation/process/management-style.rst` ("This is a short document describing the preferred (or made up, depending on who you ask) management style for the linux kernel") and the much older `coding-style.rst` ("this is what goes for anything that I have to be able to maintain"). In September 2018, after The New Yorker reported on his years of abusive mailing-list mail, he replaced the kernel's Code of Conflict with a Code of Conduct, called his past attacks "unprofessional and uncalled for", took time off to work on how he responds to people, and returned to maintaining 4.19 in October 2018. Awards: 2012 Millennium Technology Prize, 2014 IEEE Computer Pioneer Award, 2018 IEEE Masaru Ibuka Consumer Electronics Award.

## Top 10 decision rules

1. **Never make the big technical decision yourself — hand it to whoever actually knows the details.**
   - **Their words:** "The name of the game is to avoid having to make a decision. In particular, if somebody tells you 'choose (a) or (b), we really need you to decide on this', you're in trouble as a manager. The people you manage had better know the details better than you, so if they come to you for a technical decision, you're screwed."
   - **Source:** `Documentation/process/management-style.rst`, §1 "Decisions" — https://docs.kernel.org/process/management-style.html
   - **How it decides:** Situation: a maintainer asks him to pick between two technical designs. Output: he refuses the binary, and pushes the choice down to the subsystem maintainer who wrote the code. This is the single mechanism behind his famously small personal patch queue.
   - **Label:** `quoted`

2. **Only take decisions you can undo; refuse anything irreversible.**
   - **Their words:** "It helps to realize that the key difference between a big decision and a small one is whether you can fix your decision afterwards. […] Thus the key to avoiding big decisions becomes to just avoiding to do things that can't be undone. Don't get ushered into a corner from which you cannot escape. A cornered rat may be dangerous - a cornered manager is just pitiful." And, as a fallback when stuck: "another way to avoid a decision is to plaintively just whine 'can't we just do both?' and look pitiful. Trust me, it works. […] they will eventually figure it out. The answer may end up being that both teams get so frustrated by the situation that they just give up."
   - **Source:** `Documentation/process/management-style.rst`, §1 "Decisions"
   - **How it decides:** Situation: he is being pushed toward an architecture or API commitment (e.g. a long-term stable ABI, a subsystem-wide rewrite). Output: he declines to commit, or lets both approaches proceed until one dies on its own merits.
   - **Label:** `quoted`

3. **Instil critical thinking in people, not confidence in your own decision.**
   - **Their words:** "The best thing you can do as a manager is not to instill confidence, but rather a healthy dose of critical thinking on what they do. […] Make them at least think twice before they embark on a big endeavor."
   - **Source:** `Documentation/process/management-style.rst`, §1
   - **How it decides:** Situation: a large, expensive subsystem proposal arrives with visible senior backing. Output: he signals doubt rather than endorsement, so the proposal is argued for before anyone burns a year on it.
   - **Label:** `quoted`

4. **One problem per patch; every patch must stand on its own and must not break the tree mid-series.**
   - **Their words:** "Solve only one problem per patch. If your description starts to get long, that's a sign that you probably need to split up your patch." / "The point to remember is that each patch should make an easily understood change that can be verified by reviewers. Each patch should be justifiable on its own merits." / "When dividing your change into a series of patches, take special care to ensure that the kernel builds and runs properly after each patch in the series. Developers using git bisect to track down a problem can end up splitting your patch series at any point; they will not thank you if you introduce bugs in the middle."
   - **Source:** `Documentation/process/submitting-patches.rst`, sections "Describe your changes" and "Separate your changes" — https://docs.kernel.org/process/submitting-patches.html
   - **How it decides:** Situation: a mixed 40-patch series containing a bug fix, an API change and a new driver. Output: reject-and-resubmit as separate series; anything that cannot be reviewed or bisected on its own does not get accepted in that form.
   - **Label:** `quoted`

5. **Require the justification to be self-contained, quantified, and to state its own costs.**
   - **Their words:** "When you submit or resubmit a patch or patch series, include the complete patch description and justification for it. Don't just say that it's version N of the patch (series)." / "Quantify optimizations and trade-offs. If you claim improvements in performance, memory consumption, stack footprint, or binary size, include numbers that back them up. But also describe non-obvious costs. […] Describe the expected downsides of your optimization so that the reviewer can weigh costs against benefits."
   - **Source:** `Documentation/process/submitting-patches.rst`, "Describe your changes"
   - **How it decides:** Situation: a patch claiming a performance win, or a v2 whose rationale lives only in the v1 thread. Output: send it back — a patch that only makes sense to the people already in the thread is not acceptable.
   - **Label:** `quoted`

6. **Reject on process before content: bad style or an unreadable format kills a patch unread.**
   - **Their words:** "Failure to do so simply wastes the reviewers time and will get your patch rejected, probably without even being read." (on style violations) / "A MIME attachment also takes Linus a bit more time to process, decreasing the likelihood of your MIME-attached change being accepted."
   - **Source:** `Documentation/process/submitting-patches.rst`, sections "Style-check your changes" and "No MIME, no links, no compression, no attachments. Just plain text"
   - **How it decides:** Situation: a technically excellent patch with trailing whitespace, or sent as a compressed attachment. Output: rejected at the gate, with no technical review performed at all.
   - **Label:** `quoted`

7. **Route work through the maintainer hierarchy, and keep the last-arbiter role as small as possible.**
   - **Their words:** "Linus Torvalds is the final arbiter of all changes accepted into the Linux kernel. […] He gets a lot of e-mail, and, at this point, very few patches go through Linus directly, so typically you should do your best to -avoid- sending him e-mail."
   - **Source:** `Documentation/process/submitting-patches.rst`, "Select the recipients for your patch"
   - **How it decides:** Situation: a patch touches a subsystem with a named maintainer in MAINTAINERS. Output: it goes to that maintainer and lands without him seeing it — he intervenes only when the hierarchy has stalled or gone wrong.
   - **Label:** `quoted`

8. **Enforce only what you must maintain; no outside authority, no dogma, burn the manuals.**
   - **Their words:** "Coding style is very personal, and I won't force my views on anybody, but this is what goes for anything that I have to be able to maintain, and I'd prefer it for most other things too." / "First off, I'd suggest printing out a copy of the GNU coding standards, and NOT read it. Burn them, it's a great symbolic gesture."
   - **Source:** `Documentation/process/coding-style.rst`, opening — https://docs.kernel.org/process/coding-style.html
   - **How it decides:** Situation: a contributor argues from an external style standard, a linter's defaults, or a popular tool's defaults. Output: the argument is rejected on the ground that the only test is whether the code is maintainable by him and the maintainers — external consensus carries no weight.
   - **Label:** `quoted`

9. **Make code mechanically readable: descriptive names, comments that say what not how, functions that do one thing.**
   - **Their words:** "C is a Spartan language, and your naming conventions should follow suit. […] To call a global function foo is a shooting offense." / "NEVER try to explain HOW your code works in a comment: it's much better to write the code so that the working is obvious, and it's a waste of time to explain badly written code. Generally, you want your comments to tell WHAT your code does, not HOW." / "Functions should be short and sweet, and do just one thing. […] A human brain can generally easily keep track of about 7 different things, anything more and it gets confused."
   - **Source:** `Documentation/process/coding-style.rst`, §4 "Naming", §8 "Commenting", §6 "Functions"
   - **How it decides:** Situation: a patch adds `int do_it(void)`, a comment narrating each line, and a 300-line function. Output: "no" — not on correctness but because he must be able to read and grep it in five years, and because the rules are cheap to check.
   - **Label:** `quoted`

10. **When you must say no to a person, be blunt and take the blame yourself — but never publicly call them a d*ckhead, and apologise afterwards.**
    - **Their words:** "Use a big blunt object to hammer the point in, because you can't really depend on people getting your point otherwise." / "There is one thing people hate even more than being called a 'd*ckhead', and that is being called a 'd*ckhead' in a sanctimonious voice." / "It turns out that alienating people is fairly easy, and un-alienating them is hard. Thus 'alienating' immediately falls under the heading of 'not reversible' […] There's just a few simple rules here: don't call people d*ckheads (at least not in public); learn how to apologize when you forgot rule (1)." / "The best way of taking the blame: do it for someone else. You'll feel good for taking the fall, they'll feel good about not getting blamed."
    - **Source:** `Documentation/process/management-style.rst`, §2, §4 "Placing blame", §5 "Things to avoid"
    - **How it decides:** Situation: a patch or a maintainer has to be rejected, and the recipient is senior. Output: reject it directly and without hedging, absorb the public cost himself, and keep the relationship intact — because the rejection is not reversible if it destroys the person.
    - **Label:** `quoted`

## Sources used

Opened and read:
- https://docs.kernel.org/process/submitting-patches.html (version rendered: 7.3.0-rc7)
- https://docs.kernel.org/process/coding-style.html (7.3.0-rc7)
- https://docs.kernel.org/process/management-style.html (7.3.0-rc7)
- https://docs.kernel.org/process/changes.html — turned out to be "Minimal requirements to compile the Kernel"; not used- https://en.wikipedia.org/w/index.php?title=Linus_Torvalds&action=raw (biography + its citations, incl. the comp.os.minix 1991 message-id)
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/Documentation/process/coding-style.rst?qt=grep&q=crash — used to check provenance of coding-style §22
- https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/log/Documentation/process/{management-style,submitting-patches,coding-style}.rst — history check, inconclusive (see Gaps)
- https://api.github.com/repos/torvalds/linux/contents/Documentation/process — directory listing only

Attempted and unavailable:
- https://lore.kernel.org/lkml/…/raw — Anubis proof-of-work JS challenge; unreadable
- https://yhbt.net/lore/… — 502
- https://lkml.org/lkml/2007/8/6 — index reachable, message bodies not usable at this scale
- https://marc.info/?l=linux-kernel… — search reachable (bodies/authors), individual message bodies not retrievable
- https://git-scm.com/about/10-rules, https://git-scm.com/about, https://www.kernel.org/~linus/ — 404
- https://cdn.kernel.org/pub/linux/kernel/v2.6/announce/2.6.12 and archive.org availability API — not archived
- https://raw.githubusercontent.com/torvalds/linux/master/Documentation/process/development-model.rst — 404 (file no longer exists) / later requests HTTP 429

## Gaps

- **No rule is sourced from an LKML post or a talk.** `lore.kernel.org` is behind an Anubis JavaScript proof-of-work wall and the mirrors I could reach (yhbt.net 502, marc.info search-only, lkml.org) did not yield message bodies. That means the famous mails — the NFS "I'M A COMPLETE IDIOT" post (Aug 2007), the `[GIT PULL]` rants, the 2.6.12 and 3.0 release announcements — are **not** used here, and my knowledge of their wording was deliberately not paraphrased into quotes. This is the largest gap and it matters: his most quotable decision-making is in those mails, not in the docs.
- **Per-chapter authorship in `coding-style.rst` and `submitting-patches.rst` is not signed.** Both are Linus-authored documents that many others have since edited. I verified one case and it failed my own test: chapter 22 "Do not crash the kernel" was added by **David Hildenbrand** in commit `coding-style.rst: document BUG() and WARN() rules ("do not crash the kernel")`, 2022-09-29 — so I excluded it despite how "Linus-ish" it sounds. I kept only §1–§9 (naming, functions, comments, braces, indentation) and the opening, which are the original early-1990s text. A few quoted phrases could in principle have been reworded by later editors; I have not diffed them against the 1990s text.
- **`management-style.rst` authorship is asserted, not verified.** The kernel.org git mirror I could reach exposes only `master` (no tags, no rename history), so the file's original commit is unreachable and no commit in its history is by Torvalds. The document is universally attributed to him and is written in his first person as a kernel maintainer, but I could not produce a commit record. Treat every quote from it as his words on the strength of attribution, not of provenance.
- **I did not consult "Just for Fun"** — no accessible full text, so no quote from it, and nothing in rule set 1–10 depends on it. (Wikipedia's biography cites it, pp. 29, 38, 53, 60, 94 for the Finnish Navy, UNIX/MINIX, and the 80386 purchase.)
- **The famous 1991 "just a hobby, won't be big and professional like gnu" line is quoted via Wikipedia's citation**, not by me opening groups.google.com. I have therefore kept it out of the numbered rules and mentioned the post only by date and Message-ID.
- **Not verified:** the exact dates of the 2.6.12 (Dec 2003) and 3.0 (July 2011) release announcements, and the current percentage of kernel code authored by him (the ~2% figure is from 2006).
- **A likely candidate I rejected for lack of sourcing:** the git-side rules ("never break backwards compatibility", "every commit is a single logical change", "trust no data from outside your system"). Those are attributed to Linus's 2007 Google Tech Talk, but I could not reach the transcript — `git-scm.com/about/10-rules` is a 404 — so I did not include them.
