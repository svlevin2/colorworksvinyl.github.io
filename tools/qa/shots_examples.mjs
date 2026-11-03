// Examples section (repo build with EXAMPLES_APPROVED = True). Usage: node tools/qa/shots_examples.mjs <base> <outDir>
// Chromium 1440 and 390: element shot of .examples on all 16 product pages (lazy images forced eager and awaited; fails on broken images).
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/p2/examples';
fs.mkdirSync(out, { recursive: true });
const PRODUCTS = ['wall-murals','lobby-logo-decals','wayfinding-decals','window-graphics','store-hours-decals','storefront-lettering','vehicle-lettering','fleet-decals','banners','logo-stickers','die-cut-stickers','dance-floor-decals','wedding-monograms','large-format-event-graphics','full-color-vinyl-prints','custom-vinyl-decals'];
const b = await chromium.launch(); let bad = 0;
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, deviceScaleFactor: w === 390 ? 2 : 1, isMobile: w === 390, hasTouch: w === 390 });
  const p = await ctx.newPage();
  for (const s of PRODUCTS) {
    await p.goto(base + 'services/' + s + '/', { waitUntil: 'load' });
    await p.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')));
    await p.evaluate(async () => { document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
      await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
      document.querySelectorAll('img').forEach(i => i.decoding = 'sync'); await Promise.all([...document.images].map(i => i.decode().catch(() => 0))); });
    await p.addStyleTag({ content: '.site-header{display:none!important}' }); await p.waitForTimeout(400);
    const n = await p.evaluate(() => [document.querySelectorAll('.example').length, document.documentElement.scrollWidth > document.documentElement.clientWidth,
      [...document.querySelectorAll('.examples img')].filter(i => !i.naturalWidth).length]);
    if (n[0] !== 5 || n[1] || n[2]) { bad++; console.log('FAIL', s, w, n); }
    // Headless Chromium leaves offscreen images unpainted in tall element shots, so grow the viewport to the page height first.
    // Only needed at 390; at 1440 a taller viewport grows the vh hero and the plain element shot already paints.
    if (w === 390) { const H = await p.evaluate(() => document.documentElement.scrollHeight); await p.setViewportSize({ width: w, height: Math.min(H, 16000) }); await p.waitForTimeout(800); }
    await p.locator('.examples').screenshot({ path: `${out}/${s}-${w}.png` });
    if (w === 390) await p.setViewportSize({ width: w, height: 844 });
  }
  await ctx.close();
}
await b.close(); console.log('DONE shots_examples fails=' + bad);
