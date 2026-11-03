// Full-page phone shots (WebKit, iPhone 13 profile, 390x844) of the 16 product pages from the repo build.
// Usage: node tools/qa/shots_phone_full.mjs <base> <outDir>
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { webkit, devices } = require('playwright');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/p2/phone-390-full';
fs.mkdirSync(out, { recursive: true });
const PRODUCTS = ['wall-murals','lobby-logo-decals','wayfinding-decals','window-graphics','store-hours-decals','storefront-lettering','vehicle-lettering','fleet-decals','banners','logo-stickers','die-cut-stickers','dance-floor-decals','wedding-monograms','large-format-event-graphics','full-color-vinyl-prints','custom-vinyl-decals'];
const b = await webkit.launch(); let bad = 0;
const ctx = await b.newContext({ ...devices['iPhone 13'] });
const p = await ctx.newPage();
for (const s of PRODUCTS) {
  await p.goto(base + 'services/' + s + '/', { waitUntil: 'load' });
  await p.evaluate(async () => { document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in'));
    document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
    await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))); });
  await p.waitForTimeout(500);
  const r = await p.evaluate(() => ({ ex: document.querySelectorAll('.example').length, tiles: document.querySelectorAll('.example .card-media--tile').length,
    over: document.documentElement.scrollWidth > document.documentElement.clientWidth, broken: [...document.images].filter(i => !i.naturalWidth).length, w: innerWidth }));
  const ok = r.ex === 5 && !r.over && r.broken === 0 && r.w === 390;
  if (!ok) bad++;
  console.log(ok ? 'PASS' : 'FAIL', s, JSON.stringify(r));
  await p.screenshot({ path: `${out}/${s}-390-full.png`, fullPage: true });
}
await b.close(); console.log('DONE phone-390-full fails=' + bad);
