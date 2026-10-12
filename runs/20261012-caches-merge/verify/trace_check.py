"""Trace check for the merged caches design (written by the COO before the merge existed).
Checks: (1) every finding id in the merge occurs in Version A or B; (2) every number in the merge occurs in A or B
(as written); (3) the vision's never-rules are still stated; (4) no file outside this run folder changed.
It does NOT establish that a claim is attached to the right number, that a copied row still means the same thing,
or that the merge is the *best* version: that needs reading."""
import re, subprocess, sys
M = '/home/smoke01/dev/ancient-games/runs/20261012-caches-merge'
A = open(f'{M}/inputs/version-A.md').read(); B = open(f'{M}/inputs/version-B.md').read(); AB = A + B
G = open(f'{M}/merge/CACHES.merged.md').read()
ids = sorted(set(re.findall(r'\b(?:[SVG]-F\d+[a-z]?|BM-\d+|s3-F\d+|M\d+|D\d|R\d(?:\.\d)?|CP\d)\b', G)))
bad_ids = [i for i in ids if not re.search(rf'\b{re.escape(i)}\b', AB)]
nums = sorted(set(re.findall(r'(?<![\w.-])\d[\d,]*(?:\.\d+)?(?:\s?(?:%|ms|s|MB|KB|K))?(?![\w-])', G)))
bad_nums = [n for n in nums if n.strip() not in AB]
never = {'never the source of truth': r'source of truth', 'full rebuild / never patched': r'(never patched|full rebuild)',
         'not read at session start': r'session start', 'absence must not stop reading': r'(absen|readable with no cache|fall back)'}
missing_rules = [k for k, p in never.items() if not re.search(p, G, re.I)]
base = open(f'{M}/baseline-git-status.txt').read().splitlines()
now = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True,
                     cwd='/home/smoke01/dev/ancient-games').stdout.splitlines()
changed = [l for l in now if l not in base and 'runs/20261012-caches-merge' not in l]
print(f'ids in merge: {len(ids)}; not in A or B: {bad_ids}')
print(f'numbers in merge: {len(nums)}; not found verbatim in A or B ({len(bad_nums)}): {bad_nums[:60]}')
print(f'never-rules missing: {missing_rules}')
print(f'files changed outside this run since baseline: {changed}')
print('lines:', G.count(chr(10)), '| sections:', [l for l in G.splitlines() if l.startswith('## ')])
