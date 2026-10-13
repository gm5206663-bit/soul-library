#!/usr/bin/env python3
"""sync_shelf.py — copy the shelf onto its sources, re-measure, keep every surface honest.

WHY THIS EXISTS
  The shelf's own law, in its README: "Chapter text is copied unchanged from the
  source of truth... When this library and the workspace disagree, the workspace
  wins." Until this file existed, nothing enforced it. On 2026-10-13 a byte-level
  comparison found three serials behind their sources (Grey Wolf missing its
  Chapters 7-10 and holding an older Ch6; Supergirl fifteen files against
  seventeen; The Unraveled Tide all twenty-four files older than the 2026-10-11
  sentence repair). The kit ships chapters with a tool; the shelf had none — that
  is the sync-gap class of failure the house keeps recording. This is the shelf's.

WHAT IT DOES, IN ORDER — refusing to guess anywhere
  1. compare every chapter, byte-for-byte, against its source tree (one map,
     below); list missing and differing files; copy the source's bytes over
  2. re-measure EVERY chapter with this site's own recipe (analytics.measure —
     the same function that builds analytics_data.json; the site has one measure)
  3. rebuild data/serials.json: words per chapter, total_words, words_label
     (floor to whole K). Titles, badges, notes and every authored field are
     preserved untouched — this tool never writes prose
  4. rebuild search_data.json straight from disk (one entry per chapter)
  5. patch sitemap.xml: chapter URLs added/removed, lastmod bumped only on the
     files that actually changed

WHAT IT DELIBERATELY DOES NOT DO
  It does not write the news/feed entry, the README rows, or any badge text —
  those are authored surfaces and are updated by hand with the numbers this tool
  prints. It does not delete shelf files whose source is gone: it names them.

Usage:
  python3 tools/sync_shelf.py --kit /path/to/soul-land-universal-kit \
      [--supergirl /path/to/supergirl-adrian-vale] [--titles titles.json] [--dry]

  titles.json adds titles for chapters new to the shelf:
      {"grey_wolf": {"Chapter_07_The_Third_Village.md": "The Third Village"}}

  Exit 0 only when, after writing, a fresh comparison reports zero missing and
  zero differing files. A step that cannot verify itself is a bug in this tool.
"""
import argparse, hashlib, importlib.util, json, os, re, subprocess, sys, shutil

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = '2026-10-13'

# serial id -> (path template, source label). {kit} / {supergirl} are filled in.
SOURCE_MAP = {
    'adaptive_prodigy':     ('{kit}/adaptive_prodigy/chapters',                   'soul-land-universal-kit'),
    'blue_silver':          ('{kit}/_archive/2026-09-30_park/blue_silver/chapters_rebuilt', 'soul-land-universal-kit (parked)'),
    'devouring_dragon':     ('{kit}/soul_land_devouring_dragon/chapters',        'soul-land-universal-kit'),
    'golden_lion':          ('{kit}/soul_land_2_new/chapters',                   'soul-land-universal-kit'),
    'grey_wolf':            ('{kit}/soul_land_2_the_grey_wolf/chapters',         'soul-land-universal-kit'),
    'one_in_a_thousand':    ('{kit}/soul_land_3_oc/chapters',                    'soul-land-universal-kit'),
    'qian_xunji':           ('{kit}/qian_xunji/chapters',                        'soul-land-universal-kit'),
    'supergirl_adrian_vale':('{supergirl}/chapters',                             'supergirl-adrian-vale'),
    'unraveled_tide':       ('{kit}/Soul_Land_2_Project/chapters',               'soul-land-universal-kit'),
}
SKIP_NAMES = {'README.md'}          # source-tree documentation, not a chapter

def ok(m):   print(f'  ✓ {m}')
def info(m): print(f'    {m}')
def die(m):  print(f'  ✗ {m}'); sys.exit(1)

def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()

