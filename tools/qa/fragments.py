#!/usr/bin/env python3
"""In-page anchor check: every internal href with #fragment points at an existing id. Exit 1 on any miss."""
import re, glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(ROOT)
PREFIX = '/colorworksvinyl.github.io/'
bad = n = 0
for f in sorted(glob.glob('**/*.html', recursive=True)):
    if f.startswith(('src', 'tools', 'node_modules')): continue
    for h in re.findall(r'href="([^"]*#[^"]+)"', open(f).read()):
        if re.match(r'https?://', h): continue
        path, frag = h.split('#', 1); n += 1
        tgt = path[len(PREFIX):] if path.startswith(PREFIX) else (os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f)
        if tgt in ('', '.') or os.path.isdir(tgt) or path.endswith('/'): tgt = os.path.join(tgt, 'index.html')
        if not os.path.exists(tgt) or f'id="{frag}"' not in open(tgt).read(): bad += 1; print('FAIL', f, h)
print(f'SUMMARY fragments checked={n} broken={bad}'); sys.exit(1 if bad else 0)
