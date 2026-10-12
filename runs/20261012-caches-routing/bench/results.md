# Cache benchmark results

- question set: `queries.json` (40 questions)
- corpus: 490 files (123 `.py`, 367 `.md`), 4021 chunks
- git HEAD at build: `41ebd42f484708851de72d8bfe7e2ae2df13d655`
- read budget: at most 10 paths per answer, 300 characters per printed line, rg output capped at 40 lines
- a route may read: question, terms, symbol, file; `gold` is read by run_bench.py only, after the answer

## Build (full rebuild, no prior store)

| store | seconds | bytes | what it was built from |
|---|---:|---:|---|
| fts | 0.169 | 9,457,664 | git `41ebd42`, newest source mtime 1791785790.0215247 |
| vec | 0.936 | 10,215,424 | git `41ebd42`, newest source mtime 1791785790.0215247 |
| graph | 0.892 | 4,902,912 | git `41ebd42`, newest source mtime 1791785790.0215247 |

## Determinism check

Deleted `bench/.cache/`, rebuilt in 1.882s, answered every question again and compared `paths`.

- answers compared: 180
- identical: **True**

## By category

`file hit@5` counts a gold `path::name` as hit when the route returns its file. `symbol hit@5` needs the symbol itself: an entry naming it, the top-level def/class holding it or a method of it, a module-code chunk for a module-level name, and for `rg` a printed match line inside the symbol's lines. A gold given as a plain file scores the same on both. **The best route is chosen on symbol hit@5.**

`chars` is the mean number of characters of output read up to and including the first line where the route names a gold file as its answer (`# <path> (`, or a line starting `<path>:`), over the answers that named one; `n` is how many did. A miss is left out, never scored 0. What each route prints differs -- rg: a `# path (N matching lines)` header per file plus at most 40 match lines of up to 300 characters; fts: one 24-token snippet per path; vec: the first 300 characters per path; hybrid: the vec or fts block per path; graph: one id per line -- so `chars` measures the print format as much as the store.

### Category A -- exact identifier (8 questions)

| route | symbol hit@5 | file hit@5 | chars to first gold (n) | mean output chars | mean seconds |
|---|---:|---:|---:|---:|---:|
| rg | 0.75 | 0.75 | 919.5714 (7) | 2016.25 | 0.0074 |
| fts | 0.625 | 0.75 | 355.7143 (7) | 1477.25 | 0.0009 |
| vec | 0.0 | 0.5 | 837.0 (5) | 2997.0 | 0.0018 |
| hybrid | 0.5 | 0.75 | 91.3333 (6) | 2804.625 | 0.0025 |
| graph | 0.75 | 0.75 | 43.1667 (6) | 92.5 | 0.0005 |

Best on symbol hit@5: rg, graph (0.75) -- a tie

### Category B -- concept in other words (8 questions)

| route | symbol hit@5 | file hit@5 | chars to first gold (n) | mean output chars | mean seconds |
|---|---:|---:|---:|---:|---:|
| rg | 0.0 | 0.0 | -- (0) | 3827.0 | 0.0071 |
| fts | 0.0 | 0.0 | -- (0) | 1646.75 | 0.0011 |
| vec | 0.0 | 0.25 | 954.5 (2) | 2977.0 | 0.0017 |
| hybrid | 0.0 | 0.125 | 1426.5 (2) | 2847.25 | 0.0026 |
| graph | -- | -- | -- | -- | -- |

Best on symbol hit@5: none -- no route hits a gold symbol in the first 5

### Category C -- structure and test impact (10 questions)

| route | symbol hit@5 | file hit@5 | chars to first gold (n) | mean output chars | mean seconds |
|---|---:|---:|---:|---:|---:|
| rg | 0.8 | 0.8 | 1015.4444 (9) | 2960.8 | 0.0073 |
| fts | 0.9 | 0.9 | 174.5556 (9) | 1501.5 | 0.0011 |
| vec | 0.1 | 0.2 | 1421.0 (4) | 2814.0 | 0.0017 |
| hybrid | 0.9 | 0.9 | 362.0 (9) | 2711.9 | 0.0026 |
| graph | 0.7 | 0.7 | 61.1429 (7) | 217.6 | 0.0003 |

