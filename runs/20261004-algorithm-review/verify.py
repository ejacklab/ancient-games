"""Join the overall algorithm review.

Two jobs, both mechanical:

1. **Quote check.** Every finding must carry `file:line` and a verbatim quote. The inlined brief numbers lines
   exactly as the files do, so a quote is checked against the real file. A quote that is not there is discarded,
   however plausible the finding.
2. **Corroboration.** Findings are grouped by (question letter, file, line) so "two engines independently said
   this" is counted, not asserted. Same line + different question is not corroboration.

Run: python3 verify.py
"""
import pathlib
import re
import sys
from collections import defaultdict

HERE = pathlib.Path(__file__).parent
ROOT = pathlib.Path("/home/smoke01/dev/ancient-games")
ENGINES = ["agy", "claude", "codex", "opencode"]
TOLERANCE = 3

FINDING = re.compile(
    r"FINDING\s*(\d+)\s*:\s*(?P<file>[^\s|]+?)\s*:\s*(?P<line>\d+)\s*\|\s*(?P<letter>[A-Fa-f])\s*\|\s*"
    r"(?P<sev>high|med|low)\s*\|\s*(?P<what>.+?)\s*\|\s*QUOTE:\s*(?P<quote>.+)", re.I)


SUFFIX = sys.argv[1] if len(sys.argv) > 1 else ""


def text_of(engine: str) -> str:
    for name in (f"{engine}{SUFFIX}.md", f"{engine}{SUFFIX}.out"):
        p = HERE / name
        if p.exists() and p.stat().st_size:
            return p.read_text(errors="replace")
    return ""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().strip("`*_ ")).lower()


def locate(path: pathlib.Path, quote: str, claimed: int) -> tuple[str, int]:
    lines = path.read_text(errors="replace").splitlines()
    q = norm(quote)
    if len(q) < 12:
        return "too-short", 0
    hits = [i + 1 for i, l in enumerate(lines) if q in norm(l) or norm(l).startswith(q[:40])]
    if not hits:
        return "missing", 0
    near = min(hits, key=lambda h: abs(h - claimed))
    if claimed in hits:
        return "exact", claimed
    return ("near", near) if abs(near - claimed) <= TOLERANCE else ("elsewhere", near)


def main() -> int:
    findings, unresolved = [], []
    for engine in ENGINES:
        raw = text_of(engine)
        n = 0
        for m in FINDING.finditer(raw):
            f = m.group("file").strip().lstrip("./")
            cand = [p for p in ROOT.rglob(pathlib.Path(f).name)
                    if str(p.relative_to(ROOT)) == f or str(p).endswith(f)]
            rec = {"engine": engine, "file": f, "line": int(m.group("line")),
                   "letter": m.group("letter").upper(), "sev": m.group("sev").lower(),
                   "what": m.group("what").strip(), "quote": m.group("quote").strip()}
            if not cand or not cand[0].exists():
                rec["verdict"], rec["at"] = "no-such-file", 0
                unresolved.append(rec)
            else:
                rec["verdict"], rec["at"] = locate(cand[0], rec["quote"], rec["line"])
                (findings if rec["verdict"] in ("exact", "near") else unresolved).append(rec)
            n += 1
        print(f"  {engine:9} parsed {n}")

    print(f"\n=== {len(findings)} located, {len(unresolved)} discarded ===")
    by_letter = defaultdict(list)
    for f in findings:
        by_letter[f["letter"]].append(f)
    names = {"A": "composition", "B": "duplication/gaps", "C": "unreachable work",
             "D": "silences", "E": "self-consistency", "F": "order",
             "G": "enforcement (gate vs steps)", "H": "delegation (tables vs steps)",
             "I": "templates vs steps"}
    for letter in sorted(by_letter):
        hits = by_letter[letter]
        engs = {h["engine"] for h in hits}
        print(f"\n########## {letter} — {names.get(letter, '?')}  ({len(hits)} findings from {len(engs)} engine(s): "
              f"{', '.join(sorted(engs))})")
        for h in sorted(hits, key=lambda x: (x["file"], x["at"])):
            mark = "[2+]" if sum(1 for g in hits if g["file"] == h["file"] and abs(g["at"] - h["at"]) <= 3) > 1 else "    "
            print(f"  {mark} {h['engine']:9} {h['sev']:4} {h['file']}:{h['at']}")
            print(f"          {h['what'][:180]}")

    if unresolved:
        print("\n=== discarded (quote not found where claimed) ===")
        for f in unresolved:
            print(f"  {f['engine']:9} {f['verdict']:14} {f['file']}:{f['line']}  {f['what'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
