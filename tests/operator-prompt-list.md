# Operator prompt list

Copy one prompt. Fill the blanks in `ALL CAPS`. These match the requests used in this repo: read the DSD, compare it to the current JS and YAML, cite file and line, and stop at a finding when the code alone cannot decide.

## What the words mean

This work is a move from an old mediation system to a new one. The old system already billed calls. The new one has to produce the same result. Most prompts ask you to read the old source, then the new source, and say where they differ.

**DSD.** The old system's source code. DSD files are Tcl procedures the legacy CCF mediation platform ran. In this repo they live under `2509/ref-docs/ccf_infra_ama_ref/`, for example `lb_mapping.dsd` (how a call becomes an AMA record) and `br_processEvent.dsd` (what happens to each record). When a prompt says "the DSD", it means this old code, not a design note. If the DSD and a spec disagree, the DSD is what billing already received.

**ADD.** The Application Design Document, `OneMediation_Voice_Application_Phase-2a.2_ADD`. It says what the new system was supposed to do. It is intent. It is not proof of what the old system did, and it is not proof of what is deployed.

**CCF.** The legacy mediation platform those DSD files ran on. People say "the DSD" for its code and "CCF" for the platform.

**ANDF / streamer.** The new platform (also called ODF). A streamer is a pipeline. Each step is a stage. A stage is a Nashorn JavaScript file plus a block in a YAML file. The YAML names the script, the Kafka topics, and the route. The JavaScript is the logic. Prompts that say "the JS" or "the YAML" mean this pair. Local unit tests run the JavaScript alone. They do not prove the deployed streamer.

**InterOp.** This project's streamer. It takes IP interconnect call records (pCSCF and iBCF) and turns them into AMA billing records for VETTER.

**CDR.** Call detail record. One usage record from the network. A session can arrive as several partial CDRs plus a final one.

**pCSCF and iBCF.** The IMS network elements that produce those CDRs. pCSCF is record type 64. iBCF is record type 82. In this project both go through the same path.

**MO / MT.** Mobile originating and mobile terminating. MO is the calling side. MT is the called side. AMA mapping fills different fields for each.

**AMA.** Automatic Message Accounting. The billing-record layout VETTER accepts. A record is a set of numbered modules (structure 0001, module 815 for octets, module 816, and others). The streamer first writes an Avro form of that record. A later connector turns Avro into the binary AMA file.

**Avro.** The schema used on Kafka. Field names in the JavaScript must match the Avro schema. "On the wire" means the bytes in that Kafka record, which is not yet the binary AMA file.

**VETTER.** The downstream billing system that consumes the AMA files.

**iop2ama.** The sink connector that reads the AMA-out Kafka topic and writes AMA files for VETTER. The mapping JavaScript does not name those files. Whether the file bytes match the old AMA layout is unknown until someone captures a file from this connector.

**Stage.** One step in the streamer, numbered in the YAML. Examples: sensor-id enrichment, validation, AMA-conversion eligibility, aggregation eligibility, session aggregation, AMA mapping (stage 12). A prompt that says "stage N" means that step's JavaScript and its YAML block together.

**Header.** A Kafka message header the stages pass forward. The record body is the CDR. Headers carry what an earlier stage decided: `_categories`, `_sensorId`, `_recordingOfficeId`, and others. The next stage reads those headers. It does not recompute them unless its own code says so.

**Category code.** A stamp in the `_categories` header. The router reads it and sends the record to output, filter, error, or recycle. Names look like `IOP-FTR-BLR-A103` (filter), `IOP-CAL-DIR-A101` (a calculated value), `IOP-ERR-LKP-A101` (lookup error), `IOP-CAL-RYC-A101` (recycle). The current stamps are whatever the JavaScript sets today. An old note can name a code that was renamed.

**Sensor ID.** The id of the network element that produced the CDR, looked up from the host address. It is written into the AMA record and used when the output file is named. An empty `sensorId` in a log means that lookup did not fill the header.

**Recording office.** Another lookup (`spd_recordingOfficeIdentifier` on stream `CCF_VETTER`). If it fails, the AMA field stays `0000000`.

**Recycle / reprocess.** The lookup failed, but the record may succeed later (reference data arrives). The streamer stamps a recycle category, holds the record, and a reprocess streamer sends it back. "Aged off" means it was retried until the day limit and then sent to error.

**Filter.** The record is valid enough to parse but must not be billed. A filter category drops it from AMA output. In the DSD, `Lb_Filter` returning 1 means filtered.