def load_measure():
    """The site's one measuring recipe — imported from its own tool, never re-typed."""
    path = os.path.join(SITE, 'tools', 'analytics.py')
    spec = importlib.util.spec_from_file_location('shelf_analytics', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.measure

def chapter_order(entry):
    """Sort key that understands Chapter_07_..., chapter_08a.md and n='8b'."""
    n = entry.get('n')
    if isinstance(n, int):
        return (n, 0, entry['file'])
    m = re.match(r'(\d+)([a-zA-Z]?)', str(n) if n else '')
    if m:
        return (int(m.group(1)), ord(m.group(2) or 'a') - 96, entry['file'])
    m = re.match(r'chapter_(\d+)([a-z]?)', entry['file'], re.I)
    if m:
        return (int(m.group(1)), ord(m.group(2) or 'a') - 96, entry['file'])
    return (9999, 0, entry['file'])

def h1_title(text):
    for line in text.split('\n'):
        if line.startswith('# '):
            t = line[2:].strip()
            t = re.sub(r'^Chapter\s+[\dA-Za-z]+[:\s—–-]*', '', t).strip()
            return t or None
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default=os.environ.get('SOUL_LAND_KIT'))
    ap.add_argument('--supergirl', default=os.environ.get('SOUL_LAND_SUPERGIRL'))
    ap.add_argument('--titles')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    if not a.kit or not os.path.isdir(a.kit):
        die('--kit /path/to/soul-land-universal-kit is required (or SOUL_LAND_KIT)')
    fmt = dict(kit=os.path.abspath(a.kit),
               supergirl=os.path.abspath(a.supergirl) if a.supergirl else '')
    titles = json.load(open(a.titles)) if a.titles else {}
    measure = load_measure()

    sj_path = os.path.join(SITE, 'data', 'serials.json')
    book = json.load(open(sj_path))
    serials = book['serials']

    # ---- 1. compare, copy ----------------------------------------------------
    copied, new_files, changed, missing_names = [], [], [], []
    for s in serials:
        sid = s['id']
        if sid not in SOURCE_MAP:
            continue
        src = SOURCE_MAP[sid][0].format(**fmt)
        if not os.path.isdir(src):
            die(f'{sid}: source tree not found: {src}')
        sd = os.path.join(SITE, 'chapters', sid)
        src_names = {f for f in os.listdir(src) if f.endswith('.md') and f not in SKIP_NAMES}
        shelf_names = {f for f in os.listdir(sd) if f.endswith('.md')}
        for f in sorted(src_names):
            sp, tp = os.path.join(src, f), os.path.join(sd, f)
            if not os.path.exists(tp):
                new_files.append(f'{sid}/{f}')
            elif sha(sp) != sha(tp):
                changed.append(f'{sid}/{f}')
            else:
                continue
            if not a.dry:
                shutil.copyfile(sp, tp)
            copied.append(f'{sid}/{f}')
        for f in sorted(shelf_names - src_names):
            missing_names.append(f'{sid}/{f}')       # source gone; named, never deleted
    info(f'copied {len(copied)} file(s): {len(new_files)} new, {len(changed)} replaced')
    for f in new_files: info(f'  new       {f}')
    for f in changed:  info(f'  replaced  {f}')
    for f in missing_names: info(f'  source-gone (kept, named): {f}')

    # ---- 2+3. re-measure every chapter, rebuild serials.json numbers ---------
    touched = 0
    for s in serials:
        sid = s['id']
        sd = os.path.join(SITE, 'chapters', sid)
        on_disk = sorted(f for f in os.listdir(sd) if f.endswith('.md'))
        by_file = {c['file']: c for c in s['chapters']}
        out = []
        for f in on_disk:
            text = open(os.path.join(sd, f), encoding='utf-8').read()
            c = by_file.get(f)
            if c is None:
                t = (titles.get(sid, {}) or {}).get(f) or h1_title(text) or f
                m = re.match(r'chapter[_-]?(\d+)([a-z]?)', f, re.I)
                c = {'n': int(m.group(1)) if m else 0, 'file': f, 'title': t, 'words': 0}
                if m and m.group(2) and m.group(2) != 'a':
                    c['n'] = f"{m.group(1)}{m.group(2)}"
                out.append(c)
            else:
                out.append(c)
            w = measure(text)[0]   # measure() returns (words, avg, max, dialogue)
            if c['words'] != w:
                touched += 1
            c['words'] = w
        out.sort(key=chapter_order)
        for c in out:                       # keep the file's field order stable
            c2 = {k: c[k] for k in ('n', 'file', 'title', 'words') if k in c}
            c.clear(); c.update(c2)
        s['chapters'] = out
        s['total_words'] = sum(c['words'] for c in out)
        s['words_label'] = f"{s['total_words'] // 1000}K"
    info(f're-measured every chapter — {touched} number(s) changed')

    # ---- 4. search_data.json straight from disk ------------------------------
    search = []
    for s in serials:
        for c in s['chapters']:
            text = open(os.path.join(SITE, 'chapters', s['id'], c['file']), encoding='utf-8').read()
            search.append({'i': s['id'], 'n': c['n'], 't': c['title'], 'w': c['words'], 'x': text})

    # ---- 5. sitemap: chapter URLs, lastmod only where it moved ---------------
    sm_path = os.path.join(SITE, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    url_rx = re.compile(r' <url><loc>([^<]+)</loc><lastmod>([^<]+)</lastmod></url>\n')
    entries = url_rx.findall(sm)
    pages = [(loc, lm) for loc, lm in entries if '/chapters/' not in loc]
    old = {loc.rsplit('/', 1)[1] + '|' + loc.split('/chapters/')[1].split('/')[0]: lm
           for loc, lm in entries if '/chapters/' in loc}
    base = 'https://gm5206663-bit.github.io/soul-library'
    lines = [f' <url><loc>{loc}</loc><lastmod>{lm}</lastmod></url>' for loc, lm in pages]
    for s in serials:
        for c in s['chapters']:
            key = f"{c['file']}|{s['id']}"
            lm = TODAY if any(x == f"{s['id']}/{c['file']}" for x in copied) else old.get(key, TODAY)
            lines.append(f' <url><loc>{base}/chapters/{s["id"]}/{c["file"]}</loc><lastmod>{lm}</lastmod></url>')
    new_sm = sm.split(' <url>')[0] + '\n'.join(lines) + '\n</urlset>\n'

    if a.dry:
        print('  DRY RUN — nothing written. Shelf totals would become:')
        tot = sum(s['total_words'] for s in serials)
        for s in serials:
            print(f"    {s['id']:22s} {len(s['chapters']):3d} ch  {s['total_words']:7,d} w  {s['words_label']}")
        print(f"    {'TOTAL':22s} {sum(len(s['chapters']) for s in serials):3d} ch  {tot:7,d} w")
        return

    json.dump(book, open(sj_path, 'w'), indent=1, ensure_ascii=False)
    open(sj_path, 'a').write('\n')
    json.dump(search, open(os.path.join(SITE, 'search_data.json'), 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(SITE, 'search_data.json'), 'a').write('\n')
    open(sm_path, 'w').write(new_sm)
    ok('wrote data/serials.json, search_data.json, sitemap.xml')

    # ---- 6. the tools that own the other surfaces ----------------------------
    for cmd in (['python3', 'tools/analytics.py'],
                ['python3', 'tools/build_recaps.py', fmt['kit']],
                ['python3', 'tools/sentinel.py', '--kit', fmt['kit']]):
        r = subprocess.run(cmd, cwd=SITE, capture_output=True, text=True)
        tail = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else '(no output)'
        if r.returncode != 0:
            die(f"{' '.join(cmd)} failed: {tail}")
        ok(f"{' '.join(cmd)} — {tail}")

    # ---- 7. verify — a fresh comparison must find zero ------------------------
    bad = 0
    for s in serials:
        src = SOURCE_MAP[s['id']][0].format(**fmt)
        sd = os.path.join(SITE, 'chapters', s['id'])
        src_names = {f for f in os.listdir(src) if f.endswith('.md') and f not in SKIP_NAMES}
        for f in sorted(src_names):
            if not os.path.exists(os.path.join(sd, f)) or sha(os.path.join(src, f)) != sha(os.path.join(sd, f)):
                bad += 1; info(f'STILL DIFFERENT: {s["id"]}/{f}')
    if bad:
        die(f'{bad} file(s) still differ after sync')
    ok('verified: every shelf chapter byte-identical to its source')
    tot = sum(s['total_words'] for s in serials)
    ok(f'shelf totals now: {sum(len(s["chapters"]) for s in serials)} chapters · {tot:,} words')

if __name__ == '__main__':
    main()
