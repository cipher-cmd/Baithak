#!/usr/bin/env python
"""
Check every quoted line in a council session against the seats' brains.

Usage:
  python .claude/skills/baithak/scripts/check_quotes.py <session folder>

Scans round-*.md and verdict.md for quotes attributed to a source id, like "..." (S095).
The speaker is the seat named in the nearest "## <Seat>" heading (from roster.json); quotes
under other headings are checked against every brain. Each quote gets a status:
  PASS        in the speaker's brain, on a line that carries the cited id
  INTERNAL    not in the brain, but quotes an earlier round or the brief (fine)
  WRONG ID    real quote, but the brain gives it a different source id
  WRONG SEAT  real quote of a different seat
  UNVERIFIED  in no brain: invented, remove it from the verdict
Writes <session>/quote-audit.md with the source title, date, link and brain line for each
quote, so a person can check context by opening the source. Exit code 1 on any flag.
Self-test: check_quotes.py --selftest
"""
import re
import sys
import unicodedata
from pathlib import Path

BRAINS = Path(__file__).resolve().parents[1] / "brains"


# Letters, digits and Indic script blocks (Devanagari through Malayalam, incl. vowel signs) survive.
# The old ASCII-only class turned Hindi quotes into empty strings, so they passed unchecked.
KEEP = r"[^\wऀ-ൿ' ]+"


