#!/usr/bin/env python3
"""Pass 2 contact sheet from shots_p2.mjs output: 4 pages at 1440 + 390 (Chromium), then all 16 product pages at 390 (WebKit).
Usage: python3 tools/qa/contact_sheet_p2.py [p2Dir] [out.png]"""
import sys, os
from PIL import Image, ImageDraw
d = sys.argv[1] if len(sys.argv) > 1 else '/workspace/colorworks/website/qa-output/p2'
out = sys.argv[2] if len(sys.argv) > 2 else d + '/contact-sheet-p2.png'
def thumb(p, w, h):
    im = Image.open(p).convert('RGB'); im = im.resize((w, int(im.height * w / im.width)))
    return im.crop((0, 0, w, min(h, im.height)))
G, L = 16, 22
r1 = []
for n in ('home', 'category-vehicle-graphics', 'product-store-hours-decals', 'product-vehicle-lettering'):
    r1 += [(f'{n} 1440', thumb(f'{d}/{n}-1440.png', 420, 1100)), (f'{n} 390', thumb(f'{d}/{n}-390.png', 150, 1100))]
wk = sorted(os.listdir(d + '/webkit-390'))
r2 = [('webkit 390 ' + f[:-4], thumb(f'{d}/webkit-390/{f}', 210, 900)) for f in wk]
rows = [r1[:4], r1[4:], r2[:8], r2[8:]]
W = max(G + sum(im.width + G for _, im in r) for r in rows)
H = sum(max(im.height for _, im in r) + L + G for r in rows) + G
sheet = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sheet); y = G
for r in rows:
    x = G
    for lab, im in r:
        dr.text((x, y), lab, fill='black'); sheet.paste(im, (x, y + L)); dr.rectangle((x - 1, y + L - 1, x + im.width, y + L + im.height), outline='#bbb'); x += im.width + G
    y += max(im.height for _, im in r) + L + G
sheet.save(out); print(out, sheet.size, 'webkit pages', len(wk))
