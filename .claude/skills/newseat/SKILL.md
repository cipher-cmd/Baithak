---
name: newseat
description: Use when someone wants to add a new advisor to Baithak, says "/newseat", "add a seat", "add [name] to the council", "build a seat for [name]", "I want [name] on my board", or wants their own advisor (themselves, a mentor, or any Indian public figure) built from public work. Checks the person for personality-rights court orders first, then finds and fetches their public sources (English, Hindi, or Hinglish), extracts their frameworks, rules, positions, stories, and voice with parallel sub-agents, writes the brain, checks every quote is verbatim, writes the council agent, and registers the seat in the roster (on the default board if asked). No portraits, photos, or voices. Not for running a council (that is /baithak).
argument-hint: "[full name] [--quick | --deep] [--pillar \"...\"] [--default]"
---

## What this does

Adds one seat to Baithak. A seat is three things, and this skill makes all three:

1. **A brain**: `.claude/skills/baithak/brains/<slug>/`, eight files compiled from the person's public work, every quote verbatim with a source id.
2. **An agent**: `.claude/agents/council-<key>.md`, the sub-agent that reasons and talks like them from that brain.
3. **A roster entry**: one line in `.claude/skills/baithak/roster.json`, so `/baithak` knows the seat exists.

Baithak never makes portraits, photos, cartoons, or voice clones of a real person. Indian courts protect a person's name, image, voice and likeness ("personality rights"), and likeness is the core of those orders. The seat is text only, built from verbatim, sourced quotes.

The raw sources stay in a local build folder that git ignores. Only the brain ships.

Build folder: `build/<slug>/` at the project root.

Read before the first run: `references/brain-spec.md` (the brain layout and its rules), `references/extract-prompt.md` (what each extraction agent gets), `references/writer-prompt.md` (what each brain writer gets), `references/agent-template.md` (the seat agent).

## Who can be a seat

- **Public figures with a real body of public work**: essays, letters, books as they teach them in talks, long interviews where they are the main speaker, keynotes, their own channel or podcast. Living or historical.
- **The user, or someone who gave consent**: built from material the user provides (their posts, transcripts, notes). Use `--add` in step 3.
- **Not**: fictional characters, private people without their consent, or anyone whose public work is too thin. Under about 15 usable sources or 60,000 words, say so and offer `--quick` with a warning, or a different person.

The seat is a simulation, not the person. The agent says so if asked, and only quotes what is in its brain.

## Step 0: Personality-rights check (always, before anything else)

Run WebSearch (standard mode) with each of these queries, replacing NAME:
1. `"NAME" personality rights High Court`
2. `"NAME" Delhi High Court injunction name image voice`
3. `"NAME" deepfake court order`

Read the results. If any result reports a court order (interim or final) protecting this person's name, image, voice, likeness or persona:
- **Stop.** Do not fetch sources or build anything.
- Tell the user, with the link: "NAME has a personality-rights court order. Baithak does not build seats for people with such orders." Offer a different person.

Known as of 2026-11-05: **Aman Gupta** (Delhi HC, May 2026). Never build a seat for him.

If nothing turns up, create `build/<slug>/` and write one line to `build/<slug>/rights-check.md`: `Personality-rights check YYYY-MM-DD: no order found. Queries: <the three queries>`. Then continue. This lowers risk; it is not legal clearance.

## Depth

| Flag | Sources | Words | Extraction agents | Use it for |
|---|---|---|---|---|
| `--quick` | 12 to 20 | 80k+ | 2 to 3 | Trying someone out |
| default | 30 to 50 | 250k+ | 4 to 6 | A seat you will actually use |
| `--deep` | 80+ | 500k+ | 8 to 12, in waves | A flagship seat |

Quality beats count: one 90-minute keynote is worth ten 6-minute clips.

## Step 1: Who and what seat

From the user's message, get the person's full name. If anything below is missing, ask in one AskUserQuestion batch (at most four questions), offering your best guess as the first option:

1. **The pillar and the question the seat owns.** Propose one from what the person is known for, worded like the existing seats in `roster.json` (pillar: a few words; question: one plain question a founder would face). If an existing seat already owns that pillar, propose a sharper angle so the two seats argue instead of repeating each other.
2. **Default board?** Put them at the table for every council, or keep them on call (`--seats` and `ask`). If the default board already has nine seats, ask who they replace.
3. **Depth**: quick, standard, or deep (default standard).

