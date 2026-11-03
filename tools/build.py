#!/usr/bin/env python3
"""Build every page from src/pages/*.html plus the shared partials in src/partials.
Each page file starts with a JSON front-matter comment: <!--{...}-->.
Run: python3 tools/build.py   (set SITE_URL env to change the absolute URL used for canonical/og)."""
import os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get('SITE_URL', 'https://svlevin2.github.io/colorworksvinyl.github.io/')
BASE_PATH = re.sub(r'^https?://[^/]+', '', SITE)  # used by 404.html, which can be served at any depth
ICONS = os.path.join(ROOT, 'src/icons')  # vendored Lucide 1.66.0 icons (ISC, see src/icons/LICENSE-lucide.txt)
P = lambda n: open(os.path.join(ROOT, 'src/partials', n)).read()

LOGO = P('logo.svg').replace(re.search(r'viewBox="[^"]*"', P('logo.svg')).group(0), 'viewBox="120 78 2975 342"')

_icon_cache = {}
def icon(name, size=''):
    if name not in _icon_cache:
        s = open(os.path.join(ICONS, name + '.svg')).read()
        s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
        inner = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
        inner = re.sub(r'>\s+<', '><', inner).strip()
        _icon_cache[name] = inner
    cls = 'icon' + (' icon-lg' if size == 'lg' else '')
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{_icon_cache[name]}</svg>'

def render(text, ctx):
    text = re.sub(r'\{\{icon:([a-z0-9-]+)(?::(lg))?\}\}', lambda m: icon(m.group(1), m.group(2) or ''), text)
    text = re.sub(r'\{\{cur:([a-z-]+)\}\}', lambda m: ' aria-current="page"' if ctx.get('nav') == m.group(1) else '', text)
    for k, v in ctx.items():
        text = text.replace('{{' + k + '}}', str(v))
    left = re.findall(r'\{\{[^}]+\}\}', text)
    if left: raise SystemExit(f"unfilled placeholders in {ctx.get('path')}: {set(left)}")
    return text

import sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(ROOT, 'src/data'))
from categories import CATEGORIES, MOVED
from products import PRODUCTS
from examples import EXAMPLES, EXAMPLES_APPROVED
CAT = {c['slug']: c for c in CATEGORIES}
LIVE = {p['slug']: p for p in PRODUCTS if p['emit']}           # product pages that are built and linked
ENTRY = {pr['pass2']: (c, pr) for c in CATEGORIES for pr in c['products']}   # slug -> (category, card entry)
SECTION = {p['section'][0]: (p['slug'], p['section'][1]) for p in LIVE.values() if p.get('section')}  # merged product -> (page, anchor)

def product_href(pr, root):
    """Link for a category card / Home bullet: its product page, the section it was merged into, or None."""
    if pr['pass2'] in LIVE: return f'{root}services/{pr["pass2"]}/'
    if pr['pass2'] in SECTION:
        page, anchor = SECTION[pr['pass2']]
        return f'{root}services/{page}/#{anchor}'
    return None

def pic(img, root, sizes, lazy=True, extra=''):
    stem, a, b, w, h, alt = img
    load = 'loading="lazy" ' if lazy else 'fetchpriority="high" '
    return (f'<img src="{root}assets/img/{stem}-{b}.webp" srcset="{root}assets/img/{stem}-{a}.webp {a}w, {root}assets/img/{stem}-{b}.webp {b}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" {load}decoding="async" alt="{alt}"{extra}>')

def cat_url(c, root): return f'{root}services/{c["slug"]}/'

