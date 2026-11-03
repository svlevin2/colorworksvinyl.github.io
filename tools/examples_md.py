#!/usr/bin/env python3
"""Writes the COO examples draft (markdown) from src/data/examples.py so the draft and the build never drift."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, 'src/data'))
from examples import EXAMPLES
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/box/shared/colorworks/website/2026-11-03_pass2-examples-draft.md'
L = ['# Pass 2 - product page Examples (APPROVED by COO - CW 2026-11-03 10:37 CT, text as in e3d634c, shown on the site)',
     '2026-11-03 10:06 CT - Web Developer Bot. 16 pages x 5 examples, each a title plus 1-2 plain sentences. Flag EXAMPLES_APPROVED = True in src/data/examples.py since the 10:37 CT approval. Pages 14-16 lists are as approved in 2026-11-03_pass2-three-new-pages-draft.md (09:14 CT). Vinyl only: no prices, materials, brands, sizes, lifespan, durability, installation or turnaround claims.', '',
     '## Change log (CT)',
     '- 2026-11-03 10:37 CT: COO - CW APPROVED the text as written in e3d634c; flag on, examples live in the local build (not pushed).',
     '- 2026-11-03 10:30 CT COO revisions: every body now says what the piece is and what it is for (all 80 checked); wedding-monograms 4 is now the Just Married getaway car decal; page 14 example 2 body "Vinyl arrows and lettering"; storefront-lettering 5 retitled "A short tagline on the door glass or the window above the door"; wall-murals 2 now "we make the vinyl mural to fit your wall" (no design promise).',
     '- 2026-11-03 10:06 CT: first full draft (80 examples).', '',
     'Photos (Design Bot, one per example, same style): ex-<slug>-<n>, 4:3 1200x900, digital mockup, no readable fake text. Gradient icon art until each lands. Shots from the repo build: /workspace/colorworks/website/qa-output/p2/examples/ and contact-sheet-examples-{1440,390}.png.', '']
for i, (slug, ex) in enumerate(EXAMPLES.items(), 1):
    L.append(f'## {i}. /services/{slug}/')
    for n, (t, b) in enumerate(ex, 1):
        L.append(f'{n}. **{t}** - {b} (photo ex-{slug}-{n})')
    L.append('')
L += ['## Notes',
      '- wall-murals keeps its 2 approved "What it\'s for" points; these are examples, a separate list.',
      '- Wayfinding: no exit or ADA signs (regulated, not vinyl decals). Banners: table banner only, no stands or displays.',
      '- Page 14 example 2 title is the 09:13 CT wording, verbatim.']
open(OUT, 'w').write('\n'.join(L) + '\n'); print(OUT, os.path.getsize(OUT), 'bytes')
