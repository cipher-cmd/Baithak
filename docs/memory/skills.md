# Skills, commands, agents and scripts: what each does and how to use it

Read this when a task needs one of them. Each entry says what it is, where it lives, when to use it, the exact invocation, and what it writes. Update the entry whenever the skill changes.

## Baithak skills (in this repo)

### `/baithak` (`.claude/skills/baithak/SKILL.md`)
- **What:** Runs a council on one idea or decision. The Chair runs India checks, seats argue over three rounds, the Chair writes a verdict.
- **Use when:** the user brings an idea or decision for India, or asks "what would <name> say", or asks to "ask <seat>".
- **Invocations:**
  - `/baithak <idea>`: full council (confirm the board first).
  - `/baithak --quick <idea>`: four seats, two rounds. Recommend this to first-time users.
  - `/baithak --seats nithin,kunal <idea>`: named seats.
  - `/baithak ask nithin <question>`: one seat, one answer.
  - `/baithak board`: show or change the default board.
- **Writes:** `sessions/<date>-<idea>/` with `brief.md`, `india-checks.md`, `round-1.md`, `round-2.md`, `round-3.md`, `draft-resolution.md`, `verdict.md`.
- **Status:** the roster is empty, so only the India checks work until seats exist.

### `references/` (inside the baithak skill)
- `seats.md`: the planned v1 seats, weights, natural tensions.
- `india-filters.md`: the four India tiers, the 5 friction filters, the 4 scalability bottlenecks. Read in Step 2.
- `evidence-ladder.md`: validation levels 0 to 5. Read in Step 1.
- `legal-gate.md`: WHITE, GRAY, BLACK rules and the "cite only laws/" rule. Read in Step 2.
- `round-prompts.md`: exact prompt for each seat, each round, and the single-seat consult.
- `scoring.md`: score maths, verdict bands, overrides (BLACK veto, ruin cap, one-way door cap, UNMAPPED cap).
- `report-template.md`: the verdict layout.

### `laws/` (inside the baithak skill)
- One file per law. Template and rules in `laws/README.md`. Each file has `last_verified`, `zone_trigger`, `sources`.
- Verifier: `python .claude/skills/baithak/scripts/check_laws.py --lint` (all files) or `check_laws.py <session folder>` (citations in a session).

### `scripts/check_quotes.py` (baithak)
- **What:** checks that every quote attributed to a brain source appears in the brain. Unicode-aware.
- **Invocation:** `python .claude/skills/baithak/scripts/check_quotes.py <session folder>`. Self-test: `python .claude/skills/baithak/scripts/check_quotes.py --selftest`.
- **Output:** `brain quotes verified: N; ... unverified: 0` (must be 0).

### `brains/` and `.claude/agents/`
- `brains/<slug>/`: eight files per seat (`_hot.md`, `frameworks.md`, `principles.md`, `positions.md`, `voice.md`, `stories.md`, `books.md`, `sources.md`). Built by `/newseat`. Empty until the first seat.
- `.claude/agents/council-<key>.md`: one agent per seat. Built by `/newseat`.

## Seat-builder skill (`.claude/skills/newseat/SKILL.md`)

### `/newseat <Full Name>`
- **What:** builds one seat. Step 0 is the personality-rights court-order check. Then sources, extraction, brain, agent, roster.
- **Use when:** the user says "add a seat", "add <name> to the council", or wants a new advisor.
- **Flags:** `--quick` (12 to 20 sources), default (30 to 50), `--deep` (80+). Pass `--default` to put the seat on the default board.
- **Rules:** no portraits, no voice, no likeness. Hindi quotes keep original script with English in square brackets.
- **Steps (in order):**
  - Step 0: court-order check (`"NAME" personality rights High Court`, `"NAME" Delhi High Court injunction name image voice`, `"NAME" deepfake court order`).
  - Step 1: name, key, slug, short name, dimension.
  - Step 2: find sources (WebSearch). Indian source hints are in the skill.
  - Step 3: fetch (`node .claude/skills/newseat/scripts/fetch.mjs <build> --list <build>/urls.txt`).
  - Step 4: extract (parallel Sonnet agents, one per batch).
  - Step 5: write brain (three Sonnet writers).
  - Step 6: write agent from `references/agent-template.md`.
  - Step 7: register (`add_seat.mjs`).
  - Step 8: label check (the simulation disclaimer is present).
  - Step 9: test consult.
  - Step 10: report.

