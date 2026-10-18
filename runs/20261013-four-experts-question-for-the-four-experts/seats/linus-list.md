# Linus Torvalds — final list

## Changes from the top 12

1. **corrected → #4.** Drops "never", "whoever wrote the code" and "your own judgement is not the input that matters";
   restores the limits the text gives: "at least the big and painful ones", and "Making small and non-consequential
   decisions is fine" (codex row 1, agreed). Codex calls authorship "not checkable"; I add LWN's 6 Oct 2004
   publication under the title "Linus on kernel management style" and his 2005 mail on the document. That is still
   attribution, not a commit record (see Gaps).
2. **corrected → #5.** The "two" decisions are the wrong one and the right one, not a split of one decision into
   two (codex row 2, agreed). "Being wrong is cheap" is removed. The text's own warning is added: undoing a year's
   work can irrevocably lose an engineer's trust, which makes the decision a big one after all.
3. **corrected → #7.** The quotes are now separate excerpts in source order (codex row 3, agreed: "Make them at
   least think twice" comes before "The best thing you can do as a manager"). The headline "Nobody is above
   suspicion" is not in the text. It is replaced by the text's own line "the corollary to that is sadly that you are
   one too".
4. **corrected → #6.** "Actively recruit" and "never push hard" are removed. The text says "take advantage of them"
   and "just don't push too hard" (codex row 4, agreed). Kept apart from #4 as codex asks: #4 is about not
   arbitrating without the details, #6 is about letting the people who know more decide.
5. **kept → #15.** (Codex row 5: keep.) "If you can find them" is kept. The gloss "paid first, in cash, without
   excuse" is removed because the text does not say it.
6. **corrected → #16.** "Without softening" reverses the text, which says "Some humor can help pad both the
   bluntness and the moralizing" (codex row 6, agreed). His 2018 apology for personal attacks in email is added,
   because it is his own later word on the same behaviour.
7. **dropped; its timing line merged into #11.** It is narrator voice (`2.Process.rst`, third person). "One big
   irreversible decision, once per cycle" is not in the text, and the text allows exceptions to "only fixes" (codex
   row 7, agreed). His own words about timing ("explain the _timing_") are in the 2017 mail used in #11. Codex
   marked the item "change"; I drop it because nothing left in it is his words, and #1, #2 and #11 now show him
   deciding in his own words.
8. **corrected → #14.** Relabelled `attributed`, because the passage talks about him in the third person (codex row
   8, agreed). Codex's second missing item (he generally trusts maintainers and sometimes looks closely) and his own
   2005 words on trusting maintainers are merged in.
9. **dropped as a Linus rule; replaced by #11 in his own words.** I opened the Linus mail that
   `submitting-patches.rst` cites as the source of "The canonical patch format" (`Pine.LNX.4.58.0504071023190.28951`,
   LKML 7 Apr 2005). It covers only the email layout: a sortable `[PATCH 001/123]` subject, a `From:` line, the
   explanation, `Signed-off-by:`, `---`, then the diffstat. The 70–75 character summary and the "competent reader who
   has long since forgotten" text are not in it. **I disagree with codex here.** Codex row 9 keeps the item "as
   documentation guidance". It was in a Linus list only because of a Linus attribution, and that attribution does not
   hold for these rules.
