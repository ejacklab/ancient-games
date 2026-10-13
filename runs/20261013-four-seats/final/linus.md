# Linus Torvalds — final list

## Changes from the top 12
- Item 1: **corrected** — removed "Never", "whoever wrote the code", and "your own judgement is not the input that matters" (codex row 1); the source allows small decisions and frames the problem as avoiding big technical decisions where subordinates must know the details better.
- Item 2: **corrected** — removed "Only" and the interpretation that decisions must be split into two in advance (codex row 2); the text defines small decisions by reversibility via backtracking, where the two decisions are the wrong choice and its subsequent correction.
- Item 3: **corrected** — fixed the reversed quotation order identified by codex (lines 289 before lines 292–294) and removed the added slogan "Nobody is above suspicion" (codex row 3).
- Item 4: **corrected** — removed the added instruction to "actively recruit" (codex row 4); the text instructs taking advantage of smarter people when found, coasting, and prodding lightly without pushing too hard across domains.
- Item 5: **kept** — source supports taking public blame for others and notifying the developer in private, preserving "(if you can find them)" (codex row 5).
- Item 6: **corrected** — removed "without softening" because the source explicitly recommends using humor to pad bluntness and moralizing (codex row 6).
- Item 7: **corrected** — removed the unsupported framing of "one big irreversible decision" and absolute prohibition on post-window changes (codex row 7); relabeled as documented practice (`attributed`) describing the merge window, release candidates, and rare exceptions for late fixes and new drivers.
- Item 8: **corrected** — relabeled as documented practice (`attributed`) since the text describes Torvalds in the third person, and cited the maintainer-routing requirement alongside arbiter avoidance (codex row 8).
- Item 9: **corrected** — relabeled as documentation guidance (`attributed`) rather than direct speech (codex row 9), preserving the canonical formatting rules (summary under 70–75 characters in imperative mood, 75-column explanation body, and `---` separator).
- Item 10: **corrected** — removed the headline's absolute "never" and preserved the source's conditional, approximate batch limit of "say 15 or so at a time" if the patch set cannot be condensed (codex row 10); relabeled as `attributed`.
- Item 11: **corrected** — relabeled as documentation guidance (`attributed`) rather than direct speech (codex row 11); preserved the requirement to provide self-contained justifications with quantified metrics and expected downsides.
- Item 12: **corrected** — dismantled the artificial "one filter" umbrella and removed "no external standard has authority" (which conflicts with `coding-style.html:777` recognizing K&R) (codex row 12); unbundled into distinct, faithful rules for function scope, commenting, naming, code movement, and checker judgment.

## Final list

1. **Avoid big technical decisions where subordinates know the details better**
   - **Kind:** decision rule
   - **Rule:** A manager must avoid having to make big technical decisions between competing choices. If the people you manage come to you to make a technical decision, you are not competent to make it for them because they had better know the details better than you do.
   - **Their words:** "The name of the game is to **avoid** having to make a decision. In particular, if somebody tells you 'choose (a) or (b), we really need you to decide on this', you're in trouble as a manager. The people you manage had better know the details better than you, so if they come to you for a technical decision, you're screwed. You're clearly not competent to make that decision for them." — *Gloss:* If subordinates ask you to arbitrate technical alternatives, you are in the wrong position because they must possess the detailed domain knowledge required to decide.
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** top-12 #1

2. **Keep decisions small by ensuring they can be undone by backtracking**
   - **Kind:** decision rule
   - **Rule:** The key difference between a big decision and a small one is whether it can be fixed afterwards. Make decisions small by ensuring that if you were wrong, you can undo the damage later by backtracking, avoiding situations from which you cannot escape.
   - **Their words:** "It helps to realize that the key difference between a big decision and a small one is whether you can fix your decision afterwards. Any decision can be made small by just always making sure that if you were wrong (and you **will** be wrong), you can always undo the damage later by backtracking. Suddenly, you get to be doubly managerial for making **two** inconsequential decisions - the wrong one **and** the right one. ... Thus the key to avoiding big decisions becomes to just avoiding to do things that can't be undone. Don't get ushered into a corner from which you cannot escape." — *Gloss:* Consequential decisions are those that cannot be reversed; keeping actions backtrackable renders errors cheap and decisions inconsequential.
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** top-12 #2

