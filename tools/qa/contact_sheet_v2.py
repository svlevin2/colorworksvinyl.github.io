#!/usr/bin/env python3
"""Pass 1 review contact sheet from shots_v2.mjs output.
Usage: python3 tools/qa/contact_sheet_v2.py [v2Dir] [out.png]"""
import sys
from PIL import Image, ImageDraw
d = sys.argv[1] if len(sys.argv) > 1 else '/workspace/colorworks/website/qa-output/v2'
out = sys.argv[2] if len(sys.argv) > 2 else d + '/contact-sheet-v2.png'
def fit(p, w):
    im = Image.open(p).convert('RGB'); return im.resize((w, int(im.height * w / im.width)))
top = [(f'{n} 1440', fit(f'{d}/{n}-1440.png', 560)) if k == 0 else (f'{n} 390', fit(f'{d}/{n}-390.png', 180))
       for n in ('home-full', 'category-vehicle-graphics') for k in (0, 1)]
crops = [(f'{n} {w}', fit(f'{d}/{n}-{w}.png', 560 if w == 1440 else 180))
         for n in ('header-scrolled', 'who-we-are', 'footer-bar') for w in (1440, 390)]
G = 20; W = G + sum(im.width + G for _, im in top)
H1 = max(im.height for _, im in top) + 40
rows = [crops[i:i + 4] for i in range(0, len(crops), 4)]
H2 = sum(max(im.height for _, im in r) + 40 for r in rows)
sheet = Image.new('RGB', (W, H1 + H2 + G * 2), 'white'); dr = ImageDraw.Draw(sheet)
x = G
for t, im in top: dr.text((x, G), t, fill='black'); sheet.paste(im, (x, G + 16)); x += im.width + G
y = G + H1
for r in rows:
    x = G
    for t, im in r: dr.text((x, y), t, fill='black'); sheet.paste(im, (x, y + 16)); x += im.width + G
    y += max(im.height for _, im in r) + 40
sheet.save(out); print('WROTE', out, sheet.size)
