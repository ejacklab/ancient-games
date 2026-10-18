import json
import sys

prod, out_path = sys.argv[1], sys.argv[2]
HOOK = "." + "githooks/pre-commit"
F = [
    ("K2-1", "B3", "link not percent-encoded (B3 case 3)", "tools/memory_index.py",
     '    return f"entries/{urllib.parse.quote(name)}"', '    return f"entries/{name}"'),
    ("K2-2", "B2", "duplicate id passes (B2 case 3)", "tools/memory_index.py",
     "        if entry.entry_id in seen:\n            entry.errors.append",
     "        if False:\n            entry.errors.append"),
    ("K2-3", "B4", "--check passes an index over the limit (B4)", "tools/memory_index.py",
     "    if over_limit(rendered):\n        report(", "    if False:\n        report("),
    ("K2-4", "B1", "untracked entry gets a line (B1 case 1)", "tools/memory_index.py",
     '        entry.errors.append("not known to git, git add it first")', "        pass"),
    ("K2-5", "G2", "a change to the script alone skips the hook (G2)", HOOK,
     "-- project-memory/ tools/memory_index.py)", "-- project-memory/)"),
    ("K2-6", "B3", "superseded entry gets a line (B3 case 2)", "tools/memory_index.py",
     "    return [entry for entry in entries if entry.is_active]",
     '    return [entry for entry in entries if entry.status != "retired"]'),
]
out = []
for i, g, d, f, o, n in F:
    c = open(f"{prod}/{f}").read().count(o)
    assert c == 1, (i, c)
    out.append(dict(id=i, group=g, what=d, file=f, old=o, new=n))
json.dump(out, open(out_path, "w"), indent=1)
print(len(out), "faults valid")