3. **Allow competing approaches to proceed when superiority is unclear**
   - **Kind:** decision rule
   - **Rule:** When it is not clear which of two technical approaches is better, allow both to proceed. They will eventually figure it out, or both teams will become frustrated and give up, which usually indicates that both approaches were flawed.
   - **Their words:** "Btw, another way to avoid a decision is to plaintively just whine 'can't we just do both?' and look pitiful. Trust me, it works. If it's not clear which approach is better, they'll eventually figure it out. The answer may end up being that both teams get so frustrated by the situation that they just give up. That may sound like a failure, but it's usually a sign that there was something wrong with both projects, and the reason the people involved couldn't decide was that they were both wrong." — *Gloss:* When neither design shows clear dominance, let both advance in parallel until natural merit or mutual failure resolves the choice.
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** new (codex review "Missing")

4. **Preemptively admit fallibility and instill critical thinking rather than confidence**
   - **Kind:** mindset
   - **Rule:** Mitigate the cost of mistakes by admitting up-front that you do not have a clue, telling people decisions are preliminary, and reserving the right to change your mind. Rather than instilling confidence in subordinates, instill critical thinking to make them think twice before embarking on big endeavors.
   - **Their words:** "Happily, both of these reasons can be mitigated effectively by just admitting up-front that you don't have a friggin' clue, and telling people ahead of the fact that your decision is purely preliminary, and might be the wrong thing. You should always reserve the right to change your mind, and make people very **aware** of that." ... "Make them at least think twice before they embark on a big endeavor. Remember: they'd better know more about the details than you do, and they usually already think they have the answer to everything. The best thing you can do as a manager is not to instill confidence, but rather a healthy dose of critical thinking on what they do." ... "we should also admit that we're not the sharpest knife around, and that there will be other people that are less of an idiot than you are." — *Gloss:* Disclose uncertainty in advance, retain flexibility to reverse course openly, and puncture overconfidence so that developers critically evaluate their own plans.
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions" & §3 "People II - the Good Kind"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** top-12 #3

5. **Take advantage of smarter people and prod lightly within their local domain**
   - **Kind:** decision rule
   - **Rule:** When you find people smarter than you in an area, take advantage of them and let them make your decisions for you. Realize that greatness in one area does not translate to other areas, so do not push too hard when prodding them in new directions.
   - **Their words:** "Some people react badly to smart people. Others take advantage of them. Make sure that you, as a kernel maintainer, are in the second group. Suck up to them, because they are the people who will make your job easier. In particular, they'll be able to make your decisions for you, which is what the game is all about. So when you find somebody smarter than you are, just coast along. Your management responsibilities largely become ones of saying 'Sounds like a good idea - go wild', or 'That sounds good, but what about xxx?'." ... "One thing to look out for is to realize that greatness in one area does not necessarily translate to other areas. ... just don't push too hard." — *Gloss:* Delegate decision-making to domain experts, support their autonomy with light inquiry, and respect the boundaries of their specific competence.
   - **Source:** `Documentation/process/management-style.rst` §3 "People II - the Good Kind"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** top-12 #4

6. **Take blame publicly for others and inform the responsible developer in private**
   - **Kind:** decision rule
   - **Rule:** When things go wrong, accept the blame publicly on behalf of someone else. Then inform the developer who actually made the mistake in private (if you can find them), as they are the person who can fix it.
   - **Their words:** "Which brings us to the best way of taking the blame: do it for someone else. You'll feel good for taking the fall, they'll feel good about not getting blamed, and the person who lost their whole 36GB porn-collection because of your incompetence will grudgingly admit that you at least didn't try to weasel out of it. Then make the developer who really screwed up (if you can find them) know **in private** that they screwed up. Not just so they can avoid it in the future, but so that they know they owe you one. And, perhaps even more importantly, they're also likely the person who can fix it." — *Gloss:* Absorb public accountability to preserve community standing and shield contributors, while addressing the root cause directly and privately with the person capable of repairing it.
   - **Source:** `Documentation/process/management-style.rst` §4 "Placing blame"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** top-12 #5

