# Baithak

**Baithak** (बैठक, "a sitting, a meeting") is a council of AI advisors for people building in India. Bring an idea, and the council argues it out. You get back a scored verdict, a reframed version of your idea, a 7-day test under ₹5,000, and the point at which you should walk away.

Each advisor is built from one Indian founder's public statements: their interviews, podcasts, posts, and talks. Every quote is verbatim and linked to its source. Before the advisors speak, a Chair runs the checks that US-style validation skips:

- **Who pays?** India 1, India 2, India 3, or India-to-Global.
- **5 friction filters:** the ₹12k employee test, the hard-money anchor, the CA/munim gatekeeper, payment and collection friction, and public rails like UPI and ONDC.
- **Scalability:** the metro bubble, USD cost vs INR revenue, linear human ops, and pin-code and language walls.
- **Legal zone:** WHITE, GRAY, or BLACK, cited only from a dated `laws/` folder with sources.

> **Status: under construction.** The engine and India checks are in place. Seats are being built (see `WORKPLAN.md`). Until a seat is built, `/baithak` can run the India checks alone.

## The planned council

| Seat | Pillar | The question they own |
|---|---|---|
| Nithin Kamath | Trust, regulation, and capital discipline | Will Indians trust you with their money or data without you burning cash to buy them? |
| Kunal Shah | Consumer behaviour and India 1 vs Bharat | Is this a big enough leap over today's jugaad that nobody goes back? |
| Sridhar Vembu | Frugal R&D, Bharat, and bootstrapping | Can you build real depth cheaply, outside the metro bubble, without VC money? |
| Girish Mathrubootham | B2B SaaS and India-to-global | Why sell this for ₹999 in India when the world will pay $500? |
| Deepinder Goyal | Consumer habit and operations at scale | Is this a daily habit, and what breaks at 10,000 orders a day? |

## What you need

- [Claude Code](https://claude.com/claude-code). Your Claude plan covers it; no API key needed.
- Python 3 (for the quote and law checkers). Node.js 20+ and `yt-dlp` only if you build new seats.

## Run a baithak

```bash
git clone https://github.com/cipher-cmd/baithak.git
cd baithak
claude
```

Then type `/baithak` and your idea. Include:
- the idea in one line;
- who pays and how (UPI, annual, per transaction, COD);
- what customers do today instead;
- how you will reach your first 20 customers;
- your budget, time, and which way you are leaning.

```
/baithak --quick I want to build a WhatsApp GST billing assistant for hardware shops in
Tier-2 cities at ₹999/month. Today their munim does it in a notebook and Tally. I'd sell through
local CAs. I have ₹3 lakh and 6 months. Leaning yes because CAs I spoke to liked it.
```

More ways to run it:
- `--quick`: four seats, two rounds. Start here; it uses far less of your plan.
- `--seats nithin,kunal`: seats only the advisors you name.
- `ask nithin ...`: one answer from one seat.
- `board`: shows and changes the default board.
- `/newseat <name>`: builds a new advisor from public sources.

Councils are saved in `sessions/<date>-<idea>/`.

## Important

- **The seats are simulations** built from public statements. They are not the people named, are not affiliated with or endorsed by them, and do not speak for them. Only verbatim quotes with a source id are attributed to the real person.
- **No portraits, photos, or voices** of real people, ever.
- **Not legal or financial advice.** The legal zone flags what to check. GRAY and BLACK always mean: verify with a lawyer before you build.
- **Opt-out:** if you are one of the people a seat is built from (or represent them), open a ["Remove my seat" issue](../../issues/new?template=remove-my-seat.md). We remove it within 7 days, no questions asked.
- Raw transcripts used to build seats stay on the builder's machine (`build/` is gitignored). Only the brains ship: summaries and short quotes with links.

## Credits

Baithak is a fork of [Roast Room](https://github.com/nateherkai/roast-room) by nateherkai / AI Automation Society (MIT). The council engine, brain format, and seat-building pipeline come from there. The India checks, legal gate, Indian seats, and Hindi-aware quote checking are Baithak's. MIT licence; see `LICENSE`.
