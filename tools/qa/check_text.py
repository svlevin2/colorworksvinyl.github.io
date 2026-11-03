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
    # v2 copy rules (Steven, Nov 3 2026)
    WORD = 'pro' + 'of'  # split so this script itself stays clean
    # Allowed ONLY inside the How it works steps 2 and 3 (Steven, Nov 3 2026 12:37 AM CT); anywhere else fails.
    hits = allowed = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '**/*'), recursive=True)):
        if not os.path.isfile(f) or '/.git/' in f or '/node_modules/' in f or re.search(r'\.(woff2|webp|png|jpg|ico|gz)$', f): continue
        raw = open(f, encoding='utf-8', errors='ignore').read()
        spans = [(m.start(), m.end()) for m in re.finditer(r'<li class="step[^"]*"[^>]*>.*?</li>', raw, re.S) if re.search(r'Step [23]<', m.group(0))]
        for m in re.finditer(WORD, raw, re.I):
            ln = raw.count('\n', 0, m.start()) + 1
            line = ' '.join(re.sub(r'<[^>]+>|\{\{[^}]+\}\}', ' ', raw.splitlines()[ln - 1]).split())
            ok = any(x <= m.start() < y for x, y in spans)
            print(f'{WORD.upper()}-HIT {"allowed" if ok else "FAIL"} {os.path.relpath(f, ROOT)}:{ln}: {line}')
            if ok: allowed += 1
            else: hits += 1; FAIL.append(f'{os.path.relpath(f, ROOT)}:{ln}: "{WORD}" outside How it works steps 2-3')
    print(f'CHECK no-{WORD} outside-steps={hits} allowed-in-steps={allowed}')
    home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    a = home.find('id="about"'); sec = home[a:home.find('</section>', a)] if a > 0 else ''
    txt = lambda h: ' '.join(re.sub(r'<[^>]+>', '', h).split()).replace('&#x27;', "'").replace('&#39;', "'")
    got = {'heading': txt((re.search(r'<h2[^>]*id="about-title"[^>]*>(.*?)</h2>', sec, re.S) or [None, ''])[1]),
           'subhead': txt((re.search(r'<p class="subhead">(.*?)</p>', sec, re.S) or [None, ''])[1])}
    ps = [txt(x) for x in re.findall(r'<p>(.*?)</p>', sec, re.S)]
    got['p1'], got['p2'] = (ps + ['', ''])[:2]
    WANT = {'heading': 'Who We Are', 'subhead': 'Dedicated to Excellence',
            'p1': "ColorWorks Vinyl is a vinyl print-and-cut shop in Lake Zurich, IL, specializing in decals, stickers, business signage, event graphics and custom vinyl printing. We're committed to vibrant color, precise cuts and work that makes a lasting impression.",
            'p2': "We're proud to serve local businesses with storefront and window graphics, store hours decals, logo decals and signage that help them stand out. Tell us what you need, and our team will work to bring your idea to reality."}
    for k, v in WANT.items():
        ok = got[k] == v
        print(f'CHECK who-we-are {k} exact={"PASS" if ok else "FAIL"}')
        if not ok: FAIL.append(f'index.html: Who We Are {k} mismatch: {got[k]!r}')
    if re.search(r'eyebrow[^>]*>\s*who we are', sec, re.I): FAIL.append('index.html: doubled WHO WE ARE eyebrow')
    # Contact subline (Steven, Nov 3 2026 12:22 AM CT)
    RBE = 'reply by ' + 'email'; SUB = 'Tell us what you need and let our team do the rest.'
    rbe = 0
    for f in glob.glob(os.path.join(ROOT, '**/*'), recursive=True):
        if not os.path.isfile(f) or '/.git/' in f or '/node_modules/' in f or re.search(r'\.(woff2|webp|png|jpg|ico|gz)$', f): continue
        for m in re.finditer(RBE, open(f, encoding='utf-8', errors='ignore').read(), re.I):
            rbe += 1; FAIL.append(f'{os.path.relpath(f, ROOT)}: "{RBE}" at offset {m.start()}')
    print(f'CHECK no-reply-by-email hits={rbe}')
    c = home.find('id="contact"'); csec = home[c:home.find('</section>', c)] if c > 0 else ''
    lead = txt((re.search(r'<p class="lead">(.*?)</p>', csec, re.S) or [None, ''])[1])
    print(f'CHECK contact-subline home exact={"PASS" if lead == SUB else "FAIL"}')
    if lead != SUB: FAIL.append(f'index.html: contact subline mismatch: {lead!r}')
    nb = bad_b = 0
    for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True) + [os.path.join(ROOT, '404.html')]:
        if '/node_modules/' in f or '/.git/' in f: continue
        raw = open(f, encoding='utf-8').read(); b = raw.find('id="band-title"')
        if b < 0: continue
        nb += 1; bl = txt((re.search(r'<p class="lead">(.*?)</p>', raw[b:], re.S) or [None, ''])[1])
        if bl != SUB: bad_b += 1; FAIL.append(f'{os.path.relpath(f, ROOT)}: band subline mismatch: {bl!r}')
    print(f'CHECK contact-subline band pages={nb} mismatches={bad_b}')
    # Our Services subline (Steven, Nov 3 2026 12:36 AM CT), exact incl. serial commas; old line must be gone
    SVC_SUB = 'Custom vinyl decals, stickers, and signage, made to order, for businesses, events, and everything in between.'
    OLD_SVC = 'Custom vinyl made to order in Lake Zurich, IL, for local businesses and events.'
    s0 = home.find('id="services"'); ssec = home[s0:home.find('</section>', s0)] if s0 > 0 else ''
    sl = txt((re.search(r'<p class="lead">(.*?)</p>', ssec, re.S) or [None, ''])[1])
    print(f'CHECK services-subline home exact={"PASS" if sl == SVC_SUB else "FAIL"}')
    if sl != SVC_SUB: FAIL.append(f'index.html: services subline mismatch: {sl!r}')
    old_hits = 0
    for f in glob.glob(os.path.join(ROOT, '**/*'), recursive=True):
        if not os.path.isfile(f) or '/.git/' in f or '/node_modules/' in f or re.search(r'\.(woff2|webp|png|jpg|ico|gz)$', f): continue
        n_ = open(f, encoding='utf-8', errors='ignore').read().count(OLD_SVC)
        if n_ and not f.endswith('check_text.py'): old_hits += n_; FAIL.append(f'{os.path.relpath(f, ROOT)}: old services subline x{n_}')
    print(f'CHECK old-services-subline hits={old_hits}')
    # How it works step 2 title (Steven 12:37 AM CT), exact on every page with the steps
    ns = bad_s = 0
    for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
        if '/node_modules/' in f or '/.git/' in f: continue
        m = re.search(r'Step 2</span><h3>(.*?)</h3>', open(f, encoding='utf-8').read())
        if not m: continue
        ns += 1
        if m.group(1) != 'We send a quote and a digital ' + WORD: bad_s += 1; FAIL.append(f'{os.path.relpath(f, ROOT)}: step 2 title mismatch: {m.group(1)!r}')
    print(f'CHECK step2-title exact pages={ns} mismatches={bad_s}')
    # Step 3 title (Steven 12:38 AM CT): exactly "Made to Order"; "Made and shipped" must not be used as a title/heading anywhere
    n3 = bad3 = old_t = 0; body_uses = []
    for f in glob.glob(os.path.join(ROOT, '**/*'), recursive=True):
        if not os.path.isfile(f) or '/.git/' in f or '/node_modules/' in f or not re.search(r'\.(html|py|md)$', f) or f.endswith('check_text.py'): continue
        raw = open(f, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'Step 3</span><h3>(.*?)</h3>', raw):
            n3 += 1
            if m.group(1) != 'Made to Order': bad3 += 1; FAIL.append(f'{os.path.relpath(f, ROOT)}: step 3 title mismatch: {m.group(1)!r}')
        for m in re.finditer(r'<(h[1-6]|strong|span|dt|summary|button)[^>]*>\s*Made and shipped\.?\s*</\1>', raw, re.I):
            old_t += 1; FAIL.append(f'{os.path.relpath(f, ROOT)}: old title "Made and shipped"')
        if f.endswith('.html') and '/src/' not in f: body_uses += [os.path.relpath(f, ROOT)] * raw.count('Made and shipped in 1-2')
    print(f'CHECK step3-title exact={n3 - bad3}/{n3} old-title-hits={old_t}')
    print(f'NOTE "Made and shipped in 1-2 business days..." body sentences kept (step 3 body, ticks, FAQ, trust strip): {len(body_uses)} in built pages')
    # Old Wix template phrase: allowed only once, as the Who We Are subhead (Steven asked for it, Nov 3 2026)
    for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
        if '/node_modules/' in f or '/.git/' in f: continue
        raw = open(f, encoding='utf-8').read(); n = len(re.findall('dedicated to excellence', raw, re.I))
        allowed = 1 if os.path.relpath(f, ROOT) in ('index.html', os.path.join('src', 'pages', '00-home.html')) and 'dedicated to excellence' in sec.lower() else 0
        if n > allowed: FAIL.append(f'{os.path.relpath(f, ROOT)}: template phrase "Dedicated to Excellence" outside Who We Are')
    # Vinyl-only scope guard (Steven, Nov 3 2026 12:31 AM CT): visible text, title, meta, alt and JSON-LD of built pages
    NONV = re.compile(r'poster|paper|trade[- ]show|channel letter|lightbox|light box|monument|metal|acrylic|\blabel', re.I)
    nv = nv_legal = 0
    for f in sorted(glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)):
        if '/node_modules/' in f or '/.git/' in f or '/src/' in f or '/qa-' in f: continue
        rel = os.path.relpath(f, ROOT); raw = open(f, encoding='utf-8').read(); q = P(); q.feed(raw)
        t = ' '.join(q.text) + ' ' + q.title + ' ' + ' '.join(q.meta.values()) + ' ' + ' '.join(i.get('alt','') for i in q.imgs) + ' ' + ' '.join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S))
        for m in NONV.finditer(t):
            ctx = ' '.join(t[max(0, m.start()-40):m.end()+40].split())
            if rel.split(os.sep)[0] in ('privacy', 'terms', 'accessibility'): nv_legal += 1; print(f'NOTE non-vinyl word in legal page {rel}: "{m.group(0)}" ... {ctx}')
            else: nv += 1; FAIL.append(f'{rel}: non-vinyl word "{m.group(0)}" ... {ctx}')
    print(f'CHECK vinyl-only hits={nv} legal-notes={nv_legal}')
    # Legal fix (Steven, Nov 3 2026 12:39-12:40 AM CT): no leftover notes in any built page, case-insensitive
    LEFT = {'confirm': re.compile('confirm', re.I), '[[': re.compile(re.escape('[[')), 'TBD': re.compile('tbd', re.I), 'Wix': re.compile('wix', re.I)}
    lc = {k: 0 for k in LEFT}
    for f in sorted(glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True)):
        if '/node_modules/' in f or '/.git/' in f or '/src/' in f or '/qa-' in f or '/tools/' in f: continue
        rel = os.path.relpath(f, ROOT); raw = open(f, encoding='utf-8').read()
        for k, rx in LEFT.items():
            for m in rx.finditer(raw):
                lc[k] += 1; ln = raw.count('\n', 0, m.start()) + 1
                FAIL.append(f'{rel}:{ln}: leftover "{k}"')
    print('CHECK leftover-notes built pages ' + ' '.join(f'{k}={v}' for k, v in lc.items()))
    # Category template: one process section only, no near-duplicate headings, eyebrows never repeat their heading
    import html as _h
    norm = lambda t: re.sub(r'[^a-z ]', '', _h.unescape(t).lower().replace('&', ' and ')).split()
    stop = {'vinyl', 'and', 'for', 'the', 'custom', 'decals', 'graphics'}
    cn = dup_h = eb = hw = 0
    for f in sorted(glob.glob(os.path.join(ROOT, 'services/*/index.html'))):
        rel = os.path.relpath(f, ROOT); raw = open(f, encoding='utf-8').read(); cn += 1
        if re.search(r'How we work', raw): hw += 1; FAIL.append(f'{rel}: "How we work" block still present')
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.S).group(1)
        for h2 in re.findall(r'<h2[^>]*>(.*?)</h2>', raw, re.S):
            a, b = set(norm(h1)) - stop, set(norm(h2)) - stop
            if a and b and (a <= b or b <= a): dup_h += 1; FAIL.append(f'{rel}: H2 "{h2}" near-duplicates H1 "{h1}"')
        for e, h in re.findall(r'class="eyebrow">([^<]*)</p>\s*<h2[^>]*>([^<]*)', raw):
            if set(norm(e)) & (set(norm(h)) | set(norm(h1))) - stop: eb += 1; FAIL.append(f'{rel}: eyebrow "{e}" repeats heading "{h}"')
        if raw.count('class="steps"') != 1: FAIL.append(f'{rel}: expected exactly one steps list')
    print(f'CHECK category-template pages={cn} how-we-work={hw} h1-h2-near-dup={dup_h} eyebrow-repeats={eb}')
    for r in rows: print(f'PAGE {r[0]}: words={r[1]} title({r[3]})="{r[2]}" meta={r[4]}')
    for w in WARN: print('WARN', w)
    for x in FAIL: print('FAIL', x)
    print(f'SUMMARY files={len(files)} pages={len(rows)} fails={len(FAIL)} warns={len(WARN)}')
    sys.exit(1 if FAIL else 0)
