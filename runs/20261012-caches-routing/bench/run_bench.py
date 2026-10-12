#!/usr/bin/env python3
"""run_bench.py -- run every applicable route over a question set and score it.

    run_bench.py --queries ../queries.json

Builds the three stores, answers every question through every route that can
answer it, scores the answer against `gold`, and writes `results.json` (every
number, machine-readable) and `results.md` (one table per category, readable).

## The no-leakage rule, and where it is kept

`query.py` answers from a `RouteInput` that carries four fields and cannot carry
a gold answer.  This script is the only thing that reads `gold`, and it reads it
only after the route has already answered: `answer_one` hands the route the
narrowed input, returns, and `score_one` then looks at `gold`.  The two steps
are separate functions on purpose, and `results.json` records the field list the
route was given so the rule can be checked without reading the code.

## The metrics

* `hit@1/5/10`  -- a gold entry is hit by a returned path when they name the
  same file; a gold `path::name` therefore counts as hit by a route that returned
  the path alone.  hit@k is over the first k returned paths.
* `sym_hit@1/5/10` -- the same, except a gold `path::name` needs the symbol
  itself (see `symbol_hit`).  The best route is chosen on this one.
* `recall@10`  -- C questions only: the share of distinct gold files found in the
  first 10.  C questions ask for every answer, so one hit is not enough.
* `chars_to_first_gold` -- characters of `output` up to and including the first
  line where the route names a gold file as its answer (exact path, see
  `names_as_answer`), or None when it never does; means are over hits only.
  This is the token proxy: it counts what an agent reads before it knows.
* `output_chars`, `seconds` -- what the route printed, and how long it took.

## The determinism check

Delete `bench/.cache/`, rebuild from the corpus, answer every question again,
and compare `paths` answer for answer.  This is the project's first rule made
mechanical: derived from the files, so nothing but the files decides the answer.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import statistics
import sys
import time
from pathlib import Path

import build as builder
import chunk as chunker
import query as router

RESULTS_JSON = "results.json"
RESULTS_MD = "results.md"
CATEGORIES = ("A", "B", "C", "D", "E")
CATEGORY_TITLES = {
    "A": "exact identifier",
    "B": "concept in other words",
    "C": "structure and test impact",
    "D": "decision or reason in the docs",
    "E": "how to run or configure",
}
ROUTES = router.ROUTES


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------


def repo_of(entry: str) -> str:
    """The file a gold or returned entry names, with `::name` dropped."""
    return str(entry).split("::", 1)[0]


def hit_at(paths: list[str], gold: list[str], k: int) -> bool:
    """True when a returned path in the first k names the same file as a gold."""
    window = paths[:k]
    return any(repo_of(found) == repo_of(want) for found in window for want in gold)


def recall_at(paths: list[str], gold: list[str], k: int) -> float:
    """Share of distinct gold files found in the first k returned paths."""
    wanted = {repo_of(entry) for entry in gold}
    if not wanted:
        return 0.0
    found = {repo_of(found) for found in paths[:k]}
    return round(len(wanted & found) / len(wanted), 4)


def names_as_answer(line: str, path: str) -> bool:
    """True when a printed line gives `path` as the route's answer.

    Only the line's own leading name counts: the rg header `# <path> (`, a line
    starting `<path>:` (rg match lines, fts and vec blocks, `<path>::name`
    graph ids), or a line that is the path alone (a graph module id).  A line
    that merely mentions the path in its text, or names a longer path ending in
    it, does not.
    """
    line = line.rstrip("\r\n")
    return line == path or line.startswith(path + ":") or line.startswith(f"# {path} (")


def chars_to_first_gold(output: str, gold: list[str]) -> int | None:
    """Characters read up to and including the first line naming a gold path.

    None when no line names one: a miss is left out of the mean, never scored 0.
    """
    wanted = {repo_of(want) for want in gold}
    read = 0
    for line in output.splitlines(keepends=True):
        read += len(line)
        if any(names_as_answer(line, path) for path in wanted):
            return read
    return None


def find_symbol(repo: Path, path: str, name: str):
    """The `ast` node defining `name` (dotted for a method) in a Python file, or None.

    Read from the file, not from a store, so the symbol-level score does not
    depend on how a store chunked the file.  A def, a class, or (for the last
    part of the name) a module- or class-level assignment.
    """
    try:
        tree = ast.parse((repo / path).read_text(encoding="utf-8"))
    except (OSError, SyntaxError, ValueError):
        return None
    body, found = tree.body, None
    parts = name.split(".")
    for depth, part in enumerate(parts):
        last = depth == len(parts) - 1
        found = None
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name == part:
                    found = node
            elif last and isinstance(node, (ast.Assign, ast.AnnAssign)):
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                if any(isinstance(t, ast.Name) and t.id == part for t in targets):
                    found = node
        if found is None:
            return None
        body = getattr(found, "body", [])
    return found


def symbol_span(node) -> tuple[int, int]:
    """First and last line of a symbol's node, decorators included."""
    first = min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])
    return first, node.end_lineno or node.lineno


