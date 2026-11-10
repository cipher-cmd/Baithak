# Workflow phases and which model to use

The full build plan is `WORKPLAN.md`. This file says which phase needs which model and how to switch.

## How to start any session

1. In a terminal: `cd C:\Users\Furqan\Desktop\IndianRoastRoom\baithak` then `claude`. Start inside this folder, or the project skills will not load.
2. Set the model for the phase you are on (table below).
3. Type: `Read CLAUDE.md, MEMORY.md, then WORKPLAN.md, and do the next unticked task.`

## Phase table

| Phase | What it covers | Model | Status (2026-11-05) |
|---|---|---|---|
| A | Setup: yt-dlp, baseline check | Haiku | A1 and A2 done |
| B | 14 law files (verified from sources) | Haiku | **Done** |
| C | Build seats: Nithin first (then stop for review), then the other four | **Sonnet** | Next |
| D | Test councils (WHITE, BLACK, GRAY ideas), comparison with plain Claude | **Sonnet** | Not started |
| E | Publishing: `gh auth login`, private repo, public only with the user's go-ahead | Haiku | Not started |

## Switching models

- Haiku to Sonnet: type `/model sonnet`.
- Sonnet to Haiku: type `/model haiku`.
- The default model for new sessions was set to Haiku by the user on 2026-11-05.

## End-of-phase rule

At the end of each phase, Claude must:
1. Tell the user what was done, in plain words.
2. Name the next phase and the model to switch to, with the exact command.
3. Give the exact message to type next.
4. Update `MEMORY.md` and `docs/memory/session-log.md`.

## Stop points

- **After C1 (Nithin):** stop. Wait for the user to review the seat and the consult answer.
- **Before public release (E4):** the user must say "make it public".
- **Before any commit:** Claude never commits. The user does.
