// Screenshot chosen gallery slides at 390 WebKit DPR 2 and 1440 Chromium DPR 1. Usage: node tools/qa/slide_shots.mjs base outdir slug:n ...
import { createRequire } from 'module';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { chromium, webkit } = require('playwright');
const [base, out, ...items] = process.argv.slice(2);
for (const [tag, eng, vp, dpr] of [['webkit-390-2x', webkit, { width: 390, height: 844 }, 2], ['chromium-1440-1x', chromium, { width: 1440, height: 900 }, 1]]) {
  const b = await eng.launch(); const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: dpr, reducedMotion: 'reduce' }); const p = await ctx.newPage();
  for (const it of items) { const [s, n] = it.split(':');
    await p.goto(base + 'services/' + s + '/', { waitUntil: 'load' });
    const sl = p.locator('.carousel-track .slide').nth(+n - 1); await sl.scrollIntoViewIfNeeded();
    await p.locator('.carousel-track').focus(); for (let i = 1; i < +n; i++) { await p.keyboard.press('ArrowRight'); await p.waitForTimeout(250); }
    const img = sl.locator('img'); await img.evaluate(e => e.complete || new Promise(r => e.onload = r));
    const src = await img.evaluate(e => e.currentSrc.split('/').pop());
    await img.screenshot({ path: `${out}/${tag}-${s}-${n}.png` }); console.log(tag, s, n, src);
  }
  await b.close();
}
