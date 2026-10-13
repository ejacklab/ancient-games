# D5 pre-registration

Written by the COO on 2026-10-13, before K1 ran. Kept out of every file a worker reads.

## K1: the clean INDEX.md generator at 21b2597

- **Expected:** MEETS: no. G1.2 (the instruction in CLAUDE.md) and G2.2 (`hooksPath`) were never done, and B4.2
  ("every run prints the size") is disputed (backlog item 1).
- **Pass bar:** every FAIL reproduces when the COO reruns its repro, and no case is PASS while its probe stays green
  on its mutant.

## K2: six seeded faults, one group each

- **Faults:** one each in B3, B2, B4, B1, G2, and a second in B3.
- **Expected:** each variant is MEETS: no, and its group is FAIL or UNKNOWN. A FAIL is the strong result.
- **Compared with:** the product's own acceptance tests (`tests/test_memory_index.py` at 21b2597) on the same
  variants.

## K3: a doctored spec

- A planted group with ids and no Fails if comes back untestable / UNKNOWN, never PASS.
- A deleted group's ids are absent from the manifest.

## K4: the blind workspace

The marker `K4-MARKER-7f3c9e2b`, planted in the product's `tests/`, never appears under `runs/20261013-eval-k1/`.
