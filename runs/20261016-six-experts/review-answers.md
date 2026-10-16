# Answers to the review (`nodes/review.result.md`, dsh / deepseek-flash; it wrote none of the code or the tests)

| # | Finding | Answer | Test (failed on ff83d32, passes now) |
|---|---|---|---|
| 1 | an option's bracket text reaches the index | fixed: only rule/check/tool/config-advice are printed, else `-` | review 1 (guard) |
| 2 | `##F-…` (no space) shifted the override and `show` missed it | fixed: the index uses insight.ts's heading rule `/^##(?!#)\s*(.*)$/` | review 2 (guard) |
| 3 | `check --sabotage` crashed with no Chinese; a bad category regex crashed the index | fixed: sabotage alters a section and cites #99 when there is no Chinese; a bad regex matches nothing | `test_sabotage_without_chinese_still_fails_the_check`; review 3 (guard) |
| 4 | under `--claude-by-caller` nothing pinned Dave and Dario to one model | fixed: the CALLER line says `on claude-sonnet-5-5` and status.json records it | `test_caller_mode_names_dave_and_darios_model` |
| 5 | the script's docstring still said four experts and Dave the control on Opus | fixed | — (text) |
| 6 | SKILL §2 said every answer cites an item; `--only` omitted dario; the links still point at four-experts | fixed the text and the id list; the `~/.claude/skills` and `~/.agents/skills` links move at merge, when the folder exists on master | — |
| 7 | no changelog entry for the rename | added (`docs/METHOD_CHANGELOG.md`); older entries keep the name they had then | — |
| 8 | two tests could not fail | fixed: every shipped category must place a planted section; Dario's Chinese test now uses a 4+ character run that fails a persona | the same tests, now able to fail |
