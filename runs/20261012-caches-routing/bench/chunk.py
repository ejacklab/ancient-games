#!/usr/bin/env python3
"""chunk.py -- split the repo corpus into the chunks every store is built from.

The corpus is `git ls-files '*.py' '*.md'` minus the two run folders the brief
excludes.  Two languages, two rules:

* Markdown splits by heading section.  The lines above the first heading (the
  preamble) are their own chunk; a file with no heading at all is one chunk.
* Python splits by top-level `def` or `class`, decorators included, and the
  module-level code -- every line outside those blocks -- is one more chunk.

Each chunk carries `path`, `start_line`, `end_line` and `text`.  It also carries
`name`, the top-level symbol or `None`, and `kind`.  `name` is what lets a route
answer with `path::name` for a function and with `path` for a document; a
markdown chunk never gets one, so a file is one answer no matter how many
sections it has.

Used by build.py to build, and by nothing at query time: a route reads a store,
never the corpus.  Run it directly to see what the corpus looks like.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

EXCLUDED_PREFIXES = (
    "runs/20261012-caches-routing/",
    "runs/20261012-memory-caches/",
)

CORPUS_GLOBS = ("*.py", "*.md")

HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(\S.*?)[ \t]*$")

TOP_LEVEL_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


@dataclass(frozen=True)
class Chunk:
    path: str
    start_line: int
    end_line: int
    text: str
    name: str | None = None
    kind: str = "code"


def repo_root() -> Path:
    """The repo this bench belongs to: bench/ -> run -> runs/ -> repo."""
    return Path(__file__).resolve().parents[3]


def corpus_paths(repo: Path) -> list[str]:
    """Repo-relative paths of the corpus, sorted, excludes applied.

    `git ls-files` decides membership, so untracked scratch never enters a store.
    """
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files", *CORPUS_GLOBS],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    kept = [
        line.strip()
        for line in out.splitlines()
        if line.strip() and not line.startswith(EXCLUDED_PREFIXES)
    ]
    return sorted(kept)


def read_lines(repo: Path, path: str) -> list[str]:
    data = (repo / path).read_bytes().decode("utf-8", "replace")
    return data.splitlines()


def markdown_chunks(path: str, lines: list[str]) -> list[Chunk]:
    """One chunk per heading section, plus the preamble above the first heading."""
    starts = []
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match is not None:
            starts.append((index, match.group(2)))
    if not starts:
        return [Chunk(path, 1, len(lines), "\n".join(lines))] if lines else []

    chunks = []
    preamble_end = starts[0][0]
    preamble = "\n".join(lines[:preamble_end]).strip()
    if preamble:
        chunks.append(Chunk(path, 1, preamble_end, preamble))

    for position, (index, _title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = "\n".join(lines[index:end]).strip()
        if body:
            chunks.append(Chunk(path, index + 1, end, body))
    return chunks


def python_definitions(lines: list[str]) -> tuple[list[tuple[int, int, str]], list[str]]:
    """Return (top-level blocks, parse errors).

    A block is (first line, last line, name), where the first line is the first
    decorator when there is one, because a decorator belongs to its def.
    """
    source = "\n".join(lines)
    tree = ast.parse(source)
    blocks = []
    for node in tree.body:
        if not isinstance(node, TOP_LEVEL_DEFS):
            continue
        start = node.lineno
        for decorator in node.decorator_list:
            start = min(start, decorator.lineno)
        blocks.append((start, node.end_lineno or node.lineno, node.name))
    blocks.sort()
    return blocks, []


def python_chunks(path: str, lines: list[str]) -> list[Chunk]:
    try:
        blocks, _ = python_definitions(lines)
    except SyntaxError as exc:
        # A file the parser refuses is still corpus: index it whole rather than
        # drop it, and say so on stderr so the number is never quietly short.
        print(
            f"chunk.py: {path}: SyntaxError line {exc.lineno}: indexing whole file",
            file=sys.stderr,
        )
        return [Chunk(path, 1, len(lines), "\n".join(lines))] if lines else []

    chunks = []
    module_level = [
        (number, line)
        for number, line in enumerate(lines, start=1)
        if not any(first <= number <= last for first, last, _name in blocks)
    ]
    module_text = "\n".join(line for _number, line in module_level).strip()
    if module_text:
        chunks.append(
            Chunk(path, module_level[0][0], module_level[-1][0], module_text, None, "code")
        )

    for first, last, name in blocks:
        text = "\n".join(lines[first - 1 : last]).strip()
        if text:
            chunks.append(Chunk(path, first, last, text, name, "python"))
    return chunks


def chunk_text(path: str, lines: list[str]) -> list[Chunk]:
    if path.endswith(".md"):
        return markdown_chunks(path, lines)
    if path.endswith(".py"):
        return python_chunks(path, lines)
    raise ValueError(f"not in the corpus's two languages: {path}")


def chunk_corpus(repo: Path, paths: list[str] | None = None) -> list[Chunk]:
    """Every chunk of every corpus file, in corpus order."""
    corpus = corpus_paths(repo) if paths is None else paths
    chunks = []
    for path in corpus:
        chunks.extend(chunk_text(path, read_lines(repo, path)))
    return chunks


def newest_source_mtime(repo: Path, paths: list[str] | None = None) -> float:
    """Newest mtime in the corpus -- the second half of 'what it was built from'."""
    corpus = corpus_paths(repo) if paths is None else paths
    newest = 0.0
    for path in corpus:
        try:
            newest = max(newest, (repo / path).stat().st_mtime)
        except OSError:
            continue
    return newest


def git_head(repo: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="chunk.py", description=__doc__.splitlines()[0])
    parser.add_argument("--repo", default=None, help="repo root (default: inferred)")
    parser.add_argument("--show", type=int, default=0, help="print N chunks as JSON")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else repo_root()
    paths = corpus_paths(repo)
    chunks = chunk_corpus(repo, paths)
    python_chunks_count = sum(1 for chunk in chunks if chunk.kind == "python")
    report = {
        "repo": str(repo),
        "git_head": git_head(repo),
        "newest_source_mtime": newest_source_mtime(repo, paths),
        "files": len(paths),
        "files_py": sum(1 for path in paths if path.endswith(".py")),
        "files_md": sum(1 for path in paths if path.endswith(".md")),
        "chunks": len(chunks),
        "chunks_python": python_chunks_count,
        "chunks_markdown": len(chunks) - python_chunks_count,
        "bytes": sum(len(chunk.text) for chunk in chunks),
    }
    if args.show:
        report["sample"] = [asdict(chunk) for chunk in chunks[: args.show]]
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())