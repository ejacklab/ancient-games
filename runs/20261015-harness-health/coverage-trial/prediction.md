# Coverage trial — units and prediction (written before any generation and before reading the tests)

EJ, 2026-10-15: "5 go" — run the two-generation trial on one past requirement.

## The requirement

`docs/memory-system/SOURCE_OF_TRUTH_REQUIREMENTS.yaml`, **W1.1b** (MUST), checked by `tools/memory_index.py`:

> The `id` is `DD-MM-xxxxxx-YYYY`: the day, month and year the entry is written, six random lowercase letters and
> digits, for example `13-10-k3f7a2-2026`. Writers on different branches pick ids without coordinating, so an id is
> never "the next free number". No two entries share an id. An id never changes, so the file keeps its name.
>
> fails_if: an id is not in the W1.1 form, two entries share an id, or git shows an entry file renamed to a different id.

Chosen because it is short, has a `fails_if`, a tool check and existing tests (`tests/test_memory_index*.py`), and a
past fix (B2.3, merged in `6415a1c`).

## Units, fixed from the requirement before generating (孫子's step i)

Written by the main agent from the text and `fails_if` only.

| Unit | Behaviour | From |
|---|---|---|
| U1 | An id not in the form `DD-MM-xxxxxx-YYYY` is rejected (wrong separators, wrong part lengths, wrong part order, missing part) | fails_if (a) |
| U2 | The six-character part is lowercase letters and digits only (uppercase, other characters rejected) | text |
| U3 | The date parts are a real day/month/year (e.g. 32-13 rejected) | text: "the day, month and year" — *not in fails_if; whether the tool must check it is unclear* |
| U4 | Two entries with the same id are rejected | fails_if (b) |
| U5 | An entry file renamed to a different id is caught (git) | fails_if (c) |
| U6 | A valid id is accepted (the requirement met, not only broken) | text, the example |

## Method

1. Two briefs, same engine (dsh, deepseek-flash), same requirement text, **different phrasing** — A asks for "the test
   cases", B asks to "brainstorm every possible scenario and edge case". The engine sees the requirement only, not the
   tests and not the units above.
2. Main agent maps each generated case to one unit, or to **none** (a behaviour no unit holds — a candidate new unit),
   or **out** (not about this requirement).
3. Main agent reads the existing tests and marks each unit, and each generated case, covered or not, with `file:line`.
4. Report: raw count A vs B; raw coverage % A vs B; unit coverage %; cases mapped to `none` (did a run move the unit
   denominator?); classes found by both (capture–recapture, Dave: lower bound only).

## Prediction

- The raw case counts differ between A and B, and the raw coverage % differs by more than the unit coverage %
  (which, with the units fixed, moves only if a run adds a `none` case accepted as a new unit).
- At least one generated case maps to `none` or `out` in each run.

## Who wrote what, and what it does not establish

The units, the mapping and the coverage marks are all the main agent's (*my reading*). The trial is n=1 on one short
requirement, one engine; it shows whether the effect exists here, not how large it is in general. The mapping is the
weak point: a different mapper could group cases differently.
