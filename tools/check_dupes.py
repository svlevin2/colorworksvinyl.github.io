#!/usr/bin/env python3
"""Pass 3 duplicate check.
Built mode (python3 tools/check_dupes.py --built): reads the built product pages and compares the Pass 3 copy
(Good for line, detail cards, merged section, FAQ questions and answers, slide 6 caption) across pages; exit 1 on any hit.
  It also checks each page's Good for line against its hero lead: ratio < 0.50 and no shared run of 4+ words, else exit 1.
Plan mode (default):
Reads the tagged lines ([copy], [q], [a], [cap]) from the Pass 3 data file, splits them into sentences and flags
  1) exact or near-duplicate sentences on DIFFERENT pages of the proposal, and
  2) proposal sentences that exact- or near-match existing Pass 2 copy on any built page (services/*/index.html, faq/).
Near = difflib ratio >= 0.80 or word-set Jaccard >= 0.70 (sentences of 4+ words). Usage: python3 tools/check_dupes.py [data.md]"""
import re, sys, glob, os, difflib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = sys.argv[1] if len(sys.argv) > 1 else '/home/box/shared/colorworks/website/2026-11-03_pass3-product-depth-data.md'
RATIO, JACC = 0.80, 0.70
norm = lambda s: re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()
def sents(t): return [x.strip() for x in re.split(r'(?<=[.?!])\s+', t) if len(x.split()) >= 4]
def near(a, b):
    A, B = norm(a), norm(b)
    if A == B: return 'exact'
    wa, wb = set(A.split()), set(B.split())
    j = len(wa & wb) / max(1, len(wa | wb)); r = difflib.SequenceMatcher(None, A, B).ratio()
    return f'near r={r:.2f} j={j:.2f}' if r >= RATIO or j >= JACC else None
LEAD_MAX, RUN_MAX = 0.50, 4  # Good for vs lead: ratio must be < 0.50 and no shared run of 4+ words
def words(t): return re.sub(r'[^a-z0-9 ]', ' ', t.lower()).split()
def longest_run(a, b):
    A, B = words(a), words(b); best, run = 0, []
    for i in range(len(A)):
        for j in range(len(B)):
            k = 0
            while i + k < len(A) and j + k < len(B) and A[i + k] == B[j + k]: k += 1
            if k > best: best, run = k, A[i:i + k]
    return best, ' '.join(run)
def lead_vs_good(h):
    """Return (lead, good, ratio, run_len, run) for one built page; good is '' when the page has no Good for line."""
    from html import unescape
    txt = lambda x: unescape(re.sub(r'<[^>]+>', ' ', x)).strip()
    lead = re.search(r'<p class="lead">(.*?)</p>', h, re.S); good = re.search(r'<p class="good-for">(.*?)</p>', h, re.S)
    lead = txt(lead.group(1)) if lead else ''
    if not good: return lead, '', 0.0, 0, ''
    g = re.sub(r'^Good for:\s*', '', txt(good.group(1)))
    r = max(difflib.SequenceMatcher(None, norm(lead), norm(g)).ratio(), difflib.SequenceMatcher(None, norm(lead), norm('Good for ' + g)).ratio())
    n, run = longest_run(lead, g)
    return lead, g, r, n, run
if '--built' in sys.argv:
    from html import unescape
    items = []
    lead_fails = []
    print(f'LEAD vs GOOD FOR (fail if ratio >= {LEAD_MAX} or shared run >= {RUN_MAX} words; no Good for line = pass)')
    for f in sorted(glob.glob(os.path.join(ROOT, 'services/*/index.html'))):
        h = open(f, encoding='utf-8').read()
        if 'prod-depth' not in h: continue
        pg = os.path.basename(os.path.dirname(f)); lead, g, r, n, run = lead_vs_good(h)
        bad = bool(g) and (r >= LEAD_MAX or n >= RUN_MAX)
        if bad: lead_fails.append(pg)
        print(f'  {"FAIL" if bad else "ok  "} {pg:28} ratio={r:.2f} run={n} "{run}" good={"kept" if g else "none"}')
    print(f'LEAD-GOOD pages-failing={len(lead_fails)}')
    for f in sorted(glob.glob(os.path.join(ROOT, 'services/*/index.html'))):
        h = open(f, encoding='utf-8').read()
        if 'prod-depth' not in h: continue
        pg = os.path.basename(os.path.dirname(f))
        blocks = re.findall(r'<p class="good-for">(.*?)</p>', h, re.S)
        m = re.search(r'<section class="section prod-depth.*?<div class="include', h, re.S)
        if m: blocks += re.findall(r'<(?:h3|p)>(.*?)</(?:h3|p)>', re.sub(r'<svg.*?</svg>', '', m.group(0), flags=re.S), re.S)
        caps = re.findall(r'<figcaption>(.*?)</figcaption>', h, re.S)
        if len(caps) == 6: blocks.append(caps[5])
        for b in blocks:
            for s in sents(unescape(re.sub(r'<[^>]+>', ' ', b)).strip()): items.append((pg, s))
    hits = [(h_, a, b) for i, a in enumerate(items) for b in items[i + 1:] if a[0] != b[0] and (h_ := near(a[1], b[1]))]
    print(f'BUILT pages={len({i[0] for i in items})} sentences={len(items)} CROSS-PAGE hits={len(hits)}')
    for h_, a, b in hits: print(f'  {h_}: [{a[0]}] {a[1]!r} <> [{b[0]}] {b[1]!r}')
    sys.exit(1 if hits or lead_fails else 0)
# proposal
prop, page = [], None
for line in open(DATA, encoding='utf-8'):
    m = re.match(r'### \d+ ([a-z0-9-]+)', line)
    if m: page = m.group(1); continue
    m = re.match(r'\[(copy|q|a|cap)\] (.*)', line.strip())
    if m and page:
        txt = m.group(2).split(' (src:')[0]
        txt = re.split(r'\s(UNSOURCED|CONFLICT)-\d+', txt)[0]
        for s in sents(txt): prop.append((page, m.group(1), s))
# existing Pass 2 copy (visible text, scripts stripped)
exist = []
for f in sorted(glob.glob(os.path.join(ROOT, 'services/*/index.html')) + [os.path.join(ROOT, 'faq/index.html')]):
    h = open(f, encoding='utf-8').read()
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    t = re.sub(r'<[^>]+>', '\n', h); t = re.sub(r'&amp;', '&', t)
    for blk in t.split('\n'):
        for s in sents(blk.strip()): exist.append((os.path.relpath(os.path.dirname(f), ROOT), s))
exist = list(dict.fromkeys(exist))
cross = []
for i in range(len(prop)):
    for k in range(i + 1, len(prop)):
        if prop[i][0] != prop[k][0] and (h := near(prop[i][2], prop[k][2])): cross.append((h, prop[i], prop[k]))
vs = []
for p in prop:
    for e in exist:
        if (h := near(p[2], e[1])): vs.append((h, p, e))
print(f'proposal sentences={len(prop)} pages={len({p[0] for p in prop})} existing sentences={len(exist)}')
print(f'CROSS-PAGE hits={len(cross)}')
for h, a, b in cross: print(f'  {h}: [{a[0]} {a[1]}] {a[2]!r} <> [{b[0]} {b[1]}] {b[2]!r}')
print(f'VS-PASS2 hits={len(vs)}')
for h, p, e in vs: print(f'  {h}: [{p[0]} {p[1]}] {p[2]!r} <> [{e[0]}] {e[1]!r}')
sys.exit(1 if cross or vs else 0)
