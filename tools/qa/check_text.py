#!/usr/bin/env python3
"""Text and rules check for the built site. Exit 1 on any FAIL.
Checks: dashes, banned words, brand names, prices, phone/email targets, CTA labels, alt text,
one H1, noindex, title/meta length, external resource loads, headline wording."""
import os, re, sys, glob, json
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FAIL, WARN = [], []
DASH = re.compile('[\u2012\u2013\u2014\u2015\u2212]|&[nm]dash;|&#821[12];')
BANNED = [r'\betsy\b', r'\bfree\b', r'\$\s?\d', r'\bwix\b', r'testimonial', r'success stor', r'\bpickup\b', r'\binstall',
          r'\boracal\b', r'\borafol\b', r'\bavery\b', r'\b3m\b', r'\broland\b', r'\bmimaki\b', r'\bhp latex\b', r'\bsiser\b',
          r'\bcricut\b', r'\bepson\b', r'\bsumma\b', r'\bgraphtec\b', r'\barlon\b', r'\bmactac\b', r'\britrama\b', r'\bkpmf\b',
          r'\bhexis\b', r'\bstahls\b', r'\bpermanent\b', r'\bcookie banner\b',
          r'\d{2,5}\s+\w+\s+(street|st\.|road|rd\.|avenue|ave\.|drive|dr\.|lane|ln\.|parkway|pkwy)']
CTA_OK = {'Request a quote', 'Contact us', 'Call 1.833.CWVINYL', 'Email us'}

class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.stack=[]; s.text=[]; s.h=[]; s.imgs=[]; s.links=[]; s.res=[]; s.meta={}; s.title=''; s.cur=None; s.skip=0; s.a=None
    def handle_starttag(s, t, at):
        a = dict(at)
        if t in ('script','style'): s.skip += 1; s.stype = a.get('type')
        if t in ('h1','h2','h3'): s.cur=[t,'']
        if t=='title': s.cur=['title','']
        if t=='img': s.imgs.append(a)
        if t=='a': s.a=[a,'']; s.links.append(s.a)
        if t=='meta' and a.get('name'): s.meta[a['name']]=a.get('content','')
        if t in ('img','source','script') and (a.get('src') or a.get('srcset')): s.res.append(a.get('src') or a.get('srcset'))
        if t=='link' and a.get('rel') in ('stylesheet','preload','icon','apple-touch-icon','manifest'): s.res.append(a.get('href'))
    def handle_endtag(s, t):
        if t in ('script','style'): s.skip -= 1
        if s.cur and t==s.cur[0]:
            if t=='title': s.title=s.cur[1].strip()
            else: s.h.append((t, ' '.join(s.cur[1].split())))
            s.cur=None
        if t=='a': s.a=None
    def handle_data(s, d):
        if s.skip: return
        s.text.append(d)
        if s.cur: s.cur[1]+=d
        if s.a is not None: s.a[1]+=d

def check(path):
    rel = os.path.relpath(path, ROOT); raw = open(path, encoding='utf-8').read()
    for m in DASH.finditer(raw): FAIL.append(f'{rel}: dash character at offset {m.start()}')
    if not path.endswith('.html') or '/src/' in path: return
    p = P(); p.feed(raw)
    vis = ' '.join(' '.join(p.text).split())
    allt = vis + ' ' + p.title + ' ' + ' '.join(p.meta.values()) + ' ' + ' '.join(i.get('alt','') for i in p.imgs)
    for b in BANNED:
        for m in re.finditer(b, allt, re.I): FAIL.append(f'{rel}: banned "{m.group(0)}"')
    h1 = [h for h in p.h if h[0]=='h1']
    if len(h1)!=1: FAIL.append(f'{rel}: {len(h1)} h1')
    for t, h in p.h:
        if re.search(r'made in lake zurich', h, re.I): FAIL.append(f'{rel}: "made in Lake Zurich" in {t}: {h}')
    if 'noindex' not in p.meta.get('robots',''): FAIL.append(f'{rel}: missing noindex')
    tl, dl = len(p.title), len(p.meta.get('description',''))
    if not (30 <= tl <= 60): WARN.append(f'{rel}: title {tl} chars')
    if not (120 <= dl <= 160): WARN.append(f'{rel}: meta description {dl} chars')
    for i in p.imgs:
        if 'alt' not in i: FAIL.append(f'{rel}: img without alt {i.get("src")}')
        elif not i['alt'].strip() and i.get('aria-hidden')!='true' and i.get('role')!='presentation': WARN.append(f'{rel}: empty alt {i.get("src")}')
    for a, txt in p.links:
        h = a.get('href',''); txt=' '.join(txt.split())
        if h.startswith('tel:') and h!='tel:+18332984695': FAIL.append(f'{rel}: bad tel {h}')
        if h.startswith('mailto:') and h.split('?')[0]!='mailto:info@colorworksvinyl.com': FAIL.append(f'{rel}: bad mailto {h}')
        cls = a.get('class','')
        if ('btn' in cls.split() or 'btn-link' in cls) and h.startswith(('mailto:','tel:')) and txt not in CTA_OK: FAIL.append(f'{rel}: CTA label "{txt}"')
        if re.match(r'https?://', h) and 'github' not in h and 'w3.org' not in h: WARN.append(f'{rel}: external link {h}')
    for r in p.res:
        if r and re.search(r'(^|\s|,)(https?:)?//', r): FAIL.append(f'{rel}: external resource {r}')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S):
        try: json.loads(m.group(1))
        except Exception as e: FAIL.append(f'{rel}: bad JSON-LD {e}')
    return rel, len(vis.split()), p.title, tl, dl

if __name__ == '__main__':
    rows = []
    files = [f for f in glob.glob(os.path.join(ROOT, '**/*'), recursive=True)
             if os.path.isfile(f) and re.search(r'\.(html|css|js|py|mjs|md|txt|xml|json|svg|sh)$', f) and '/node_modules/' not in f and '/.git/' not in f and '/src/icons/' not in f]
    for f in sorted(files):
        r = check(f)
        if r: rows.append(r)
    for r in rows: print(f'PAGE {r[0]}: words={r[1]} title({r[3]})="{r[2]}" meta={r[4]}')
    for w in WARN: print('WARN', w)
    for x in FAIL: print('FAIL', x)
    print(f'SUMMARY files={len(files)} pages={len(rows)} fails={len(FAIL)} warns={len(WARN)}')
    sys.exit(1 if FAIL else 0)
