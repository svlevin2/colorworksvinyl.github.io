// Pass 3 review screenshots. Usage: node tools/qa/shots_p3.mjs [baseUrl] [outDir]
// Chromium 1440 + 390: 3 sample product pages full page + gallery close-ups (start and after 2 Next clicks).
// WebKit 390 (iPhone 12) + Chromium 1440: every product page, for contact sheets.
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { chromium, webkit, devices } = require('playwright');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/p3';
const PRODUCTS = ['wall-murals','lobby-logo-decals','wayfinding-decals','window-graphics','store-hours-decals','storefront-lettering','vehicle-lettering','fleet-decals','banners','logo-stickers','die-cut-stickers','dance-floor-decals','wedding-monograms','large-format-event-graphics','full-color-vinyl-prints','custom-vinyl-decals'];
const SAMPLE = ['window-graphics', 'vehicle-lettering', 'banners'];
for (const d of ['', '/webkit-390', '/chromium-1440']) fs.mkdirSync(out + d, { recursive: true });
const full = async (p, path) => { await p.screenshot({ path, fullPage: true }); await p.waitForTimeout(900); await p.screenshot({ path, fullPage: true }); };
const settle = async p => { await p.evaluate(async () => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')); document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager'); for (let y = 0; y < document.body.scrollHeight; y += innerHeight) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); await Promise.all([...document.images].map(i => i.decode().catch(() => 0))); }); await p.waitForTimeout(600); };
let errs = 0;
const b = await chromium.launch();
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, deviceScaleFactor: w === 390 ? 2 : 1, isMobile: w === 390, hasTouch: w === 390 });
  const p = await ctx.newPage(); p.on('pageerror', () => errs++); p.on('console', m => { if (m.type() === 'error') errs++; });
  for (const s of SAMPLE) {
    await p.goto(base + `services/${s}/`, { waitUntil: 'load' }); await settle(p);
    await full(p, `${out}/${s}-${w}.png`);
    const g = p.locator('.gallery-sec');
    await g.scrollIntoViewIfNeeded(); await g.screenshot({ path: `${out}/${s}-${w}-gallery.png` });
    await p.click('.carousel-btn[data-dir="1"]'); await p.waitForTimeout(700); await p.click('.carousel-btn[data-dir="1"]'); await p.waitForTimeout(900);
    await g.screenshot({ path: `${out}/${s}-${w}-gallery-3.png` });
  }
  if (w === 1440) for (const s of PRODUCTS) { await p.goto(base + `services/${s}/`, { waitUntil: 'load' }); await settle(p); await full(p, `${out}/chromium-1440/${s}.png`); }
  await ctx.close();
}
await b.close();
const wk = await webkit.launch();
const ctx = await wk.newContext({ ...devices['iPhone 12'], viewport: { width: 390, height: 844 } });
const p = await ctx.newPage(); p.on('pageerror', () => errs++);
for (const s of PRODUCTS) { await p.goto(base + `services/${s}/`, { waitUntil: 'load' }); await settle(p); await full(p, `${out}/webkit-390/${s}.png`); }
await wk.close();
console.log('DONE shots_p3 console-errors=' + errs);
