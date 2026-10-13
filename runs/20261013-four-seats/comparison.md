# agy vs Opus — final lists compared

Written by Claude (main session), 2026-10-13. agy = `gemini-3.8-flash-medium`, no web (headless denies `read_url`),
`final/`. Opus = Opus xhigh with web, `final-opus/`. The two were blind to each other.

**How matched:** my script (`compare.py`, scratchpad) pairs items by shared 3-character runs of the quoted Chinese
(English words for Linus), threshold 0.35. Approximate: e.g. agy 范蠡 #12 and #13 quote the same 國語21:19 passage, so
one of them shows as "agy only" though Opus #8 covers both. Read "only" as "no close match found", not "absent".

**Quote check (my script, words only):** every Opus quote found in the sources, counting the texts the Opus seats
fetched (in the session scratchpad, not yet in `sources/`). agy: 范蠡 163/164, 孫子 294/294, 老子 273/275, Linus
49/51. agy 老子 ch.66 blends two editions: 「是以聖人欲上民」 is in neither (王弼 「是以欲上民」, silk 「是以聖人之欲上民也」)
and 「非以其無爭與」 is the silk's question written with 爭 for its 諍.

## fan-li
```
agy 17 items, opus 18 items, matched 14
  both  opus#2  agy#1  0.52  Three kinds of state affairs, three things to go by
  both  opus#3  agy#2  0.91  While the time has not come
  both  opus#4  agy#4  0.78  When the time comes, go; having it, finish
  both  opus#5  agy#9  0.72  The plan does not shift
  both  opus#6  agy#7  0.77  Leaving
  both  opus#8  agy#13 0.91  A fresh disaster can unite the enemy
  both  opus#9  agy#10 0.76  Disorder that has only sprouted
  both  opus#11 agy#17 0.85  People start it, Heaven and Earth show it, the sage completes it
  both  opus#12 agy#11 0.54  When to engage
  both  opus#13 agy#3  0.84  Contention is the last of affairs
  both  opus#14 agy#6  0.72  Say who is better at what
  both  opus#15 agy#5  0.73  Steadying what is tilting: humble yourself, then bargain with your per
  both  opus#16 agy#16 0.74  Take a method that worked for the state to the household
  both  opus#17 agy#14 0.83  Send the one who can part with money
  OPUS only #1  Keep to the time: Heaven's time and human affairs together
  OPUS only #7  Do not plan early
  OPUS only #10 Turning at the extreme, and stopping
  OPUS only #18 Examine the preparations
  AGY only  #8  Reaching great wealth at home and the rank of minister in office is the extreme 
  AGY only  #12 When an enemy's disaster is fresh and their populace is terrified, their leaders
  AGY only  #15 When a besieging victory is at hand and the adversary attempts to stall through 
```

## sun-tzu
```
agy 17 items, opus 20 items, matched 16
  both  opus#1  agy#1  0.78  Reckon before battle
  both  opus#2  agy#3  0.77  Make yourself unbeatable first; win, then seek battle
  both  opus#3  agy#2  0.98  Whole over broken; strike plans first, walled cities last
  both  opus#4  agy#4  0.63  Know whether you can fight; know the other side and yourself
  both  opus#5  agy#5  1.00  Move only when it accords with advantage; never from anger
  both  opus#7  agy#7  0.84  War is the way of deception
  both  opus#8  agy#12 0.53  Value victory, not duration; speed; supply from the enemy
  both  opus#9  agy#9  1.00  Bring the other side to you; do not be brought
  both  opus#10 agy#8  0.73  Avoid the solid, strike the empty; have no constant form
  both  opus#11 agy#6  0.64  Foreknowledge must come from people; pay for it
  both  opus#12 agy#10 0.56  Seek it in 勢, made of the regular and the irregular, not from the peop
  both  opus#15 agy#15 0.68  The general's faults: five dangers, six defeats
  both  opus#16 agy#13 0.74  Orders clear first, then enforced; care that cannot command is useless
  both  opus#17 agy#16 0.76  Learn the enemy by probing and by signs
  both  opus#18 agy#14 1.00  Spirit, heart, strength and change: meet theirs with yours
  both  opus#19 agy#17 0.97  Name the ground, act as prescribed; troops with no way out fight
  OPUS only #6  In deliberating, mix harm into benefit
  OPUS only #13 Not every road is taken, and not every command of the ruler is accepted
  OPUS only #14 Choose the action by the ratio of forces
  OPUS only #20 Which house falls first: judge by the land unit, the tax, and what they breed
  AGY only  #11 In battle, engage with the orthodox and win with the unorthodox. The changes of 
```

