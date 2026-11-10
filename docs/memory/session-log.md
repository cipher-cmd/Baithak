# Session log (append newest at the bottom)

Each entry: date, model, what was done, what changed, what is next. Keep entries short and factual.

## 2026-11-05 (session 1, model: Opus 5.5 then Haiku 5.5)

- Read the Gemini file (`india_roast_validator_skill.md`). Judged it useful for the India layer, but its seats were invented and its legal table had errors (real-money gaming and DPDP timing).
- Cloned Roast Room, read its engine and seat-building pipeline.
- Chose the name Baithak. Chose five seats and real names with guardrails. Excluded Aman Gupta (Delhi HC personality-rights order, May 2026).
- Wrote the plan at `IndianRoastRoom/PLAN.md` (now marked superseded) and `baithak/WORKPLAN.md`.
- Cloned upstream into `baithak/`. Removed the US seats, the web app, the portrait pipeline. Renamed skills to `baithak` and `newseat`.
- Fixed the quote checkers for Hindi (Unicode). Added `check_laws.py` (self-test and lint). Added `--selftest` to all checkers.
- Fixed `fetch.mjs`: Hindi caption tracks, `python -m yt_dlp` fallback.
- Pinned brain writers, extraction agents and seat agents to Sonnet.
- Added the personality-rights check (Step 0) to `/newseat`. Removed portraits from `/newseat`.
- Wrote the India layer references and the legal gate. Added the BLACK-zone veto and the UNMAPPED cap to `scoring.md`.
- Made two local commits, then undid them on the user's instruction (soft reset to `e40f406`). All work is uncommitted.
- Installed yt-dlp 2026.10.26 with `python -m pip install --user`. Smoke-tested a 10,104-word transcript.
- **Phase B (laws) done.** Wrote 12 new law files (14 total). Lint passes. Many sources were secondary; see `laws-status.md`.
- Vendored `ai-job-search` into `vendor/ai-job-search/`. Added its personal-data paths to `.gitignore`.
- Created memory system: `CLAUDE.md` (rewritten), `MEMORY.md`, and `docs/memory/` (user-preferences, decisions, skills, workflow-phases, laws-status, ai-job-search, session-log).

**Next:** Phase C on Sonnet. Preflight: A1 fetch smoke test and Hindi check. Then C0 for Nithin Kamath, then `/newseat`. Stop after Nithin for the user's review.

## 2026-11-10 (session 2, model: Opus 5.5 then Sonnet 5.5)

- Reviewed state; all self-tests pass; upstream Roast Room unchanged (2,039 stars, 474 forks).
- User granted git authority and asked for a branch per feature. Updated CLAUDE.md, user-preferences, decisions D14 and D15.
- Added `origin`, committed Phase A+B on `feat/india-layer-and-laws`, pushed. Remote `main` has only a README.
- Gave the user a token estimate for 5 quick seats and an open-source growth plan.

**Next:** user confirms; build Nithin at `--quick` on `feat/seat-nithin`.
- Built Nithin Kamath seat at seed depth on `feat/seat-nithin`. Court-order check clean. 12 sources, S005 and S006 garbled (Devanagari phonetics / spam captions), S009 has no Nithin words. 9 usable. Consult test passed after one source-id fix (S003). Added `--depth` and `--sources` to add_seat.mjs. YouTube search trick: `python -m yt_dlp "ytsearch6:query" --flat-playlist --print "%(duration)s|%(id)s|%(channel)s|%(title)s"` finds long videos without inventing URLs. YourStory returns HTTP 403 to fetch.mjs.
- Built Kunal Shah seat (seed depth, 10 videos, 125k words, 605 note quotes, 185 brain quotes) on `feat/seat-kunal`. Consult on the D1 GST idea passed. Delta 4 appears only in S001, S002, S005, S007, S010; India 1/2/3 labels not used by him (no recorded position). Branches are stacked: kunal on nithin.
- **Token cost per seat (sum of subagent usage as reported by the harness; excludes the main session's own tokens):** Nithin about 898k (extraction 433k, writers 370k, consult 94k). Kunal about 1.04M (extraction 575k, writers 367k, consult about 95k). Rule of thumb: about 1M per seed seat. Cheaper next time: fewer and shorter sources (one 3-hour video costs about 30k words), skip garbled captions before extraction.
- seatkit.py built and tested on Nithin (screening catches S005 spam, S006 Devanagari, S009 short) and Kunal (finish passes). Fixed add_seat colour drift on re-register. Girish set up with seatkit up to extraction; paused for the user to switch to Haiku.
- Built Girish with seatkit end to end. **Recipe that worked (use for every next seat):** Opus/Sonnet main session does rights check (3 WebSearch calls, alone in one message), `discover` (2 passes), hand-picks URLs, `fetch`, `plan`; extraction agents spawned with `model: haiku` and the one-line prompt "Read build/<slug>/prompts/extract-NN.md and follow it exactly"; main session re-runs the quote check itself (never trust the agent's claim); writers `model: sonnet` with the same one-line pattern; main session writes `_hot.md` and the agent file; consult on Sonnet; `finish` must print ALL CHECKS PASS.
- **Haiku extraction result:** 397 quotes, 0 errors, 52 frameworks, 66 rules, 142 positions across 2 batches. Same quality bar as Sonnet. Tokens 534k (Kunal on Sonnet: 575k), so the count is similar but Haiku tokens cost far less of the plan.
- **Girish total:** 988k sub-agent tokens (extraction 534k Haiku, writers 373k Sonnet, consult 81k). Logged in `build/girish-mathrubootham/cost.tsv`.
- seatkit fixes found on this run: plan now creates the brain folder (fetch --sources-md needed it), command echo flushes, stdout forced to UTF-8 (₹ crashed cp1252).
