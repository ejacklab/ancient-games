I'll read the brief first.
I'll research this properly with primary sources before drafting.
Wikipedia output was mostly boilerplate. Going straight to primary texts.
ctext blocks automated access. Trying Wikisource and other primary mirrors.
Got the full received text. Now the 銀雀山 bamboo text — finding the right article.
Now the biography + textual-variant scholarship. Fetching raw wikitext to grep precisely.
One more: the bamboo-only chapter 〈吳問〉, where 孫子 speaks directly.
Research complete. I printed nothing to disk in the workspace; two source pages were fetched into `/tmp/opencode` for charset decoding only.

---

# 孫子 /孫武 (Sun Tzu) — who they are and how they decided

## Who they are

孫子, personal name 孫武, courtesy name 長卿, was a military man from 齊 (Qi), traditionally placed in the late Spring and Autumn period (544–496 BC). The earliest account of his life is Sima Qian's biography in 《史記·孫武孫臏吳起列傳》, written around 97 BC — roughly500 years after he is supposed to have lived; in it吳王闔廬 says 「子之十三篇，吾盡觀之矣」 ("your thirteen chapters — I have read them all") before testing him by drilling the king's 180 concubines, which he then turns into a functioning unit by executing the two company commanders who laughed ([史記/卷065, Wikisource](https://zh.wikisource.org/wiki/%E5%8F%B2%E8%A8%98/%E5%8D%B7065)). The biography credits him with 「西破彊楚，入郢，北威齊晉」 — breaking Chu, entering Ying, overawing Qi and Jin — a claim Sima Qian attaches to 孫子 and to no one else's strategy. What is known of his actual *decisions* is almost entirely the text 《孫子兵法》, thirteen chapters that open by declaring war 「國之大事，死生之地，存亡之道」 and never stop being an argument about how to decide under that weight ([孫子兵法, 始計第一](https://zh.wikisource.org/wiki/%E5%AD%AB%E5%AD%90%E5%85%B5%E6%B3%95)). That text's earliest layer is generally dated by scholars to the Warring States period, at least a century after the Sun Wu of the 《史記》 — Song-dynasty scholar 葉世 first noticed that the much earlier 《左傳》 never mentions him ([Sun Tzu, Wikipedia](https://en.wikipedia.org/wiki/Sun_Tzu)). The 1972 excavation of the銀雀山 Han tomb near Linyi, Shandong, turned up a Western Han bamboo copy of thirteen fragmentary chapters of 《孫子》 plus five further pieces under other or lost titles, alongside the then-lost 《孫臏兵法》 — the oldest physical witness to his writing ([Yinqueshan Han Slips](https://en.wikipedia.org/wiki/Yinqueshan_Han_Slips)). The honest summary: a man whose recorded biography is one famous training episode and one claimed campaign, and whose recorded reasoning is unusually complete and unusually early.

## Top 10 decision rules

1. **Rule (plain English):** Never commit to a course before you have counted; if you go in uncalculated, you have already lost.
   - **Their words:** 「兵者，國之大事，死生之地，存亡之道，不可不察也」…「多算勝，少算不勝，而況於無算乎？吾以此觀之，勝負見矣。」 — "War is a great matter of state, the ground of life and death, the road to preservation and ruin; it must not go unexamined… More calculation wins, less calculation loses — how much more so *none*. By this I judge, and victory or defeat is visible." (始計第一). And on where foreknowledge may legitimately come from: 「先知者，不可取於鬼神，不可象於事，不可驗於度，必取於人，知敵之情者也。」 — "For the foreknowing, it cannot be gotten from ghosts and spirits, cannot be matched to precedent, cannot be verified by calculation — it must be taken from people who know the enemy's situation." (用間第十三)
   - **Source:** 《孫子兵法》始計第一 and 用間第十三, in the received text at [zh.wikisource 孫子兵法](https://zh.wikisource.org/wiki/%E5%AD%AB%E5%AD%90%E5%85%B5%E6%B3%95)
   - **How it decides:** In: a decision whose downside is catastrophic and whose facts are contested → Out: run the five factors (道/天/地/將/法) and the seven comparisons (道/將/天地/法令/兵眾/士卒/賞罰) explicitly, and source missing information from people, not from omens, precedent, or arithmetic. Note the second half forbids *both* superstition *and* analysis-only as the source of certainty.
   - **Label:** `quoted`

2. **Rule (plain English):** Treat defeating an opponent without a battle as the goal; a fight is the fallback you pay for, and winning many fights is a sign you arranged things badly.
   - **Their words:** 「是故百戰百勝，非善之善者也；不戰而屈人之兵，善之善者也。」 — "Therefore a hundred battles won is not the best of the good; to subdue the enemy without battle is the best of the good." 「故上兵伐謀，其次伐交，其次伐兵，其下攻城。」 — "Hence the best army attacks plans; the next attacks alliances; the next attacks troops; the lowest assaults a city." (謀攻第三)
   - **Source:** 《孫子兵法》謀攻第三, received text, [zh.wikisource](https://zh.wikisource.org/wiki/%E5%AD%AB%E5%AD%90%E5%85%B5%E6%B3%95). He adds a hard cost ranking: 「攻城之法，為不得已」 — "the method of besieging a city is a last resort" — and he prices it: 「修櫓轒轀，具器械，三月而後成」, three months to build the equipment and three more to close the breach, with a third of your soldiers dead and the city still standing.
   - **How it decides:** In: an opponent you could reshape, outmaneuver, or detach, versus one you could only overpower → Out: spend your effort on plans, alliances, and positioning first; force a direct contest only when the cheaper options are closed. 「故善用兵者，屈人之兵而非戰也…必以全爭於天下，故兵不頓而利可全」 — "the skilled wielder of troops subdues an enemy without fighting… and must contest for all under heaven, so his troops never tire and his advantage is kept whole."
   - **Label:** `quoted`

3. **Rule (plain English):** Make yourself impossible to beat before you look for a way to beat them — and do not treat your own victory as a thing you can simply produce on demand.
   - **Their words:** 「昔之善戰者，先為不可勝，以待敵之可勝。不可勝在己，可勝在敵。故善戰者，能為不可勝，不能使敵之必可勝。故曰：勝可知，而不可為。」 — "The ancients' good commanders first made themselves unb defeatable and waited for the enemy to become defeatable. Being unb defeatable lies with you; being defeatable-able lies with the enemy. Hence the skilled commander can make himself unb defeatable; he cannot make the enemy necessarily defeatable. Hence: victory can be known, it cannot be manufactured." (軍形第四). Note不可勝/可勝 both begin with the syllable 可 — the same term, negated or not. The distinction is who holds it.
   - **Source:** 《孫子兵法》軍形第四, received text
   - **How it decides:** In: any plan whose win condition depends on the other party changing → Out: split the question. Everything within your own control becomes "first make yourself unb defeatable"; the enemy's error is only "waited for." Then 「勝兵先勝而後求戰，敗兵先戰而後求勝」 — "the victorious army wins before it seeks battle; the defeated army seeks battle before it wins."
   - **Label:** `quoted`

4. **Rule (plain English):** Prefer the quick, decisive course over the thorough, slow one; prolonged effort is itself the enemy.
   - **Their words:** 「其用戰也貴勝，久則鈍兵挫銳，攻城則力屈，久暴師則國用不足…故兵聞拙速，未睹巧之久也。夫兵久而國利者，未之有也。故不盡知用兵之害者，則不能盡知用兵之利也。」 — "In fighting he values victory. Long campaigns blunt the troops and dull their edge; besieging exhausts strength; a long-exposed army leaves the state's resources insufficient… So soldiers hear of clumsy haste; they have never seen skill in long duration. Long war that benefits the state — there has never been such. Therefore he who has not fully understood the harm of using troops cannot fully understand its benefit." (作戰第二)
   - **Source:** 《孫子兵法》作戰第二, received text
   - **How it decides:** In: an engagement whose resolution depends on outlasting the other side → Out: time-box it and treat slowness as a cost with a price, not as thoroughness. He runs the same logic on money: 「故智將務食於敵」 — "the wise commander feeds on the enemy" — 「食敵一鍾，當吾二十鍾」 — "one bushel taken from the enemy is worth twenty of my own."
   - **Label:** `quoted`

5. **Rule (plain English):** Change the conditions rather than exhorting the people; judge people by the position you put them in, not by their character.
   - **Their words:** 「故善戰者，求之於勢，不責於人，故能擇人而任勢。」 — "Therefore the skilled commander seeks it in the momentum and does not blame the men; being able to select men and invest them with momentum." 「任勢者，其戰人也，如轉木石。木石之性，安則靜，危則動，方則止，圓則行。」 — "One who commands momentum fights as one who rolls wood and stone. The nature of wood and stone: at rest they are still, on a slope they move; square they stop, round they roll." (兵勢第五)
   - **Source:** 《孫子兵法》兵勢第五, received text
   - **How it decides:** In: a team that is not delivering and a temptation to push harder on people → Out: move the ground — 「形之，敵必從之；予之，敵必取之。以利動之，以卒待之」 — "shape them and the enemy will follow; give them and the enemy will take it. Move them with advantage and meet them with troops." Same chapter, on complexity: 「紛紛紜紜，鬥亂而不可亂也；渾渾沌沌，形圓而不可敗也」 — "tangled and confused, fighting disorderly yet not disordered; formless, yet unbeatable."
   - **Label:** `quoted`

6. **Rule (plain English):** Make the other side come to you, and make the ground you meet them on unknowable to them.
   - **Their words:** 「故善戰者，致人而不致於人。」 — "Therefore the skilled commander draws the enemy in, and is not drawn in." 「故善攻者，敵不知其所守；善守者，敵不知其所攻。微乎微乎，至於無形；神乎神乎，至於無聲，故能為敵之司命。」 — "Hence the skilled attacker does not let the enemy know where he will defend; the skilled defender does not let the enemy know where he will attack. Subtler than subtle — reaching formlessness; more spiritlike than spiritlike — reaching silence. Thus he can be the arbiter of the enemy's life." (虛實第六)
   - **Source:** 《孫子兵法》虛實第六, received text
   - **How it decides:** In: a situation where the pacing and the terms are being set by the other party → Out: fix the conditions yourself (「我欲戰，敵雖高壘深溝，不得不與我戰者，攻其所必救也；我不欲戰…敵不得與我戰者，乖其所之也」 — "attack what they must rescue; go against where they are bound"). On information asymmetry: 「故形人而我無形，則我專而敵分」 — "let them see your form while you keep yours invisible, and you are concentrated while they are divided."
   - **Label:** `quoted`

7. **Rule (plain English):** Deceive deliberately and consistently — advertise what you cannot do, and it becomes a tool, not a trick.
   - **Their words:** 「兵者，詭道也。故能而示之不能，用而示之不用，近而示之遠，遠而示之近。利而誘之，亂而取之，實而備之，強而避之，怒而撓之，卑而驕之，佚而勞之，親而離之。攻其無備，出其不意。此兵家之勝，不可先傳也。」 — "War is the way of deception. Therefore when able, appear unable; when using, appear not to be using; when near, appear far; when far, appear near. Lure on advantage and take them in disorder; when they are solid, be prepared; when strong, avoid them; when angry, harass them; when humble, make them overconfident; when rested, tire them; when close, separate them. Attack where they are unprepared, emerge where they did not expect. This is the way to victory in war and cannot be transmitted beforehand." (始計第一). Restated as method, not tactic: 「故兵以詐立，以利動，以分合為變者也。」 — "War is established on deception, moved by advantage, changed by dividing and combining." (軍爭第七)
   - **Source:** 《孫子兵法》始計第一 and 軍爭第七, received text
   - **How it decides:** In: any position where your real capability is legible to the other side → Out: state the false capability deliberately and consistently enough to be acted on. He names the mechanism he is aiming at: 「攻其無備，出其不意」 — attack the unprepared, emerge from the unexpected.
   - **Label:** `quoted`

8. **Rule (plain English):** Test every plan against harm as well as benefit, before you commit — not after.
   - **Their words:** 「是故智者之慮，必雜於利害，雜於利而務可信也，雜於害而患可解也。」 — "Therefore the wise person's deliberation must be mixed with benefit and harm; mixed in with benefit, the affair can be trusted; mixed in with harm, the affliction can be dissolved." 「凡此五者，將之過也，用兵之災也。覆軍殺將，必以五危，不可不察也。」 — "These five are the general's faults, the disasters of using troops. Overrunning the army and killing the general will come of the five dangers, and one must not fail to examine them." (九變第八)
   - **Source:** 《孫子兵法》九變第八, received text. The five dangers he names: 「必死，可殺也；必生，可虜也；忿速，可侮也；廉潔，可辱也；愛民，可煩也」 — "the habit of seeking death can be used to kill him; the habit of seeking life can be used to capture him; anger and haste can be used to insult him; incorruptibility can be used to shame him; love of the people can be used to trouble him."
   - **How it decides:** In: a plan that only survives if everything goes your way → Out: write the harm column before the benefit column, and separately check your own decision style against the five dangers — each is a virtue that is a lever against you.
   - **Label:** `quoted`

9. **Rule (plain English):** Do not build your plan on the other side choosing not to attack; build on your own readiness and let their restraint be a bonus.
   - **Their words:** 「故用兵之法，無恃其不來，恃吾有以待也；無恃其不攻，恃吾有所不可攻也。」 — "Therefore the method of using troops: do not rely on their not coming; rely on your having a preparation. Do not rely on their not attacking; rely on your having a place they cannot attack." (九變第八)
   - **Source:** 《孫子兵法》九變第八, received text. Same chapter, on judgement: 「將通於九變之利者，知用兵矣」 — "a general who understands the advantage of the nine transformations knows how to use troops" — and on discretion, the explicit release of the ruler's standing orders: 「途有所不由，軍有所不擊，城有所不攻，地有所不爭，君命有所不受。」 — "There are paths not to be taken, troops not to be attacked, cities not to be assaulted, ground not to be contested, and the ruler's orders not to be obeyed."
   - **How it decides:** In: a defence or plan resting on assumptions about the opponent's restraint, fear, or good sense → Out: convert each such assumption into a preparation you own. If nothing on your side would change if they *did* move, you have rested on their restraint, not on readiness.
   - **Label:** `quoted`

10. **Rule (plain English):** Do not let anger, or wounded pride, start a war or continue one — irreversibility is the reason.
   - **Their words:** 「夫戰勝攻取，而不修其功者凶，命曰『費留』。故曰：明主慮之，良將修之，非利不動，非得不用，非危不戰。主不可以怒而興師，將不可以慍而致戰。合於利而動，不合於利而止。怒可以復喜，慍可以復悅；亡國不可以復存，死者不可以復生。」 — "To win battles and take cities and then not bring the work to completion is bad; it is called 'wasted leave.' Therefore the enlightened ruler considers it, the good general repairs it: do not move without advantage, do not act without gain, do not fight without danger. A ruler may not raise an army in anger; a general may not go to battle in resentment. Move when it accords with advantage; stop when it does not. Anger can become joy again, resentment can become pleasure again; a destroyed state cannot be restored, the dead cannot be brought back." (火攻第十二)
   - **Source:** 《孫子兵法》火攻第十二, received text. **Placement note:** in the received text I read, this passage closes 火攻第十二, not 謀攻, where it is often cited. Cite it to 火攻 unless you have checked your edition. Also note 費留 — victory gained and then squandered — as his name for the most common way a successful plan still ends badly.
   - **How it decides:** In: a proposal that is mainly the expression of a grievance, an insult, or a face → Out: the emotion is reversible, the consequences are not; therefore the burden of proof is on the party proposing. 「合於利而動，不合於利而止」 is the whole decision rule in five characters.
   - **Label:** `quoted`

## Sources used

- 《孫子兵法》 received text, all 13 chapters + the 答話 appendix — `https://zh.wikisource.org/wiki/孫子兵法` (opened in full; this is the text every Chinese quotation above is verified against, including the 「一作」 variant notes and the editorial doubts about 答話 appended at the end)
- 《史記》卷六十五 孫武孫臏吳起列傳 — `https://zh.wikisource.org/wiki/史記/卷065` (via `?action=raw`; 孫武 biography and闔廬/孫武 dialogue)
- Sun Tzu — `https://en.wikipedia.org/wiki/Sun_Tzu` (wikitext read in full; carries the cits to Gawlikowski & Loewe, Lewis, Mair)
- Yinqueshan Han Slips — `https://en.wikipedia.org/wiki/Yinqueshan_Han_Slips` (wikitext read in full; excavation date, tomb contents, the 孫子兵法（十三篇殘文；佚文五篇） inventory)
- 孫子兵法 — `https://zh.wikipedia.org/wiki/孙子兵法` (via MediaWiki API; the YQS-only lost-chapter titles 吳問, 四變, 黃帝伐赤帝, 地形二, 見吳王, 程兵, and the 銀雀山漢簡本 as earliest edition)
- 王家祥,〈從銀雀山漢簡《孫子·用間》篇看《孫子兵法》的作者與年代〉 — `https://web.archive.org/web/20131110075429/http://www.bamboosilk.org/Wssf/2002/wangjiaxiang01.htm` (GB2312 page; decoded locally. Quotes 銀雀山漢墓竹簡(壹) 上編 pp. 27–28 and 李學勤〈《孫子》篇題木牍與佚文〉, 《孫子學刊》1992年第4期)

## Gaps

**Where the received text and the 銀雀山 bamboo text differ, and where it matters here.** I could not obtain a line-by-line transcription of the bamboo 《孫子》, so most of my ten rules are quoted from the received text with no confirmation that the same wording stands in the Han bamboo copy. Two differences I *can* source, and both bite:

- **The bamboo text is much shorter, and what it contains is not always what the received text contains.** Gawlikowski & Loewe, *Early Chinese Texts* (1993), pp. 446–455, state that the Yinqueshan text is "about one-third of the chapters of the modern Art of War" and "their texts match very closely" — I read this quoted in the Wikipedia article, not in the book. Practical consequence: absence of a line from the bamboo text is *not* evidence that the line is corrupt, and I cannot certify presence for any single quote above.
- **One confirmed divergence, in 用間 — the chapter my rule 1 draws on.** The bamboo 用間 reads 「周之興也，吕牙在□〔□□□〕□＊＊師比在陉。燕之興也，苏秦在齊，唯明主賢將能……」 — the received text has only 「昔殷之興也，伊摯在夏；周之興也，呂牙在殷。」 The 銀雀山 editors' note, quoted in Wang Jiaxiang's article, records that the 十一家本 lacks 「師比在陉。燕之興也，蘇秦在齊」 and that 「蘇秦」 is anachronistic for Sun Wu. Wang Jiaxiang uses this to argue the received text is Sun Bin's work; that conclusion is a contested position, not the scholarly consensus, and I cite him only for the reading of the slips.
- **Chapter boundaries are not secure.** Per 李學勤 (as quoted by Wang Jiaxiang), the YQS 篇題木牍 (chapter-title wooden tablet) lists *more* chapter names than thirteen — including 《火陣》 and 《七勢》 — so the bamboo 《孫子》 was not limited to the received thirteen. Combined with the 答話 problem below, be careful attributing a maxim to a chapter number without saying which edition you mean.
- **The 答話 ("Questions and Answers") section is received-text-only and should not be treated as Sun Tzu speaking.** The 吳王問孫武 exchanges are absent from the 銀雀山 inventory, and the Song-edition editors themselves flag them: 「何氏引此文，亦云『兵法曰』，則知問答之詞亦在八十二篇之內也」 and, of a parallel 《孫子兵法論》 quotation, 「此亦不似孫武語」. Several of the most-quoted lines in the popular literature come from here — 「爭地之法，讓之者得，爭之者失」 and 「困而不謀者窮，窮而不戰者亡」 — so if you build a rule on either, label it `attributed`, not `quoted`. I kept them out of my ten for that reason. The bamboo text does contain Sunzi-in-dialogue pieces, 〈吳問〉 and 〈見吳王〉, but I could not obtain their contents; if you want a rule from Sun Tzu's own mouth that is *attested* in the oldest text, 〈吳問〉 is where to look next.
- **Base edition uncollated.** My Chinese base text is the zh.wikisource 宋本-based text. I did not collate it against 曹操's edition, the 十一家本, or the 銀雀山 text itself. Note the Wikisource text flags some readings itself, e.g. 「兵非貴益多也」 marked 「一作『益多』」 in 行軍, and 「勝可擅一作『為』也」 in 虛實.
- **ctext.org is unavailable to automated fetching.** It returned an anti-scraping block for every request, so I could not use its page-level collation or its 銀雀山漢墓竹簡 wiki resource (`res=526653`). A human browser would get further than I did.
- **The biography is one ancient source and a contested one.** Everything in "Who they are" about what Sun Wu did rests on 史記, composed ~100 BC. 葉世 (12th c.) observed that the 《左傳》 — far earlier and far fuller on the Battle of Boju — never mentions him, and the name孫武 appears in no text before Sima Qian. The dates544–496 BC are traditional, not documented. He is known for deciding through a text that is probably at least a century later than he was.
- **I did not use 《孫臏兵法》.** The 1972 tomb yielded both, and they are different works; if a rule fails to fit, check whether it belongs to Sun Bin instead.
