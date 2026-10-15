#!/usr/bin/env python3
"""paths.py — P2's path check, written by the COO for run 20261015-sot-leftovers (L3, U5).

Every file the requirements YAML names as part of the design kit — a `.md` path in `basis` or in a record's text —
must exist relative to the YAML's own folder. Names of files a project creates (AGENTS.md, CLAUDE.md, INDEX.md,
state.md) are the project's, not the kit's, and are skipped. What it does NOT establish: that the files travel
together into another project.

  paths.py YAML            exit 0 when every kit path resolves, 1 otherwise
  paths.py --self-test     proves it can fail
"""
import re
import sys
from pathlib import Path

import yaml

PROJECT_FILES = {"AGENTS.md", "CLAUDE.md", "INDEX.md", "state.md"}
MD = re.compile(r"[\w./-]+\.md")


def kit_paths(data):
    texts = list(data.get("basis", {}).values())
    texts += [r["text"] for c in data["categories"] for g in c["groups"] for r in g["requirements"]]
    texts += [g["basis"] for c in data["categories"] for g in c["groups"]]
    out = []
    for t in texts:
        for p in MD.findall(t):
            if Path(p).name not in PROJECT_FILES and p not in out:
                out.append(p)
    return out


def missing(yaml_path):
    data = yaml.safe_load(Path(yaml_path).read_text(encoding="utf-8"))
    base = Path(yaml_path).parent
    return [p for p in kit_paths(data) if not (base / p).exists()], kit_paths(data)


def main(argv):
    if argv[1:] == ["--self-test"]:
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "real.md").write_text("x")
            doc = {"basis": {"v": "the vision, real.md"}, "categories": [{"groups": [{"basis": "d: x", "requirements": [
                {"text": "see `gone/missing.md` and AGENTS.md"}]}]}]}
            y = Path(d) / "r.yaml"
            y.write_text(yaml.safe_dump(doc))
            bad, allp = missing(y)
            assert bad == ["gone/missing.md"], bad
            assert "AGENTS.md" not in allp
        print("self-test: PASS")
        return 0
    bad, allp = missing(argv[1])
    print("kit paths:", ", ".join(allp) or "none")
    if bad:
        print("missing:", ", ".join(bad))
        return 1
    print("all kit paths resolve from", Path(argv[1]).parent)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
