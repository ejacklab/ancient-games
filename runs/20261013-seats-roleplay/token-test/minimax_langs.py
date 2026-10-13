"""Same six-language UDHR test (Articles 1-25, see udhr_langs.py) on MiniMax's published tokenizers (HuggingFace
MiniMaxAI/MiniMax-M3 and -M2 tokenizer.json). opencode runs MiniMax-M3.1-Flash-Preview, whose tokenizer is not
published (401), so M3 stands in for it — not verified to be the same.
Run: uv run --no-project --with tiktoken --with tokenizers python minimax_langs.py <dir with MiniMax-M3.json, MiniMax-M2.json>"""
import sys, pathlib
from tokenizers import Tokenizer
__file__ = str(pathlib.Path(__file__).parent / "udhr_langs.py")
exec(open(__file__).read().split("for k, v in langs.items():")[0])
for name in ("MiniMax-M3", "MiniMax-M2"):
    tok = Tokenizer.from_file(str(pathlib.Path(sys.argv[1]) / f"{name}.json"))
    count = lambda x: len(tok.encode(x, add_special_tokens=False).ids)
    base = sum(count(x) for x in langs["English"])
    print(name)
    for k, v in langs.items():
        t = sum(count(x) for x in v)
        print(f"  {k:22} {t:5} tokens  {t/base:.2f}x English")
