"""Is every classical citation grounded in the notes?

Three earlier attempts at this each produced false positives, and each failure was instructive:

1. punctuation stripped from the citation but not the notes — `以正合以奇勝` missed `以正合，以奇勝`;
2. punctuation stripped from everything — every file collapsed into one run, so all 3 files "failed";
3. ellipsis treated as a separator — good, but set that aside *without* an ellipsis and the two halves merge into
   one run that matches nothing. Real quotation does this constantly: `知彼知己，百戰不殆；不知彼而知己，一勝一負`
   quoted as `知彼知己…一勝一負` is an elision, and quoting it without the marker is normal practice.

So the check is a **segmentation**, not a substring test: a citation is grounded if it can be cut into pieces of at
least MIN_PIECE characters, each of which appears somewhere in the notes. An elision produces two long pieces; a
fabricated line produces none. `--self-check` proves the difference on a fabricated classical line, because a check
that cannot fail is the defect this whole exercise is about.

Run: python3 check_citations.py <dir-with-areas-files> [...]   |   --self-check
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ("claude-opus-5-5.md", "minimax-m3.1-flash.md", "deepseek-v4-pro.md", "CANONICAL.md")
INNER = set("，。、；：！？（）「」『』〔〕《》〈〉·　")
SPLIT = set("…—")
MIN_PIECE = 4          # shorter than this and any string is 'grounded' by accident


def _cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def norm(s: str) -> str:
    return "".join(c for c in s if _cjk(c))


def quotations(text: str) -> set[str]:
    pat = r"[^" + "".join(sorted(INNER | SPLIT)) + r"\u4e00-\u9fff]+"
    return {n for c in re.split(pat, text) if len(n := norm(c)) >= 4}


def segments(cite: str, hay: str) -> bool:
    """Can `cite` be covered by note-substrings, none shorter than MIN_PIECE?

    A short citation is accepted only verbatim: `上兵伐謀` is a real four-character phrase, and letting it be
    covered by pieces would accept almost anything of that length.
    """
    if len(cite) <= 5:
        return cite in hay
    i = 0
    while i < len(cite):
        best = 0
        for j in range(len(cite), i + best, -1):
            if cite[i:j] in hay:
                best = j - i
                break
        if best < MIN_PIECE:
            return False
        i += best
    return True


def main(argv: list[str]) -> int:
    hay = norm("".join((ROOT / "docs" / "research" / "20261004-sunzi" / f).read_text() for f in NOTES))
    if "--self-check" in argv:
        real = "知彼知己不知彼而知己一勝一負"                       # an elision, grounded
        fake = "兵者國之大事也不可不察矣"                            # a real line, reworded — not in the notes
        ok = segments(real, hay) and not segments(fake, hay)
        print("CITATION CHECK CAN FAIL" if ok else "CITATION CHECK CANNOT FAIL")
        print(f"  elision accepted: {segments(real, hay)}   fabrication rejected: {not segments(fake, hay)}")
        return 0 if ok else 1

    targets = [pathlib.Path(a) for a in argv if not a.startswith("-")] or \
              sorted((ROOT / "runs/20261004-domain-fix-review/surveys").glob("areas-*.md"))
    if not targets:
        print("  FAIL  no files to check — absence is not success")
        return 1
    total = outside = 0
    for p in targets:
        cites = quotations(p.read_text())
        bad = sorted(c for c in cites if not segments(c, hay))
        total += len(cites)
        outside += len(bad)
        print(f"  {'PASS' if not bad else 'FAIL'}  {p.name:36} citations {len(cites):3}  ungrounded {len(bad)}")
        for c in bad:
            print(f"          UNGROUNDED: {c[:70]}")
    print(f"\n  {total} citations checked, {outside} not traceable to the notes")
    return 1 if outside else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
