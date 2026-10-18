| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| L01 | B4.1 the largest row per unit applies, not the smallest | killed | 1 failed, 1501 passed in 77.12s (0:01:17) | killed |
| L02 | B4.1 a unit with no row has no limit instead of the example | killed | 1 failed, 1504 passed in 78.30s (0:01:18) | killed |
| L03 | B4.1 a characters limit is never enforced | killed | 1 failed, 1507 passed in 78.41s (0:01:18) | killed |
| L05 | B4.5 a bad file falls back to the example silently | killed | 1 failed, 1585 passed in 82.35s (0:01:22) | survived |
| L06 | B4.5 an empty limits list passes | killed | 1 failed, 1615 passed in 83.55s (0:01:23) | killed |
| L07 | B4.5 a limit of 0 passes | killed | 1 failed, 1687 passed in 87.71s (0:01:27) | killed |
| L08 | B4.5 a JSON true passes as a limit | killed | 1 failed, 1717 passed in 89.67s (0:01:29) | killed |
| L09 | B4.5 an unknown basis passes | killed | 1 failed, 1753 passed in 91.54s (0:01:31) | killed |
| L10 | B4.2 the limits source line is wrong | killed | 1 failed, 1501 passed in 76.99s (0:01:16) | killed |
| L11 | B4.2 the characters segment is never printed | killed | 1 failed, 1507 passed in 77.96s (0:01:17) | killed |
| L12 | B4.5 check mode reads the limits from the working tree | killed | 1 failed, 1795 passed in 94.01s (0:01:34) | survived |
| C01 | B2.8 the matched credential is printed | killed | 1 failed, 361 passed in 18.76s | killed |
| C02 | B2.8 a credential is only a warning | killed | 1 failed, 361 passed in 18.69s | killed |
| C03 | B2.8 the ASIA prefix is not detected | killed | 1 failed, 388 passed in 20.28s | killed |
| C04 | B2.8 a value one short of the AWS form is flagged | killed | 1 failed, 1027 passed in 53.47s | killed |
| C05 | B2.8 a private key header with a short body is flagged | killed | 1 failed, 1465 passed in 76.82s (0:01:16) | killed |
| C06 | B2.8 private key blocks are not detected | killed | 1 failed, 793 passed in 41.97s | killed |
| C07 | B2.8 xoxe- Slack tokens are not detected | killed | 1 failed, 712 passed in 37.70s | killed |
| C08 | B2.8 GitLab tokens are not detected | killed | 1 failed, 631 passed in 33.32s | killed |

19/19 killed; originals restored (1 file(s))
