# corpus_check — 100 prompts, results results_r2.jsonl

bugs: 11 {"EXEC": 11}

- codex: agreement 21/25 (84%)
- agy: agreement 18/25 (72%)

- [EXEC] p130: codex: result=['test data gen'] tiny=False builds=False | expected=['test data gen'] tiny=False builds=True
- [EXEC] p139: codex: result=['test script gen'] tiny=False builds=True | expected=['test cases gen'] tiny=False builds=True
- [EXEC] p141: codex: result=['code review'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p143: codex: result=['test script gen'] tiny=False builds=True | expected=['test cases gen'] tiny=False builds=True
- [EXEC] p187: agy: result=['code generation', 'research and reports', 'test script gen'] tiny=False builds=True | expected=['code generation', 'research and reports', 'test cases gen'] tiny=False builds=True
- [EXEC] p190: agy: result=['code generation', 'multi step planning', 'test script gen'] tiny=False builds=True | expected=['code generation', 'multi step planning', 'test cases gen'] tiny=False builds=True
- [EXEC] p193: agy: result=['code generation', 'information extraction'] tiny=False builds=True | expected=['code generation', 'information extraction', 'web search'] tiny=False builds=True
- [EXEC] p195: agy: result=['document and explain', 'test data gen'] tiny=False builds=True | expected=['document and explain', 'test data gen', 'test script gen'] tiny=False builds=True
- [EXEC] p196: agy: result=[] tiny=True builds=False | expected=['others'] tiny=False builds=False
- [EXEC] p197: agy: result=[] tiny=True builds=False | expected=['others'] tiny=False builds=False
- [EXEC] p199: agy: result=[] tiny=True builds=False | expected=['others'] tiny=False builds=True
