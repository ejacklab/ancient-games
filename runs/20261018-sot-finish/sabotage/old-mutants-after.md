| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| M01 | B1.2 untracked entry gets a line | killed | 1 failed, 3 passed in 0.35s | killed |
| M02 | B1.1 file outside B1.1 gets a line (subfolder) | killed | 1 failed in 0.16s | killed |
| M03 | B1.1 file outside B1.1 gets a line (prefix) | INVALID (old occurs 0x) |  |  |
| M04 | B1.3 non-ASCII path read wrongly in check mode | killed | 1 failed, 3 passed in 0.32s | survived |
| M05 | B1.3 check mode reads the working tree, not git objects | killed | 1 failed, 8 passed in 0.64s | survived |
| M06 | B2.4 malformed active entry gets a line | killed | 1 failed, 29 passed in 1.78s | killed |
| M07 | B2.4 prefix/kind mismatch passes | killed | 1 failed, 35 passed in 2.09s | killed |
| M08 | B2.3/G4.2 duplicate id passes | killed | 1 failed, 147 passed in 8.00s | killed |
| M09 | B2.5 broken retired entry stops the build | killed | 1 failed, 156 passed in 8.43s | killed |
| M10 | B2.6 bad UTF-8 ends in a traceback | killed | 1 failed, 178 passed in 9.66s | killed |
| M11 | B2.1 quotes not stripped | killed | 1 failed, 12 passed in 0.88s | killed |
| M12 | B2.2 whitespace not collapsed | killed | 1 failed, 13 passed in 0.94s | killed |
| M13 | B2.2 claim not cut at **Why:** | killed | 1 failed in 0.16s | killed |
| M14 | B3.3 locale/case order instead of code points | killed | 1 failed, 2693 passed in 142.04s (0:02:22) | survived |
| M15 | B3.1 superseded entry gets a line | killed | 1 failed, 49 passed in 2.80s | killed |
| M16 | B3.1 link not percent-encoded | killed | 1 failed, 10 passed in 0.73s | killed |
| M17 | B3.3 CRLF kept | killed | 1 failed, 2698 passed in 142.73s (0:02:22) | killed |
| M18 | B3.2 wrong fixed head | killed | 1 failed in 0.16s | killed |
| M19 | B3.4 identical file rewritten | killed | 1 failed, 2700 passed in 142.37s (0:02:22) | killed |
| M20 | B4.3 line dropped to fit | INVALID (old occurs 0x) |  |  |
| M21 | B4.3 --check passes over the limit | INVALID (old occurs 0x) |  |  |
| M22 | B4.1 bytes not measured against MAX_BYTES | INVALID (old occurs 0x) |  |  |
| M23 | B4.3 write mode exits non-zero over the limit | INVALID (old occurs 0x) |  |  |
| M24 | B4.2 size line wrong | INVALID (old occurs 0x) |  |  |
| M25 | C1.2 hand edit / stale index passes | killed | 1 failed, 3085 passed in 164.50s (0:02:44) | survived |
| M26 | C1.2 no diff printed | killed | 1 failed, 3085 passed in 164.73s (0:02:44) | survived |
| M27 | C1.2 bad rev passes | SURVIVED | 3114 passed in 166.32s (0:02:46) | killed |
| M28 | C1.3 no project-memory fails | killed | 1 failed, 3096 passed in 164.72s (0:02:44) | survived |
| M29 | C1.4 check mode changes a file | killed | 1 failed, 1 passed in 0.21s | survived |
| M30 | C1.3 unborn HEAD fails | killed | 1 failed, 3098 passed in 165.87s (0:02:45) | survived |
| M31 | G2.1 change to the script alone skips the check | killed | 1 failed, 3107 passed in 165.64s (0:02:45) | survived |
| M32 | G2.1 hook lets a wrong INDEX.md through | killed | 1 failed, 3104 passed in 165.60s (0:02:45) | survived |
| N01 | B2.3 trailing junk passes (start-only match) | killed | 1 failed, 102 passed in 5.72s | killed |
| N02 | B2.3 non-ASCII digit passes (\d) | killed | 1 failed, 111 passed in 6.11s | killed |
| N03 | B2.1/B2.3 form checked on the raw value, before quotes and spaces are stripped | killed | 1 failed in 0.16s | killed |
| N04 | B2.3 id form checked in active entries only | killed | 1 failed, 67 passed in 3.81s | killed |
| N05 | B2.7 markers checked in active entries only | killed | 1 failed, 182 passed in 9.81s | killed |
| N06 | B2.7 markers in the header not checked | INVALID (old occurs 0x) |  |  |
| N07 | B2.7 >>>>>>> not a marker | killed | 1 failed, 208 passed in 11.21s | killed |
| N08 | B2.7 ======= treated as a marker | killed | 1 failed, 235 passed in 12.61s | killed |
| N09 | B2.7 an indented marker counts (not 'starts with') | killed | 1 failed, 253 passed in 13.48s | killed |
| N10 | B2.3 no id-form check at all | killed | 1 failed, 66 passed in 3.71s | killed |
| N11 | B2.3 upper case passes | killed | 1 failed, 93 passed in 5.13s | killed |
| N12 | B2.3 five random characters pass | killed | 1 failed, 84 passed in 4.66s | killed |
| N13 | B2.7 a marker is only a warning | killed | 1 failed, 181 passed in 9.76s | killed |
| N14 | B2.7 only the first marker line is reported (DESIGN step 5: report them all) | INVALID (old occurs 0x) |  |  |

37/46 killed; originals restored (2 file(s))
