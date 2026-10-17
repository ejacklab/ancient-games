"""Tests for item 8 — judged-merge removes the judge's /tmp folder once it has read what it needs.

`model_io.py judged-merge` reads `judge-1.json` from the judge's folder (`_judge_folder(run)`, under `/tmp`), copies
it into the run folder and, before this change, left the folder behind. The brief
(`runs/20261018-finish-everything/briefs/ev-cleanup-code.md`) says the merge removes that folder on every path that
reaches it, including when it raises after the folder was read; a missing folder is no error; only the path
`_judge_folder(run)` returns is removed, and only when it is a real directory, never a symlink.

House style: the inputs and the CLI helpers come from `test_evaluator_model_io.py`, and the run folder is built the
way `test_evaluator_r1.py`'s `judge_run` builds it — `build_run`, then renamed to a unique name, so the /tmp folder is
this test's own and never a real run's. judge-input is really run, because its output is judged-merge's input.

judged_merge's paths, each fed one case here: no judged rows (the folder is not needed); rows with a plant (call 2
required); rows with no plant (call 2 not required); and the two raises after the folder is reached.
"""
from __future__ import annotations

import shutil
import uuid
from pathlib import Path

import pytest

from test_evaluator_model_io import (CALL_ONE_MISSED, CALL_TWO_FOUND, CALC, CLEAN_QUOTE, NO_JUDGED, build_run,
                                     cli_ok, read, run_model_io, write_json)


def judge_folder(run: Path) -> Path:
    """The folder judge-input builds for call 1: outside the run folder, named after the runId."""
    return Path("/tmp") / f"evaluator-judge-{Path(run).name}"


