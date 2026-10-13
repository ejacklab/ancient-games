"""Same content in four formats, generated from one source so only the format differs: 孫子's items 1-5 from
site/ancients/content/ancients.json (fields title, kind, rule, words, source, label). Markdown is the layout the
seat lists use; XML has one element per field; JSON indented (indent=2) and compact (no spaces)."""
import json, pathlib
from xml.sax.saxutils import escape
here = pathlib.Path(__file__).parent
doc = json.loads((here.parents[3] / "site/ancients/content/ancients.json").read_text())
p = next(x for x in doc["persons"] if x["id"] == "sun-tzu")
F = ["title", "kind", "rule", "words", "source", "label"]
items = [{"n": it["n"], **{f: it[f] for f in F}} for it in p["items"][:5]]
md = [f"# {p['name']} — decision rules 1-5", ""]
for it in items:
    md += [f"### {it['n']}. {it['title']}", f"- **Kind:** {it['kind']}", f"- **Rule:** {it['rule']}",
           f"- **Their words:** {it['words']}", f"- **Source:** {it['source']}", f"- **Words are:** {it['label']}", ""]
xml = [f'<rules person="{escape(p["name"])}">']
for it in items:
    xml.append(f'  <item n="{it["n"]}">')
    xml += [f"    <{f}>{escape(it[f])}</{f}>" for f in F]
    xml.append("  </item>")
xml.append("</rules>")
data = {"person": p["name"], "items": items}
out = {"markdown.md": "\n".join(md), "xml.xml": "\n".join(xml),
       "json_indented.json": json.dumps(data, ensure_ascii=False, indent=2),
       "json_compact.json": json.dumps(data, ensure_ascii=False, separators=(",", ":"))}
for name, text in out.items():
    (here / name).write_text(text); print(f"{name:20} {len(text):6} chars")
