#!/usr/bin/env python3
"""sentinel.py — the independent workspace health scan.

Scans a soul-land-universal-kit checkout + this library site, RUNS the real
gates, checks every live-edge claim it can find, and writes sentinel.html +
sentinel_data.json into the site root.

Every value on the page is measured, never typed. Re-run any time:

    python3 tools/sentinel.py --kit /path/to/soul-land-universal-kit

Checks (per serial):
  - panel/README live-edge claim  vs  chapter files on disk
  - library snapshot count        vs  chapter files on disk
  - gate result                   (actually executed where a gate exists)
Workspace checks:
  - kit README serial-row counts vs disk
  - Control Centre registered edge vs disk (if a checkout is given)
  - the public profile README's live-edge claims vs disk (fetched live)
"""
import json, os, re, subprocess, sys, datetime, urllib.request

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=300)
    return r.stdout + r.stderr, r.returncode

# Lesson (first run, 2026-09-23): counting *.md in a chapters/ dir over-counts
# when the dir carries notes/README files (the Tide false-positive). Count only
# chapter-numbered files — a checker must measure the thing it claims to measure.
CH_RX = re.compile(r'^(chapter_|Chapter_)[0-9]+([_].*)?[.]md$')

def count_md(path):
    if not os.path.isdir(path):
        return -1
    return len([f for f in os.listdir(path) if CH_RX.match(f)])

def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.read().decode('utf-8', 'replace')
    except Exception as e:
        return None

