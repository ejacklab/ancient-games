| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| N01 | B2.3 trailing junk passes (start-only match) | killed | 1 failed, 102 passed in 5.22s | killed |
| N02 | B2.3 non-ASCII digit passes (\d) | killed | 1 failed, 111 passed in 5.83s | killed |
| N03 | B2.1/B2.3 form checked on the raw value, before quotes and spaces are stripped | killed | 1 failed in 0.08s | killed |
| N04 | B2.3 id form checked in active entries only | killed | 1 failed, 67 passed in 3.69s | killed |
| N05 | B2.7 markers checked in active entries only | killed | 1 failed, 182 passed in 9.29s | killed |
| N06 | B2.7 markers in the header not checked | killed | 1 failed, 181 passed in 9.20s | killed |
| N07 | B2.7 >>>>>>> not a marker | killed | 1 failed, 208 passed in 10.50s | killed |
| N08 | B2.7 ======= treated as a marker | killed | 1 failed, 235 passed in 11.97s | killed |
| N09 | B2.7 an indented marker counts (not 'starts with') | SURVIVED | 300 passed in 16.04s | killed |
| N10 | B2.3 no id-form check at all | killed | 1 failed, 66 passed in 3.51s | killed |
| N11 | B2.3 upper case passes | killed | 1 failed, 93 passed in 4.85s | killed |
| N12 | B2.3 five random characters pass | killed | 1 failed, 84 passed in 4.40s | killed |
| N13 | B2.7 a marker is only a warning | killed | 1 failed, 181 passed in 9.29s | killed |

12/13 killed; originals restored (1 file(s))
