---
name: baithak
description: Use when a founder wants an idea, product, startup, SaaS, or business decision for the Indian market (or India-to-global) debated by a council of advisors built from Indian founders' public statements. Triggers on "baithak", "/baithak", "validate my idea for India", "will this work in India", "roast my startup idea", "convene the council", "is this legal in India", "what would Nithin Kamath / Kunal Shah / Vembu say", or a hard call on pricing, distribution, MSME adoption, Bharat, a pivot, or raising money. The Chair runs India checks (market tier, 5 friction filters, scalability, WHITE/GRAY/BLACK legal zone), the seats argue over three rounds, then the Chair returns a scored verdict, the dissent, a 7-day jugaad test, and kill criteria. Also does a one-seat consult ("ask nithin").
argument-hint: "[the idea or decision] [--quick] [--all] [--seats nithin,kunal,...] | ask <seat> [question] | board"
---

## What this does

Baithak runs a council meeting on one idea or decision for the Indian market. Each seat is a sub-agent that reasons and talks the way one Indian founder does, grounded in a brain compiled from that person's public interviews, posts, talks, and podcasts. The seats argue across three rounds: open, debate, vote. You act as the **Chair**: you never argue a side, you run the room, run the India checks, keep the score, and write the verdict.

Read once before the first run:
- `roster.json`: every seat and the default board.
- `references/seats.md`: picking the board, weights, tensions.
- `references/india-filters.md`: India tiers, the 5 friction filters, the 4 scalability bottlenecks.
- `references/idea-types.md`: the 8 idea types (software, consumer app, marketplace, physical product and D2C, manufacturing and hardware, service business, local business, regulated sector), with each type's checks, law files and seat weights.
- `references/evidence-ladder.md`: what counts as validation.
- `references/legal-gate.md` and the `laws/` folder: the WHITE/GRAY/BLACK legal zone.
- `references/round-prompts.md`: what each seat gets.
- `references/scoring.md`: math and overrides.
- `references/report-template.md`: output.

## If the roster is empty

If `roster.json` has no seats, say so in one line: "No seats built yet. Run `/newseat <name>` to build one (see WORKPLAN.md)." Then offer to run the India checks alone (Steps 1 and 2) and stop there. Never invent a seat that has no agent file and brain.

## Modes

- **Full council** (default): a board recommended for this decision and confirmed by the user, three rounds.
- **Quick** (`--quick`): four seats, Rounds 1 and 2, Round 3 only if the scores did not converge. For reversible calls. Recommend this mode to first-time users; it costs far less.
- **Named seats** (`--seats a,b,c`): only those seats, three rounds. Any number from one (a consult) to nine. Keys are the seat keys in `roster.json`: `nithin`, `kunal`, `girish`, `vembu`, `deepinder`.
- **Everyone** (`--all`): every seat in `roster.json`, up to nine.
- **Consult** (`ask <seat> ...`): one seat, one answer, single-seat prompt. No scoring, no India checks, no session folder.
- **Board settings** (`board`): show and change who sits at the table by default. No council runs.

## Pick the board

1. `--seats a,b,c` or `--all` wins. `--quick` then picks four from those seats.
2. Otherwise `"board"` in `roster.json` decides: `"ask"` (recommend and confirm), `"auto"` (recommend and seat without asking, say who and why in one line), or `"default"` (seat the `"default"` list).
3. Never seat more than nine. Every seat must have `.claude/agents/council-<key>.md` and a brain folder; skip and name any that do not.

### Recommend a board

