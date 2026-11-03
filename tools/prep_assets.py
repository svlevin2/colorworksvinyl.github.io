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
    opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = ['kern', 'liga', 'smcp', 'c2sc']
    s = subset.Subsetter(opts); s.populate(unicodes=subset.parse_unicodes(UNI)); s.subset(font)
    font.flavor = 'woff2'; font.save(out); print(out, os.path.getsize(out))
sub(TTFont(f'{FONTS}/CormorantSC-Bold.ttf'), f'{FNT}/cormorant-sc-700.woff2')
os_ = TTFont(f'{FONTS}/OpenSans[wdth,wght].ttf')
os_ = instancer.instantiateVariableFont(os_, {'wdth': 100, 'wght': (400, 700)})
os_.save('/tmp/os-inst.ttf'); os_ = TTFont('/tmp/os-inst.ttf')
sub(os_, f'{FNT}/open-sans-var.woff2')
shutil.copy(f'{FONTS}/CormorantSC-OFL.txt', f'{FNT}/CormorantSC-OFL.txt')
shutil.copy(f'{FONTS}/OpenSans-OFL.txt', f'{FNT}/OpenSans-OFL.txt')

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
shutil.copy(f'{SRC}/colorworks-vinyl-og-share-image v1.jpg', f'{IMG}/og-share-1200x630.jpg')

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
