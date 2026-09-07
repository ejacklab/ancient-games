"""NEW — `commit(message)`. I1′/I4′(b) are checked by the loop before this body runs;
the body checks its own checkpoint precondition (an in-window
`approval_recorded{gate=checkpoint, action_id=commit:['master']}`, K4) — the refusal
names every D-KIND `closed_world` override in this run for the gate to see — and only
then stages the changed files and runs `git commit`. Never raises; git's own
stderr is the reason on failure."""
from ancient_games.journal import Journal, kind_overrides

from ..types import ToolResult
from ._shared import (COMMIT_ACTION_ID_ARGS, action_id, approvals_after, changed_files, git, internal_error,
                      last_commit_index, require_str)

MANIFEST = {
    "name": "commit", "inputs": {"message": "str"}, "outputs": "{hash}",
    "side_effects": "commit", "cost": "cheap", "participates_in": ["I1", "I4"], "entrypoint": "run",
}


def overrides_note(events: list[dict], run_id: str) -> str:
    """D-KIND: the checkpoint gate shows every claim whose author overrode the rule's `judgment` to
    `executable`, with the `closed_world` reason verbatim, so the human accepts or rejects it there."""
    ov = kind_overrides(events, run_id)
    if not ov:
        return ""
    return "; kind overrides for the gate to accept or reject: " + "; ".join(
        f"{o['claim_id']} (executable by closed_world: {o['closed_world']!r})" for o in ov)


def run(env, args):
    bad = require_str(args, "message")  # before the try: a missing message is the caller's error
    if bad is not None:
        return bad
    try:
        events = Journal(env.journal_path, env.run_id).read()
        aid = action_id(*COMMIT_ACTION_ID_ARGS)
        if not approvals_after(events, "checkpoint", aid, last_commit_index(events)):
            return ToolResult(ok=False, reason="checkpoint-not-cleared" + overrides_note(events, env.run_id))
        changed = changed_files(env.cwd)
        if changed:
            p = git(env.cwd, "add", "--", *changed)
            if p.returncode != 0:
                return ToolResult(ok=False, reason=p.stderr.strip())
        p = git(env.cwd, "commit", "-m", args["message"])
        if p.returncode != 0:
            return ToolResult(ok=False, reason=(p.stderr.strip() or p.stdout.strip()))
        return ToolResult(ok=True, value={"hash": git(env.cwd, "rev-parse", "HEAD").stdout.strip()})
    except Exception as e:
        return internal_error(e)
