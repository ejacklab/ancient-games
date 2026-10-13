#!/usr/bin/env python3
"""check_content.py — R5.2: is content/ancients.json a faithful copy of its sources?

Checks, per person: the schema (06-data-model.md); 1-20 items; every item field non-empty and its kind one of the
three; every text field a whitespace-normalised substring of its source .md (catches any rewording); every Chinese
clause in "their words" found in runs/20261013-four-seats/sources/<id>/ (variant characters and the wiki's
commentary markup normalised). Exit 0 when all pass, 1 otherwise, with one line per failure.

What it does not establish: that a quote is attributed to the right speaker, or that a gloss or rule reads its words
fairly — those were the reviews' job in run 20261013-four-seats.

Usage: check_content.py [content/ancients.json] [--repo DIR] [--sabotage]
  --sabotage  alter one character of one quote in memory and require the check to fail (proves it can fail)
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
KINDS = {"decision rule", "mindset", "algorithm"}
ITEM_KEYS = ("n", "title", "kind", "rule", "words", "source", "label", "from", "kind_tag")
# Names of editions that appear inside "their words" as labels, not as quotes.
EDITION_NAMES = {"十一家注"}
VARIANTS = str.maketrans("吴彊爲裏於无亓恆脩塡胜饑倶", "吳強為裡于無其恒修填勝飢俱")


def ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def cjk(s: str) -> str:
    s = re.sub(r"\{\{[^{}]*?\|([^{}|]*)\|[^{}]*\}\}", r"\1", s)  # {{另|詬|垢}} → 詬
    s = re.sub(r"\{\{\*\|.*?\}\}|-\{|\}-", "", s, flags=re.S)
    return re.sub(r"[^㐀-鿿]", "", s).translate(VARIANTS)


def source_texts(folder: Path) -> list[str]:
    """Each source twice: the main text, and the text with its commentary notes kept (the lists quote 韋昭, 王弼 and
    the 十一家注 as commentary, labelled as such)."""
    out = []
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix in (".txt", ".html", ".htm", ".rst"):
            raw = p.read_text(encoding="utf-8", errors="ignore")
            out += [cjk(raw), re.sub(r"[^\u3400-\u9fff]", "", raw).translate(VARIANTS)]
    return out


def check(doc: dict, repo: Path) -> list[str]:
    bad = []
    persons = doc.get("persons")
    if not isinstance(persons, list) or len(persons) != 4:
        return ["schema: persons must be a list of 4"]
    for p in persons:
        pid = p.get("id", "?")
        for key in ("id", "name", "who", "list_source", "items"):
            if not p.get(key):
                bad.append(f"{pid}: missing {key}")
        items = p.get("items") or []
        if not 1 <= len(items) <= 20:
            bad.append(f"{pid}: {len(items)} items, want 1-20")
        lst = ws((repo / p.get("list_source", "")).read_text(encoding="utf-8")) if p.get("list_source") else ""
        bio = ws((repo / p["who"]["source"]).read_text(encoding="utf-8")) if p.get("who") else ""
        if p.get("who") and ws(p["who"].get("markdown", "")) not in bio:
            bad.append(f"{pid}: 'who' is not a verbatim copy of {p['who']['source']}")
        srcs = source_texts(repo / "runs" / "20261013-four-seats" / "sources" / pid)
        for it in items:
            n = it.get("n", "?")
            for key in ITEM_KEYS:
                if it.get(key) in (None, ""):
                    bad.append(f"{pid} #{n}: empty {key}")
            if it.get("kind_tag") not in KINDS:
                bad.append(f"{pid} #{n}: kind_tag {it.get('kind_tag')!r} not one of {sorted(KINDS)}")
            for key in ("title", "kind", "rule", "words", "source", "label", "from"):
                if it.get(key) and ws(it[key]) not in lst:
                    bad.append(f"{pid} #{n}: {key} is not a verbatim copy of the list: {ws(it[key])[:60]!r}")
            # each unbroken run of Chinese characters, split at Chinese punctuation, is one clause
            for clause in re.findall(r"[\u3400-\u9fff]+", it.get("words", "")):
                if clause in EDITION_NAMES:
                    continue
                c = clause.translate(VARIANTS)
                if len(c) >= 4 and not any(c in t for t in srcs):
                    bad.append(f"{pid} #{n}: Chinese clause not found in sources/{pid}/: {clause.strip()[:30]}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("content", nargs="?", default=str(HERE / "content" / "ancients.json"))
    ap.add_argument("--repo", default=str(HERE.parent.parent))
    ap.add_argument("--sabotage", action="store_true")
    a = ap.parse_args()
    doc = json.loads(Path(a.content).read_text(encoding="utf-8"))
    repo = Path(a.repo)
    if a.sabotage:
        broken = copy.deepcopy(doc)
        it = next(i for p in broken["persons"] for i in p["items"] if re.search(r"[一-鿿]{4}", i["words"]))
        m = re.search(r"[一-鿿]{4}", it["words"])
        it["words"] = it["words"][:m.start() + 1] + "鑫" + it["words"][m.start() + 2:]
        found = check(broken, repo)
        print(f"sabotage: altered one character in a quote → {len(found)} failure(s) reported")
        return 0 if found else 1
    bad = check(doc, repo)
    for b in bad:
        print("FAIL", b)
    total = sum(len(p.get("items") or []) for p in doc.get("persons", []))
    print(f"{'PASS' if not bad else 'FAIL'}: 4 persons, {total} items, {len(bad)} failure(s)")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
