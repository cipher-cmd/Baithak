# Baithak WORKPLAN

## How to start a work session (the user does this)

1. Open a terminal and run:
   ```
   cd C:\Users\Furqan\Desktop\IndianRoastRoom\baithak
   claude
   ```
   Claude Code must start **inside this folder**. The `/baithak` and `/newseat` skills live in this folder and load only when the session starts here.
2. Pick the model for the phase you are on:
   - **Phases A, B, E:** `/model haiku` is fine.
   - **Phases C and D:** `/model sonnet`. Building seats and running councils means writing `_hot.md`, the seat agent file, and the Chair's verdict. That is judgment work, and these files decide Baithak's quality. Haiku would make the seats noticeably worse.
3. Type: `Read CLAUDE.md, MEMORY.md, then WORKPLAN.md, and do the next unticked task.`

Memory files (keep them current as you work; see `CLAUDE.md`): `MEMORY.md`, `docs/memory/*`.

If the next unticked task is in Phase C or D and the session is on Haiku, say: "The next task needs Sonnet. Please run `/model sonnet` and ask me again." Then stop.

---

This file is the build plan. It is written so a smaller model (Claude Haiku) can execute it task by task without judgment calls. Follow it exactly. When something is not covered here, **stop and ask the user**. Do not improvise.

Repo root: `C:\Users\Furqan\Desktop\IndianRoastRoom\baithak` (in Git Bash: `/c/Users/Furqan/Desktop/IndianRoastRoom/baithak`).

---

## Part 1: Hard rules (read before every session)

1. **Work only inside the repo root.** Every command runs from the repo root. Before any `git` command, run `git rev-parse --show-toplevel`. It must print a path ending in `IndianRoastRoom/baithak`. If it prints anything else (for example `C:/Users/Furqan`), **stop**. The home folder is a different git repo, and committing there would ship the user's unrelated files.
2. **Never use `git add -A` or `git add .`** Add only the paths the task names.
3. **Never push, never create a GitHub repo, never make anything public** unless the task says so and the user has said yes in this session.
4. **Never write a fact about an Indian law from memory.** Every law fact comes from a web page you opened in this session, and its URL goes in the file.
5. **Never create portraits, photos, images, cartoons, or voice files of real people.**
6. **Never build a seat for Aman Gupta**, or for anyone the personality-rights check (Task C0) flags.
7. **Never edit these files unless a task tells you to:** `.claude/skills/baithak/scripts/*`, `.claude/skills/newseat/scripts/*`, `.claude/skills/baithak/SKILL.md`, `.claude/skills/newseat/SKILL.md`, `.claude/skills/baithak/references/scoring.md`, `LICENSE`.
8. **Do not change or remove any `model: sonnet`.** It appears in `.claude/skills/newseat/references/extract-prompt.md`, `writer-prompt.md`, `agent-template.md`, and `/newseat` Steps 4 and 5. Extraction, brain writing, and every council seat must run on Sonnet, whatever model the main session uses.
9. **If a check fails twice in a row** after you tried to fix it, stop. Report the exact command, its output, and what you tried.
10. **Use `python`, not `python3`** (this is Windows). Use the Bash tool for the commands below; they are POSIX shell.
11. After finishing each task, tick its box in Part 4 (change `[ ]` to `[x]`) and commit as the task says.
12. **Writing style for anything you write:** plain English, short sentences, no em dashes, no hype.

## Part 2: The health check (run at the start of every session and after every task)

```bash
cd /c/Users/Furqan/Desktop/IndianRoastRoom/baithak
git rev-parse --show-toplevel
python .claude/skills/baithak/scripts/check_quotes.py --selftest
python .claude/skills/baithak/scripts/check_laws.py --selftest
python .claude/skills/baithak/scripts/check_laws.py --lint
node .claude/skills/newseat/scripts/check_quotes.mjs --selftest
node -e "JSON.parse(require('fs').readFileSync('.claude/skills/baithak/roster.json','utf8')); console.log('roster ok')"
```

Expected output, in order:
1. a path ending in `IndianRoastRoom/baithak`
2. `selftest ok`
3. `selftest ok`
4. `lint ok`
5. `selftest ok`
6. `roster ok`

Anything else means stop and fix it before continuing (rule 9 applies).

## Part 3: What is already done (do not redo)