### `scripts/fetch.mjs`
- **What:** turns web pages, YouTube videos, or local files into corpus files with source ids (S001, S002...).
- **Invocations:**
  - `node .claude/skills/newseat/scripts/fetch.mjs <build> <url> [<url>...]`
  - `node .claude/skills/newseat/scripts/fetch.mjs <build> --list <build>/urls.txt`
  - `node .claude/skills/newseat/scripts/fetch.mjs <build> --add <file> --title "..." --date YYYY-MM-DD`
  - `node .claude/skills/newseat/scripts/fetch.mjs <build> --manifest`
- **Writes:** `<build>/corpus/S0xx-*.md`, `<build>/sources.json`. Build folder is gitignored.
- **Env:** `NO_YTDLP=1` skips yt-dlp.

### `scripts/check_quotes.mjs` (newseat)
- **Invocation:** `node .claude/skills/newseat/scripts/check_quotes.mjs <build> <file or folder>`. Self-test: `node .claude/skills/newseat/scripts/check_quotes.mjs --selftest`.
- **Pass:** `wrong source id: 0; not found: 0`.

### `scripts/add_seat.mjs`
- **What:** writes one seat into `roster.json`. Refuses if the agent or any brain file is missing.
- **Invocation:** `node .claude/skills/newseat/scripts/add_seat.mjs --key nithin --name "Nithin Kamath" --short Nithin --slug nithin-kamath --pillar "..." --question "..." --dimension "..." [--default] [--swap <key>]`

### `references/`
- `brain-spec.md`, `extract-prompt.md` (Sonnet), `writer-prompt.md` (Sonnet), `agent-template.md` (includes `model: sonnet`).
- `example/`: the upstream Paul Graham seat, kept only as a format reference. It is not a Baithak seat and is not in the roster.

## Vendored skills (inside `vendor/ai-job-search/`)

These load only when you work inside that folder (its `.claude/` is project-level there). See `docs/memory/ai-job-search.md`. Paths in these files are relative to `vendor/ai-job-search/`.

- **Skills** (`.claude/skills/`):
  - `job-application-assistant`: job fit evaluation, CV tailoring, cover letters, interview prep. Reads the candidate profile in its own `CLAUDE.md`.
  - `scrape` (folder `job-scraper`): finds new postings through the portal CLIs. Triggers on "find jobs", "job scrape".
  - `upskill`: skill gaps against tracked postings and a learning plan. Triggers on "/upskill", "skill gaps".
- **Commands** (`.claude/commands/`, typed as `/name`): `setup`, `add-portal`, `add-template`, `apply`, `expand`, `gmail-sync`, `html-report`, `interview`, `notion-sync`, `outcome`, `rank`, `reset`.
  - `/setup` writes the user's personal data into tracked files. Do not run it in a public copy.
  - `gmail-sync` and `notion-sync` connect to external accounts. Ask the user first.
- **Agents** (`.claude/agents/`): `posting-fetcher`, `posting-scorer`, `application-reviewer`. Spawned by the commands.
- **Portal CLIs** (`.agents/skills/*/cli`): `jobbank-search`, `jobdanmark-search`, `jobindex-search`, `jobnet-search`, `linkedin-search`, `freehire-search`. Run with Bun, for example `bun run .agents/skills/jobindex-search/cli/src/cli.ts`.
- **Tools** (`tools/`): `rank_state.py`, `scrape_state.py`, `job_key.py`, `verify_pdf.py`, `verify_layout.py`, `robots_check.py`, `fetch_page.py`, `posting_guard.py`, `security_guards.py`, `install_portal_clis.py`, and others. Used by the skills.

## Other tools

- **Git:** the user commits. Claude may only run `git status`, `git diff`, `git log`, `git rev-parse`.
- **yt-dlp:** `python -m yt_dlp --version` (installed 2026-11-05).
- **Self-tests (run all of these after any script change):**
  - `python .claude/skills/baithak/scripts/check_quotes.py --selftest`
  - `python .claude/skills/baithak/scripts/check_laws.py --selftest`
  - `python .claude/skills/baithak/scripts/check_laws.py --lint`
  - `node .claude/skills/newseat/scripts/check_quotes.mjs --selftest`
