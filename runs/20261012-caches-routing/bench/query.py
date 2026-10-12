#!/usr/bin/env python3
"""query.py -- answer one question through one route.

    query.py --route rg|fts|vec|hybrid|graph --query-json '<json>'

Prints JSON: `paths` (ranked, unique, at most 10, `path` or `path::name`),
`output` (the text an agent would read) and `seconds`.

## The no-leakage rule, and how it is enforced here

A route may read only `question`, `terms`, `symbol` and `file`.  It may never
read `gold`, `gold_check` or `literal_overlap`.

That is not a promise in a comment, it is the type of what reaches a route.
`pick_route_input` is the only code in the harness that touches a query
mapping, and it copies four keys into a frozen `RouteInput`.  Every route takes
a `RouteInput`, so no route can see a gold answer even by accident, and the
field list is asserted at import so a fifth key cannot be added quietly.
`answer_query` is the seam: it picks, then answers, and returns only the route's
own answer.  run_bench.py scores afterwards, from its own copy of the question.

## The routes

* `rg`      the baseline: `rg -n -i -F` over the corpus, files ranked by the
            number of distinct terms matched, then by matching lines.  Terms
            are fixed strings, which is what makes it comparable with the FTS
            route's quoted terms; a term holding a regex metacharacter cannot
            break it.  Every ranked file's header is printed; only the match
            lines under them are capped.
* `fts`     FTS5 `MATCH` with the terms OR-joined and each quoted, ranked by
            bm25, `snippet()` as the output.
* `vec`     embed the `question`, nearest 10 chunks by cosine distance.
* `hybrid`  reciprocal rank fusion of `fts` and `vec`, `sum(1/(60+rank))`.
* `graph`   only for a question carrying a `symbol` or a `file`, and only for
            the three things the graph can answer: who calls a symbol, which
            tests reach a symbol, which tests reach anything in a file.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import build as builder
import chunk as chunker

ROUTES = ("rg", "fts", "vec", "hybrid", "graph")
ROUTE_FIELDS = ("question", "terms", "symbol", "file")
MAX_PATHS = 10
RRF_K = 60
VEC_EXCERPT_CHARS = 300
LINE_EXCERPT_CHARS = 300
RG_OUTPUT_LINE_CAP = 40
SNIPPET_TOKENS = 24

_MODEL = None


@dataclass(frozen=True)
class RouteInput:
    """The only thing a route ever sees of a question."""

    question: str
    terms: tuple[str, ...]
    symbol: str | None
    file: str | None


assert tuple(RouteInput.__dataclass_fields__) == ROUTE_FIELDS, (
    "RouteInput must carry exactly the four fields a route may read"
)


def pick_route_input(query: Mapping) -> RouteInput:
    """Narrow a question to what a route may read.

    The whitelist is the rule.  A key that is not in `ROUTE_FIELDS` is dropped
    here and cannot reach a route by any path, so `gold` cannot leak even if
    the caller passes the whole question through.
    """
    terms = query.get("terms") or []
    if isinstance(terms, str):
        terms = [terms]
    return RouteInput(
        question=str(query.get("question") or ""),
        terms=tuple(str(term) for term in terms if str(term).strip()),
        symbol=(str(query["symbol"]) if query.get("symbol") else None),
        file=(str(query["file"]) if query.get("file") else None),
    )


def empty(seconds: float, note: str | None = None, error: str | None = None) -> dict:
    """What a route says when it has nothing.  Still a well-formed answer."""
    answer = {"paths": [], "output": "", "seconds": round(seconds, 6)}
    if note:
        answer["note"] = note
    if error:
        answer["error"] = error
    return answer


def display(path: str, name: str | None) -> str:
    return f"{path}::{name}" if name else path


def excerpt(text: str, limit: int) -> str:
    """One printed line, cut at `limit` characters with a marker.

    A proxy for what an agent reads.  1495 corpus lines are longer than 300
    characters, so an uncapped line would decide the token metric on its own.
    """
    return text if len(text) <= limit else text[:limit] + " [...]"


def read_store(store: str) -> tuple[sqlite3.Connection | None, str | None]:
    """Open a store read-only.  Missing file is an answer, never an empty db."""
    path = builder.store_path(store)
    if not path.exists():
        return None, (
            f"store file is missing: {path} (run build.py --store {store}); "
            "no database was created"
        )
    try:
        return builder.open_db(path, read_only=True), None
    except sqlite3.Error as exc:
        return None, f"store file could not be opened read-only: {exc}"


# --------------------------------------------------------------------------
# rg
# --------------------------------------------------------------------------


def answer_rg(route_input: RouteInput) -> dict:
    started = time.perf_counter()
    repo = chunker.repo_root()
    paths = chunker.corpus_paths(repo)
    if not route_input.terms:
        return empty(time.perf_counter() - started, note="no terms to search for")

    command = ["rg", "-n", "-i", "-F", "--no-heading", "--color=never", "--no-messages"]
    for term in route_input.terms:
        command += ["-e", term]
    command += ["--"] + paths
    done = subprocess.run(command, cwd=repo, capture_output=True, text=True)
    if done.returncode not in (0, 1):  # 0 = matched, 1 = no match, else a real error
        return empty(time.perf_counter() - started, error=f"rg failed: {done.stderr.strip()[:200]}"
        )

    per_file: dict[str, list[str]] = {}
    terms_hit: dict[str, set[str]] = {}
    folded_terms = [term.casefold() for term in route_input.terms]
    for line in done.stdout.splitlines():
        head, sep, rest = line.partition(":")
        if not sep:
            continue
        per_file.setdefault(head, []).append(line)
        content = rest.partition(":")[2].casefold()
        terms_hit.setdefault(head, set()).update(t for t in folded_terms if t in content)

    # Distinct terms matched first, so a file holding every term outranks one
    # that repeats a single common term; then matching lines; then path.
    ranked = sorted(
        per_file.items(), key=lambda item: (-len(terms_hit[item[0]]), -len(item[1]), item[0])
    )
    top = ranked[:MAX_PATHS]
    # Every ranked file's header is printed, so every path in `paths` appears in
    # `output`; the line cap applies to the match lines under the headers only.
    blocks, printed, capped = [], 0, False
    for path, matches in top:
        blocks.append(f"# {path} ({len(matches)} matching lines)")
        for match in matches:
            if printed >= RG_OUTPUT_LINE_CAP:
                if not capped:
                    blocks.append(f"[match lines capped at {RG_OUTPUT_LINE_CAP}]")
                    capped = True
                break
            blocks.append(excerpt(match, LINE_EXCERPT_CHARS))
            printed += 1
    return {
        "paths": [path for path, _ in top],
        "output": "\n".join(blocks),
        "seconds": round(time.perf_counter() - started, 6),
        "files_matched": len(per_file),
        "lines_matched": sum(len(matches) for matches in per_file.values()),
    }


# --------------------------------------------------------------------------
# fts
# --------------------------------------------------------------------------


def match_expression(terms) -> str:
    """The FTS5 MATCH string: each term quoted, OR-joined.

    Quoting is not decoration.  An id like `D-0012` is parsed as FTS5 syntax
    (`D - 0012`) and silently matches something else, or nothing.
    """
    quoted = ['"' + term.replace('"', '""') + '"' for term in terms if term.strip()]
    return " OR ".join(quoted)


def fts_ranked_chunks(route_input: RouteInput, limit: int = 200) -> list[dict]:
    """Chunks in bm25 order.  Used by `fts` and by `hybrid`."""
    conn, problem = read_store("fts")
    if conn is None:
        raise LookupError(problem)
    try:
        expression = match_expression(route_input.terms)
        if not expression:
            return []
        rows = conn.execute(
            "SELECT path, name, start_line, end_line,"
            "       snippet(chunks, 4, '<<', '>>', ' ... ', ?) AS snip,"
            "       bm25(chunks) AS score"
            "  FROM chunks"
            " WHERE chunks MATCH ?"
            " ORDER BY score"
            " LIMIT ?",
            (SNIPPET_TOKENS, expression, limit),
        ).fetchall()
    finally:
        conn.close()
    return [
        {
            "path": path,
            "name": name,
            "start_line": start_line,
            "end_line": end_line,
            "text": snip,
            "score": score,
            "display": display(path, name),
        }
        for path, name, start_line, end_line, snip, score in rows
    ]


def fts_answer(route_input: RouteInput) -> tuple[list[str], dict[str, str]]:
    """The `fts` route's answer as data: its paths, and each path's printed block.

    Ranked chunks are collapsed to unique paths here, at most `MAX_PATHS`, so
    `hybrid` fuses the answer `fts` would actually give rather than a longer
    internal scan.  Raises LookupError when the store file is missing.
    """
    paths, blocks = [], {}
    for chunk in fts_ranked_chunks(route_input):
        name = chunk["display"]
        if name in blocks:
            continue
        paths.append(name)
        blocks[name] = f"{name}:{chunk['start_line']}-{chunk['end_line']}: {chunk['text']}"
        if len(paths) == MAX_PATHS:
            break
    return paths, blocks


def answer_fts(route_input: RouteInput) -> dict:
    started = time.perf_counter()
    if not route_input.terms:
        return empty(time.perf_counter() - started, note="no terms to search for")
    try:
        unique, blocks = fts_answer(route_input)
    except LookupError as exc:
        return empty(time.perf_counter() - started, error=str(exc))
    return {
        "paths": unique,
        "output": "\n".join(blocks[name] for name in unique),
        "seconds": round(time.perf_counter() - started, 6),
        "expression": match_expression(route_input.terms),
        "paths_found": len(unique),
    }


# --------------------------------------------------------------------------
# vec
# --------------------------------------------------------------------------


def embedder():
    """The one embedding model, loaded once per process, and never rebuilt."""
    global _MODEL
    if _MODEL is None:
        from model2vec import StaticModel

        _MODEL = StaticModel.from_pretrained(builder.EMBED_MODEL)
    return _MODEL


def vec_ranked_chunks(route_input: RouteInput, k: int = MAX_PATHS) -> list[dict]:
    """The k nearest chunks by cosine distance.  Used by `vec` and by `hybrid`.

    Empty when there is nothing to embed: an empty question has no vector, and
    the model returns no embedding for it rather than a zero one.  Raises
    LookupError when the store file is missing, so the caller decides how to say
    so and never creates a database by asking.
    """
    if not route_input.question.strip():
        return []
    conn, problem = read_store("vec")
    if conn is None:
        raise LookupError(problem)
    try:
        model = embedder()
        import numpy as np
        import sqlite_vec

        vector = np.asarray(model.encode([route_input.question]), dtype=np.float32)
        neighbors = conn.execute(
            "SELECT v.chunk_id AS chunk_id, v.distance AS distance"
            "  FROM chunk_vec AS v"
            " WHERE v.embedding MATCH ? AND k = ?"
            " ORDER BY v.distance",
            (sqlite_vec.serialize_float32(vector[0]), k),
        ).fetchall()
        if not neighbors:
            return []
        marks = ",".join("?" * len(neighbors))
        rows = conn.execute(
            f"SELECT chunk_id, path, name, start_line, text FROM chunk WHERE chunk_id IN ({marks})",
            [chunk_id for chunk_id, _distance in neighbors],
        ).fetchall()
    finally:
        conn.close()
    by_id = {
        row[0]: {"path": row[1], "name": row[2], "start_line": row[3], "text": row[4]}
        for row in rows
    }
    chunks = []
    for chunk_id, distance in neighbors:
        found = by_id.get(chunk_id)
        if found is None:
            continue
        found = dict(found)
        found["distance"] = distance
        found["display"] = display(found["path"], found["name"])
        chunks.append(found)
    return chunks


def vec_block(chunk: Mapping) -> str:
    """What the vec route prints for a chunk: its name, line and first 300 chars."""
    return f"{chunk['display']}:{chunk['start_line']}: {excerpt(chunk['text'], VEC_EXCERPT_CHARS)}"


def answer_vec(route_input: RouteInput) -> dict:
    started = time.perf_counter()
    if not route_input.question.strip():
        return empty(time.perf_counter() - started, note="empty question: nothing to embed")
    try:
        chunks = vec_ranked_chunks(route_input)
    except LookupError as exc:
        return empty(time.perf_counter() - started, error=str(exc))
    except sqlite3.Error as exc:
        return empty(time.perf_counter() - started, error=f"vector query failed: {exc}")
    if not chunks:
        return empty(time.perf_counter() - started, note="no chunks in the store")

    unique, blocks = [], []
    for chunk in chunks:
        if chunk["display"] in unique:
            continue
        unique.append(chunk["display"])
        blocks.append(vec_block(chunk))
    return {
        "paths": unique,
        "output": "\n".join(blocks),
        "seconds": round(time.perf_counter() - started, 6),
        "distances": [round(chunk["distance"], 4) for chunk in chunks],
    }


# --------------------------------------------------------------------------
# hybrid
# --------------------------------------------------------------------------


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = RRF_K) -> list[str]:
    """`score = sum(1/(k + rank))` over the rankings, best first.

    `rank` starts at 1, so the best result of one list scores 1/61 and a result
    that two lists agree on early scores twice that.  Ties keep the order the
    routes were fused in, which is fixed, so the output is deterministic.
    """
    scores: dict[str, float] = {}
    first_seen: dict[str, int] = {}
    for ranking in rankings:
        for position, item in enumerate(ranking, start=1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + position)
            first_seen.setdefault(item, len(first_seen))
    return sorted(scores, key=lambda item: (-scores[item], first_seen[item]))


def answer_hybrid(route_input: RouteInput) -> dict:
    """Rank fusion of the two content routes; the graph route is not part of it.

    Each route keeps its own text for a path, and a fused hit shows the text of
    whichever route ranked it.  A path both routes found shows once.
    """
    started = time.perf_counter()
    problems = []
    fts_list, fts_text = [], {}
    if not route_input.terms:
        problems.append("no terms to search for")
    else:
        try:
            fts_list, fts_text = fts_answer(route_input)
        except LookupError as exc:
            problems.append(str(exc))

    vec_list, vec_text = [], {}
    try:
        for chunk in vec_ranked_chunks(route_input):
            name = chunk["display"]
            if name in vec_text:
                continue
            vec_list.append(name)
            vec_text[name] = vec_block(chunk)
    except (LookupError, sqlite3.Error) as exc:
        problems.append(f"vec: {exc}")

    fused = reciprocal_rank_fusion([fts_list, vec_list])[:MAX_PATHS]
    blocks = [vec_text.get(name) or fts_text[name] for name in fused if name in fts_text or name in vec_text]
    answer = {
        "paths": fused,
        "output": "\n".join(blocks),
        "seconds": round(time.perf_counter() - started, 6),
        "fts_paths": len(fts_list),
        "vec_paths": len(vec_list),
    }
    if problems:
        answer["note"] = "; ".join(problems)
    return answer


# --------------------------------------------------------------------------
# graph
# --------------------------------------------------------------------------

TEST_INTENT = re.compile(
    r"\b(test|tests|testing|cover|covers|covered|coverage|exercis|reach|reaches|reached"
    r"|regression|regressions|break|breaks)\w*",
    re.IGNORECASE,
)
CALL_INTENT = re.compile(
    r"\b(call|calls|called|caller|callers|invoke|invokes|invoked|depend|depends"
    r"|depended|uses|used|using)\w*",
    re.IGNORECASE,
)


def graph_intent(route_input: RouteInput) -> str | None:
    """Which of the graph's three answers this question is asking for.

    Decided from `question` words only, because that is all a caller knows.  A
    test question wins over a call question: "which tests call X" is a test
    question.
    """
    question = route_input.question
    if route_input.symbol:
        if TEST_INTENT.search(question):
            return "tests-reaching-symbol"
        if CALL_INTENT.search(question):
            return "callers-of-symbol"
        return "where-symbol-is"
    if route_input.file:
        if TEST_INTENT.search(question):
            return "tests-reaching-file"
        return "file-functions"
    return None


def resolve_symbol(conn: sqlite3.Connection, symbol: str, file: str | None) -> list[tuple]:
    """Function rows for a symbol: (id, file, name, role).

    Qualified name first (`Class.method`), then every function with that bare
    name, then a class's methods (`Class.*`; code_graph has no class nodes).
    A name that is not a function at all may be a module, whose stem or
    whose parent directory is the name.  When `file` is known it narrows, never
    widens.
    """
    if file:
        rows = conn.execute(
            "SELECT id, file, name, role FROM function WHERE qualname = ? AND file = ?"
            " ORDER BY file, line",
            (symbol, file),
        ).fetchall()
        if rows:
            return rows
    rows = conn.execute(
        "SELECT id, file, name, role FROM function WHERE qualname = ? ORDER BY file, line",
        (symbol,),
    ).fetchall()
    if rows:
        return rows
    if file:
        rows = conn.execute(
            "SELECT id, file, name, role FROM function WHERE name = ? AND file = ? ORDER BY file, line",
            (symbol, file),
        ).fetchall()
        if rows:
            return rows
    rows = conn.execute(
        "SELECT id, file, name, role FROM function WHERE name = ? ORDER BY file, line",
        (symbol,),
    ).fetchall()
    if rows:
        return rows
    # A class: code_graph has no class nodes, only its methods (`Class.method`).
    # An exact, case-sensitive prefix test; LIKE would fold ASCII case.
    prefix = symbol + "."
    if file:
        rows = conn.execute(
            "SELECT id, file, name, role FROM function WHERE substr(qualname, 1, ?) = ?"
            " AND file = ? ORDER BY file, line",
            (len(prefix), prefix, file),
        ).fetchall()
        if rows:
            return rows
    rows = conn.execute(
        "SELECT id, file, name, role FROM function WHERE substr(qualname, 1, ?) = ?"
        " ORDER BY file, line",
        (len(prefix), prefix),
    ).fetchall()
    if rows:
        return rows
    return conn.execute(
        "SELECT module_id, file, NULL, 'module' FROM module_file"
        " WHERE file = ? OR file = ? OR file LIKE ? ORDER BY file",
        (f"{symbol}.py", f"{symbol}/__init__.py", f"{symbol}/%"),
    ).fetchall()


def tests_reaching(conn: sqlite3.Connection, function_ids: list[str]) -> list[tuple]:
    """Tests that reach any of these functions, nearest first.

    `hops` is the shortest number of call and fixture edges, so a test that
    calls the function is ranked above one that reaches it through two hops.
    """
    if not function_ids:
        return []
    marks = ",".join("?" * len(function_ids))
    return conn.execute(
        f"SELECT r.test_id, r.function_id, min(r.hops) AS hops"
        f"  FROM test_reach AS r"
        f"  JOIN function AS f ON f.id = r.test_id"
        f" WHERE r.function_id IN ({marks})"
        f" GROUP BY r.test_id, r.function_id"
        f" ORDER BY hops, r.test_id",
        function_ids,
    ).fetchall()


def callers_of(conn: sqlite3.Connection, function_ids: list[str]) -> list[tuple]:
    """Callers of these functions: (caller, callee), functions before modules."""
    if not function_ids:
        return []
    marks = ",".join("?" * len(function_ids))
    return conn.execute(
        f"SELECT c.caller, c.callee FROM call_edge AS c"
        f" LEFT JOIN function AS f ON f.id = c.caller"
        f" WHERE c.callee IN ({marks})"
        f" ORDER BY (f.id IS NULL), c.caller",
        function_ids,
    ).fetchall()


def answer_graph(route_input: RouteInput) -> dict:
    started = time.perf_counter()
    intent = graph_intent(route_input)
    if intent is None:
        return empty(time.perf_counter() - started,
            note="no symbol and no file: the graph cannot answer this without one",
        )
    conn, problem = read_store("graph")
    if conn is None:
        return empty(time.perf_counter() - started, error=problem)

    hits: list[str] = []
    try:
        if intent in ("callers-of-symbol", "tests-reaching-symbol", "where-symbol-is"):
            targets = resolve_symbol(conn, route_input.symbol, route_input.file)
            ids = [row[0] for row in targets]
            if intent == "callers-of-symbol":
                hits = [caller for caller, _callee in callers_of(conn, ids)]
            elif intent == "tests-reaching-symbol":
                hits = [test_id for test_id, _fn, _hops in tests_reaching(conn, ids)]
            else:
                hits = ids
        else:  # tests-reaching-file, file-functions
            file_rows = conn.execute(
                "SELECT module_id FROM module_file WHERE file = ?", (route_input.file,)
            ).fetchall()
            ids = [row[0] for row in file_rows]
            ids += [
                row[0]
                for row in conn.execute(
                    "SELECT id FROM function WHERE file = ? ORDER BY line", (route_input.file,)
                ).fetchall()
            ]
            if intent == "tests-reaching-file":
                hits = [test_id for test_id, _fn, _hops in tests_reaching(conn, ids)]
            else:
                hits = ids
    except sqlite3.Error as exc:
        return empty(time.perf_counter() - started, error=f"graph query failed: {exc}")
    finally:
        conn.close()

    unique: list[str] = []
    for hit in hits:
        if hit not in unique:
            unique.append(hit)
    unique = unique[:MAX_PATHS]
    note = None
    if not unique:
        note = f"no graph answer for {route_input.symbol or route_input.file} ({intent})"
    return {
        "paths": unique,
        "output": "\n".join(unique),
        "seconds": round(time.perf_counter() - started, 6),
        "intent": intent,
        "hits_before_cap": len(set(hits)),
        "note": note,
    }


# --------------------------------------------------------------------------
# dispatch
# --------------------------------------------------------------------------

_HANDLERS = {
    "rg": answer_rg,
    "fts": answer_fts,
    "vec": answer_vec,
    "hybrid": answer_hybrid,
    "graph": answer_graph,
}

# The `graph` route is applicable only when the question carries a symbol or a
# file; the others need terms (rg, fts) or a question (vec, hybrid).
NEEDS = {"graph": ("symbol", "file"), "rg": ("terms",), "fts": ("terms",), "vec": ("question",)}


def route_applies(route: str, route_input: RouteInput) -> bool:
    if route == "graph":
        return bool(route_input.symbol or route_input.file)
    if route == "hybrid":
        return bool(route_input.terms or route_input.question)
    return True


def answer(route: str, route_input: RouteInput) -> dict:
    """Answer with one route.  The only question a route sees is `route_input`."""
    if route not in _HANDLERS:
        raise ValueError(f"unknown route: {route}; choose from {', '.join(ROUTES)}")
    result = _HANDLERS[route](route_input)
    result["route"] = route
    return result


def answer_query(route: str, query: Mapping) -> dict:
    """Pick what a route may read, then answer.  Nothing else crosses over."""
    return answer(route, pick_route_input(query))


def main(argv=None):
    parser = argparse.ArgumentParser(prog="query.py", description=__doc__.splitlines()[0])
    parser.add_argument("--route", required=True, choices=ROUTES)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query-json", help="the question as a JSON object")
    group.add_argument("--query-file", help="a file holding the question as JSON")
    args = parser.parse_args(argv)

    raw = args.query_json if args.query_json else Path(args.query_file).read_text(encoding="utf-8")
    query = json.loads(raw)
    if isinstance(query, list):
        if len(query) != 1:
            raise SystemExit("query.py answers one question; give one object")
        query = query[0]
    print(json.dumps(answer_query(args.route, query), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())