def shared(root):
    """Category-driven snippets used by the header, footer and Home."""
    nav = ''.join(f'<li><a href="{cat_url(c, root)}">{c["name"]}</a></li>' for c in CATEGORIES)
    foot = '\n          '.join(f'<li><a href="{cat_url(c, root)}">{c["name"]}</a></li>' for c in CATEGORIES)
    grid = []
    for i, c in enumerate(CATEGORIES):
        if c['card']:
            art = ' card-media--art' if c['card'][0].startswith('monogram') else ''
            media = f'<div class="card-media{art}">' + pic(c['card'], root, '(max-width: 734px) 88vw, (max-width: 1068px) 45vw, 380px') + '</div>'
        else:
            media = f'<div class="card-media card-media--tile" aria-hidden="true">{icon(c["icon"])}</div>'
        items = ''.join((f'<li><a href="{h}">{icon(pr["icon"])}<span>{pr["name"]}</span></a></li>' if (h := product_href(pr, root))
                         else f'<li>{icon(pr["icon"])}<span>{pr["name"]}</span></li>') for pr in c['products'])
        grid.append(f'''      <article class="card card-link svc acc-{c["acc"]} reveal" style="--i:{i % 3}">
        {media}
        <div class="card-body">
          <span class="card-icon">{icon(c["icon"])}</span>
          <h3><a href="{cat_url(c, root)}">{c["name"]}</a></h3>
          <p>{c["summary"]}</p>
          <ul class="svc-list">{items}</ul>
          <span class="more chev" aria-hidden="true">Learn more</span>
        </div>
      </article>''')
    return dict(nav_services=nav, footer_services=foot, services_grid='\n'.join(grid))

def gallery(c):
    lis = ''.join(f'\n      <li class="reveal" style="--i:{i % 3}">' + pic((stem, 320, 640, 640, 640, alt), '{{root}}', '(max-width: 734px) 44vw, 310px') + '</li>' for i, (stem, alt) in enumerate(c['gallery']))
    return f'''
<section class="section" aria-labelledby="designs-title">
  <div class="wrap">
    <div class="section-head center reveal">
      <h2 id="designs-title">A few of our monogram designs</h2>
      <p class="lead">Sample designs. We customize the names, initials, date and colors for your event.</p>
    </div>
    <ul class="gallery">{lis}
    </ul>
  </div>
</section>
'''

def include_box(c):
    # "What to include" box: approved Home checklist wording, plus the category's own approved line (if any) that is not
    # already said by the steps ("quote by email", "made and shipped", "made to your size and colors" are dropped).
    inc = [('ruler', 'The size, for example 12 x 12 inch, and how many'), ('palette', 'Your colors'),
           ('map-pin', 'Where it goes, for example the outside of a door or window'), ('image-plus', 'Your logo or artwork, if you have it')]
    dup = {'Made to your size and colors.', 'We send a quote by email.', 'Send your logo or artwork, if you have it.'}
    extra_lines = [(ic, t) for ic, t in c['ticks'] if t not in dup]
    inc += [(ic, t.rstrip('.')) for ic, t in extra_lines if t.startswith('Choose')]   # a choice the buyer makes goes in the list
    notes = [(ic, t) for ic, t in extra_lines if not t.startswith('Choose')]          # a fact about the product goes under it
    ticks = '\n'.join(f'        <li><span class="tick">{{{{icon:{ic}}}}}</span><span>{t}</span></li>' for ic, t in inc)
    note = ''.join(f'\n      <p class="include-note">{{{{icon:{ic}}}}}<span>{t}</span></p>' for ic, t in notes)
    return ticks, note

