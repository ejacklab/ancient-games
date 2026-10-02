# corpus_check — 100 prompts, results results_r3.jsonl

bugs: 7 {"EXEC": 7}

- codex: agreement 24/25 (96%)
- agy: agreement 19/25 (76%)

- [EXEC] p231: codex: result=['research and reports'] tiny=False builds=False | expected=['web search'] tiny=False builds=False
- [EXEC] p273: agy: result=['code generation', 'debugging', 'document and explain', 'grade a run'] tiny=False builds=True | expected=['debugging', 'document and explain', 'grade a run'] tiny=False builds=True
- [EXEC] p279: agy: result=['debugging', 'grade a run'] tiny=False builds=False | expected=['debugging', 'grade a run'] tiny=False builds=True
- [EXEC] p285: agy: result=['code generation', 'debugging'] tiny=False builds=True | expected=['debugging'] tiny=False builds=True
- [EXEC] p286: agy: result=['document and explain', 'test data gen'] tiny=False builds=True | expected=['document and explain', 'test data gen', 'test script gen'] tiny=False builds=True
- [EXEC] p288: agy: result=['code generation', 'research and reports'] tiny=False builds=True | expected=['document and explain', 'web search'] tiny=False builds=False
- [EXEC] p295: agy: result=['research and reports'] tiny=False builds=False | expected=['document and explain'] tiny=False builds=False
