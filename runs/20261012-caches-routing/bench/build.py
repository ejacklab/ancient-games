#!/usr/bin/env python3
"""build.py -- full rebuild of the three stores the routes read.

    build.py --store fts|vec|graph|all

Three stores, three files, under `bench/.cache/`:

* `fts.sqlite`   FTS5 over the chunks, `path` and the line numbers UNINDEXED,
                 the default tokenizer, ranked by bm25 at query time.
* `vec.sqlite`   a sqlite-vec `vec0` table of chunk embeddings plus the chunk
                 table the vectors point into.
* `graph.sqlite` the code graph, in tables with an index for each way the
                 `graph` route asks about it.

Every store obeys the project's four rules:

1. Derived, never the source.  Nothing outside this folder is written, and the
   store holds nothing a reader needs in order to be right.
2. Full rebuild only.  Each store is built into a temporary file in the same
   directory and then `os.replace`d over the old one, so a reader either sees
   the whole previous store or the whole new one.  There is no update path and
   no code that could add one.
3. It records what it was built from: `git_head` and `newest_source_mtime`, in a
   `meta` table in the store itself.
4. A reader opens it read-only (`file:...?mode=ro`, `uri=True`); a missing file
   is an answer, not an empty database.  That is query.py's half of the rule and
   the reason nothing here creates a store on demand.

Rebuilding from nothing gives the same answers: nothing carries state between
runs, every insert is in corpus order, and no clock, hash seed or rowid
sequence reaches a stored value.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from collections import defaultdict, deque
from pathlib import Path

import chunk as chunker

STORES = ("fts", "vec", "graph")
CACHE_DIRNAME = ".cache"
EMBED_DIMS = 256
EMBED_MODEL = "minishlab/potion-base-8M"
CODE_GRAPH = Path("code_graph/code_graph.py")
GRAPH_EXCLUDES = ("runs/20261012-caches-routing/*", "runs/20261012-memory-caches/*")
COVERAGE_FOLLOWS = ("call", "fixture")

_MODEL = None


def cache_dir() -> Path:
    return Path(__file__).resolve().parent / CACHE_DIRNAME


def store_path(store: str, directory: Path | None = None) -> Path:
    return (directory or cache_dir()) / f"{store}.sqlite"


def open_db(path: Path, read_only: bool = False) -> sqlite3.Connection:
    """Open a store, always with the sqlite-vec extension loaded.

    `vec0` is an eponymous virtual table, so querying the vector store needs the
    extension even to read; loading it costs nothing for the other two.

    `read_only` is the rule from the brief: `file:...?mode=ro`, `uri=True`, so a
    missing file raises instead of being created empty.  That is the whole
    reason no route may build a store on demand -- the open would succeed and
    hand back a database with no rows, which looks like an answer.
    """
    if read_only:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    else:
        conn = sqlite3.connect(str(path))
    conn.enable_load_extension(True)
    import sqlite_vec

    sqlite_vec.load(conn)
    conn.enable_load_extension(False)
    return conn


def write_meta(conn: sqlite3.Connection, store: str, repo: Path, paths: list[str], extra=None):
    conn.execute("CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT)")
    facts = {
        "store": store,
        "git_head": chunker.git_head(repo),
        "newest_source_mtime": repr(chunker.newest_source_mtime(repo, paths)),
        "files": str(len(paths)),
        "schema": "bench-cache/1",
    }
    if extra:
        facts.update({key: str(value) for key, value in extra.items()})
    conn.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)", sorted(facts.items())
    )


def read_meta(path: Path) -> dict:
    """What a store says it was built from.  Empty when the file is missing."""
    if not path.exists():
        return {}
    conn = open_db(path, read_only=True)
    try:
        rows = conn.execute("SELECT key, value FROM meta").fetchall()
    except sqlite3.Error:
        return {}
    finally:
        conn.close()
    return dict(rows)


def build_full(store: str, repo: Path, directory: Path) -> dict:
    """Build one store from the corpus, into a temp file, then replace.

    The returned report is what build.py prints: seconds and bytes.  Nothing is
    kept in memory between the corpus read and the file, so the file is the
    whole build.
    """
    directory.mkdir(parents=True, exist_ok=True)
    target = store_path(store, directory)
    paths = chunker.corpus_paths(repo)
    chunks = chunker.chunk_corpus(repo, paths)

    builder = {"fts": build_fts, "vec": build_vec, "graph": build_graph}[store]
    temp = target.with_name(f".{target.name}.building")
    for leftover in (temp, Path(f"{temp}-journal"), Path(f"{temp}-wal"), Path(f"{temp}-shm")):
        leftover.unlink(missing_ok=True)

    started = time.perf_counter()
    conn = open_db(temp)
    try:
        facts = builder(conn, repo, paths, chunks) or {}
        conn.commit()
        write_meta(conn, store, repo, paths, facts)
        conn.commit()
    finally:
        conn.close()
    os.replace(temp, target)
    seconds = time.perf_counter() - started

    report = {
        "store": store,
        "path": str(target.relative_to(Path(__file__).resolve().parents[1])),
        "seconds": round(seconds, 3),
        "bytes": target.stat().st_size,
        **facts,
    }
    return report


# --------------------------------------------------------------------------
# fts
# --------------------------------------------------------------------------


def build_fts(conn: sqlite3.Connection, repo: Path, paths: list[str], chunks: list[chunker.Chunk]):
    conn.execute(
        "CREATE VIRTUAL TABLE chunks USING fts5("
        "  path UNINDEXED,"
        "  start_line UNINDEXED,"
        "  end_line UNINDEXED,"
        "  name UNINDEXED,"
        "  text"
        ")"
    )
    conn.executemany(
        "INSERT INTO chunks(path, start_line, end_line, name, text) VALUES (?, ?, ?, ?, ?)",
        [(c.path, c.start_line, c.end_line, c.name, c.text) for c in chunks],
    )
    return {"chunks": len(chunks), "tokenizer": "default (unicode61) 1"}


# --------------------------------------------------------------------------
# vec
# --------------------------------------------------------------------------


def embedder():
    """The one embedding model, loaded once per process."""
    global _MODEL
    if _MODEL is None:
        from model2vec import StaticModel

        _MODEL = StaticModel.from_pretrained(EMBED_MODEL)
    return _MODEL


def build_vec(conn: sqlite3.Connection, repo: Path, paths: list[str], chunks: list[chunker.Chunk]):
    import numpy as np
    import sqlite_vec

    conn.execute(
        "CREATE TABLE chunk("
        "  chunk_id INTEGER PRIMARY KEY,"
        "  path TEXT NOT NULL,"
        "  start_line INTEGER NOT NULL,"
        "  end_line INTEGER NOT NULL,"
        "  name TEXT,"
        "  text TEXT NOT NULL"
        ")"
    )
    conn.execute(
        "CREATE VIRTUAL TABLE chunk_vec USING vec0("
        f"  chunk_id INTEGER PRIMARY KEY,"
        f"  embedding FLOAT[{EMBED_DIMS}] distance_metric=cosine"
        ")"
    )
    model = embedder()
    vectors = np.asarray(model.encode([c.text for c in chunks]), dtype=np.float32)
    rows = [
        (index, chunk.path, chunk.start_line, chunk.end_line, chunk.name, chunk.text)
        for index, chunk in enumerate(chunks, start=1)
    ]
    conn.executemany(
        "INSERT INTO chunk(chunk_id, path, start_line, end_line, name, text) VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.executemany(
        "INSERT INTO chunk_vec(chunk_id, embedding) VALUES (?, ?)",
        [
            (index, sqlite_vec.serialize_float32(vectors[index - 1]))
            for index in range(1, len(chunks) + 1)
        ],
    )
    return {"chunks": len(chunks), "model": EMBED_MODEL, "dims": EMBED_DIMS}


# --------------------------------------------------------------------------
# graph
# --------------------------------------------------------------------------

GRAPH_SCHEMA = """
CREATE TABLE node(
  id TEXT PRIMARY KEY, kind TEXT, file TEXT, line INTEGER, end_line INTEGER,
  name TEXT, qualname TEXT, module TEXT, role TEXT, is_test_file INTEGER, tested INTEGER
);
CREATE TABLE edge(src TEXT, dst TEXT, kind TEXT, line INTEGER);

