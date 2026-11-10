# docs/memory: index

These files hold the project's memory. Claude reads them when a session starts and when a task needs them. Keep them current. The rules for keeping them current are in `CLAUDE.md`.

| File | What it holds | When to read it |
|---|---|---|
| `../../MEMORY.md` | Live state: current phase, next step, open questions | Every session, first |
| `user-preferences.md` | Every instruction the user has given, dated | Every session, second |
| `decisions.md` | Design and policy decisions, with the reason for each | Before changing a design |
| `skills.md` | Every skill, command, agent, script and how to invoke it | When a task uses one |
| `workflow-phases.md` | Phases, which model to use, how to switch | At the start of a phase, and at its end |
| `laws-status.md` | Confidence for each law file and what is still unverified | Before citing or editing a law file |
| `ai-job-search.md` | The vendored job-search framework: where it is, how to use it, privacy rules | When working on job search |
| `session-log.md` | Dated log of what each session did | To catch up after a break |

Related: `../../CLAUDE.md` (instructions for Claude, auto-loaded), `../../WORKPLAN.md` (the build plan with tick boxes).
