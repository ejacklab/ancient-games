"""Join the test-log review: verify every quote, group by question.

Quotes are checked against the real files. `testlog.md` is checked as its own artefact, so a finding about the log
is verified the same way as a finding about the gate.

Run: python3 verify_log.py
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
    r"FINDING\s*(\d+)\s*:\s*(?P<file>[^\s|]+?)\s*:\s*(?P<line>\d+)\s*\|\s*(?P<letter>[A-Ea-e])\s*\|\s*"
    r"(?P<sev>high|med|low)\s*\|\s*(?P<what>.+?)\s*\|\s*QUOTE:\s*(?P<quote>.+)", re.I)


def text_of(engine: str) -> str:
    p = HERE / f"{engine}.out"
    return p.read_text(errors="replace") if p.exists() and p.stat().st_size else ""


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().strip("`*_ ")).lower()


def resolve(name: str) -> pathlib.Path | None:
    n = name.strip().lstrip("./")
    if n == "testlog.md" or n.endswith("testlog.md"):
        return HERE / "testlog.md"
    for p in ROOT.rglob(pathlib.Path(n).name):
        if str(p).endswith(n) or str(p.relative_to(ROOT)) == n:
            return p
    return None


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
    kept, dropped = [], []
    for engine in ENGINES:
        n = 0
        for m in FINDING.finditer(text_of(engine)):
            rec = {"engine": engine, "file": m.group("file").strip().lstrip("./"), "line": int(m.group("line")),
                   "letter": m.group("letter").upper(), "sev": m.group("sev").lower(),
                   "what": m.group("what").strip(), "quote": m.group("quote").strip()}
            p = resolve(rec["file"])
            if p is None or not p.exists():
                rec["verdict"], rec["at"] = "no-such-file", 0
            else:
                rec["file"] = "testlog.md" if p.parent == HERE else str(p.relative_to(ROOT))
                rec["verdict"], rec["at"] = locate(p, rec["quote"], rec["line"])
            (kept if rec["verdict"] in ("exact", "near") else dropped).append(rec)
            n += 1
        print(f"  {engine:9} parsed {n}")

    print(f"\n=== {len(kept)} located, {len(dropped)} discarded ===")
    names = {"A": "verdict on the null result", "B": "classification or definition",
             "C": "what the design sample shows", "D": "what the log cannot see",
             "E": "what would make the test decisive"}
    by = defaultdict(list)
    for f in kept:
        by[f["letter"]].append(f)
    for letter in sorted(by):
        hits = by[letter]
        print(f"\n########## {letter} — {names.get(letter, '?')}  ({len(hits)} findings, "
              f"{len({h['engine'] for h in hits})} engine(s): {', '.join(sorted({h['engine'] for h in hits}))})")
        for h in sorted(hits, key=lambda x: (x["file"], x["at"])):
            print(f"    {h['engine']:9} {h['sev']:4} {h['file']}:{h['at']}")
            print(f"          {h['what'][:190]}")
    if dropped:
        print("\n=== discarded ===")
        for f in dropped:
            print(f"  {f['engine']:9} {f['verdict']:13} {f['file']}:{f['line']}  {f['what'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
