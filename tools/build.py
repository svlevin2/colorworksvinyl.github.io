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

def build():
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'src/pages/*.html'))):
        raw = open(f).read()
        m = re.match(r'\s*<!--(\{.*?\})-->\s*', raw, re.S)
        meta = json.loads(m.group(1)); body = raw[m.end():]
        path = meta['path']                       # '' for home, 'faq/' etc, '404.html' for 404
        is404 = path == '404.html'
        depth = 0 if is404 or path == '' else path.strip('/').count('/') + 1
        root = BASE_PATH if is404 else '../' * depth
        home = root if root else './'
        ctx = dict(meta)
        ctx.update(root=root, home=home, site=SITE, logo=LOGO,
                   url=SITE + ('' if is404 else path),
                   preload=''.join(f'<link rel="preload" as="image" type="image/webp" {p}>\n' for p in meta.get('preload', [])).replace('{{root}}', root),
                   jsonld=''.join('<script type="application/ld+json">' + json.dumps(j, separators=(',', ':')) + '</script>\n' for j in meta.get('jsonld', [])))
        ctx.pop('preload_list', None)
        ctx['band'] = render(P('band.html'), dict(ctx))
        html = render(P('head.html'), ctx) + render(P('header.html'), ctx) + '<main id="main">\n' + render(body, ctx) + '</main>\n' + render(P('footer.html'), ctx)
        dest = os.path.join(ROOT, path if is404 else os.path.join(path, 'index.html'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w').write(html)
        out.append(dest)
    # robots and sitemap (Disallow-all until launch)
    open(os.path.join(ROOT, 'robots.txt'), 'w').write('# Pre-launch preview. Remove the Disallow line at launch.\nUser-agent: *\nDisallow: /\n')
    pages = [json.loads(re.match(r'\s*<!--(\{.*?\})-->', open(f).read(), re.S).group(1))['path'] for f in sorted(glob.glob(os.path.join(ROOT, 'src/pages/*.html')))]
    urls = ''.join(f'  <url><loc>{SITE}{p}</loc></url>\n' for p in pages if p != '404.html')
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(os.path.join(ROOT, '.nojekyll'), 'w').write('')
    for d in out: print('built', os.path.relpath(d, ROOT))

if __name__ == '__main__':
    build()
