#!/usr/bin/env python3
"""yaml_check.py — P2's structure check, written by the COO for run 20261015-sot-leftovers before P2 starts, so the
check is not edited by the hand it checks (孫子's N2). Reads only the YAML, never the build script.

Checks: the file loads; every record has the same eight keys; `level` is one of three words; `check` names only known
checks, and is `none` exactly for guidance; ids are unique; the 46 requirement ids are all present, whole or as
clauses; every id in `links` is a known id. What it does NOT establish: that the text is right.

  yaml_check.py YAML          exit 0 when all hold, 1 otherwise
  yaml_check.py --self-test   proves it can fail
"""
import sys

import yaml

KEYS = {"id", "part_of", "level", "text", "fails_if", "check", "who_decides", "links"}
LEVELS = {"MUST", "SHOULD", "guidance"}
CHECKS = {"tool", "git", "reviewer", "secret scanner", "none"}
IDS = ("W1.1 W1.2 W1.3 W2.1 W2.2 W3.1 W3.2 W3.3 W3.4 W3.5 W3.6 W4.1 W4.2 W4.3 W5.1 W5.2 W5.3 W6.1 W6.2 W6.3 K1.1 "
       "K4.1 K4.2 K4.3 K5.1 K5.2 K6.1 K6.2 K6.3 Rd1.1 Rd1.2 Rd2.1 Rd2.2 Rd2.3 Rd3.1 Rd4.1 Rd4.2 Rd4.3 Rd4.4 Rd4.5 "
       "Rd5.1 Rd5.2 Rd5.3 Rd5.4 Rd5.5 Rd6.1").split()


def problems(data):
    out = []
    groups = [g for c in data["categories"] for g in c["groups"]]
    recs = [r for g in groups for r in g["requirements"]]
    ids = [r.get("id") for r in recs]
    known = set(ids) | set(IDS) | {g["id"] for g in groups}
    for r in recs:
        if set(r) != KEYS:
            out.append(f"{r.get('id')}: keys {sorted(set(r) ^ KEYS)}")
            continue
        if not isinstance(r["level"], str) or r["level"] not in LEVELS:
            out.append(f"{r['id']}: level {r['level']!r}")
        parts = [p.strip() for p in str(r["check"]).split(";")]
        if not all(p in CHECKS for p in parts):
            out.append(f"{r['id']}: check {r['check']!r}")
        if (r["check"] == "none") != (r["level"] == "guidance"):
            out.append(f"{r['id']}: check none and guidance must go together")
        for link in r["links"] or []:
            if link not in known:
                out.append(f"{r['id']}: link {link} resolves to nothing")
    if len(ids) != len(set(ids)):
        out.append("duplicate ids")
    covered = {r.get("part_of") if r.get("part_of") not in (None, "none") else r.get("id") for r in recs}
    for i in IDS:
        if i not in covered:
            out.append(f"{i}: missing")
    return out


def self_test():
    good = {"categories": [{"groups": [{"id": "W1", "requirements": [
        {"id": i, "part_of": "none", "level": "MUST", "text": "t", "fails_if": "f", "check": "tool",
         "who_decides": "none", "links": []} for i in IDS]}]}]}
    assert problems(good) == [], problems(good)
    import copy
    bad = copy.deepcopy(good); bad["categories"][0]["groups"][0]["requirements"].pop()
    assert any("missing" in p for p in problems(bad))
    bad = copy.deepcopy(good); bad["categories"][0]["groups"][0]["requirements"][0]["links"] = ["Z9.9"]
    assert any("resolves to nothing" in p for p in problems(bad))
    bad = copy.deepcopy(good); bad["categories"][0]["groups"][0]["requirements"][0]["level"] = {"MUST": "x"}
    assert any("level" in p for p in problems(bad))
    print("self-test: PASS")
    return 0


def main(argv):
    if argv[1:] == ["--self-test"]:
        return self_test()
    p = problems(yaml.safe_load(open(argv[1], encoding="utf-8")))
    for line in p:
        print(line)
    print("ok" if not p else f"{len(p)} problem(s)")
    return 1 if p else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
