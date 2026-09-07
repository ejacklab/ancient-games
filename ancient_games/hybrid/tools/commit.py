"""NEW — `commit(message)`. I1′/I4′(b) are checked by the loop before this body runs;
the body checks its own checkpoint precondition (an in-window
`approval_recorded{gate=checkpoint, action_id=commit:['master']}`, K4) and only
then stages the changed files and runs `git commit`. Never raises; git's own
stderr is the reason on failure."""
from ancient_games.journal import Journal

from ..types import ToolResult
from ._shared import (COMMIT_ACTION_ID_ARGS, action_id, approvals_after, diff_name_only_head, git, internal_error,
                      last_commit_index)

MANIFEST = {
    "name": "commit", "inputs": {"message": "str"}, "outputs": "{hash}",
    "side_effects": "commit", "cost": "cheap", "participates_in": ["I1", "I4"], "entrypoint": "run",
}


def run(env, args):
    try:
        events = Journal(env.journal_path, env.run_id).read()
        aid = action_id(*COMMIT_ACTION_ID_ARGS)
        if not approvals_after(events, "checkpoint", aid, last_commit_index(events)):
            return ToolResult(ok=False, reason="checkpoint-not-cleared")
        changed = diff_name_only_head(env.cwd)
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
