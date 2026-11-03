#!/usr/bin/env python3
"""Merge devices-*.json into the device and browser QA markdown table."""
import json, glob, sys, os, datetime
d = sys.argv[1]; outmd = sys.argv[2]
cfgs, res = {}, []
for f in sorted(glob.glob(os.path.join(d, 'devices-*.json'))):
    j = json.load(open(f)); [cfgs.setdefault(c['id'], c) for c in j['configs']]; res += j['results']
order = ['chrome-desktop', 'chrome-android', 'safari-ios', 'safari-desktop', 'firefox']
pages = []
for r in res:
    if r.get('page') and r['page'] not in pages and r['page'] != '(all)': pages.append(r['page'])
L = ['# ColorWorks Vinyl - device and browser QA (Pass 1, local build)', '',
     f'Run: November 3, 2026 (America/Chicago), script tools/qa/devices.mjs (Playwright {os.environ.get("PWV","")}) against the local build at http://localhost:8765/colorworksvinyl.github.io/. Not deployed.', '',
     '**Honest labels.** These are browser engines with emulated screen sizes, touch and device pixel ratio. They are not real phones, tablets or branded browsers. "Chrome Android" is Chromium with Pixel-style emulation; "Safari iOS" is Playwright WebKit with iPhone emulation; "Safari desktop" is Playwright WebKit; Edge was not installed (no msedge channel), so Edge is covered only as "Chromium engine (same as Edge)" by the Chrome desktop runs. tel and mailto links: href verified (exact href, visible text, plain anchors that page script does not block); no call or email was placed.', '',
     '**Checks per page and viewport:** no horizontal scroll (scrollWidth <= clientWidth); tap targets >= 44x44 on phone sizes (min side <= 430; inline links inside a sentence exempt per WCAG 2.5.8; card links measured by the card); body text >= 16px on phone sizes (short labels .eyebrow, .step-num, .tile-label exempt); no text overlap, clipping or text past the screen edge; cropped images use object-fit (not stretched); mobile nav opens, traps Tab and Shift+Tab, closes on Escape (focus back on the button) and on link tap; in-page anchors not covered by the sticky header; tel/mailto hrefs; no page errors, cookies or external requests. Moved pages (business-signage/, stickers-decals/, events/) checked for the redirect only.', '',
     'Hero and photo crops were also checked by eye on the WebKit iPhone 390x844 full-page shots listed below.', '']
tot = sum(1 for r in res if 'vp' in r); bad = [r for r in res if r.get('fails') or r.get('error')]
L += [f'**Summary:** {tot} page loads across {len(cfgs)} engine setups, {len(bad)} with a failure.', '']
for cid in order:
    if cid not in cfgs: continue
    c = cfgs[cid]; vps = c['vps']
    L += [f'## {c["label"]}', '', '| Page | ' + ' | '.join(vps) + ' |', '|---|' + '---|' * len(vps)]
    for p in pages:
        row = []
        for v in vps:
            r = [x for x in res if x.get('cfg') == cid and x.get('vp') == v and x.get('page') == p]
            row.append('-' if not r else ('FAIL' if r[0]['fails'] else 'PASS'))
        L.append(f'| {p} | ' + ' | '.join(row) + ' |')
    ext = [x for x in res if x.get('cfg') == cid and x.get('page') == '(all)']
    err = [x for x in res if x.get('cfg') == cid and x.get('error')]
    L += ['', f'External requests: {"none" if not ext else ext}. ' + (f'Launch error: {err[0]["error"]}' if err else ''), '']
if bad:
    L += ['## Failures', '']
    for r in bad: L.append(f'- {r.get("cfg")} {r.get("vp","")} {r.get("page","")}: {"; ".join(r.get("fails") or [r.get("error","")])}')
    L.append('')
shots = sorted(glob.glob(os.path.join(d, 'webkit-iphone-390', '*.png')))
L += ['## WebKit iPhone 390x844 full-page screenshots', ''] + [f'- {s}' for s in shots] + ['']
open(outmd, 'w').write('\n'.join(L))
print(f'WROTE {outmd} loads={tot} fails={len(bad)} shots={len(shots)}')
