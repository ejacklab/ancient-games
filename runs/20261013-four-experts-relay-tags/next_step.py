#!/usr/bin/env python3
"""next_step.py N PREV_ANSWER — cut `### The copy` out of the previous step's answer into copy-<N-1>.md and write
q-step<N>.md (relay header + the copy, authors' names removed + facts.md). Written by the main agent (Claude)."""
import re, sys
from pathlib import Path
D = Path(__file__).parent
n, prev = int(sys.argv[1]), Path(sys.argv[2])
text = prev.read_text()
m = re.search(r"^### The copy\s*\n(.*?)(?=^## How I decided)", text, re.S | re.M)
if not m:
    sys.exit(f"no '### The copy' section in {prev}")
copy = m.group(1).strip()
(D / f"copy-{n-1}.md").write_text(copy + "\n")
q = f"""# Question

This is a relay. Earlier experts have written and improved a proposal, one at a time; you are step {n} of 5. Improve
the **same copy**: keep what is right, change what is wrong, add what is missing, remove what is more than needed.

The repo has several different sets of trust tags for research findings. They should be one set. The copy proposes
which set is official, where it lives, what each tag means, the rule for when two tags seem to fit, which files
change, and what happens to old files.

In your `## Answer` section: one or two sentences on what you changed, then a heading `### The copy` containing the
**complete** improved proposal — not a diff, not a list of edits. Under `## How I decided`, list each change as kept /
changed / added / removed, with the item that drove it. Do not search the web; work from the copy and the facts below.

# The current copy

{copy}

"""
(D / f"q-step{n}.md").write_text(q + (D / "facts.md").read_text())
print(f"copy-{n-1}.md: {len(copy.splitlines())} lines; q-step{n}.md written")
