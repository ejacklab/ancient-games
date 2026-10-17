"""Plant one break at a time in six_experts.py; each must turn at least one six-experts test red. Restores the file."""
import pathlib, subprocess, sys
F = pathlib.Path(".claude/skills/six-experts/scripts/six_experts.py")
ORIG = F.read_text(encoding="utf-8")
PLANTS = [
    ("no-shell line gone", "question names, if any. Run no shell commands — no git, no ls, no search.", "question names, if any."),
    ("vote form never read back", "return VOTE_SECTIONS if form.exists()", "return SECTIONS if form.exists()"),
    ("whole Rule, not first sentence", '(f" — {first.group(0)}" if first else "")', '(f" — {\' \'.join(rule.group(1).split())}" if rule else "")'),
    ("mcode pastes the full files under --card", 'if engine == "mcode" and card:', 'if engine == "mcode" and False:'),
    ("card not applied", "            text = card_brief(text, rule_card(lst, ident))", "            pass"),
    ("Dario gets no vote form", 'text = vote_brief(text, "Answer", "one reason per line")', "pass"),
]
results = []
try:
    for name, old, new in PLANTS:
        assert ORIG.count(old) == 1, f"plant site not found exactly once: {name}"
        F.write_text(ORIG.replace(old, new), encoding="utf-8")
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests/test_six_experts.py"], capture_output=True, text=True,
                           env={k: v for k, v in __import__("os").environ.items() if k != "NO_COLOR"})
        last = p.stdout.strip().splitlines()[-1]
        results.append((name, "KILLED" if p.returncode else "SURVIVED", last))
finally:
    F.write_text(ORIG, encoding="utf-8")
for r in results:
    print(" | ".join(r))
