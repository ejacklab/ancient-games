"""Format token test result: text tokens per format per engine = prompt tokens - the engine's baseline call.
Uses the parsers in ../engines_result.py; codex baseline is codex/baseline.jsonl (15,054, the stable re-take)."""
import pathlib, sys
here = pathlib.Path(__file__).parent; root = here.parent
src = (root / "engines_result.py").read_text().split("engines = {")[0]
exec(src)  # defines codex, agy, claude, opencode, dsh parsers
E = {"claude": (claude, root / "claude/baseline.json"), "codex": (codex, root / "codex/baseline.jsonl"),
     "agy": (agy, root / "agy/baseline.json"), "opencode": (opencode, root / "opencode/baseline.jsonl"),
     "dsh": (dsh, root / "dsh/baseline.jsonl")}
FM = ["markdown", "xml", "json_indented", "json_compact"]
rows = [f"{'engine':9} " + " ".join(f"{f:>15}" for f in FM)]
for e, (fn, base) in E.items():
    try:
        b = fn(base); n = {f: fn(here / f"{e}-{f}.out") - b for f in FM}
    except Exception as ex:
        rows.append(f"{e:9} not ready ({ex.__class__.__name__})"); continue
    rows.append(f"{e:9} " + " ".join(f"{n[f]:6} ({n[f]/n['markdown']:.2f}x)" for f in FM))
print("\n".join(rows)); (here / "result.txt").write_text("\n".join(rows) + "\n")
