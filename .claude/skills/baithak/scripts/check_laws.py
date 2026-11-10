#!/usr/bin/env python
"""
Check law citations in a Baithak session, or lint the laws/ folder.

Usage:
  python .claude/skills/baithak/scripts/check_laws.py <session folder>   check citations
  python .claude/skills/baithak/scripts/check_laws.py --lint             check every laws/*.md file
  python .claude/skills/baithak/scripts/check_laws.py --selftest

A citation looks like [laws/online-gaming-act-2025.md]. Each must point to an existing file in
laws/ whose last_verified date is within MAX_AGE_DAYS. Exit code 1 if anything fails.
"""
import re
import sys
from datetime import date
from pathlib import Path

LAWS = Path(__file__).resolve().parents[1] / "laws"
MAX_AGE_DAYS = 183
REQUIRED = ["title", "regulator", "status", "zone_trigger", "last_verified", "sources"]
CITE = re.compile(r"\[laws/([a-z0-9-]+\.md)\]")


def front(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        k = re.match(r"([a-z_]+):\s*(.*)$", line)
        if k:
            fields[k.group(1)] = k.group(2).strip()
    fields["_urls"] = re.findall(r"^\s*-\s*(https?://\S+)", m.group(1), re.M)
    return fields


def problems(path, today):
    """Return a list of problems with one law file (empty when it is fine)."""
    if not path.exists():
        return ["file does not exist"]
    f = front(path.read_text(encoding="utf-8"))
    out = [f"missing field {k}" for k in REQUIRED if k not in f]
    if f.get("zone_trigger") not in ("BLACK", "GRAY", "WHITE"):
        out.append("zone_trigger must be BLACK, GRAY, or WHITE")
    if not f.get("_urls"):
        out.append("sources needs at least one https:// url")
    try:
        age = (today - date.fromisoformat(f.get("last_verified", ""))).days
        if age > MAX_AGE_DAYS:
            out.append(f"STALE: last verified {age} days ago (limit {MAX_AGE_DAYS})")
        if age < 0:
            out.append("last_verified is in the future")
    except ValueError:
        out.append("last_verified must be YYYY-MM-DD")
    return out


def lint(today):
    files = sorted(p for p in LAWS.glob("*.md") if p.name != "README.md")
    bad = {p.name: problems(p, today) for p in files}
    bad = {k: v for k, v in bad.items() if v}
    for name, ps in bad.items():
        print(f"  {name}: {'; '.join(ps)}")
    print("lint ok" if not bad else f"lint failed: {len(bad)} of {len(files)} files")
    return 1 if bad else 0


def check_session(session, today):
    files = sorted(session.glob("*.md"))
    cited = {}
    for f in files:
        for name in CITE.findall(f.read_text(encoding="utf-8", errors="replace")):
            cited.setdefault(name, f.name)
    bad = {n: problems(LAWS / n, today) for n in cited}
    bad = {k: v for k, v in bad.items() if v}
    print(f"law citations: {len(cited)}; problems: {len(bad)}")
    for name, ps in bad.items():
        print(f"  [laws/{name}] (first cited in {cited[name]}): {'; '.join(ps)}")
    return 1 if bad else 0


def selftest():
    import tempfile
    global LAWS
    real = LAWS
    with tempfile.TemporaryDirectory() as d:
        LAWS = Path(d)
        (LAWS / "good.md").write_text("---\ntitle: T\nregulator: RBI\nstatus: in force\nzone_trigger: BLACK\n"
                                      "last_verified: 2026-01-01\nsources:\n  - https://x.in\n---\nbody\n", encoding="utf-8")
        assert problems(LAWS / "good.md", date(2026, 3, 1)) == []
        assert any("STALE" in p for p in problems(LAWS / "good.md", date(2027, 1, 1)))
        assert problems(LAWS / "nope.md", date(2026, 3, 1)) == ["file does not exist"]
        assert CITE.findall("see [laws/good.md] and [laws/nope.md]") == ["good.md", "nope.md"]
    LAWS = real
    print("selftest ok")
    return 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252 and crash on Hindi or ₹
    today = date.today()
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "--selftest":
        return selftest()
    if sys.argv[1] == "--lint":
        return lint(today)
    return check_session(Path(sys.argv[1]), today)


if __name__ == "__main__":
    sys.exit(main())
