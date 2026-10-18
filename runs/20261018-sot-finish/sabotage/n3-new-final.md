| mutant | Fails if it breaks | acceptance file | acceptance summary | unit file (info) |
|---|---|---|---|---|
| L01 | B4.1 the largest row per unit applies, not the smallest | killed | 1 failed, 2704 passed in 140.84s (0:02:20) | killed |
| L02 | B4.1 a unit with no row has no limit instead of the example | killed | 1 failed, 2707 passed in 141.03s (0:02:21) | killed |
| L03 | B4.1 a characters limit is never enforced | killed | 1 failed, 2710 passed in 141.48s (0:02:21) | killed |
| L05 | B4.5 a bad file falls back to the example silently | killed | 1 failed, 2789 passed in 145.68s (0:02:25) | survived |
| L06 | B4.5 an empty limits list passes | killed | 1 failed, 2818 passed in 147.48s (0:02:27) | killed |
| L07 | B4.5 a limit of 0 passes | killed | 1 failed, 2890 passed in 151.57s (0:02:31) | killed |
| L08 | B4.5 a JSON true passes as a limit | killed | 1 failed, 2920 passed in 152.91s (0:02:32) | killed |
| L09 | B4.5 an unknown basis passes | killed | 1 failed, 2956 passed in 155.44s (0:02:35) | killed |
| L10 | B4.2 the limits source line is wrong | killed | 1 failed, 2704 passed in 140.76s (0:02:20) | killed |
| L11 | B4.2 the characters segment is never printed | killed | 1 failed, 2710 passed in 143.21s (0:02:23) | killed |
| L12 | B4.5 check mode reads the limits from the working tree | killed | 1 failed, 3071 passed in 164.88s (0:02:44) | survived |
| C01 | B2.8 the matched credential is printed | killed | 1 failed, 361 passed in 19.16s | killed |
| C02 | B2.8 a credential is only a warning | killed | 1 failed, 361 passed in 19.11s | killed |
| C03 | B2.8 the ASIA prefix is not detected | killed | 1 failed, 388 passed in 20.66s | killed |
| C04 | B2.8 a value one short of the AWS form is flagged | killed | 1 failed, 1027 passed in 54.16s | killed |
| C05 | B2.8 a private key header with a short body is flagged | killed | 1 failed, 1465 passed in 76.95s (0:01:16) | killed |
| C06 | B2.8 private key blocks are not detected | killed | 1 failed, 793 passed in 41.90s | killed |
| C07 | B2.8 xoxe- Slack tokens are not detected | killed | 1 failed, 712 passed in 37.60s | killed |
| C08 | B2.8 GitLab tokens are not detected | killed | 1 failed, 631 passed in 33.36s | killed |
| R01 | B2.8 another report prints a credential (shown() disabled) | killed | 1 failed, 1972 passed in 103.55s (0:01:43) | survived |
| R02 | B4.5 deep JSON ends in a traceback | killed | 1 failed, 3052 passed in 162.76s (0:02:42) | survived |
| R03 | B4.5 a dangling link falls back to the example | killed | 1 failed, 3058 passed in 162.56s (0:02:42) | survived |
| R04 | B4.5 an unmerged limits file falls back to the example | killed | 1 failed, 3062 passed in 163.61s (0:02:43) | survived |
| R05 | B4.5 a missing limits blob falls back to the example | killed | 1 failed, 3063 passed in 163.06s (0:02:43) | survived |
| R06 | B4.5 a limits error is hidden behind entry errors (write mode) | killed | 1 failed, 3065 passed in 163.25s (0:02:43) | survived |
| R07 | B2.8 a BEGIN marker inside a line is missed | killed | 1 failed, 1876 passed in 98.76s (0:01:38) | survived |
| R08 | B2.8 a Slack token right after _ is flagged | killed | 1 failed, 1630 passed in 85.66s (0:01:25) | survived |
| R09 | B2.8 surrounding spaces count toward the key body | killed | 1 failed, 1948 passed in 102.47s (0:01:42) | survived |
| R10 | B4.5 a folder at the limits path in the snapshot falls back to the example | SURVIVED | 3114 passed in 166.38s (0:02:46) | killed |

28/29 killed; originals restored (1 file(s))
