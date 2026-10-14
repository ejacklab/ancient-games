#!/usr/bin/env python3
"""Move SOURCE_OF_TRUTH.md's requirements into SOURCE_OF_TRUTH_REQUIREMENTS.yaml, word for word, with levels."""
import re
import sys
import textwrap

import yaml

MD = sys.argv[1]
OUT = sys.argv[2]

LEVEL = {  # id -> level, or {level: what it covers} for an id split by clause
    "W1.1": {"MUST": "one file per entry; the prefix is one of the five and matches `kind`; kind and id never change; "
                     "ids are unique; the id is in the form `DD-MM-xxxxxx-YYYY`",
             "SHOULD": "the folder and the `-<slug>.md` spelling of the file name"},
    "W1.2": "SHOULD",
    "W1.3": {"MUST": "the `**Why:**` line; one claim per entry",
             "SHOULD": "the `**How to apply:**` line, the order of the sections and the sentence count"},
    "W2.1": {"guidance": "the definitions", "SHOULD": "decisions and facts are written before the code"},
    "W2.2": {"guidance": "the definitions", "SHOULD": "a hypothesis is labelled as one"},
    "W3.1": "SHOULD", "W3.2": "MUST",
    "W3.3": {"MUST": "nothing from another agent's private state", "SHOULD": "no raw transcripts"},
    "W3.4": "SHOULD",
    "W3.5": {"MUST": "no user memory and no agent memory in the project", "SHOULD": "both live in the home folder"},
    "W3.6": "SHOULD",
    "W4.1": {"guidance": "anyone may create or change any entry; no owner and no approval",
             "MUST": "`status` is only `active`, `superseded` or `retired`; the Rd5.3 exception"},
    "W4.2": "SHOULD", "W4.3": "guidance",
    "W5.1": "SHOULD", "W5.2": "SHOULD",
    "W5.3": {"SHOULD": "adding `done:`", "MUST": "a mismatch is reported, not settled in `done:`"},
    "W6.1": {"MUST": "each new entry gets its own file; agents never append to one shared file",
             "SHOULD": "one journal file per agent session"},
    "W6.2": "SHOULD",
    "W6.3": {"MUST": "whoever merges keeps both sides, both `changed:` lines and both links; nobody chooses between "
                     "two claims; two entries superseding one are reported",
             "SHOULD": "a conflict in `INDEX.md` is resolved by regenerating it"},
    "K1.1": "SHOULD",
    "K4.1": "MUST", "K4.2": "guidance", "K4.3": "MUST",
    "K5.1": "SHOULD", "K5.2": "SHOULD",
    "K6.1": {"MUST": "`INDEX.md` equals what the tool builds: one line per active entry, with its id, kind and claim",
             "SHOULD": "it is generated, never edited by hand"},
    "K6.2": "MUST",
    "K6.3": {"MUST": "no conflict markers are left in the entry files",
             "SHOULD": "`INDEX.md` is regenerated, never merged by hand"},
    "Rd1.1": "SHOULD", "Rd1.2": "MUST",
    "Rd2.1": "SHOULD", "Rd2.2": "SHOULD",
    "Rd2.3": {"MUST": "credentials; another agent's transcripts", "SHOULD": "the other four"},
    "Rd3.1": {"MUST": "`INDEX.md` fits the strictest limit, and the K6 check fails when it does not",
              "guidance": "the example numbers"},
    "Rd4.1": "MUST", "Rd4.2": "guidance", "Rd4.3": "guidance", "Rd4.4": "SHOULD",
    "Rd4.5": {"guidance": "an agent may read another agent's memory",
              "SHOULD": "it treats it as that agent's memory and says whose it is"},
    "Rd5.1": "MUST", "Rd5.2": "MUST", "Rd5.3": "MUST", "Rd5.4": "guidance", "Rd5.5": "guidance",
    "Rd6.1": "MUST",
}

CAT = re.compile(r"^### (.+)$")
SEC = re.compile(r"^\*\*([A-Z][a-z]?\d) — (.+?)\*\* \((.+)\)$")
REQ = re.compile(r"^- \*\*([A-Z][a-z]?\d\.\d)\*\* (.*)$")
FAILS = re.compile(r"^- \*\*Fails if\*\* (.*)$")