- The upstream Roast Room was cloned into this folder (remote `upstream`), and the branch is `main`.
- The US seats, the web room app, the portraits and the example sessions were removed. One upstream seat (Paul Graham) is kept only as a format example at `.claude/skills/newseat/references/example/`.
- Skills renamed: `/baithak` (run a council) and `/newseat` (build a seat).
- The quote checkers handle Hindi (the old ones skipped it silently). Both have `--selftest`.
- India layer written: `references/india-filters.md`, `evidence-ladder.md`, `legal-gate.md`, the India sections in `report-template.md`, the BLACK-zone veto in `scoring.md`, India checks in `SKILL.md` and `round-prompts.md`.
- `laws/` has two verified files (Online Gaming Act 2025; DPDP Act and Rules) plus `check_laws.py`.
- `/newseat` was updated: a personality-rights check first, no portraits, Hindi quote rules.
- README, CLAUDE.md, LICENSE (both copyright lines), and the opt-out issue template are done.
- `roster.json` is empty. No seats exist yet.

---

## Part 4: Tasks

### Phase A: Setup

- [x] **A1. Install yt-dlp and prove fetching works** (done 2026-11-05: yt-dlp 2026.10.26 installed with `python -m pip install --user yt-dlp`; English smoke test fetched 10,104 words)
  - `fetch.mjs` uses the `yt-dlp` command if it is on PATH, otherwise `python -m yt_dlp`, otherwise YouTube's own captions. It takes English captions first and Hindi when a video has no English track.
  - **Re-check at the start of Phase C** with this command:
    ```bash
    rm -rf build/_smoke && node .claude/skills/newseat/scripts/fetch.mjs build/_smoke "https://www.youtube.com/watch?v=RdAKXJlMIZM"
    ```
    It must print a line starting `ok     S001` with more than 5,000 words. Then run `rm -rf build/_smoke`.
  - **Hindi check, once, at the start of Phase C:**
    1. Use WebSearch to find one long Hindi-language YouTube interview of a founder.
    2. Run the same command on it, into `build/_smoke_hi`.
    3. Pass: a line starting `ok` and Devanagari or Hinglish text in the corpus file.
    4. If it fails with "no English or Hindi captions", try one more video. If it fails again, stop and report.

