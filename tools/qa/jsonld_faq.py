#!/usr/bin/env python3
"""Pass 3: FAQPage JSON-LD must match the visible FAQ (.prod-faq .qa h3/p) exactly, in order; questions unique across pages."""
import re, glob, json, os, sys
from html import unescape
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bad, n, qs = 0, 0, {}
for f in sorted(glob.glob(os.path.join(ROOT, 'services/*/index.html'))):
    h = open(f, encoding='utf-8').read(); pg = os.path.basename(os.path.dirname(f))
    vis = [(unescape(q), unescape(a)) for q, a in re.findall(r'<div class="qa"><h3>(.*?)</h3><p>(.*?)</p></div>', h)]
    ld = []
    for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        d = json.loads(s)
        for x in (d if isinstance(d, list) else d.get('@graph', [d])):
            if x.get('@type') == 'FAQPage': ld += [(e['name'], e['acceptedAnswer']['text']) for e in x['mainEntity']]
    if vis or ld:
        n += 1; ok = vis == ld
        print(f'{pg}: visible={len(vis)} jsonld={len(ld)} {"MATCH" if ok else "MISMATCH"}'); bad += not ok
    for q, _ in vis: qs.setdefault(q.lower(), []).append(pg)
dq = {q: p for q, p in qs.items() if len(p) > 1}
print(f'pages with FAQ={n} mismatches={bad} duplicate questions across pages={len(dq)}', dq or '')
sys.exit(1 if bad or dq else 0)
