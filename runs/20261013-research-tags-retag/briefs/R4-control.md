# Brief — tag 143 research findings (pass C)

You are a classifier. One job: give each row in the sheet one tag, using only the definitions below and only what
the row itself says.

## Read only these two things

1. This brief.
2. The sheet: `rows.md` in the current directory — 146 rows, each `id | Finding | Source`.

Do not open, search or list any other file or folder, and do not use the web. You do not need anything
else, and other files would spoil the task.

## The definitions (quoted verbatim; use these and nothing else)

    Labels: verified = the primary document was read; reported = a secondary source; unknown = not settled;
    unproven = claimed without evidence.

Judge from the row: the Finding is the claim; the Source cell shows what was read (its URL, date and quote).

## Output

Print exactly 146 lines and nothing else — no heading, no commentary, no code fence. One JSON object per line, in
the sheet's order:

    {"id": "R001", "tag": "verified"}

`tag` is one of `verified`, `reported`, `unknown`, `unproven`.

## One example (not from the sheet)

Row: `| RX | The vendor's system is 60% faster. | https://vendor.example/blog (2026-01-01), quoted verbatim: "our system is 60% faster" |`
Line: `{"id": "RX", "tag": "verified"}` — the vendor's own blog, the primary document for this claim, was read.

## Standard (how your output is checked, by a script you cannot change)

146 lines; every id from the sheet exactly once; every tag one of the four. A missing id, an extra line, or any
other word fails the check.
