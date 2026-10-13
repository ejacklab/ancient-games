Status: settled (accepted by EJ on 2026-10-13)
Drawn from: 03-domain-model.md; 02-requirements.md R1.2, R5

# Data model — `content/ancients.json`

```json
{
  "title": "The Ancient Games — Four Seats",
  "built_from": "runs/20261013-four-seats",
  "persons": [
    {
      "id": "fan-li",
      "name": "范蠡 (Fan Li)",
      "who": { "markdown": "<verbatim 'Who they are' text>", "source": "runs/20261013-four-seats/identity/fan-li.md" },
      "list_source": "runs/20261013-four-seats/final-opus/fan-li.md",
      "items": [
        { "n": 1, "title": "<verbatim heading>", "kind": "decision rule", "rule": "<verbatim>",
          "words": "<verbatim, Markdown>", "source": "<verbatim>", "label": "<verbatim 'Words are' value>",
          "from": "<verbatim>" }
      ]
    }
  ]
}
```

Decisions: every text field is a verbatim copy of its source file (whitespace may be normalised), so the check can
test it as a substring (R5.2). `words` keeps Markdown so the original and the gloss stay as the list wrote them.