def remove_path(path: Path) -> None:
    """Teardown: a symlink is unlinked (rmtree refuses one), a folder is removed, a missing path is nothing."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path, ignore_errors=True)


def gone(path: Path) -> bool:
    """Nothing at the path: no folder, no file, no dangling link."""
    return not path.exists() and not path.is_symlink()


@pytest.fixture
def make_run(tmp_path):
    """A factory for run folders with unique names; every /tmp path they touch is removed after the test."""
    touched: list[Path] = []

    def factory(*, classify=None, plants=None, siblings=()):
        built = build_run(tmp_path / f"root-{len(touched)}", classify=classify, plants=plants)
        run = built.parent / f"cleanup-{uuid.uuid4().hex[:12]}"
        built.rename(run)
        folder = judge_folder(run)
        remove_path(folder)
        touched.append(folder)
        touched.extend(Path(f"{folder}{suffix}") for suffix in siblings)
        return run

    yield factory
    for path in touched:
        remove_path(path)


def answered(run: Path, call_one=CALL_ONE_MISSED, call_two=CALL_TWO_FOUND) -> Path:
    """judge-input's real output, then the two judge calls' answers where DATA.md puts them (None: not written)."""
    cli_ok("judge-input", run)
    folder = judge_folder(run)
    assert folder.is_dir(), f"judge-input did not build {folder}"
    if call_one is not None:
        write_json(folder / "judge-1.json", call_one)
    if call_two is not None:
        write_json(run / "judge-2.json", call_two)
    return folder


# --- the folder is gone after a successful merge ---------------------------------------------------

def test_a_successful_merge_removes_the_judge_folder_and_keeps_call_one_in_the_run(make_run):
    """Item 8 — after judged-merge the /tmp folder is gone and judge-1.json lives on in the run folder."""
    run = make_run()
    folder = answered(run)
    result = cli_ok("judged-merge", run)
    assert result.stdout.strip() == "plant_found: true", result.stdout
    assert gone(folder), f"{folder} was left behind: {sorted(str(p) for p in folder.rglob('*'))}"
    assert (run / "judge-1.json").is_file(), "call 1's answer was not kept in the run folder"
    assert read(run / "judge-1.json") == CALL_ONE_MISSED
    judged = read(run / "judged.json")
    assert sorted(entry["case"] for entry in judged["cases"]) == ["G2-F1", "G2-F2"], judged


def test_a_merge_with_no_plant_removes_the_judge_folder_too(make_run):
    """Item 8 — with judged cases but no valid plant, call 2 is not required; the folder still goes."""
    run = make_run(plants=[])
    call_one = {"cases": [{"case": "G2-F1", "holds": True, "evidence": CLEAN_QUOTE}]}
    folder = answered(run, call_one=call_one, call_two=None)
    assert read(run / ".coordinator/plant.json")["plant_case"] is None
    result = cli_ok("judged-merge", run)
    assert result.stdout.strip() == "plant_found: false", result.stdout
    assert gone(folder), f"{folder} was left behind on the no-plant path"
    assert read(run / "judge-1.json") == call_one
    assert [entry["case"] for entry in read(run / "judged.json")["cases"]] == ["G2-F1"]


# --- the folder is gone when the merge raises after reading it ------------------------------------

def test_a_malformed_call_one_answer_still_removes_the_judge_folder(make_run):
    """Item 8 — judge-1.json that is not JSON makes the merge exit 2, and the folder is removed all the same."""
    run = make_run()
    folder = answered(run, call_one=None)
    (folder / "judge-1.json").write_text("{ this is not json", encoding="utf-8")
    result = run_model_io("judged-merge", run)
    assert result.returncode == 2, f"exited {result.returncode}: {result.stdout}{result.stderr}"
    assert "judge-1.json" in result.stderr, result.stderr
    assert gone(folder), f"{folder} was left behind after the merge raised"


def test_a_missing_call_two_answer_still_removes_the_judge_folder(make_run):
    """Item 8 — with a plant and no judge-2.json the merge exits 1 (EV-C6.2), and the folder is removed too."""
    run = make_run()
    folder = answered(run, call_two=None)
    assert not (run / "judge-2.json").exists()
    result = run_model_io("judged-merge", run)
    assert result.returncode == 1, f"exited {result.returncode}: {result.stdout}{result.stderr}"
    assert "judge-2.json" in result.stderr, result.stderr
    assert gone(folder), f"{folder} was left behind after the merge raised"


# --- a missing folder is no error where the merge does not need it --------------------------------

def test_a_missing_judge_folder_is_no_error_when_nothing_was_judged(make_run):
    """Item 8 — with no judged case the merge never needs the folder, so its absence changes nothing."""
    run = make_run(classify=NO_JUDGED)
    cli_ok("judge-input", run)
    remove_path(judge_folder(run))
    assert gone(judge_folder(run))
    result = cli_ok("judged-merge", run)
    assert result.stdout.strip() == "plant_found: true", result.stdout
    assert read(run / "judged.json") == {"plant_found": True, "cases": []}
    assert gone(judge_folder(run)), "the merge built a folder it had no use for"


# --- a symlink at the folder path is not followed --------------------------------------------------

def test_a_symlink_at_the_judge_folder_path_is_not_followed_and_its_target_survives(make_run, tmp_path):
    """Item 8 — only a real directory is removed; a symlink there must not take its target's files with it."""
    run = make_run()
    folder = answered(run)
    target = tmp_path / "symlink-target"
    shutil.move(str(folder), str(target))
    keep = target / "keep.txt"
    keep.write_text("not the evaluator's to remove\n", encoding="utf-8")
    folder.symlink_to(target, target_is_directory=True)
    assert folder.is_symlink() and (folder / "judge-1.json").is_file(), "the link was not set up"

    run_model_io("judged-merge", run)  # the exit code is not this test's rule

    assert target.is_dir(), "the symlink was followed and its target folder removed"
    assert keep.read_text(encoding="utf-8") == "not the evaluator's to remove\n"
    assert read(target / "judge-1.json") == CALL_ONE_MISSED, "the target's own files were removed"
    assert (target / "product/calc.py").is_file(), "the target's product copy was removed"
    assert (target / "judge-input.json").is_file(), "the target's judge-input.json was removed"


# --- nothing outside the folder is removed --------------------------------------------------------

def test_the_merge_removes_nothing_outside_the_judge_folder(make_run, tmp_path):
    """Item 8 — the run folder, look-alike /tmp siblings and what a link inside the folder points to all survive."""
    run = make_run(siblings=("-sibling", "x"))
    folder = answered(run)
    siblings = [Path(f"{folder}-sibling"), Path(f"{folder}x")]
    for sibling in siblings:
        sibling.mkdir()
        (sibling / "keep.txt").write_text("a look-alike name\n", encoding="utf-8")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "keep.txt").write_text("linked from inside the judge folder\n", encoding="utf-8")
    (folder / "link-out").symlink_to(outside, target_is_directory=True)
    (folder / "file-link").symlink_to(outside / "keep.txt")

    cli_ok("judged-merge", run)

    assert gone(folder), "the judge folder itself was not removed"
    for sibling in siblings:
        assert (sibling / "keep.txt").read_text(encoding="utf-8") == "a look-alike name\n", f"{sibling} was removed"
    assert (outside / "keep.txt").read_text(encoding="utf-8") == "linked from inside the judge folder\n"
    for kept in ("workspace/product/calc.py", "judge-input.json", "judge-2.json", "judged.json", "judge-1.json",
                 ".coordinator/plant.json", "requirements.json", "classify.json", "plants.json", "probes/test_b1.py"):
        assert (run / kept).is_file(), f"{kept} was removed from the run folder"
    assert (run / "workspace/product/calc.py").read_text(encoding="utf-8") == CALC
