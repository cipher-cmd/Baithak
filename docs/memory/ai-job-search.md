# ai-job-search (vendored setup)

## What it is

`ai-job-search` is an MIT-licensed Claude Code framework by Mads Lorentzen (repo: `https://github.com/ai-job-search-dev/ai-job-search`). It turns Claude Code into a job-application assistant: profile setup, job scraping, fit ranking, CV and cover letter tailoring (LaTeX), interview prep, and outcome tracking. Its job portal skills are built for Denmark (Jobindex, Jobnet, Akademikernes Jobbank, Freehire, LinkedIn). The core workflow is country-agnostic.

## Where it lives in this setup

- **Path:** `C:\Users\Furqan\Desktop\IndianRoastRoom\baithak\vendor\ai-job-search\`
- **How it was added:** on 2026-11-05 a copy of the upstream repo (commit `87d1857`, "fix(install): find bun at standard install locations") was copied in, without `.git` and without `tests/` folders.
- **Why vendored, not merged:** its skills and commands use paths relative to its own root. Copying them into Baithak's root `.claude/skills/` would break those paths.
- **Its own `CLAUDE.md`, `AGENTS.md`, `SETUP.md`, and `.claude/` apply when you open Claude Code inside that folder.**

## How to use it

1. Open a terminal: `cd C:\Users\Furqan\Desktop\IndianRoastRoom\baithak\vendor\ai-job-search` then `claude`.
2. Follow its `SETUP.md`. Prerequisites: Claude Code, Python 3.10+, Bun, a LaTeX distribution (for CV and cover letters), pypdf optional.
3. First-time profile: `/setup`. **Warning:** `/setup` writes personal data (name, contact, employment history, salary expectations) into tracked files. Do this only in a private copy, not in the public Baithak repo. Ask the user before running it.

## Privacy protection in the Baithak repo

`.gitignore` in the Baithak root now ignores the personal-data paths inside `vendor/ai-job-search/`:
- `documents/*` (except `README.md` and `.gitkeep` folders)
- `company_research/*`, `job_scraper/*` (except `.gitkeep`)
- `cv/*.tex` (except `main_example.tex`)
- `cover_letters/*.tex` (except `cover_example.tex`); `cover.cls` stays tracked
- `.claude/settings.local.json`
- `salary_data/`

Verify any time with: `git check-ignore -v vendor/ai-job-search/cv/main.tex`.

## Not copied

- `.git/` (not needed)
- `tests/` folders inside the Bun CLIs. Re-copy them if you want to run the CLI test suite.
- `.claude/settings.local.json` (personal, gitignored if present).

Its `.claude/settings.json` IS copied, inside `vendor/ai-job-search/.claude/`. It applies only when Claude Code is started inside `vendor/ai-job-search/`, not from the Baithak root. Baithak's own `.claude/settings.json` is separate.

## Safety notes from the review (2026-11-05)

- No hooks in its `settings.json`.
- Its `settings.json` allows `bun run` of its portal CLIs and `python tools/...` scripts. It denies `.env`, SSH and AWS reads, and POST/PUT uploads by curl.
- Its skills treat job postings and company pages as untrusted data (`09-web-research.md`). Keep that rule.
- No `curl |`, `wget |`, `eval`, or base64 found in its `.claude` or `tools`.

## Upstream updates

The upstream has an update check (`tools/check_upstream_updates.py`). Re-vendoring is a manual copy from a fresh clone. Note the date and commit here each time.
