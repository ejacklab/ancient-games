# corpus_check — 100 prompts, results results_r1.jsonl

bugs: 41 {"EXEC": 41}

- codex: agreement 3/25 (12%)
- agy: agreement 6/25 (24%)

- [EXEC] p001: codex: result=['information extraction', 'repo scanning'] tiny=False builds=False | expected=['repo scanning'] tiny=False builds=False
- [EXEC] p002: codex: result=['document and explain', 'information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p003: codex: result=['information extraction', 'repo scanning'] tiny=False builds=False | expected=['repo scanning'] tiny=False builds=False
- [EXEC] p004: codex: result=['information extraction', 'repo scanning'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p005: codex: result=['information extraction', 'repo scanning'] tiny=False builds=False | expected=['repo scanning'] tiny=False builds=False
- [EXEC] p006: codex: result=['information extraction'] tiny=False builds=False | expected=['repo scanning'] tiny=False builds=False
- [EXEC] p007: codex: result=['information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p008: codex: result=['information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p009: codex: result=['information extraction', 'repo scanning'] tiny=False builds=False | expected=['repo scanning'] tiny=False builds=False
- [EXEC] p011: codex: result=['code review'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p012: codex: result=['code review'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p013: codex: result=['code review', 'information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p014: codex: result=['code review', 'debugging'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p015: codex: result=['code review'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p016: codex: result=['code review'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p017: codex: result=['document and explain'] tiny=False builds=True | expected=['research and reports'] tiny=False builds=False
- [EXEC] p018: codex: result=['code review'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p020: codex: result=['grade a run'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p021: codex: result=['code review', 'document and explain', 'information extraction'] tiny=False builds=True | expected=['information extraction', 'research and reports'] tiny=False builds=False
- [EXEC] p022: codex: result=['code review'] tiny=False builds=True | expected=['research and reports'] tiny=False builds=False
- [EXEC] p023: codex: result=[] tiny=True builds=True | expected=[] tiny=True builds=False
- [EXEC] p024: codex: result=['information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p051: agy: result=['debugging', 'information extraction'] tiny=False builds=False | expected=['debugging'] tiny=False builds=False
- [EXEC] p052: agy: result=['code review', 'information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p054: agy: result=['information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p055: agy: result=['code review', 'multi step planning'] tiny=False builds=False | expected=['multi step planning'] tiny=False builds=False
- [EXEC] p058: agy: result=['document and explain', 'information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p059: agy: result=['code review', 'information extraction'] tiny=False builds=False | expected=['information extraction'] tiny=False builds=False
- [EXEC] p060: agy: result=['document and explain', 'information extraction'] tiny=False builds=False | expected=['research and reports'] tiny=False builds=False
- [EXEC] p061: agy: result=[] tiny=True builds=False | expected=['code generation'] tiny=False builds=True
- [EXEC] p062: agy: result=['test cases gen', 'test script gen'] tiny=False builds=True | expected=['test script gen'] tiny=False builds=True
- [EXEC] p063: agy: result=['multi step planning', 'repo scanning'] tiny=False builds=False | expected=['multi step planning'] tiny=False builds=False
- [EXEC] p064: agy: result=['information extraction', 'repo scanning'] tiny=False builds=False | expected=['repo scanning'] tiny=False builds=False
- [EXEC] p065: agy: result=['code generation', 'test script gen'] tiny=False builds=True | expected=['test script gen'] tiny=False builds=True
- [EXEC] p066: agy: result=['test data gen'] tiny=False builds=False | expected=['test data gen'] tiny=False builds=True
- [EXEC] p067: agy: result=['debugging', 'information extraction'] tiny=False builds=False | expected=['test data gen'] tiny=False builds=False
- [EXEC] p068: agy: result=['test cases gen', 'test script gen'] tiny=False builds=True | expected=['test cases gen'] tiny=False builds=True
- [EXEC] p069: agy: result=['debugging', 'test data gen'] tiny=False builds=True | expected=['test data gen'] tiny=False builds=True
- [EXEC] p070: agy: result=['code generation', 'test script gen'] tiny=False builds=True | expected=['test script gen'] tiny=False builds=True
- [EXEC] p072: agy: result=['code generation', 'test script gen'] tiny=False builds=True | expected=['test data gen'] tiny=False builds=True
- [EXEC] p074: agy: result=['document and explain', 'research and reports'] tiny=False builds=False | expected=['document and explain'] tiny=False builds=False
