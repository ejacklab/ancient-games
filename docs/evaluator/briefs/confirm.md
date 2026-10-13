# Evaluator step E8 — is this failing probe faithful to its requirement?

## Task (one deliverable)

For each probe that failed on the real product, listed in `{RUN}/confirm-input.json`, answer one question: **does
this probe test what the requirement's own sentence says?** Write `{RUN}/confirm.json`. You do not judge the product;
you judge the probe.

## Context (only what this step needs)

For each entry, `{RUN}/confirm-input.json` gives:
- the case id and its failure text;
- the requirement sentences of its group, quoted from the spec;
- the probe's source;
- the probe's failure output, capped.

You see nothing else: not the product's code, not the mutants, not the other probes.

## Template (DATA.md, E8)

```json
{"cases": [{"case": "<id>", "probe": "<probe key>", "faithful": true|false,
            "requirement_quote": "<the exact sentence the probe relies on>",
            "probe_quote": "<the exact assertion that failed>"}]}
```

- **First, read the failure output.** It must show **the quoted assertion itself failing**. A setup error, a
  collection error, an import error, a missing file or path, or an empty output means the probe never reached its
  check. Answer `faithful: false`, and say so in your reply. *(Calibration K1, 2026-10-13: 28 probes that never ran
  were confirmed from their source alone.)*
- **faithful: true** means the failed assertion is what the sentence requires, and the output shows that assertion
  failing. The product is then wrong.
- **faithful: false** means the assertion demands something the sentence does not say, or contradicts another sentence
  of the same spec. The probe is then wrong, and the case becomes UNKNOWN (EV-C4.2).

## Example (real sentence from the evaluator's spec, EV-R1.1)

- **Sentence:** *"A requirement the file marks *open* is listed as out of scope, with that reason."*
- **Probe:** asserts `verdict == "UNKNOWN"` for the open id `G4.1`.
- **Output:** `KeyError: 'G4.1'`, because the id is in `out_of_scope` and has no verdict row.

```json
{"case": "EV-R1-F2", "probe": "test_spec::test_open_id", "faithful": false,
 "requirement_quote": "A requirement the file marks *open* is listed as out of scope, with that reason.",
 "probe_quote": "assert row[\"verdict\"] == \"UNKNOWN\""}
```

The sentence asks for "out of scope", not for an UNKNOWN verdict, so the probe is not faithful.

## Standard

- `requirement_quote` and `probe_quote` are **verbatim**. A script checks each against its source, and a quote that
  is not found voids your answer for that case.
- One answer per listed probe. No answer counts as not faithful.

## Write the result to

Write every file with the Write tool, not with shell redirection such as `cat > file`. Then list the file once to confirm it exists: a step whose file is missing has failed, and the run stops there.

`{RUN}/confirm.json`. Reply in one line: the counts of faithful and not faithful.