def parse(lines):
    cats, cur_item = [], None
    for raw in lines:
        line = raw.rstrip("\n")
        if m := CAT.match(line):
            cats.append({"title": m.group(1), "groups": []})
        elif m := SEC.match(line):
            cats[-1]["groups"].append({"id": m.group(1), "title": m.group(2), "basis": m.group(3),
                                       "requirements": [], "fails_if": ""})
        elif m := REQ.match(line):
            cur_item = {"id": m.group(1), "text": m.group(2), "items": []}
            cats[-1]["groups"][-1]["requirements"].append(cur_item)
        elif m := FAILS.match(line):
            cur_item = cats[-1]["groups"][-1]
            cur_item["fails_if"] = m.group(1)
            cur_item = ("fails", cur_item)
        elif line.startswith("  - "):
            cur_item["items"].append(line[4:])
        elif line.startswith("    ") and cur_item and not isinstance(cur_item, tuple) and cur_item["items"]:
            cur_item["items"][-1] += " " + line.strip()
        elif line.startswith("  ") and cur_item:
            if isinstance(cur_item, tuple):
                cur_item[1]["fails_if"] += " " + line.strip()
            else:
                cur_item["text"] += " " + line.strip()
        elif line.strip() == "":
            continue
        else:
            raise SystemExit(f"unparsed line: {line!r}")
    return cats


def block(key, text, indent):
    pad = " " * indent
    body = textwrap.wrap(text, 118 - indent - 2, break_long_words=False, break_on_hyphens=False)
    return [f"{pad}{key}: >-"] + [f"{pad}  {b}" for b in body]


def scalar(value):
    return yaml.safe_dump(value, width=1000, allow_unicode=True).strip().removesuffix("\n...")


def emit(cats):
    out = [
        "# Source-of-Truth Memory — requirements",
        "#",
        "# The requirements of SOURCE_OF_TRUTH.md, which holds the design and why. Grouped by what happens to a memory:",
        "# it is written, it is kept true, and it is read. Each group has one check, fails_if, that some case breaks.",
        "# There are no fixed numbers: where a limit applies, it is a comparison that measurement decides.",
        "",
        "levels:",
        "  MUST: A gate. When it fails, the work stops.",
        "  SHOULD: A default. It may be skipped with a written reason.",
        "  guidance: Explanation or advice. Nothing to pass or fail.",
        "",
        "basis:",
        "  v: the vision, vision-statements/source-of-truth-memory-vision-statements.md",
        "  d: this design's text, SOURCE_OF_TRUTH.md (the section named)",
        "",
        "categories:",
    ]
    for c in cats:
        out += [f"  - title: {scalar(c['title'])}", "    groups:"]
        for g in c["groups"]:
            out += [f"      - id: {g['id']}", f"        title: {scalar(g['title'])}",
                    f"        basis: {scalar(g['basis'])}", "        requirements:"]
            for r in g["requirements"]:
                lv = LEVEL[r["id"]]
                out.append(f"          - id: {r['id']}")
                if isinstance(lv, str):
                    out.append(f"            level: {lv}")
                else:
                    out.append("            level:")
                    for k, v in lv.items():
                        out += block(k, v, 14)
                out += block("text", r["text"], 12)
                if r["items"]:
                    out.append("            items:")
                    for it in r["items"]:
                        out.append(f"              - {scalar(it)}")
            out += block("fails_if", g["fails_if"], 8)
    return "\n".join(out) + "\n"


def main():
    text = open(MD, encoding="utf-8").read()
    start = text.index("### Write — what goes in, and how")
    cats = parse(text[start:].splitlines())
    ids = [r["id"] for c in cats for g in c["groups"] for r in g["requirements"]]
    assert sorted(ids) == sorted(LEVEL), set(ids) ^ set(LEVEL)
    open(OUT, "w", encoding="utf-8").write(emit(cats))
    # round trip: every word of the Markdown requirements is in the YAML's text, items and fails_if
    data = yaml.safe_load(open(OUT, encoding="utf-8"))
    def words(s):
        return re.sub(r"\s+", " ", s).strip()
    for c, dc in zip(cats, data["categories"]):
        assert c["title"] == dc["title"]
        for g, dg in zip(c["groups"], dc["groups"]):
            assert (g["id"], g["title"], g["basis"]) == (dg["id"], dg["title"], dg["basis"]), g["id"]
            assert words(g["fails_if"]) == dg["fails_if"], g["id"]
            for r, dr in zip(g["requirements"], dg["requirements"]):
                assert words(r["text"]) == dr["text"], r["id"]
                assert [words(i) for i in r["items"]] == dr.get("items", []), r["id"]
    print(f"{len(ids)} requirements, {sum(len(c['groups']) for c in cats)} groups; round trip: text identical")


main()
