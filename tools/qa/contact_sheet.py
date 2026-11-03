#!/usr/bin/env python3
"""Contact sheet from shots/*.png: one row per page, 1440 and 390 side by side, tops cropped to a fixed height.
Usage: python3 tools/qa/contact_sheet.py <shotsDir> <out.png> [cropHeightAt1440]"""
import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; out = sys.argv[2]; crop = int(sys.argv[3]) if len(sys.argv) > 3 else 2600
pages = sorted({os.path.basename(f).rsplit('-', 1)[0] for f in glob.glob(d + '/*-1440.png')}, key=lambda n: (n != 'home', n))
SW, MW, H = 480, 160, int(crop / 3)
sheet = Image.new('RGB', (40 + (SW + MW + 60) * 3, 40 + len(pages[:]) // 3 * 0 + ((len(pages) + 2) // 3) * (H + 70)), 'white')
dr = ImageDraw.Draw(sheet)
for i, n in enumerate(pages):
    x = 20 + (i % 3) * (SW + MW + 60); y = 20 + (i // 3) * (H + 70)
    dr.text((x, y), n, fill='black')
    a = Image.open(f'{d}/{n}-1440.png'); a = a.crop((0, 0, a.width, min(a.height, crop))); a = a.resize((SW, int(a.height * SW / a.width)))
    b = Image.open(f'{d}/{n}-390.png'); b = b.crop((0, 0, b.width, min(b.height, int(crop * 390 / 1440 * 2.2)))); b = b.resize((MW, int(b.height * MW / b.width)))
    sheet.paste(a, (x, y + 18)); sheet.paste(b, (x + SW + 16, y + 18))
sheet.save(out); print(out, sheet.size, len(pages), 'pages')
