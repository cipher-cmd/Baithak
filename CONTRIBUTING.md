# Contributing to Baithak

Thank you for helping. Baithak is only as good as its law files and its advisors' sources, and both get better with more eyes.

## The most useful contributions

1. **Check a law file against the official text.** Every file in `.claude/skills/baithak/laws/` has a "Watch for" section listing what was not verified. Many were built from law-firm summaries because official sites block automated reading. If you can open the official text (RBI, SEBI, India Code, the Gazette, a regulator's site), fix what differs, put the official URL first in `sources`, update `last_verified`, and remove the "not opened" line.
2. **Add a missing law.** Wanted: state shop and trade licences, FDI rules for e-commerce, drones, agri-marketing (APMC), AI rules, clinical establishments. Use the template in `.claude/skills/baithak/laws/README.md`.
3. **Add sources for an advisor.** Long, public material where the person is the main speaker. Their own writing (letters, blog posts, long threads) beats interviews. Open a "Add sources" issue with the links.
4. **Propose a new advisor.** Open a "Propose a seat" issue. We run the personality-rights court-order check ourselves before building anything.
5. **Report a bad verdict.** Ran Baithak and the Chair or an advisor got it wrong? Open a "Bad verdict" issue with the session's `verdict.md`.

## Rules for law files

- Every fact comes from a page you opened. Never from memory.
- Prefer, in order: official text, then reputable law firms or legal news, then national news.
- Body under 300 words, plain English, no em dashes.
- Run `python .claude/skills/baithak/scripts/check_laws.py --lint` before opening a pull request. It must print `lint ok`.

## Rules for advisors

- Seats are simulations built from public statements. Only verbatim quotes with a source id are attributed to the real person.
- No portraits, photos, voices, or likenesses of real people, anywhere: not in the repo, not in issues, not in social posts.
- We never build a seat for anyone with a personality-rights court order.
- Raw transcripts stay on your machine (`build/` is gitignored). Only the brain ships.
- Build with `/newseat <Full Name>`; the repeatable steps are scripted in `.claude/skills/newseat/scripts/seatkit.py`.

## Before you open a pull request

Run the checks (CI runs them too):

```bash
python .claude/skills/baithak/scripts/check_quotes.py --selftest
python .claude/skills/baithak/scripts/check_laws.py --selftest
python .claude/skills/baithak/scripts/check_laws.py --lint
node .claude/skills/newseat/scripts/check_quotes.mjs --selftest
python .claude/skills/newseat/scripts/seatkit.py --selftest
```

One feature or fix per pull request, on its own branch.

## Opt-out

If you are one of the people an advisor is built from, or represent them, use the "Remove my seat" issue. We remove it within 7 days, no questions asked.
