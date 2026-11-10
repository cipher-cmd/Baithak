# Seats

`roster.json` (one folder up) is the source of truth: every seat that is actually built, its key, pillar, question, and scorecard dimension, plus the default board. A seat exists only when it has an agent file (`.claude/agents/council-<key>.md`) and a brain (`brains/<slug>/`).

## Planned v1 seats

These are the five seats to build first, with `/newseat`. Until a seat is built and registered, it is not at the table.

| Key | Name | Slug | Pillar | Owns the question | Dimension |
|---|---|---|---|---|---|
| `nithin` | Nithin Kamath | `nithin-kamath` | Trust, regulation, and capital discipline | Will Indians trust you with their money or data without you burning cash to buy them? | Trust and capital efficiency |
| `kunal` | Kunal Shah | `kunal-shah` | Consumer behaviour and India 1 vs Bharat | Is this a big enough leap over today's jugaad that nobody goes back? | Behaviour change and segment fit |
| `vembu` | Sridhar Vembu | `sridhar-vembu` | Frugal R&D, Bharat, and bootstrapping | Can you build real depth cheaply, outside the metro bubble, without VC money? | Frugality and depth |
| `girish` | Girish Mathrubootham | `girish-mathrubootham` | B2B SaaS and India-to-global | Why sell this for ₹999 in India when the world will pay $500? | Market choice and SaaS go-to-market |
| `deepinder` | Deepinder Goyal | `deepinder-goyal` | Consumer habit and operations at scale | Is this a daily habit, and what breaks at 10,000 orders a day? | Frequency and operational scale |

Downside guard: `nithin`. When he is not seated, use `vembu`.

## Relevance weights

The Chair sets a weight per seat for each decision, before Round 1, with a one-line reason.

| Weight | Meaning |
|---|---|
| 3 | The idea lives in the seat's pillar |
| 2 | The pillar is materially affected |
| 1 | The pillar is touched at the edges |

Every seat is at least 1. Exactly one or two seats get a 3.

## Quick council

`--quick` seats four: the two highest-weight seats, the downside guard, and the seat most likely to disagree with the others (the Chair names why).

## Natural tensions to expect

- Vembu (domestic, rural, frugal, no VC) against Girish (sell to the world in USD, build an inside-sales machine).
- Vembu and Nithin (bootstrap, never burn to buy users) against Deepinder (move fast, build operations at scale, raise when the market is there).
- Kunal (is the behaviour change big enough, and which India is this for) against Deepinder (frequency and operations decide it).
- Nithin (regulators and trust first) against any seat pushing speed in a GRAY zone.

Seats added with `/newseat` append their own tension lines here.

If Round 1 comes back unanimous, the Chair should be suspicious and press the seat whose pillar is most at risk in Round 2.