**Aggregation.** Several partial CDRs for one call are combined into one record before AMA mapping. The aggregation key is what decides they belong together (session id plus charging identifier). Summed fields add across partials. Last-value fields keep the latest partial's value.

**Distributor.** In the DSD, the component that takes the finished AMA bytes and writes the output file (`Lb_DistMgrWrite`). The mapping procedure does not build the filename. The filename pattern lives in that distributor's configuration, which is not in the DSD files in this repo.

**`.rec` fixture.** A captured or built input record used to inject one test call into Kafka. It must match the Avro schema the environment actually has. Changing the streamer so a bad fixture is accepted is not allowed.

**dev116 / dev217.** Real ANDF environments. dev217 is the one current end-to-end runs target. A pass counts only when that environment's logs show this run's key, the stage, and the output. `UNKNOWN` or `UNPROVEN` means those logs were not here.

**Schema Registry `40403`.** A standing error: the filter topic's schema subject is missing, so the filter path cannot serialize. It shows up on almost every log. It is not the bug under study unless the error names this run's key.

**Findings list.** One row per difference between the DSD and the current JavaScript or YAML: what differs, both citations, and whether it is confirmed. It is not a design document, a task plan, or a note to someone else.

**`interop-source/` and `interop/`.** New streamer JavaScript is edited under `interop-source/`. `interop/` is the deployed snapshot. A prompt that says "edit the JS" means `interop-source/` unless it names the other path.

**General rules.** The category-code naming rules (what FTR, CAL, ERR, and RYC mean, and when a stamp is applied). A prompt that cites them is asking for that rule, not a new code invented for the test.

**Correlation tag / `testSetId`.** An id stamped on a test record so a log line can be tied to that inject and not to someone else's traffic in the same environment.

Rules already in force here, so the prompts below assume them:

- InterOp streamer edits go in `interop-source/` first. Ask before copying into `interop/`.
- Sensor-ID recycling is read from `interop/iopEnrichSensorId.js` until a current copy is deployed from `interop-source/`.
- A local test is not a dev116 or dev217 pass. Missing runtime logs stay `UNKNOWN` or `UNPROVEN`.
- Ignore the recurring `iop-cdr-filter` Schema Registry `40403` unless this run's key is on it.
- A findings list is the deliverable. Do not turn it into an ADR, a task graph, or an email.
- Do not change production JS to make a test pass.

---

## Look up the source

1. Where is `FUNCTION` implemented? Point at the DSD file and line, then the JS file and line. One short paragraph, then a table.

2. Read `DSD_FILE` and explain `FUNCTION` in plain English. Point form, then a table sorted in the same order as the DSD, then a simple ASCII flow. Cite file and line.

3. Is `FUNCTION` called from `CALLER`, or does it stand alone? Quote the call site.

4. What does stage `N` implement from the DSD? List the DSD procedures and the JS file that owns each one.

5. Find every place `CATEGORY_CODE` is set. Cite JS file and line, and the DSD or general-rule line it comes from.

6. Search the DSD for how `FIELD` is handled. Quote the branch. Do not infer from the ADD if the DSD already says it.

7. Read ADD §`SECTION` and tell me only what it says about `TOPIC`. If the ADD and the DSD disagree, say so in one line and keep the DSD as the behavior.

8. Is there a file naming pattern for `ARTIFACT` in the DSD? If the DSD only hands the bytes to the distributor, say that and cite the call. Do not invent a pattern from the ADD.

9. Which file is authoritative for `TOPIC` right now: `interop/`, `interop-source/`, or the deployed YAML? Say which one you read.

10. Show me the current `_categories` codes in `interop/iopEnrichSensorId.js` and `interop/iopAggregationElig.js`. Do not cite a renamed or deleted code as current.

---

## Compare DSD to the streamer

11. Compare `DSD_PROC` in `DSD_FILE` to `JS_FILE`. List only the divergences. One row each: title, DSD citation, JS citation, `CONFIRMED` / `INFERRED` / `GAP` / `UNPROVEN`, and one line on why it matters.

12. Does `JS_FILE` follow `DSD_PROC`, or did we put the check in the wrong stage? Say which stage owns it in the DSD and which stage owns it in the YAML.

13. This DSD branch looks like a filter. Which `IOP-FTR-*` code is it, and is that code set in the JS? Cite both sides.

14. Walk this record through the DSD and then through the JS. Tell me the first branch where they disagree.

15. The JS skips `STEP`. Did the DSD skip it too? Quote the DSD. If the JS skip is not in the DSD, say so and stop.

