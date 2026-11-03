#!/usr/bin/env python3
"""Live (or local) deploy check under the site subpath.
Usage: live_check.py [BASE]  (default: the github.io project URL)
Checks: page status codes, own 404 for a missing path, every href/src/srcset/og:image/
preload/favicon resolves (200) and stays under BASE, canonical and og:url match the page,
noindex meta, sitemap URLs return 200 and match the canonicals, robots Disallow-all,
no third-party resource URLs."""
import re, sys, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
BASE = sys.argv[1] if len(sys.argv) > 1 else "https://svlevin2.github.io/colorworksvinyl.github.io/"
PAGES = ["", "services/indoor-wall-graphics/", "services/storefront-signage/", "services/vehicle-graphics/", "services/banners-large-format/", "services/decals-stickers/", "services/event-decals/", "faq/", "privacy/", "terms/", "accessibility/"]
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "cw-qa"}), timeout=30)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.meta={}; s.canon=None
    def handle_starttag(s, t, a):
        a = dict(a)
        for k in ("href", "src"):
            if a.get(k): s.refs.append((t, a[k]))
        for k in ("srcset", "imagesrcset"):
            if a.get(k): s.refs += [(t, x.strip().split()[0]) for x in a[k].split(",") if x.strip()]
        if t == "meta":
            n = a.get("name") or a.get("property")
            if n: s.meta[n] = a.get("content", "")
        if t == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
fails = []; checked = {}; host = urlparse(BASE).netloc
def chk(u, src):
    if u in checked: return
    st, _ = get(u); checked[u] = st
    if st != 200: fails.append(f"{st} {u} (from {src})")
def page(path, expect):
    u = urljoin(BASE, path); st, body = get(u)
    if st != expect: fails.append(f"status {st}!={expect} {u}")
    p = P(); p.feed(body.decode("utf-8", "replace"))
    if "noindex" not in p.meta.get("robots", ""): fails.append(f"no noindex {u}")
    if expect == 200:
        if p.canon != u: fails.append(f"canonical {p.canon} != {u}")
        if p.meta.get("og:url") != u: fails.append(f"og:url {p.meta.get('og:url')} != {u}")
    refs = p.refs + [("meta", p.meta[k]) for k in ("og:image", "twitter:image") if p.meta.get(k)]
    for t, r in refs:
        if r.startswith(("mailto:", "tel:")) or r.startswith("#"): continue
        a = urljoin(u, r).split("#")[0]
        if urlparse(a).netloc != host:
            if t in ("a",): continue  # outbound text links (e.g. GitHub docs) are fine
            fails.append(f"third-party resource {a} on {u}"); continue
        if not a.startswith(BASE): fails.append(f"escapes subpath {a} on {u}"); continue
        chk(a, u)
    return st
for pth in PAGES: page(pth, 200)
page("no-such-page/", 404); page("deep/missing/path.html", 404)
css = urljoin(BASE, "assets/css/styles.css"); _, cb = get(css)
for r in set(re.findall(r"url\(['\"]?([^'\")]+)", cb.decode())):
    if not r.startswith("data:"): chk(urljoin(css, r), "styles.css")
st, sm = get(urljoin(BASE, "sitemap.xml")); locs = re.findall(r"<loc>([^<]+)</loc>", sm.decode())
if sorted(locs) != sorted(urljoin(BASE, p) for p in PAGES): fails.append(f"sitemap locs mismatch {locs}")
for l in locs: chk(l, "sitemap.xml")
st, rb = get(urljoin(BASE, "robots.txt"))
if st != 200 or "Disallow: /" not in rb.decode(): fails.append("robots.txt not Disallow-all")
for f in fails: print("FAIL", f)
print(f"SUMMARY live pages={len(PAGES)}+2x404 urls-checked={len(checked)} sitemap-locs={len(locs)} fails={len(fails)}")
sys.exit(1 if fails else 0)
