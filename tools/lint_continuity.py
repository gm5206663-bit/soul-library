#!/usr/bin/env python3
"""lint_continuity.py — cross-chapter consistency checks for the Devouring Dragon.

The 2026-09-23 deep-discoverability addition to the Sentinel. Checks:
  1. TIMELINE monotonicity — no chapter may travel back in time: each row's
     real-age span must start at-or-after the previous row's close.
  2. TIMELINE coverage — every chapter on disk must have a "written (chN…)"
     row, and no row may reference a chapter that does not exist.
  3. PLACES references — every "(chN)" citation must point at an existing
     chapter (or one of the next two shipped chapters is fine to mention in
     advance? NO — a place cited for a chapter that does not exist is a
     forward-reference mistake).
  4. CONTINUITY coverage — chapters ch1..chN all present in the anchor/recap
     tables.

Exit 0 = clean. Any failure prints a receipt and exits 1.
"""
import os, re, sys

KIT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/mine/kit'
DD = os.path.join(KIT, 'soul_land_devouring_dragon')

def read(p):
    return open(p, encoding='utf-8').read()

def main():
    errs = []
    chdir = os.path.join(DD, 'chapters')
    disk = sorted(int(m.group(1)) for f in os.listdir(chdir)
                  if (m := re.match(r'Chapter_(\d+)[_.]', f)) and f.endswith('.md'))
    n = max(disk)

    # 1+2: TIMELINE
    rows = []
    for line in read(os.path.join(DD, 'codex', 'TIMELINE.md')).splitlines():
        m = re.match(r'^\| DL (\d+)[–-](\d+)[^|]*\|[^|]*?~?(\d+)[–-](\d+)\s*(?:→|->)\s*~?(\d+)[–-](\d+)\s*months', line)
        if m:
            rows.append((int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6))))
    for a, b in zip(rows, rows[1:]):
        if a[2] > b[0]:  # prev close > next start
            errs.append(f'TIMELINE goes back in time: closes ~{a[2]} then starts ~{b[0]}')
    written = [int(m.group(1)) for line in read(os.path.join(DD, 'codex', 'TIMELINE.md')).splitlines()
               if (m := re.search(r'written \(ch(\d+)', line))]
    missing = [c for c in disk if c not in written]
    ghost = [c for c in written if c not in disk]
    if missing: errs.append(f'TIMELINE missing rows for chapters: {missing}')
    if ghost: errs.append(f'TIMELINE rows for non-existent chapters: {ghost}')

    # 3: PLACES forward references
    cites = [int(x) for x in re.findall(r'\(ch(\d+)\)', read(os.path.join(DD, 'codex', 'PLACES.md')))]
    fwd = sorted({c for c in cites if c > n})
    if fwd: errs.append(f'PLACES cite chapters that do not exist: {fwd}')

    # 4: CONTINUITY coverage
    cont = {m.group(1) for m in re.finditer(r'^\| ch(\d+) \|', read(os.path.join(DD, 'foundation', 'CONTINUITY.md')), re.M)}
    holes = [c for c in disk if str(c) not in cont]
    if holes: errs.append(f'CONTINUITY missing rows for chapters: {holes}')

    if errs:
        print('continuity lint: FAIL')
        for e in errs: print('  - ' + e)
        sys.exit(1)
    print(f'continuity lint: PASS — {len(rows)} timeline rows monotonic; ch1–{n} covered in TIMELINE and CONTINUITY; '
          f'{len(cites)} place citations all valid')

if __name__ == '__main__':
    main()
