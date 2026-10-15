1. `13-10-k3f7a2-2026` (the exact example) → passes: W1.1 form, unique, unchanged.
2. Six random characters all lowercase letters (`13-10-abcdef-2026`) → passes if the alphabet is `[a-z0-9]` with no per-type quota; spec gap if W1.1 requires at least one digit.
3. Six random characters all digits (`13-10-123456-2026`) → passes if alphabet-only; spec gap if W1.1 requires at least one letter.
4. Random part mixed letters and digits (`13-10-a1b2c3-2026`) → passes.
5. Random part contains an uppercase letter (`13-10-A1b2c3-2026`) → fails: uppercase is outside the lowercase alphabet.
6. Random part contains a hyphen (`13-10-k3-7a2-2026`) → fails: the six-character field gains a delimiter/illegal character.
7. Random part contains `_`, `.`, `/`, `+`, `#`, `@` or a space → fails.
8. Random part contains a non-ASCII letter (`13-10-käf7a2-2026`) → fails.
9. Random part contains a Unicode digit or a full-width character → fails.
10. Random part contains an emoji or a combining mark → fails.
11. Random part has 5 characters (`13-10-k3f7a-2026`) → fails: wrong length.
12. Random part has 7 characters (`13-10-k3f7a22-2026`) → fails: wrong length.
13. Random part absent (`13-10--2026`) → fails: empty field.
14. An extra hyphen-delimited field (`13-10-k3f7a2-extra-2026`) → fails: extra field.
15. Year missing (`13-10-k3f7a2`) → fails: not the W1.1 form.
16. Single-digit day (`3-10-k3f7a2-2026`) → fails: DD is two digits.
17. Single-digit month (`13-3-k3f7a2-2026`) → fails: MM is two digits.
18. Three-digit day or month (`013-10-...`, `13-010-...`) → fails.
19. Day `00` (`00-10-k3f7a2-2026`) → in shape but not a real date; spec gap: does W1.1 require a calendar-valid date?
20. Month `00` (`13-00-k3f7a2-2026`) → same gap.
21. Month `13` (`13-13-k3f7a2-2026`) → same gap.
22. Day `32` (`32-10-k3f7a2-2026`) → same gap.
23. February 30 (`30-02-k3f7a2-2026`) → same gap.
24. February 29 in a non-leap year (`29-02-k3f7a2-2023`) → same gap.
25. February 29 in a leap year (`29-02-k3f7a2-2024`) → passes if calendar validity is required and leap years are handled.
26. Day 31 in a 30-day month (`31-04-k3f7a2-2026`) → same gap.
27. Year not four digits (`-26`, `-20266`) → fails.
28. Year contains a letter (`13-10-k3f7a2-20a6`) → fails.
29. Year `0000` → in shape but calendar-invalid; spec gap.
30. Separators removed (`1310-k3f7a2-2026`) → fails.
31. Separators changed to `/`, `.`, `_` or a space → fails.
32. Extra or trailing separator (`13-10-k3f7a2-2026-`) → fails.
33. Unicode dash or en-dash instead of `-` → fails.
34. Non-breaking space between fields → fails.
35. Leading/trailing whitespace on the filename id → fails unless the checker trims; trimming rule must be stated.
36. Leading/trailing whitespace on the header id value → passes if trimmed, otherwise flagged as a mismatch.
37. Id empty or the field missing in filename and/or header → fails.
38. Total id length wrong even though fields look right → fails.
39. Id correct in every field → passes.
40. Filename id valid, header id identical → passes.
41. Filename id valid, header id missing → fails: the entry's id is not in the header.
42. Filename id valid, header id malformed → fails.
43. Filename id malformed, header id valid → fails.
44. Filename id and header id both valid but different → fails: one entry carries two ids / name and header disagree.
45. Filename id and header id differ only by case or whitespace → fails or is normalized, per the case/trim rule.
46. Id date matches the day the entry file was written → passes.
47. Id date is one day after the write date → fails the "day it is written" clause if an authoritative timestamp exists.
48. Id date is one day before the write date → fails the same clause; timezone ambiguity must be resolved.
49. Entry written 23:59 local where UTC is already the next day and the id uses UTC → spec gap: which clock is authoritative.
50. Entry written just after local midnight with the previous day's id → fails under a local-date rule.
51. Entry written on 1 January whose id carries the previous year → fails under a local-date rule.
52. Id date matches the header's recorded date but not the filesystem/git date → spec gap: which date the checker may trust.
53. Id date is in the future relative to the checker's clock → fails as not the write date, unless clock granularity explains it.
54. Very old entry with a valid-shape id from a previous format era → passes on form; retroactive W1.1 needs a grandfathering rule.
55. One entry in the folder → passes.
56. Two entries with the same id and different slugs → fails: shared id.
57. Two entries with the same id that would produce identical filenames → fails; git cannot hold both names.
58. Two entries with the same id in different subfolders → fails if the checker's scope is the whole tree; passes if scope is one folder — spec gap.
59. Two filenames share an id but their header ids differ → fails: shared filename id.
60. Two headers share an id but their filename ids differ → fails: shared header id.
61. Two ids differ only in the random part → passes: distinct ids.
62. Two ids differ only in the date part → passes: distinct ids, and neither is "the next free number".
63. Two branches pick different random parts on the same date → passes after merge.
64. Two branches pick the same date and the same six random characters → fails after merge: collision.
65. Two branches pick the same full id and the same slug → fails: filename collision at merge.
66. A rebase reproduces one branch's id on top of the other's → same as a collision; fails.
67. Duplicate id exists only on an unmerged branch → checker on that branch fails, checker on main passes; the rule's scope over branches must be stated.
68. A duplicate existed in history but one file was later deleted → current tree has one id; whether historical sharing counts is a spec gap.
69. An id is reused after its original entry is deleted → currently unique; whether reuse is forbidden is a spec gap.
70. A copied file left beside the original keeps the same id → fails: duplicate.
71. A backup or temp file in the folder contains a second copy of the id → fails if scanned, ignored if the checker filters extensions; the filter must be stated.
72. Duplicate id where one file is a symlink to the other → one logical entry or two? spec gap; likely counted once.
73. Duplicate id where the two files have different prefixes → fails: the prefix does not make the id distinct.
74. Three or more entries sharing one id → fails, and the report must list every member.
75. Duplicate id where both occurrences are malformed → both fail on form; the duplicate is secondary.
76. Duplicate id where one is valid and one malformed → both findings: the malformed one on form, the pair on near-collision.
77. Rename with the id unchanged and only the slug edited → not one of the three named failures, but it breaks "the file keeps its name" — spec gap.
78. Rename with the id unchanged and only the prefix changed → same gap.
79. File renamed to a different valid id → fails.
80. File renamed to a malformed id → fails on rename-to-different-id and on form.
81. Id changed in both filename and header, git shows R100 → fails.
82. Id changed in the filename only, header keeps the old id → fails on rename and on filename/header mismatch.
83. Id changed in the header only, filename keeps the old id → fails: the entry's id changed.
84. Id edited in place with no rename (same filename, header changed) → fails "an id never changes".
85. Git shows delete + add (similarity below the rename threshold) with a different id → fails if the checker reads history/content, not only `git status`.
86. Rename A→B→A over two commits → a head-only check passes and a history check fails — spec gap: which is authoritative.
87. A revert restores the old id after a rename → the id changed in between; same gap as A→B→A.
88. A squash merge collapses the rename commits → history may show only the final name; the check must not depend on commit granularity.
89. A rebase or force-push rewrites the rename → same as 88.
90. A rename is staged but not committed → the index shows R and the tree shows the new name; the checker must state whether it reads index or tree.
91. A rename is in the working tree, unstaged → git shows delete + untracked; a filesystem-only checker sees only the new file.
92. Entry moved to another folder with the id unchanged → passes: not an id change.
93. Entry moved to another folder with a different id → fails.
94. A copy with a new id, original kept → a distinct entry; passes if the new id is unique and well-formed.
95. A copy keeping the old id, original kept → fails: duplicate.
96. Case-only rename on a case-insensitive filesystem → an uppercase id fails form.
97. Shallow clone with no history → the rename rule is "not checkable", not a silent pass.
98. Folder not under git → the rename rule is not checkable and must be reported as skipped.
99. Git rename detection disabled or threshold changed → the checker must compare ids itself rather than trust `git status`.
100. A merge-conflict resolution renames a file → treated as any rename.
101. History rewritten by filter-repo/filter-branch → a changed id must still be compared with the original.
102. A symlink is retargeted from one entry to another → an id change by indirection; spec gap.
103. File deleted and re-added with the same id → passes: the id did not change.
104. File deleted and re-added with a different id → fails if history is checked; a head-only check passes — same gap as A→B→A.
105. Entry renamed to a different id but git records a same-content delete/add → only content/history comparison catches it.
106. Filename is `<prefix>-<id>-<slug>.md` and the header id matches → passes.
107. Filename missing the prefix → outside the id rule; a naming violation, reported if naming is in scope.
108. Filename missing the slug or with an empty slug → same.
109. Slug contains hyphens → passes; the parser must key on the fixed id shape, not split on hyphens.
110. Slug contains a substring that itself looks like an id → passes; the parser must anchor on the real id, not report a phantom id.
111. Prefix contains digits and hyphens that look like date/random fields → passes; the parser must not misidentify a prefix fragment as the id.
112. Prefix is empty so the filename begins `-<id>-<slug>.md` → naming gap.
113. Slug contains uppercase, spaces or non-ASCII → outside the id rule; naming gap.
114. Extension `.MD` or `.markdown` → the checker's extension filter decides; must be stated, not silently skipped.
115. Non-Markdown file placed in the folder → skipped by the filter or flagged; must be stated.
116. Editor or hidden files (`.foo.md`, `foo.md~`, `.foo.md.swp`, `.#foo.md`) → must be ignored to avoid false positives.
117. Entry nested in a subdirectory → scanned or not per the recursion rule; must be stated.
118. Empty memory folder → no violations.
119. Folder contains only directories → no violations.
120. A directory whose name matches the entry-file pattern → must be ignored.
121. Entry file is a symlink → followed or not, as stated; following can create a duplicate false positive.
122. Entry file is unreadable → the checker reports an error for it and still checks the rest.
123. Header id in YAML front matter (`id: <id>`) → passes.
124. Header id as inline bold, an HTML comment, or a table cell → passes only if the parser supports it, else a real id is missed.
125. Header id quoted (`id: "13-10-k3f7a2-2026"`) → passes if quotes are stripped.
126. Header id with a trailing comment (`id: <id> # note`) → passes if the comment is stripped, else a false violation.
127. Two `id:` fields with the same value → ambiguous header; duplicate field must be flagged or accepted — spec gap.
128. Two `id:` fields with different values → fails.
129. Field name written `ID:` or `Id:` → passes only if the parser is case-insensitive, otherwise missed.
130. The id string also appears in the body as an example or cross-reference → must not count; the checker reads only the header.
131. Header uses CRLF line endings → must parse the same as LF.
132. File begins with a UTF-8 BOM → must parse the same as without.
133. Header id has leading/trailing spaces or tabs → the trim rule must be stated.
134. The id value is split across two lines → not found; fails.
135. The id is wrapped in backticks or markdown emphasis → passes only if markup is stripped.
136. Header is absent entirely → fails.
137. Header is truncated or malformed → fails with a parse error, not a silent pass.
138. Header id valid but the body's stated creation date disagrees with the id date → spec gap: which is authoritative.
139. One form violation → the checker exits nonzero and names the file and the rule.
140. One duplicate → exits nonzero and names both files.
141. One rename-to-different-id → exits nonzero and names the old and new ids.
142. No violations → exits zero with a clean report.
143. The checker is run twice on the same folder → identical result (idempotent).
144. Output names the violated rule and every offending file → required for verifiability.
145. One unreadable file among many → that file's error is reported and the others are still checked.
146. A file is being written during the scan → partial header; the checker retries or reports, never a false pass.
147. A very large folder → completes or reports a stated limit; no silent truncation.
148. Folder not under git during the run → the rename rule is skipped with a stated reason.
149. Shallow clone during the run → the rename rule is skipped with a stated reason.
150. Unborn branch / no commits → the rename rule is skipped with a stated reason.
151. `git` rename detection disabled by config → the checker must not silently pass.
152. The checker's regex is anchored to the full id → no partial-match false positives.
153. The checker's regex is unanchored → a 7-character random part can be accepted as 6; a false negative.
154. The checker's regex allows uppercase or wrong lengths → false negatives; this test must fail the checker.
155. The checker case-folds before comparing → an uppercase id wrongly passes; this test must fail the checker.
156. The checker trims whitespace before validating → a padded id passes; the stated trim rule decides.
157. The checker normalizes Unicode → a lookalike id passes; safe only if the `[a-z0-9]` alphabet is enforced after normalization.
158. The checker's date validation uses a different timezone than the writer → a valid id may be flagged; the timezone must be pinned.
159. The checker does no calendar validation → `32-13-...` passes; this test must fail the checker if calendar validity is required.
160. The checker's locale changes letter casing (e.g., Turkish `I`) → only matters where uppercase appears; test with a locale set.
161. One file has both a malformed id and a duplicate → both findings are reported; neither hides the other.
162. Duplicates are grouped so every member is listed → required for verifiability.
163. A filename/header id mismatch is reported as its own finding → required.
164. Git rename detection is restricted to entry files → other repo renames create no false positives.
165. A prefix or slug rename is not reported as an id change when the id bytes are unchanged → required.
166. A delete+add with the same id is not reported as a rename-to-different-id → required.
167. Rename comparison is on ids, not paths → a folder move with the same id passes.
168. Paths with spaces or non-ASCII → files still resolve and are checked.
169. The checker follows `.git` internals or ignored files → must not; otherwise false positives.
170. Windows path separators and CRLF → the same findings as on Linux.
171. A filename longer than the OS limit or otherwise unreadable → an error is reported.
172. Random part drawn uniformly from `[a-z0-9]` → passes.
173. Random part drawn from a biased or narrow alphabet → form-valid; the checker cannot judge randomness.
174. Random part generated as a counter (`000001`, `000002`) → form-valid but violates "never the next free number"; only policy review detects it, not the checker.
175. Random part derived from hostname or timestamp → predictable; form-valid, not shape-detectable.
176. Random part generated uppercase then lowercased → collisions possible after folding; the uniqueness check catches them.
177. Two branches seed the same RNG identically → the same random part on the same date → collision; fails.
178. Random part truncated by an off-by-one → 5 or 7 characters; fails form.
179. A collision is retried with a fresh random part → the new entry's id is unique; passes.
180. A writer hand-edits an existing id to "fix" it → the id changed; fails.
181. A writer chooses the next free number after reading other entries → may pass form while violating the intent; flagged.
182. A writer copies another entry as a template and forgets to re-randomize → duplicate; fails.
183. An id generated once is reused for a second entry on the same date → duplicate; fails.
184. Two entries written on the same day with independent random parts → both pass.
185. An entry written on a different day carries a different date prefix → passes; the date prefix is not a sequence.
186. Two branches edit the same entry and one changes the id → fails on the id change.
187. Two branches rename the same entry to two different ids → at least one id is lost; fails.
188. One branch deletes an entry and another keeps it → no duplicate; the id is simply retired.
189. A branch adds an id that main later also used → merge collision; fails.
190. The memory folder itself is moved in a branch → ids unchanged; passes, and the checker must be pointed at the new root.
191. `.gitattributes` line-ending normalization changes header bytes → parsing must survive, else a false failure.
192. Git LFS/smudge leaves the header unexpanded on checkout → the checker reports a parse failure, not a pass.
193. Sparse checkout omits some entries → duplicates may be hidden; the checker must state its scope.
194. The memory folder is a submodule → history checks must run inside the submodule.
195. Two worktrees check out the same branch → running the checker in both finds no new violation.
196. W1.1 is revised to a longer random part → old ids either keep passing under a grandfather rule or start failing; must be stated.
197. A two-digit year appears elsewhere in the name but not in the id → only the id fields are checked; passes.
198. The id appears in a link or anchor in another file → not an entry id; the checker reads entry files only.
199. A file with a valid id has an empty body → passes; the rule constrains the id, not the content.
200. The entry is written but not yet committed → a working-tree checker passes; git-based rename checks have no commit to compare.
