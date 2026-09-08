"""Reproduction for docs/DKIND_MIRROR_RESEARCH.md §2, kept as a living check now that §8 has
landed. Run from the repo root: python3 docs/research/dkind_bypass_repro.py

BEFORE the fix, the three cases printed:
  A  record_claim, executable + closed_world  -> override seen, commit REFUSED by the grant
  B  ingest_return, executable, no reason     -> override NOT seen, commit SUCCEEDED
  (C did not exist: a helper could not state a reason, because nothing asked it for one.)

AFTER: B is recorded as `judgment` — the cheap label is gone, so the helper's own checks no
longer corroborate it — and C, the helper's override in writing, is refused by the same grant
that refuses MAIN's. The honest path and the silent path now get the same answer."""
import os, sys, tempfile
sys.path.insert(0, ".")
from ablation import fixtures
from ancient_games.ctx import Ctx
from ancient_games.journal import Journal, kind_overrides
from ancient_games.hybrid.registry import load_tools
from ancient_games.hybrid.tools import commit as CM, dispatch as D, ingest_return as I, record_claim as R
from ancient_games.hybrid.types import ToolEnv

TOOLS = load_tools()
TEXT = "the six helpers are dead — nothing calls them"
CW = "AST over every .py + grep for the name as a string + no getattr/globals() idioms"

def setup(tag):
    d = tempfile.mkdtemp()
    repo = fixtures.make_uc2(os.path.join(d, "repo"))
    open(os.path.join(repo, "loop", "main.py"), "a").write("# edit\n")
    jp = os.path.join(d, f"{tag}.jsonl")
    env = ToolEnv(tag, jp, Ctx(actor={"land": "MAIN"}), cwd=repo, tools=TOOLS)
    j = Journal(jp, tag)
    j.append({"event": "preauthorization_recorded", "grant_id": "grant:1", "approver": "owner",
              "scope_paths": ["**"], "max_uses": 1, "allow_kind_overrides": False,
              "note": "unattended commit, but NOT under a D-KIND override"})
    return env, j

def report(label, env, j):
    ov = kind_overrides(j.read(), env.run_id)
    ev = [e for e in j.read() if e["event"] == "claim_recorded"][0]
    r = CM.run(env, {"message": "land it"})
    print(f"{label}\n  recorded kind = {ev['kind']}, kind_override = {ev['kind_override']}"
          f", closed_world = {ev['closed_world'] is not None}")
    print(f"  kind_overrides() sees = {len(ov)}")
    print(f"  commit -> ok={r.ok}  {('reason: ' + str(r.reason)) if not r.ok else 'COMMITTED ' + r.value['hash'][:8]}\n")

# A: MAIN records it, declaring executable with a closed_world reason (the disclosed path)
env, j = setup("dk-main")
R.run(env, {"claim_id": "C1", "author": "MAIN", "actor": "agent-x", "kind": "executable", "text": TEXT,
            "evidence_type": "command", "evidence_ref": "$ grep -r", "closed_world": CW})
report("A  record_claim, executable + closed_world:", env, j)

# B: a dispatched agent returns the identical claim, declaring executable itself, no reason given
env, j = setup("dk-agent")
D.run(env, {"role": "researcher", "framing": "f1", "agent_id": "adv-1"})
I.run(env, {"agent_id": "adv-1", "actor": "agent-x", "framing": "f1",
            "fields": {"CLAIMS": [{"claim_id": "C1", "kind": "executable", "text": TEXT,
                                   "evidence_type": "command", "evidence_ref": "$ grep -r"}]}})
report("B  ingest_return, executable self-declared, no reason:", env, j)

# C: the same helper, stating why its check space is complete — the ratified policy
env, j = setup("dk-agent-cw")
D.run(env, {"role": "researcher", "framing": "f1", "agent_id": "adv-1"})
I.run(env, {"agent_id": "adv-1", "actor": "agent-x", "framing": "f1",
            "fields": {"CLAIMS": [{"claim_id": "C1", "kind": "executable", "text": TEXT,
                                   "evidence_type": "command", "evidence_ref": "$ grep -r",
                                   "closed_world": CW}]}})
report("C  ingest_return, executable + closed_world:", env, j)
