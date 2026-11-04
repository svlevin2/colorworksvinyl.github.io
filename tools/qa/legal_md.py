#!/usr/bin/env python3
"""Write the legal pages' full text (prose div) as markdown. Usage: python3 tools/qa/legal_md.py <out.md>"""
import sys, re
from bs4 import BeautifulSoup
from markdownify import markdownify as md
out = sys.argv[1]
parts = ['# ColorWorks Vinyl - legal pages, full text (Pass 1 draft)\n\nGenerated from the built pages in /workspace/colorworks/website/gh-pages-site (privacy/, terms/, accessibility/) on November 3, 2026. Links are kept as on the site; relative links point inside the site.\n']
for p in ['privacy', 'terms', 'accessibility']:
    s = BeautifulSoup(open(f'{p}/index.html', encoding='utf-8').read(), 'html.parser')
    d = s.select_one('.prose')
    for x in d.select('svg'): x.decompose()
    t = md(str(d), heading_style='ATX', bullets='-')
    t = re.sub(r'\n{3,}', '\n\n', t).strip()
    parts.append(f'---\n\nPage: {p}/\n\n{t}\n')
open(out, 'w', encoding='utf-8').write('\n'.join(parts)); print(out)
