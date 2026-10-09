# The Soul Library

**Read the serials.** The shelf of [Gaurav Meena](https://github.com/gm5206663-bit) —
live, complete, and paused serials in Soul Land and beyond, published as one clean
reading site — 219 chapters (The Unraveled Tide counts its 8-B special), 928K+ words of chapter
text, every shipped chapter
machine-checked against canon before it lands here.

**Live:** https://gm5206663-bit.github.io/soul-library/

## What's on the shelf

| Serial | Era | State |
|---|---|---|
| The Golden Lion | Soul Land 2 | 🔴 LIVE — new chapters near-daily; the shelf tracks the source repo's latest editions |
| The Grey Wolf | Soul Land 2 | 🔴 LIVE · PERFECT REBUILD · 6 chapters, 16K words — Arc 1 Grey Ridge complete, Arc 2 hem-road craft daily life, clean and clear gated |
| The Devouring Dragon | Soul Land +1,000 years | 🔴 LIVE — 24 chapters, every one gate-PASS; the canon-voice rollout is republishing the early chapters as they're rewritten (Ch 1–12 live in the new voice; the s52 plain-scene pass has already redone Ch 19–24); [the dragon's full status sheet](dd-status.html) |
| Blue Silver | pre-canon | ✅ Book One complete — 15 chapters, all seven gates passing |
| The Adaptive Prodigy | Soul Land 3 | 116 chapters, ten-layer verification suite all green |
| The Unraveled Tide | Soul Land 2 | 24 chapters, paused |
| One in a Thousand | Soul Land 3 | 🔴 LIVE — 7 chapters, 64K words; the OC beside canon in Glorybound |
| Supergirl — Adrian Vale | DC TV · Supergirl S01 | 🔴 LIVE — 15 chapters, 59K words, ultra clean prose; a native Kryptonian/Daxamite OC in season one |
| Qian Xun Ji Reborn | Soul Land · 11 years before canon | 🔴 LIVE — 4 chapters, all rebuilt in the canon voice and gate-pass; the era's Angel Douluo — a codex instead of a war, the second core formed through the sword's winter |

## How this is built

- Chapter text is copied **unchanged** from the source of truth:
  [soul-land-universal-kit](https://github.com/gm5206663-bit/soul-land-universal-kit),
  [soul-land-2-the-grey-wolf](https://github.com/gm5206663-bit/soul-land-2-the-grey-wolf),
  [qian-xunji-adaptation](https://github.com/gm5206663-bit/qian-xunji-adaptation), and
  [supergirl-adrian-vale](https://github.com/gm5206663-bit/supergirl-adrian-vale).
  When this library and the workspace disagree, the workspace wins.
- Word counts are measured from the files, never typed.
- The reader is one self-contained `index.html` — no frameworks, no CDN, no
  tracking; reading progress lives in your browser's localStorage only.
- The method that keeps these serials canon-true:
  [how-to-write-fanfiction](https://github.com/gm5206663-bit/how-to-write-fanfiction).

## Rebuild

Chapter sources live under `chapters/<serial>/`; metadata in `data/serials.json`.
To refresh a serial: copy the live chapter files from the workspace, re-measure,
and update `data/serials.json` (counts measured from disk, never typed).

---

**⚖️ Fan work.** Soul Land (Douluo Dalu) and all related characters, settings and
terms belong to Tang Jia San Shao (唐家三少) and the original rights holders.
Everything here is non-commercial derivative fan work. Reading copies only —
prose may not be reposted or remixed. Code is MIT ([LICENSE](LICENSE)).