10. **corrected → #19.** The headline's "never post more than about fifteen" is replaced by the source's condition
    and approximation: "If you cannot condense … only post say 15 or so" (codex row 10, agreed). Relabelled
    `attributed`: these are kernel-doc words and not shown to be his (see #9 above).
11. **corrected → #18.** Relabelled `attributed` (codex row 11, agreed). The rule itself is unchanged.
12. **corrected → #17.** "No external standard has authority" and "the only test" are removed. The same document
    says GNU indent's makers "recognize the authority of K&R" and recommends formatting tools (codex row 12, agreed).
    The "checker is a guide" clause is dropped because it comes from `submitting-patches.rst`, not from his text.
    Naming is dropped to keep the item to what he states as rules for code he must maintain. The text is now
    confirmed present, in the first person, in `Documentation/CodingStyle` of Linux 2.0 (1996).

**Codex's "Missing" rows:** row 1 ("can't we just do both?") is new item #8. I word it without codex's "keep
competing approaches alive", because the text does not say that. Row 2 is merged into #14.

## Final list

1. **A change that breaks what used to work for users is a kernel bug: fix it or revert it, in the kernel, and admit it.**
   - **Kind:** decision rule
   - **Rule:** If a change makes user programs break, the bug is in the kernel, not in the user program. The change
     must be fixed or reverted, and fixed in the kernel. When a regression happens, it is admitted and fixed instead of
     blamed on user space. If the kernel used to work for you, it continues to work for you. He says there have been
     exceptions, but "few and far between". For API breakage inside the kernel: whoever broke something fixes it too.
   - **Their words:** (English original)
     - "If a change results in user programs breaking, it's a bug in the kernel. We never EVER blame the user programs." … "WE DO NOT BREAK USERSPACE!"
     - "The first rule is: - we don't cause regressions and the corollary is that when regressions *do* occur, we admit to them and fix them, instead of blaming user space."
     - "If the kernel used to work for you, the rule is that it continues to work for you. There have been exceptions, but they are few and far between, and they generally have some major and fundamental reasons for having happened, that were basically entirely unavoidable, and people _tried_hard_ to avoid them."
     - "But if something actually breaks, then the change must get fixed or reverted. And it gets fixed in the *kernel*."
     - "Nobody can say "I now broke the API you used, and now _you_ need to fix it up". Whoever broke something gets to fix it too."
   - **Source:** LKML, 23 Dec 2012, "Re: [Regression w/ patch] Media commit causes user space to misbahave (was: Re:
     Linux 3.8-rc1)", https://lkml.org/lkml/2012/12/23/75 · LKML, 26 Oct 2017, "Re: regression in 4.14-rc2 caused
     by apparmor: add base infastructure for socket mediation",
     https://lkml.iu.edu/hypermail/linux/kernel/1710.3/02474.html and …/1710.3/02487.html
   - **Words are:** `quoted`
   - **From:** new (my research)

2. **Talk is cheap; show the code.**
   - **Kind:** mindset
   - **Rule:** A claim that something can be built costs nothing to make; what he asks for is the code. In 2017 he
     did not accept a main pull request because its untested code "clearly didn't do what it claimed it did".
   - **Their words:** (English original)
     - "Talk is cheap. Show me the code." (his whole reply to Jamie Lokier's claim that the best of user-space and
       kernel threads could be combined "in less than 8kB per thread")
     - "untested code that clearly didn't do what it claimed it did, and which caused me to not even accept the main pull request"
   - **Source:** LKML, 25 Aug 2000, "Re: SCO: "thread creation is about a thousand times faster than on native
     Linux"", https://lkml.org/lkml/2000/8/25/132 · LKML, 26 Oct 2017, same apparmor thread,
     https://lkml.iu.edu/hypermail/linux/kernel/1710.3/02507.html
   - **Words are:** `quoted`
   - **From:** new (my research). This is the line `design.md` builds the Linus seat on; this is its primary source.

3. **What counts as a regression is a user's breakage, not an ABI, a document or a test.**
   - **Kind:** decision rule
   - **Rule:** A regression is the kernel not giving the same end result with the same user space. The rule is about
     breaking a user's workflow. It is not about documented behaviour, about where the code lives, or about behaviour
     never changing. A test that now behaves differently is a warning sign, not by itself a regression. Changing an
     API is fine as long as nobody notices.
   - **Their words:** (English original)
     - "As far as the kernel is concerned, a regressions is THE KERNEL NOT GIVING THE SAME END RESULT WITH THE SAME USER SPACE." (2017)
     - "The rules about regressions have never been about any kind of documented behavior, or where the code lives. The rules about regressions are always about "breaks user workflow". Users are literally the _only_ thing that matters." (2020)
     - "And our regression rule has never been "behavior doesn't change". That would mean that we could never make any changes at all." (2017)
     - "But if you have some random test that now behaves differently, it's not a regression. It's a *warning* sign, sure: tests are useful." (2024)
     - "You can make any changes to an API you like - as long as nobody notices." (2020/2021, see Gaps)
   - **Source:** 2017 line: LKML 26 Oct 2017, https://lkml.iu.edu/hypermail/linux/kernel/1710.3/02474.html (opened).
     The others: his mails as reproduced in `Documentation/process/handling-regressions.rst`, "Quotes from Linus
     about regression" (https://docs.kernel.org/process/handling-regressions.html), entries 2020-05-21, 2017-11-05,
     "2024-29-01" and 2021-05-21, each with its lore.kernel.org link (originals not opened).
   - **Words are:** `quoted`
   - **From:** new (my research)