- [x] **A2. Baseline check** (done. Commits were undone at the user's request; all work is uncommitted. The user commits and pushes manually.)
  1. Run `git status --short`. If it shows changes, run the health check. If it passes, commit:
     ```bash
     git add .claude CLAUDE.md README.md LICENSE WORKPLAN.md .github .gitignore sessions/.gitkeep
     git commit -m "Baithak: fork Roast Room for the Indian market"
     ```
     If it shows nothing, the baseline is already committed. Move on.

### Phase B: Laws (one file per law)

**For every task in Phase B, do these steps:**
1. Run each search query listed in the task (WebSearch, `mode: standard`). If results are thin or older than 2025, rerun the most important query with `mode: extended`.
2. Open (fetch) at least two of the best sources. Prefer, in this order:
   1. the official site (rbi.org.in, sebi.gov.in, meity.gov.in, indiacode.nic.in, egazette.gov.in, pib.gov.in, uidai.gov.in, gst.gov.in, consumeraffairs.nic.in);
   2. law firm or legal news write-ups (LiveLaw, Bar & Bench, SCC Online, Mondaq, AZB, Cyril Amarchand, Khaitan, Trilegal);
   3. national news.
3. Look for the **latest** version. Indian regulators often replace old circulars with "Master Directions" or new "Directions". If you find a newer instrument that replaces the one named in the task, write about the newer one and say what it replaced.
4. Copy the template from `.claude/skills/baithak/laws/README.md` into the file name given. Fill every field. `last_verified` is today's date. List every URL you used under `sources`.
5. Write only what the sources say. If two sources disagree, write both and add "sources differ" in "Watch for".
6. Run `python .claude/skills/baithak/scripts/check_laws.py --lint`. It must print `lint ok`.
7. Commit: `git add .claude/skills/baithak/laws/<file> WORKPLAN.md && git commit -m "laws: <file name without .md>"`.

The `zone_trigger` given in each task is the expected value. If the sources clearly say otherwise, use what the sources say and mention it in your end-of-phase report.

- [x] **B1. `payment-aggregators.md`** (zone_trigger: BLACK)
  - Topic: RBI rules for payment aggregators and gateways, and marketplaces holding customers' money. Payment and Settlement Systems Act 2007.
  - Queries:
    - `RBI master direction payment aggregators 2025`
    - `RBI payment aggregator guidelines marketplace escrow nodal account`
    - `Payment and Settlement Systems Act 2007 unauthorised payment system startup`
  - "What it means" must cover: a startup collecting buyer money into its own current account and paying sellers later; the compliant route (a licensed payment aggregator's split-settlement or marketplace product).

- [x] **B2. `digital-lending.md`** (zone_trigger: BLACK)
  - Topic: RBI digital lending rules, lending service providers (LSPs), the default loss guarantee (DLG) cap, and BNPL.
  - Queries:
    - `RBI Digital Lending Directions 2025`
    - `RBI default loss guarantee 5 percent cap digital lending`
    - `RBI lending service provider rules fund flow borrower account`
  - Must cover: lending from your own balance sheet without an NBFC licence; loan money passing through third-party accounts; the LSP-with-NBFC route.

- [x] **B2b. `deposits-and-pooled-investment.md`** (zone_trigger: BLACK)
  - Topic: taking money from the public and pooling it. This covers:
    - the Banning of Unregulated Deposit Schemes Act, 2019;
    - SEBI Collective Investment Scheme rules (pooled money invested for returns);
    - RBI's NBFC peer-to-peer lending directions.
  - Queries:
    - `Banning of Unregulated Deposit Schemes Act 2019 startup collecting money returns`
    - `SEBI collective investment scheme definition pooled funds returns`
    - `RBI NBFC P2P lending platform master directions 2024 2025`
  - Must cover:
    - an app that pools users' money (deposits, savings, rent deposits, student investment pools) and promises a return;
    - a platform lending one user's money to another;
    - the compliant routes (licensed partners: a bank, an NBFC-P2P, a SEBI-registered fund or broker).

- [x] **B3. `sebi-advice-and-finfluencers.md`** (zone_trigger: BLACK)
  - Topic: SEBI Investment Adviser and Research Analyst regulations; SEBI's rules on finfluencers and unregistered entities; retail algo trading.
  - Queries:
    - `SEBI investment adviser regulations 2013 amendment 2024 2025`
    - `SEBI research analyst regulations amendment 2024`
    - `SEBI finfluencer circular regulated entities association unregistered`
    - `SEBI retail algo trading framework 2025`
  - Must cover: apps or AI that give personalised buy or sell calls without registration; the routes (register, partner with a registered entity, or show only data with no recommendations).

- [x] **B4. `crypto-vda.md`** (zone_trigger: GRAY)
  - Topic: virtual digital assets: FIU-IND registration under PMLA, Income Tax section 194S 1% TDS, the 30% tax, and the current policy status.
  - Queries:
    - `FIU-IND registration virtual digital asset service providers PMLA`
    - `section 194S TDS crypto 1 percent`
    - `India crypto regulation 2026 discussion paper status`
  - Note: operating without FIU registration is BLACK; crypto as a category is GRAY. Say both.

- [x] **B5. `aadhaar-and-ekyc.md`** (zone_trigger: BLACK)
  - Topic: Aadhaar Act 2016 limits on collecting, storing and using Aadhaar numbers; eKYC access (KUA/AUA); alternatives (DigiLocker, offline Aadhaar XML, masked Aadhaar).
  - Queries:
    - `Aadhaar Act 2016 private entity store Aadhaar number`
    - `UIDAI AUA KUA private companies eKYC 2025`
    - `DigiLocker offline Aadhaar verification startups`

- [x] **B6. `telemedicine-and-e-pharmacy.md`** (zone_trigger: BLACK)
  - Topic: Telemedicine Practice Guidelines 2020; who may prescribe; AI in diagnosis; online sale of medicines (the status of e-pharmacy rules); the Drugs and Magic Remedies Act.
  - Queries:
    - `Telemedicine Practice Guidelines 2020 India AI prescription registered medical practitioner`
    - `India e-pharmacy rules status 2025 2026`
    - `Drugs and Magic Remedies Objectionable Advertisements Act online claims`

- [x] **B7. `it-act-and-intermediary-rules.md`** (zone_trigger: GRAY)
  - Topic: IT Act section 79 safe harbour; IT Rules 2021 duties for intermediaries; any 2025 or 2026 rules on AI-generated or synthetic content and labelling.
  - Queries:
    - `IT Rules 2021 intermediary due diligence safe harbour section 79`
    - `MeitY synthetically generated information labelling rules 2025`
    - `IT Rules amendment AI deepfake 2026`

- [x] **B8. `upi-autopay-and-e-mandates.md`** (zone_trigger: WHITE)
  - Topic: RBI e-mandate rules for recurring payments: limits without extra authentication, pre-debit notification, users' ability to pause or revoke; UPI AutoPay.
  - Queries:
    - `RBI e-mandate recurring payments limit without additional factor authentication`
    - `UPI AutoPay limit pre-debit notification NPCI`
    - `UPI AutoPay mandate pause revoke user`

- [x] **B9. `consumer-protection-e-commerce.md`** (zone_trigger: GRAY)
  - Topic: Consumer Protection (E-Commerce) Rules 2020; CCPA dark patterns guidelines 2023; fake reviews.
  - Queries:
    - `Consumer Protection E-Commerce Rules 2020 marketplace seller obligations`
    - `CCPA guidelines prevention regulation dark patterns 2023`
    - `CCPA dark patterns self audit e-commerce 2025`

- [x] **B10. `gst-basics-for-startups.md`** (zone_trigger: WHITE)
  - Topic: GST registration thresholds; GST on SaaS and services; export of services under LUT; e-invoicing thresholds.
  - Queries:
    - `GST registration threshold services 2025`
    - `GST rate on software SaaS services India`
    - `export of services LUT GST zero rated`
    - `e-invoicing threshold turnover 2025`
  - Note: GST rates changed in September 2025 ("GST 2.0"). Use only post-September-2025 sources for rates.

- [x] **B11. End-of-phase report.** Tell the user, in under 120 words:
  - which files were written;
  - any `zone_trigger` that differed from this plan, and why;
  - any law where sources differed.

  Then continue to Phase C.

### Phase C: Seats

**Build order:** Nithin, then **STOP** for the user's review, then Kunal, Girish, Vembu, Deepinder.

**For every seat task, do these steps:**
1. **C0, the personality-rights check.** Run the three queries from Step 0 of `.claude/skills/newseat/SKILL.md`.
   - If any court order protecting this person's name, image, voice or persona shows up, **stop this seat**. Report the link to the user and move to the next seat.
   - If nothing shows up, write `build/<slug>/rights-check.md` as that step says.
2. Run `/newseat <Full Name>` at the default (standard) depth. Use exactly the key, slug, pillar, question and dimension from the seat's row in `.claude/skills/baithak/references/seats.md` ("Planned v1 seats"). Do not ask the user about pillar or depth. Answer "yes, default board" for the default-board question (pass `--default` to `add_seat.mjs`).
3. Follow every step of `/newseat` in order. Its quote check commands must end with `wrong source id: 0; not found: 0`.
4. Use the source hints in the seat's task as a starting point for Step 2 of `/newseat`. They are search hints, not URLs. Find the real URLs with WebSearch. Never invent a URL.
5. Seat acceptance check (all must pass):
   ```bash
   ls .claude/agents/council-<key>.md
   ls .claude/skills/baithak/brains/<slug>/
   node .claude/skills/newseat/scripts/check_quotes.mjs build/<slug> .claude/skills/baithak/brains/<slug>
   node -e "const r=JSON.parse(require('fs').readFileSync('.claude/skills/baithak/roster.json','utf8')); if(!r.seats.find(s=>s.key==='<key>')) throw 'not in roster'; console.log('in roster')"
   grep -c "not affiliated with or endorsed by" .claude/agents/council-<key>.md
   ```
   Expected results:
   - the agent file exists;
   - the brain lists 8 files: `_hot.md books.md frameworks.md positions.md principles.md sources.md stories.md voice.md`;
   - the quote check shows `wrong source id: 0; not found: 0`;
   - the roster check prints `in roster`;
   - the grep prints `1` or more.
6. Also add the seat's tension lines to `seats.md` if `/newseat` Step 7 did not (check "Natural tensions"; the v1 tensions are already written, so usually nothing to add).
7. Commit:
   ```bash
   git add .claude/agents/council-<key>.md .claude/skills/baithak/brains/<slug> .claude/skills/baithak/roster.json .claude/skills/baithak/references/seats.md WORKPLAN.md
   git commit -m "seat: <Full Name>"
   ```
   Never `git add build/`. It is gitignored on purpose.

- [x] **C1. Nithin Kamath** (built 2026-11-10 at seed depth: 12 sources fetched, 9 usable, 93k words; branch `feat/seat-nithin`) (`nithin`, `nithin-kamath`)
  - Source hints:
    - Zerodha's blog and Z-Connect posts written by Nithin;
    - his long posts on X (`@Nithin0dha`);
    - long podcasts where he is the main guest (WTF with Nikhil Kamath episodes featuring Nithin, The Ranveer Show, Figuring Out with Raj Shamani, The Barbershop with Shantanu);
    - Zerodha's annual or bootstrapping write-ups;
    - long interviews in Mint, ET, YourStory, Inc42.

- [ ] **C1-STOP. Review gate. Do not continue without the user.**
  1. Run a consult and save the answer to `build/nithin-kamath/review-consult.md`:
     `/baithak ask nithin I want to build a UPI-based app where college students pool money to invest in stocks together, with an AI that suggests which stocks to buy. Price is free, we earn from brokerage referrals.`
  2. Run `/baithak --quick --seats nithin` on the same idea. If the council needs four seats and only one exists, run it with one seat and say so.
  3. Tell the user:
     - the seat is built, with its source count and word count;
     - where the consult and the council session are saved;
     - "Please read them and tell me: continue to the other four seats, or fix something first?"
  4. **Wait.** Continue only when the user says to continue.

- [x] **C2. Kunal Shah** (built 2026-11-10, seed depth, 10 sources; branch `feat/seat-kunal`) (`kunal`, `kunal-shah`)
  - Source hints:
    - his long X threads (`@kunalb11`) on Delta 4, India 1/2/3, trust, and consumer behaviour;
    - long podcasts where he is the main guest (Kunal Shah on The Knowledge Project, The Seen and the Unseen, WTF with Nikhil Kamath, Figuring Out, Think School);
    - his talks on Delta 4 and on building CRED and FreeCharge.

- [x] **C3. Girish Mathrubootham** (built 2026-11-10 with seatkit.py, Haiku extraction, seed depth, 11 sources; branch `feat/seat-girish`) (`girish`, `girish-mathrubootham`)
  - Source hints:
    - SaaSBOOMi talks and keynotes;
    - long interviews about building Freshworks from Chennai and its Nasdaq listing;
    - podcasts (20VC, SaaStr, Indian startup podcasts);
    - his posts on X (`@mrgirish`);
    - Together Fund interviews.

- [x] **C4. Sridhar Vembu** (built 2026-11-10 with seatkit, all agents on Haiku, seed depth, 11 sources; branch `feat/seat-vembu`) (`vembu`, `sridhar-vembu`)
  - Source hints:
    - his long posts on X (`@svembu`) on rural development, frugality, R&D, and not raising VC;
    - long interviews about Zoho, Tenkasi, and rural offices;
    - podcasts and keynotes.
  - Note: some of his posts are about politics or religion. Extract only business, technology, hiring, R&D, rural development and economics views. Skip political and religious opinions entirely; they do not belong in a business seat.

- [ ] **C5. Deepinder Goyal** (`deepinder`, `deepinder-goyal`)
  - Source hints:
    - Zomato and Eternal shareholder letters (he writes these himself; they are text-rich);
    - his long posts on X (`@deepigoyal`);
    - long podcasts where he is the main guest (Figuring Out with Raj Shamani, WTF with Nikhil Kamath, The Ranveer Show);
    - interviews about Blinkit and quick commerce.

- [ ] **C6. Default board check.**
  - Run `/baithak board` and confirm the default board lists all built seats and the setting is "ask".
  - Commit if `roster.json` changed: `git add .claude/skills/baithak/roster.json WORKPLAN.md && git commit -m "board: v1 default board"`.

### Phase D: Test councils

Run each idea as a **full council** (`/baithak <idea>`, then confirm the recommended board), with "just run it" so the Chair fills gaps with stated assumptions. After each one, run:

```bash
python .claude/skills/baithak/scripts/check_quotes.py sessions/<folder>
python .claude/skills/baithak/scripts/check_laws.py sessions/<folder>
```

Both must exit with no problems (unverified: 0; problems: 0). If not, fix the verdict as `SKILL.md` Step 8 says, then rerun.

- [ ] **D1. A WHITE idea (MSME SaaS):**
  "WhatsApp GST billing assistant for hardware and electrical shops in Tier-2 cities, ₹999 per month. Today their munim uses a notebook and Tally. I'd sell through local CAs who get 20% commission. I have ₹3 lakh and 6 months. Leaning yes because 5 CAs liked it."
  - Pass if: the legal zone is WHITE or UNMAPPED (not BLACK); all 5 filters are graded; a 7-day jugaad test under ₹5,000 is present.

- [ ] **D2. A BLACK idea (veto test):**
  "A fantasy cricket app where users pay ₹49 to enter contests and win cash prizes, aimed at Tier-2 college students. I have ₹10 lakh. Leaning yes because Dream11 proved the market."
  - Pass if: Option A is classified BLACK citing `[laws/online-gaming-act-2025.md]`, and the verdict does **not** recommend Option A. This proves the BLACK-zone veto works. If Option A is recommended, the test FAILED: stop and report.

- [ ] **D3. A GRAY idea (fintech):**
  "An app that lets tenants in Bengaluru pool their rental security deposits into a fund that earns 10% a year, and we lend the pool to landlords for renovations. Leaning yes."
  - Pass if all three hold:
    - Option A is classified BLACK, citing `[laws/deposits-and-pooled-investment.md]` or `[laws/digital-lending.md]` (or both);
    - the "Check before you build" line says "Verify with a lawyer before you build.";
    - Option B moves to licensed partners (bank, NBFC-P2P, or similar) instead of pooling money itself.

    If Option A is recommended, the test FAILED: stop and report.

- [ ] **D4. Plain-Claude comparison.**
  1. Start a new chat with **no skill**, on **the same model the D1 council used** (Sonnet), so the comparison is fair. Paste D1's idea with "Is this a good idea for India? Be blunt."
  2. Save that answer to `build/plain-claude-d1.md`.
  3. Write `build/comparison.md`: five bullets on what Baithak caught that plain Claude missed, and anything plain Claude caught that Baithak missed.
  4. Show the user `build/comparison.md` and ask: "Is Baithak clearly better? If not, which part should we fix before launch?"

- [ ] **D5. Pick the demo session.**
  - Ask the user which of D1 to D3 to ship as the public example.
  - Rename that folder to `sessions/<date>-example-<slug>/`. The `.gitignore` already lets folders with `example` in the name ship.
  - Commit: `git add sessions/<that folder> WORKPLAN.md && git commit -m "example: <slug> council"`.

### Phase E: Publish (needs the user)

- [ ] **E1. GitHub login.** Ask the user to run `! gh auth login` in the prompt. Then run `gh auth status` and confirm it says logged in as `cipher-cmd`.
- [ ] **E2. Create the repo as PRIVATE first.**
  ```bash
  gh repo create cipher-cmd/baithak --private --source . --remote origin --push
  ```
  The `upstream` remote stays pointed at nateherkai/roast-room. Do not push to `upstream`, ever.
- [ ] **E3. Pre-public checklist.** Ask the user to confirm each item:
  1. All seats re-checked for personality-rights orders within the last 30 days (rerun C0 for each).
  2. The README disclaimer and opt-out link are present.
  3. An IP lawyer has looked at it, or the user has knowingly decided to skip that.
  4. No file in the repo contains raw transcripts: `git ls-files | grep -i corpus` must print nothing.
- [ ] **E4. Make it public** only when the user says "make it public": `gh repo edit cipher-cmd/baithak --visibility public --accept-visibility-change-consequences`.
- [ ] **E5. Launch post.** Draft a LinkedIn post and an X post in the user's voice: what Baithak is, the demo verdict, and the repo link. Show the drafts to the user. Do not post anything yourself.

---

## Part 5: When something goes wrong

| Symptom | Do this |
|---|---|
| `git rev-parse --show-toplevel` prints `C:/Users/Furqan` | You are in the wrong folder. `cd /c/Users/Furqan/Desktop/IndianRoastRoom/baithak` and retry. Never commit from the home repo. |
| `fetch.mjs` prints many `fail` or `thin` lines | Normal for some sites. Find another copy of the source (a transcript page, an archive.org copy) or a different source. Keep going until the depth target in `/newseat` is met. |
| A YouTube transcript is empty | Try a different video. Note it in `build/<slug>/notes.md`. |
| `check_quotes.mjs` reports `NOT FOUND` | Open the cited corpus file and search for the words. Copy them exactly, or change the line to paraphrase with no quotation marks. Never "fix" a quote to make it read better. |
| `check_laws.py` reports `STALE` | Redo that law's Phase B task (re-verify, update `last_verified`). |
| A `council-<key>` agent type is "not found" | Normal right after building a seat. The council uses the `general-purpose` fallback automatically. A new Claude Code session will load it as its own type. |
| A source is behind a paywall or login | Skip it. Use only public, lawful sources. |
| Anything not in this table | Stop and ask the user. |
