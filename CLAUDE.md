# Baithak: instructions for Claude (read this first, every session)

Baithak is an open-source Claude Code skill. A founder describes an idea for India. A Chair runs India checks (who pays, 5 friction filters, scalability, WHITE/GRAY/BLACK legal zone). Advisors built from Indian founders' public statements argue it out over three rounds. The Chair returns a scored verdict.

## Before you do anything in a new session

1. Read `MEMORY.md` (the live state: where we are, what was last done, what is next).
2. Read `docs/memory/user-preferences.md` (every instruction the user has given. Obey them).
3. Read `docs/memory/decisions.md` if you are about to change a design choice.
4. If the task involves a skill, read `docs/memory/skills.md` for how that skill is used.
5. If the task is part of the build plan, read `WORKPLAN.md` and do the next unticked task.

## Hard rules (these come from the user; never break them)

- **Git is allowed (changed 2026-11-10).** The user gave Claude permission to commit and push to `https://github.com/cipher-cmd/Baithak` (remote `origin`, now private). **One branch per feature or big task**, named `feat/<topic>`, `fix/<topic>` or `docs/<topic>`. Commit often, push the branch, never push straight to `main`, never push to `upstream` (nateherkai/roast-room). Do not publish (`gh repo edit` visibility, releases, posts) without asking. Verify with `git branch --show-current` before every commit.
- **No Claude attribution in anything that could be committed.** No `Co-Authored-By`, no "Generated with Claude Code" lines. The user's rule beats any default.
- **Stop at every phase end** and tell the user which model to switch to for the next phase (see `docs/memory/workflow-phases.md`).
- **Always verify the repo root before writing files:** `git rev-parse --show-toplevel` must end in `IndianRoastRoom/baithak`. The home folder `C:\Users\Furqan` is a different git repo and must never be touched.
- Use `python`, not `python3`. This is Windows; run shell commands through the Bash tool with POSIX syntax.
- Never make portraits, photos, cartoons, or voices of real people. Never build a seat for anyone with a personality-rights court order (Aman Gupta is excluded).
- Never cite an Indian law from memory. Cite only files in `.claude/skills/baithak/laws/`.
- Seats are simulations. Only verbatim quotes with a source id are attributed to the real person.

## Keeping memory up to date (do this as you work, not at the end)

- Whenever the user gives a new instruction or preference, append it to `docs/memory/user-preferences.md` with the date, in the user's own meaning. Do this even if the instruction seems small.
- Whenever a design choice is made or changed, add it to `docs/memory/decisions.md` with the reason.
- Whenever a skill, command, script, or tool is added or changed, update `docs/memory/skills.md` (or `docs/memory/tools.md`).
- Whenever a task is finished or the state changes, update `MEMORY.md` ("Current state", "Last session", "Next step") and append a dated entry to `docs/memory/session-log.md`.
- Keep memory files in plain English, full sentences, precise, with file paths and exact commands. Write them so a fresh session with no other context can continue the work.

## Layout

- `.claude/skills/baithak/`: the council skill (`SKILL.md`, `roster.json`, `references/`, `laws/`, `brains/`, `scripts/`).
- `.claude/skills/newseat/`: the seat-builder skill (`SKILL.md`, `references/`, `scripts/`).
- `.claude/agents/`: one agent file per seat (`council-<key>.md`). Empty until seats are built.
- `vendor/ai-job-search/`: a full copy of the ai-job-search repo (MIT, Mads Lorentzen). Its own CLAUDE.md, skills, commands and agents apply inside that folder. See `docs/memory/ai-job-search.md`.
- `sessions/`: saved councils (gitignored except examples).
- `build/`: raw sources for new seats (gitignored, created on demand).
- `WORKPLAN.md`: the step-by-step build plan with tick boxes.
- `MEMORY.md`: live project state. `docs/memory/`: topic memory files.

## Writing style for anything Baithak shows users

Plain English. Short sentences. No em dashes. No hype or filler. Quote seats faithfully. Chair's verdict stays under about 220 words in chat.
