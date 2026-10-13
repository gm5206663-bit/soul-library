# The Soul Library

**Read the serials.** The shelf of [Gaurav Meena](https://github.com/gm5206663-bit) —
live, complete, and paused serials in Soul Land and beyond, published as one clean
reading site — **312 chapters** across **18 serials** (The Unraveled Tide counts its 8-B
special), **1.35M+ words** of chapter text, every shipped chapter
machine-checked against canon before it lands here.

**Live:** https://gm5206663-bit.github.io/soul-library/

## What's on the shelf

| Serial | Era | State |
|---|---|---|
| The Golden Lion | Soul Land 2 | 🔴 LIVE — new chapters near-daily; the shelf tracks the source repo's latest editions |
| The Grey Wolf | Soul Land 2 | 🔴 LIVE · PERFECT REBUILD · 10 chapters, 26K words — Arc 1 Grey Ridge complete, Arc 2 the road to Shrek City and the combat exam, clean and clear gated |
| The Devouring Dragon | Soul Land +1,000 years | 🔴 LIVE — 24 chapters, every one gate-PASS; the canon-voice rollout is republishing the early chapters as they're rewritten (Ch 1–12 live in the new voice; the s52 plain-scene pass has already redone Ch 19–24); [the dragon's full status sheet](dd-status.html) |
| Blue Silver | pre-canon | ✅ Book One complete — 15 chapters, all seven gates passing |
| The Adaptive Prodigy | Soul Land 3 | 116 chapters, ten-layer verification suite all green |
| The Unraveled Tide | Soul Land 2 | 24 chapters, paused |
| One in a Thousand | Soul Land 3 | 🔴 LIVE — 7 chapters, 64K words; the OC beside canon in Glorybound |
| Supergirl — Adrian Vale | DC TV · Supergirl S01 | 🔴 LIVE — 17 chapters, 62K words, ultra clean prose; a native Kryptonian/Daxamite OC in season one |
| Qian Xun Ji Reborn | Soul Land · 11 years before canon | 🔴 LIVE — 9 chapters, all gate-pass; the era's Angel Douluo — a codex instead of a war, the second core formed through the sword's winter |
| Fire Phoenix | Soul Land 4 | 🔴 LIVE — 52 chapters, 271K words; the published layer complete through *Amiable Beasts* (Ch 52); the late-arc V2 promotion awaits the author's ruling |
| Lan Shen | Soul Land 3 | 🔴 LIVE — 7 chapters, 32K words; dual-track — canon on the page, complete and in order, the OC's parallel on the same clock |
| Fire Dragon Lizard | Soul Land 1 | ✅ Complete — 5 chapters, 19K words; Tang San's best friend from Holy Spirit Village, a Ground Fire Dragon Lizard soul, no system at all |
| Holy Spirit | Soul Land 2 | Paused at Chapter 4 — the reincarnator who awakens the Devouring Dragon soul |
| The System Cheat | Soul Land · system | ⚙ Design stage — 4 sample chapters, 16K words; the system is fully specified |
| Dragon Prince Yuan | Dragon Prince Yuan (Yuan Zun) | Chapter 1 — a native OC with natural butterflies; the serial waits on source text |
| Stark Heir | MCU · film order | 5 chapters, 28K words — Tony's son, a public heir with a hidden mutation; canon on-page in film order |
| MCU Eternal — Varun | MCU · post-Blip (Eternals) | Paused at Chapter 3 — an eleventh Eternal; gravity and kinetic command, the Adaptation Talent |
| Soul Land 3 — The New Serial | Soul Land 3 | Retired — one gated chapter kept (working title pending R1) |

## How this is built

- Chapter text is copied **unchanged** from the source of truth:
  [soul-land-universal-kit](https://github.com/gm5206663-bit/soul-land-universal-kit)
  (every Soul Land serial — the live builds, the parked Blue Silver, the frozen reference),
  [supergirl-adrian-vale](https://github.com/gm5206663-bit/supergirl-adrian-vale),
  [stark_heir](https://github.com/gm5206663-bit/stark_heir) and
  [mcu_eternal_fanfic](https://github.com/gm5206663-bit/mcu_eternal_fanfic).
  When this library and the workspace disagree, the workspace wins.
- Word counts are measured from the files, never typed.
- The reader is one self-contained `index.html` — no frameworks, no CDN, no
  tracking; reading progress lives in your browser's localStorage only.
- The method that keeps these serials canon-true:
  [how-to-write-fanfiction](https://github.com/gm5206663-bit/how-to-write-fanfiction).

## Rebuild

Chapter sources live under `chapters/<serial>/`; metadata in `data/serials.json`.
To refresh the shelf: `python3 tools/sync_shelf.py --kit <path-to-kit> --supergirl
<path-to-supergirl-repo> --stark <path-to-stark-heir> --mcu <path-to-mcu-eternal>`. It copies each source byte-for-byte, re-measures every
chapter with the site's own recipe (the same function that builds the analytics),
rebuilds `serials.json`, `search_data.json` and the sitemap, re-runs analytics,
recaps and the sentinel — and refuses to finish unless a fresh byte comparison
finds zero differences. Hand-copying is how the shelf fell behind before; this is
the way now.

---

**⚖️ Fan work.** Soul Land (Douluo Dalu) and all related characters, settings and
terms belong to Tang Jia San Shao (唐家三少) and the original rights holders.
Everything here is non-commercial derivative fan work. Reading copies only —
prose may not be reposted or remixed. Code is MIT ([LICENSE](LICENSE)).