def category_page(c):
    """Front matter + body for one category page, from the single template src/partials/category.html."""
    path = f'services/{c["slug"]}/'; root = '../../'; url = SITE + path
    hero = (pic(c['hero'], '{{root}}', '(max-width: 734px) 88vw, (max-width: 1068px) 692px, 980px', lazy=False) if c['hero']
            else f'<div class="art-tile" aria-hidden="true">{{{{icon:{c["icon"]}}}}}</div>')
    prods = []
    for i, pr in enumerate(c['products']):
        tile = ('', ' tile-b', ' tile-c')[i % 3]
        media = ('<div class="card-media">' + pic(pr['img'], '{{root}}', '(max-width: 734px) 88vw, (max-width: 1068px) 340px, 310px') + '</div>' if pr['img']
                 else f'<div class="card-media card-media--tile{tile}" aria-hidden="true">{{{{icon:{pr["icon"]}}}}}</div>')
        h = product_href(pr, '{{root}}')
        prods.append(f'''      <article class="card product{' card-link' if h else ''} reveal" style="--i:{i}">
        {media}
        <div class="card-body">
          <span class="card-icon">{{{{icon:{pr["icon"]}}}}}</span>
          <h3>{f'<a href="{h}">{pr["name"]}</a>' if h else pr["name"]}</h3>
          <p>{pr["line"]}</p>{'<span class="more chev" aria-hidden="true">Learn more</span>' if h else ''}
        </div>
      </article>''')
    extra = gallery(c) if c.get('gallery') else ''
    ticks, note = include_box(c)
    rel = '\n'.join(f'''      <li class="acc-{o["acc"]} reveal" style="--i:{i % 3}"><a href="{{{{root}}}}services/{o["slug"]}/"><span class="card-icon">{{{{icon:{o["icon"]}}}}}</span><span class="rel-text"><strong>{o["name"]}</strong><span>{o["summary"]}</span></span></a></li>'''
                     for i, o in enumerate([o for o in CATEGORIES if o is not c]))
    plain = lambda t: t.replace('&amp;', '&')
    area = [{"@type": "City", "name": "Lake Zurich, IL"}, {"@type": "AdministrativeArea", "name": "Chicago, IL and nearby areas"}]
    meta = dict(path=path, nav='services', title=c['title'], description=c['description'],
                jsonld=[{"@context": "https://schema.org", "@type": "Service", "name": plain(c['name']), "serviceType": plain(c['name']), "description": plain(c['description']), "url": url,
                         "areaServed": area,
                         "provider": {"@type": "LocalBusiness", "name": "ColorWorks Vinyl", "url": SITE, "telephone": "+1-833-298-4695", "email": "info@colorworksvinyl.com", "areaServed": area},
                         "hasOfferCatalog": {"@type": "OfferCatalog", "name": plain(c['name']), "itemListElement": [dict({"@type": "OfferCatalog", "name": pr['name'], "description": pr['line']}, **({"url": product_href(pr, SITE)} if product_href(pr, SITE) else {})) for pr in c['products']]}},
                        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                            {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "#services"},
                            {"@type": "ListItem", "position": 3, "name": plain(c['name']), "item": url}]}])
    if c['hero']:
        stem, a, b = c['hero'][:3]
        meta['preload'] = [f'href="{{{{root}}}}assets/img/{stem}-{b}.webp" imagesrcset="{{{{root}}}}assets/img/{stem}-{a}.webp {a}w, {{{{root}}}}assets/img/{stem}-{b}.webp {b}w" imagesizes="(max-width: 734px) 88vw, (max-width: 1068px) 692px, 980px"']
    body = P('category.html')
    for k, v in dict(cat_name=c['name'], cat_acc=c['acc'], cat_h1=c['h1'], cat_lead=c['lead'], cat_hero=hero, cat_products='\n'.join(prods),
                     cat_products_title='Vinyl products', cat_extra=extra, cat_include=ticks, cat_note=note, cat_related=rel).items():
        body = body.replace('{{' + k + '}}', v)
    return meta, body

