# Legal gate: WHITE, GRAY, BLACK

The Chair classifies Option A and Option B before Round 1. Baithak is not legal advice. Its job is to flag where an idea collides with Indian law so the founder knows what to check, not to replace a lawyer.

## The only allowed sources

- The Chair cites **only** files in the skill's `laws/` folder, written as `[laws/<file>.md]`.
- Never cite an Act, section, circular or rate from memory. Laws in India change quickly. Memory is how stale or invented citations get in.
- If no law file covers the idea's domain, write `zone: UNMAPPED`, name the likely regulator (RBI, SEBI, IRDAI, MeitY, CDSCO, a state government, GST Council), and tell the founder to check before building. An UNMAPPED zone is not WHITE.
- If a cited law file's `last_verified` date is more than 6 months old, say "may be stale" next to the citation. `check_laws.py` enforces this.

## The three zones

| Zone | Meaning | What the Chair does |
|---|---|---|
| **BLACK** | Option clearly breaks an active law or regulator rule in a `laws/` file | Hard veto on that option (see `scoring.md`). Option B must move to legal rails, or the verdict is DON'T DO IT |
| **GRAY** | The law is silent, unclear, or still being written for this model (for example, a rule notified but not yet in force, or a new kind of AI product) | The founder may move, but with a **compliance switch**: what they would have to change within days if a rule lands. Examples: keep user money out of the company account, clean GST invoicing, a written consent log. Name the switch |
| **WHITE** | Ordinary business with a known compliance path | Tell the founder not to spend big on legal structure before the first 10 paying customers. List only day-one basics |

Every GRAY or BLACK result ends with: **"Verify with a lawyer before you build."**

## How seats use it

Seats read the zone in `india-checks.md`. A seat may argue that the Chair's zone is wrong, but only by pointing to a `laws/` file. If a seat flags a legal risk with no law file, the Chair records it as `UNMAPPED risk raised by <seat>` and lists it under "Check before you build".
