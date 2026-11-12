# laws/

One file per Indian law, rule, or regulator direction that Baithak may cite. The Chair cites these files and nothing else (see `references/legal-gate.md`).

## Rules for adding or updating a file

1. File name: lowercase words joined by hyphens, ending `.md`, for example `online-gaming-act-2025.md`.
2. Every fact must come from a source you opened today. Prefer, in order:
   1. the official text (India Code, the Gazette, rbi.org.in, sebi.gov.in, meity.gov.in, PIB);
   2. a reputable law firm or legal news write-up (LiveLaw, Bar & Bench, SCC Online, Mondaq, big law-firm notes);
   3. national news.
   Never write a fact from memory.
3. Copy the frontmatter below exactly. `last_verified` is the date you checked the sources (YYYY-MM-DD). `zone_trigger` is BLACK, GRAY, or WHITE.
4. Keep the body under 300 words, in plain English.
5. Run `python scripts/check_laws.py --lint` (from the skill folder; in this repo `python .claude/skills/baithak/scripts/check_laws.py --lint`) after editing. It must print `lint ok`.

## Template

```markdown
---
title: <official name of the law or direction>
regulator: <RBI | SEBI | MeitY | Parliament | GST Council | ...>
status: <in force | partly in force | notified, not yet in force | draft | struck down>
zone_trigger: <BLACK | GRAY | WHITE>
last_verified: YYYY-MM-DD
sources:
  - <url>
  - <url>
---

## What it says
<2 to 5 plain sentences.>

## What it means for a founder
- BLACK if: <the kinds of product that break it>
- GRAY if: <where it is unclear or not yet in force>
- Compliant route: <the legal way to do something similar>

## Watch for
<pending rules, court challenges, phased dates.>
```
