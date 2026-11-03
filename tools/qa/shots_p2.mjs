// Pass 2 review screenshots. Usage: node tools/qa/shots_p2.mjs [baseUrl] [outDir] [quick]
// Chromium 1440 + 390: Home, one category, two product pages. WebKit 390 (iPhone): every product page.
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { chromium, webkit, devices } = require('playwright');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/p2';
const quick = process.argv[4] === 'quick';
fs.mkdirSync(out + '/webkit-390', { recursive: true });
const PRODUCTS = ['wall-murals','lobby-logo-decals','wayfinding-decals','window-graphics','store-hours-decals','storefront-lettering','vehicle-lettering','fleet-decals','banners','logo-stickers','die-cut-stickers','dance-floor-decals','wedding-monograms','large-format-event-graphics','full-color-vinyl-prints','custom-vinyl-decals'];
// fullPage capture resizes the viewport, which can swap srcset candidates mid-capture: shoot twice, keep the second.
const full = async (p, path) => { await p.screenshot({ path, fullPage: true }); await p.waitForTimeout(1200); await p.screenshot({ path, fullPage: true }); };
const settle = async p => { await p.evaluate(async () => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')); document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); await Promise.all([...document.images].map(i => i.decode().catch(() => 0))); }); await p.waitForTimeout(600); };
const b = await chromium.launch();
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, deviceScaleFactor: w === 390 ? 2 : 1, isMobile: w === 390, hasTouch: w === 390 });
  const p = await ctx.newPage();
  for (const [name, u] of [['home', ''], ['category-vehicle-graphics', 'services/vehicle-graphics/'], ['product-store-hours-decals', 'services/store-hours-decals/'], ['product-vehicle-lettering', 'services/vehicle-lettering/'], ...(quick ? [['product-wedding-monograms', 'services/wedding-monograms/'], ['product-custom-vinyl-decals', 'services/custom-vinyl-decals/']] : [])]) {
    await p.goto(base + u, { waitUntil: 'load' }); await settle(p);
    await full(p, `${out}/${name}-${w}.png`);
  }
  await ctx.close();
}
await b.close();
if (!quick) {
  const wk = await webkit.launch();
  const ctx = await wk.newContext({ ...devices['iPhone 12'], viewport: { width: 390, height: 844 } });
  const p = await ctx.newPage();
  for (const s of PRODUCTS) { await p.goto(base + `services/${s}/`, { waitUntil: 'load' }); await settle(p); await full(p, `${out}/webkit-390/${s}.png`); }
  await wk.close();
}
console.log('DONE shots_p2');
