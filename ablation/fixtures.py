"""Fixture repos for the ablation (HYBRID_SPEC §9): the repo a subagent acts on.

Each `make_ucN(path)` materializes a small git repo at `path` (absolute) with
the *unfixed* task state committed — the scripted case files carry the fix in
`fixture.modified`; here the agent has to produce it. Built with the runner's
own `setup_fixture`, so the repo shape is the one the scripted cases run in.

Paths follow the built-in registry (`ancient_games/registry.py`): UC2's
`loop/program_db.jsonl` is R4 (stakes 2, hub, checkpoint) and UC3's
`eval/protocol.json` is R1 (stakes 3, owner-gated) — the CLI and the loop
consult the same registry, so no separate test registry is needed.
"""
from __future__ import annotations

import os

from ancient_games.hybrid.runner import setup_fixture

GITIGNORE = "__pycache__/\n.pytest_cache/\n"  # v1.1 D-A: caches would otherwise count as untracked changes

# UC1 — T2: `research.stability` imports `_WF_GRID` from the wrong module (ImportError).
UC1_FILES = {
    ".gitignore": GITIGNORE,
    "research/__init__.py": "",
    "research/walkforward.py": "_WF_GRID = [1, 2, 3]\n",
    "research/stability.py": "from research.sweep import _WF_GRID\n",
    "tests/test_research_importable.py": "def test_placeholder():\n    assert True\n",
}

# UC2 — T1: six dead helpers in loop/program_db.py; loop/program_db.jsonl is the R4 hub.
_DEAD = "".join(f"\n\ndef _helper_{i}(row):\n    return row.get('k{i}')\n" for i in range(1, 7))
UC2_FILES = {
    ".gitignore": GITIGNORE,
    "loop/__init__.py": "",
    "loop/program_db.py": (
        "import json\n\nDB_PATH = 'loop/program_db.jsonl'\n\n\n"
        "def append(event):\n    with open(DB_PATH, 'a') as fh:\n        fh.write(json.dumps(event) + '\\n')\n\n\n"
        "def read():\n    with open(DB_PATH) as fh:\n        return [json.loads(l) for l in fh if l.strip()]\n" + _DEAD
    ),
    "loop/main.py": "from loop.program_db import append, read\n\n\ndef run():\n    append({'event_type': 'tick'})\n    return read()\n",
    "loop/program_db.jsonl": '{"event_type": "trial", "id": 1}\n{"event_type": "trial", "id": 2}\n',
    "tests/test_loop.py": "from loop import program_db\n\n\ndef test_importable():\n    assert callable(program_db.append)\n",
}

# UC3 — T3: read-only research task over the owner-gated protocol file (R1).
UC3_FILES = {
    ".gitignore": GITIGNORE,
    "eval/protocol.json": '{"holdout": "sealed", "unseal": "owner-gated (ej)", "one_shot": true}\n',
    "eval/README.md": "The sealed holdout has never been opened for a real decision; unsealing is owner-gated.\n",
    "research/.keep": "",
}


def _make(files: dict[str, str], path: str) -> str:
    if not os.path.isabs(path):
        raise ValueError(f"fixture path must be absolute: {path!r}")
    setup_fixture({"fixture": {"files": files}}, path)
    return path


def make_uc1(path: str) -> str:
    return _make(UC1_FILES, path)


def make_uc2(path: str) -> str:
    return _make(UC2_FILES, path)


def make_uc3(path: str) -> str:
    return _make(UC3_FILES, path)


MAKERS = {"UC1": make_uc1, "UC2": make_uc2, "UC3": make_uc3}


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3 or sys.argv[1] not in MAKERS:
        sys.exit("usage: python3 -m ablation.fixtures UC1|UC2|UC3 /abs/path")
    print(MAKERS[sys.argv[1]](sys.argv[2]))
