VERDICT: REPAIR

1. **Numbers — FAIL.** doc:33 overstates graph recall; doc:37 mistakes a category mean for a per-question maximum. Sources: `nodes/runtime-recall.json:93,98,103,108`; `bench/results.md:276`.
2. **Claims — FAIL.** doc:42–45 generalizes latency and treats conditional output measurements as reading savings. Source: `bench/results.md:28,98–102`.
3. **Labels — FAIL.** “My reading” and “proposed” are present (doc:41,55), but doc:15 omits material limits of the reading-cost metric. Source: `bench/results.md:28`.
4. **Routing table — FAIL.** doc:62–64 implies more coverage or stronger route preferences than its evidence establishes. Sources: `nodes/runtime-recall.json:93,98`; `bench/results.md:200–214,73–75,85–87`.
5. **Vision — PASS.** doc:73–78 preserves existing rules, identifies the proposed scope conflict, and leaves changes to EJ. Source: `docs/memory-system/vision-statements/caches-memory-vision-statements.md:15–20,28–34`.

Findings:

- **High — doc:33: graph recall is 0.78, not 0.92.** The four source recalls are 0.33, 0.8, 1.0 and 1.0; their mean is 0.7825, rounded to **0.78**. Source: `nodes/runtime-recall.json:93,98,103,108`. The stated 0.92 makes graph-based test selection appear substantially more complete.

- **High — doc:15,19,29–30,43–45,69–70: the metric stops at a correct file, not a correct answer.** It excludes misses, averages different successful question subsets, and depends on unequal output formats. Source: `bench/results.md:28`; grep’s mean includes 26 answers, full-text’s 25, graph’s 13 (`bench/results.md:98–102`). For A05, full-text reaches the gold file after 84 characters while missing the required symbol in its top five (`bench/results.md:129`; `bench/results.json:1041–1068`). These measurements support claims about printed output to a gold file; they do not establish the reading required to answer correctly or an end-to-end sixfold saving.

- **Medium — doc:37,42: the latency bound and universal conclusion overreach.** E04 grep takes **14.68 ms**, exceeding 11 ms (`bench/results.md:276`). The 10.7 ms figure is the category mean (`bench/results.md:84`). One repository does not establish that speed is “never” a reason to use a cache.

- **Medium — doc:52–53,62: graph plus full-text remains an incomplete test-selection heuristic.** Both routes miss C05 entirely (`bench/results.md:200–204`), although its verified test is `code_graph/tests/test_code_graph.py` (`queries.json:407–412`; `nodes/gold-verdicts.json:123–126`). Graph also recalls only 0.33 and 0.8 for C01 and C02 (`nodes/runtime-recall.json:93,98`). State that the selected subset can omit affected tests even after combining the routes; the full-suite step mitigates this before committing.

- **Low — doc:63: BM-4 supports a tie, not a unique full-text preference.** Full-text and hybrid both score 0.625; hybrid’s reported characters-to-gold mean is 516.4 versus full-text’s 525.2 (`bench/results.md:73,75`). Full-text does print less total output, so retaining it as the default is defensible, but the row should identify that tradeoff instead of implying BM-4 establishes an unqualified winner.

- **Medium — doc:48,64: BM-5 does not establish “full-text first.”** Full-text scores 0.3333 at symbol hit@5; hybrid and vector score 0.5 (`bench/results.md:85–87,90`). The sequential fallback was not measured, and doc:48 itself says the six-question sample is too small to act on. Present this ordering as a policy proposal requiring further evidence, rather than a preference demonstrated by BM-5.
