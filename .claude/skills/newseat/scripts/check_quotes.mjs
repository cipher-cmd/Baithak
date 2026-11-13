#!/usr/bin/env node
// Check that every quote in a seat's notes or brain is verbatim in the source it cites.
//
//   node .claude/skills/newseat/scripts/check_quotes.mjs <build dir> <file or folder> [...] [--stamp]
//
// A quote is text in double quotes followed within a few characters by a source id, like
// "..." (S014) or "..." (S014, S020). Each quote must appear in the corpus file of one of
// its ids. A quote found under a different id is reported with the right one; a quote found
// nowhere is reported as not found and must be cut or replaced. Quotes with "..." are checked
// piece by piece. Exit code 1 when anything needs fixing.
//
//   --stamp  also write the video time of each verified quote into the file, after its id:
//            "..." (S014@12:34, 2022-06-17). The time is the transcript's [mm:ss] marker at or
//            before the quote, so a reader can jump to the passage. Web sources get no time.
import fs from "node:fs";
import path from "node:path";

// letters, marks (Hindi vowel signs) and digits in any script; the old a-z0-9 class erased Hindi
const norm = (s) => s.normalize("NFC").toLowerCase()
  .replace(/[‘’`]/g, "'").replace(/[“”]/g, '"')
  .replace(/'\s+(t|s|re|ll|ve|d|m)\b/g, "'$1")
  .replace(/\[\d+:\d\d(:\d\d)?\]/g, " ")
  .replace(/[^\p{L}\p{M}\p{N}' ]+/gu, " ").replace(/\s+/g, " ").trim();

/** transcript -> {text: normalized text, marks: [[offset in text, "mm:ss"]]} */
function timeline(raw) {
  const parts = raw.split(/\[(\d+:\d\d(?::\d\d)?)\]/);
  let text = norm(parts[0]);
  const marks = [];
  for (let i = 1; i < parts.length; i += 2) {
    if (text) text += " ";
    marks.push([text.length, parts[i]]);
    text += norm(parts[i + 1] || "");
  }
  return { text: text.trimEnd(), marks };
}

/** the marker at or before the quote's first piece, or null for a source without markers.
 * Uses the last occurrence: podcast cold opens replay a clip of the answer in the first minute,
 * and the full passage, with its context, comes later. */
function stampOf(tl, q) {
  const piece = q.split(/\.\.\.|…/).map(norm).find((x) => x.split(" ").length >= 3) || norm(q);
  const at = tl.text.lastIndexOf(piece);
  if (at < 0 || !tl.marks.length) return null;
  let best = null;
  for (const [off, st] of tl.marks) if (off <= at) best = st;
  return best;
}

const args = process.argv.slice(2);
const STAMP = args.includes("--stamp");
const [buildArg, ...targets] = args.filter((a) => a !== "--stamp");
if (buildArg === "--selftest") {
  const src = norm("नितिन ने कहा: हम कभी ग्राहकों को स्पैम नहीं करते, यही हमारा भरोसा है।");
  const real = norm("हम कभी ग्राहकों को स्पैम नहीं करते");
  const fake = norm("हम हमेशा ग्राहकों को कॉल करके बेचते हैं");
  if (!(real.split(" ").length >= 4 && src.includes(real))) throw new Error("real Hindi quote must verify");
  if (!(fake.split(" ").length >= 4 && !src.includes(fake))) throw new Error("fake Hindi quote must fail");
  if (norm("We never  SPAM—our users!") !== "we never spam our users") throw new Error("English norm changed");
  const t = timeline("[00:03] Intro words here.\n\n[01:27] We never raise money we do not need.\n\n[102:05] Later talk here");
  if (stampOf(t, "never raise money we do not") !== "01:27") throw new Error("stamp must be the marker before the quote");
  if (stampOf(t, "we do not need. Later talk") !== "01:27") throw new Error("a quote across markers takes the first one");
  if (stampOf(t, "Later talk here") !== "102:05") throw new Error("three-digit minutes must parse");
  const teaser = timeline("[00:05] money is hardly ever right for you\n\n[04:42] so money is hardly ever right for you in full");
  if (stampOf(teaser, "money is hardly ever right for you") !== "04:42") throw new Error("cold-open teaser must not win");
  if (stampOf(timeline("plain web text with no markers"), "web text with no") !== null) throw new Error("web text has no stamp");
  console.log("selftest ok");
  process.exit(0);
}
if (!buildArg || !targets.length) {
  console.error("usage: check_quotes.mjs <build dir> <file or folder> [...] [--stamp]");
  process.exit(2);
}
const BUILD = path.resolve(buildArg);
const sources = JSON.parse(fs.readFileSync(path.join(BUILD, "sources.json"), "utf8"));

const timelines = new Map(sources.map((s) => [s.id, timeline(fs.readFileSync(path.join(BUILD, s.file), "utf8"))]));
const corpus = new Map([...timelines].map(([id, tl]) => [id, tl.text]));

const files = [];
const walk = (p) => {
  if (fs.statSync(p).isDirectory()) for (const n of fs.readdirSync(p)) walk(path.join(p, n));
  else if (/\.md$/.test(p)) files.push(p);
};
for (const t of targets) walk(path.resolve(t));

const found = (q, id) => {
  const hay = corpus.get(id);
  if (!hay) return false;
  // "..." splits a quote into pieces that must each be in the source
  return q.split(/\.\.\.|…/).map(norm).filter((p) => p.split(" ").length >= 3).every((p) => hay.includes(p));
};

let ok = 0, stamped = 0;
const wrong = [], missing = [];
const ID = String.raw`S\d{3}(?:@\d+:\d\d(?::\d\d)?)?`;
const re = new RegExp(String.raw`["“]([^"“”\n]{12,600})["”][^\n"“]{0,40}?[(\[]((?:${ID})(?:\s*[,;]\s*${ID})*)`, "g");
for (const f of files) {
  const raw = fs.readFileSync(f, "utf8");
  const lines = raw.split(/\r?\n/);
  let changed = false;
  lines.forEach((line, i) => {
    const edits = [];
    for (const m of line.matchAll(re)) {
      const q = m[1];
      if (norm(q).split(" ").length < 4) continue;
      const ids = m[2].split(/\s*[,;]\s*/).map((x) => x.split("@")[0]);
      const where = `${path.relative(process.cwd(), f)}:${i + 1}`;
      const hit = ids.find((id) => found(q, id));
      if (hit) {
        ok++;
        const st = STAMP && stampOf(timelines.get(hit), q);
        if (st) {
          stamped++;
          const fixed = m[2].replace(new RegExp(String.raw`\b${hit}(@[\d:]+)?`), `${hit}@${st}`);
          if (fixed !== m[2]) edits.push([m.index + m[0].length - m[2].length, m[2].length, fixed]);
        }
        continue;
      }
      const other = sources.find((s) => found(q, s.id));
      if (other) wrong.push(`${where}  cites ${ids.join(", ")}, but the quote is in ${other.id}: "${q.slice(0, 90)}"`);
      else missing.push(`${where}  not found in any source: "${q.slice(0, 110)}"`);
    }
    // apply right to left so earlier offsets stay valid
    for (const [at, len, fixed] of edits.reverse()) line = line.slice(0, at) + fixed + line.slice(at + len);
    if (edits.length) { lines[i] = line; changed = true; }
  });
  if (changed) fs.writeFileSync(f, lines.join(raw.includes("\r\n") ? "\r\n" : "\n"), "utf8");
}

console.log(`quotes verified: ${ok}; wrong source id: ${wrong.length}; not found: ${missing.length}` +
  (STAMP ? `; video times written: ${stamped}` : ""));
for (const w of wrong) console.log("  WRONG ID  " + w);
for (const m of missing) console.log("  NOT FOUND " + m);
process.exit(wrong.length || missing.length ? 1 : 0);
