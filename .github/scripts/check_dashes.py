"""Fail if any seat, brain or law file contains an em or en dash (house style)."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2] / ".claude" / "skills" / "baithak"
DASHES = ("–", "—")
bad = [str(p) for d in ("seats", "brains", "laws") for p in (ROOT / d).rglob("*.md")
       if any(c in p.read_text(encoding="utf-8") for c in DASHES)]
print("\n".join(bad) or "dash check ok")
sys.exit(1 if bad else 0)
