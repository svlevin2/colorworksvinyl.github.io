import { createRequire } from 'module';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { webkit, devices } = require('playwright');
const b = await webkit.launch(); const ctx = await b.newContext({ ...devices['iPhone 12'] }); const p = await ctx.newPage();
for (const s of ['window-graphics', 'die-cut-stickers']) {
  await p.goto('http://localhost:8765/colorworksvinyl.github.io/services/' + s + '/', { waitUntil: 'load' }); await p.waitForTimeout(800);
  const r = await p.evaluate(() => { const g = document.querySelector('.good-for'); const t = document.querySelector('.prod-hero-text'); const e = g || t; const bb = e.getBoundingClientRect(); return { y: bb.bottom + scrollY, good: !!g, lead: document.querySelector('.lead').innerText }; });
  await p.screenshot({ path: `/workspace/colorworks/website/qa-output/p3/gate-fix/${s}-390-hero.png`, clip: { x: 0, y: 0, width: 390, height: Math.ceil(r.y + 16) }, fullPage: true });
  console.log(s, JSON.stringify(r));
}
await b.close();