## lao-tzu
```
agy 17 items, opus 19 items, matched 15
  both  opus#1  agy#1  0.61  Take away, and take away again.
  both  opus#2  agy#9  0.78  Know what is enough; know to stop.
  both  opus#4  agy#2  0.59  Acting on it ruins it; gripping it loses it.
  both  opus#6  agy#5  0.47  Act while it is small and easy; treat it as difficult.
  both  opus#7  agy#6  0.40  Be as careful at the end as at the beginning.
  both  opus#8  agy#11 0.71  Know that you do not know.
  both  opus#9  agy#14 0.47  To be above, put yourself below; to be in front, put yourself behind.
  both  opus#10 agy#10 0.88  Three treasures: compassion, frugality, not daring to be first.
  both  opus#12 agy#8  0.72  What is to be shrunk must first be stretched.
  both  opus#13 agy#16 0.46  Achieve the result and stop; use weapons when it cannot be avoided; mo
  both  opus#14 agy#3  0.65  Do not display yourself; do not contend.
  both  opus#15 agy#4  0.77  The highest good is like water.
  both  opus#16 agy#12 1.00  Knowing yourself is clarity; overcoming yourself is strength.
  both  opus#17 agy#15 1.00  The use is in what is not there.
  both  opus#18 agy#13 1.00  When your time comes, ride out; when it does not, drift away.
  OPUS only #3  Stop before it is full; when the work is done, withdraw.
  OPUS only #5  I do not act, and the people transform by themselves.
  OPUS only #11 The weak and soft overcome the hard and strong.
  OPUS only #19 Where others take the front, take the rear; restraint as the rule.
  AGY only  #7  When the work is accomplished and merit achieved, withdraw oneself; accomplish r
  AGY only  #17 The reason one experiences great misfortune or distress is having a bodily self;
```

## linus
```
agy 18 items, opus 19 items, matched 11
  both  opus#4  agy#1  0.66  Avoid having to make the big decisions; the people who know the detail
  both  opus#5  agy#2  0.71  A decision is big only if it can't be undone; avoid doing things that 
  both  opus#6  agy#5  0.78  Let people smarter than you make the decisions; prod, don't push too h
  both  opus#7  agy#4  0.69  Say up front that you may be wrong; give people critical thinking, not
  both  opus#8  agy#3  0.93  When it isn't clear which of two approaches is better, ask "can't we j
  both  opus#14 agy#10 0.50  Patches go to the subsystem maintainer; he trusts the maintainers he p
  both  opus#15 agy#6  0.77  Take the blame, best of all for someone else; tell the one who really 
  both  opus#16 agy#7  0.68  Don't hide the problem in politeness; never be sanctimonious; apologis
  both  opus#17 agy#16 0.49  For code he has to maintain: short functions that do one thing, shallo
  both  opus#18 agy#13 0.77  Quantify the claimed win and state its costs; the description must sta
  both  opus#19 agy#11 0.84  One logical change per patch, each one buildable; send a long series a
  OPUS only #1  A change that breaks what used to work for users is a kernel bug: fix it or reve
  OPUS only #2  Talk is cheap; show the code.
  OPUS only #3  What counts as a regression is a user's breakage, not an ABI, a document or a te
  OPUS only #9  Design the code around the data, not the other way round.
  OPUS only #10 Good code: see the problem differently so the special case becomes the normal ca
  OPUS only #11 A pull must tell him what he is pulling and why, as a record that will last; any
  OPUS only #12 Clean history: rebase your own private work, never other people's history; merge
  OPUS only #13 Start small, for an immediate need; don't push your "vision" too hard on the pro
  AGY only  #8  Filter code through a lieutenant chain of trust while reserving selective scruti
  AGY only  #9  Open a two-week merge window for major changes, followed by stabilization releas
  AGY only  #12 Format commit messages for permanent changelogs and separate transient comments
  AGY only  #14 Do not modify moved code in the patch that moves it
  AGY only  #15 Treat automated style checkers as guides subordinate to human judgment
  AGY only  #17 Write comments to explain what and why code works, never how
  AGY only  #18 Scale variable naming descriptiveness to scope: Spartan locals, descriptive glob
```

