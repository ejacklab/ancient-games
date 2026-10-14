"""Unit tests for the INDEX.md generator's own functions.

The acceptance tests (tests/test_memory_index.py) drive `tools/memory_index.py` as a subprocess over temporary
repositories. These tests call its parser, renderer and link encoder directly, so a failure points at one
function instead of at a whole run.

Imported by path, not by name: `tools/` is not a package and this test must not depend on sys.path.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[1] / "tools/memory_index.py"


def load_tool():
    """Import tools/memory_index.py under a name in sys.modules (its dataclass needs one)."""
    spec = importlib.util.spec_from_file_location("memory_index", TOOL)
    module = importlib.util.module_from_spec(spec)
    sys.modules["memory_index"] = module
    spec.loader.exec_module(module)
    return module


memory_index = load_tool()

ENTRY_TEXT = (
    "---\nid: 14-10-a1b2c3-2026\nkind: decision\nstatus: active\n---\n"
    "Use code-point order.\n\n**Why:** locale order made collaborators rewrite the file.\n"
)


# --- the parser ------------------------------------------------------------------------------------------------
def test_header_reads_top_level_fields_and_strips_quotes():
    """B2.1 — an indented line is a nested field, and one pair of quotes comes off a value."""
    fields, end, problem = memory_index.parse_header([
        "---", "id:  '14-10-a1b2c3-2026'  ", 'kind: "decision"', "status: 'active'", "scope:", "  id: nested", "---", "body",
    ])
    assert fields == {"id": "14-10-a1b2c3-2026", "kind": "decision", "status": "active"}
    assert (end, problem) == (6, None)


def test_header_problems_are_reported_not_raised():
    """B2.1 — a missing opening or closing `---` is a problem, never an exception."""
    assert memory_index.parse_header(["id: 14-10-a1b2c3-2026"])[2] == "no header"
    assert memory_index.parse_header(["---", "id: 14-10-a1b2c3-2026"])[2] == "header is not closed"


def test_claim_stops_at_why_and_collapses_whitespace():
    """B2.2 — the claim is the body up to `**Why:**`: one sentence, no whitespace runs, nothing after it."""
    claim, has_why = memory_index.read_claim(
        ["", "Use\tcode-point", "", " order   for the index.", "**Why:** reason", "ignored"]
    )
    assert claim == "Use code-point order for the index."
    assert has_why is True


def test_claim_is_empty_without_a_why_line():
    """B2.4 — no `**Why:**` line means the reader never gets a rationale, and an active entry may not have it."""
    claim, has_why = memory_index.read_claim([" \t ", "Claim."])
    assert (claim, has_why) == ("Claim.", False)


def test_crlf_entry_parses_like_an_lf_entry():
    """B3.3 — CRLF input must give the same entry, or the bytes depend on the writer."""
    assert memory_index.parse_entry("D-one.md", ENTRY_TEXT.replace("\n", "\r\n")) == \
        memory_index.parse_entry("D-one.md", ENTRY_TEXT)


def test_active_problems_are_errors_and_inactive_ones_are_warnings():
    """B2.4 B2.5 — a missing or mismatched kind stops an active entry and only warns in an old one."""
    active = memory_index.parse_entry(
        "D-one.md", "---\nid: 14-10-a1b2c3-2026\nkind: fact\nstatus: active\n---\nC.\n**Why:** r\n")
    assert active.errors == ["kind 'fact' does not match the D- file prefix"]
    assert active.warnings == []
    inactive = memory_index.parse_entry(
        "D-one.md", "---\nid: 14-10-a1b2c3-2026\nkind: fact\nstatus: retired\n---\nC.\n")
    assert inactive.errors == []
    assert inactive.warnings == ["kind 'fact' does not match the D- file prefix", "no **Why:** line"]


def test_invalid_utf8_is_a_problem_not_a_crash():
    """B2.6 — undecodable bytes name the file and stop the build."""
    assert memory_index.entry_from_bytes("F-bad.md", b"---\nid: 14-10-a1b2c3-2026\n\xff\n").errors == ["not valid UTF-8"]


def test_duplicate_ids_are_found_in_any_status():
    """B2.3 G4.2 — two entries with one id is an error even when one of them is retired."""
    entries = [
        memory_index.parse_entry("D-one.md", ENTRY_TEXT),
        memory_index.parse_entry("D-two.md", "---\nid: 14-10-a1b2c3-2026\nstatus: retired\n---\n"),
    ]
    memory_index.flag_duplicate_ids(entries)
    assert entries[0].errors == [] and entries[1].errors == ["duplicate id 14-10-a1b2c3-2026"]


@pytest.mark.parametrize("entry_id", ["14-10-a1b2c3-2026", "31-02-a1b2c3-2026"])
def test_id_in_w11_form_passes_without_calendar_validation(entry_id):
    """B2.3 G4.2 — the form is the whole rule: `31-02-...` is not a real date, and is still a valid id."""
    entry = memory_index.parse_entry("D-one.md", ENTRY_TEXT.replace("14-10-a1b2c3-2026", entry_id))
    assert entry.errors == []


@pytest.mark.parametrize("status", ["active", "superseded", "retired"])
@pytest.mark.parametrize("entry_id", [
    "D-20261012-a1",
    "14-10-a1b2c-2026",
    "14-10-a1B2c3-2026",
    "14-10-a1b2c3-2026x",
    "١٤-10-a1b2c3-2026",
])
def test_id_outside_w11_form_is_an_error_in_every_status(entry_id, status):
    """B2.3 B2.5 — the whole value must be the form, ASCII only, whatever the status. An old entry cannot be
    grandfathered, so B2.3 and B2.7 are the only exceptions to B2.5."""
    entry = memory_index.parse_entry(
        "D-one.md", f"---\nid: {entry_id}\nkind: decision\nstatus: {status}\n---\nC.\n**Why:** r\n")
    assert entry.errors == [f"id {entry_id!r} is not in the form DD-MM-xxxxxx-YYYY (x: a lowercase letter or digit)"], (entry_id, status)


def test_missing_id_is_still_reported_as_empty():
    """B2.3 — a missing or nested-only id is `empty id`, not a form complaint about `''`."""
    for raw in ("---\nkind: decision\nstatus: active\n---\nC.\n**Why:** r\n",
                "---\nid: ''\nkind: decision\nstatus: active\n---\nC.\n**Why:** r\n",
                "---\n  id: 14-10-a1b2c3-2026\nkind: decision\nstatus: active\n---\nC.\n**Why:** r\n"):
        assert memory_index.parse_entry("D-one.md", raw).errors == ["empty id"]


@pytest.mark.parametrize("status", ["active", "superseded", "retired"])
@pytest.mark.parametrize("marker", ["<<<<<<< ours", ">>>>>>> theirs"])
@pytest.mark.parametrize("location", ["header", "claim", "after-why"])
def test_conflict_marker_is_an_error_in_every_status(location, marker, status):
    """B2.7 — either marker prefix, in the header or the body, stops the build whatever the status."""
    raw = ENTRY_TEXT.replace("status: active", f"status: {status}")
    if location == "header":
        raw = raw.replace("---\n", f"---\n{marker}\n", 1)
    elif location == "claim":
        raw = raw.replace("\n**Why:**", f"\n{marker}\n**Why:**", 1)
    else:
        raw += f"{marker}\n"
    entry = memory_index.parse_entry("D-one.md", raw)
    assert len(entry.errors) == 1, entry.errors
    assert entry.errors[0].startswith("unresolved conflict marker on line"), entry.errors


def test_every_marker_line_is_reported():
    """B2.7 — a conflict leaves both markers; each is named, as DESIGN step 5 reports every problem."""
    raw = ENTRY_TEXT.replace("Use code-point order.", "<<<<<<< ours\nUse code-point order.\n>>>>>>> theirs")
    errors = memory_index.parse_entry("D-one.md", raw).errors
    assert len(errors) == 2 and all(e.startswith("unresolved conflict marker on line") for e in errors), errors


def test_only_a_line_starting_with_the_marker_is_one():
    """B2.7 — `=======` is a Markdown heading underline, and an indented marker is quoted text, not a merge."""
    for line in ("=======", "  <<<<<<< ours", "x <<<<<<< ours"):
        entry = memory_index.parse_entry("D-one.md", ENTRY_TEXT.replace("Use code-point order.", f"Use order.\n{line}"))
        assert entry.errors == [], line


def test_an_untracked_entry_is_an_error_in_every_status():
    """B1.2 — an entry file git does not know about is named and rejected, active or not."""
    for status in ("active", "superseded", "retired"):
        entry = memory_index.parse_entry(
            "D-old.md", f"---\nid: 14-10-old000-2026\nkind: decision\nstatus: {status}\n---\nC.\n", tracked=False
        )
        assert "not known to git, git add it first" in entry.errors, status


def test_unborn_head_and_a_revision_naming_no_commit_are_told_apart(tmp_path, monkeypatch):
    """C1.2 C1.3 — HEAD before the first commit is "nothing to check"; a revision that names no commit fails."""
    for name in [name for name in os.environ if name.startswith("GIT_")]:
        monkeypatch.delenv(name)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Unit tests")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "unit@example.invalid")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "Unit tests")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "unit@example.invalid")
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)

    assert git("init", "-b", "main").returncode == 0
    assert memory_index.head_is_unborn(repo) is True
    (repo / "a.txt").write_text("a\n")
    git("add", "-A")
    assert git("commit", "-m", "one").returncode == 0
    assert memory_index.head_is_unborn(repo) is False
    assert memory_index.rev_is_commit(repo, "HEAD") is True
    assert memory_index.rev_is_commit(repo, "no-such-rev") is False


# --- the renderer ----------------------------------------------------------------------------------------------
def test_render_is_the_exact_index_bytes():
    """B3.2 B3.3 — fixed head, one line per active entry, UTF-8, LF, one final newline."""
    entries = memory_index.active_entries([memory_index.parse_entry("D-one.md", ENTRY_TEXT)])
    assert memory_index.render_index(entries) == (
        b"# Project memory index\n\n"
        b"<!-- Generated by tools/memory_index.py from project-memory/entries/. Do not edit by hand. "
        b"Rebuild: python3 tools/memory_index.py -->\n\n"
        b"- [14-10-a1b2c3-2026](entries/D-one.md) decision: Use code-point order.\n"
    )


def test_only_active_entries_get_a_line():
    """B3.1 — superseded and retired entries are indexed by no line at all."""
    entries = [
        memory_index.parse_entry("D-one.md", ENTRY_TEXT),
        memory_index.parse_entry("D-old.md", "---\nid: 14-10-old000-2026\nstatus: superseded\n---\n"),
        memory_index.parse_entry("F-old.md", "---\nid: 14-10-retir-2026\nkind: fact\nstatus: retired\n---\n"),
    ]
    assert [entry.name for entry in memory_index.active_entries(entries)] == ["D-one.md"]


def test_render_without_active_entries_is_the_placeholder():
    """B3.2 — no active entries is a fixed line, never an empty file."""
    assert memory_index.render_index([]).endswith(b"(no active entries)\n")
    assert memory_index.render_index([]).count(b"\n") == 5  # title, blank, generated note, blank, the line


def test_size_is_measured_in_lines_and_utf8_bytes():
    """B4.2 — the reported numbers must be the file's own lines and bytes, for an accented claim included."""
    rendered = memory_index.render_index(
        memory_index.active_entries(
            [memory_index.parse_entry(
                "F-é.md", "---\nid: 14-10-accent-2026\nkind: fact\nstatus: active\n---\nCafé.\n**Why:** r\n")]
        )
    )
    lines, byte_count = memory_index.measure(rendered)
    assert (lines, byte_count) == (5, len(rendered))
    assert memory_index.size_report(rendered) == (
        f"INDEX.md: 5/{memory_index.MAX_LINES} lines, {byte_count}/{memory_index.MAX_BYTES} bytes"
    )


