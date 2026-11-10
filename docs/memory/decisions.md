# Decisions (with reasons)

Newest at the bottom. If you change a decision, do not delete the old one. Add a new entry that says "supersedes" and why.

## D1. Fork Roast Room, do not build from scratch
- **Date:** 2026-11-05.
- **Decision:** Fork `nateherkai/roast-room` (MIT). Keep its engine: sub-agent seats, brains, three rounds, scoring, quote checks. Replace the seats and add the India layer.
- **Why:** About 80% of the hard work already exists and is tested. Upstream is MIT, so forking is allowed with credit.

## D2. Drop the web room app and the cartoon portraits for v1
- **Date:** 2026-11-05.
- **Decision:** Remove `app/`, `docs/`, the portrait scripts and all portrait assets.
- **Why:** Personality-rights orders in India protect a person's likeness, so portraits are the riskiest part. The app was not needed to run councils. It can come back later as v1.1.

## D3. Real names, with guardrails
- **Date:** 2026-11-05.
- **Decision:** Use real founder names. Every seat is labelled a simulation. Only verbatim quotes with a source id are attributed. Opt-out process: an issue template, honoured within 7 days.
- **Why:** The user wants real founders. Roast Room uses real names too. Guardrails reduce risk. This is not legal advice, and the user has been told an IP-lawyer check is worth doing before going public.

## D4. Court-order check before every seat
- **Date:** 2026-11-05.
- **Decision:** `/newseat` runs three web searches for personality-rights orders before building anything. A hit stops the seat.
- **Why:** Aman Gupta's order (Delhi HC, May 2026) covers his name, voice, likeness and catchphrases. Building a seat for him would be risky.

## D5. Legal gate uses a dated laws folder, not a lawyer persona
- **Date:** 2026-11-05.
- **Decision:** The Chair may cite only files in `.claude/skills/baithak/laws/`. `check_laws.py` fails on missing files, bad fields, or stale dates (over 183 days). GRAY and BLACK verdicts end with "Verify with a lawyer before you build."
- **Why:** Laws in India change often. Gemini's version gave confident, out-of-date rules, including a real-money gaming position that the 2025 Act had banned. A persona would invent citations.

## D6. BLACK-zone veto
- **Date:** 2026-11-05.
- **Decision:** An option in the BLACK zone, citing a law file, cannot get GO or GO WITH CONDITIONS. If all options except "don't do it" are BLACK, the verdict is DON'T DO IT.
- **Why:** Facts beat headcount. A council of happy seats must not override an illegal business model.

## D7. Hindi-aware quote checking
- **Date:** 2026-11-05.
- **Decision:** Both quote checkers normalise Unicode (Devanagari included) and have `--selftest`. Hindi quotes keep their original script, with the English translation after the source id in square brackets.
- **Why:** The old checker turned Hindi quotes into empty strings, so they passed unchecked.

## D8. Seat models run on Sonnet
- **Date:** 2026-11-05.
- **Decision:** Brain writers, extraction agents and seat agents use `model: sonnet`. The main session is Haiku for phases A, B and E, and Sonnet for C and D.
- **Why:** Seat quality depends on the brain and agent files. Haiku would make them weaker.

## D9. Five seats for v1, Aman excluded
- **Date:** 2026-11-05.
- **Decision:** Nithin Kamath (downside guard), Kunal Shah, Sridhar Vembu, Girish Mathrubootham, Deepinder Goyal.
- **Why:** Each has a large body of public English material. Each covers a different pillar and creates real disagreement. Aman is excluded by D4.

## D10. yt-dlp via python -m, with caption fallback
- **Date:** 2026-11-05.
- **Decision:** `fetch.mjs` tries the `yt-dlp` command, then `python -m yt_dlp`, then YouTube's own captions. It takes English captions first, then Hindi.
- **Why:** On Windows, `pip install --user` often leaves the command off PATH. Indian podcasts are often in Hindi.

## D11. Laws to cover (Phase B)
- **Date:** 2026-11-05.
- **Decision:** Payments, digital lending, deposits and pooled investment, SEBI advice and finfluencers, crypto, Aadhaar, telemedicine and e-pharmacy, IT Rules, UPI e-mandates, consumer protection and dark patterns, GST basics, plus the two seed files (Gaming Act 2025, DPDP).
- **Why:** These are the laws that the India-specific test ideas touch.

## D12. ai-job-search is vendored, not merged
- **Date:** 2026-11-05.
- **Decision:** Copy the whole repo into `vendor/ai-job-search/`. Do not copy its skills into the root `.claude/skills/`.
- **Why:** Its skills and commands use paths relative to its own root (`tools/`, `documents/`, `.agents/skills/...`). Copied into the Baithak root, those paths would break. Its personal-data folders are gitignored.

## D13. Memory lives in the repo
- **Date:** 2026-11-05.
- **Decision:** `CLAUDE.md` (auto-loaded), `MEMORY.md` (live state), and `docs/memory/*` (topic files). A pointer note also lives in the user's global Claude memory folder.
- **Why:** The user may end a session and resume a week later. The repo is the one place that survives.

## D14. Git workflow: branch per feature, Claude may push
- **Date:** 2026-11-10.
- **Decision:** Claude commits and pushes to `origin` (cipher-cmd/Baithak, private). One branch per feature (`feat/...`). `main` changes only via merge or PR the user approves. Supersedes the earlier "user does all git" rule.
- **Why:** The user granted authority and wants a clean per-feature history.

## D15. All five seats at --quick depth first
- **Date:** 2026-11-10.
- **Decision:** Build the five v1 seats at `--quick` (12 to 20 sources each). Roster gets a `depth` field. Chair names thin seats in the verdict. Deepen later. Partly supersedes the "standard depth" line in WORKPLAN Phase C. The stop-after-Nithin review stays, but shorter.
- **Why:** Land a working council today; contributors can deepen seats later.
