# User preferences and instructions (append-only log)

Every instruction the user has given, in order, with the date. Newest at the bottom. Obey all of them unless the user changes one. When the user gives a new instruction, add it here at once.

## Working style

- **2026-11-05. Explain like a complete beginner.** The user is a newcomer to this kind of work. Give step-by-step guidance, as if pointing at a menu ("top right of the screen"). Use full sentences for explanations.
- **2026-11-05. Write plans precise enough for a smaller model.** The user wants Haiku to be able to run the build plan without mistakes. Keep `WORKPLAN.md` exact: exact commands, expected output, stop conditions.
- **2026-11-05. Work phase by phase.** Do one phase, stop, report. At the end of each phase, tell the user which model to switch to for the next one (`/model haiku` or `/model sonnet`) and what to type next.
- **2026-11-05. Stop for review after the first seat.** Build Nithin Kamath first, then wait for the user's OK before the other four.
- **2026-11-05. Ask before anything outward-facing.** Publishing, pushing, and making the repo public all need the user's explicit go-ahead.

## Git and publishing

- **2026-11-05. Do not commit or push anything.** The user will commit and push manually. Anything committed by Claude would be attributed to Claude, and the user does not want that. Claude's two earlier local commits were undone (soft reset to `e40f406`) on the user's request.
- **2026-11-05. Create the GitHub repo is the user's job.** The user created `https://github.com/cipher-cmd/Baithak`. Claude must not push to it. Claude must not push to `upstream` (nateherkai/roast-room) either.
- **2026-11-05. No attribution lines in anything the user might commit.** Do not add `Co-Authored-By` or "Generated with Claude Code" to any text meant for the repo.

## Project identity

- **2026-11-05. Name: Baithak.** The user liked it. The project was renamed from "India Roast Room" to Baithak entirely.
- **2026-11-05. Open source, free, for anyone in India** building ideas. No paid tier in v1.
- **2026-11-05. Real names are fine, with guardrails.** Every seat says it is a simulation, not endorsed by the person. Only verbatim sourced quotes are attributed. No portraits or voices. Opt-out process must exist.
- **2026-11-05. Use the first five seats:** Nithin Kamath, Kunal Shah, Sridhar Vembu, Girish Mathrubootham, Deepinder Goyal. More can be added later.
- **2026-11-05. Aman Gupta is excluded**, because of the Delhi High Court personality-rights order. Claude suggested Deepinder Goyal as his replacement; the user accepted the five-seat list.
- **2026-11-05. Gemini's India content is the base for the India layer**, but its seat descriptions are not used. Its legal table had errors; every law must be verified before use.

## Tools and setup

- **2026-11-05. Include the ai-job-search skill in the setup.** The user gave the repo `https://github.com/ai-job-search-dev/ai-job-search`. It is vendored into `vendor/ai-job-search/` (see `docs/memory/ai-job-search.md`).
- **2026-11-05. Memory must persist across sessions.** The user may end a session and come back a week later. `CLAUDE.md`, `MEMORY.md` and `docs/memory/` must always be current. Update them as the work progresses, and add every new instruction here.
- **2026-11-05. Use the Haiku model for the early phases** (A, B, E) and Sonnet for seat building and council runs (C, D). The user set Haiku as the default model.

## Updates 2026-11-10

- **2026-11-10. Git permission granted (supersedes the 2026-11-05 "do not commit or push" rule).** Claude may commit and push to `cipher-cmd/Baithak`. The user made the repo private. Full authority for commits and pushes.
- **2026-11-10. One branch per new feature or big task.** Every time something new is integrated, planned or built, make a new branch (`feat/<topic>`) and push there. Make it a habit. Do not pile everything into one branch.
- **2026-11-10. Still no Claude attribution lines in commits** (earlier rule stands; the user did not lift it).
- **2026-11-10. Build all 5 seats at `--quick` depth first** (user agreed). Deepen later, ideally with contributors.
- **2026-11-10. User wants Claude to act as an advisor on open-source growth:** how to market, make public, and get contributors.
- **2026-11-10. User wants a token-cost estimate** for the 5 quick seats before building.
