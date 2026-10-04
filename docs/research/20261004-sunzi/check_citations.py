"""Every classical citation in a gate review must be grounded in the notes (or CANONICAL).

Punctuation-insensitive and ellipsis-aware: 「凡戰者，以正合，以奇勝」 and 「以正合…以奇勝」 both reduce to the
notes' own wording. An ellipsis is a *splitter*, because it means text was omitted, so each side is checked alone.
"""
import pathlib, re, sys

NOTES = ("claude-opus-5-5.md", "minimax-m3.1-flash.md", "deepseek-v4-pro.md", "CANONICAL.md")
CJK = lambda ch: "\u4e00" <= ch <= "\u9fff"
INNER = set("，。、；：！？（）「」『』〔〕《》〈〉·　")     # kept inside a quotation
SPLIT = set("…—")                                        # an omission: split here

def norm(s): return "".join(ch for ch in s if CJK(ch))
def chunks(s):
    pat = r"[^" + "".join(sorted(INNER | SPLIT)) + r"\u4e00-\u9fff]+"
    return {n for c in re.split(pat, s) if len(n := norm(c)) >= 4}

def main(folder="."):
    d = pathlib.Path(folder)
    hay = norm("".join((d / f).read_text() for f in NOTES))
    tot = bad = 0
    for f in sorted(d.glob("gate-review-*.md")):
        out = sorted(r for r in chunks(f.read_text()) if r not in hay)
        tot += len(chunks(f.read_text())); bad += len(out)
        print(f"  {f.name:36} citations {len(chunks(f.read_text())):3}  ungrounded {len(out)}")
        for r in out: print(f"       UNGROUNDED: {r[:60]}")
    print(f"\n  {tot} citations checked, {bad} ungrounded")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