Then fix the names: `key` (short lowercase, letters only, unique in the roster, usually the first name for Indian founders: `nithin`, `kunal`; the surname when another seat shares the first name), `slug` (`first-last`), `short` (how the council names them: "Nithin", "Kunal"), and the scorecard `dimension` (a few words for what this seat scores, like "Trust and capital efficiency"). If the person is listed under "Planned v1 seats" in `.claude/skills/baithak/references/seats.md`, use exactly the key, slug, pillar, question and dimension from that table and skip the questions above except depth.

Check the roster first: if the person already has a seat, stop and offer to refresh it instead (step 3 onward on the same slug; fetch skips sources already in `sources.json`).

## Step 2: Find sources

Use WebSearch to build a source list, best first. Look for:

- Their own site, blog, essays, newsletter archive, or letters (the richest text, with dates).
- Long talks and keynotes where they are the speaker.
- Long interviews and podcasts where they are the main guest (their own podcast counts).
- Their books as they teach them in public: author talks, interviews about the book, chapters they posted free. Never fetch pirated or paywalled book text.
- Indian sources that tend to be rich: their own blog or company blog, their long X (Twitter) posts, long podcasts where they are the main guest (The Ranveer Show, Figuring Out with Raj Shamani, WTF is with Nikhil Kamath, The Barbershop with Shantanu, Think School), conference keynotes (SaaSBOOMi, Nasscom, TiE), and long-form interviews with YourStory, Inc42, Mint, or The Economic Times.
- Hindi or Hinglish sources are welcome when they add something the English sources do not. Prefer English first: YouTube's Hindi auto-captions are rough.
- Recent material (last two years) so `positions.md` reflects current views, and a spread of years so changes of mind show up.

Skip clips under about 10 minutes, fan compilations, reaction videos, and pieces where someone else does most of the talking. Write the URLs to `<build>/urls.txt`, one per line, with a `# heading` line per group. Aim for the source count of the chosen depth plus about 20 percent, since some will fail.

## Step 3: Fetch

```bash
node .claude/skills/newseat/scripts/fetch.mjs <build> --list <build>/urls.txt
```

Each source becomes `<build>/corpus/S001-<title>.md`, logged in `<build>/sources.json`. It prints `ok`, `skip`, `thin` (paywall or a JavaScript page), or `fail` per URL, then a manifest. YouTube uses yt-dlp when installed, otherwise YouTube's own captions. For local material the user gave you:

```bash
node .claude/skills/newseat/scripts/fetch.mjs <build> --add path/to/file.md --title "..." --date 2024-05-01
```

If a source came back thin or failed, find a different copy (a transcript page, an archive.org copy) or replace it. A PDF without `pdftotext` is saved as `pending-*.pdf`: read it with the Read tool, save the text as a `.md`, then `--add` it. Re-run until the manifest meets the depth target, then open two or three corpus files to confirm they are clean text by the right person. Write the manifest line counts into your notes for the final report.

## Step 4: Extract (map)

Split the sources into batches of about 50,000 words each (a 90-minute talk is about 13,000; a long essay 5,000). Spawn one extraction agent per batch, in **one message**, in parallel, foreground: `subagent_type: general-purpose`, `model: sonnet`, with the prompt from `references/extract-prompt.md` (fill in the name, the seat's pillar and question, the batch's source ids and file paths, and the notes file to write). Run at most six at a time; for `--deep`, run them in waves.

Each agent writes `<build>/notes/batch-NN.md`. Wait until every agent has reported. When all are back, check every note quote:

```bash
node .claude/skills/newseat/scripts/check_quotes.mjs <build> <build>/notes
```

Fix what it reports: correct a wrong source id, delete a quote it cannot find. Notes with no verifiable quote can stay as paraphrase, marked "inferred from S0xx".

## Step 5: Write the brain (reduce)

Create `.claude/skills/baithak/brains/<slug>/`. Write `sources.md` with the script:

```bash
node .claude/skills/newseat/scripts/fetch.mjs <build> --sources-md .claude/skills/baithak/brains/<slug>/sources.md --name "Full Name"
```

Then spawn three writer agents in one message, in parallel (`general-purpose`, `model: sonnet`; never a smaller model, since the brain decides seat quality), with the prompt from `references/writer-prompt.md`. Each reads every notes file plus `references/brain-spec.md` and writes its files into the brain folder, following the spec's budgets and rules:

