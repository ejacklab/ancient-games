| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| M01 | B1.2 untracked entry gets a line | killed | 1 failed, 3 passed in 0.23s | killed |
| M02 | B1.1 file outside B1.1 gets a line (subfolder) | killed | 1 failed in 0.09s | killed |
| M03 | B1.1 file outside B1.1 gets a line (prefix) | INVALID (old occurs 0x) |  |  |
| M04 | B1.3 non-ASCII path read wrongly in check mode | killed | 1 failed, 3 passed in 0.23s | survived |
| M05 | B1.3 check mode reads the working tree, not git objects | killed | 1 failed, 8 passed in 0.47s | survived |
| M06 | B2.4 malformed active entry gets a line | killed | 1 failed, 29 passed in 1.70s | killed |
| M07 | B2.4 prefix/kind mismatch passes | killed | 1 failed, 35 passed in 1.97s | killed |
| M08 | B2.3/G4.2 duplicate id passes | killed | 1 failed, 147 passed in 7.65s | killed |
| M09 | B2.5 broken retired entry stops the build | killed | 1 failed, 156 passed in 8.02s | killed |
| M10 | B2.6 bad UTF-8 ends in a traceback | killed | 1 failed, 178 passed in 9.11s | killed |
| M11 | B2.1 quotes not stripped | killed | 1 failed, 12 passed in 0.79s | killed |
| M12 | B2.2 whitespace not collapsed | killed | 1 failed, 13 passed in 0.84s | killed |
| M13 | B2.2 claim not cut at **Why:** | killed | 1 failed in 0.09s | killed |
| M14 | B3.3 locale/case order instead of code points | killed | 1 failed, 362 passed in 18.48s | survived |
| M15 | B3.1 superseded entry gets a line | killed | 1 failed, 49 passed in 2.64s | killed |
| M16 | B3.1 link not percent-encoded | killed | 1 failed, 10 passed in 0.64s | killed |
| M17 | B3.3 CRLF kept | killed | 1 failed, 367 passed in 18.51s | killed |
| M18 | B3.2 wrong fixed head | killed | 1 failed in 0.08s | killed |
| M19 | B3.4 identical file rewritten | killed | 1 failed, 369 passed in 18.57s | killed |
| M20 | B4.3 line dropped to fit | killed | 1 failed, 373 passed in 18.94s | survived |
| M21 | B4.3 --check passes over the limit | killed | 1 failed, 375 passed in 19.27s | survived |
| M22 | B4.1 bytes not measured against MAX_BYTES | killed | 1 failed, 376 passed in 19.32s | survived |
| M23 | B4.3 write mode exits non-zero over the limit | killed | 1 failed, 373 passed in 18.92s | killed |
| M24 | B4.2 size line wrong | killed | 1 failed, 370 passed in 18.83s | killed |
| M25 | C1.2 hand edit / stale index passes | killed | 1 failed, 379 passed in 19.82s | survived |
| M26 | C1.2 no diff printed | killed | 1 failed, 379 passed in 20.60s | survived |
| M27 | C1.2 bad rev passes | SURVIVED | 408 passed in 22.66s | killed |
| M28 | C1.3 no project-memory fails | killed | 1 failed, 390 passed in 20.46s | survived |
| M29 | C1.4 check mode changes a file | killed | 1 failed, 1 passed in 0.13s | survived |
| M30 | C1.3 unborn HEAD fails | killed | 1 failed, 392 passed in 20.56s | survived |
| M31 | G2.1 change to the script alone skips the check | killed | 1 failed, 401 passed in 20.67s | survived |
| M32 | G2.1 hook lets a wrong INDEX.md through | killed | 1 failed, 398 passed in 20.68s | survived |

30/32 killed; originals restored (2 file(s))
