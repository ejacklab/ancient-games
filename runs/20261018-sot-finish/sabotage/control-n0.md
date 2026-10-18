| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| M01 | B1.2 untracked entry gets a line | killed | 1 failed, 3 passed in 0.22s | killed |
| M02 | B1.1 file outside B1.1 gets a line (subfolder) | killed | 1 failed in 0.08s | killed |
| M03 | B1.1 file outside B1.1 gets a line (prefix) | INVALID (old occurs 0x) |  |  |
| M04 | B1.3 non-ASCII path read wrongly in check mode | killed | 1 failed, 3 passed in 0.23s | survived |
| M05 | B1.3 check mode reads the working tree, not git objects | killed | 1 failed, 8 passed in 0.48s | survived |
| M06 | B2.4 malformed active entry gets a line | killed | 1 failed, 29 passed in 1.62s | killed |
| M07 | B2.4 prefix/kind mismatch passes | killed | 1 failed, 35 passed in 1.91s | killed |
| M08 | B2.3/G4.2 duplicate id passes | killed | 1 failed, 147 passed in 7.46s | killed |
| M09 | B2.5 broken retired entry stops the build | killed | 1 failed, 156 passed in 7.86s | killed |
| M10 | B2.6 bad UTF-8 ends in a traceback | killed | 1 failed, 178 passed in 8.99s | killed |
| M11 | B2.1 quotes not stripped | killed | 1 failed, 12 passed in 0.77s | killed |
| M12 | B2.2 whitespace not collapsed | killed | 1 failed, 13 passed in 0.83s | killed |
| M13 | B2.2 claim not cut at **Why:** | killed | 1 failed in 0.08s | killed |
| M14 | B3.3 locale/case order instead of code points | killed | 1 failed, 362 passed in 18.11s | survived |
| M15 | B3.1 superseded entry gets a line | killed | 1 failed, 49 passed in 2.62s | killed |
| M16 | B3.1 link not percent-encoded | killed | 1 failed, 10 passed in 0.62s | killed |
| M17 | B3.3 CRLF kept | killed | 1 failed, 367 passed in 18.20s | killed |
| M18 | B3.2 wrong fixed head | killed | 1 failed in 0.08s | killed |
| M19 | B3.4 identical file rewritten | killed | 1 failed, 369 passed in 18.20s | killed |
| M20 | B4.3 line dropped to fit | killed | 1 failed, 373 passed in 18.48s | survived |
| M21 | B4.3 --check passes over the limit | killed | 1 failed, 375 passed in 18.64s | survived |
| M22 | B4.1 bytes not measured against MAX_BYTES | killed | 1 failed, 376 passed in 18.89s | survived |
| M23 | B4.3 write mode exits non-zero over the limit | killed | 1 failed, 373 passed in 18.54s | killed |
| M24 | B4.2 size line wrong | killed | 1 failed, 370 passed in 18.27s | killed |
| M25 | C1.2 hand edit / stale index passes | killed | 1 failed, 379 passed in 19.08s | survived |
| M26 | C1.2 no diff printed | killed | 1 failed, 379 passed in 19.05s | survived |
| M27 | C1.2 bad rev passes | SURVIVED | 408 passed in 20.51s | killed |
| M28 | C1.3 no project-memory fails | killed | 1 failed, 390 passed in 19.57s | survived |
| M29 | C1.4 check mode changes a file | killed | 1 failed, 1 passed in 0.13s | survived |
| M30 | C1.3 unborn HEAD fails | killed | 1 failed, 392 passed in 19.77s | survived |
| M31 | G2.1 change to the script alone skips the check | killed | 1 failed, 401 passed in 20.21s | survived |
| M32 | G2.1 hook lets a wrong INDEX.md through | killed | 1 failed, 398 passed in 20.84s | survived |
| N01 | B2.3 trailing junk passes (start-only match) | killed | 1 failed, 102 passed in 5.41s | killed |
| N02 | B2.3 non-ASCII digit passes (\d) | killed | 1 failed, 111 passed in 5.89s | killed |
| N03 | B2.1/B2.3 form checked on the raw value, before quotes and spaces are stripped | killed | 1 failed in 0.09s | killed |
| N04 | B2.3 id form checked in active entries only | killed | 1 failed, 67 passed in 3.60s | killed |
| N05 | B2.7 markers checked in active entries only | killed | 1 failed, 182 passed in 9.61s | killed |
| N06 | B2.7 markers in the header not checked | killed | 1 failed, 181 passed in 9.46s | killed |
| N07 | B2.7 >>>>>>> not a marker | killed | 1 failed, 208 passed in 10.84s | killed |
| N08 | B2.7 ======= treated as a marker | killed | 1 failed, 235 passed in 12.34s | killed |
| N09 | B2.7 an indented marker counts (not 'starts with') | killed | 1 failed, 253 passed in 13.07s | killed |
| N10 | B2.3 no id-form check at all | killed | 1 failed, 66 passed in 3.58s | killed |
| N11 | B2.3 upper case passes | killed | 1 failed, 93 passed in 4.97s | killed |
| N12 | B2.3 five random characters pass | killed | 1 failed, 84 passed in 4.43s | killed |
| N13 | B2.7 a marker is only a warning | killed | 1 failed, 181 passed in 9.10s | killed |
| N14 | B2.7 only the first marker line is reported (DESIGN step 5: report them all) | SURVIVED | 408 passed in 20.64s | killed |

43/46 killed; originals restored (2 file(s))