16. Are these two stages applying the same business rule twice? Name the rule, both files, and which stage the DSD actually runs it in.

17. Sort the comparison in DSD source order so I can read the DSD beside it.

18. Check `HEADER` on this path. What does the DSD write, what does the JS write, and what does the YAML route on?

19. Read `ALGORITHM_MD` and check the unit tests and E2E against it. List tests that assert the algorithm, and tests that assert a comment or an old variable name.

20. A local test passed. Say what that proves and what is still `UNPROVEN` until a dev217 or dev116 log shows it.

---

## Findings, not a workflow

21. Extract the algorithm from `DSD_FILE`, compare it to `JS_FILE` and the stage YAML, and append divergences to `FINDINGS_FILE`. Flat list only.

22. Re-read finding `ID` against the current `JS_FILE`. Mark it still open, resolved, or wrong, with the new line citation.

23. This finding needs a human decision. Add one sentence in the row and stop. Do not draft an email or an options table.

24. List what is still not extracted. One line per item. Do not start the next extraction unless I name it.

25. Do not dispatch parallel agents. Work this list yourself, one finding at a time.

---

## Logs

26. Read `LOG_PATH`. Tell me what came in, whether it shares one aggregation key, the order, what the aggregate looked like at each step, how many records came out, where they went, and which category each one got.

27. This record hit an error. Walk the stages in the log and say which check fired. Cite the log line and the JS branch. Ignore `40403` unless it is this run's key.

28. Why is `sensorId` empty in this log? Separate enrichment lookup, recycle return, and init default. Cite the log lines.

29. Compare these two logs: `LOG_A` and `LOG_B`. What changed in category, child count, and destination?

30. Grade this run directory. Keep functional, committed-delivery, and application-health verdicts separate. Missing proof is `UNKNOWN` or `INVALID_RUN`, not `PASS`.

31. The checker failed. Is it reading another run's traffic, or is this run actually wrong? Show the key, `testSetId`, and the output record that decided it.

32. Describe this aggregation log bundle with the log-describe skill. I have not seen this bundle before.

33. Here is a screenshot at `IMAGE_PATH`. Read it and tie each line to the JS or YAML that produced it.

---

## AMA mapping

34. In `iopAMAmapping.js`, module `NNN`, what field is set and from which input? Cite the JS line and the DSD or mapping-sheet cell.

35. Compare module `NNN` in `interop-source/iopAMAmapping.js` to `lb_mapping.dsd`. One finding row if they differ.

36. Edit `interop-source/iopAMAmapping.js` only. Change module `NNN` so `FIELD` follows the DSD. Do not touch other modules.

37. Does the AMA Avro field exist on the wire, and do we know whether iop2ama keeps it in the AMA bytes? If there is no captured file, label the byte layout `UNPROVEN`.

38. For case `CASE_ID`, say what Stage 12 should emit. Do not grade iop2ama bytes unless I give you the captured file.

39. Trace `recordingOfficeID` from Stage 5b through Stage 12. What value must still be on the AMA record if the lookup fails?

40. List the modules `iopAMAmapping.js` writes, in the order the JS appends them, next to the DSD order. Do not claim iop2ama preserves that order without a capture.

---

## Aggregation, eligibility, filters

41. Explain `iopAggregationElig.js`: the category codes, the algorithm for each, and why each stamp exists. Tie each one to the general rules and to the DSD or the ADD.

42. Is `IOP-CAL-DIR-A101` an aggregation-eligibility stamp or an AMA-eligibility stamp? Cite the DSD procedure and the stage that sets it now.

43. Where is `Lb_Filter` implemented, and where is `Lb_IsEligibleForAMAConversion` implemented? Point form, table in DSD order, ASCII flow.

44. In the DSD, a return of 1 from `Lb_Filter` means filtered. Does the JS do the same, or does it keep going? Quote both.

45. Read `interop/pcscf_path/fresh-filter-algorithm.md` and compare it to the fresh-record JS. Findings list only.

46. Read `interop/pcscf_path/recycled-filter-algorithm.md` and compare it to the recycled-record JS and its tests. Findings list only.

47. What is the aggregation key, which fields are summed, and which fields are last-value? Cite the YAML `sumFields` and `lastValueFields` and the JS. Do not cite a graph.

48. This partial plus this final: what should the aggregate contain for octets, video direction, video port, and video duration? Use the DSD store rules, not a guessed formula.

49. A filtered record still got an aggregation stamp. Is that what the router does? Cite the route predicate.

50. Change the log lines in `JS_FILE` to match the style in `STYLE_FILE`. Do not change the if/else logic.