def printed_lines(output: str, path: str) -> list[int]:
    """Line numbers of the rg match lines printed for `path`."""
    pattern = re.compile(re.escape(path) + r":(\d+):")
    return [int(m.group(1)) for m in (pattern.match(line) for line in output.splitlines()) if m]


def symbol_hit(found: str, want: str, route: str, output: str, repo: Path) -> bool:
    """Does one returned entry hit one gold entry at the symbol level?

    A gold with no `::` is a file, scored as at file level.  For a gold
    `path::name` the entry must be in that file and:
    * `rg` (paths only): a printed match line of that file lies inside the
      symbol's lines;
    * a `path::X` entry: X is the symbol, the top-level def/class holding it, or
      a method of it (graph ids nest with `::`, read here as `.`);
    * a bare `path` entry (a module-code chunk or a graph module): the symbol is
      module-level code.
    """
    want_path, _, want_name = want.partition("::")
    found_path, _, found_name = found.partition("::")
    if found_path != want_path:
        return False
    if not want_name:
        return True
    node = find_symbol(repo, want_path, want_name)
    if node is None:
        return False
    if route == "rg":
        first, last = symbol_span(node)
        return any(first <= n <= last for n in printed_lines(output, want_path))
    if found_name:
        found_name = found_name.replace("::", ".")
        return (
            found_name == want_name
            or found_name.startswith(want_name + ".")
            or want_name.startswith(found_name + ".")
        )
    return "." not in want_name and isinstance(node, (ast.Assign, ast.AnnAssign))


def symbol_hit_at(paths, gold, k, route, output, repo) -> bool:
    """hit@k where a gold `path::name` needs that symbol, not just its file."""
    return any(
        symbol_hit(found, want, route, output, repo) for found in paths[:k] for want in gold
    )


def answer_one(route: str, question: dict) -> dict:
    """Ask one route one question.  The route is handed four fields and no gold."""
    route_input = router.pick_route_input(question)
    return router.answer(route, route_input)


def score_one(question: dict, answer: dict, route: str, repo: Path) -> dict:
    """Score an answer that already exists.  Only now is `gold` read."""
    gold = list(question.get("gold") or [])
    paths = list(answer.get("paths") or [])
    output = answer.get("output") or ""
    scored = {
        "hit@1": hit_at(paths, gold, 1),
        "hit@5": hit_at(paths, gold, 5),
        "hit@10": hit_at(paths, gold, 10),
        "sym_hit@1": symbol_hit_at(paths, gold, 1, route, output, repo),
        "sym_hit@5": symbol_hit_at(paths, gold, 5, route, output, repo),
        "sym_hit@10": symbol_hit_at(paths, gold, 10, route, output, repo),
        "chars_to_first_gold": chars_to_first_gold(output, gold),
        "output_chars": len(output),
        "seconds": answer.get("seconds", 0.0),
        "paths_returned": len(paths),
    }
    if str(question.get("category")) == "C":
        scored["recall@10"] = recall_at(paths, gold, 10)
    return scored


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------


def applicable_routes(question: dict) -> list[str]:
    route_input = router.pick_route_input(question)
    return [route for route in ROUTES if router.route_applies(route, route_input)]


