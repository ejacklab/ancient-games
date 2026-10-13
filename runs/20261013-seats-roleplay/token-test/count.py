"""Chinese vs English token count on the same meaning: each 「Chinese quote」 — "English translation" pair in the
ancients page content. Tokenizers: OpenAI o200k_base (GPT-4o and later) and cl100k_base (GPT-4/3.5), via tiktoken.
Claude's tokenizer is not measured: the count_tokens API refused (credit balance too low).
Run: uv run --no-project --with tiktoken python count.py"""
import json, re, pathlib, tiktoken
root = pathlib.Path(__file__).resolve().parents[3]
doc = json.loads((root / "site/ancients/content/ancients.json").read_text())
pairs = []
for p in doc["persons"]:
    for it in p["items"]:
        for zh, en in re.findall(r'「([^」]+)」\s*[—–-]+\s*"([^"]+)"', it["words"]):
            pairs.append((p["id"], zh, re.sub(r"\s+", " ", en)))
encs = {n: tiktoken.get_encoding(n) for n in ("o200k_base", "cl100k_base")}
print(f"{len(pairs)} pairs (classical Chinese quote, English translation)\n")
for n, e in encs.items():
    zh = sum(len(e.encode(z)) for _, z, _ in pairs); en = sum(len(e.encode(x)) for _, _, x in pairs)
    print(f"{n:12} Chinese {zh:5} tokens  English {en:5} tokens  ratio zh/en = {zh/en:.2f}")
zc = sum(len(z) for _, z, _ in pairs); ec = sum(len(x) for _, _, x in pairs)
print(f"\ncharacters: Chinese {zc}, English {ec}; tokens per Chinese character (o200k) = {sum(len(encs['o200k_base'].encode(z)) for _,z,_ in pairs)/zc:.2f}")
print("\nexamples (o200k):")
for pid, z, x in pairs[:4]:
    print(f"  {len(encs['o200k_base'].encode(z)):3} vs {len(encs['o200k_base'].encode(x)):3}  {z[:30]}")