Best on symbol hit@5: fts, hybrid (0.9) -- a tie

Category C also reports recall@10: rg 0.85, fts 0.9, vec 0.4, hybrid 0.85, graph 0.7

### Category D -- decision or reason in the docs (8 questions)

| route | symbol hit@5 | file hit@5 | chars to first gold (n) | mean output chars | mean seconds |
|---|---:|---:|---:|---:|---:|
| rg | 0.625 | 0.625 | 4470.1667 (6) | 6192.5 | 0.0089 |
| fts | 0.625 | 0.625 | 525.2 (5) | 2354.125 | 0.0051 |
| vec | 0.5 | 0.5 | 810.0 (5) | 3140.0 | 0.0018 |
| hybrid | 0.625 | 0.625 | 516.4 (5) | 3116.875 | 0.0066 |
| graph | 0.0 | 0.0 | -- (0) | 38.0 | 0.0005 |

Best on symbol hit@5: rg, fts, hybrid (0.625) -- a tie

### Category E -- how to run or configure (6 questions)

| route | symbol hit@5 | file hit@5 | chars to first gold (n) | mean output chars | mean seconds |
|---|---:|---:|---:|---:|---:|
| rg | 0.1667 | 0.5 | 6874.75 (4) | 7709.1667 | 0.0107 |
| fts | 0.3333 | 0.3333 | 1146.0 (4) | 2305.0 | 0.0074 |
| vec | 0.5 | 0.5 | 569.0 (3) | 3325.5 | 0.0018 |
| hybrid | 0.5 | 0.5 | 1120.0 (4) | 3026.8333 | 0.0091 |
| graph | -- | -- | -- | -- | -- |

Best on symbol hit@5: vec, hybrid (0.5) -- a tie

## Every category, one row per route

The routes do not answer the same number of questions: `graph` applies only where the question names a symbol or a file, so its row is over fewer questions. The `questions` column is the denominator.

| route | questions | symbol hit@1 / @5 / @10 | file hit@1 / @5 / @10 | chars to first gold (n) | mean output chars | mean seconds |
|---|---:|---:|---:|---:|---:|---:|
| rg | 40 | 0.275 / 0.5 / 0.6 | 0.275 / 0.55 / 0.65 | 2688.3077 (26) | 4303.725 | 0.0081 |
| fts | 40 | 0.2 / 0.525 / 0.625 | 0.35 / 0.55 / 0.625 | 450.84 (25) | 1816.75 | 0.0028 |
| vec | 40 | 0.025 / 0.2 / 0.3 | 0.075 / 0.375 / 0.475 | 922.8947 (19) | 3025.125 | 0.0018 |
| hybrid | 40 | 0.2 / 0.525 / 0.575 | 0.375 / 0.6 / 0.65 | 527.7308 (26) | 2885.75 | 0.0044 |
| graph | 20 | 0.65 / 0.65 / 0.65 | 0.65 / 0.65 / 0.65 | 52.8462 (13) | 149.6 | 0.0004 |

## Per question