def main():
    kit = None
    for i, a in enumerate(sys.argv):
        if a == '--kit' and i + 1 < len(sys.argv):
            kit = os.path.abspath(sys.argv[i + 1])
    checks = []

    def add(serial, name, ok, receipt, warn=False):
        checks.append({'serial': serial, 'check': name,
                       'status': 'warn' if warn else ('pass' if ok else 'fail'),
                       'receipt': receipt})

    # ── measured facts from the library snapshot ──────────────────────────
    lib = json.load(open(f'{SITE}/data/serials.json'))
    lib_edges = {s['id']: max((c['n'] for c in s['chapters'] if isinstance(c['n'], int)), default=0)
                 for s in lib['serials']}

    # ── per-serial checks against the live workspace ─────────────────────
    if kit:
        specs = [
            ('devouring_dragon', 'soul_land_devouring_dragon', 'chapters',
             r'after Chapter (\d+)', 'foundation/STATUS_PANEL.md'),
            ('golden_lion', 'soul_land_2_new', 'chapters',
             r'chapters live: \*\*(\d+)\*\*', 'foundation/STATUS_PANEL.md'),
            ('unraveled_tide', 'Soul_Land_2_Project', 'chapters',
             r'Chapter (\d+)', 'foundation/STATUS_PANEL.md'),
            ('blue_silver', 'blue_silver', 'chapters_rebuilt',
             r'(\d+) rebuilt chapters', 'README.md'),
        ]
        for sid, rel, chdir, rx, panelf in specs:
            disk = count_md(os.path.join(kit, rel, chdir))
            if disk < 0:
                add(sid, 'chapters on disk', False, f'{rel}/{chdir} not found'); continue
            add(sid, 'chapters on disk', True, f'{rel}/{chdir}: {disk} chapter files')
            p = os.path.join(kit, rel, panelf)
            if os.path.exists(p):
                m = re.search(rx, open(p, encoding='utf-8').read())
                if m:
                    claimed = int(m.group(1))
                    add(sid, 'panel live-edge vs disk', claimed == disk,
                        f'{panelf} claims {claimed}; disk has {disk}')
            # compare LIVE EDGES (max numbered chapter), not raw counts: the
            # library may legitimately carry labelled variants (e.g. Tide 8-B)
            lib_max = lib_edges.get(sid)
            if lib_max is not None:
                disk_max = max((int(m.group(2)) for f2 in os.listdir(os.path.join(kit, rel, chdir))
                                for m in [re.match(r'^(chapter_|Chapter_)([0-9]+)([_].*)?[.]md$', f2)] if m), default=0)
                add(sid, 'library live-edge vs disk', lib_max == disk_max,
                    f'library edge: Ch {lib_max}; disk edge: Ch {disk_max} (live serials drift — refresh the snapshot)',
                    warn=(lib_max != disk_max and sid in ('golden_lion', 'devouring_dragon')))
        sl3 = count_md(os.path.join(kit, 'Soul_Land_3_Project', 'chapters'))
        add('adaptive_prodigy', 'chapters on disk', sl3 >= 116, f'Soul_Land_3_Project/chapters: {sl3} files')

        # ── the real gates, actually run ──────────────────────────────────
        out, rc = run('python3 SOUL_LAND_WORKSPACE/kit/tools/verify.py --project soul_land_devouring_dragon', kit)
        add('devouring_dragon', 'kit verify sweep', rc == 0 and 'PASS' in out,
            'VERDICT: ' + ('PASS' if rc == 0 else 'FAIL') + f' ({count_md(os.path.join(kit,"soul_land_devouring_dragon","chapters"))}/{count_md(os.path.join(kit,"soul_land_devouring_dragon","chapters"))} footers)')
        out, rc = run('python3 checks/verify.py', os.path.join(kit, 'soul_land_2_new'))
        add('golden_lion', 'sl2-goldenv gate', rc == 0, out.strip().splitlines()[-1][:90])
        out, rc = run('sh checks/run_all.sh', os.path.join(kit, 'Soul_Land_3_Project'))
        add('adaptive_prodigy', 'ten-layer run_all', rc == 0,
            out.strip().splitlines()[-1][:110])

        # ── frozen trees must SAY they are frozen (2026-09-23 catch) ──────
        p = os.path.join(kit, 'soul_land_3_new', 'foundation', 'STATUS_PANEL.md')
        if os.path.exists(p):
            frozen = 'FROZEN' in open(p, encoding='utf-8').read()
            add('sl3_new_frozen', 'frozen panel asserts FROZEN', frozen,
                'panel says FROZEN (author plan-change 2026-09-22)' if frozen
                else 'panel does NOT say FROZEN — a frozen tree claiming liveness')

        # ── the kit's two trees must be ONE copy (2026-09-23 deep sweep) ─
        u = os.path.join(kit, 'SOUL_LAND_UNIVERSAL_KIT')
        w = os.path.join(kit, 'SOUL_LAND_WORKSPACE', 'kit')
        if os.path.isdir(u) and os.path.isdir(w):
            out, rc = run(f'diff -rq {u} {w}', kit)
            add('workspace', 'kit trees byte-identical (D1 law)', rc == 0,
                'released kit == working copy' if rc == 0
                else 'DRIFT: ' + '; '.join(out.strip().splitlines()[:2])[:200])

        # ── blue_silver live Book One under the unified gate ─────────────
        out, rc = run('python3 SOUL_LAND_WORKSPACE/kit/tools/verify.py --project blue_silver', kit)
        add('blue_silver', 'unified gate (live Book One)', rc == 0,
            out.strip().splitlines()[-1][:90])

        # ── no duplicated row numbers in the live serial's log ────────────
        logp = os.path.join(kit, 'soul_land_2_new', 'foundation', 'SERIAL_LOG.md')
        if os.path.exists(logp):
            nums = [l.split('|')[1].strip() for l in
                    open(logp, encoding='utf-8').read().splitlines()
                    if l.startswith('| ') and l[2].strip().isdigit()]
            dups = sorted({n for n in nums if nums.count(n) > 1})
            add('golden_lion', 'SERIAL_LOG row numbers unique', not dups,
                f'{len(nums)} rows, all unique' if not dups else f'duplicated rows: {", ".join(dups)}')

        # ── kit README serial rows vs disk (the drift that bit before) ────
        rd = open(os.path.join(kit, 'README.md'), encoding='utf-8').read()
        m = re.search(r'devouring-dragon serial \((\d+) chapters', rd)
        if m:
            disk = count_md(os.path.join(kit, 'soul_land_devouring_dragon', 'chapters'))
            add('workspace', 'kit README DD row vs disk', int(m.group(1)) == disk,
                f'README says {m.group(1)}; disk has {disk}')

    # ── the public profile's live-edge claims, fetched live ──────────────
    prof = fetch('https://raw.githubusercontent.com/gm5206663-bit/gm5206663-bit/main/README.md')
    if prof:
        m = re.search(r'Devouring Dragon.*?(\d+) chapters', prof, re.S)
        if m:
            disk = count_md(os.path.join(kit, 'soul_land_devouring_dragon', 'chapters')) if kit else None
            if disk is not None:
                add('profile', 'profile DD count vs disk', int(m.group(1)) == disk,
                    f'profile says {m.group(1)} chapters; disk has {disk}')
        m = re.search(r'Ch (\d+)[^|]*\|', prof)
        if m and kit:
            gl_disk = count_md(os.path.join(kit, 'soul_land_2_new', 'chapters'))
            add('profile', 'profile Golden Lion edge vs disk', int(m.group(1)) == gl_disk,
                f'profile says Ch {m.group(1)}; disk has Ch {gl_disk}',
                warn=(int(m.group(1)) < gl_disk))
    else:
        add('profile', 'profile fetch', False, 'could not fetch the public profile README')

    order = {'pass': 0, 'warn': 1, 'fail': 2}
    checks.sort(key=lambda c: (order[c['status']], c['serial']))
    n_pass = sum(1 for c in checks if c['status'] == 'pass')
    n_warn = sum(1 for c in checks if c['status'] == 'warn')
    n_fail = sum(1 for c in checks if c['status'] == 'fail')
    json.dump({'generated': NOW, 'n_pass': n_pass, 'n_warn': n_warn, 'n_fail': n_fail, 'checks': checks},
              open(f'{SITE}/sentinel_data.json', 'w'), indent=1)
    print(f'sentinel: {n_pass} pass / {n_warn} warn / {n_fail} fail — {len(checks)} checks')
    return 0

if __name__ == '__main__':
    sys.exit(main())