def norm(s):
    s = unicodedata.normalize("NFC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(KEEP, " ", s).replace("_", " ")
    return re.sub(r"\s+", " ", s).strip()


def selftest():
    brain = norm("नितिन ने कहा: हम कभी ग्राहकों को स्पैम नहीं करते, यही हमारा भरोसा है।")
    real = norm("हम कभी ग्राहकों को स्पैम नहीं करते, यही हमारा भरोसा है")
    fake = norm("हम हमेशा ग्राहकों को कॉल करके बेचते हैं और पैसा कमाते हैं")
    assert len(real.split()) >= 6 and real in brain, "real Hindi quote must verify"
    assert len(fake.split()) >= 6 and fake not in brain, "fake Hindi quote must fail"
    assert norm("We never  SPAM—our users!") == "we never spam our users"
    print("selftest ok")


ID = re.compile(r"S\d{3}")
QUOTE = re.compile(r"[\"“]([^\"“”\n]{20,400})[\"”][^\n\"]{0,40}?[\(\[](S\d{3})")


def load_brains(root=BRAINS):
    """slug -> {"lines": [(file, lineno, norm text, ids)], "blob": norm text, "sources": {id: (title, url, date)}}"""
    brains = {}
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        lines, sources = [], {}
        for f in sorted(d.glob("*.md")):
            for i, raw in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                lines.append((f.name, i, norm(raw), set(ID.findall(raw))))
                if f.name == "sources.md" and raw.startswith("- S"):
                    parts = [x.strip() for x in raw[2:].split("|")]
                    if len(parts) >= 4:
                        sources[parts[0]] = (parts[1], parts[2], parts[3])
        brains[d.name] = {"lines": lines, "blob": " ".join(l[2] for l in lines), "sources": sources}
    return brains


def seat_slugs():
    """lowercased heading name (short or full) -> brain slug, from roster.json."""
    import json
    roster = json.loads((BRAINS.parent / "roster.json").read_text(encoding="utf-8"))
    out = {}
    for s in roster["seats"]:
        for k in (s["short"], s["name"], s["key"]):
            out[k.lower()] = s["slug"]
    return out


def classify(nq, cited, speaker, brains):
    """Return (status, slug, file, line). Speaker None means unknown (verdict, chair notes)."""
    seats = [speaker] if speaker in brains else list(brains)
    for slug in seats:
        hits = [l for l in brains[slug]["lines"] if nq in l[2]]
        with_id = [l for l in hits if cited in l[3]]
        if with_id:
            return "PASS", slug, with_id[0][0], with_id[0][1]
        if hits:
            return "WRONG ID", slug, hits[0][0], hits[0][1]
        if nq in brains[slug]["blob"]:  # quote spans two brain lines
            return "PASS", slug, None, None
    others = [s for s in brains if s not in seats and nq in brains[s]["blob"]]
    if others:
        return "WRONG SEAT", others[0], None, None
    return "UNVERIFIED", None, None, None


def selftest_audit(tmp):
    d = tmp / "brains" / "a-seat"
    d.mkdir(parents=True)
    (d / "sources.md").write_text("- S001 | Talk one | https://x.test/1 | 2024-01-02 | 10\n", encoding="utf-8")
    (d / "positions.md").write_text('- "we never raise money we do not need at all" (S001, 2024-01-02)\n', encoding="utf-8")
    e = tmp / "brains" / "b-seat"
    e.mkdir()
    (e / "positions.md").write_text('- "build depth in the village not the metro bubble" (S001, 2023)\n', encoding="utf-8")
    b = load_brains(tmp / "brains")
    q = norm("we never raise money we do not need")
    assert classify(q, "S001", "a-seat", b) == ("PASS", "a-seat", "positions.md", 1)
    assert classify(q, "S002", "a-seat", b)[0] == "WRONG ID"
    assert classify(norm("build depth in the village not the metro"), "S001", "a-seat", b)[0] == "WRONG SEAT"
    assert classify(norm("we always cold call every single customer"), "S001", None, b)[0] == "UNVERIFIED"
    assert classify(q, "S001", None, b)[0] == "PASS"


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on Hindi or ₹
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        import tempfile
        selftest()
        with tempfile.TemporaryDirectory() as t:
            selftest_audit(Path(t))
        return print("audit selftest ok")
    session = Path(sys.argv[1])
    brains = load_brains()
    slugs = seat_slugs()
    session_files = sorted(session.glob("round-*.md")) + [p for p in [session / "verdict.md"] if p.exists()]
    brief = norm((session / "brief.md").read_text(encoding="utf-8")) if (session / "brief.md").exists() else ""
    rows, counts = [], {}
    seen_session = ""
    for f in session_files:
        speaker = None
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("## "):
                speaker = slugs.get(line[3:].strip().lower())
            # only quotes attributed to a source id, e.g. "..." (S095) or "..." [S048, 2026]
            for q, cited in QUOTE.findall(line):
                nq = norm(q)
                if len(nq.split()) < 6:
                    continue
                status, slug, bfile, bline = classify(nq, cited, speaker, brains)
                if status != "PASS" and (nq in seen_session or nq in brief):
                    status = "INTERNAL"  # quoting an earlier round or the founder
                counts[status] = counts.get(status, 0) + 1
                rows.append((f.name, speaker, q, cited, status, slug, bfile, bline))
            seen_session += " " + norm(line)
    write_audit(session, rows, brains)
    print("; ".join(f"{k}: {v}" for k, v in sorted(counts.items())) or "no attributed quotes")
    bad = [r for r in rows if r[4] not in ("PASS", "INTERNAL")]
    for name, speaker, q, cited, status, slug, *_ in bad:
        print(f"  {status} [{name}, {speaker or 'unknown seat'}, {cited}] \"{q[:160]}\"")
    print(f"audit written to {session / 'quote-audit.md'}")
    sys.exit(1 if bad else 0)


def write_audit(session, rows, brains):
    out = ["# Quote audit", "",
           "Each quote attributed to a source id, checked against the speaking seat's brain.",
           "PASS: found in that seat's brain on a line with the cited id. INTERNAL: quotes an earlier round or the brief.",
           "WRONG ID: real quote, wrong source id. WRONG SEAT: the quote belongs to another seat. UNVERIFIED: found nowhere.",
           "A PASS shows the words are real. Open the source link to check they are used in context.", ""]
    n = {}
    for name, speaker, q, cited, status, slug, bfile, bline in rows:
        who = speaker or "unknown seat"
        n[who] = n.get(who, 0) + 1
        out.append(f"### {who}, quote {n[who]} ({name})")
        out.append(f'> "{q}"')
        out.append(f"- **Status:** {status}")
        src = brains.get(slug, {}).get("sources", {}).get(cited) if status in ("PASS", "WRONG ID") else None
        if src:
            out.append(f"- **Source:** {cited}, {src[0]} ({src[2]}) {src[1]}")
        else:
            out.append(f"- **Cited id:** {cited}")
        if bfile:
            path = f".claude/skills/baithak/brains/{slug}/{bfile}"
            out.append(f"- **Brain line:** [`{path}#L{bline}`](../../{path}#L{bline})")
        elif slug:
            out.append(f"- **Found in brain:** {slug}")
        out.append("")
    (session / "quote-audit.md").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
