"""four-experts: Linus moves from Codex to opencode when Codex has 20% or less left (EJ, 2026-10-16)."""
import argparse
import importlib.util
import json
import os
import time
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / ".claude" / "skills" / "four-experts" / "scripts" / "four_experts.py"
spec = importlib.util.spec_from_file_location("four_experts", SCRIPT)
fe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fe)

NOW = 1_792_120_000.0
LATER = NOW + 3600
EARLIER = NOW - 3600
ANSWER = "\n\n".join(s + "\nx" for s in fe.SECTIONS) + "\n"


def rollout(home, name, windows, mtime):
    """A Codex session log whose lines carry the given (primary, secondary) rate-limit snapshots, in order."""
    d = home / "sessions" / "2026" / "10" / "16"
    d.mkdir(parents=True, exist_ok=True)
    f = d / name
    lines = [json.dumps({"type": "event_msg", "payload": {"type": "token_count", "rate_limits": {
        "limit_id": "premium", "primary": p, "secondary": s}}}) for p, s in windows]
    f.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.utime(f, (mtime, mtime))
    return f


def window(used, resets_at):
    return {"used_percent": used, "window_minutes": 300, "resets_at": resets_at}


def test_codex_left_is_the_lower_window(tmp_path):
    rollout(tmp_path, "a.jsonl", [(window(85.0, LATER), window(47.0, LATER))], NOW)
    assert fe.codex_left(tmp_path, NOW) == 15.0


def test_codex_left_counts_a_reset_window_as_full(tmp_path):
    rollout(tmp_path, "a.jsonl", [(window(100.0, EARLIER), window(47.0, LATER))], NOW)
    assert fe.codex_left(tmp_path, NOW) == 53.0


def test_codex_left_skips_a_snapshot_with_no_windows(tmp_path):
    rollout(tmp_path, "old.jsonl", [(window(90.0, LATER), window(10.0, LATER))], NOW - 100)
    rollout(tmp_path, "new.jsonl", [(None, None)], NOW)
    assert fe.codex_left(tmp_path, NOW) == 10.0


def test_codex_left_is_none_with_no_logs(tmp_path):
    assert fe.codex_left(tmp_path, NOW) is None


class FakeProc:
    def __init__(self, rc):
        self.returncode = rc

    def poll(self):
        return self.returncode


def run_linus(tmp_path, monkeypatch, left, outcomes):
    """Run only Linus with fake engines; outcomes maps engine -> (exit, answer text, log text)."""
    calls = []

    def fake_start(engine, prompt, ans, log, timeout, web, shell, cwd):
        calls.append(engine)
        rc, ans_text, log_text = outcomes[engine]
        ans.write_text(ans_text, encoding="utf-8")
        log.write_text(log_text, encoding="utf-8")
        return FakeProc(rc), time.time()

    seat = tmp_path / "seat.md"
    seat.write_text("## Final list\n\n1. **one**\n", encoding="utf-8")
    monkeypatch.setattr(fe, "seat_files", lambda sid: (seat, seat))
    monkeypatch.setattr(fe, "codex_left", lambda *args, **kwargs: left)
    monkeypatch.setattr(fe, "start", fake_start)
    monkeypatch.setattr(fe.time, "sleep", lambda s: None)
    monkeypatch.chdir(tmp_path)
    out = tmp_path / "run"
    a = argparse.Namespace(question="q?", question_file=None, out=str(out), needs_web=False, needs_shell=False,
                           timeout=60, progress=None, only="linus", claude_by_caller=True)
    rc = fe.run(a)
    return rc, calls, json.loads((out / "status.json").read_text(encoding="utf-8"))


def test_linus_moves_to_opencode_at_20_percent_left(tmp_path, monkeypatch):
    rc, calls, status = run_linus(tmp_path, monkeypatch, 20.0, {"opencode": (0, ANSWER, "")})
    assert calls == ["opencode"]
    assert rc == 0
    assert status["linus"]["engine"] == "opencode"
    assert status["linus"]["fallback_from"] == "codex"
    assert "20" in status["linus"]["fallback_reason"]


def test_linus_stays_on_codex_above_20_percent_left(tmp_path, monkeypatch):
    rc, calls, status = run_linus(tmp_path, monkeypatch, 21.0, {"codex": (0, ANSWER, "")})
    assert calls == ["codex"]
    assert status["linus"]["engine"] == "codex"


def test_linus_falls_back_when_codex_hits_its_usage_limit(tmp_path, monkeypatch):
    limit = "ERROR: You've hit your usage limit. ... try again at 2:37 PM.\n"
    rc, calls, status = run_linus(tmp_path, monkeypatch, None,
                                  {"codex": (1, "", limit), "opencode": (0, ANSWER, "")})
    assert calls == ["codex", "opencode"]
    assert rc == 0
    assert status["linus"]["engine"] == "opencode"
    assert status["linus"]["fallback_from"] == "codex"
    assert status["linus-codex"]["ok"] is False
    assert (tmp_path / "run" / "logs" / "linus.codex-failed.log").exists()


def test_linus_other_codex_failure_does_not_fall_back(tmp_path, monkeypatch):
    rc, calls, status = run_linus(tmp_path, monkeypatch, None, {"codex": (1, "", "ERROR: model not found\n")})
    assert calls == ["codex"]
    assert rc == 1
    assert status["linus"]["engine"] == "codex"
