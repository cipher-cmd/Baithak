#!/usr/bin/env python
"""seatkit: the mechanical half of building a Baithak seat, in one place.

Claude (or you) still does the judgment steps: the personality-rights check,
picking sources from the candidate list, and running the extraction, writer
and consult agents. seatkit does everything around them and writes the agent
prompts as files, so any model (Haiku for extraction) can run them as-is.

Run from the repo root. Steps, in order:

  python .claude/skills/newseat/scripts/seatkit.py discover girish "Girish Mathrubootham interview" "Girish Freshworks podcast" --must girish
      yt-dlp search; writes build/<slug>/candidates.tsv (long videos only). Pick lines into build/<slug>/urls.txt.
  python .claude/skills/newseat/scripts/seatkit.py fetch girish
      runs fetch.mjs on urls.txt, then screens every source (garbled, spam, Devanagari, too short).
  python .claude/skills/newseat/scripts/seatkit.py plan girish
      batches usable sources (about 45k words each) and writes build/<slug>/prompts/*.md and RUNBOOK.md.
  python .claude/skills/newseat/scripts/seatkit.py check girish [notes|brain|<file>]
      quote check (wraps check_quotes.mjs).
  python .claude/skills/newseat/scripts/seatkit.py finish girish
      writes sources.md if missing, registers the seat, runs every acceptance check.
  python .claude/skills/newseat/scripts/seatkit.py cost girish [stage tokens]
      log or show sub-agent token use per stage.
  python .claude/skills/newseat/scripts/seatkit.py --selftest

<key> is the seat key from references/seats.md ("Planned v1 seats"); the name, slug, pillar,
question and dimension come from that table. Standard library only.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
NEWSEAT = os.path.join(ROOT, ".claude", "skills", "newseat")
BAITHAK = os.path.join(ROOT, ".claude", "skills", "baithak")
SEATS_MD = os.path.join(BAITHAK, "references", "seats.md")
BATCH_WORDS = 45000
BRAIN_FILES = ["_hot.md", "books.md", "frameworks.md", "positions.md", "principles.md", "sources.md", "stories.md", "voice.md"]
STOP = set("the and to of a is that you it in i we this for so what be have are not was they do but on "
           "with like if your can my me people think know".split())


def die(msg):
    sys.exit("seatkit: " + msg)


def run(cmd, check=True):
    print("$ " + " ".join(cmd), flush=True)
    r = subprocess.run(cmd, cwd=ROOT, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        die(f"command failed ({r.returncode})")
    return r.returncode


def seat(key):
    """Read one row of the 'Planned v1 seats' table in seats.md."""
    for line in open(SEATS_MD, encoding="utf-8"):
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0] == key:
            return dict(zip(["key", "name", "slug", "pillar", "question", "dimension"], cells))
    die(f"no row for key '{key}' in {os.path.relpath(SEATS_MD, ROOT)}")


def build_dir(s):
    d = os.path.join(ROOT, "build", s["slug"])
    os.makedirs(d, exist_ok=True)
    return d


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def load_sources(b):
    p = os.path.join(b, "sources.json")
    if not os.path.exists(p):
        die("no sources.json yet; run fetch first")
    return json.load(open(p, encoding="utf-8"))


def template(name):
    """The fenced prompt block from a newseat reference file."""
    text = open(os.path.join(NEWSEAT, "references", name), encoding="utf-8").read()
    m = re.search(r"```\n(.*?)```", text, re.S)
    return m.group(1)


def consult_template():
    text = open(os.path.join(BAITHAK, "references", "round-prompts.md"), encoding="utf-8").read()
    m = re.search(r"## Single-seat consult\s*```\n(.*?)```", text, re.S)
    return m.group(1)


# ---------- screening ----------

def screen(text, kind):
    """Return '' if a corpus file looks usable, else a short reason."""
    words = re.findall(r"[^\W\d_]+", text.lower())
    n = len(words)
    if n < 500:
        return f"too short ({n} words)"
    deva = sum(1 for w in words if re.search("[ऀ-ॿ]", w)) / n
    if deva > 0.5:
        return f"Devanagari script ({deva:.0%}); Hindi or English written phonetically. Keep only after reading it"
    if text.lower().count("subscribe") * 1000 / n > 5:
        return "caption spam ('subscribe' repeated)"
    stop = sum(1 for w in words if w in STOP) / n
    # ponytail: stopword ratio is a crude English-quality proxy; good captions sit near 0.40,
    # garbled ones near 0.30 or lower. Only applied to video, since written pieces run lower.
    if kind == "video" and stop < 0.33:
        return f"garbled captions (English stopword ratio {stop:.2f})"
    return ""


def screen_all(b, sources):
    excluded = {}
    for s in sources:
        why = screen(open(os.path.join(b, s["file"]), encoding="utf-8").read(), s.get("kind", ""))
        if why:
            excluded[s["id"]] = why
    with open(os.path.join(b, "excluded.json"), "w", encoding="utf-8") as f:
        json.dump(excluded, f, indent=2)
    return excluded


# ---------- commands ----------

def cmd_discover(s, args):
    must = []
    if "--must" in args:
        i = args.index("--must")
        must = [w.lower() for w in args[i + 1].split(",")]
        args = args[:i] + args[i + 2:]
    min_minutes = 25
    if "--min" in args:
        i = args.index("--min")
        min_minutes = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    if not args:
        die('discover needs at least one search query, like "Name interview"')
    must = must or [s["name"].split()[-1].lower()]
    seen, rows = set(), []
    for q in args:
        out = subprocess.run([sys.executable, "-m", "yt_dlp", f"ytsearch10:{q}", "--flat-playlist",
                              "--print", "%(duration)s\t%(id)s\t%(channel)s\t%(title)s"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) != 4 or parts[1] in seen:
                continue
            try:
                minutes = int(float(parts[0])) // 60
            except ValueError:
                continue
            hay = (parts[2] + " " + parts[3]).lower()
            if minutes < min_minutes or not any(m in hay for m in must):
                continue
            seen.add(parts[1])
            rows.append((minutes, parts[1], parts[2], parts[3]))
    b = build_dir(s)
    with open(os.path.join(b, "candidates.tsv"), "w", encoding="utf-8") as f:
        f.write("minutes\turl\tchannel\ttitle\n")
        for m, vid, ch, t in sorted(rows, key=lambda r: -r[0]):
            f.write(f"{m}\thttps://www.youtube.com/watch?v={vid}\t{ch}\t{t}\n")
    print(f"{len(rows)} candidates -> {rel(os.path.join(b, 'candidates.tsv'))}")
    print("Next: copy the URLs where the person is the main speaker into urls.txt "
          "(drop titles about a different person with the same surname, and clips with many guests).")


def cmd_fetch(s, args):
    b = build_dir(s)
    urls = os.path.join(b, "urls.txt")
    if not os.path.exists(urls):
        die(f"write {rel(urls)} first (one URL per line)")
    run(["node", os.path.join(NEWSEAT, "scripts", "fetch.mjs"), rel(b), "--list", rel(urls)], check=False)
    sources = load_sources(b)
    excluded = screen_all(b, sources)
    usable = [x for x in sources if x["id"] not in excluded]
    print(f"\nscreen: {len(usable)} usable, {len(excluded)} excluded, "
          f"{sum(x['words'] for x in usable):,} usable words")
    for sid, why in excluded.items():
        print(f"  excluded {sid}: {why}")
    print("Quick depth wants 12 to 20 sources and 80k+ words. Add URLs and rerun fetch if short.")


def cmd_plan(s, args):
    b = build_dir(s)
    sources = load_sources(b)
    excluded = json.load(open(os.path.join(b, "excluded.json"), encoding="utf-8")) \
        if os.path.exists(os.path.join(b, "excluded.json")) else screen_all(b, sources)
    usable = [x for x in sources if x["id"] not in excluded]
    if not usable:
        die("no usable sources")
    depth = "quick"
    if "--depth" in args:
        depth = args[args.index("--depth") + 1]
    # --note "..." adds a seat-specific rule to every extract and writer prompt
    note = "\nSeat-specific rule: " + args[args.index("--note") + 1] + "\n" if "--note" in args else ""
    # balanced batching: as few agents as the word count needs, largest source into the lightest batch
    n = -(-sum(x["words"] for x in usable) // BATCH_WORDS)
    batches = [[] for _ in range(n)]
    for src in sorted(usable, key=lambda x: -x["words"]):
        min(batches, key=lambda bt: sum(x["words"] for x in bt)).append(src)
    pdir = os.path.join(b, "prompts")
    os.makedirs(pdir, exist_ok=True)
    os.makedirs(os.path.join(b, "notes"), exist_ok=True)
    root = ROOT.replace(os.sep, "/")
    common = {"[Full Name]": s["name"], "[pillar]": s["pillar"], "[question]": s["question"],
              "[absolute path]": root, "[build]": rel(b)}
    ext = template("extract-prompt.md")
    for i, bt in enumerate(batches, 1):
        nn = f"{i:02d}"
        lines = "\n".join(f"{x['id']} | {rel(b)}/{x['file']} | {x['words']:,} words"
                          for x in sorted(bt, key=lambda x: x["id"]))
        p = ext.replace("[one line per source: S0xx | corpus/S0xx-....md | words]", lines).replace("[NN]", nn)
        for k, v in common.items():
            p = p.replace(k, v)
        p += (f"\nBefore you finish, run `node .claude/skills/newseat/scripts/check_quotes.mjs {rel(b)} "
              f"{rel(b)}/notes/batch-{nn}.md` and fix every problem it reports. YouTube sources are auto-captions "
              f"with no speaker labels: use context to tell which lines are {s['name']}'s. Add the checker's final "
              f"line to your one-line reply.\n") + note
        open(os.path.join(pdir, f"extract-{nn}.md"), "w", encoding="utf-8").write(p)
    brain = f".claude/skills/baithak/brains/{s['slug']}"
    os.makedirs(os.path.join(ROOT, brain), exist_ok=True)  # fetch.mjs --sources-md needs it
    wr = template("writer-prompt.md")
    for tag, files in [("A", "frameworks.md, principles.md, books.md"),
                       ("B", "positions.md, stories.md"), ("C", "voice.md")]:
        p = wr.replace("[quick | standard | deep]", depth).replace("[slug]", s["slug"]).replace("[files]", files)
        for k, v in common.items():
            p = p.replace(k, v)
        p += ("\nFor format, also skim the matching files of a finished seat: .claude/skills/baithak/brains/nithin-kamath/. "
              "Sources are mostly auto-captions: prefer quotes that read cleanly. Where the notes have nothing on a topic, "
              "write \"no recorded position\"; never guess.\n")
        if excluded:
            p += "Excluded sources (do not cite): " + ", ".join(sorted(excluded)) + ".\n"
        p += note
        open(os.path.join(pdir, f"write-{tag}.md"), "w", encoding="utf-8").write(p)
    c = consult_template().replace("[absolute path]", root).replace("[SEAT]", s["key"].capitalize())
    c = c.replace("[question, plus any context]",
                  "I want to build a WhatsApp GST billing assistant for hardware and electrical shops in Tier-2 cities "
                  "at Rs 999 per month. Today their munim uses a notebook and Tally. I'd sell through local CAs who get "
                  "20% commission. I have Rs 3 lakh and 6 months. Leaning yes because 5 CAs liked it.")
    c = (f"Read .claude/agents/council-{s['key']}.md and follow it as your instructions for this whole task. "
         f"Only read files; do not write anything.\n\n" + c)
    open(os.path.join(pdir, "consult.md"), "w", encoding="utf-8").write(c)
    runbook = f"""# Runbook: {s['name']} ({s['key']})

