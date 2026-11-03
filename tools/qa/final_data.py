"""Final QA data tables for the 27 sitemap URLs: business-days grep, Fast turn-around hits, breadcrumb + JSON-LD check.
Phrase BD is built by split so the repo text scan does not hit this file. Usage: python3 tools/qa/final_data.py > <out.md>"""
import re, json, html, glob, os, sys
BD = 'business ' + 'days'
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)
BASE = 'https://svlevin2.github.io/colorworksvinyl.github.io/'
urls = re.findall(r'<loc>(.*?)</loc>', open('sitemap.xml').read())
def path(u):
    r = u[len(BASE):]; return (r + 'index.html') if (r == '' or r.endswith('/')) else r
def txt(s): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()
files = sorted(f for f in glob.glob('**/*', recursive=True) if os.path.isfile(f) and f.split('/')[0] not in ('src','tools','node_modules','.git') and f.endswith(('.html','.xml','.txt','.json','.js','.css','.md')))
out = []; fails = 0
out.append(f'## 1. "{BD}" grep (built site, all text files)\n')
bd = []
for f in files:
    for i, l in enumerate(open(f, errors='ignore'), 1):
        for m in re.finditer(BD, l):
            bd.append((f, i, l[max(0, m.start()-90):m.end()+60].strip()))
for f, i, c in bd: out.append(f'- `{f}:{i}` ... {html.escape(c)} ...')
inld = sum(1 for f,i,c in bd if '"text"' in c or 'acceptedAnswer' in c)
okf = all(f in ('faq/index.html','README.md') for f,_,_ in bd)
out.append(f'\nHits: {len(bd)}; files: {sorted(set(f for f,_,_ in bd))}. Only FAQ answer + its JSON-LD: {"PASS" if okf else "FAIL"}\n')
if not okf: fails += 1
out.append('## 2. "Fast turn-around" hits (built pages)\n')
out.append('| # | File:line | Context |\n|---|---|---|')
n = 0
for f in files:
    if not f.endswith('.html'): continue
    src = open(f, errors='ignore').read()
    for m in re.finditer(r'Fast turn-around', src):
        n += 1; line = src.count('\n', 0, m.start()) + 1
        ctx = txt(src[max(0, m.start()-160):m.end()+20]).split('>')[-1]
        where = 'trust strip' if '</span>Fast turn-around</li>' in src[m.start()-7:m.end()+5] else ('step 3 body' if 'Made to Order' in src[max(0,m.start()-400):m.start()] else 'other')
        if where == 'other': fails += 1
        out.append(f'| {n} | `{f}:{line}` | {where}: "{txt(src[m.start():m.end()+1])}" |')
out.append(f'\nTotal: {n}\n')
home = open('index.html').read()
NAV = {}
for h, t in re.findall(r'<a href="([^"#]+/)">([^<]+)</a>', home): NAV.setdefault(BASE + h, html.unescape(t))
out.append('Name rule: JSON-LD name = H1, or = the page\'s site nav label (the name the home nav, footer and child breadcrumbs use). Pages that use the nav label are marked NAV.\n')
out.append('## 3. Breadcrumb + JSON-LD per page (27 sitemap URLs)\n')
out.append('| Page | H1 | JSON-LD types | JSON valid | Service name = H1 / url = canonical | Breadcrumb last = H1 + canonical; visible crumb matches | FAQPage Qs = visible | Result |\n|---|---|---|---|---|---|---|---|')
for u in urls:
    f = path(u); s = open(f).read()
    h1 = txt(re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S).group(1))
    can = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    ok = True; objs = []
    for b in blocks:
        try: objs.append(json.loads(b))
        except Exception: ok = False
    types = [o.get('@type') for o in objs]
    res = ok and can == u
    navl = NAV.get(u)
    def nm(x): return 'H1' if x == h1 else ('NAV' if x == navl else None)
    svc = next((o for o in objs if o.get('@type') == 'Service'), None)
    if svc: k = nm(svc['name']); c1 = bool(k) and svc['url'] == can; res &= c1; c1 = f'PASS ({k}: {svc["name"]})' if c1 else f'FAIL ({svc["name"]} / {svc["url"]})'
    else: c1 = '-'
    bl = next((o for o in objs if o.get('@type') == 'BreadcrumbList'), None)
    if bl:
        last = bl['itemListElement'][-1]
        vis = re.search(r'<nav[^>]*class="[^"]*breadcrumb[^"]*"[^>]*>(.*?)</nav>', s, re.S)
        visok = True
        if vis:
            vt = txt(vis.group(1)); visok = all(txt(e['name']) in vt for e in bl['itemListElement'][:-1][-1:])
        k2 = nm(last['name']); c2 = bool(k2) and last['item'] == can and [e['position'] for e in bl['itemListElement']] == list(range(1, len(bl['itemListElement'])+1)) and visok
        res &= c2; c2 = (f'PASS ({k2}, {len(bl["itemListElement"])} levels' + (', visible back link' if vis else '') + ')') if c2 else f'FAIL ({last["name"]} / {last["item"]})'
    else: c2 = '-'
    fq = next((o for o in objs if o.get('@type') == 'FAQPage'), None)
    if fq:
        qs = [q['name'] for q in fq['mainEntity']]; c3 = all(html.escape(q, quote=False) in s or q in html.unescape(s) for q in qs)
        res &= c3; c3 = f'{"PASS" if c3 else "FAIL"} ({len(qs)} Qs)'
    else: c3 = '-'
    if not res: fails += 1
    out.append(f'| `{u[len(BASE)-1:]}` | {h1} | {", ".join(types) or "none"} | {"PASS" if ok else "FAIL"} ({len(blocks)}) | {c1} | {c2} | {c3} | {"PASS" if res else "FAIL"} |')
out.append(f'\nSUMMARY pages={len(urls)} fails={fails}')
print('\n'.join(out))
print(f'SUMMARY final-data pages={len(urls)} BD-hits={len(bd)} fast-turn-around={n} fails={fails}', file=sys.stderr)
