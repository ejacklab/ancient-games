# Traceability — 20261014-memory-index-cleanup

Written by the COO at N5 from `trace_check.cited()` over both test files at `6126804`, `sabotage/n3-new-final.md`
and `nodes/n4-1.result.md`. Only the criteria this run changed or depends on; the rest is the baseline, unchanged
(old mutants identical to N0's control, `sabotage/old-mutants-final.md`).

| criterion | acceptance tests (N1, Codex) | unit tests (N2, COO) | mutants (N3) | review (N4) |
|---|---|---|---|---|
| B2.1 | 3: test_crlf_entries_render_as_lf_utf8, test_header_reads_only_top_level_fields_and_strips_quotes, test_malformed_entries_fail_without_writing | 2 | N03 killed; M11 killed | O1 to backlog |
| B2.3 | 7: test_all_validation_problems_are_reported, test_duplicate_ids_are_rejected_in_every_status, test_entries_require_top_level_nonempty_id, test_id_form_is_accepted_without_calendar_validation, test_inactive_entries_still_require_id_and_status, test_invalid_id_forms_fail_in_every_status, test_malformed_entries_fail_without_writing | 5 | N01 N02 N03 N04 N10 N11 N12 killed; M08 killed | checklist 1 yes; F3 fixed; O1 to backlog |
| B2.5 | 2: test_inactive_content_problems_warn_without_blocking, test_inactive_entries_still_require_id_and_status | 2 | N04 N05 N13 killed; M09 killed | — |
| B2.7 | 3: test_conflict_markers_after_other_characters_are_accepted, test_conflict_markers_fail_in_every_status, test_heading_underline_is_not_a_conflict_marker | 4 | N05 N06 N07 N08 N09 N13 killed; N14 killed by the unit file only | checklist 2 no on the plant only (F1 = plant); F2 to backlog; F4 F5 fixed |
| G4.2 | 3: test_duplicate_ids_are_rejected_in_every_status, test_id_form_is_accepted_without_calendar_validation, test_invalid_id_forms_fail_in_every_status | 2 | N01 N02 N04 N10 N11 N12 killed; M08 killed | checklist 1 yes |
