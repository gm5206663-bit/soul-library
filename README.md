# The Soul Library

**Read the serials.** Every gated Soul Land (斗罗大陆) fanfiction serial by
[Gaurav Meena](https://github.com/gm5206663-bit), published as one clean reading
site — 187 chapters, 781K+ words of chapter text, every shipped chapter
machine-checked against canon before it lands here.

**Live:** https://gm5206663-bit.github.io/soul-library/

## What's on the shelf

| Serial | Era | State |
|---|---|---|
| The Golden Lion | Soul Land 2 | 🔴 LIVE — new chapters near-daily (snapshot at build) |
| The Devouring Dragon | Soul Land +1,000 years | 🔴 LIVE — 24 chapters, every one gate-PASS; the canon-voice rollout is republishing the early chapters as they're rewritten (Ch 1–10 live in the new voice); [the dragon's full status sheet](dd-status.html) |
| Blue Silver | pre-canon | ✅ Book One complete — 15 chapters, all seven gates passing |
| The Adaptive Prodigy | Soul Land 3 | 116 chapters, ten-layer verification suite all green |
| The Unraveled Tide | Soul Land 2 | 24 chapters, paused |

## How this is built

- Chapter text is copied **unchanged** from the source of truth:
  [soul-land-universal-kit](https://github.com/gm5206663-bit/soul-land-universal-kit).
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
