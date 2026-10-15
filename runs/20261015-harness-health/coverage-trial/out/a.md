1. A file named `<prefix>-13-10-k3f7a2-2026-<slug>.md` with the header id `13-10-k3f7a2-2026` → no violation.
2. Random part all digits, `13-10-012345-2026` → no violation.
3. Random part all lowercase letters, `13-10-abcdef-2026` → no violation.
4. Random part of 5 characters, `13-10-k3f7a-2026` → violation: not the W1.1 form.
5. Random part of 7 characters, `13-10-k3f7a2b-2026` → violation: not the W1.1 form.
6. Random part contains an uppercase letter, `13-10-K3F7A2-2026` → violation: not the W1.1 form.
7. Random part contains a non-alphanumeric character, `13-10-k3f7_2-2026` → violation: not the W1.1 form.
8. Day is not zero-padded, `3-10-k3f7a2-2026` → violation: not the W1.1 form.
9. Month is not zero-padded, `13-1-k3f7a2-2026` → violation: not the W1.1 form.
10. Year is two digits, `13-10-k3f7a2-26` → violation: not the W1.1 form.
11. Separators are wrong, `13/10/k3f7a2/2026` → violation: not the W1.1 form.
12. Day is `00`, `00-10-k3f7a2-2026` → violation: not a real writing date.
13. Day is `32`, `32-10-k3f7a2-2026` → violation: not a real writing date.
14. Month is `13`, `13-13-k3f7a2-2026` → violation: not a real writing date.
15. Date cannot exist, `31-02-k3f7a2-2026` → violation: not a real writing date.
16. Extra segment, `13-10-k3f7a2-2026-1` → violation: not the W1.1 form.
17. Missing segment, `13-10-2026` → violation: not the W1.1 form.
18. Id is empty → violation: not the W1.1 form.
19. Two files in the folder carry the same id → violation: duplicate id.
20. Two entries share an id, one in a filename and one only in a file header → violation: duplicate id.
21. Header id differs from the filename id → violation: the entry's id is not consistent/not in form.
22. Filename or header has no id at all → violation: no W1.1-form id.
23. `git` shows an entry file renamed to a name carrying a different id → violation: id changed on rename.
24. `git` shows the slug renamed but the id unchanged → no violation: the id is unchanged.
25. `git` shows the file modified with no rename → no violation.
26. A new id that does not follow the folder's previous id numerically, e.g. `13-10-k3f7a2-2026` when the newest existing id is `09-10-aaaaaa-2026` → no violation: ids are never "the next free number".
27. Two writers on different branches independently pick the same id and the branches are merged into one folder → violation: duplicate id.
28. The id's date differs from the date the entry was written → no violation from the three stated failures; the requirement does not cover this case.
