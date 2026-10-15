# Work for this session — do every step in order, then write REPORT.md

1. Create `src/textstats.py` with three functions: `word_count(text)`, `top_words(text, n)` (the n most common words,
   lower-cased, ties broken alphabetically) and `line_lengths(text)` (a list of the lengths of each line).
2. Write pytest tests for all three in `tests/test_textstats.py` (at least three tests per function).
3. Run `python3 -m pytest -q` and fix anything that fails until it is green.
4. Run `python3 gen_log.py` to create `data/log.txt`, then read the first 300 lines of it.
5. Add `error_lines(path)` to `src/textstats.py`: the lines of the file that contain `ERROR`. Add two tests for it.
6. Run the tests again.
7. Write `NOTES.md`: which error messages occur in `data/log.txt`, how often each, and which service has the most.
8. Ask the codex engine for a review: run `codex exec "Review src/textstats.py for bugs" -o out/review.md` and apply
   any fix it suggests.
9. Add a command line: `python3 -m src.textstats FILE` prints the word count and the 5 top words. Add a test for it.
10. Run the tests again.
11. Rename `top_words` to `most_common_words` everywhere, including the tests, and run the tests.
12. Ask the codex engine for test ideas: run `codex exec "Suggest three more tests for src/textstats.py" -o out/test-ideas.md`
    and add the tests it suggests.
13. Run the tests a final time.
14. Write `REPORT.md`: what you did in each step, and anything that did not work.
