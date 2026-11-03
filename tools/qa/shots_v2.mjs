// Review screenshots for Pass 1 (Chromium engine). Usage: node tools/qa/shots_v2.mjs [baseUrl] [outDir]
import { createRequire } from 'module';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { chromium } = require('playwright');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/v2';
const b = await chromium.launch();
for (const w of [1440, 390]) {
  const ctx = await b.newContext({ viewport: { width: w, height: w === 390 ? 844 : 900 }, deviceScaleFactor: w === 390 ? 2 : 1, isMobile: w === 390, hasTouch: w === 390 });
  const p = await ctx.newPage();
  const open = async u => { await p.goto(base + u, { waitUntil: 'load' }); await p.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')); }); await p.waitForTimeout(500); };
  await open('');
  await p.screenshot({ path: `${out}/home-hero-${w}.png` });
  await p.screenshot({ path: `${out}/home-full-${w}.png`, fullPage: true });
  await p.evaluate(() => scrollTo(0, 1400)); await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/header-scrolled-${w}.png`, clip: { x: 0, y: 0, width: w, height: w === 390 ? 160 : 180 } });
  await p.evaluate(() => scrollTo(0, 0));
  const ab = p.locator('#about'); await ab.scrollIntoViewIfNeeded(); await p.waitForTimeout(400);
  await ab.screenshot({ path: `${out}/who-we-are-${w}.png` });
  const fb = p.locator('.footer-bottom'); await fb.scrollIntoViewIfNeeded(); await p.waitForTimeout(300);
  const r = await fb.boundingBox();
  await p.screenshot({ path: `${out}/footer-bar-${w}.png`, clip: { x: 0, y: Math.max(0, r.y - 24), width: w, height: r.height + 48 } });
  const centered = await p.evaluate(() => { const s = document.querySelector('.footer-bottom span, .footer-bottom p, .footer-bottom small'); const r = s.getBoundingClientRect(); return { text: s.textContent.trim(), left: Math.round(r.left), right: Math.round(innerWidth - r.right) }; });
  console.log(`footer-bar ${w}: "${centered.text}" left-gap=${centered.left} right-gap=${centered.right}`);
  await open('services/vehicle-graphics/');
  await p.screenshot({ path: `${out}/category-vehicle-graphics-${w}.png`, fullPage: true });
  await ctx.close();
}
await b.close(); console.log('DONE shots_v2');
