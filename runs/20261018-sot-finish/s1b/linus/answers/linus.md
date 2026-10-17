# Linus Torvalds — Finish the memory design

## Answer

Provisionally choose **D1:** `project-memory/start-file-limits.json`; **D2:** replace the built-in example only with complete reader coverage; **D3:** keep both replacement paths; **D4:** adopt `detect-secrets` alongside review; **D5:** attempt agy measurement now. These are recommendations for EJ’s final review, not measured results.

## How I decided

1. **D1 — JSON beside `INDEX.md`: my #9 and my #13.**

   These are the project’s installed readers and limits, so their data belongs with the project’s memory. JSON avoids adding a parser dependency: Python supplies it, including hooks that can reject duplicate keys and non-finite numbers. [Python documentation](https://docs.python.org/3/library/json.html)

   **Words to write — proposed design:**

   Store the owner’s reader inventory and limit records in `project-memory/start-file-limits.json`. Each reader record contains `agent`, `engine_version`, `load_path`, and `limits`. Each limit contains `value`, `unit`, `scope`, `basis` (`measured`, `documented`, or `example`), and `source`.

   Enforce every applicable constraint in its own unit and scope. Do not compare bytes with lines or convert tokens using an assumed ratio. A combined startup budget includes the other startup material.

   Write mode reads the working-tree configuration; check mode reads it from the same git snapshot as the entries being checked.

2. **D2 — Complete coverage before replacement: my #1, my #7, and my #9.**

   File existence proves nothing about coverage. An explicit inventory lets the tool detect a missing reader record, although the owner still determines whether that inventory reflects actual startup behavior.

   **Words to write — proposed design:**

   When the file is absent, retain Rd3.1b’s existing example of **200 lines and 24,000 bytes**, and report its example basis. Replace that fallback only when every reader in the owner’s inventory has a valid record with enforceable constraints.

   A present but incomplete or invalid file causes both modes to return failure and identify the problem. Missing reader records, duplicate keys, empty inventories, non-positive values, missing sources, and unsupported units are errors; they do not silently restore the fallback.

   File-based values retain their individual basis labels. Reading a documented limit does not make it measured. The tool cannot claim complete startup coverage from example values.

3. **D3 — Preserve both replacements: my #5 and my #9.**

   W6.3a already preserves additions from both sides. Apply that consistently using the merge base: replacing one original path with different paths produces two additions and removal of the original. Repository existence cannot decide which path the memory should cover.

   **Words to write — proposed clarification of W6.3a:**

   When both sides replace the same base `covers` path differently, the merger removes the original path, retains both replacement paths, and preserves both `changed:` records. A later correction follows the existing entry-correction rules.

   This avoids discarding either contributor’s information or creating a new approval gate.

4. **D4 — Adopt `detect-secrets`, retain the reviewer: my #13, my #17, and my #18.**

   Maintaining credential detectors is a separate responsibility from generating an index. `detect-secrets` supplies an existing installation and review workflow; it is an added development dependency. [Project documentation](https://github.com/Yelp/detect-secrets)

   **Words to write — proposed design:**

   The main implementation agent installs and records a tested release of `detect-secrets` in the project’s development environment and integrates it as a separate scanner. `tools/memory_index.py` remains standard-library-only.

   The scanner checks all entry files from the same snapshot being validated. Scanner findings and scanner execution failures stop that automated check. The project owner or their designated reviewer classifies findings and reviews sensitive material outside the scanner’s coverage. Suppressions record reviewed false positives; they do not permit actual credentials.

   Keep W3.2’s `check: secret scanner; reviewer`. Until installation and integration are verified, describe the check as reviewer-only, as the current requirements already do.

5. **D5 — Attempt measurement now: my #2, my #7, and my #18.**

   The run needs evidence about the installed loader. Start from the documented **24,000-byte** per-file figure supplied in the brief, treating it as a probe location rather than an established boundary.

   **Words to write — proposed measurement guidance:**

   The main agent tests agy’s actual startup load path in an isolated fixture, recording engine version, configuration, file encoding, exact sizes, other startup files, and observed results. Use a small control file and fresh sessions with unpredictable sentinels at recorded offsets. Do not explicitly read the files during the test.

   Probe below and above the documented boundary, then narrow any observed transition. Vary multibyte text and competing startup files separately to distinguish byte, character, and aggregate-budget effects.

   Prefer loader logs or captured startup content. Sentinel recall establishes behavioral evidence; failure to recall does not by itself prove truncation. If the control fails or startup loading cannot be observed, report the measurement as inconclusive and retain the documented/example basis.

6. **My reading — requirement-check of these proposals.**

   | Criterion | Result |
   |---|---|
   | Who decides | **Pass:** owner supplies readers; tool applies constraints; merger preserves changes; reviewer judges findings. |
   | One thing | **Pass:** configuration, validation, merge handling, scanning, and measurement remain separate actions. |
   | Unit | **Pass:** native units and scope are recorded; no estimated conversions. |
   | Can it fail | **Pass:** missing records, exceeded constraints, lost replacements, and scanner failures are concrete failures. |
   | Weak words | **FAIL:** W3.2’s sensitive-data scope remains unspecified beyond credentials. |
   | Level | **Pass:** existing safety gates remain gates; measurement is guidance. |
   | Basis | **Pass as provisional:** existing requirements and supplied research support the choices; their effectiveness here is not measured. Revisit at EJ’s end-of-run review. |
   | Links | **Pass:** D1–D2 serve Rd3.1; D3 clarifies W6.3a; D4 implements W3.2’s stated checks. |

## What I need to know

- Which installed agents and startup paths actually load `INDEX.md`? This determines the inventory and applicable constraints.
- Which sensitive-data categories does EJ intend W3.2 to cover beyond credentials? Provisionally, the reviewer judges those cases.
- Can agy expose startup-loader evidence? Without it, report behavioral bounds rather than an exact loader limit.

These questions return to the main run under its time-boxed decision process.

## Costs and risks

- **D1 — my #9, my #18:** JSON requires careful editing; scope-aware counting adds implementation work.
- **D2 — my #1, my #7:** incomplete configuration blocks validation. The missing-file fallback remains an example and cannot prove that every reader fits.
- **D3 — my #5:** retaining both replacements can leave obsolete coverage. Normal reading and correction must resolve that.
- **D4 — my #13, my #18:** installation, updates, and false-positive review cost time. Passing the scanner does not establish absence of credentials or sensitive data.
- **D5 — my #2, my #18:** probing consumes run time and may establish only bounds for the tested installation.

## How we would know I was right

These are **checks proposed by this advisor**, not executed or independent evidence:

- Configuration checks reject incomplete records and enforce differently expressed constraints without unit conversion.
- Merge fixtures preserve both replacements and both change records while removing the original path.
- Scanner integration catches synthetic credential fixtures in the validated snapshot, including when the working tree differs from staging.
- Agy trials reproduce an observed loading boundary or honestly report an inconclusive result.
- An actual fresh session loads the complete generated index and continues the project’s work.

Passing implementation checks alone would not establish complete reader coverage or absence of sensitive data.