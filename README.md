# Weekly Health Brief (demo)

**Portfolio demo** of a wearable-export → decision brief.  
**All metrics are synthetic SAMPLE data** — not a real person’s health record.

> Coach-light summary for self-awareness. **Not medical advice.**

## Problem → model → decisions

1. **Problem:** Wearable privacy dumps (CSV/JSON ZIPs) are plumber-first. Lots of rows, weak story.
2. **Daily model:** Normalize to simple daily aggregates (sleep, steps, resting HR) + workout sessions (here: tennis load).
3. **Decisions:** Lead with a **weekly brief** — at-a-glance tiles, a short story, soft hints, general wellness notes — and put charts/tables behind **Look closer**.

UX defaults: one scrolling page · coach-light tone · tennis as a first-class tile · stress / SpO₂ / weight out of the default story.

## Quick look

Open [`brief/index.html`](brief/index.html) in a browser (or browse the raw file on GitHub).

Featured SAMPLE week: **2025-04-05 → 2025-04-11** for a fictional “Demo athlete · recreational tennis.”

## What’s in the repo

```
sample_data/          # synthetic CSVs only
charts/               # plots regenerated from sample_data
brief/
  index.html          # the brief
  generate_brief.py   # rebuild HTML from sample CSVs
  charts/             # copies used by index.html
```

No raw wearable exports. No private paths.

## How to run

```bash
# optional: edit sample_data/*.csv (keep column names)
python3 brief/generate_brief.py
# optional: python3 brief/generate_brief.py --week-end 2025-04-11
open brief/index.html   # or any browser
```

Requires Python 3.10+ (stdlib only for the brief). Charts in this repo were pre-generated; regenerating PNGs needs `matplotlib` if you change the plotting script locally.

## Update path (demo)

v1 is human cadence: swap CSVs → regenerate brief. Live wristband sync is intentionally out of scope (fragile + not cheap for a portfolio slice).

**Keep real personal exports out of public remotes.**

## Disclaimer

This is a UX / product-thinking demo. Numbers are invented. Guidelines cited in the brief (e.g. adult sleep bands, WHO activity framing) are general public guidance, not a diagnosis or training plan.
