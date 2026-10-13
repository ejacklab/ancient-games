# Brief — tag 143 research findings (pass N)

You are a classifier. One job: give each row in the sheet a tag, using only the rules below and only what the row
itself says.

## Read only these two things

1. This brief, including the rules quoted in it.
2. The sheet: `rows.md` in the current directory — 146 rows, each `id | Finding | Source`.

Do not open, search or list any other file or folder, and do not use the web. You do not need anything
else, and other files would spoil the task.

## The rules (quoted verbatim from the project's one copy; use these and nothing else)

    ## The tags

    **Scope:** The researcher gives each research finding one tag. The tag describes the evidence the researcher has for the finding's exact wording. It is neither a confidence score nor a declaration of universal truth.

    **Primary and secondary are relative to that exact wording, not to the source's reputation.** One document is primary evidence for the claim that it says what it says. It is secondary for a claim about the world that it only reports. That is why the same blog can carry `verified` for one row and `unproven` for the next.

    **The four tags.** Each tag names one measure: the evidence in hand for the exact claim. The four are parallel answers to one question, not rungs of a ladder. Their order is not their strength, and no fifth tag (such as source rank) is added.

    | Tag | Definition |
    |---|---|
    | `verified` | The supporting evidence itself was inspected: the primary document's own measurements, data or wording. It directly supports the exact claim within its stated scope, and the row shows what was inspected. Merely reading an assertion does not qualify. |
    | `reported` | You read an account that gives a locator for where the claim comes from (a URL, a DOI, or the exact title), and you have not inspected that source. You do not yet know what evidence it holds. This holds whether the source could not be obtained or simply was not fetched. |
    | `unproven` | You read the claim, and nothing beyond the assertion is in hand: no evidence is shown, and no locator leads further. A primary source that asserts without evidence is `unproven`; so is an account that names no locator ("studies show", "the company says", "per the Smith paper"). |
    | `unknown` | Evidence bearing on the claim is in hand but does not settle it, in one of two ways: it conflicts and the conflict is unresolved, or it was inspected and neither supports nor contradicts the exact wording. One tag serves both; the reason goes in the row, not in the vocabulary. |

    **When two tags seem to fit:** First check whether the row contains two claims. Split a statement about what a source says from a statement about whether that assertion holds. Then tag each claim separately, each citing the same passage.

    For one claim, ask one question: what evidence is in hand for that exact wording? Source rank does not substitute for evidence, whether the asserting document is primary or secondary. What is in hand is one of these:

    - nothing beyond the assertion → `unproven`
    - an account that gives a locator for a source you have not inspected, whether or not you could get it → `reported`
    - the evidence itself, inspected and directly supporting the claim → `verified`
    - evidence in hand that conflicts unresolved, or that does not settle the exact wording → `unknown`, and state the unresolved point
    - evidence in hand that contradicts the claim → this is not a fifth tag. Write the finding as what the evidence shows, which is then `verified`. Keep the contradicted assertion as its own row with its own tag.

    **`reported` or `unproven`, for a secondhand account.** One question: **does the account give a locator** — a URL, a DOI, or the exact title of the source the claim comes from? Yes → `reported`. No → `unproven`. The locator may sit anywhere in the account (a footnote, a bibliography entry). An exact title is a title written out in full; a short name such as "the Smith paper" is not one. Nothing else is a locator, in any combination: an author's name, a venue, a year or a benchmark name, alone or together, is not one. What kind of source the locator leads to (a paper, a whitepaper, a README, a company post, a recording — anything) and the account's verb ("claims", "found", "shows") do not change the tag; what that source holds is learned only by inspecting it, and the inspection is a new finding with its own tag.

    Examples: "a 2025 arXiv paper (link) found +12% recall on LoCoMo" → `reported`. "The company says it is 60% faster" with a link to the company's post → `reported`; inspect the post, and if it shows no measurements, a new finding "the 60% claim has no evidence in its source" is `verified` and the claim itself stays `unproven`. "Per the Smith paper, latency drops 40%" → `unproven`. "Studies show it is faster" → `unproven`.

    A row saying what the account itself says ("the blog states X") is `verified`, and is written only when what the account said matters to the answer; the row the tag rules are for is the claim itself.

    Write each finding so that one row fits. If you cannot, it is two findings.

    **Never upgrade a label in place.** A finding's label is fixed once assigned. When later investigation inspects primary evidence, record a new finding that references the original; do not edit the earlier record.

    **The row must show what was inspected.** A `verified` row carries, in the row itself and not in a footnote, the wording, figure or file:line that was inspected. If a reader cannot see from the claim and its row what was looked at, the row is either two findings or not `verified`.

    For example, reading a vendor announcement supports a `verified` finding that the vendor made a performance claim, because the announcement's wording is the evidence for what it says. The performance claim itself is `unproven` if the announcement supplies no measurements, and `reported` if it gives a locator for a benchmark that was not inspected.

    `verified` does not imply independent replication. State whose evidence was inspected and the conditions it covers. A vendor's benchmark cannot establish performance outside its tested conditions.

    **Other finding types:** `INFERRED` and `GAP` are no longer choices in the trust-label field.

    - Write a researcher's deduction as inference prose that names its premise finding IDs and the reasoning.
    - Write an unsuccessful search as gap prose that names the question, the query and the places searched.
    - A search that found nothing is a gap, not a tag. Do not record absence as though it were evidence.
    - An inference does not inherit `verified` from its premises, and failing to find evidence does not show that something does not exist.
    - An inference or a gap is not a row in the findings table. It is prose, and it carries no trust tag.

    When sources disagree, keep separate findings with their own citations and tags. Describe the disagreement explicitly; do not average it away. An unresolved overall conclusion is `unknown`.

Judge from the row: the Finding is the claim; the Source cell shows what was read (its URL, date and quote). The
"you" in the rules is the researcher who wrote the row.

## Output

Print exactly 146 lines and nothing else — no heading, no commentary, no code fence. One JSON object per line, in
the sheet's order. Each line is one of three shapes:

    {"id": "R001", "tag": "verified"}
    {"id": "R002", "split": [{"part": "<the first claim, in a few words>", "tag": "verified"}, {"part": "<the second claim>", "tag": "unproven"}]}
    {"id": "R003", "stuck": ["reported", "unproven"], "why": "<one short sentence: why both still fit after splitting>"}

Use `split` when the rules say the row holds two claims. Use `stuck` only when, after splitting, one claim still fits
two tags and the rules do not decide between them. Tags: `verified`, `reported`, `unproven`, `unknown`.

## One example (not from the sheet)

Row: `| RX | The vendor's system is 60% faster. | https://vendor.example/blog (2026-01-01), quoted verbatim: "our system is 60% faster" |`
Line: `{"id": "RX", "split": [{"part": "the vendor's blog states 60% faster", "tag": "verified"}, {"part": "the system is 60% faster", "tag": "unproven"}]}`

## Standard (how your output is checked, by a script you cannot change)

146 lines; every id from the sheet exactly once; tags from the four; a split has at least two parts; a stuck names
two different tags and a reason. Anything else fails the check.
