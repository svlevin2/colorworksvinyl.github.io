// Pass 3 gallery QA: keyboard (Arrow/Home/End on the track), buttons, counter, aria-disabled, reduced motion, CLS, 4:3 slides, lazy images.
// Usage: node tools/qa/gallery.mjs [baseUrl]   Runs Chromium, WebKit and Firefox on all 16 product pages.
import { createRequire } from 'module';
const require = createRequire('/workspace/colorworks/website/qa-tools/package.json');
const { chromium, webkit, firefox } = require('playwright');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const P = ['wall-murals','lobby-logo-decals','wayfinding-decals','window-graphics','store-hours-decals','storefront-lettering','vehicle-lettering','fleet-decals','banners','logo-stickers','die-cut-stickers','dance-floor-decals','wedding-monograms','large-format-event-graphics','full-color-vinyl-prints','custom-vinyl-decals'];
let fails = 0, checks = 0; const slides = {};
const ok = (c, m) => { checks++; if (!c) { fails++; console.log('FAIL ' + m); } };
for (const [name, eng] of [['chromium', chromium], ['webkit', webkit], ['firefox', firefox]]) {
  const b = await eng.launch();
  for (const rm of ['no-preference', 'reduce']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: rm });
    const p = await ctx.newPage(); let errs = 0; p.on('pageerror', () => errs++); p.on('console', m => { if (m.type() === 'error') errs++; });
    for (const s of P) {
      const tag = `${name} ${rm} ${s}`;
      await p.addInitScript(() => { window.__cls = 0; try { new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: 'layout-shift', buffered: true }); } catch (e) {} });
      await p.goto(base + 'services/' + s + '/', { waitUntil: 'load' });
      const info = await p.evaluate(() => { const t = document.querySelector('.carousel-track'); const sl = [...t.querySelectorAll('.slide')];
        return { n: sl.length, navHidden: document.querySelector('.carousel-nav').hidden, ratios: sl.map(x => { const r = x.querySelector('img').getBoundingClientRect(); return +(r.width / r.height).toFixed(2); }), lazy: sl.every(x => x.querySelector('img').loading === 'lazy'), sb: getComputedStyle(document.documentElement).scrollBehavior, autoplay: !!document.querySelector('[data-autoplay]') }; });
      slides[s] = info.n;
      ok(!info.navHidden, tag + ' nav hidden'); ok(info.lazy, tag + ' not lazy'); ok(!info.autoplay, tag + ' autoplay');
      ok(info.ratios.every(r => Math.abs(r - 1.33) < 0.02), tag + ' ratio ' + info.ratios);
      if (rm === 'reduce') ok(info.sb !== 'smooth', tag + ' smooth scroll under reduce');
      const cnt = () => p.locator('.carousel-count').innerText();
      const prevDis = () => p.locator('.carousel-btn[data-dir="-1"]').getAttribute('aria-disabled');
      const nextDis = () => p.locator('.carousel-btn[data-dir="1"]').getAttribute('aria-disabled');
      ok((await cnt()).trim() === `1 of ${info.n}`, tag + ' start count ' + await cnt()); ok(await prevDis() === 'true', tag + ' prev not disabled at start');
      await p.locator('.carousel-track').focus(); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(rm === 'reduce' ? 250 : 900);
      ok((await cnt()).trim() === `2 of ${info.n}`, tag + ' ArrowRight -> ' + await cnt());
      await p.keyboard.press('End'); await p.waitForTimeout(rm === 'reduce' ? 250 : 1200);
      ok((await cnt()).trim() === `${info.n} of ${info.n}`, tag + ' End -> ' + await cnt()); ok(await nextDis() === 'true', tag + ' next not disabled at end');
      await p.keyboard.press('Home'); await p.waitForTimeout(rm === 'reduce' ? 250 : 1200);
      ok((await cnt()).trim() === `1 of ${info.n}`, tag + ' Home -> ' + await cnt());
      await p.locator('.carousel-btn[data-dir="1"]').click(); await p.waitForTimeout(rm === 'reduce' ? 250 : 900);
      ok((await cnt()).trim() === `2 of ${info.n}`, tag + ' Next click -> ' + await cnt());
      await p.keyboard.press('Tab'); // buttons reachable
      const bs = await p.locator('.carousel-btn').evaluateAll(e => e.map(x => [x.getBoundingClientRect().width, x.getBoundingClientRect().height]));
      ok(bs.every(([w, h]) => w >= 44 && h >= 44), tag + ' button size ' + bs);
      if (name === 'chromium') { const cls = await p.evaluate(() => window.__cls); ok(cls < 0.01, tag + ' CLS ' + cls); }
    }
    ok(errs === 0, `${name} ${rm} console errors ${errs}`);
    await ctx.close();
  }
  await b.close();
}
console.log('slides per page', JSON.stringify(slides));
console.log(`SUMMARY gallery checks=${checks} fails=${fails}`);
process.exit(fails ? 1 : 0);