Usable sources: {len(usable)} ({sum(x['words'] for x in usable):,} words). Excluded: {', '.join(sorted(excluded)) or 'none'}.

1. Extraction ({len(batches)} agents, one message, in parallel; Haiku is fine, the quote checker is the safety net):
   spawn `general-purpose` with each prompt file's full text: {', '.join(f'prompts/extract-{i:02d}.md' for i in range(1, len(batches) + 1))}
   Log each agent's tokens: `python .claude/skills/newseat/scripts/seatkit.py cost {s['key']} extract-NN <tokens>`
2. `python .claude/skills/newseat/scripts/seatkit.py check {s['key']} notes` must end `not found: 0`.
3. `node .claude/skills/newseat/scripts/fetch.mjs {rel(b)} --sources-md {brain}/sources.md --name "{s['name']}"`
4. Writers (3 agents, Sonnet): prompts/write-A.md, write-B.md, write-C.md.
5. Write `{brain}/_hot.md` and `.claude/agents/council-{s['key']}.md` yourself (spec: newseat SKILL.md steps 5 and 6).
6. Consult test (Sonnet): prompts/consult.md. Save the answer to {rel(b)}/review-consult.md, then `check {s['key']} {rel(b)}/review-consult.md`.
7. `python .claude/skills/newseat/scripts/seatkit.py finish {s['key']}` must print `ALL CHECKS PASS`.
"""
    open(os.path.join(b, "RUNBOOK.md"), "w", encoding="utf-8").write(runbook)
    for i, bt in enumerate(batches, 1):
        print(f"batch {i:02d}: {', '.join(x['id'] for x in sorted(bt, key=lambda x: x['id']))} "
              f"({sum(x['words'] for x in bt):,} words)")
    print(f"prompts -> {rel(pdir)}/   runbook -> {rel(os.path.join(b, 'RUNBOOK.md'))}")


def cmd_check(s, args):
    b = build_dir(s)
    what = args[0] if args else "brain"
    target = {"notes": rel(os.path.join(b, "notes")),
              "brain": f".claude/skills/baithak/brains/{s['slug']}"}.get(what, what)
    return run(["node", os.path.join(NEWSEAT, "scripts", "check_quotes.mjs"), rel(b), target], check=False)


def cmd_finish(s, args):
    b = build_dir(s)
    brain = os.path.join(BAITHAK, "brains", s["slug"])
    agent = os.path.join(ROOT, ".claude", "agents", f"council-{s['key']}.md")
    problems = []
    if not os.path.exists(os.path.join(b, "rights-check.md")):
        problems.append("no rights-check.md (personality-rights check not recorded)")
    if not os.path.exists(os.path.join(brain, "sources.md")):
        run(["node", os.path.join(NEWSEAT, "scripts", "fetch.mjs"), rel(b), "--sources-md",
             rel(os.path.join(brain, "sources.md")), "--name", s["name"]])
    missing = [f for f in BRAIN_FILES if not os.path.exists(os.path.join(brain, f))]
    if missing:
        problems.append("brain missing " + ", ".join(missing))
    if not os.path.exists(agent):
        problems.append(f"missing {rel(agent)}")
    elif "not affiliated with or endorsed by" not in open(agent, encoding="utf-8").read():
        problems.append("agent file lacks the simulation disclaimer")
    for p in [agent] + [os.path.join(brain, f) for f in BRAIN_FILES]:
        if os.path.exists(p) and re.search("[–—]", open(p, encoding="utf-8").read()):
            problems.append(f"em or en dash in {rel(p)}")
    if cmd_check(s, ["brain"]):
        problems.append("brain quote check failed")
    if not problems:
        excluded = json.load(open(os.path.join(b, "excluded.json"), encoding="utf-8")) \
            if os.path.exists(os.path.join(b, "excluded.json")) else {}
        usable = len(load_sources(b)) - len(excluded)
        depth = "seed" if usable < 30 else ("standard" if usable < 80 else "deep")
        run(["node", os.path.join(NEWSEAT, "scripts", "add_seat.mjs"), "--key", s["key"], "--name", s["name"],
             "--short", s["key"].capitalize(), "--slug", s["slug"], "--pillar", s["pillar"],
             "--question", s["question"], "--dimension", s["dimension"], "--default",
             "--depth", depth, "--sources", str(usable)])
    print("\n" + ("ALL CHECKS PASS" if not problems else "PROBLEMS:\n  " + "\n  ".join(problems)))
    return 1 if problems else 0


def cmd_cost(s, args):
    p = os.path.join(build_dir(s), "cost.tsv")
    if len(args) == 2:
        with open(p, "a", encoding="utf-8") as f:
            f.write(f"{args[0]}\t{int(args[1].replace(',', ''))}\n")
    rows = [l.split("\t") for l in open(p, encoding="utf-8").read().splitlines()] if os.path.exists(p) else []
    total = 0
    for stage, n in rows:
        total += int(n)
        print(f"{stage:<14}{int(n):>12,}")
    print(f"{'total':<14}{total:>12,}  (sub-agents only; the main session is not counted)")


def selftest():
    good = ("so the thing is you know we did not raise money because it is the right thing for the customer "
            "and that is what I think people should do ") * 40
    assert screen(good, "video") == ""
    assert "spam" in screen(good + " subscribe" * 200, "video")
    assert "Devanagari" in screen("नमस्ते दुनिया यह एक परीक्षण है " * 200, "video")
    assert "garbled" in screen(("zerodha rupees brokerage market trading platform " * 120) + good[:300], "video")
    assert "too short" in screen("hello world", "web")
    assert seat("nithin")["slug"] == "nithin-kamath"
    print("selftest ok")


COMMANDS = {"discover": cmd_discover, "fetch": cmd_fetch, "plan": cmd_plan,
            "check": cmd_check, "finish": cmd_finish, "cost": cmd_cost}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console is cp1252; seat text has ₹
    a = sys.argv[1:]
    if a[:1] == ["--selftest"]:
        selftest()
    elif len(a) < 2 or a[0] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    else:
        os.chdir(ROOT)
        sys.exit(COMMANDS[a[0]](seat(a[1]), a[2:]) or 0)
