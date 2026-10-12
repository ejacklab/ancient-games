# Traceability — 20261012-index-md-build

Written by the COO at N5 from `trace_check.cited()` over both test files and `sabotage/n3-table-3.md`. Criterion → tests → mutants → review. M27 is the one survivor: an **equivalent** mutant (a bad rev still exits 1 through the git-error path; verified by hand, N3 log).

| criterion | acceptance tests (N1, Codex) | unit tests (N2/COO) | mutants (N3) | review (N4) |
|---|---|---|---|---|
| B1.1 | 2: test_only_direct_matching_entry_files_are_read, test_golden_bytes_for_all_kinds_and_encode | 1 | M02 killed, M02 killed, M03 killed, M03 killed |  |
| B1.2 | 3: test_untracked_matching_entry_is_an_error, test_untracked_inactive_entry_is_an_error, test | 1 | M01 killed |  |
| B1.3 | 2: test_check_uses_snapshot_instead_of_working_tree, test_snapshot_reads_use_nul_paths_and_on | 0 | M04 killed, M05 killed |  |
| B2.1 | 3: test_header_reads_only_top_level_fields_and_strips_quotes, test_malformed_entries_fail_wit | 2 | M11 killed |  |
| B2.2 | 1: test_claim_ends_at_why_and_collapses_whitespace | 1 | M12 killed, M13 killed |  |
| B2.3 | 4: test_malformed_entries_fail_without_writing, test_duplicate_ids_are_rejected_in_every_stat | 2 | M08 killed | F2 fixed |
| B2.4 | 3: test_malformed_entries_fail_without_writing, test_staged_malformed_active_entries_fail_wit | 2 | M06 killed, M07 killed |  |
| B2.5 | 2: test_inactive_content_problems_warn_without_blocking, test_inactive_entries_still_require_ | 1 | M09 killed |  |
| B2.6 | 2: test_invalid_utf8_reports_filename_without_traceback, test_all_validation_problems_are_rep | 2 | M10 killed | F5 fixed |
| B3.1 | 2: test_golden_bytes_for_all_kinds_and_encoded_paths, test_no_active_entries_has_fixed_placeh | 2 | M15 killed, M16 killed |  |
| B3.2 | 2: test_golden_bytes_for_all_kinds_and_encoded_paths, test_no_active_entries_has_fixed_placeh | 2 | M18 killed |  |
| B3.3 | 3: test_golden_bytes_for_all_kinds_and_encoded_paths, test_locale_does_not_change_bytes, test | 2 | M14 killed, M17 killed |  |
| B3.4 | 2: test_missing_index_is_created, test_identical_index_is_not_rewritten | 0 | M19 killed |  |
| B4.1 | 3: test_size_line_counts_lines_and_utf8_bytes, test_overflow_is_written_whole_with_warning, t | 0 | M22 killed |  |
| B4.2 | 1: test_size_line_counts_lines_and_utf8_bytes | 1 | M24 killed | F4 → backlog |
| B4.3 | 2: test_overflow_is_written_whole_with_warning, test_check_rejects_equal_bytes_over_size_limi | 1 | M20 killed, M21 killed, M23 killed | F3 fixed |
| B4.4 | 1: test_reducing_index_below_limit_clears_check | 0 | — |  |
| C1.1 | 3: test_check_uses_snapshot_instead_of_working_tree, test_check_rejects_wrong_snapshot_index_ | 0 | — |  |
| C1.2 | 5: test_malformed_entries_fail_without_writing, test_check_rejects_equal_bytes_over_size_limi | 1 | M25 killed, M26 killed, M27 SURVIVED |  |
| C1.3 | 1: test_empty_snapshots_report_nothing_to_check | 1 | M28 killed, M30 killed |  |
| C1.4 | 1: test_check_does_not_write_files_or_git_state | 0 | M29 killed |  |
| C2.1 | 2: test_golden_bytes_for_all_kinds_and_encoded_paths, test_repository_head_passes_committed_s | 0 | the file runs under the repo's pytest (gate) |  |
| C2.2 | 4: test_golden_bytes_for_all_kinds_and_encoded_paths, test_identical_index_is_not_rewritten,  | 0 | golden bytes M18; rerun M19; hand edit M25; superseded M15; --check HEAD (O4: checks nothing yet) |  |
| G1.1 | 4: test_check_rejects_wrong_snapshot_index_with_diff, test_pre_commit_blocks_relevant_changes | 0 | caught through C1 (M25, M31, M32) |  |
| G2.1 | 4: test_pre_commit_blocks_relevant_changes_with_wrong_index, test_pre_commit_allows_consisten | 0 | M31 killed, M32 killed |  |
| G2.3 | 2: test_repository_head_passes_committed_snapshot_check, test_check_catches_commit_that_bypas | 0 | through C2.2 --check HEAD and the bypass test (M25) |  |
| G3.1 | 1: test_index_merge_attribute_uses_normal_text | 0 | [static] test; no mutant (a file attribute, not code) |  |
| G3.2 | 1: test_conflicted_index_is_regenerated_from_merged_entries | 0 | behaviour of a rerun; covered by the build mutants |  |
| G4.2 | 1: test_duplicate_ids_are_rejected_in_every_status | 1 | M08 killed |  |

Criteria with no acceptance test: none.