4. **Avoid having to make the big decisions; the people who know the details should not need you to pick.**
   - **Kind:** decision rule
   - **Rule:** The aim is to avoid having to make decisions, at least the big and painful ones. If people you manage
     ask you to choose (a) or (b) on a technical matter, you are in trouble: they should know the details better than
     you, so you are not competent to decide it for them. If they don't know the details better than you, you are in
     the wrong job. Small, non-consequential decisions are fine. The job is to turn the big and painful ones into small
     things.
   - **Their words:** (English original) "The name of the game is to avoid having to make a decision. In particular,
     if somebody tells you "choose (a) or (b), we really need you to decide on this", you're in trouble as a manager.
     The people you manage had better know the details better than you, so if they come to you for a technical
     decision, you're screwed. You're clearly not competent to make that decision for them." … "So the name of the
     game is to avoid decisions, at least the big and painful ones. Making small and non-consequential decisions is
     fine, and makes you look like you know what you're doing, so what a kernel manager needs to do is to turn the big
     and painful ones into small things where nobody really cares."
   - **Source:** `Documentation/process/management-style.rst` §1 "Decisions",
     https://docs.kernel.org/process/management-style.html. The same text is in LWN, 6 Oct 2004, "Linus on kernel
     management style", https://lwn.net/Articles/105375/
   - **Words are:** `quoted`. Authorship is by attribution only (see Gaps).
   - **From:** top-12 #1 (corrected)

