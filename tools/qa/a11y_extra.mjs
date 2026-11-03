// Keyboard and reduced-motion checks. Usage: node tools/qa/a11y_extra.mjs [baseUrl]
import { createRequire } from 'module';
const require = createRequire((process.env.QA_TOOLS || '/workspace/colorworks/website/qa-tools') + '/package.json');
const puppeteer = require('puppeteer-core');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const pages = ['', 'services/storefront-signage/', 'services/vehicle-lettering/', 'services/custom-vinyl-decals/', 'faq/', 'privacy/'];
const b = await puppeteer.launch({ executablePath: '/home/box/.local/bin/google-chrome', args: ['--no-sandbox'] });
let fails = 0; const log = (ok, m) => { if (!ok) fails++; console.log((ok ? 'PASS ' : 'FAIL ') + m); };
for (const p of pages) {
  const pg = await b.newPage(); await pg.setViewport({ width: 1440, height: 900 });
  await pg.goto(base + p, { waitUntil: 'networkidle0' });
  await pg.keyboard.press('Tab');
  const first = await pg.evaluate(() => document.activeElement.className);
  log(first.includes('skip-link'), `${p || 'home'} first Tab = skip link (${first})`);
  let noOutline = 0, n = 0, reachedSub = false;
  for (let i = 0; i < 40; i++) {
    const r = await pg.evaluate(() => { const e = document.activeElement; if (e === document.body) return { body: true }; const cs = getComputedStyle(e); const vis = e.getBoundingClientRect().width > 0 && cs.visibility !== 'hidden';
      const has = s => s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0 || s.boxShadow !== 'none';
      const card = e.closest('.card-link');  // stretched-link cards draw the ring on the card (:focus-within)
      return { ring: has(cs) || (card && has(getComputedStyle(card))), vis, sub: !!e.closest('.sub-menu') }; });
    if (r.body) { await pg.keyboard.press('Tab'); continue; }
    n++; if (!r.ring) noOutline++; if (r.sub && r.vis) reachedSub = true;
    await pg.keyboard.press('Tab');
  }
  log(noOutline === 0, `${p || 'home'} visible focus on ${n - noOutline}/${n} tab stops`);
  log(reachedSub, `${p || 'home'} Services submenu opens and is reachable by keyboard`);
  await pg.close();
}
const m = await b.newPage(); await m.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true });
await m.goto(base, { waitUntil: 'networkidle0' });
await m.focus('.menu-toggle'); await m.keyboard.press('Enter');
log(await m.evaluate(() => document.getElementById('site-menu').classList.contains('is-open')), 'phone menu opens with Enter');
await m.keyboard.press('Escape');
log(await m.evaluate(() => !document.getElementById('site-menu').classList.contains('is-open') && document.activeElement.classList.contains('menu-toggle')), 'phone menu closes with Escape and focus returns to the button');
const r = await b.newPage(); await r.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
await r.goto(base, { waitUntil: 'networkidle0' });
const rm = await r.evaluate(() => { const els = [...document.querySelectorAll('.reveal')]; return { n: els.length, hidden: els.filter(e => parseFloat(getComputedStyle(e).opacity) < 1).length, anim: els.filter(e => getComputedStyle(e).transitionDuration.split(',').some(d => parseFloat(d) > 0)).length }; });
log(rm.hidden === 0 && rm.anim === 0, `reduced motion: ${rm.n} reveal items, ${rm.hidden} hidden, ${rm.anim} with transitions`);
console.log(`SUMMARY a11y-extra fails=${fails}`);
await b.close();
