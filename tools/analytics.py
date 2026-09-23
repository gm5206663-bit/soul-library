#!/usr/bin/env python3
"""analytics.py — measure every chapter the house way (sentence avg, dialogue
density, length) and write analytics_data.json. Measured, never typed."""
import json, os, re, glob, statistics
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def measure(text):
    body = text.split('## Footer')[0]
    body = '\n'.join(l for l in body.split('\n') if not l.startswith('# '))
    words = len(body.split())
    prose = re.sub(r'"[^"]*"', '', body)
    sents = [s for s in re.split(r'(?<=[.!?])\s+', prose) if s.strip()]
    lens = [len(s.split()) for s in sents]
    dlg = len(re.findall(r'"([^"]{4,})"', body))
    return words, (sum(lens)/len(lens) if lens else 0), (max(lens) if lens else 0), dlg

data = {}
lib = json.load(open(f'{SITE}/data/serials.json'))
for s in lib['serials']:
    rows = []
    for c in s['chapters']:
        if not isinstance(c['n'], int):
            continue
        t = open(f"{SITE}/chapters/{s['id']}/{c['file']}", encoding='utf-8').read()
        w, avg, mx, dlg = measure(t)
        rows.append({'n': c['n'], 'w': w, 'avg': round(avg, 1), 'mx': mx, 'dd': round(dlg / w * 1000, 1) if w else 0})
    data[s['id']] = {'title': s['title'], 'chapters': rows,
                     'avg_words': round(statistics.mean(r['w'] for r in rows)),
                     'avg_sentence': round(statistics.mean(r['avg'] for r in rows), 1),
                     'avg_dialogue': round(statistics.mean(r['dd'] for r in rows), 1)}
json.dump(data, open(f'{SITE}/analytics_data.json', 'w'))
for k, v in data.items():
    print(f"  {k:<18} {len(v['chapters']):>3} ch | avg {v['avg_words']:>5} w/ch | sentence {v['avg_sentence']:>4} | dialogue {v['avg_dialogue']:>5}/1000w")