---

## Sensor ID, recycle, categories

51. Why did recycle bring every header back except `sensorId`? Read the reprocess log and `iopEnrichSensorId.js`. Cite the line that skips the lookup.

52. On a recycled record, does the DSD skip the sensor-id lookup? Quote it. If the JS skips and the DSD does not, say that in one finding row.

53. What category is set when the sensor-id lookup fails, when it ages off, and when recording-office lookup fails? Cite the current JS, not an old note.

54. FTR versus recycle: if both markers could apply, which one wins? Cite the router.

55. Generate the YAML and JS change list for `CHANGE`. Do not edit until I say to implement it. Name the files and the lines.

56. Implement only the sensor-id fix in `interop-source/`. Undo any skip that is not in the DSD. Leave recording office and aggregation alone.

---

## YAML and config

57. Read `YAML_PATH`. List stages, script filenames, input topics, and route predicates for stage `N`. Quote the predicates.

58. Why does this values file have one `inputSchemaName`? Check the other dynamic streamer and say whether two names are required.

59. Compare `VALUES_A` to `VALUES_B`. List keys that differ. Do not treat a template placeholder as a live value.

60. The dev217 sink values do not set `file.name`. Say what the file will be named from the config that is actually there, and what is unset.

61. Do not patch `interop/*.js` or deployment YAML. The change belongs in `interop-source/`. At the end, ask me what else must be promoted.

---

## E2E, fixtures, inject

62. I want one E2E folder for `SUITE`, aimed at dev217. One shell entrypoint. Fixed cases inside the Python driver. No extra scenario manifest.

63. Before writing it, look at the working package `REFERENCE_PACKAGE` and say what you will copy and what you will not.

64. Which files do I copy to dev217 to run `COMMAND`? List only those files.

65. Make the injector send one record per run. Each record needs a new correlation tag. Do not overwrite a transferred `.rec`.

66. Inject `N` MO then `N` MT. Each record must differ in a field the pipeline actually reads. Say which field.

67. Is `RECORD_FILE` a valid `.rec` against the captured dev schema? If it will be rejected, say the missing field.

68. Add the validation and filter cases that are in the algorithm doc and missing from the suite. Do not add cases the algorithm does not name.

69. The package failed on dev217 because the fixtures were missing root fields. Fix the fixtures. Do not change the streamer to accept the bad shape.

70. A failed inject must say why. Show the producer error, not only a non-zero exit.

71. Grade case `CASE_ID` from the run directory only: injected record, committed output, run-window log. Local unit tests do not count.

72. This run's fixtures must stay immutable. Stage any correlation edits under the run directory. Check the source hashes before and after.

73. Write the operator command for the copied package, including `--list`, one case, and all cases. Shell scripts use LF line endings.

---

## Explain it to a person

74. Write a short note I can hand to my senior: why these category stamps exist, which general rule and which DSD line each one comes from, and what breaks if we remove one.

75. Write a `.txt` file, not markdown. No bold, no special characters. DSD behavior, then the bug in the ANDF JS, with file and line.

76. Write a markdown file a junior can read: what the stage does, which file to edit, and what not to change.

77. Update `plans/diary.md` for this session. What changed, what was decided, what is still open.

78. Review the markdown you just wrote against `SOURCE`. Flag anything that is missing or assumed. Do not add a second summary file.

---

## Change the code

79. Implement the plan. Do not edit the plan file. Do not recreate the todos.

80. Fix `BUG` in `interop-source/JS_FILE` only. Stay inside the lines I named. Do not tidy the next function.

81. The test failed after the code change. If the code matches the DSD, fix the test. If the test found a real defect, stop and report it. Do not fix the JS in that same step.

82. Search the engineering-practices corpus before adding a new hot-path helper. A hit is a lead. Read the source locator before reusing it.

83. Do not add a field, header, lookup, or log on the record path unless you can name the DSD line or the confirmed defect that requires it.

84. Review `JS_FILE` against `SPEC_MD` and the DSD. Write a structured issue report. Do not edit the JS in that pass.

85. I said the logic is halfway, not a bug. Finish it. Write the implementation plan first and wait.

---

## Session control

86. Check the todo list. Tell me what is done and what is blocked. Do not start new work.

87. Stop. You are solving a different task than the one I asked. Restate the task in one sentence and wait.

88. The AT&T repos are not in this sandbox. Give me the commands to run on my machine. Do not clone them.

89. Commit the files for this task. Do not push unless I say push.

90. What is my first step on `TASK`? One step, then stop.
