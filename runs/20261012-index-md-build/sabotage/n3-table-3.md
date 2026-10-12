| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| M01 | B1.2 untracked entry gets a line | killed | 1 failed, 3 passed in 0.24s | killed |
| M02 | B1.1 file outside B1.1 gets a line (subfolder) | killed | 1 failed in 0.08s | killed |
| M03 | B1.1 file outside B1.1 gets a line (prefix) | killed | 1 failed in 0.08s | killed |
| M04 | B1.3 non-ASCII path read wrongly in check mode | killed | 1 failed, 3 passed in 0.24s | survived |
| M05 | B1.3 check mode reads the working tree, not git objects | killed | 1 failed, 8 passed in 0.49s | survived |
| M06 | B2.4 malformed active entry gets a line | killed | 1 failed, 53 passed in 2.97s | killed |
| M07 | B2.4 prefix/kind mismatch passes | killed | 1 failed, 45 passed in 2.59s | killed |
| M08 | B2.3/G4.2 duplicate id passes | killed | 1 failed, 60 passed in 3.33s | killed |
| M09 | B2.5 broken retired entry stops the build | killed | 1 failed, 66 passed in 3.70s | killed |
| M10 | B2.6 bad UTF-8 ends in a traceback | killed | 1 failed, 88 passed in 4.84s | killed |
| M11 | B2.1 quotes not stripped | killed | 1 failed, 12 passed in 0.83s | killed |
| M12 | B2.2 whitespace not collapsed | killed | 1 failed, 13 passed in 0.89s | killed |
| M13 | B2.2 claim not cut at **Why:** | killed | 1 failed in 0.08s | killed |
| M14 | B3.3 locale/case order instead of code points | killed | 1 failed, 92 passed in 4.96s | survived |
| M15 | B3.1 superseded entry gets a line | killed | 1 failed, 66 passed in 3.61s | killed |
| M16 | B3.1 link not percent-encoded | killed | 1 failed, 10 passed in 0.65s | killed |
| M17 | B3.3 CRLF kept | killed | 1 failed, 96 passed in 5.18s | killed |
| M18 | B3.2 wrong fixed head | killed | 1 failed in 0.08s | killed |
| M19 | B3.4 identical file rewritten | killed | 1 failed, 98 passed in 5.31s | killed |
| M20 | B4.3 line dropped to fit | killed | 1 failed, 102 passed in 5.57s | survived |
| M21 | B4.3 --check passes over the limit | killed | 1 failed, 104 passed in 5.83s | survived |
| M22 | B4.1 bytes not measured against MAX_BYTES | killed | 1 failed, 105 passed in 5.90s | survived |
| M23 | B4.3 write mode exits non-zero over the limit | killed | 1 failed, 102 passed in 5.58s | killed |
| M24 | B4.2 size line wrong | killed | 1 failed, 99 passed in 5.33s | killed |
| M25 | C1.2 hand edit / stale index passes | killed | 1 failed, 108 passed in 6.29s | survived |
| M26 | C1.2 no diff printed | killed | 1 failed, 108 passed in 6.31s | survived |
| M27 | C1.2 bad rev passes | SURVIVED | 137 passed in 7.99s | killed |
| M28 | C1.3 no project-memory fails | killed | 1 failed, 119 passed in 6.89s | survived |
| M29 | C1.4 check mode changes a file | killed | 1 failed, 1 passed in 0.13s | survived |
| M30 | C1.3 unborn HEAD fails | killed | 1 failed, 121 passed in 6.87s | survived |
| M31 | G2.1 change to the script alone skips the check | killed | 1 failed, 130 passed in 8.11s | survived |
| M32 | G2.1 hook lets a wrong INDEX.md through | killed | 1 failed, 127 passed in 7.97s | survived |

31/32 killed; originals restored (2 file(s))
