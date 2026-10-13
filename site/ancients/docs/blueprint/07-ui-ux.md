Status: settled (accepted by EJ on 2026-10-13)
Drawn from: 02-requirements.md R1–R4; 01-vision.md

# UI / UX

**Layout.** A row of four full-screen panels, side by side; the row scrolls horizontally with snap, so one swipe
shows exactly one person (R2.1). Each panel scrolls vertically on its own (R3). A quiet header shows the current
name, "n / 4" and four dots (R2.2, R2.3) and an "Aa" button (R4.1). Each panel ends its view with a small footer
showing % read (R4.4). Look, fonts, colours and the menu come from the `kindle-page` skill (R4.1). Swipes start
away from the screen edges, so Android's edge "back" gesture is not triggered (unclear spot U4; EJ checks on the
phone in P4).

**DOM contract** (the tests use exactly these; the builder must provide them):

| Selector | What |
|---|---|
| `#people` | the horizontal row |
| `section.person[data-person="<id>"]` | one per person, in R1.1 order; the vertical scroller |
| `.person .person-name` | the name inside a panel |
| `.person .who` | the "who they are" text |
| `.person .kinds` | the count of each kind, e.g. "3 mindsets · 15 decision rules" (R1.3) |
| `.item .kind` | the item's kind tag: `mindset`, `decision rule` or `algorithm` (R1.3) |
| `.person .item[data-n="<n>"]` | one per list item, containing `.kind`, `.rule`, `.words`, `.source`, `.label` |
| `#person-name`, `#person-pos` | header: current name, and "n / 4" |
| `#dots button[data-goto="<0-3>"]` | one dot per person |
| `#aa` | opens `#menu`; `#menu` holds the R4.1 choices as buttons with `data-setting` and `data-value` |
| `.person .pct` | that panel's % read |
