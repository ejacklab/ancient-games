#!/usr/bin/env python3
"""build.py — render content/ancients.json into one self-contained dist/index.html.

Every Markdown field is rendered to HTML here, at build time, with markdown-it-py, so the page
needs no library at runtime: the only thing it fetches from outside is the Google Fonts stylesheet
(N2). The look — theme colours, fonts, sizes, spacing, margins, alignment, the quiet bars and the
"Aa" menu in localStorage — is the kindle-page skill's; templates/style.css and templates/app.js
are that template's CSS and JS, reshaped for a row of four vertical panels instead of one column
of pages. Templates hold the shell; this file fills it from the data.
"""
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

from markdown_it import MarkdownIt

HERE = Path(__file__).resolve().parent
CONTENT = HERE / "content" / "ancients.json"
TEMPLATES = HERE / "templates"
DIST = HERE / "dist"

MD = MarkdownIt("commonmark", {"html": False, "typographer": True}).enable(["table", "strikethrough"])

LINK_START = re.compile(r"\[([^\]\n]*)\]\(")

KIND_ORDER = ("mindset", "decision rule", "algorithm")

WHO_NOTE = ("From the first research round; its Chinese quotes were checked, its other facts were not re-checked.")

DEFAULTS = {"theme": "sepia", "font": "literata", "size": 18, "leading": "normal", "margin": "normal", "align": "justify"}

SETTINGS = (
    ("font", "Font", (("literata", "Literata"), ("georgia", "Georgia"), ("sans", "Sans"), ("hyper", "Hyperlegible"))),
    ("size", "Size", tuple((size, str(size)) for size in (14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 32))),
    ("leading", "Spacing", (("compact", "Compact"), ("normal", "Normal"), ("loose", "Loose"))),
    ("margin", "Margins", (("narrow", "Narrow"), ("normal", "Normal"), ("wide", "Wide"))),
    ("align", "Alignment", (("justify", "Justify"), ("left", "Left"))),
    ("theme", "Page colour", (("white", "White"), ("sepia", "Sepia"), ("green", "Green"), ("black", "Black"))),
)


def references(text: str) -> str:
    """Write `[label](address)` as `label (address)`.

    For prose, where a citation is read in the sentence rather than tapped: an address behind a tap
    would leave the field's own words off the page. Written before markdown-it sees the text, so the
    address stays spelled as the field spells it. Items keep markdown-it's links: there the address
    is a separate line's business, and the item's own letters are what the item shows.
    """
    out, i = [], 0
    while True:
        found = LINK_START.search(text, i)
        if not found:
            out.append(text[i:])
            return "".join(out)
        out.append(text[i:found.start()])
        depth, k = 1, found.end()
        while k < len(text) and depth:
            depth += {"(": 1, ")": -1}.get(text[k], 0)
            k += 1
        if depth:
            out.append(text[found.start():])
            return "".join(out)
        out.append(f"{found.group(1)} ({text[found.end():k - 1]})")
        i = k


def number_ordered_lists(tokens: list) -> None:
    """Put an ordered list's own numbers into its items as text, and drop the CSS list markers.

    A generated marker is not in the page's text, so the digits of "1. 2. 3." would exist in the
    field and not on the page (R5.1). `<ol class="plain">` still counts the items for a screen
    reader; it just does not draw a second number next to the one that is text.
    """
    open_lists: list[list[int] | None] = []
    for i, token in enumerate(tokens):
        if token.type == "ordered_list_open":
            start = int(token.attrGet("start") or 1)
            open_lists.append([start, start - 1])
            token.attrSet("class", "plain")
        elif token.type == "bullet_list_open":
            open_lists.append(None)
        elif token.type in ("ordered_list_close", "bullet_list_close"):
            open_lists.pop()
        elif token.type == "list_item_open" and open_lists and open_lists[-1]:
            open_lists[-1][1] += 1
            number = f"{open_lists[-1][1]}. "
            for token2 in tokens[i + 1:]:
                if token2.type == "inline" and token2.children and token2.children[0].type == "text":
                    token2.children[0].content = number + token2.children[0].content
                    break
                if token2.type in ("paragraph_close", "list_item_close"):
                    break


def block(text: str) -> str:
    tokens = MD.parse(text or "")
    number_ordered_lists(tokens)
    return MD.renderer.render(tokens, MD.options, {})


def prose(text: str) -> str:
    """A field of running prose (the biography), where a citation is read rather than tapped: the field's
    own letters have to be on the page, and its `[label](address)` keeps both."""
    tokens = MD.parse(references(text or ""))
    number_ordered_lists(tokens)
    return MD.renderer.render(tokens, MD.options, {})


