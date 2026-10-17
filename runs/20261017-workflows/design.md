# Design — two workflows for the plan-B pattern (run 20261017-workflows)

Both are saved in `.claude/workflows/` and run with the Workflow tool (`{name, args}`). Every step is an agent, because
the script API has no plain shell step (workflow-authoring reference). A step that only runs a command uses
`claude-haiku-5-5` at `effort: low`; a step that reads and writes uses the session model.

**The clock.** A script cannot read the time. Every step's agent first runs
`bun .claude/skills/workflow-design/guard/src/cli.ts deadline status`. When that exits 1 ("time is up") the step returns
`{time_up: true}` and does nothing; the script then starts no further step and returns what it has, with
`stopped: "time is up"`. With no deadline recorded (exit 2), the step proceeds.

**Progress.** The six-experts runner writes `--progress` lines per expert; every other step appends one line to
`<run>/nodes/<workflow>.progress.md` as it starts and ends (the node-brief format), so `deadline status` shows it.

## experts-decide

args: `{run: "runs/<id>", question: "<path inside the repo>", out: "<subfolder>", only?: ["linus", …],
insights?: "instruction,check", needsWeb?: bool, research?: "<a research question>"}`

| Step | Agent | Does | Returns |
|---|---|---|---|
| Research (only with `research`) | session model | answers the research question from the web, findings labelled verified/reported, writes `<run>/research/<out>.md` | `{time_up, file, digest}` |
| Ask, one per expert | haiku, low | `six_experts.py run --question-file Q --out <run>/<out>/<sid> --only <sid> [--insights] [--needs-web] --progress <run>/nodes/<out>.progress.md --timeout 540 </dev/null` (timeout 580) | `{time_up, sid, exit, ok, answer_bytes, problem}` |
| Check, one per expert | haiku, low | `six_experts.py check <run>/<out>/<sid>`, lines for that expert only | `{time_up, sid, pass, failures}` |
| Rerun once | haiku, low | an expert with no usable answer (`ok` false or check fails on a missing section) is asked once more | same as Ask |
| Compare | session model | reads every answer, writes `<run>/<out>/compare.md` (agree, disagree side by side, what each added, dissent, questions), quoted | `{time_up, file, agree, disagree, dissent, questions}` |

Order: all experts but 老子 run at once (each its own subfolder, no shared `status.json`); 老子 (opencode) runs on its
own. Compare starts after every expert is checked. **The script decides nothing**: the main agent reads the summary
and decides (method 3.8 item 14).

## crossed-build-check

args: `{run: "runs/<id>", base: "<commit>", tests: [{id, engine, brief, test_cmd}], review: {engine, brief}}`

| Step | Agent | Does | Returns |
|---|---|---|---|
| Write tests, one per brief | haiku, low | runs the engine on the brief ("Read <brief> and do what it says.", `</dev/null`, timeout 580) | `{time_up, id, exit, result_file, status}` |
| Fail first | session model | in a temporary `git worktree` at `base`, copies the new test files in, runs `test_cmd`, removes the worktree; every new test must fail there | `{time_up, id, failed_on_base, passed_on_base}` |
| Head | haiku, low | runs `test_cmd` in the repo | `{time_up, id, pass, failing}` |
| Review | haiku, low | runs the review engine read-only on its brief; saves its final message | `{time_up, file, findings_count}` |

Order: opencode briefs run one after another; the others in parallel; Fail first and Head follow each brief in a
pipeline; Review starts after all of them. The engine of each brief must differ from the engine that wrote the code
(passed as `code_engine`); the script refuses a brief on the same engine.

Engine commands (from the runs that used them):
- opencode: `opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent build --variant high "Read <brief> and do what it says."`
- codex: `codex exec -m gpt-6.1-sol -c model_reasoning_effort=medium -s workspace-write --skip-git-repo-check -o <run>/nodes/<id>.last.txt "Read <brief> and do what it says."`
- dsh: `dsh headless "Read <brief> and do what it says." > <run>/nodes/<id>.result.md`
- claude: `claude -p --model claude-opus-5-5 "Read <brief> and do what it says." > <run>/nodes/<id>.result.md`
- review, read-only: codex with `-s read-only`, or dsh headless.

## Checks (each shown failing in the offline harness)
- a missing or malformed arg stops before any agent;
- a `time_up` step stops the rest;
- 老子 never starts while another opencode step runs; no two opencode test briefs overlap;
- an expert with no usable answer is rerun once, and only once;
- a brief on the code's own engine is refused;
- a test that passes on the base commit is reported, never counted as failing first.