| id | category | route | symbol hit@10 | file hit@10 | recall@10 | chars to first gold | output chars | seconds |
|---|---|---|---:|---:|---:|---:|---:|---:|
| A01 | A | rg | 1 | 1 | -- | 2415 | 4017 | 0.007871 |
| A01 | A | fts | 1 | 1 | -- | 1608 | 2331 | 0.001013 |
| A01 | A | vec | 0 | 0 | -- | -- | 3226 | 0.00197 |
| A01 | A | hybrid | 0 | 0 | -- | -- | 3071 | 0.002593 |
| A01 | A | graph | 1 | 1 | -- | 38 | 38 | 0.000395 |
| A02 | A | rg | 0 | 0 | -- | -- | 5235 | 0.007111 |
| A02 | A | fts | 0 | 0 | -- | -- | 2369 | 0.002504 |
| A02 | A | vec | 1 | 1 | -- | 2202 | 2622 | 0.001813 |
| A02 | A | hybrid | 0 | 0 | -- | -- | 2762 | 0.004194 |
| A02 | A | graph | 1 | 1 | -- | 48 | 48 | 0.000498 |
| A03 | A | rg | 1 | 1 | -- | 44 | 704 | 0.006906 |
| A03 | A | fts | 1 | 1 | -- | 97 | 1264 | 0.000562 |
| A03 | A | vec | 0 | 1 | -- | 1349 | 3233 | 0.001932 |
| A03 | A | hybrid | 1 | 1 | -- | 85 | 2591 | 0.002243 |
| A03 | A | graph | 0 | 0 | -- | -- | 0 | 0.000569 |
| A04 | A | rg | 1 | 1 | -- | 46 | 187 | 0.006867 |
| A04 | A | fts | 1 | 1 | -- | 84 | 449 | 0.000652 |
| A04 | A | vec | 0 | 1 | -- | 249 | 1295 | 0.001787 |
| A04 | A | hybrid | 1 | 1 | -- | 57 | 1534 | 0.00224 |
| A04 | A | graph | 1 | 1 | -- | 49 | 530 | 0.000596 |
| A05 | A | rg | 1 | 1 | -- | 3318 | 3722 | 0.007344 |
| A05 | A | fts | 1 | 1 | -- | 84 | 2242 | 0.000993 |
| A05 | A | vec | 0 | 0 | -- | -- | 3301 | 0.001878 |
| A05 | A | hybrid | 0 | 1 | -- | 84 | 2769 | 0.002375 |
| A05 | A | graph | 0 | 0 | -- | -- | 0 | 0.000749 |
| A06 | A | rg | 1 | 1 | -- | 54 | 873 | 0.00688 |
| A06 | A | fts | 1 | 1 | -- | 408 | 1135 | 0.00064 |
| A06 | A | vec | 1 | 1 | -- | 102 | 3142 | 0.001798 |
| A06 | A | hybrid | 1 | 1 | -- | 154 | 3352 | 0.002166 |
| A06 | A | graph | 1 | 1 | -- | 44 | 44 | 0.000409 |
| A07 | A | rg | 1 | 1 | -- | 44 | 362 | 0.007833 |
| A07 | A | fts | 1 | 1 | -- | 94 | 447 | 0.000511 |
| A07 | A | vec | 0 | 1 | -- | 283 | 3428 | 0.001778 |
| A07 | A | hybrid | 1 | 1 | -- | 53 | 3291 | 0.002007 |
| A07 | A | graph | 1 | 1 | -- | 34 | 34 | 0.000438 |
| A08 | A | rg | 1 | 1 | -- | 516 | 1030 | 0.00807 |
| A08 | A | fts | 1 | 1 | -- | 115 | 1581 | 0.000682 |
| A08 | A | vec | 0 | 0 | -- | -- | 3729 | 0.001756 |
| A08 | A | hybrid | 1 | 1 | -- | 115 | 3067 | 0.002287 |
| A08 | A | graph | 1 | 1 | -- | 46 | 46 | 0.000397 |
| B01 | B | rg | 0 | 0 | -- | -- | 6945 | 0.007297 |
| B01 | B | fts | 0 | 0 | -- | -- | 2420 | 0.002011 |
| B01 | B | vec | 0 | 0 | -- | -- | 3329 | 0.001746 |
| B01 | B | hybrid | 0 | 0 | -- | -- | 2986 | 0.003549 |
| B02 | B | rg | 0 | 0 | -- | -- | 4184 | 0.007803 |
| B02 | B | fts | 0 | 0 | -- | -- | 861 | 0.000665 |
| B02 | B | vec | 0 | 0 | -- | -- | 3071 | 0.001583 |
| B02 | B | hybrid | 0 | 0 | -- | -- | 2981 | 0.002048 |
| B03 | B | rg | 0 | 0 | -- | -- | 3938 | 0.006816 |
| B03 | B | fts | 0 | 0 | -- | -- | 1889 | 0.001616 |
| B03 | B | vec | 0 | 0 | -- | -- | 2717 | 0.001619 |
| B03 | B | hybrid | 0 | 0 | -- | -- | 2170 | 0.002973 |
| B04 | B | rg | 0 | 0 | -- | -- | 2921 | 0.006698 |
| B04 | B | fts | 0 | 0 | -- | -- | 2451 | 0.000957 |
| B04 | B | vec | 0 | 0 | -- | -- | 2492 | 0.001589 |
| B04 | B | hybrid | 0 | 0 | -- | -- | 2445 | 0.002547 |
| B05 | B | rg | 0 | 0 | -- | -- | 2584 | 0.006611 |
| B05 | B | fts | 0 | 0 | -- | -- | 923 | 0.000717 |
| B05 | B | vec | 0 | 1 | -- | 454 | 3026 | 0.001714 |
| B05 | B | hybrid | 0 | 1 | -- | 947 | 3048 | 0.002265 |
| B06 | B | rg | 0 | 0 | -- | -- | 3628 | 0.006759 |
| B06 | B | fts | 0 | 0 | -- | -- | 2175 | 0.001025 |
| B06 | B | vec | 0 | 0 | -- | -- | 3690 | 0.00178 |
| B06 | B | hybrid | 0 | 0 | -- | -- | 3087 | 0.002486 |
| B07 | B | rg | 0 | 0 | -- | -- | 5224 | 0.007011 |
| B07 | B | fts | 0 | 0 | -- | -- | 2005 | 0.001409 |
| B07 | B | vec | 0 | 0 | -- | -- | 2392 | 0.001671 |
| B07 | B | hybrid | 0 | 0 | -- | -- | 2841 | 0.002951 |
| B08 | B | rg | 0 | 0 | -- | -- | 1192 | 0.007713 |
| B08 | B | fts | 0 | 0 | -- | -- | 450 | 0.000542 |
| B08 | B | vec | 0 | 1 | -- | 1455 | 3099 | 0.001647 |
| B08 | B | hybrid | 0 | 1 | -- | 1906 | 3220 | 0.002172 |
| C01 | C | rg | 1 | 1 | 1.0 | 52 | 3900 | 0.007766 |
| C01 | C | fts | 1 | 1 | 1.0 | 153 | 2276 | 0.0009 |
| C01 | C | vec | 0 | 0 | 0.0 | -- | 3576 | 0.001695 |
| C01 | C | hybrid | 1 | 1 | 1.0 | 153 | 3013 | 0.002356 |
| C01 | C | graph | 1 | 1 | 1.0 | 79 | 957 | 0.000335 |
| C02 | C | rg | 1 | 1 | 1.0 | 51 | 723 | 0.006767 |
| C02 | C | fts | 1 | 1 | 1.0 | 93 | 1237 | 0.000493 |
| C02 | C | vec | 0 | 0 | 0.0 | -- | 3288 | 0.001636 |
| C02 | C | hybrid | 1 | 1 | 1.0 | 93 | 2918 | 0.001909 |
| C02 | C | graph | 1 | 1 | 1.0 | 101 | 830 | 0.000322 |
| C03 | C | rg | 1 | 1 | 1.0 | 42 | 515 | 0.007549 |
| C03 | C | fts | 1 | 1 | 1.0 | 348 | 1195 | 0.000577 |
| C03 | C | vec | 0 | 0 | 0.0 | -- | 3142 | 0.001652 |
| C03 | C | hybrid | 1 | 1 | 1.0 | 1391 | 3174 | 0.002217 |
| C03 | C | graph | 1 | 1 | 1.0 | 88 | 162 | 0.000308 |
| C04 | C | rg | 1 | 1 | 1.0 | 42 | 4450 | 0.007518 |
| C04 | C | fts | 1 | 1 | 1.0 | 381 | 2015 | 0.002443 |
| C04 | C | vec | 0 | 0 | 0.0 | -- | 3201 | 0.0016 |
| C04 | C | hybrid | 1 | 1 | 1.0 | 711 | 2719 | 0.003953 |
| C04 | C | graph | 1 | 1 | 1.0 | 45 | 112 | 0.000284 |
| C05 | C | rg | 0 | 0 | 0.0 | -- | 8744 | 0.007786 |
| C05 | C | fts | 0 | 0 | 0.0 | -- | 1632 | 0.001409 |
| C05 | C | vec | 0 | 0 | 0.0 | -- | 1080 | 0.001653 |
| C05 | C | hybrid | 0 | 0 | 0.0 | -- | 1611 | 0.002945 |
| C05 | C | graph | 0 | 0 | 0.0 | -- | 0 | 0.000438 |
| C06 | C | rg | 1 | 1 | 1.0 | 364 | 777 | 0.006731 |
| C06 | C | fts | 1 | 1 | 1.0 | 97 | 870 | 0.000598 |
| C06 | C | vec | 1 | 1 | 1.0 | 2469 | 3078 | 0.001681 |
| C06 | C | hybrid | 1 | 1 | 1.0 | 433 | 2827 | 0.002126 |
| C06 | C | graph | 0 | 0 | 0.0 | -- | 0 | 0.000293 |
| C07 | C | rg | 1 | 1 | 0.5 | 8451 | 8602 | 0.007223 |
| C07 | C | fts | 1 | 1 | 1.0 | 140 | 2091 | 0.002588 |
| C07 | C | vec | 0 | 0 | 0.0 | -- | 1880 | 0.001803 |
| C07 | C | hybrid | 1 | 1 | 0.5 | 140 | 2187 | 0.004106 |
| C07 | C | graph | 0 | 0 | 0.0 | -- | 0 | 0.000318 |
| C08 | C | rg | 1 | 1 | 1.0 | 46 | 186 | 0.006841 |
| C08 | C | fts | 1 | 1 | 1.0 | 87 | 369 | 0.000512 |
| C08 | C | vec | 1 | 1 | 1.0 | 80 | 2983 | 0.001893 |
| C08 | C | hybrid | 1 | 1 | 1.0 | 80 | 2983 | 0.00217 |
| C08 | C | graph | 1 | 1 | 1.0 | 46 | 46 | 0.000412 |
| C09 | C | rg | 1 | 1 | 1.0 | 47 | 1508 | 0.006952 |
| C09 | C | fts | 1 | 1 | 1.0 | 148 | 2209 | 0.000824 |
| C09 | C | vec | 0 | 1 | 1.0 | 843 | 3389 | 0.001749 |
| C09 | C | hybrid | 1 | 1 | 1.0 | 140 | 2972 | 0.002347 |
| C09 | C | graph | 1 | 1 | 1.0 | 33 | 33 | 0.000335 |
| C10 | C | rg | 1 | 1 | 1.0 | 44 | 203 | 0.007767 |
| C10 | C | fts | 1 | 1 | 1.0 | 124 | 1121 | 0.000555 |
| C10 | C | vec | 0 | 1 | 1.0 | 2292 | 2523 | 0.001745 |
| C10 | C | hybrid | 1 | 1 | 1.0 | 117 | 2715 | 0.002105 |
| C10 | C | graph | 1 | 1 | 1.0 | 36 | 36 | 0.00031 |
| D01 | D | rg | 1 | 1 | -- | 5704 | 6005 | 0.0082 |
| D01 | D | fts | 1 | 1 | -- | 106 | 2366 | 0.005738 |
| D01 | D | vec | 1 | 1 | -- | 2116 | 2869 | 0.001878 |
| D01 | D | hybrid | 1 | 1 | -- | 822 | 3007 | 0.007765 |
| D02 | D | rg | 1 | 1 | -- | 3900 | 4257 | 0.009373 |
| D02 | D | fts | 1 | 1 | -- | 1121 | 2680 | 0.004074 |
| D02 | D | vec | 1 | 1 | -- | 98 | 2674 | 0.001726 |
| D02 | D | hybrid | 1 | 1 | -- | 98 | 3257 | 0.005652 |
| D02 | D | graph | 0 | 0 | -- | -- | 0 | 0.000649 |
| D03 | D | rg | 0 | 0 | -- | -- | 5247 | 0.008112 |
| D03 | D | fts | 0 | 0 | -- | -- | 2202 | 0.001585 |
| D03 | D | vec | 0 | 0 | -- | -- | 3223 | 0.001605 |
| D03 | D | hybrid | 0 | 0 | -- | -- | 2942 | 0.003264 |
| D04 | D | rg | 0 | 0 | -- | -- | 10980 | 0.011394 |
| D04 | D | fts | 0 | 0 | -- | -- | 2394 | 0.0082 |
| D04 | D | vec | 0 | 0 | -- | -- | 2851 | 0.00181 |
| D04 | D | hybrid | 0 | 0 | -- | -- | 3147 | 0.0094 |
| D05 | D | rg | 1 | 1 | -- | 2610 | 6278 | 0.00687 |
| D05 | D | fts | 0 | 0 | -- | -- | 2248 | 0.001572 |
| D05 | D | vec | 0 | 0 | -- | -- | 3620 | 0.001732 |
| D05 | D | hybrid | 0 | 0 | -- | -- | 2959 | 0.003034 |
| D05 | D | graph | 0 | 0 | -- | -- | 76 | 0.000358 |
| D06 | D | rg | 1 | 1 | -- | 4328 | 4518 | 0.010191 |
| D06 | D | fts | 1 | 1 | -- | 271 | 2225 | 0.00852 |
| D06 | D | vec | 1 | 1 | -- | 979 | 3433 | 0.001839 |
| D06 | D | hybrid | 1 | 1 | -- | 760 | 2986 | 0.009614 |
| D07 | D | rg | 1 | 1 | -- | 5328 | 6904 | 0.009115 |
| D07 | D | fts | 1 | 1 | -- | 1032 | 2338 | 0.006953 |
| D07 | D | vec | 1 | 1 | -- | 420 | 3668 | 0.001722 |
| D07 | D | hybrid | 1 | 1 | -- | 820 | 3442 | 0.008405 |
| D08 | D | rg | 1 | 1 | -- | 4951 | 5351 | 0.007669 |
| D08 | D | fts | 1 | 1 | -- | 96 | 2380 | 0.004412 |
| D08 | D | vec | 1 | 1 | -- | 437 | 2782 | 0.001691 |
| D08 | D | hybrid | 1 | 1 | -- | 82 | 3195 | 0.005915 |
| E01 | E | rg | 0 | 0 | -- | -- | 8203 | 0.008635 |
| E01 | E | fts | 1 | 1 | -- | 1588 | 2500 | 0.005576 |
| E01 | E | vec | 0 | 0 | -- | -- | 3716 | 0.001722 |
| E01 | E | hybrid | 0 | 0 | -- | -- | 3158 | 0.007295 |
| E02 | E | rg | 0 | 0 | -- | -- | 7674 | 0.013762 |
| E02 | E | fts | 0 | 0 | -- | -- | 2303 | 0.010022 |
| E02 | E | vec | 0 | 0 | -- | -- | 3406 | 0.001884 |
| E02 | E | hybrid | 0 | 0 | -- | -- | 2948 | 0.011486 |
| E03 | E | rg | 0 | 1 | -- | 4845 | 5235 | 0.007678 |
| E03 | E | fts | 1 | 1 | -- | 963 | 2523 | 0.005474 |
| E03 | E | vec | 1 | 1 | -- | 519 | 3512 | 0.001833 |
| E03 | E | hybrid | 1 | 1 | -- | 133 | 3415 | 0.006641 |
| E04 | E | rg | 0 | 1 | -- | 6965 | 7482 | 0.01468 |
| E04 | E | fts | 1 | 1 | -- | 1280 | 2331 | 0.010171 |
| E04 | E | vec | 0 | 0 | -- | -- | 2674 | 0.001839 |
| E04 | E | hybrid | 1 | 1 | -- | 2831 | 3005 | 0.011602 |
| E05 | E | rg | 1 | 1 | -- | 7499 | 9471 | 0.008913 |
| E05 | E | fts | 1 | 1 | -- | 753 | 2164 | 0.00486 |
| E05 | E | vec | 1 | 1 | -- | 760 | 3128 | 0.001883 |
| E05 | E | hybrid | 1 | 1 | -- | 425 | 2904 | 0.006607 |
| E06 | E | rg | 1 | 1 | -- | 8190 | 8190 | 0.010546 |
| E06 | E | fts | 0 | 0 | -- | -- | 2009 | 0.008367 |
| E06 | E | vec | 1 | 1 | -- | 428 | 3517 | 0.001926 |
| E06 | E | hybrid | 1 | 1 | -- | 1091 | 2731 | 0.010743 |

20 route/question pairs were not applicable (the graph route needs a symbol or a file).

