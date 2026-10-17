# Brief — P5 judge: score two answer sets against the answer key

You score two sets of answers to the same ten questions about one opencode module. You do not know how either
set was made. Score only against the key and the code.

## Read

- The key: KEY (claims M?.Na…, each with a source line and a quote). The key is the reference; where a claim in an
  answer goes beyond the key, check it in the code under ROOT before scoring it.
- Answer set A: ANS_A. Answer set B: ANS_B.

Read nothing else.

## Score

For each question and each set, count:
- **correct**: key claims the answer states, with a file:line within 3 lines of the key's;
- **missed**: key claims the answer does not state;
- **wrong**: claims in the answer that contradict the key or the code (check the code before calling a claim wrong).

## Return

Your final message only, in this shape, nothing else:

```
| Q | A correct | A missed | A wrong | B correct | B missed | B wrong |
|---|---|---|---|---|---|---|
| Q1 | ... |
...
| Total | ... |
```

Then one line per wrong claim: set, question, the claim, and why it is wrong (file:line).
