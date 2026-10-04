"""Deterministic code/test engine assignment — EJ, 2026-10-04: 60% opencode, 40% codex.

Why this is a design-time rule and not a run-time one: `docs/DISPATCHER_DESIGN.md` §5 records EJ's decision that
there is no run-time routing fork and no decision model — the plan names one engine per node and the dispatcher
executes it without choosing. So the split happens while the plan is written, the plan still names one engine per
node, and nothing about the dispatcher changes.

The rule, and why it has this shape
-----------------------------------
A module is a unit of work with a code node and (usually) a test node. Two things are wanted at once:

1. **Load** — 60% of build nodes on opencode, 40% on codex.
2. **Independent tests** — a module's tests should be written by the engine that did *not* write its code. That is
   what today's single-engine runs do not get, and it is free wherever the budget allows.

These conflict, and the conflict is exact: **crossing every pair gives 50/50, always**, because each pair then
sends exactly one node to each engine — whatever the share of primaries. So 60/40 buys fewer independent pairs
than 50/50 does, and the question is only how few it has to be.

For N paired modules and share `s` for the primary engine: cross every module the *other* engine primaries, then
cross as many primary modules as the budget still allows. The remainder must self-test, on the primary side:

    self-tested fraction = 2s - 1        (0.20 at s = 0.6)
    independent fraction = 2 - 2s        (0.80 at s = 0.6)

At s = 0.6 the pattern is periodic in 5 modules — three primary, two other — with the third primary module
self-testing. That is the maximum independence available at that share, not a compromise chosen by hand:

| module | code     | tests    | independent |
|--------|----------|----------|-------------|
| 1      | opencode | codex    | yes         |
| 2      | opencode | codex    | yes         |
| 3      | opencode | opencode | **no**      |
| 4      | codex    | opencode | yes         |
| 5      | codex    | opencode | yes         |

Evidence for the basis
----------------------
The share is EJ's decision on n=1: one POC run of opencode + MiniMax-M3.1-Flash-Preview passed 19/19 objective
checks (`runs/20261004-opencode-poc/README.md`). It is a policy, not a measurement. Record the split in the
ledger so the next run compares the engines on the same work instead of trusting this number.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

TEST_MARKERS = ("test", "tests")


def module_of(node: dict) -> str:
    """The unit a node belongs to. An explicit `module` wins; otherwise the id without its last `-segment`."""
    if node.get("module"):
        return str(node["module"])
    nid = str(node.get("id", ""))
    return nid.rsplit("-", 1)[0] if "-" in nid else nid


def kind_of(node: dict) -> str:
    """`test` or `code`. An explicit `kind` wins; otherwise the role, then the id, is read for a test marker."""
    if node.get("kind") in ("code", "test"):
        return node["kind"]
    hay = f"{node.get('role', '')} {node.get('id', '')}".lower()
    return "test" if any(m in hay for m in TEST_MARKERS) else "code"


def assign(nodes: list[dict], share: float = 0.6, primary: str = "opencode",
           other: str = "codex") -> dict[str, str]:
    """Return {node id: engine} for the build nodes. Deterministic: same nodes in, same map out.

    Sorted by module id, so the assignment does not depend on the plan's node order — adding a node does not
    silently re-shuffle every other one's engine.
    """
    if not 0.0 <= share <= 1.0:
        raise ValueError("share must be between 0 and 1")
    modules: dict[str, dict[str, dict]] = {}
    for n in nodes:
        modules.setdefault(module_of(n), {})[kind_of(n)] = n
    order = sorted(modules)
    n_mod = len(order)

    # `p` is the share of modules whose *code* goes to the primary engine. It is not the node share: the node
    # share also counts the tests, and the primary engine picks up tests from every other-primary module.
    #     primary nodes = p*N (codes) + a*N (its own module's tests) + (1-p)*N (crossed tests) = N(1+a)
    # so the node share is (1+a)/2, and hitting share `s` means a = 2s-1 exactly. `p` only has to be >= a.
    want_primary_code = round(share * n_mod)
    self_n = max(0, min(want_primary_code, round((2 * share - 1) * n_mod)))
    first_self = want_primary_code - self_n

    out: dict[str, str] = {}
    for i, mod in enumerate(order):
        code, test = modules[mod].get("code"), modules[mod].get("test")
        primary_code = i < want_primary_code
        # The self-testing modules are the last `self_n` of the primary ones, which is what makes the periodic
        # s=0.6 case come out as cross, cross, self, cross, cross.
        self_test = primary_code and i >= first_self
        if code:
            out[code["id"]] = primary if primary_code else other
        if test:
            out[test["id"]] = primary if (self_test or not primary_code) else other

    # A module with only one node cannot be crossed, so it is steered to whichever engine is furthest behind.
    target_primary = round(share * (len(out) + sum(1 for m in order if len(modules[m]) == 1)))
    for mod in order:
        if len(modules[mod]) != 1:
            continue
        only = next(iter(modules[mod].values()))
        have = sum(1 for e in out.values() if e == primary)
        remaining_primary = sum(1 for m in order if m > mod and len(modules[m]) == 1)
        want = target_primary - have
        out[only["id"]] = primary if want > remaining_primary / 2 else other
    return out


def check(nodes: list[dict], engines: dict[str, str], share: float = 0.6, primary: str = "opencode",
          other: str = "codex") -> list[str]:
    """Findings about a proposal. Empty means the split is balanced and no module grades its own tests."""
    f: list[str] = []
    build = {n["id"]: engines[n["id"]] for n in nodes if n["id"] in engines}
    if not build:
        return ["no build nodes to assign"]
    n_primary = sum(1 for e in build.values() if e == primary)
    got = n_primary / len(build)
    if abs(got - share) > 0.05:
        f.append(f"share is {got:.0%} on {primary}, wanted {share:.0%} (±5 points)")

    modules: dict[str, dict[str, str]] = {}
    for n in nodes:
        if n["id"] in engines:
            modules.setdefault(module_of(n), {})[kind_of(n)] = engines[n["id"]]
    # A module may grade its own tests only up to the budget the share forces: 2s-1 of them. At 60/40 that is one
    # module in five, so a correct plan is clean and a plan that self-tests everything is not.
    self_tested = [m for m, g in sorted(modules.items())
                   if g.get("code") and g.get("code") == g.get("test")]
    budget = round((2 * share - 1) * len(modules))
    if len(self_tested) > budget:
        f.append(f"{len(self_tested)} module(s) grade their own tests ({', '.join(self_tested)}); a "
                 f"{share:.0%} share forces at most {budget}")
    # rule 5: a node's verifier must be a different kind from the node's worker
    for n in nodes:
        v = n.get("verified_by") or n.get("verifier")
        if v and n["id"] in engines and engines.get(v) and engines[v] == engines[n["id"]]:
            f.append(f"{n['id']}: verifier {v} runs the same engine ({engines[v]}) — rule 5")
    return f


def render(nodes: list[dict], engines: dict[str, str]) -> str:
    """The assignment as a table, so the plan's reader can see it was assigned rather than chosen."""
    modules: dict[str, dict[str, dict]] = {}
    for n in nodes:
        if n["id"] in engines:
            modules.setdefault(module_of(n), {})[kind_of(n)] = n
    lines = [f"  {'module':16} {'code':10} {'tests':10} independent"]
    self_n = 0
    for mod in sorted(modules):
        got = modules[mod]
        code = engines.get(got.get("code", {}).get("id", ""), "-")
        test = engines.get(got.get("test", {}).get("id", ""), "-")
        indep = "yes" if code != test else "NO (self-tested)"
        self_n += code == test
        lines.append(f"  {mod:16} {code:10} {test:10} {indep}")
    counts: dict[str, int] = {}
    for e in engines.values():
        counts[e] = counts.get(e, 0) + 1
    total = sum(counts.values())
    lines.append("  " + "  ".join(f"{e} {c}/{total} ({c/total:.0%})" for e, c in sorted(counts.items())))
    lines.append(f"  independently tested modules: {len(modules)-self_n}/{len(modules)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--plan", required=True, help="plan JSON with a `nodes` array")
    ap.add_argument("--share", type=float, default=0.6, help="primary engine's share (default 0.6)")
    ap.add_argument("--primary", default="opencode")
    ap.add_argument("--other", default="codex")
    ap.add_argument("--write", action="store_true", help="write the engines back into the plan")
    args = ap.parse_args(argv)

    path = pathlib.Path(args.plan)
    plan = json.loads(path.read_text())
    nodes = plan["nodes"]
    engines = assign(nodes, args.share, args.primary, args.other)
    print(render(nodes, engines))
    findings = check(nodes, engines, args.share, args.primary, args.other)
    for finding in findings:
        print(f"  FINDING: {finding}")
    if args.write:
        for n in nodes:
            if n["id"] in engines:
                n["engine"] = engines[n["id"]]
                n["engine_assigned_by"] = f"workload.py share={args.share} ({args.primary}/{args.other})"
        path.write_text(json.dumps(plan, indent=2) + "\n")
        print(f"  wrote engines into {path}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