- Writer A: `frameworks.md`, `principles.md`, and `books.md`.
- Writer B: `positions.md` and `stories.md`.
- Writer C: `voice.md`.

Tell each writer the seat's pillar and question, the build folder (so it can open a corpus file to check a quote's context), and that every quote must be copied exactly from the notes with its source id. Writers write only their own files.

When they are back, write `_hot.md` yourself from the six finished files (the spec lists what goes in it, including "where this lens misfires"). Then check the whole brain:

```bash
node .claude/skills/newseat/scripts/check_quotes.mjs <build> .claude/skills/baithak/brains/<slug>
```

Fix until it passes: every quote verbatim, every id right. Read `_hot.md` once more as the agent will: it should tell you how this person decides, in their words, in under 800 words.

## Step 6: Write the agent

Write `.claude/agents/council-<key>.md` from `references/agent-template.md`. Fill every bracket from the brain: the lens (five or six questions this person asks of any decision), how they talk (from `voice.md`), how they debate (name their natural opponents among the seats in `roster.json` and what they concede, from "where this lens misfires"), and the never-list. The description names the pillar, the source count and what the brain is built from, and the trigger phrases ("what would [name] say").

## Step 7: Register the seat

```bash
node .claude/skills/newseat/scripts/add_seat.mjs --key <key> --name "<Full Name>" --short "<Short>" --slug <slug> --pillar "<pillar>" --question "<question>" --dimension "<dimension>" [--default] [--swap <key>]
```

It refuses if the agent file or a brain file is missing. `--default` adds the seat to the default board; `--swap <key>` takes another seat off it in the same move. Then:

- Add one or two "natural tension" lines for the new seat to `.claude/skills/baithak/references/seats.md` (who they will clash with, and over what).

## Step 8: Label the seat

Open `.claude/agents/council-<key>.md` and confirm the first paragraph says the seat is a simulation built from public statements, is not the person, and is not affiliated with or endorsed by them. The template already says this; do not remove it.

## Step 9: Test the seat

New agent files load when Claude Code starts, so test with the fallback the council itself uses: spawn `general-purpose` with `Read .claude/agents/council-<key>.md and follow it as your instructions for this whole task. Only read files; do not write anything.` followed by the single-seat consult prompt from `.claude/skills/baithak/references/round-prompts.md`, on a short sample decision in the seat's pillar. Then check its answer:

- It sounds like the person (compare with `voice.md`), speaks in the first person, and never claims to be them.
- It names frameworks with source ids, and every quote passes `check_quotes.mjs` (save the answer to `<build>/test-consult.md` and run the checker on it).
- It owns its pillar instead of giving generic advice.

If it fails, fix the agent or `_hot.md` and test again, once.

## Step 10: Report

Tell the user, in under 150 words:

- Who was added, their pillar and question, and whether they are on the default board.
- The brain: sources, words, years covered, and the files written.
- How to use them now: `/baithak ask <key> ...` for one answer, `/baithak --seats <key>,nithin,... ...` to seat them, and `/baithak board` to change the default board.
- One line: restart Claude Code (or open a new session) so the seat loads as its own agent type; until then the council uses the fallback automatically.

## Without sub-agents (Codex or a runtime that cannot spawn agents)

Run steps 4 and 5 yourself, one batch at a time: extract a batch into its notes file, then move to the next. Write the brain files one at a time from the notes. Everything else is the same.

## Rules

- Public and lawful sources only. The corpus stays in the build folder and is never committed or shared; the brain holds short quotes (under 45 words) and paraphrase, never book text.
- Every quote in the brain is verbatim and passes `check_quotes.mjs`. A line with no source is inference and says so.
- Do not touch the other seats' brains or agents. Only `roster.json`'s `"seats"` and `"default"` change, through `add_seat.mjs`.
- Plain English in everything you write yourself: short sentences, no em dashes, no filler.
- Never make or add a portrait, photo, cartoon, voice, or likeness of the person.
- Hindi and Hinglish quotes stay in the original script and words, exactly as in the source. Put an English translation after the source id, in square brackets: "..." (S012) [English: ...]. The checker matches the original only.
- Cost: a standard seat is about 8 to 10 sub-agent runs. Say which depth you used.