7. **Deliver feedback bluntly without sanctimony, avoid public name-calling, and use humor to pad criticism**
   - **Kind:** decision rule
   - **Rule:** Do not be too polite or subtle about problems, but avoid public name-calling and never speak in a sanctimonious voice. Use humor to pad bluntness and moralizing so criticism does not alienate developers irreversibly, and apologize when you fail to follow restraint.
   - **Their words:** "There's just a few simple rules here: (1) don't call people d*ckheads (at least not in public) (2) learn how to apologize when you forgot rule (1)." ... "There's one thing people hate even more than being called 'd*ckhead', and that is being called a 'd*ckhead' in a sanctimonious voice." ... "Similarly, don't be too polite or subtle about things. Politeness easily ends up going overboard and hiding the problem, and as they say, 'On the internet, nobody can hear you being subtle'. Use a big blunt object to hammer the point in, because you can't really depend on people getting your point otherwise." ... "Some humor can help pad both the bluntness and the moralizing. Going overboard to the point of being ridiculous can drive a point home without making it painful to the recipient, who just thinks you're being silly." ... "alienating people is fairly easy, and un-alienating them is hard. Thus 'alienating' immediately falls under the heading of 'not reversible'". — *Gloss:* Be direct enough that technical critiques cannot be misunderstood, but avoid moral superiority or public abuse, softening the blow with humor to keep professional relationships intact.
   - **Source:** `Documentation/process/management-style.rst` §2 "People" & §5 "Things to avoid"
   - **Words are:** `quoted` (first-person text in kernel documentation traditionally attributed to Linus Torvalds)
   - **From:** top-12 #6

