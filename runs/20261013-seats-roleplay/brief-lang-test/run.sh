#!/usr/bin/env bash
# brief = brief_<cond> + the same data (token-test/formats/xml.xml). opencode, dsh: en_md, en_xml, zh_xml;
# claude, codex, agy: en_md, en_xml. Wall time per call -> times.tsv. Run from brief-lang-test/.
DATA=../token-test/formats/xml.xml
call() { local e=$1 c=$2 f t0 t1
  f=brief_${c/_md/.md}; f=${f/_xml/.xml}
  P="$(cat $f)

Data:
$(cat $DATA)"
  t0=$(date +%s.%N)
  case $e in
    claude)   timeout 600 env -u ANTHROPIC_API_KEY claude -p --model claude-opus-5-5 --output-format json "$P" </dev/null >$e-$c.out 2>$e-$c.err ;;
    codex)    timeout 600 codex -m gpt-6.1-sol exec -s read-only --skip-git-repo-check --json -o $e-$c.txt "$P" </dev/null >$e-$c.out 2>$e-$c.err ;;
    agy)      timeout 600 agy -p "$P" --mode plan --model gemini-3.8-flash-medium --output-format json </dev/null >$e-$c.out 2>$e-$c.err ;;
    opencode) timeout 600 opencode run -m minimax-coding-plan/MiniMax-M3.1-Flash-Preview --agent plan --format json "$P" </dev/null >$e-$c.out 2>$e-$c.err ;;
    dsh)      timeout 600 dsh headless --json "$P" </dev/null >$e-$c.out 2>$e-$c.err ;;
  esac
  local rc=$?; t1=$(date +%s.%N); printf '%s\t%s\t%s\t%s\n' $e $c "$(echo "$t1 - $t0" | bc)" $rc >> times.tsv; }
: > times.tsv
(for c in en_md en_xml zh_xml; do call opencode $c; done) &
(for c in en_md en_xml zh_xml; do call dsh $c; done) &
(for c in en_md en_xml; do call claude $c; done) &
(for c in en_md en_xml; do call codex $c; done) &
(for c in en_md en_xml; do call agy $c; done) &
wait
