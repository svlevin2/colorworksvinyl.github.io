#!/usr/bin/env python3
"""Prepare fonts, images, favicons and logo for the site. Rerunnable.
Sources: build-v1/assets-v2, brand-kit/fonts_dl, marketing-src/logos/svg."""
import os, re, shutil
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = '/workspace/colorworks/website/build-v1/assets-v2'
FONTS = '/workspace/colorworks/brand-kit/fonts_dl'
LOGO = '/workspace/colorworks/marketing-src/logos/svg/Color logo - no background.svg'
IMG = os.path.join(ROOT, 'assets/img'); ICO = os.path.join(ROOT, 'assets/icons'); FNT = os.path.join(ROOT, 'assets/fonts')

# Fonts: Latin subset, woff2
UNI = 'U+0020-007E,U+00A0,U+00A9,U+00AE,U+00D7,U+2019,U+201C,U+201D,U+2022,U+203A,U+2122'
def sub(font, out):
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['kern', 'liga', 'calt', 'ss01', 'cv11', 'tnum', 'case']
    s = subset.Subsetter(opts); s.populate(unicodes=subset.parse_unicodes(UNI)); s.subset(font)
    font.flavor = 'woff2'; font.save(out); print(out, os.path.getsize(out))
# Inter 4.1 variable (rsms/inter release zip, web/InterVariable.woff2), weight axis limited to 400-800, opsz kept
it = instancer.instantiateVariableFont(TTFont(f'{FONTS}/InterVariable.woff2'), {'wght': (400, 800)})
it.flavor = None; it.save('/tmp/inter-inst.ttf')
sub(TTFont('/tmp/inter-inst.ttf'), f'{FNT}/inter-var.woff2')
shutil.copy(f'{FONTS}/Inter-OFL.txt', f'{FNT}/Inter-OFL.txt')

# Images: responsive webp widths
jobs = {
 'hero-desktop': ('hero-colorful-ink-splash-artwork-desktop v2.webp', [1920, 1440, 960]),
 'hero-mobile': ('hero-colorful-ink-splash-artwork-mobile v2.webp', [750, 480]),
 'card-signage': ('business-signage-storefront-window-decal-mockup-card v1.webp', [800, 400]),
 'card-stickers': ('custom-die-cut-stickers-mockup-card v1.webp', [800, 400]),
 'card-dance-floor': ('wedding-dance-floor-monogram-decal-mockup-card v3.webp', [800, 400]),
 'local-storefront': ('storefront-window-lettering-mockup-local v1.webp', [1200, 600]),
 'banner-signage': ('business-signage-storefront-window-decal-mockup-banner v1.webp', [1600, 800]),
 'banner-store-hours': ('store-hours-window-decal-mockup-banner v1.webp', [1600, 800]),
 'banner-stickers': ('custom-logo-stickers-packaging-mockup-banner v1.webp', [1600, 800]),
 'banner-dance-floor': ('wedding-dance-floor-monogram-decal-mockup-banner v1.webp', [1600, 800]),
}
for name, (f, widths) in jobs.items():
    im = Image.open(os.path.join(SRC, f)).convert('RGB')
    for w in widths:
        h = round(im.height * w / im.width)
        out = f'{IMG}/{name}-{w}.webp'
        (im if w == im.width else im.resize((w, h), Image.LANCZOS)).save(out, 'WEBP', quality=78, method=6)
        print(out, w, h, os.path.getsize(out))
# OG share image: keep the stripe and logo from the brand image, redraw the text lines
# (the source image's last line mentions a marketplace, which the site must not show).
from PIL import ImageDraw, ImageFont
og = Image.open(f'{SRC}/colorworks-vinyl-og-share-image v1.jpg').convert('RGB')
bgc = og.getpixel((600, 560)); canvas = Image.new('RGB', og.size, bgc); canvas.paste(og.crop((0, 0, og.width, 330)), (0, 0))
d = ImageDraw.Draw(canvas)
def inter(size, wght):
    ft = ImageFont.truetype(f'{FONTS}/InterVariable.ttf', size); ft.set_variation_by_axes([min(32, max(14, size)), wght]); return ft
for text, y, ft, col in [('Signage, stickers, decals and vinyl printing', 392, inter(44, 700), (255, 255, 255)),
                         ('Lake Zurich, IL', 462, inter(30, 500), (201, 210, 223))]:
    tw = d.textlength(text, font=ft); d.text(((og.width - tw) / 2, y), text, font=ft, fill=col)
canvas.save(f'{IMG}/og-share-1200x630.jpg', quality=88, optimize=True); print('og rebuilt')

# Real ColorWorks monogram designs (shop listing images), square, used on the events page
ETSY = '/workspace/colorworks/website/build-v1/assets-etsy'
for i, f in enumerate(['bs1.jpg', 'bs2.jpg', 'bs3.jpg', 'bs4.jpg', 'bs5.jpg', 'bs6.jpg']):
    im = Image.open(f'{ETSY}/{f}').convert('RGB')
    for w in (640, 320):
        out = f'{IMG}/monogram-{i + 1}-{w}.webp'; im.resize((w, w), Image.LANCZOS).save(out, 'WEBP', quality=80, method=6); print(out, os.path.getsize(out))

# Favicons
fav = Image.open(f'{SRC}/colorworks-favicon-512 v1.png').convert('RGBA')
fav.save(f'{ICO}/favicon-512.png', optimize=True)
fav.resize((192, 192), Image.LANCZOS).save(f'{ICO}/favicon-192.png', optimize=True)
fav.resize((32, 32), Image.LANCZOS).save(f'{ICO}/favicon-32.png', optimize=True)
bg = Image.new('RGBA', (180, 180), (255, 255, 255, 255)); bg.alpha_composite(fav.resize((180, 180), Image.LANCZOS))
bg.convert('RGB').save(f'{ICO}/apple-touch-icon.png', optimize=True)

# Logo: strip Illustrator switch/foreignObject cruft, use currentColor
s = open(LOGO).read()
s = re.sub(r'<\?xml.*?\?>', '', s, flags=re.S)
s = re.sub(r'<foreignObject.*?</foreignObject>', '', s, flags=re.S)
s = re.sub(r'</?switch[^>]*>', '', s)
s = re.sub(r'\si:extraneous="[^"]*"', '', s)
s = s.replace('<defs></defs>', '')
s = re.sub(r'#00204a', 'currentColor', s, flags=re.I)
s = re.sub(r'\s(id|featureKey|xmlns:[a-z]+|data-name|class|xml:space|style|x|y|width|height|enable-background)="[^"]*"', '', s)
s = re.sub(r'>\s+<', '><', s).strip()
s = re.sub(r'\s+', ' ', s)
s = s.replace('<svg ', '<svg class="logo-svg" role="img" aria-label="ColorWorks Vinyl" focusable="false" ', 1)
open(f'{ROOT}/src/partials/logo.svg', 'w').write(s)
print('logo', len(s))