8. **Filter code through a lieutenant chain of trust while reserving selective scrutiny**
   - **Kind:** decision rule
   - **Rule:** Structure large-scale code integration around subsystem maintainers who act as gatekeepers in a chain of trust. Trust maintainers not to send bad patches upstream, while varying personal attention and looking closely at pull requests when warranted.
   - **Their words:** "The way the kernel developers have addressed this growth is through the use of a lieutenant system built around a chain of trust... Subsystem maintainers are the gatekeepers (in a loose way) for the portion of the kernel they manage; they are the ones who will (usually) accept a patch for inclusion into the mainline kernel... When the merge window opens, top-level maintainers will ask Linus to 'pull' the patches... The amount of attention that Linus pays to specific patches received in a pull operation varies. It is clear that, sometimes, he looks quite closely. But, as a general rule, Linus trusts the subsystem maintainers to not send bad patches upstream." — *Gloss:* Scale governance by delegating frontline review to trusted subsystem lieutenants, backing broad trust with occasional direct spot-checks.
   - **Source:** `Documentation/process/2.Process.rst` §2.3 "How patches get into the Kernel"
   - **Words are:** `attributed` (third-person kernel documentation describing Torvalds's development process)
   - **From:** new (codex review "Missing")

9. **Open a two-week merge window for major changes, followed by stabilization release candidates**
   - **Kind:** algorithm
   - **Rule:** Merge pre-staged new features during an approximate two-week merge window, declare the window closed with the -rc1 release, and restrict submissions over the next six to ten weeks to bug fixes (with rare exceptions for non-regressing new drivers), releasing -rc kernels weekly until stable.
   - **Their words:** "The merge window lasts for approximately two weeks. At the end of this time, Linus Torvalds will declare that the window is closed and release the first of the 'rc' kernels... The -rc1 release is the signal that the time to merge new features has passed, and that the time to stabilize the next kernel has begun. Over the next six to ten weeks, only patches which fix problems should be submitted to the mainline. On occasion a more significant change will be allowed, but such occasions are rare... (An occasional exception is made for drivers for previously-unsupported hardware; if they touch no in-tree code, they cannot cause regressions and should be safe to add at any time)... Linus releases new -rc kernels about once a week; a normal series will get up to somewhere between -rc6 and -rc9 before the kernel is considered to be sufficiently stable and the final release is made." — *Gloss:* Regulate cycle workflow in distinct phases: a brief front-loaded intake window for bulk changes, followed by a strict stabilization period dedicated to regression fixes.
   - **Source:** `Documentation/process/2.Process.rst` §2.1 "The development process"
   - **Words are:** `attributed` (third-person kernel documentation describing Torvalds's release management)
   - **From:** top-12 #7

10. **Route patches to subsystem maintainers and avoid sending mail to the top arbiter**
    - **Kind:** decision rule
    - **Rule:** Direct patches to the subsystem maintainers listed in MAINTAINERS rather than to Linus Torvalds. Although Torvalds is the final arbiter of all accepted changes, contributors should do their best to avoid emailing him directly because very few patches pass through him without subsystem routing.
    - **Their words:** "You should always copy the appropriate subsystem maintainer(s) and list(s) on any patch to code that they maintain; look through the MAINTAINERS file and the source code revision history to see who those maintainers are... Linus Torvalds is the final arbiter of all changes accepted into the Linux kernel... He gets a lot of e-mail, and, at this point, very few patches go through Linus directly, so typically you should do your best to -avoid- sending him e-mail." — *Gloss:* Route patches through designated subsystem maintainers; keep the root arbiter's personal queue unencumbered by treating direct submission as an exception.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Select the recipients for your patch"
    - **Words are:** `attributed` (kernel submission documentation describing Torvalds's role)
    - **From:** top-12 #8

11. **Enforce one logical change per patch, guarantee bisectability across series, and throttle large sets**
    - **Kind:** algorithm
    - **Rule:** Separate each logical change into its own patch so that every change can be verified and justified independently. Ensure the kernel builds and runs properly after each patch in the series so that `git bisect` is never broken; if the series cannot be condensed into a smaller set, post say 15 or so at a time and wait for review.
    - **Their words:** "Separate each **logical change** into a separate patch... The point to remember is that each patch should make an easily understood change that can be verified by reviewers. Each patch should be justifiable on its own merits... When dividing your change into a series of patches, take special care to ensure that the kernel builds and runs properly after each patch in the series. Developers using `git bisect` to track down a problem can end up splitting your patch series at any point; they will not thank you if you introduce bugs in the middle. If you cannot condense your patch set into a smaller set of patches, then only post say 15 or so at a time and wait for review and integration." — *Gloss:* Decompose work into self-contained logical units, preserve functional compilation at every intermediate commit to protect bisection, and pace large submissions in batches of roughly 15.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Separate your changes"
    - **Words are:** `attributed` (kernel submission documentation)
    - **From:** top-12 #10

12. **Format commit messages for permanent changelogs and separate transient comments**
    - **Kind:** algorithm
    - **Rule:** Format patch summaries to be no more than 70–75 characters in the imperative mood, describing both the change and why it is necessary. Write the explanation body wrapped at 75 columns with sufficient detail for a competent stranger to understand years later, and place non-permanent commentary (such as version changelogs and diffstats) below a `---` marker so it is stripped before committing.
    - **Their words:** "Describe your changes in imperative mood, e.g. 'make xyzzy do frotz' instead of '[This patch] makes xyzzy do frotz' or '[I] changed xyzzy to do frotz'..." ... "the ``summary`` must be no more than 70-75 characters, and it must describe both what the patch changes, as well as why the patch might be necessary." ... "The explanation body will be committed to the permanent source changelog, so should make sense to a competent reader who has long since forgotten the immediate details of the discussion that might have led to this patch... The text should be written in such detail so that when read weeks, months or even years later, it can give the reader the needed details to grasp the reasoning for **why** the patch was created." ... "A marker line containing simply ``---``. Any additional comments not suitable for the changelog... Please put this information **after** the ``---`` line which separates the changelog from the rest of the patch." — *Gloss:* Structure patch descriptions as enduring historical documentation for future maintainers, isolating ephemeral review notes behind the commit separator.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Describe your changes" & §"The canonical patch format"
    - **Words are:** `attributed` (kernel submission documentation)
    - **From:** top-12 #9

13. **Provide self-contained patch justifications with quantified data and explicit downsides**
    - **Kind:** decision rule
    - **Rule:** Make patch descriptions fully self-contained rather than referencing prior versions or external discussions. Quantify claimed optimizations with numbers and describe non-obvious costs and expected downsides so reviewers can weigh trade-offs.
    - **Their words:** "When you submit or resubmit a patch or patch series, include the complete patch description and justification for it. Don't just say that this is version N of the patch (series)... I.e., the patch (series) and its description should be self-contained." ... "Quantify optimizations and trade-offs. If you claim improvements in performance, memory consumption, stack footprint, or binary size, include numbers that back them up. But also describe non-obvious costs... Describe the expected downsides of your optimization so that the reviewer can weigh costs against benefits." — *Gloss:* Require every patch submission to justify itself independently with concrete metrics and frank acknowledgment of associated costs.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Describe your changes"
    - **Words are:** `attributed` (kernel submission documentation)
    - **From:** top-12 #11

14. **Do not modify moved code in the patch that moves it**
    - **Kind:** decision rule
    - **Rule:** When moving code from one file to another, do not modify the moved code in the same patch that moves it. Delineate the move from functional modifications to assist human review and history tracking tools.
    - **Their words:** "One significant exception is when moving code from one file to another -- in this case you should not modify the moved code at all in the same patch which moves it. This clearly delineates the act of moving the code and your changes. This greatly aids review of the actual differences and allows tools to better track the history of the code itself." — *Gloss:* Isolate structural relocation of code from substantive modifications across distinct patches to keep diffs reviewable and preserve tracking.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Style-check your changes"
    - **Words are:** `attributed` (kernel submission documentation)
    - **From:** new (noted in top-12 review #6 as an explicit exception)

15. **Treat automated style checkers as guides subordinate to human judgment**
    - **Kind:** decision rule
    - **Rule:** View patch style checkers as guides rather than replacements for human judgment. If code looks better with a style violation, leave it alone, but remain prepared to justify any violation left in the patch.
    - **Their words:** "Check your patches with the patch style checker prior to submission (scripts/checkpatch.pl). Note, though, that the style checker should be viewed as a guide, not as a replacement for human judgment. If your code looks better with a violation then its probably best left alone... You should be able to justify all violations that remain in your patch." — *Gloss:* Automated linter output is advisory; human readability governs, provided deviations can be defended.
    - **Source:** `Documentation/process/submitting-patches.rst` §"Style-check your changes"
    - **Words are:** `attributed` (kernel submission documentation)
    - **From:** top-12 #12

16. **Keep functions short and single-purpose, with limited local variables**
    - **Kind:** decision rule
    - **Rule:** Functions should be short, do just one thing well, and fit on one or two screenfuls of text. Limit local variables to 5–10; exceeding this indicates the function should be rethought and split into smaller helper pieces because the human brain struggles to track more than about seven things.
    - **Their words:** "Functions should be short and sweet, and do just one thing. They should fit on one or two screenfuls of text (the ISO/ANSI screen size is 80x24, as we all know), and do one thing and do that well." ... "Another measure of the function is the number of local variables. They shouldn't exceed 5-10, or you're doing something wrong. Re-think the function, and split it into smaller pieces. A human brain can generally easily keep track of about 7 different things, anything more and it gets confused. You know you're brilliant, but maybe you'd like to understand what you did 2 weeks from now." — *Gloss:* Restrict function scope to a single task fitting standard terminal screens, capping local state to respect human cognitive working memory.
    - **Source:** `Documentation/process/coding-style.rst` §6 "Functions"
    - **Words are:** `quoted` (Linus Torvalds's first-person text in `coding-style.rst`)
    - **From:** top-12 #12

17. **Write comments to explain what and why code works, never how**
    - **Kind:** decision rule
    - **Rule:** Never attempt to explain how code works in a comment; write the code so that its operation is obvious. Use comments at the head of a function to tell what the code does and why it was written, avoiding redundant comments inside function bodies.
    - **Their words:** "Comments are good, but there is also a danger of over-commenting. NEVER try to explain HOW your code works in a comment: it's much better to write the code so that the <strong>working</strong> is obvious, and it's a waste of time to explain badly written code. Generally, you want your comments to tell WHAT your code does, not HOW. Also, try to avoid putting comments inside a function body... Instead, put the comments at the head of the function, telling people what it does, and possibly WHY it does it." — *Gloss:* Make implementation logic self-evident in the code itself; reserve comments for intent, rationale, and behavioral purpose.
    - **Source:** `Documentation/process/coding-style.rst` §8 "Commenting"
    - **Words are:** `quoted` (Linus Torvalds's first-person text in `coding-style.rst`)
    - **From:** top-12 #12

18. **Scale variable naming descriptiveness to scope: Spartan locals, descriptive globals**
    - **Kind:** decision rule
    - **Rule:** Keep local variable names short and to the point (such as `i` or `tmp`), but mandate descriptive names for global variables and global functions. Encoding type information into names (Hungarian notation) is forbidden as unnecessary compiler clutter.
    - **Their words:** "C is a Spartan language, and your naming conventions should follow suit... descriptive names for global variables are a must. To call a global function ``foo`` is a shooting offense. GLOBAL variables (to be used only if you <strong>really</strong> need them) need to have descriptive names, as do global functions... LOCAL variable names should be short, and to the point. If you have some random integer loop counter, it should probably be called ``i``... Encoding the type of a function into the name (so-called Hungarian notation) is asinine - the compiler knows the types anyway and can check those, and it only confuses the programmer." — *Gloss:* Minimize identifier length for narrow local contexts while enforcing explicit semantic naming for globally exposed identifiers.
    - **Source:** `Documentation/process/coding-style.rst` §4 "Naming"
    - **Words are:** `quoted` (Linus Torvalds's first-person text in `coding-style.rst`)
    - **From:** top-12 #12

## Gaps
- **No web fetching was possible:** In accordance with the headless execution constraints, external network requests and URL fetching tools were disabled. All citations and checks were drawn strictly from the local repository files under `runs/20261013-four-seats/sources/linus/` (`management-style.html`, `coding-style.html`, `submitting-patches.html`, `2.Process.html`).
- **Famous mailing list statements could not be verified from primary sources:** Iconic Torvalds decisions documented on LKML—such as the "never break userspace" rule, the git pull refusals, the 2007 Google Tech Talk rules on data structures and git, and the August 2007 "I'M A COMPLETE IDIOT" posting—are not preserved in the four local kernel documentation HTML files. They were excluded rather than reconstructed from memory or unverified secondary summaries.
- **Authorship attribution across documentation files:** While `coding-style.rst` begins with Torvalds's verified personal preamble and early chapters (§1–§9), chapters in `submitting-patches.rst` and `2.Process.rst` represent collaborative community documentation describing kernel practice or referring to Torvalds in the third person. Similarly, `management-style.rst` is composed in the first person and universally attributed to Torvalds, but its provenance in this static corpus lacks a signed git commit block. These items are strictly labelled `attributed` or identified as attributed first-person text to avoid over-claiming personal speech.
- **Excluded rules lacking strict textual grounding:** Statements asserting that Torvalds "never decides anything" or takes "only one irreversible decision per cycle" were omitted because the texts describe a multi-week merge window with ongoing pull requests and rare mid-cycle exceptions. Likewise, Greg Kroah-Hartman's `stable-api-nonsense.rst` was excluded because it represents Kroah-Hartman's authorship rather than Torvalds's own words.
