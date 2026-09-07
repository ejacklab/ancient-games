"""Dispatch an agent: `stages.dispatch_source` when it counts toward CAP (B·3, increments
`ctx.dispatch_count`), else `journal.dispatch`. Generates `agent_id` as
`{role}-{framing}-{uuid4().hex[:8]}` (DECISIONS_HYBRID_4); a scripted case may pass one."""
import uuid

from ancient_games.journal import Journal
from ancient_games.stages import dispatch_source

from ..types import ToolResult
from ._shared import internal_error

MANIFEST = {
    "name": "dispatch", "inputs": {"role": "str", "framing": "str", "payload": "dict", "counts_toward_cap": "bool", "agent_id": "str"},
    "outputs": "agent_id", "side_effects": "invoke", "cost": "agent", "participates_in": ["I5"], "entrypoint": "run",
}


def run(env, args):
    try:
        journal = Journal(env.journal_path, env.run_id)
        role, framing = args["role"], args["framing"]
        agent_id = args.get("agent_id") or f"{role}-{framing}-{uuid.uuid4().hex[:8]}"
        payload = args.get("payload") or {}
        if args.get("counts_toward_cap", True):
            dispatch_source(env.ctx, journal, agent_id, framing, role)
        else:
            journal.dispatch(agent_id, role, framing, sorted(payload) or ["INTENT", "STOP", "FRAMING", "OUTPUT"],
                             f"/agents/{agent_id}.md")
        return ToolResult(ok=True, value=agent_id)
    except Exception as e:
        return internal_error(e)
