#!/usr/bin/env python3
"""build_recaps.py — build recaps_data.json ("The Story So Far") for the Library.

Sources:
  - kit devouring-dragon foundation/CONTINUITY.md (two table formats; the LAST
    occurrence per chapter wins — the recap table overrides the anchor table)
  - site data/serials.json (chapter titles; the fallback for every serial
    without a continuity mirror)

Output: recaps_data.json — {serial: {"title":…, "chapters":[["n","title","recap"],…]}}
Re-run after every chapter ship (the ship script calls analytics; call this too).
"""
import json, os, re, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/mine/kit'

def dd_recaps():
    p = os.path.join(KIT, 'soul_land_devouring_dragon', 'foundation', 'CONTINUITY.md')
    out = {}
    for line in open(p, encoding='utf-8'):
        m = re.match(r'^\| (ch\d+[a-z]?) \|', line)
        if not m:
            continue
        n = m.group(1)[2:]
        cols = [c.strip() for c in line.split('|')[1:-1]]
        # anchor table: | chN | date | event | constrains |  -> use event
        # recap table:  | chN | state | recap |             -> use recap (wins)
        text = cols[2] if len(cols) >= 3 else ''
        out[n] = re.sub(r'\s+', ' ', text).strip()
    return out

def main():
    d = json.load(open(os.path.join(SITE, 'data', 'serials.json'), encoding='utf-8'))
    rich = dd_recaps()
    data = {}
    for s in d['serials']:
        chs = []
        for c in s['chapters']:
            n = str(c['n'])
            chs.append([n, c['title'], rich.get(n, '')])
        data[s['id']] = {'title': s.get('name', s['id']), 'chapters': chs}
    json.dump(data, open(os.path.join(SITE, 'recaps_data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    rich_n = sum(1 for ch in rich.values() if ch)
    print(f"recaps: {sum(len(v['chapters']) for v in data.values())} chapters across {len(data)} serials; {rich_n} carry full continuity recaps")

if __name__ == '__main__':
    main()