# --- what counts as an entry ------------------------------------------------------------------------------------
def test_links_are_percent_encoded():
    """B3.1 — a space, a `#` and a non-ASCII character must all resolve in the link."""
    assert memory_index.index_link("D-a b.md") == "entries/D-a%20b.md"
    assert memory_index.index_link("D-a b#.md") == "entries/D-a%20b%23.md"
    assert memory_index.index_link("F-é.md") == "entries/F-%C3%A9.md"


def test_only_matching_names_directly_in_the_entries_folder_are_entries():
    """B1.1 — no subfolder, no dotfile, no other prefix, no INDEX.md, no bare `D-.md`."""
    entries = "project-memory/entries"
    assert memory_index.is_entry_path(f"{entries}/D-one.md")
    assert memory_index.is_entry_path(f"{entries}/F-é a.md")
    for path in (f"{entries}/nested/D-one.md", f"{entries}/.D-hidden.md", f"{entries}/INDEX.md",
                 f"{entries}/X-hidden.md", f"{entries}/D-hidden.txt", f"{entries}/D-.md",
                 f"{entries}/D-one.markdown"):
        assert not memory_index.is_entry_path(path), path

# --- fixes from the review (run 20261012-index-md-build, N4 findings F2, F3, F5) -------------------------------
def make_memory_repo(tmp_path, monkeypatch):
    """A repository under tmp_path, git config isolated, with one staged active entry."""
    for name in [name for name in os.environ if name.startswith("GIT_")]:
        monkeypatch.delenv(name)
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", "/dev/null")
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    repo = tmp_path / "repo"
    (repo / "project-memory/entries").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=repo, check=True)
    (repo / "project-memory/entries/D-one.md").write_text(ENTRY_TEXT, encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    return repo


def test_a_tracked_entry_that_cannot_be_read_is_an_error(tmp_path, monkeypatch, capsys):
    """B2.3 — Must not 4: a tracked entry missing from the working tree is named and stops the build."""
    repo = make_memory_repo(tmp_path, monkeypatch)
    (repo / "project-memory/entries/D-one.md").unlink()
    assert memory_index.write_index(repo) == 1
    assert "D-one.md: cannot be read in the working tree" in capsys.readouterr().err
    assert not (repo / "project-memory/INDEX.md").exists()


def test_an_index_already_over_the_limit_still_warns(tmp_path, monkeypatch, capsys):
    """B4.3 — over the limit, write mode warns and exits 0, also when INDEX.md is already up to date."""
    repo = make_memory_repo(tmp_path, monkeypatch)
    monkeypatch.setattr(memory_index, "MAX_LINES", 3)
    assert memory_index.write_index(repo) == 0
    capsys.readouterr()
    assert memory_index.write_index(repo) == 0
    out = capsys.readouterr().out
    assert "is up to date" in out and "over the limit" in out


def test_an_os_error_on_the_index_is_a_problem_not_a_traceback(tmp_path, monkeypatch, capsys):
    """B2.6 — INDEX.md being a folder is reported as `<file>: <problem>` with exit 1, never a traceback."""
    repo = make_memory_repo(tmp_path, monkeypatch)
    (repo / "project-memory/INDEX.md").mkdir()
    monkeypatch.chdir(repo)
    monkeypatch.setattr(sys, "argv", ["memory_index.py"])
    assert memory_index.main() == 1
    assert "INDEX.md: " in capsys.readouterr().err