def product_page(p):
    """Front matter + body for one product page, from the single template src/partials/product.html."""
    c = CAT[p['cat']]; _, pr = ENTRY[p['slug']]
    path = f'services/{p["slug"]}/'; url = SITE + path
    plain = lambda t: t.replace('&amp;', '&')
    img = pr['img'] if p['hero'] == 'card' else p['hero']
    art = bool(img) and img[0].startswith('monogram')
    sizes = '(max-width: 860px) 88vw, (max-width: 1068px) 45vw, 520px'
    hero = (f'<div class="prod-media{" prod-media--art" if art else ""}">' + pic(img, '{{root}}', sizes, lazy=False) + '</div>' if img
            else f'<div class="art-tile prod-tile" aria-hidden="true">{{{{icon:{pr["icon"]}}}}}</div>')
    first = 'uses-title' if p['uses'] else 'include-title'
    uses = ''
    if p['uses']:
        lis = '\n'.join(f'        <li><span class="tick">{{{{icon:check}}}}</span><span>{u}</span></li>' for u in p['uses'])
        uses = ('\n    <div class="uses reveal">\n      <h2 id="uses-title">What it\'s for</h2>\n      <ul class="checklist">\n'
                + lis + '\n      </ul>\n    </div>')
    sec = ''
    if p.get('section'):
        mslug, anchor, head = p['section']; _, mpr = ENTRY[mslug]
        sec = (f'\n    <div class="merged reveal" id="{anchor}">\n      <span class="card-icon">{{{{icon:{mpr["icon"]}}}}}</span>\n'
               f'      <div><h2>{head}</h2><p>{mpr["line"]}</p></div>\n    </div>')
    ex = ''
    if EXAMPLES_APPROVED and EXAMPLES.get(p['slug']):
        # Shared Examples component: example 1 is a wide feature card, 2-5 a 2x2 grid; every other page mirrors the feature.
        if not p['uses']: first = 'examples-title'
        flip = [q['slug'] for q in PRODUCTS].index(p['slug']) % 2
        cards = []
        for i, (t, d) in enumerate(EXAMPLES[p['slug']], 1):
            stem = f'ex-{p["slug"]}-{i}'
            sz = '(max-width: 734px) 88vw, 560px' if i == 1 else '(max-width: 734px) 88vw, 480px'
            if os.path.exists(os.path.join(ROOT, f'assets/img/{stem}-1200.webp')):
                media = '<div class="card-media">' + pic((stem, 600, 1200, 1200, 900, 'Digital mockup of ' + t[0].lower() + t[1:]), '{{root}}', sz) + '</div>'
            else:
                media = f'<div class="card-media card-media--tile{("", " tile-b", " tile-c")[(i - 1) % 3]}" aria-hidden="true">{{{{icon:{pr["icon"]}}}}}</div>'
            cls = 'card example example--feature' if i == 1 else 'card example'
            cards.append(f'      <li class="{cls} reveal" style="--i:{(i - 1) % 2}">{media}<div class="card-body"><h3>{t}</h3><p>{d}</p></div></li>')
        ex = (f'\n    <div class="examples{" examples--flip" if flip else ""}">\n      <h2 id="examples-title" class="reveal">Examples</h2>\n      <ul class="example-grid">\n'
              + '\n'.join(cards) + '\n      </ul>\n    </div>')
    ticks, note = include_box(c)
    rels = [LIVE[r] for r in p['related'] if r in LIVE]
    rel = '\n'.join(f'      <li class="acc-{CAT[o["cat"]]["acc"]} reveal" style="--i:{i % 3}"><a href="{{{{root}}}}services/{o["slug"]}/"><span class="card-icon">{{{{icon:{ENTRY[o["slug"]][1]["icon"]}}}}}</span>'
                    f'<span class="rel-text"><strong>{ENTRY[o["slug"]][1]["name"]}</strong><span>{ENTRY[o["slug"]][1]["line"]}</span></span></a></li>'
                    for i, o in enumerate(rels))
    area = [{"@type": "City", "name": "Lake Zurich, IL"}, {"@type": "AdministrativeArea", "name": "Chicago, IL and nearby areas"}]
    meta = dict(path=path, nav='services', title=p['title'], description=p['description'],
                jsonld=[{"@context": "https://schema.org", "@type": "Service", "name": plain(pr['name']), "serviceType": plain(pr['name']), "description": p['description'], "url": url,
                         "category": plain(c['name']), "areaServed": area,
                         "provider": {"@type": "LocalBusiness", "name": "ColorWorks Vinyl", "url": SITE, "telephone": "+1-833-298-4695", "email": "info@colorworksvinyl.com", "areaServed": area}},
                        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                            {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "#services"},
                            {"@type": "ListItem", "position": 3, "name": plain(c['name']), "item": SITE + f'services/{c["slug"]}/'},
                            {"@type": "ListItem", "position": 4, "name": plain(pr['name']), "item": url}]}])
    if img:
        stem, a, b = img[:3]
        meta['preload'] = [f'href="{{{{root}}}}assets/img/{stem}-{b}.webp" imagesrcset="{{{{root}}}}assets/img/{stem}-{a}.webp {a}w, {{{{root}}}}assets/img/{stem}-{b}.webp {b}w" imagesizes="{sizes}"']
    body = P('product.html')
    for k, v in dict(cat_name=c['name'], cat_slug=c['slug'], cat_acc=c['acc'], prod_name=pr['name'], prod_lead=pr['line'], prod_hero=hero, prod_first_id=first,
                     prod_uses=uses, prod_section=sec, prod_examples=ex, cat_include=ticks, cat_note=note,
                     cat_extra=gallery(c) if p.get('gallery') else '', prod_related=rel).items():
        body = body.replace('{{' + k + '}}', v)
    return meta, body

