"""Modern Chinese vs English token count on an official parallel text: the UN Universal Declaration of Human Rights,
Articles 1-28 (the NLTK copy of the English stops inside Article 29). Simplified = NLTK 'Chinese_Mandarin-GB2312';
Traditional = the same converted by OpenCC s2t (mechanical). Spaces the NLTK copy puts between Chinese characters are
removed. Tokenizers: OpenAI o200k_base and cl100k_base. Claude's tokenizer not measured (API credit too low).
Run: uv run --no-project --with tiktoken python udhr_count.py"""
import re, tiktoken, pathlib
d = pathlib.Path(__file__).parent / "udhr"
en = (d / "udhr_en.txt").read_text(); hans = (d / "udhr_zh_hans.txt").read_text(); hant = (d / "udhr_zh_hant.txt").read_text()
def zh_articles(t):
    t = re.sub(r"(?<=[^\x00-\x7f]) +|  +(?=[^\x00-\x7f])", "", t)          # drop spaces next to Chinese characters
    t = re.sub(r" +(?=[^\x00-\x7f])", "", t)
    parts = re.split(r"第[一二三四五六七八九十]+[条條]", t)
    return [p.strip() for p in parts[1:]]
def en_articles(t):
    return [p.strip() for p in re.split(r"\nArticle \d+ *\n", t)[1:]]
E, S, T = en_articles(en), zh_articles(hans), zh_articles(hant)
n = 28
E, S, T = E[:n], S[:n], T[:n]
print(f"articles compared: {n} (English {len(en_articles(en))} found, Chinese {len(zh_articles(hans))} found)")
print("article 1:", E[0][:60], "|", S[0][:30], "|", T[0][:30])
for name in ("o200k_base", "cl100k_base"):
    e = tiktoken.get_encoding(name)
    a, b, c = (sum(len(e.encode(x)) for x in L) for L in (E, S, T))
    print(f"{name:12} English {a:5}  Simplified {b:5} ({b/a:.2f}x)  Traditional {c:5} ({c/a:.2f}x)")
print(f"characters: Simplified {sum(map(len,S))}, English words {sum(len(x.split()) for x in E)}")
