| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| N01 | B2.3 trailing junk passes (start-only match) | killed | 1 failed, 102 passed in 5.34s | killed |
| N02 | B2.3 non-ASCII digit passes (\d) | killed | 1 failed, 111 passed in 5.78s | killed |
| N03 | B2.1/B2.3 form checked on the raw value, before quotes and spaces are stripped | killed | 1 failed in 0.08s | killed |
| N04 | B2.3 id form checked in active entries only | killed | 1 failed, 67 passed in 3.56s | killed |
| N05 | B2.7 markers checked in active entries only | killed | 1 failed, 182 passed in 9.41s | killed |
| N06 | B2.7 markers in the header not checked | killed | 1 failed, 181 passed in 9.38s | killed |
| N07 | B2.7 >>>>>>> not a marker | killed | 1 failed, 208 passed in 10.69s | killed |
| N08 | B2.7 ======= treated as a marker | killed | 1 failed, 235 passed in 12.00s | killed |
| N09 | B2.7 an indented marker counts (not 'starts with') | killed | 1 failed, 253 passed in 12.99s | killed |
| N10 | B2.3 no id-form check at all | killed | 1 failed, 66 passed in 3.50s | killed |
| N11 | B2.3 upper case passes | killed | 1 failed, 93 passed in 4.86s | killed |
| N12 | B2.3 five random characters pass | killed | 1 failed, 84 passed in 4.41s | killed |
| N13 | B2.7 a marker is only a warning | killed | 1 failed, 181 passed in 9.39s | killed |
| N14 | B2.7 only the first marker line is reported (DESIGN step 5: report them all) | SURVIVED | 408 passed in 21.30s | killed |

13/14 killed; originals restored (1 file(s))