def moved_page(old, c):
    meta = dict(path=old, nav='services', title='This Page Has Moved - ColorWorks Vinyl',
                description=f'This page has moved. {c["name"].replace("&amp;", "and")} from ColorWorks Vinyl in Lake Zurich, IL is now at a new address on this site. Follow the link to see it.',
                refresh=f'services/{c["slug"]}/')
    body = f'''<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <h1 id="page-title">This page has moved</h1>
    <p class="lead">{c["name"]} now has its own page.</p>
    <div class="ctas">
      <a class="btn btn-primary" href="{{{{root}}}}services/{c["slug"]}/">Go to {c["name"]}</a>
    </div>
    <div class="hero-art"></div>
  </div>
</section>
'''
    return meta, body

def render_page(meta, body):
    path = meta['path']                       # '' for home, 'faq/' etc, '404.html' for 404
    is404 = path == '404.html'
    depth = 0 if is404 or path == '' else path.strip('/').count('/') + 1
    root = BASE_PATH if is404 else '../' * depth
    home = root if root else './'
    ctx = dict(hdr='')
    ctx.update(meta)
    ctx.update(shared(root))
    canon = SITE + meta['refresh'] if meta.get('refresh') else SITE + ('' if is404 else path)
    ctx.update(root=root, home=home, site=SITE, logo=LOGO, url=canon,
               preload=''.join(f'<link rel="preload" as="image" type="image/webp" {p}>\n' for p in meta.get('preload', [])).replace('{{root}}', root),
               jsonld=''.join('<script type="application/ld+json">' + json.dumps(j, separators=(',', ':')) + '</script>\n' for j in meta.get('jsonld', [])))
    ctx.pop('refresh', None)
    ctx['band'] = render(P('band.html'), dict(ctx))
    head = render(P('head.html'), ctx)
    if meta.get('refresh'):
        head = head.replace('</head>', f'<meta http-equiv="refresh" content="0; url={root}{meta["refresh"]}">\n</head>')
    html = head + render(P('header.html'), ctx) + '<main id="main">\n' + render(body, ctx) + '</main>\n' + render(P('footer.html'), ctx)
    dest = os.path.join(ROOT, path if is404 else os.path.join(path, 'index.html'))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'w').write(html)
    return dest

def build():
    out, pages = [], []
    srcs = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/pages/*.html'))):
        raw = open(f).read()
        m = re.match(r'\s*<!--(\{.*?\})-->\s*', raw, re.S)
        srcs.append((json.loads(m.group(1)), raw[m.end():]))
    cats = [category_page(c) for c in CATEGORIES]
    cats += [product_page(p) for p in PRODUCTS if p['emit']]
    moved = [moved_page(o, next(c for c in CATEGORIES if c['slug'] == s)) for o, s in MOVED.items()]
    home = [x for x in srcs if x[0]['path'] == '']
    rest = [x for x in srcs if x[0]['path'] != '']
    for meta, body in home + cats + rest + moved:
        out.append(render_page(meta, body))
        if meta['path'] != '404.html' and not meta.get('refresh'): pages.append(meta['path'])
    # robots and sitemap (Disallow-all until launch); moved pages and the 404 are left out
    open(os.path.join(ROOT, 'robots.txt'), 'w').write('# Pre-launch preview. Remove the Disallow line at launch.\nUser-agent: *\nDisallow: /\n')
    urls = ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in pages)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
    for d in out: print('built', os.path.relpath(d, ROOT))

if __name__ == '__main__':
    build()
