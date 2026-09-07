"""§4 B·1 + hybrid v1.1 D-B (one author, one source): `count_sources` gives MAIN at most one
contribution per claim across (a) and (b). Asserted on the real function's return."""
from ancient_games.journal import Journal
from ancient_games.stages import CapState, Claim, count_sources


def test_main_counts_once_when_qualifying_under_both_a_and_b(tmp_path):
    j = Journal(str(tmp_path / "j.jsonl"), "db")
    # actor is an agent; MAIN records a command-backed claim with its own distinct framing
    j.claim_recorded("c", "MAIN", "designer", "judgment", "t", "command", "python3 -m pytest -q", framing="executed-check")
    claim = Claim("c", "judgment", n_required=2, stakes=2, actor="designer")
    n, remedy = count_sources(claim, j.read(), CapState(0), [])
    assert (n, remedy) == (1, "gate-checkpoint")  # was 2 under v1.0 ((a) framing + (b) once more)
    # a second, non-MAIN author with a distinct framing adds one; MAIN still contributes one
    j.claim_recorded("c", "reviewer-2", "designer", "judgment", "t", "file:line", "/agents/reviewer-2.md:1", framing="review")
    assert count_sources(claim, j.read(), CapState(0), []) == (2, None)


def test_main_still_counts_via_b_when_actor_is_main_excluded_from_a(tmp_path):
    """Unchanged: with actor=MAIN, MAIN's own event fails both (a) and (b) — nothing to double count."""
    j = Journal(str(tmp_path / "j.jsonl"), "db")
    j.claim_recorded("c", "MAIN", "MAIN", "judgment", "t", "command", "grep", framing="scan")
    j.claim_recorded("c", "historian", "MAIN", "judgment", "t", "file:line", "/agents/h.md:1", framing="read")
    assert count_sources(Claim("c", "judgment", n_required=2, stakes=2, actor="MAIN"), j.read(), CapState(1), ["x"]) == (1, "add-differently-framed-source")