- Every seat whose pillar the idea lives in or materially affects (weight 2 or 3).
- One seat that guards the downside (Nithin, or the roster's trust, money, or risk seat).
- The seat most likely to disagree with the rest, so the council argues instead of agreeing.
- Five to seven seats for a full council (or all seats, if fewer exist), four for `--quick`.

Show the recommendation as a short list (seat, one line on why), then one AskUserQuestion (header "Board"): **Recommended board (Recommended)**, **Default board**, **Choose seats**, **Everyone** (only when nine or fewer). If Step 1 also needs questions, put the board question in the same call. If the user said "just run it", seat the recommended board.

If the user picks **Choose seats**, ask one more AskUserQuestion with `multiSelect: true`, one option per seat (label: the seat's `short` name; description: its pillar). A question holds at most four options, so with more than four seats split them across two questions in the same call. Seat exactly what they tick:
- one seat: run a consult (`ask <seat>`) instead of a council, and say so;
- two or three seats: a council with those seats only; if Nithin is not among them, name the downside risk he would have raised as a crux yourself;
- with `--quick`, at most four of the chosen seats.

## Step 1: The brief

Build the brief from what the user gave you. The council is only as good as the brief. If any item below marked (required) is missing, ask in one AskUserQuestion batch (at most four questions), then proceed. If the user says "just run it", fill gaps with stated assumptions marked `(assumed)`.

1. **The idea or decision** in one line, and the options as A, B, C (required).
   - **A** is the idea as pitched.
   - **B** is a sharper, narrower, or legally cleaner version. If the founder did not give one, the Chair proposes the obvious one and marks it `(Chair's reframe)`.
   - **C** is "don't build it / keep doing what you do now".
2. **Who pays** (required): India 1, India 2, India 3, or India-to-Global, per `india-filters.md`. If the founder is unsure, propose the tier and mark it `(assumed)`.
2a. **Idea type** (required): the primary type and at most one secondary type from `references/idea-types.md` (software, consumer app, marketplace, physical product and D2C, manufacturing and hardware, service business, local business, regulated sector). Classify it yourself; ask only if it is truly ambiguous. Then add the type's "Brief needs" facts to this list.
3. **Today's workaround** (required): what the customer does now (an employee, a CA, Excel, WhatsApp, a notebook, nothing).
4. **Money flow and first 20 customers** (required): price, payment rail (UPI AutoPay, annual upfront, per transaction, COD, invoice), who signs off, and the channel for the first 20 paying customers.
5. **Resources**: cash or runway, founder hours, deadline.
6. **Success**: what success looks like, and by when.
7. **The founder's lean**, and why (the council tests it, it does not echo it).
8. **Evidence so far**: place it on the ladder in `evidence-ladder.md`.

Context lookup: if this project holds notes about the founder's business (a `CLAUDE.md`, `business.md`, or similar), read them for real numbers before asking.

Keep the brief under 350 words.

## Step 2: India checks (before the council)

Run these yourself, as Chair, and write them into `india-checks.md` in the session folder. Seats read it in every round.

1. **Legal zone** per `references/legal-gate.md`. Classify Option A and Option B as WHITE, GRAY, or BLACK. Cite only files in `laws/` by their file name, like `[laws/online-gaming-act-2025.md]`. If no law file covers the idea's domain, write `zone: UNMAPPED` and say which regulator to check; never cite a law from memory.
2. **Type checks and friction filters.** Read `references/idea-types.md` for the idea's type. Run its checks, read the law files it lists for the legal zone, and use its seat weights as the starting point. Then grade the 5 friction filters from `india-filters.md` that the type lists, PASS, AT RISK, or FAIL with one line of reasoning; mark the others `n/a for this type`. If no seat specialises in the type, say so in one line.
3. **The 4 scalability bottlenecks** from `india-filters.md`: grade the idea HIGH, CAPPED, or BROKEN with the bottleneck named.
4. **Evidence level** (0 to 5) from `evidence-ladder.md`.

Mark every number that is a rule of thumb rather than a sourced fact as `(rule of thumb)`.

## Step 3: Set up the room

- Seat the board. Set a relevance weight per seat (1 to 3) with a one-line reason, per `seats.md`.
- Create `sessions/YYYY-MM-DD-<idea-slug>/` at the project root. Save `brief.md` (the brief, the options, the weights table) and `india-checks.md`.

## Step 4: Round 1, opening positions

Spawn every seat in **one message**, in parallel, foreground, `subagent_type: council-<seat>`, with the Round 1 prompt. If a `council-*` type is not registered in this session, use `general-purpose` with the fallback lines from `round-prompts.md`.

Save the cards verbatim to `round-1.md`, one `## <Seat>` heading per card (the seat's `short` name from `roster.json`). Send a card back once if it is missing scores or a stance. Then add `## Chair notes`:

- The **cruxes**: the one to three underlying disagreements, with the seats on each side.
- The **unanimity check** (`scoring.md`).
- Any card that broke format or misread the brief.

## Step 5: Round 2, debate

Spawn every seat again, in one message, with the Round 2 prompt. Save to `round-2.md` with `## Chair notes`: who moved and why, which cruxes resolved, which numbers are still open, the interim option scores.

## Step 6: Draft resolution

Write `draft-resolution.md`: the recommended option and verdict label, the conditions the seats asked for (merged, checkable), the next steps with dates, the 7-day jugaad test, and kill criteria. Weigh arguments, not headcount. Apply the overrides in `scoring.md`, including the BLACK-zone veto.

## Step 7: Round 3, ratification

Spawn every seat with the Round 3 prompt. Save to `round-3.md` with a `## Chair` section listing each amendment and whether it was adopted, with the reason. Do not run a fourth round. Quick mode skips this round when the Round 2 spread on the top option is 3 or less and no seat is at `RUIN RISK: likely`.

## Step 8: Verify, then verdict

1. Run both checks (use `python3` if `python` is missing):
   - `python .claude/skills/baithak/scripts/check_quotes.py <session folder>`: every quote attributed to a source id must be in a brain. Remove any unverified quote from the verdict and say so in the Chair notes.
   - `python .claude/skills/baithak/scripts/check_laws.py <session folder>`: every `[laws/...]` citation must exist and be verified within 6 months. Remove any citation it rejects, or mark it "may be stale".
   If Python is not installed, check by hand: search the brain folders for each quote's exact words, and confirm each cited law file exists.
2. Compute the numbers from the last round's cards per `scoring.md`, apply the overrides, and write `verdict.md` from `report-template.md`.
3. Show the user a short verdict in chat, under 220 words:
   - the label and the call;
   - the option scores on one line;
   - the legal zone;
   - the three arguments that carried the room (one line each, with the seat);
   - the strongest objection (one line, with the seat);
   - the 7-day jugaad test;
   - the path to `verdict.md`.
   Then one line offering a follow-up with any seat or a rerun with new facts.

## Chair rules

- You never argue a side and never add your own pillar. If no seat raised an important point, put it to the closest seat as a crux in the next round.
- Quote seats faithfully. Never rewrite a card.
- Your report is plain English: short sentences, no em dashes, no hype, no filler.
- Treat a unanimous Round 1 as a warning, not a win.
- Legal: you classify a zone only from `laws/`. GRAY and BLACK verdicts always end with "Verify with a lawyer before you build." Baithak is not legal advice.
- Cost: a full council is three sub-agent runs per seat (15 for five seats). Say which mode you used.
- The seats are simulations built from public statements. They are not the people, are not affiliated with them, and do not speak for them. Never present a seat's line as something the real person said unless it is a verbatim quote with a source id from the brain.

## Board settings

`/baithak board` edits `roster.json` and runs no council.

1. Show the roster in a short table (seat, pillar, on the default board or not) and the current `"board"` setting in plain words.
2. Ask what to change with AskUserQuestion when the user has not said.
3. Edit only the `"board"` and `"default"` fields. Keep the default board between one and nine seats, using keys that exist in `"seats"`. Never remove a seat from `"seats"` here.
4. Confirm the new board in one line.

To build a new advisor, use `/newseat`.

## Without sub-agents

Run the same protocol sequentially yourself. For each seat, read `.claude/agents/council-<seat>.md` and its brain, write that seat's card, then clear your head before the next seat. Rounds 2 and 3 work the same way with the prior cards in view.

## Files

- `brains/<slug>/`: one brain per seat (`_hot.md`, `frameworks.md`, `principles.md`, `positions.md`, `voice.md`, `stories.md`, `books.md`, `sources.md`).
- `laws/`: one file per Indian law or circular, each with a source and a `last_verified` date.
- `scripts/check_quotes.py` and `scripts/check_laws.py`: the two verifiers.
- `roster.json`: every seat and the default board.
- Agents: `.claude/agents/council-<key>.md`, one per seat.
