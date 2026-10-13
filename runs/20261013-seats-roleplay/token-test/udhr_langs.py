"""English vs Spanish, Japanese, Korean, Chinese token counts on the UN Universal Declaration of Human Rights,
Articles 1-25 (the NLTK copies of Spanish and Korean stop inside Article 26). Official translations from NLTK's udhr
corpus; Traditional Chinese = Simplified converted by OpenCC s2t. Line-wrap spaces inside Japanese and Chinese are
removed; other whitespace collapsed. Tokenizers: OpenAI o200k_base and cl100k_base. Claude's tokenizer not measured.
The NLTK Japanese copy writes Article 23 as 「弟23条」 (typo), so the marker accepts 弟 too.
Run: uv run --no-project --with tiktoken python udhr_langs.py"""
import re, tiktoken, pathlib
d = pathlib.Path(__file__).parent / "udhr"
N = 25
def split(text, marker, cjk=False):
    if cjk:
        text = re.sub(r"(?<=[^\x00-\x7f])[ 　\n]+|[ 　\n]+(?=[^\x00-\x7f])", "", text)
    parts = re.split(marker, text)[1:]
    return [re.sub(r"\s+", " ", p).strip() for p in parts][:N]
langs = {
    "English":     split((d / "udhr_en.txt").read_text(), r"\nArticle \d+ *\n"),
    "Spanish":     split((d / "udhr_Spanish-Latin1.txt").read_text(), r"Art[íi]culo \d+"),
    "Japanese":    split((d / "udhr_Japanese_Nihongo-EUC.txt").read_text(), r"[第弟][0-9０-９]+条", cjk=True),
    "Korean":      split((d / "udhr_Korean_Hankuko-UTF8.txt").read_text(), r"제 *\d+ *조"),
    "Chinese (Simplified)":  split((d / "udhr_zh_hans.txt").read_text(), r"第[一二三四五六七八九十]+条", cjk=True),
    "Chinese (Traditional)": split((d / "udhr_zh_hant.txt").read_text(), r"第[一二三四五六七八九十]+條", cjk=True),
}
for k, v in langs.items():
    assert len(v) == N, (k, len(v))
    print(f"{k:22} art.1: {v[0][:50]}")
print()
for name in ("o200k_base", "cl100k_base"):
    e = tiktoken.get_encoding(name)
    base = sum(len(e.encode(x)) for x in langs["English"])
    print(name)
    for k, v in langs.items():
        t = sum(len(e.encode(x)) for x in v)
        print(f"  {k:22} {t:5} tokens  {t/base:.2f}x English")
