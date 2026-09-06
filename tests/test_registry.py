"""§3 — matching semantics, specificity suppression, the D2′ union."""
from __future__ import annotations

from ancient_games.ctx import ArtifactRef
from ancient_games.registry import REGISTRY, direct_matches, lookup, row_by_id


def _ids(matches):
    return [m.row.id for m in matches]


def test_nine_rows_with_the_spec_columns():
    assert [r.id for r in REGISTRY] == [f"R{i}" for i in range(1, 10)]
    assert row_by_id("R7").hub is False and row_by_id("R7").stakes == 2
    assert row_by_id("R6").verb == "commit" and row_by_id("R6").kind == "action"
    assert row_by_id("R9").pattern == () and row_by_id("R9").owner == "ej"


def test_dir_prefix_match():
    assert _ids(direct_matches(ArtifactRef("engine/liquidity.py", "mutate"))) == ["R7"]
    assert _ids(direct_matches(ArtifactRef("research/stability.py", "mutate"))) == ["R8"]
    assert _ids(direct_matches(ArtifactRef("config.py", "mutate"))) == ["R7"]  # a file key in a dir-kind row still prefix-matches
    assert _ids(direct_matches(ArtifactRef("docs/x.md", "mutate"))) == []


def test_file_exact_match_beats_dir_prefix():
    # eval/protocol.json matches R1 (file) and R7 (eval/ dir): the specific row wins, the generic is suppressed
    assert _ids(direct_matches(ArtifactRef("eval/protocol.json", "mutate"))) == ["R1"]
    assert _ids(direct_matches(ArtifactRef("eval/protocol.jsonx", "mutate"))) == ["R7"]  # not exact → dir only


def test_callable_matches_only_on_invoke():
    assert _ids(direct_matches(ArtifactRef("eval.partitions.load_holdout", "invoke"))) == ["R3"]
    assert _ids(direct_matches(ArtifactRef("eval.partitions.load_holdout", "mutate"))) == []


def test_action_verb_match():
    assert _ids(direct_matches(ArtifactRef("master", "mutate", verb="commit"))) == ["R6"]
    assert _ids(direct_matches(ArtifactRef("master", "mutate", verb="push"))) == []


def test_read_is_never_matched():
    assert direct_matches(ArtifactRef("eval/protocol.json", "read")) == []
    assert tuple(lookup([ArtifactRef("eval/protocol.json", "read")])) == (1, [], "none", None)


def test_r9_per_instance_suppresses_r7_on_same_ref():
    # Case 1: config.py's backoff constant reaches Binance rate-limit state
    ref = ArtifactRef("config.py", "mutate", external_state="Binance-rate-limit-state")
    assert _ids(direct_matches(ref)) == ["R9"]
    stakes, hubs, gate, owner = lookup([ref])
    assert (stakes, hubs, gate, owner) == (3, ["Binance-rate-limit-state"], "owner", "ej")


def test_d2_prime_union_with_registered_consumer():
    # T1: direct R7 (dir, hub?=no) ∪ consumer R4 (file, hub?=yes) → one hub, stakes max(2,2)=2
    ref = ArtifactRef("loop/program_db.py", "mutate", consumers=("loop/program_db.jsonl",))
    hit = lookup([ref])
    assert hit.row_ids == ["R7", "R4"]
    assert tuple(hit) == (2, ["loop/program_db.jsonl"], "checkpoint", None)
    assert hit.consumer_answer == "R4"
    # Case (i): direct R8 (stakes 1) ∪ consumer R1 (stakes 3, hub?=yes) → stakes 3, hub=[eval/protocol.json]
    hit = lookup([ArtifactRef("research/report.py", "mutate", consumers=("eval/protocol.json",))])
    assert hit.row_ids == ["R8", "R1"]
    assert tuple(hit) == (3, ["eval/protocol.json"], "owner", "ej")


def test_consumer_in_the_disposable_tier_does_not_elevate():
    # a consumer that is itself stakes-1 (research/) is not a registered stakes≥2 row → no union element
    hit = lookup([ArtifactRef("research/report.py", "mutate", consumers=("research/stability.py",))])
    assert hit.row_ids == ["R8"] and tuple(hit) == (1, [], "none", None) and hit.consumer_answer == "no"


def test_generic_dir_alone_contributes_no_hub_but_still_gates():
    hit = lookup([ArtifactRef("engine/liquidity.py", "mutate")])
    assert tuple(hit) == (2, [], "checkpoint", None)


def test_stakes_is_max_over_both_sets_hub_notwithstanding():
    hit = lookup([ArtifactRef("engine/x.py", "mutate"), ArtifactRef("master", "mutate", verb="commit")])
    assert tuple(hit) == (2, ["default-branch-history"], "checkpoint", None)
    hit = lookup([ArtifactRef("eval/holdout_access.log", "invoke")])
    assert tuple(hit) == (3, ["eval/holdout_access.log"], "owner", "ej")


def test_default_when_nothing_matches():
    assert tuple(lookup([ArtifactRef("docs/README.md", "mutate")])) == (1, [], "none", None)
