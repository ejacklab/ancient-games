# Token count for dsh (deepseek-flash): instruction + text, per language; baseline is dsh/baseline.jsonl
P="Reply with only the word OK. Do not use any tools."
for l in english chinese_simplified chinese_traditional spanish korean japanese; do
  timeout 600 dsh headless --json "$P

$(cat opencode/text_$l.txt)" </dev/null > dsh/$l.jsonl 2>dsh/$l.stderr; echo "dsh $l exit=$?" >> dsh/exits.txt
done
