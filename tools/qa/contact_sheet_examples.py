#!/usr/bin/env python3
"""Examples contact sheets (repo build, EXAMPLES_APPROVED = True) from shots_examples.mjs: one sheet per width, 16 pages.
Usage: python3 tools/qa/contact_sheet_examples.py [dir]"""
import sys, os
from PIL import Image, ImageDraw
d = sys.argv[1] if len(sys.argv) > 1 else '/workspace/colorworks/website/qa-output/p2/examples'
slugs = sorted({f.rsplit('-', 1)[0] for f in os.listdir(d) if f.endswith(('-1440.png', '-390.png'))})
for w, tw, cols in ((1440, 560, 4), (390, 220, 8)):
    ims = []
    for s in slugs:
        im = Image.open(f'{d}/{s}-{w}.png').convert('RGB'); ims.append((s, im.resize((tw, int(im.height * tw / im.width)))))
    G, L = 16, 20; rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    W = G + cols * (tw + G); H = G + sum(max(im.height for _, im in r) + L + G for r in rows)
    sh = Image.new('RGB', (W, H), 'white'); dr = ImageDraw.Draw(sh); y = G
    for r in rows:
        x = G
        for s, im in r:
            dr.text((x, y), f'{s} {w} (repo build)', fill='black'); sh.paste(im, (x, y + L)); dr.rectangle((x - 1, y + L - 1, x + im.width, y + L + im.height), outline='#bbb'); x += tw + G
        y += max(im.height for _, im in r) + L + G
    o = f'{os.path.dirname(d)}/contact-sheet-examples-{w}.png'; sh.save(o); print(o, sh.size, len(ims))