def run_questions(questions: list[dict], repo: Path, keep_output: bool = False) -> list[dict]:
    """Answer every question through every applicable route."""
    rows = []
    for question in questions:
        for route in ROUTES:
            if route not in applicable_routes(question):
                rows.append(
                    {
                        "id": question.get("id"),
                        "category": question.get("category"),
                        "route": route,
                        "applicable": False,
                        "reason_not_applicable": router.NEEDS.get(route, ()),
                    }
                )
                continue
            answer = answer_one(route, question)
            row = {
                "id": question.get("id"),
                "category": question.get("category"),
                "route": route,
                "applicable": True,
                "paths": answer.get("paths", []),
            }
            row.update(score_one(question, answer, route, repo))
            if answer.get("error"):
                row["error"] = answer["error"]
            if answer.get("note"):
                row["note"] = answer["note"]
            if answer.get("intent"):
                row["graph_intent"] = answer["intent"]
            if keep_output:
                row["output"] = answer.get("output", "")
            else:
                row["output_head"] = (answer.get("output") or "")[:400]
            rows.append(row)
    return rows


def compare_paths(first: list[dict], second: list[dict]) -> dict:
    """Where two runs disagree, answer for answer."""
    index = {(row["id"], row["route"]): row for row in first if row.get("applicable")}
    other = {(row["id"], row["route"]): row for row in second if row.get("applicable")}
    mismatches = []
    for key in sorted(set(index) | set(other)):
        here = index.get(key, {}).get("paths", [])
        there = other.get(key, {}).get("paths", [])
        if here != there:
            mismatches.append(
                {"id": key[0], "route": key[1], "first": here, "second": there}
            )
    return {
        "answers_compared": len(set(index) | set(other)),
        "mismatches": mismatches,
        "identical": not mismatches,
    }


def determinism_check(repo: Path, questions: list[dict]) -> dict:
    """Delete the cache, rebuild from the corpus, answer again, compare.

    Nothing survives the delete except the corpus and the questions, so an
    identical `paths` set means the answer is derived from the files.
    """
    cache = builder.cache_dir()
    if cache.exists():
        shutil.rmtree(cache)
    started = time.perf_counter()
    rebuilds = [builder.build_full(store, repo, cache) for store in builder.STORES]
    rebuild_seconds = round(time.perf_counter() - started, 3)
    again = run_questions(questions, repo)
    return {"rebuild_seconds": rebuild_seconds, "rebuilds": rebuilds, "second_run": again}


def mean(values: list[float]) -> float | None:
    clean = [value for value in values if value is not None]
    return round(statistics.fmean(clean), 4) if clean else None


def category_table(rows: list[dict], category: str) -> dict:
    """One entry per route, over the questions of one category.

    `ALL` means every question that route could answer.
    """
    table = {}
    for route in ROUTES:
        picked = [
            row
            for row in rows
            if row.get("applicable")
            and row["route"] == route
            and (category == "ALL" or row["category"] == category)
        ]
        if not picked:
            table[route] = None
            continue
        chars = [row["chars_to_first_gold"] for row in picked]
        table[route] = {
            "questions": len(picked),
            "mean_hit@5": mean([float(row["hit@5"]) for row in picked]),
            "mean_hit@1": mean([float(row["hit@1"]) for row in picked]),
            "mean_hit@10": mean([float(row["hit@10"]) for row in picked]),
            "mean_sym_hit@5": mean([float(row["sym_hit@5"]) for row in picked]),
            "mean_sym_hit@1": mean([float(row["sym_hit@1"]) for row in picked]),
            "mean_sym_hit@10": mean([float(row["sym_hit@10"]) for row in picked]),
            # Over the answers that named a gold path only; a miss is left out.
            "chars_counted": sum(1 for value in chars if value is not None),
            "mean_chars_to_first_gold": mean(
                [float(value) for value in chars if value is not None]
            ),
            "mean_output_chars": mean([float(row["output_chars"]) for row in picked]),
            "mean_seconds": mean([float(row["seconds"]) for row in picked]),
        }
        recalls = [row.get("recall@10") for row in picked if row.get("recall@10") is not None]
        if recalls:
            table[route]["mean_recall@10"] = mean([float(value) for value in recalls])
    return table


def dash(value) -> str:
    """`--` for a value that does not exist, such as chars over zero hits."""
    return "--" if value is None else str(value)