def inline(text: str) -> str:
    return MD.renderInline(text or "")


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def validate(persons: list[dict]) -> None:
    problems = []
    for person in persons:
        for key in ("id", "name", "items"):
            if not person.get(key):
                problems.append(f'{person.get("id", "?")}: no {key}')
        if not str(person.get("who", {}).get("markdown", "")).strip():
            problems.append(f'{person.get("id", "?")}: no who')
        for item in person.get("items", []):
            for key in ("n", "title", "kind_tag", "rule", "words", "source", "label"):
                if item.get(key) in (None, ""):
                    problems.append(f'{person["id"]}#{item.get("n", "?")}: no {key}')
            if item.get("kind_tag") not in KIND_ORDER:
                problems.append(f'{person["id"]}#{item.get("n", "?")}: kind {item.get("kind_tag")!r}')
        if not kinds_line(person.get("items", [])):
            problems.append(f'{person.get("id", "?")}: no kinds')
    if problems:
        raise SystemExit("content/ancients.json is not shaped like docs/blueprint/06-data-model.md:\n  "
                         + "\n  ".join(problems))


def kinds_line(items: list[dict]) -> str:
    counts = Counter(item.get("kind_tag") or item.get("kind") or "" for item in items)
    parts = [f"{n} {kind}{'' if n == 1 else 's'}" for kind in KIND_ORDER if (n := counts.get(kind, 0))]
    return " · ".join(parts)


def item_html(item: dict) -> str:
    return (
        f'<article class="item" data-n="{esc(item["n"])}">'
        f'<span class="kind">{esc(item["kind_tag"])}</span>'
        f"<h3>{inline(item['title'])}</h3>"
        f'<div class="rule">{block(item["rule"])}</div>'
        f'<blockquote class="words">{block(item["words"])}</blockquote>'
        f'<p class="source">{inline(item["source"])}</p>'
        f'<p class="label">{inline(item["label"])}</p>'
        "</article>"
    )


def person_html(person: dict) -> str:
    items = "".join(item_html(item) for item in person["items"])
    return (
        f'<section class="person" data-person="{esc(person["id"])}">'
        f'<h1 class="person-name">{esc(person["name"])}</h1>'
        f'<p class="kinds">{esc(kinds_line(person["items"]))}</p>'
        f'<div class="who">{prose(person["who"]["markdown"])}</div>'
        f'<p class="who-note">{esc(WHO_NOTE)}</p>'
        f"{items}"
        '<p class="pct">0%</p>'
        "</section>"
    )


def menu_html() -> str:
    rows = []
    for setting, label, options in SETTINGS:
        buttons = []
        for value, text in options:
            chosen = ' class="on"' if str(DEFAULTS[setting]) == str(value) else ""
            buttons.append(f'<button type="button" data-setting="{setting}" data-value="{esc(value)}"{chosen}>{esc(text)}</button>')
        rows.append(f'<div class="row"><label>{esc(label)}</label><span class="opts">{"".join(buttons)}</span></div>')
    return '<div class="head"><h2>Aa — Display</h2><button id="done" type="button">Done</button></div>' + "".join(rows)


def header_html(persons: list[dict]) -> str:
    dots = []
    for i, person in enumerate(persons):
        chosen = ' class="on"' if i == 0 else ""
        dots.append(f'<button type="button" data-goto="{i}" aria-label="{esc(person["name"])}"{chosen}></button>')
    return (
        f'<div class="line"><span id="person-name">{esc(persons[0]["name"])}</span>'
        f'<span id="person-pos">1 / {len(persons)}</span></div>'
        f'<div class="line"><nav id="dots">{"".join(dots)}</nav>'
        f'<button id="aa" type="button" aria-haspopup="true" aria-controls="menu" aria-expanded="false">Aa</button></div>'
    )


def build() -> Path:
    data = json.loads(CONTENT.read_text(encoding="utf-8"))
    persons = data["persons"]
    validate(persons)
    page = (TEMPLATES / "page.html").read_text(encoding="utf-8")
    style = (TEMPLATES / "style.css").read_text(encoding="utf-8")
    script = (TEMPLATES / "app.js").read_text(encoding="utf-8")

    defaults = json.dumps(DEFAULTS, ensure_ascii=False).replace("<", "\\u003c")
    script = script.replace("__DEFAULTS__", defaults)
    out = page
    for token, value in (
        ("__TITLE__", esc(data["title"])),
        ("__LANG__", "en"),
        ("__STYLE__", style),
        ("__HEADER__", header_html(persons)),
        ("__PEOPLE__", "".join(person_html(p) for p in persons)),
        ("__MENU__", menu_html()),
        ("__SCRIPT__", script),
    ):
        out = out.replace(token, value)

    left = [t for t in ("__TITLE__", "__STYLE__", "__HEADER__", "__PEOPLE__", "__MENU__", "__DEFAULTS__", "__SCRIPT__") if t in out]
    if left:
        raise SystemExit(f"template placeholder left unfilled: {', '.join(left)}")

    DIST.mkdir(parents=True, exist_ok=True)
    target = DIST / "index.html"
    target.write_text(out, encoding="utf-8")
    print(f"wrote {target} ({len(out):,} bytes): " + ", ".join(f"{p['id']} {len(p['items'])}" for p in persons))
    return target


if __name__ == "__main__":
    sys.exit(0 if build() else 1)