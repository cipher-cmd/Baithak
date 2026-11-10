# MEMORY: live project state

Last updated: 2026-11-10. Keep this file current. Read it at the start of every session. See `docs/memory/` for topic files.

## Current state (one screen)

- **Project:** Baithak, open-source Indian-market idea council. Fork of Roast Room (nateherkai, MIT).
- **Repo:** `C:\Users\Furqan\Desktop\IndianRoastRoom\baithak`, branch `main`.
  - Git (2026-11-10): Claude MAY commit and push. One branch per feature. All Phase A+B work is committed on `feat/india-layer-and-laws` (pushed to `origin`, repo is private). Remote `main` holds only a README (unrelated history); merge needs `--allow-unrelated-histories` once the user approves.
  - Remotes: `upstream` = nateherkai/roast-room (never push there). `origin` = cipher-cmd/Baithak (private).
- **Seats:** Nithin built 2026-11-10 (seed depth, 9 usable of 12 sources, 209 quotes verified, branch `feat/seat-nithin`, awaiting user review). Kunal built 2026-11-10 (seed, 10 sources, 185 quotes verified, branch `feat/seat-kunal`, stacked on feat/seat-nithin). Girish built 2026-11-10 with seatkit (Haiku extraction, seed, 11 sources, 288 quotes, branch `feat/seat-girish`). Vembu and Deepinder not built: next, same recipe (`build/<slug>/RUNBOOK.md`). `.claude/skills/baithak/roster.json` has an empty roster. Planned v1 seats: Nithin Kamath, Kunal Shah, Sridhar Vembu, Girish Mathrubootham, Deepinder Goyal (Aman Gupta excluded: Delhi HC order, May 2026).
- **Laws:** 14 files in `.claude/skills/baithak/laws/`. Phase B complete (2026-11-05). `check_laws.py --lint` passes. Several files are marked as secondary-source only; see `docs/memory/laws-status.md`.
- **Scripts:** `check_quotes.py` (Baithak, brain quotes, has `--selftest`), `check_laws.py` (has `--selftest`, `--lint`), `check_quotes.mjs` and `fetch.mjs` and `add_seat.mjs` (newseat). All self-tests pass.
- **Tools installed:** yt-dlp 2026.10.26 via `python -m yt_dlp` (not on PATH). `fetch.mjs` finds it automatically. Node 26, Python 3.13.
- **Vendored:** `vendor/ai-job-search/` (full copy of ai-job-search, 2026-11-05). Personal-data paths are gitignored.
- **Current phase:** Phase C (seats) next. Requires Sonnet. See `WORKPLAN.md` Part 4.

## Next step

**Waiting on user review of Nithin** (`build/nithin-kamath/review-consult.md`). If approved: build Kunal, Girish, Vembu, Deepinder at `--quick`, one branch per seat batch.


0. Decision D15: all five seats at `--quick` depth, Nithin first, short review, then the rest. Branch per seat batch: `feat/seat-nithin`, then `feat/seats-v1-rest`.
1. Session model is Sonnet (set 2026-11-10).
2. User says: `Read CLAUDE.md, MEMORY.md, then WORKPLAN.md, and do the next unticked task.`
3. The next task is the Phase C preflight in A1 (fetch smoke test, Hindi caption check), then C0 (personality-rights check for Nithin), then `/newseat Nithin Kamath`, then the **stop for review** after Nithin.

## Open decisions and questions for the user

- Project name: "Baithak" chosen. Confirmed.
- Real names with guardrails: chosen. Opt-out issue template in `.github/ISSUE_TEMPLATE/remove-my-seat.md`.
- IP-lawyer check before going public: still open (the user has not decided).
- Whether to run `/setup` in `vendor/ai-job-search`: not yet. Warn the user first. `/setup` writes personal data into tracked files. Use a private copy for personal data.
- Public or private GitHub repo: not decided. Phase E in WORKPLAN.

## Last session

2026-11-05. See `docs/memory/session-log.md` for the full list.