CREATE TABLE function(
  id TEXT PRIMARY KEY, name TEXT, qualname TEXT, file TEXT, module TEXT,
  role TEXT, line INTEGER, end_line INTEGER, tested INTEGER
);
CREATE TABLE module_file(module_id TEXT PRIMARY KEY, file TEXT NOT NULL);
CREATE TABLE call_edge(caller TEXT, callee TEXT, line INTEGER);
CREATE TABLE fixture_edge(consumer TEXT, fixture TEXT, line INTEGER);
CREATE TABLE test_reach_direct(test_id TEXT, function_id TEXT);
CREATE TABLE test_reach(test_id TEXT, function_id TEXT, hops INTEGER);

CREATE INDEX function_name      ON function(name);
CREATE INDEX function_file      ON function(file);
CREATE INDEX call_caller        ON call_edge(caller);
CREATE INDEX call_callee        ON call_edge(callee);
CREATE INDEX fixture_consumer   ON fixture_edge(consumer);
CREATE INDEX fixture_fixture    ON fixture_edge(fixture);
CREATE INDEX reach_direct_fn    ON test_reach_direct(function_id);
CREATE INDEX reach_direct_test  ON test_reach_direct(test_id);
CREATE INDEX reach_fn           ON test_reach(function_id);
CREATE INDEX reach_test         ON test_reach(test_id);
CREATE INDEX module_file_file   ON module_file(file);
CREATE INDEX node_file          ON node(file);
CREATE INDEX edge_src           ON edge(src);
CREATE INDEX edge_dst           ON edge(dst);
"""


def run_code_graph(repo: Path) -> dict:
    """code_graph.py's JSON, read from stdout.

    The script exits 1 when it logged a read or parse error, so a non-zero exit
    with usable JSON is reported rather than thrown away.
    """
    command = [sys.executable, str(repo / CODE_GRAPH), str(repo)]
    for pattern in GRAPH_EXCLUDES:
        command += ["--exclude", pattern]
    done = subprocess.run(command, capture_output=True, text=True)
    if not done.stdout.strip():
        raise RuntimeError(f"code_graph.py printed nothing: {done.stderr.strip()[:400]}")
    return json.loads(done.stdout)


def reachability(edges: list[tuple[str, str, str, int]]) -> dict:
    """The adjacency the graph route's reachability is walked over.

    Follows `call` and `fixture` edges only, which is code_graph's own rule.
    """
    adjacency = defaultdict(list)
    for src, dst, kind, _line in edges:
        if kind in COVERAGE_FOLLOWS:
            adjacency[src].append(dst)
    return adjacency


def build_graph(conn: sqlite3.Connection, repo: Path, paths: list[str], chunks: list[chunker.Chunk]):
    payload = run_code_graph(repo)
    nodes = payload["nodes"]
    edges = [(e["from"], e["to"], e["kind"], e["line"]) for e in payload["edges"]]
    conn.executescript(GRAPH_SCHEMA)

    conn.executemany(
        "INSERT INTO node(id, kind, file, line, end_line, name, qualname, module, role,"
        " is_test_file, tested) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                n["id"], n["kind"], n["file"], n["line"], n.get("end_line"),
                n.get("name"), n.get("qualname"), n.get("module"), n.get("role"),
                int(bool(n.get("is_test_file"))), None if n.get("tested") is None else int(n["tested"]),
            )
            for n in nodes
        ],
    )
    conn.executemany(
        "INSERT INTO edge(src, dst, kind, line) VALUES (?, ?, ?, ?)", edges
    )
    conn.executemany(
        "INSERT INTO function(id, name, qualname, file, module, role, line, end_line, tested)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                n["id"], n["name"], n.get("qualname"), n["file"], n["module"], n["role"],
                n["line"], n.get("end_line"), int(bool(n["tested"])),
            )
            for n in nodes
            if n["kind"] == "function"
        ],
    )
    conn.executemany(
        "INSERT INTO module_file(module_id, file) VALUES (?, ?)",
        [(n["id"], n["file"]) for n in nodes if n["kind"] == "module"],
    )
    conn.executemany(
        "INSERT INTO call_edge(caller, callee, line) VALUES (?, ?, ?)",
        [(src, dst, line) for src, dst, kind, line in edges if kind == "call"],
    )
    conn.executemany(
        "INSERT INTO fixture_edge(consumer, fixture, line) VALUES (?, ?, ?)",
        [(src, dst, line) for src, dst, kind, line in edges if kind == "fixture"],
    )

    adjacency = reachability(edges)
    direct, transitive = [], []
    for node in nodes:
        if node.get("role") != "test":
            continue
        start = node["id"]
        hops = {start: 0}
        queue = deque([start])
        while queue:
            current = queue.popleft()
            for neighbour in adjacency.get(current, ()):
                if neighbour in hops:
                    continue
                hops[neighbour] = hops[current] + 1
                queue.append(neighbour)
        for target, distance in sorted(hops.items()):
            if distance == 0:
                continue
            transitive.append((start, target, distance))
            if distance == 1:
                direct.append((start, target))
    conn.executemany(
        "INSERT INTO test_reach(test_id, function_id, hops) VALUES (?, ?, ?)", transitive
    )
    conn.executemany(
        "INSERT INTO test_reach_direct(test_id, function_id) VALUES (?, ?)", direct
    )

    # Cross-check: the graph tool has its own coverage count; if the walk above
    # disagrees with it, the store is not the thing it claims to be.
    mine = conn.execute(
        "SELECT count(DISTINCT function_id) FROM test_reach WHERE function_id IN"
        " (SELECT id FROM function WHERE role = 'code')"
    ).fetchone()[0]
    theirs = payload["coverage"]["tested"]
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "functions": sum(1 for n in nodes if n["kind"] == "function"),
        "tests": payload["stats"]["tests"],
        "reach_rows": len(transitive),
        "reach_direct_rows": len(direct),
        "coverage_tested": mine,
        "coverage_tested_by_code_graph": theirs,
        "coverage_agrees": mine == theirs,
        "code_graph_errors": len(payload["errors"]),
        "code_graph_exit_nonzero": bool(payload["errors"]),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(prog="build.py", description=__doc__.splitlines()[0])
    parser.add_argument(
        "--store", default="all", choices=[*STORES, "all"], help="which store to rebuild"
    )
    parser.add_argument("--repo", default=None, help="repo root (default: inferred)")
    parser.add_argument("--cache-dir", default=None, help="override bench/.cache")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else chunker.repo_root()
    directory = Path(args.cache_dir).resolve() if args.cache_dir else cache_dir()
    wanted = STORES if args.store == "all" else (args.store,)
    reports = []
    for store in wanted:
        report = build_full(store, repo, directory)
        # Read the provenance back out of the store rather than trusting what was
        # just written: this is the same read-only open a route does.
        meta = read_meta(store_path(store, directory))
        report["git_head"] = meta.get("git_head")
        report["newest_source_mtime"] = meta.get("newest_source_mtime")
        reports.append(report)
    print(json.dumps({"stores": reports}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())