5. **A decision is big only if it can't be undone; avoid doing things that can't be undone.**
   - **Kind:** decision rule
   - **Rule:** What separates a big decision from a small one is whether you can fix it afterwards. Any decision can be
     made small by making sure that, if you were wrong (and you will be wrong), you can undo the damage by
     backtracking. So avoid doing things that can't be undone. Deleting the work is easy, but you may have irrevocably
     lost the trust of the engineer who did it, and then the decision was a big one after all.
   - **Their words:** (English original) "It helps to realize that the key difference between a big decision and a
     small one is whether you can fix your decision afterwards. Any decision can be made small by just always making
     sure that if you were wrong (and you will be wrong), you can always undo the damage later by backtracking." …
     "Thus the key to avoiding big decisions becomes to just avoiding to do things that can't be undone. Don't get
     ushered into a corner from which you cannot escape." … "while the actual work was easy enough to undo by just
     deleting it, you may have irrevocably lost the trust of that engineer. And remember: "irrevocable" was what we
     tried to avoid in the first place, and your decision ended up being a big one after all."
   - **Source:** `management-style.rst` §1 "Decisions"; LWN 2004 (as #4)
   - **Words are:** `quoted`. Authorship is by attribution only (see Gaps).
   - **From:** top-12 #2 (corrected)

6. **Let people smarter than you make the decisions; prod, don't push too hard.**
   - **Kind:** decision rule
   - **Rule:** Take advantage of smart people: they can make your decisions for you. When you find somebody smarter
     than you, coast along, and your job becomes saying "Sounds like a good idea - go wild" or "That sounds good, but
     what about xxx?". Greatness in one area does not necessarily carry over to others. You may prod people in a
     direction, which is not irreversible because people drift back to what they are good at, but don't push too hard.
   - **Their words:** (English original) "Some people react badly to smart people. Others take advantage of them.
     Make sure that you, as a kernel maintainer, are in the second group. Suck up to them, because they are the people
     who will make your job easier. In particular, they'll be able to make your decisions for you, which is what the
     game is all about." … "So when you find somebody smarter than you are, just coast along. Your management
     responsibilities largely become ones of saying "Sounds like a good idea - go wild", or "That sounds good, but what
     about xxx?"." … "One thing to look out for is to realize that greatness in one area does not necessarily translate
     to other areas. So you might prod people in specific directions, but let's face it, they might be good at what
     they do, and suck at everything else. The good news is that people tend to naturally gravitate back to what they
     are good at, so it's not like you are doing something irreversible when you do prod them in some direction, just
     don't push too hard."
   - **Source:** `management-style.rst` §3 "People II - the Good Kind"; LWN 2004
   - **Words are:** `quoted`. Authorship is by attribution only (see Gaps).
   - **From:** top-12 #4 (corrected)

7. **Say up front that you may be wrong; give people critical thinking, not confidence.**
   - **Kind:** mindset
   - **Rule:** Admit up front that you don't know. Tell people ahead of time that your decision is preliminary and
     might be wrong, keep the right to change your mind, and make sure they know it. If the people doing the work
     aren't sure their work is a good idea, don't encourage them by promising it will be included; make them think
     twice before a big endeavour. The best thing a manager can do is give them a healthy dose of critical thinking
     about what they do, not confidence. And you are one of the idiots too.
   - **Their words:** (English original, in source order) "Happily, both of these reasons can be mitigated
     effectively by just admitting up-front that you don't have a friggin' clue, and telling people ahead of the fact
     that your decision is purely preliminary, and might be the wrong thing. You should always reserve the right to
     change your mind, and make people very aware of that." … "After all, if they aren't certain whether it's a good
     idea, you sure as hell shouldn't encourage them by promising them that what they work on will be included. Make
     them at least think twice before they embark on a big endeavor." … "The best thing you can do as a manager is not
     to instill confidence, but rather a healthy dose of critical thinking on what they do." … (§3) "While it turns out
     that most people are idiots, the corollary to that is sadly that you are one too"
   - **Source:** `management-style.rst` §1 "Decisions", §3 "People II - the Good Kind"; LWN 2004
   - **Words are:** `quoted`. Authorship is by attribution only (see Gaps).
   - **From:** top-12 #3 (corrected)

8. **When it isn't clear which of two approaches is better, ask "can't we just do both?"**
   - **Kind:** decision rule
   - **Rule:** Another way to avoid a decision is to ask "can't we just do both?". If it is not clear which approach is
     better, the people involved will eventually figure it out. Sometimes both teams give up. He reads that as usually
     a sign that both projects had something wrong with them, and that they couldn't decide because both were wrong.
   - **Their words:** (English original) "Btw, another way to avoid a decision is to plaintively just whine "can't we
     just do both?" and look pitiful. Trust me, it works. If it's not clear which approach is better, they'll
     eventually figure it out. The answer may end up being that both teams get so frustrated by the situation that they
     just give up." … "That may sound like a failure, but it's usually a sign that there was something wrong with both
     projects, and the reason the people involved couldn't decide was that they were both wrong."
   - **Source:** `management-style.rst` §1 "Decisions"; LWN 2004
   - **Words are:** `quoted`. Authorship is by attribution only (see Gaps).
   - **From:** new (codex "Missing" row 1)

9. **Design the code around the data, not the other way round.**
   - **Kind:** mindset
   - **Rule:** He favours designing code around the data rather than the reverse, and gives it as one reason git
     worked. He claims the difference between a bad programmer and a good one is whether they treat their code or
     their data structures as more important.
   - **Their words:** (English original) "In fact, I'm a huge proponent of designing your code around the data,
     rather than the other way around, and I think it's one of the reasons git has been fairly successful (*)." …
     "(*) I will, in fact, claim that the difference between a bad programmer and a good one is whether he considers
     his code or his data structures more important. Bad programmers worry about the code. Good programmers worry
     about data structures and their relationships."
   - **Source:** git mailing list, 27 Jul 2006, "Re: Licensing and the library version of git", Message-ID
     `Pine.LNX.4.64.0607270936200.4168@g5.osdl.org`, https://marc.info/?l=git&m=115401850825206&w=2 (also LWN Quote
     of the week, 29 Jul 2006, https://lwn.net/Articles/193244/)
   - **Words are:** `quoted`
   - **From:** new (my research)

10. **Good code: see the problem differently so the special case becomes the normal case.**
    - **Kind:** mindset
    - **Rule:** Sometimes you can see a problem in a different way and rewrite it so that a special case goes away and
      becomes the normal case, and he calls that good code. The sign of people he wants to work with is good taste,
      which is about seeing the big patterns and knowing by instinct the right way to do things.
    - **Their words:** (English original, spoken; about two ways to remove an entry from a singly linked list) "I
      want you to understand that sometimes you can see a problem in a different way and rewrite it so that a special
      case goes away and becomes the normal case. And that's good code." … "To me, the sign of people I really want to
      work with is that they have good taste" … "Good taste is about really seeing the big patterns and kind of
      instinctively knowing what's the right way to do things."
    - **Source:** TED2016, "The mind behind Linux" (interview with Chris Anderson), transcript at
      https://www.ted.com/talks/linus_torvalds_the_mind_behind_linux/transcript
    - **Words are:** `quoted` (spoken, as TED's transcript gives it)
    - **From:** new (my research)

11. **A pull must tell him what he is pulling and why, as a record that will last; anything odd or late must be explained.**
    - **Kind:** decision rule
    - **Rule:** To him, the message is the important part. He wants to understand what he is pulling and why he should pull it. The
      message becomes the merge message, so it must also make sense as a historical record. Anything odd belongs in the
      explanation. If you touch files you don't maintain, explain why; he will see it in the diffstat anyway, and if it
      isn't mentioned he gets extra suspicious. For anything sent after the merge window, or fixes that look scary,
      explain what it does, why, and the timing.
    - **Their words:** (English original) "Anyway, at least to me, the important part is the *message*. I want to
      understand what I'm pulling, and why I should pull it. I also want to use that message as the message for the
      merge, so it should not just make sense to me, but make sense as a historical record too. Note that if there is
      something odd about the pull request, that should very much be in the explanation. If you're touching files that
      you don't maintain, explain _why_. I will see it in the diffstat anyway, and if you didn't mention it, I'll just
      be extra suspicious. And when you send me new stuff after the merge window (or even bug-fixes, but ones that look
      scary), explain not just what they do and why they do it, but explain the _timing_. What happened that this
      didn't go through the merge window.."
    - **Source:** LKML, 14 Nov 2017, "Re: git pull", https://lkml.iu.edu/hypermail/linux/kernel/1711.1/04939.html
      (also reproduced in `Documentation/maintainer/pull-requests.rst`, "As said by Linus")
    - **Words are:** `quoted`
    - **From:** new (my research). Replaces top-12 #9 and takes the timing point of top-12 #7.

12. **Clean history: rebase your own private work, never other people's history; merge only for a reason.**
    - **Kind:** decision rule
    - **Rule:** People can, and probably should, rebase their own private trees, which is cleanup. Never rebase other
      people's history, which destroys it. The rule is about history, not code: a patch you applied yourself is your
      history. Once you have published your history, it is no longer private. Don't push out work that is still in the
      rebase phase. Don't merge upstream code at random points, and have a reason for merging downstream work. He won't
      pull from a tree whose log is full of random merges of his tree.
    - **Their words:** (English original) "I want clean history, but that really means (a) clean and (b) history.
      People can (and probably should) rebase their _private_ trees (their own work). That's a _cleanup_. But never
      other peoples code. That's a "destroy history"" … "You must never EVER destroy other peoples history. You must
      not rebase commits other people did." … "Notice that this really is about other peoples _history_, not about
      other peoples _code_." … "once you've published your history in some public site, other people may be using it,
      and so now it's clearly not your _private_ history any more." … "Don't expose your crap. This means: if you're
      still in the "git rebase" phase, you don't push it out." … "Don't merge upstream code at random points." …
      "Slightly more complex version: "Always have a _reason_ for merging downstream stuff"." … "But if I see a lot of
      "Merge branch 'linus'" in your logs, I'm not going to pull from you, because your tree has obviously had random
      crap in it that shouldn't be there."
    - **Source:** "Re: [git pull] drm-next", to Dave Airlie, 29 Mar 2009, Message-ID
      `alpine.LFD.2.00.0903291409030.3994@localhost.localdomain`, as published at https://lwn.net/Articles/328438/
    - **Words are:** `quoted`
    - **From:** new (my research)

13. **Start small, for an immediate need; don't push your "vision" too hard on the project.**
    - **Kind:** mindset
    - **Rule:** Don't set out to build a large project. Start with a small, trivial one and don't expect it to get
      large; expecting that leads to over-design, or to being scared off. Think about the details, not a big picture:
      if it doesn't solve a fairly immediate need, it is almost certainly over-designed. Projects have a life of their
      own, so don't enforce your "vision" too strongly. You are usually wrong anyway, so be willing to take input,
      change direction and admit mistakes.
    - **Their words:** (English original) "Nobody should start to undertake a large project. You start with a small
      _trivial_ project, and you should never expect it to get large. If you do, you'll just overdesign and generally
      think it is more important than it likely is at that stage. Or worse, you might be scared away by the sheer size
      of the work you envision. So start small, and think about the details. Don't think about some big picture and
      fancy design. If it doesn't solve some fairly immediate need, it's almost certainly over-designed." … "projects
      have a life of their own, and you should _not_ try to enforce your "vision" too strongly on them. Most often
      you're wrong anyway, and if you're not flexible and willing to take input from others (and willing to change
      direction when it turned out your vision was flawed), you'll never get anything good done. In other words, be
      willing to admit your mistakes" · TED2016: "I am not a visionary. I do not have a five-year plan. I'm an
      engineer." … "But I'm looking at the ground, and I want to fix the pothole that's right in front of me before I
      fall in."
    - **Source:** Linux Times email interview by Preston St. Pierre, posted 25 Oct 2004 ("Linus Torvalds: 'Desktop
      Market has already started'"), Wayback capture
      https://web.archive.org/web/20041106193140/http://www.linuxtimes.net/modules.php?name=News&file=article&sid=145 ·
      TED2016 transcript (as #10)
    - **Words are:** `quoted`
    - **From:** new (my research)

14. **Patches go to the subsystem maintainer; he trusts the maintainers he pulls from and avoids being the throttle.**
    - **Kind:** decision rule
    - **Rule:** Patches go to the subsystem maintainer, and very few go through him directly. People are told to avoid
      sending him email even though he is the final arbiter. When he pulls from maintainers, the attention he gives
      varies: sometimes he looks quite closely, but as a general rule he trusts them not to send bad patches. In his
      own words in 2005, he can process a hundred emailed patches almost as easily as one "as long as I trust the
      maintainer". If no parallel-merge tool could be found soon, he would distribute the merging over a few people
      rather than be the throttle himself.
    - **Their words:** (English original)
      - Doc: "Linus Torvalds is the final arbiter of all changes accepted into the Linux kernel. … He gets a lot of e-mail, and, at this point, very few patches go through Linus directly, so typically you should do your best to -avoid- sending him e-mail."
      - Doc: "The amount of attention that Linus pays to specific patches received in a pull operation varies. It is clear that, sometimes, he looks quite closely. But, as a general rule, Linus trusts the subsystem maintainers to not send bad patches upstream."
      - His 2005 words: "I can process a hundred emails almost as easily as one, as long as I trust the maintainer (which, when it's used as a BK replacement, I obviously do)." … "at least try to distribute the merging out over a few people rather than making _me_ be the throttle."
    - **Source:** `Documentation/process/submitting-patches.rst` "Select the recipients for your patch" ·
      `Documentation/process/2.Process.rst` §2.3 "How patches get into the Kernel" · LKML, 7 Apr 2005, "Re: Kernel
      SCM saga..", https://lkml.iu.edu/hypermail/linux/kernel/0504.0/1826.html
    - **Words are:** the two doc passages are `attributed` (third person, not his); the 2005 lines are `quoted`.
    - **From:** top-12 #8 (corrected), plus codex "Missing" row 2

15. **Take the blame, best of all for someone else; tell the one who really screwed up in private.**
    - **Kind:** decision rule
    - **Rule:** When things go wrong, take the blame, and the best way is to take it for someone else. Then let the
      developer who really screwed up (if you can find them) know in private. That way they can avoid it next time,
      they know they owe you one, and they are likely the person who can fix it. Taking the blame is part of what makes
      people trust you.
    - **Their words:** (English original) "Which brings us to the best way of taking the blame: do it for someone
      else. You'll feel good for taking the fall, they'll feel good about not getting blamed" … "Then make the
      developer who really screwed up (if you can find them) know in private that they screwed up. Not just so they can
      avoid it in the future, but so that they know they owe you one. And, perhaps even more importantly, they're also
      likely the person who can fix it." … "Taking the blame is also why you get to be manager in the first place. It's
      part of what makes people trust you"
    - **Source:** `management-style.rst` §4 "Placing blame"; LWN 2004
    - **Words are:** `quoted`. Authorship is by attribution only (see Gaps).
    - **From:** top-12 #5 (kept)

16. **Don't hide the problem in politeness; never be sanctimonious; apologise. In 2018 he apologised for his personal attacks.**
    - **Kind:** decision rule
    - **Rule:** Don't be too polite or subtle, because politeness can end up hiding the problem; make the point
      bluntly. Some humour can soften both the bluntness and the moralizing. Don't call people d*ckheads (at least not
      in public), and learn to apologise when you do. Worse than that is saying it in a sanctimonious voice, which
      people may not give you the chance to apologise for. Alienating people counts as "not reversible". In 2018 he
      wrote that his flippant attacks in email, especially the personal ones, were unprofessional and uncalled for,
      that this was not OK, and that he needed to change his behaviour.
    - **Their words:** (English original) "Similarly, don't be too polite or subtle about things. Politeness easily
      ends up going overboard and hiding the problem, and as they say, "On the internet, nobody can hear you being
      subtle". Use a big blunt object to hammer the point in, because you can't really depend on people getting your
      point otherwise. Some humor can help pad both the bluntness and the moralizing." … "don't call people d*ckheads
      (at least not in public)" / "learn how to apologize when you forgot rule (1)" … "There's one thing people hate
      even more than being called "d*ckhead", and that is being called a "d*ckhead" in a sanctimonious voice. The first
      you can apologize for, the second one you won't really get the chance." … "It turns out that alienating people is
      fairly easy, and un-alienating them is hard. Thus "alienating" immediately falls under the heading of "not
      reversible"" · 2018: "My flippant attacks in emails have been both unprofessional and uncalled for. Especially at
      times when I made it personal. In my quest for a better patch, this made sense to me. I know now this was not OK
      and I am truly sorry." … "hey, I need to change some of my behavior"
    - **Source:** `management-style.rst` §2 "People", §5 "Things to avoid"; LWN 2004 · LKML, 16 Sep 2018, "Linux
      4.19-rc4 released, an apology, and a maintainership note", https://lkml.org/lkml/2018/9/16/167
    - **Words are:** `quoted` (management-style authorship by attribution only, see Gaps; the 2018 mail is his)
    - **From:** top-12 #6 (corrected)

17. **For code he has to maintain: short functions that do one thing, shallow nesting, comments that say what and not how.**
    - **Kind:** decision rule
    - **Rule:** These are his rules for code he has to maintain. He won't force them on anybody else, but would prefer
      them there too. Functions should be short and do one thing. If you need more than 3 levels of indentation, fix
      your program. Local variables shouldn't exceed 5–10, because "maybe you'd like to understand what you did 2
      weeks from now". Comments should say what the code does, not how. A formatting tool is not a fix for bad
      programming.
    - **Their words:** (English original) "Coding style is very personal, and I won't _force_ my views on anybody, but
      this is what goes for anything that I have to be able to maintain, and I'd prefer it for most other things too.
      Please at least consider the points made here." … "if you need more than 3 levels of indentation, you're screwed
      anyway, and should fix your program." … "Functions should be short and sweet, and do just one thing." … "Another
      measure of the function is the number of local variables. They shouldn't exceed 5-10, or you're doing something
      wrong." … "You know you're brilliant, but maybe you'd like to understand what you did 2 weeks from now." …
      "Generally, you want your comments to tell WHAT your code does, not HOW." … "But remember: "indent" is not a fix
      for bad programming."
    - **Source:** `Documentation/CodingStyle` in the Linux 2.0 release (1996), chapters 1, 4, 5 and 6
      (https://cdn.kernel.org/pub/linux/kernel/v2.0/linux-2.0.tar.gz). The same sentences are in today's
      `Documentation/process/coding-style.rst`, opening and §1, §6, §8, §9.
    - **Words are:** `quoted`, first person ("anything that I have to be able to maintain"). Authorship is by
      attribution, not by signature (see Gaps).
    - **From:** top-12 #12 (corrected)

18. **Quantify the claimed win and state its costs; the description must stand alone.**
    - **Kind:** decision rule
    - **Rule:** Describe the problem that motivated the patch and its impact on users. If you claim improvements in
      performance, memory, stack footprint or binary size, include numbers that back them up. Also describe the
      expected downsides, so the reviewer can weigh costs against benefits. Every submission or resubmission carries
      its complete description, not just "version N", so that it is self-contained.
    - **Their words:** (English original) "Describe your problem. Whether your patch is a one-line bug fix or 5000
      lines of a new feature, there must be an underlying problem that motivated you to do this work." … "Quantify
      optimizations and trade-offs. If you claim improvements in performance, memory consumption, stack footprint, or
      binary size, include numbers that back them up. But also describe non-obvious costs." … "Describe the expected
      downsides of your optimization so that the reviewer can weigh costs against benefits." … "Don't just say that
      this is version N of the patch (series)." … "I.e., the patch (series) and its description should be
      self-contained."
    - **Source:** `Documentation/process/submitting-patches.rst` "Describe your changes",
      https://docs.kernel.org/process/submitting-patches.html
    - **Words are:** `attributed`: kernel process documentation, not shown to be his words. He is named in the same
      document as the final arbiter.
    - **From:** top-12 #11 (corrected: relabelled)

19. **One logical change per patch, each one buildable; send a long series about 15 at a time.**
    - **Kind:** decision rule
    - **Rule:** Put each logical change in its own patch, and keep a single change across many files in one patch.
      Each patch should be easy to understand, verifiable, and justifiable on its own merits. In a series, the kernel
      should build and run after each patch, because `git bisect` may split the series anywhere. If you cannot condense
      the set, post say 15 or so at a time and wait for review and integration.
    - **Their words:** (English original) "Separate each logical change into a separate patch." … "On the other hand,
      if you make a single change to numerous files, group those changes into a single patch." … "The point to
      remember is that each patch should make an easily understood change that can be verified by reviewers. Each patch
      should be justifiable on its own merits." … "take special care to ensure that the kernel builds and runs properly
      after each patch in the series. Developers using git bisect to track down a problem can end up splitting your
      patch series at any point; they will not thank you if you introduce bugs in the middle." … "If you cannot
      condense your patch set into a smaller set of patches, then only post say 15 or so at a time and wait for review
      and integration."
    - **Source:** `Documentation/process/submitting-patches.rst` "Separate your changes"
    - **Words are:** `attributed`: kernel process documentation, not shown to be his words.
    - **From:** top-12 #10 (corrected)

## Gaps

- **The order of the list is my reading, not measured.** Placing #1–#3 first rests on his calling the regression rule
  "the first rule of kernel development" (2017) and on how often he restates it. #2 is near the top partly because
  `design.md` builds the seat on it.
- **Who wrote `management-style.rst` (#4–#8, #15, #16) is attribution only.** Three pieces of evidence: LWN published
  it on 6 Oct 2004 under the title "Linus on kernel management style"; it is written in the first person as a kernel
  maintainer; and his own 2005 mail says "Most of the ManagementStyle document is perfectly valid"
  (https://lkml.iu.edu/hypermail/linux/kernel/0509.3/0964.html). That mail calls the document painful truths said "as
  a joke"; it does not say he wrote it. I found no commit record: the git history starts at the 2.6.12-rc2 import
  (2005), and the BitKeeper-era history on git.kernel.org is behind Anubis. The document calls itself "a lark" that
  "may or may not have anything to do with reality". The sentences quoted here are the same in the 2004 LWN text.
- **Who wrote `coding-style` (#17) is also attribution.** I confirmed that the quoted sentences, first person
  included, are in `Documentation/CodingStyle` in the Linux 2.0 tarball (1996). No signature or commit record says
  who wrote it.
- **#18 and #19, and the doc passages in #14, are not his words.** The Linus mail that `submitting-patches.rst` cites
  (`Pine.LNX.4.58.0504071023190.28951@ppc970.osdl.org`, read at
  https://lkml.iu.edu/hypermail/linux/kernel/0504.0/1865.html) covers only the email layout. I kept them, labelled
  `attributed`, because they are the project's rules at his gate. They do not show how he personally decides.
- **Part of #3 comes through a document others curated.** I read the 2020, 2021 and "2024-29-01" lines in
  `handling-regressions.rst` (curated by Thorsten Leemhuis), not in the original mails, because lore.kernel.org
  blocks automated readers (Anubis). That document gives the same lore link under two dates (2020-05-21 and
  2021-05-21) and prints one date as "2024-29-01". I opened the 2012 and 2017 mails directly (lkml.org,
  lkml.iu.edu), and the quotes in #1 and the 2017 line in #3 match them.
- **#13 comes from a 2004 capture.** I read the interview in a Wayback capture of linuxtimes.net dated 2004-11-06. A
  reprint in an OSNews comment has the same wording. I did not see the original page live.
- **#10 and part of #13 are speech.** They are TED's transcript of a spoken interview, not text he wrote.
- **Left out because I could not state them without adding to the words, or could not source them:**
  - His 2006 remarks in the same thread as #9: with bad data structures, be willing to say "screw the ABI". They were
    about git and library ABIs. Next to #1 they would read as a contradiction unless I add context the words do not
    give.
  - "Security problems are just bugs" (2008): I did not open the mail. The verified 2021 line, "security people need
    to understand that "not working" is not a success case of security", is in `handling-regressions.rst` but was not
    needed beyond #1 and #3.
  - The 2007 Google talk on git: not checked.
  - "Given enough eyeballs, all bugs are shallow": Eric Raymond's words, not his.
  - `coding-style.rst` §22 (WARN rather than BUG): added by David Hildenbrand in 2022, as the identity research found.
  - `stable-api-nonsense.rst`: Greg Kroah-Hartman's.
- **The 2012 mail in #1 is written in the abusive style he apologised for in 2018 (#16).** Only its rule lines are
  quoted here.
- **I did not read `runs/20261013-four-seats/final/`,** as my brief required. Codex's review was read and used row by
  row above. Codex worked from the four local files without web access. My authorship findings add evidence for
  management-style and coding-style but no proof.