def markdown_report(payload: dict) -> str:
    out = []
    add = out.append
    add("# Cache benchmark results\n")
    add(f"- question set: `{payload['queries_file']}` ({payload['questions']} questions)")
    add(f"- corpus: {payload['corpus']['files']} files "
        f"({payload['corpus']['files_py']} `.py`, {payload['corpus']['files_md']} `.md`), "
        f"{payload['corpus']['chunks']} chunks")
    add(f"- git HEAD at build: `{payload['corpus']['git_head']}`")
    add(f"- read budget: at most {payload['config']['max_paths']} paths per answer, "
        f"{payload['config']['line_excerpt_chars']} characters per printed line, "
        f"rg output capped at {payload['config']['rg_output_line_cap']} lines")
    add(f"- a route may read: {', '.join(payload['route_input_fields'])}; "
        "`gold` is read by run_bench.py only, after the answer\n")

    add("## Build (full rebuild, no prior store)\n")
    add("| store | seconds | bytes | what it was built from |")
    add("|---|---:|---:|---|")
    for build in payload["builds"]:
        add(
            f"| {build['store']} | {build['seconds']} | {build['bytes']:,} | "
            f"git `{build['git_head'][:7]}`, newest source mtime {build['newest_source_mtime']} |"
        )
    add("")

    determinism = payload["determinism"]
    add("## Determinism check\n")
    if determinism.get("skipped"):
        add("Skipped (`--skip-determinism`).\n")
    else:
        add(f"Deleted `bench/.cache/`, rebuilt in {determinism['rebuild_seconds']}s, "
            f"answered every question again and compared `paths`.\n")
    add(f"- answers compared: {determinism['answers_compared']}")
    add(f"- identical: **{determinism['identical']}**")
    if determinism["mismatches"]:
        add(f"- mismatches: {len(determinism['mismatches'])}")
        for mismatch in determinism["mismatches"][:10]:
            add(f"  - `{mismatch['id']}` via `{mismatch['route']}`: "
                f"{mismatch['first']} != {mismatch['second']}")
    add("")

    add("## By category\n")
    add("`file hit@5` counts a gold `path::name` as hit when the route returns its file. "
        "`symbol hit@5` needs the symbol itself: an entry naming it, the top-level def/class "
        "holding it or a method of it, a module-code chunk for a module-level name, and for "
        "`rg` a printed match line inside the symbol's lines. A gold given as a plain file "
        "scores the same on both. **The best route is chosen on symbol hit@5.**\n")
    add("`chars` is the mean number of characters of output read up to and including the "
        "first line where the route names a gold file as its answer (`# <path> (`, or a line "
        "starting `<path>:`), over the answers that named one; `n` is how many did. A miss is "
        "left out, never scored 0. What each route prints differs -- "
        f"{payload['config']['printed_per_answer']} -- so `chars` measures the print format as "
        "much as the store.\n")
    for category in CATEGORIES:
        group = payload["by_category"].get(category)
        if not group:
            continue
        table = group["routes"]
        questions = group["n_questions"]
        add(f"### Category {category} -- {CATEGORY_TITLES[category]} "
            f"({questions} question{'' if questions == 1 else 's'})\n")
        add("| route | symbol hit@5 | file hit@5 | chars to first gold (n) | "
            "mean output chars | mean seconds |")
        add("|---|---:|---:|---:|---:|---:|")
        for route in ROUTES:
            row = table.get(route)
            if not row:
                add(f"| {route} | -- | -- | -- | -- | -- |")
                continue
            add(
                f"| {route} | {row['mean_sym_hit@5']} | {row['mean_hit@5']} | "
                f"{dash(row['mean_chars_to_first_gold'])} ({row['chars_counted']}) | "
                f"{row['mean_output_chars']} | {row['mean_seconds']} |"
            )
        scored = {route: row["mean_sym_hit@5"] for route, row in table.items() if row}
        top = max(scored.values())
        best = [route for route, value in scored.items() if value == top]
        if top:
            add(f"\nBest on symbol hit@5: {', '.join(best)} ({top})"
                + (" -- a tie" if len(best) > 1 else "") + "\n")
        else:
            add("\nBest on symbol hit@5: none -- no route hits a gold symbol in the first 5\n")
        if category == "C":
            recalls = [
                f"{route} {table[route]['mean_recall@10']}"
                for route in ROUTES
                if table.get(route) and table[route].get("mean_recall@10") is not None
            ]
            if recalls:
                add("Category C also reports recall@10: " + ", ".join(recalls) + "\n")

    add("## Every category, one row per route\n")
    add("The routes do not answer the same number of questions: `graph` applies only where the "
        "question names a symbol or a file, so its row is over fewer questions. The `questions` "
        "column is the denominator.\n")
    add("| route | questions | symbol hit@1 / @5 / @10 | file hit@1 / @5 / @10 | "
        "chars to first gold (n) | mean output chars | mean seconds |")
    add("|---|---:|---:|---:|---:|---:|---:|")
    for route, row in payload["overall"].items():
        add(
            f"| {route} | {row['questions']} | {row['mean_sym_hit@1']} / {row['mean_sym_hit@5']} / "
            f"{row['mean_sym_hit@10']} | {row['mean_hit@1']} / {row['mean_hit@5']} / "
            f"{row['mean_hit@10']} | {dash(row['mean_chars_to_first_gold'])} ({row['chars_counted']}) | "
            f"{row['mean_output_chars']} | {row['mean_seconds']} |"
        )
    add("")

    add("## Per question\n")
    add("| id | category | route | symbol hit@10 | file hit@10 | recall@10 | chars to first gold | "
        "output chars | seconds |")
    add("|---|---|---|---:|---:|---:|---:|---:|---:|")
    for row in payload["results"]:
        if not row.get("applicable"):
            continue
        add(
            f"| {row['id']} | {row['category']} | {row['route']} | "
            f"{int(row['sym_hit@10'])} | {int(row['hit@10'])} | {row.get('recall@10', '--')} | "
            f"{dash(row['chars_to_first_gold'])} | "
            f"{row['output_chars']} | {row['seconds']} |"
        )
    add("")

    not_applicable = [row for row in payload["results"] if not row.get("applicable")]
    if not_applicable:
        add(f"{len(not_applicable)} route/question pairs were not applicable "
            "(the graph route needs a symbol or a file).\n")
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="run_bench.py", description=__doc__.splitlines()[0])
    parser.add_argument(
        "--queries",
        default=str(Path(__file__).resolve().parent.parent / "queries.json"),
        help="question set as JSON (default: ../queries.json)",
    )
    parser.add_argument("--repo", default=None, help="repo root (default: inferred)")
    parser.add_argument("--no-build", action="store_true", help="use the stores already there")
    parser.add_argument(
        "--keep-output", action="store_true", help="keep every full output in results.json"
    )
    parser.add_argument(
        "--skip-determinism",
        action="store_true",
        help="do not delete and rebuild the stores a second time",
    )
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent
    repo = Path(args.repo).resolve() if args.repo else chunker.repo_root()
    queries_path = Path(args.queries)
    if not queries_path.exists():
        raise SystemExit(
            f"question set not found: {queries_path}\n"
            "pass --queries <file>; bench/sample_queries.json is a 5-question stand-in"
        )
    raw = queries_path.read_bytes()
    questions = json.loads(raw)
    if isinstance(questions, dict):
        questions = questions.get("queries", [])
    if not questions:
        raise SystemExit(f"no questions in {queries_path}")

    builds = []
    if args.no_build:
        for store in builder.STORES:
            path = builder.store_path(store)
            meta = builder.read_meta(path)
            builds.append(
                {
                    "store": store,
                    "seconds": None,
                    "bytes": path.stat().st_size if path.exists() else 0,
                    "git_head": meta.get("git_head"),
                    "newest_source_mtime": meta.get("newest_source_mtime"),
                    "reused_existing_store": True,
                }
            )
    else:
        for store in builder.STORES:
            report = builder.build_full(store, repo, builder.cache_dir())
            meta = builder.read_meta(builder.store_path(store))
            report["git_head"] = meta.get("git_head")
            report["newest_source_mtime"] = meta.get("newest_source_mtime")
            builds.append(report)

    model_started = time.perf_counter()
    router.embedder()  # loaded once, so a route's seconds are its own work
    model_seconds = round(time.perf_counter() - model_started, 3)

    started = time.perf_counter()
    results = run_questions(questions, repo, keep_output=args.keep_output)
    run_seconds = round(time.perf_counter() - started, 3)

    determinism = (
        {"skipped": True, "identical": None, "answers_compared": 0, "mismatches": []}
        if args.skip_determinism
        else determinism_check(repo, questions)
    )
    if not args.skip_determinism:
        determinism.update(compare_paths(results, determinism.pop("second_run")))
        determinism.pop("rebuilds", None)

    by_category = {}
    for category in CATEGORIES:
        picked = [row for row in results if row.get("applicable") and row["category"] == category]
        if not picked:
            continue
        by_category[category] = {
            "n_questions": len({row["id"] for row in picked}),
            "routes": category_table(results, category),
        }

    overall = category_table(results, "ALL")
    overall = {route: row for route, row in overall.items() if row}

    corpus_paths = chunker.corpus_paths(repo)
    payload = {
        "bench_version": 2,
        "queries_file": str(queries_path),
        "queries_sha256": hashlib.sha256(raw).hexdigest(),
        "questions": len(questions),
        "config": {
            "max_paths": router.MAX_PATHS,
            "rrf_k": router.RRF_K,
            "rg_output_line_cap": router.RG_OUTPUT_LINE_CAP,
            "line_excerpt_chars": router.LINE_EXCERPT_CHARS,
            "vec_excerpt_chars": router.VEC_EXCERPT_CHARS,
            "fts_tokenizer": "default (unicode61) 1",
            "embedding_model": builder.EMBED_MODEL,
            "rg_terms_are": "fixed strings, case-insensitive",
            "rg_rank": "distinct terms matched, then matching lines, then path",
            "rg_output": "a header for every ranked file; match lines capped in total",
            "fts_snippet_tokens": router.SNIPPET_TOKENS,
            "printed_per_answer": (
                f"rg: a `# path (N matching lines)` header per file plus at most "
                f"{router.RG_OUTPUT_LINE_CAP} match lines of up to {router.LINE_EXCERPT_CHARS} "
                f"characters; fts: one {router.SNIPPET_TOKENS}-token snippet per path; vec: the "
                f"first {router.VEC_EXCERPT_CHARS} characters per path; hybrid: the vec or fts "
                "block per path; graph: one id per line"
            ),
            "symbol_hit": "gold path::name needs the symbol (see results.md); plain-file gold as file hit",
            "chars_to_first_gold": "exact path as the line's answer; misses left out of the mean",
        },
        "route_input_fields": list(router.ROUTE_FIELDS),
        "gold_read_by": "run_bench.py, after the route answered",
        "corpus": {
            "files": len(corpus_paths),
            "files_py": sum(1 for path in corpus_paths if path.endswith(".py")),
            "files_md": sum(1 for path in corpus_paths if path.endswith(".md")),
            "chunks": len(chunker.chunk_corpus(repo, corpus_paths)),
            "git_head": chunker.git_head(repo),
            "newest_source_mtime": chunker.newest_source_mtime(repo, corpus_paths),
        },
        "model_load_seconds": model_seconds,
        "query_seconds_total": run_seconds,
        "builds": builds,
        "determinism": determinism,
        "by_category": by_category,
        "overall": overall,
        "results": results,
    }

    (here / RESULTS_JSON).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (here / RESULTS_MD).write_text(markdown_report(payload) + "\n")
    print(
        json.dumps(
            {
                "results_json": str(here / RESULTS_JSON),
                "results_md": str(here / RESULTS_MD),
                "questions": len(questions),
                "builds": [
                    {"store": b["store"], "seconds": b["seconds"], "bytes": b["bytes"]}
                    for b in builds
                ],
                "determinism_identical": determinism["identical"],
                "determinism_mismatches": len(determinism["mismatches"]),
                "overall": {
                    route: {
                        "mean_sym_hit@5": row["mean_sym_hit@5"],
                        "mean_hit@5": row["mean_hit@5"],
                        "mean_chars_to_first_gold": row["mean_chars_to_first_gold"],
                        "chars_counted": row["chars_counted"],
                        "mean_seconds": row["mean_seconds"],
                    }
                    for route, row in overall.items()
                },
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())