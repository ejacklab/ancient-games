node: r1-tests-codex

Created [test_evaluator_r1_matrix_spec.py](/home/smoke01/dev/ancient-games-evaluator/tests/test_evaluator_r1_matrix_spec.py). Only that file changed; no commit.

| Finding | Test names |
|---|---|
| F3 | `test_required_citation_is_read` (5 variants), `test_prefixed_citations_follow_parametrised_keys`, `test_citation_grammar_uses_imported_spec_id` |
| F4 | `test_product_probe_write_is_recorded`, `test_copy_restores_to_before_product_run` (6 variants) |
| F5 | `test_junit_errors_are_separate_from_failures`, `test_mutant_run_records_its_own_junit_errors`, `test_collection_error_is_listed_by_junit_key`, `test_timeout_has_run_status` (2 variants), `test_missing_junit_report_has_no_report_status`, `test_existing_matrix_keys_keep_their_shapes` |
| F1 | `test_spec_cli_rejects_empty_manifest` (3 variants), `test_vision_id_prevents_empty_manifest_rejection` |
| F14 | `test_unparsed_ids_include_colon_bold_bullets`, `test_unparsed_ids_find_orphans_without_counting_prose`, `test_fully_parsed_spec_has_empty_unparsed_ids`, `test_spec_cli_writes_unparsed_ids` |

Five tests pass today:

- `test_required_citation_is_read[B1-F1]`, `[W1.3-F2]`, `[V5-F1]`: the existing regex already accepts these citations.
- `test_existing_matrix_keys_keep_their_shapes`: the existing fields already have the required shapes.
- `test_vision_id_prevents_empty_manifest_rejection`: vision ids already populate the manifest.

Collect summary: **29 tests collected in 0.03s**, exit 0.  
Current-code result: **24 failed, 5 passed in 7.63s**.

These Codex-authored checks establish the pre-repair baseline; the future repair remains unverified.