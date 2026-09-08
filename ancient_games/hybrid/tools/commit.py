"""NEW — `commit(message)`. I1′/I4′(b) are checked by the loop before this body runs;
the body checks its own checkpoint precondition (an in-window
`approval_recorded{gate=checkpoint, action_id=commit:['master']}`, K4) — the refusal
names every D-KIND `closed_world` override in this run for the gate to see — and only
then stages the changed files and runs `git commit`. Never raises; git's own
stderr is the reason on failure."""
from ancient_games.journal import Journal, kind_overrides

from .. import autonomy
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
        journal = Journal(env.journal_path, env.run_id)
        events = journal.read()
        aid = action_id(*COMMIT_ACTION_ID_ARGS)
        overrides = kind_overrides(events, env.run_id)
        grant, changed = None, None
        if not approvals_after(events, "checkpoint", aid, last_commit_index(events)):
            # AUTONOMY_DESIGN v2 §5: a pre-authorisation is evaluated FRESH, here, against the
            # paths actually about to be committed. It mints no approval — every commit shares the
            # constant action_id ("commit", ["master"]), so a stored derived approval would sit
            # in-window and clear a LATER commit whose paths its scope never covered.
            # `changed_files` shells out to git, so it stays behind the grants check: with no grant
            # on record this reports `checkpoint-not-cleared` without needing a repo at all, which
            # is what it did before pre-authorisation existed.
            if not autonomy.grants(events):
                return ToolResult(ok=False, reason="checkpoint-not-cleared" + overrides_note(events, env.run_id))
            changed = changed_files(env.cwd)
            grant, why = autonomy.live_grant(events, changed, bool(overrides))
            if grant is None:
                note = f"; no live pre-authorisation: {why}" if why else ""
                return ToolResult(ok=False, reason="checkpoint-not-cleared"
                                  + overrides_note(events, env.run_id) + note)
        if changed is None:
            changed = changed_files(env.cwd)  # BEFORE the commit; afterwards the tree is clean
        if changed:
            p = git(env.cwd, "add", "--", *changed)
            if p.returncode != 0:
                return ToolResult(ok=False, reason=p.stderr.strip())
        p = git(env.cwd, "commit", "-m", args["message"])
        if p.returncode != 0:
            return ToolResult(ok=False, reason=(p.stderr.strip() or p.stdout.strip()))
        if grant is not None:
            _record_grant_use(journal, grant, aid, changed, overrides)
        return ToolResult(ok=True, value={"hash": git(env.cwd, "rev-parse", "HEAD").stdout.strip()})
    except Exception as e:
        return internal_error(e)


def _record_grant_use(journal, grant, aid: str, changed: list[str], overrides: list[dict]) -> None:
    """Audit records, written only AFTER `git commit` returned 0 — they authorise nothing and
    `run`'s explicit-approval branch never reads them (§5.2).

    A commit taken under a grant is a commit no human saw, so each D-KIND `closed_world` override
    that would have been surfaced verbatim in the refusal is queued instead of shown: `deferred_
    decision` is the record that the disclosure happened with nobody reading it (§6). It is a
    record, not a gate — nothing downstream reads it back."""
    journal.append({"event": "approval_derived", "grant_id": grant["grant_id"], "action_id": aid,
                    "approver": grant["approver"], "paths": list(changed)})
    for o in overrides:
        journal.append({"event": "deferred_decision", "kind": "kind-override",
                        "payload": f"{o['claim_id']} (executable by closed_world: {o['closed_world']!r})",
                        "boundary": aid,
                        "reason": f"committed under pre-authorisation {grant['grant_id']}; not reviewed at a gate"})
