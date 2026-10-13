#!/usr/bin/env python3
"""count.py — piece R2 of run 20261013-research-tags-retag (written by the COO, Claude, before any tag sheet existed).

Compares tag sheets with the old labels in the key. Each row of a sheet is one JSON object:
  {"id": "R001", "tag": "verified"}                                   -> same (tag == old) or moved (old -> tag)
  {"id": "R001", "split": [{"part": "...", "tag": "..."}, ...]}       -> split (old -> each part's tag)
  {"id": "R001", "stuck": ["reported", "unproven"], "why": "..."}     -> stuck (between the two)

Usage: count.py --key KEY SHEET [SHEET ...] [--names control,new]   prints Markdown; exit 1 if a sheet is invalid.
       count.py --key KEY SHEET --totals                            prints one JSON line of totals (for the test).
"""
import argparse, json, sys
from collections import Counter

TAGS = ("verified", "reported", "unproven", "unknown")


def load(path, key):
    rows, bad = {}, []
    for n, line in enumerate(open(path), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError as e:
            bad.append(f"line {n}: not JSON ({e})"); continue
        rid = r.get("id")
        if rid not in key: bad.append(f"line {n}: id {rid!r} not in the key")
        elif rid in rows: bad.append(f"line {n}: id {rid} twice")
        else: rows[rid] = r
    missing = sorted(set(key) - set(rows))
    if missing: bad.append(f"{len(missing)} ids missing: {missing[:8]}")
    return rows, bad


def outcome(r, old):
    if "tag" in r:
        return ("same", None) if r["tag"] == old else ("moved", f"{old} -> {r['tag']}")
    if "split" in r:
        return "split", f"{old} -> " + " + ".join(p["tag"] for p in r["split"])
    if "stuck" in r:
        return "stuck", f"{old}: between {' and '.join(r['stuck'])} — {r.get('why', '')}"
    return "invalid", str(r)


def count(rows, key):
    totals, moves, details = Counter(), Counter(), {"split": [], "stuck": [], "invalid": []}
    for rid in sorted(rows):
        kind, what = outcome(rows[rid], key[rid]["old"])
        totals[kind] += 1
        if kind == "moved": moves[what] += 1
        if kind in details: details[kind].append(f"{rid} ({key[rid]['section']} {key[rid]['orig']}): {what}")
    return totals, moves, details


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key", required=True); ap.add_argument("sheets", nargs="+")
    ap.add_argument("--names"); ap.add_argument("--totals", action="store_true")
    a = ap.parse_args()
    key = json.load(open(a.key))
    names = a.names.split(",") if a.names else a.sheets
    results, rc = [], 0
    for name, path in zip(names, a.sheets):
        rows, bad = load(path, key)
        if bad:
            rc = 1; print(f"**{name}: invalid sheet** — " + "; ".join(bad))
        results.append((name,) + count(rows, key))
    if a.totals:
        print(json.dumps({n: dict(t) for n, t, _, _ in results})); return rc
    print(f"# Re-tag counts — {len(key)} rows\n")
    print("| outcome | " + " | ".join(n for n, *_ in results) + " |")
    print("|---|" + "---|" * len(results))
    for k in ("same", "moved", "split", "stuck", "invalid"):
        print(f"| {k} | " + " | ".join(str(t.get(k, 0)) for _, t, _, _ in results) + " |")
    for name, _, moves, details in results:
        print(f"\n## {name}\n\nMoved (old -> new):")
        for m, c in sorted(moves.items()): print(f"- {m}: {c}")
        for k in ("split", "stuck", "invalid"):
            if details[k]:
                print(f"\n{k.capitalize()} rows:"); [print(f"- {d}") for d in details[k]]
    return rc


if __name__ == "__main__":
    sys.exit(main())
