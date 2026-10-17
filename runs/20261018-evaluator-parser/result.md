# Result — the evaluator's parser reads the paragraph form (DATA.md E1 rule 9)

**Status: done.** `tools/evaluator/spec_parse.py` reads the paragraph form beside the bullet form, so
`tests/test_evaluator_spec_parse_paragraph.py` passes and every other evaluator test still does.

## What changed in `spec_parse.py`

- **Three new patterns.** `HEADING_GROUP` (`## <group> — <title>`, U+2014, group without a `.n` part),
  `PARAGRAPH_START` (`**<id>` then a space or the bold's own `**`, at column 0) and `FAILS_IF_IN_TEXT`
  (`**Fails if**`, `**Fails if:**`, plain `Fails if:`), which `_starts_fails_if` matches at the start of a
  paragraph and `_paragraph_fails_if` searches anywhere inside one.
- **Four new helpers.** `_paragraph` (lines up to the blank line, joined by one space), `_starts_fails_if`,
  `_paragraph_fails_if` (the text from the marker to the paragraph's end), `_paragraph_title` (the rest of the
  bold, which titles a group of its own) and `_new_group` (the group dict the group-heading branch now uses too).
- **`_read_groups` has one more branch.** An `#` heading either opens a heading group or closes the open one; a line
  that begins nothing else and starts with `**<id>` or a **Fails if** marker is read as a paragraph. The paragraph's
  id joins the open heading group, or makes a group of its own named after the id when no heading group is open;
  rule 5 reads the whole paragraph; a **Fails if** inside it goes to that group. A heading group is made when its
  first paragraph lands in it, so a heading over bullets adds no group of its own.
- **Nothing else.** The bullet branch (rules 1–5, `unparsed_ids`) is the code that was there, indented into the
  branch it now shares the loop with. `parse()` of the four rule 1–8 fixtures is byte-identical to the previous
  version's, compared as JSON against `git show HEAD:tools/evaluator/spec_parse.py`. Stdlib only.

## The command's last lines

```
$ python3 -m pytest -q tests/test_evaluator_*.py
........................................................................ [ 39%]
........................................................................ [ 78%]
........................................                                 [100%]
184 passed in 39.98s
```

## CONTRADICTS

- Rule 9: *"A heading line `#… <group> — <title>` … opens group `<group>`; the requirement paragraphs after it belong
  to it. Any other heading closes it."* — read literally, it cannot be met beside rules 1–8.
  `tests/fixtures/evaluator/index-md-REQUIREMENTS.md` (rule 1–8, frozen at 10 groups) holds exactly those headings:
  `## B — Build: from entries to \`INDEX.md\``, `## C — Check: …`, `## G — Git: …`, each above bold groups of
  bullets. Opening a group on the heading adds three empty groups (B, C, G) and breaks the frozen count, and nothing
  in rule 9 says a heading group with no requirement paragraph may not exist.
  **Resolution taken:** the heading names the group, and the group is made when its first paragraph lands in it — a
  heading that holds no requirement paragraph adds no group. `harness-REQUIREMENTS.md` (`## R11 — …`, `## R12 — …`,
  paragraphs under each) reads the same under either reading; `index-md-REQUIREMENTS.md` reads as rules 1–8 froze it.
  A one-line change to DATA.md — "a group only when a requirement paragraph lands in it" — would make the rule and
  this parser agree.