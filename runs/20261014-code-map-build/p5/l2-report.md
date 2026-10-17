# L2 — the map against reading, round 1

## Setup

- **Tool:** the code-map tool as it stood when A5 closed, frozen in `p4/tool-a5-src/`.
- **Questions:** three opencode modules, ten fixed questions each. The questions came from the P1 answer keys,
  without the answers.
- **Arms:** two arms on the same model (claude-sonnet-5-5, `claude -p`), in a fresh session each.
  - The **map** arm may run the tool (`Bash(bun:*)`) and also read and grep.
  - The **reading** arm may only Read, Grep and Glob.
- **Scoring:** a blind Claude opus judge per module scored both sets against the key: correct, missed and wrong. It
  checked every claim beyond the key against the code. The labels were drawn at random and unblinded after all
  three scores were in (`blind-map.json`). The draw happened to put the map arm as A in all three modules.

## Results

| Module | Arm | Correct | Missed | Wrong | Wall time | Tokens, total | New input | Cache read | Output | Cost (USD) |
|---|---|---|---|---|---|---|---|---|---|---|
| session | map | 55 | 6 | 0 | 421 s | 1,716,730 | 100,782 | 1,590,559 | 25,389 | 0.82 |
| session | reading | 57 | 4 | 2 | 186 s | 1,515,010 | 99,953 | 1,397,056 | 18,001 | 0.72 |
| tool + permission | map | 56 | 8 | 0 | 443 s | 1,827,982 | 92,084 | 1,714,576 | 21,322 | 0.75 |
| tool + permission | reading | 57 | 7 | 0 | 161 s | 1,477,324 | 91,336 | 1,366,114 | 19,874 | 0.70 |
| ai | map | 55 | 8 | 1 | 236 s | 1,838,722 | 101,296 | 1,715,808 | 21,618 | 0.79 |
| ai | reading | 58 | 5 | 0 | 152 s | 2,525,226 | 133,834 | 2,371,263 | 20,129 | 0.97 |
| **All** | **map** | **166** | **22** | **1** | **1,100 s** | **5,383,434** | **294,162** | | **68,329** | **2.36** |
| **All** | **reading** | **172** | **16** | **2** | **499 s** | **5,517,560** | **325,123** | | **58,004** | **2.39** |

- **Build cost:** the tool builds the type program on every call: about 10 s and 2.7 GB for core, and 4 s and
  0.9 GB for ai (`p4/`). It has no cache, so that cost is inside the map arm's wall time and is paid again on every
  call.
- **Map size** (P4, JSON): 1.83 MB for session against 431 KB of source, 852 KB for tool + permission against
  199 KB, and 3.91 MB for ai against 1.24 MB. A whole map is larger than reading the whole module. The map arm used
  one-question commands, not whole maps.

## What it shows (my reading)

- **Correctness:** the map was not better. It got 6 fewer correct claims (166 against 172) and 6 more misses (22
  against 16). It had 1 wrong claim where reading had 2. Most misses on both sides were line-number or detail misses,
  not wrong answers.
- **Tokens:** about equal in total (−2.4% for the map). The map used 10% less new input, and its output was 18%
  higher. The only module where the map saved tokens was ai (−27%), the largest module.
- **Time:** the map was 2.2 times slower, mostly because of the per-call program build.
- **Worse result, stated plainly:** on these thirty questions, with this version of the tool, reading did as well
  or better on correctness and time, at about the same tokens.

## What it does not establish

- n = 1 run per arm per module, one model and one target. The questions were written for answer keys made by
  reading, which may favour reading.
- The tool is the A5 version. A2's shortest-route fix and later rounds are not in it.
- The judge's 3-line rule decides some misses. The same rule was applied to both arms.

## For the next round (P5 rounds 2–3, if time)

1. Keep the type program between calls: a cache, or one process for several questions. This is the main cost by
   time.
2. Look at the ai module, where the map saved tokens, against the two smaller modules, where it did not.
