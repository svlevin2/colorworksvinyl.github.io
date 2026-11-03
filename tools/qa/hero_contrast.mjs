// Measures real contrast of text over images and gradients against the actual pixels behind it:
// the Home hero with the overlay header (top of page), and the Who We Are section (color swirl).
// Text is made transparent, the viewport is screenshotted, and every pixel inside each text box is
// compared with the text's own color. Reports the minimum (strict) and 5th percentile per element.
// Usage: node tools/qa/hero_contrast.mjs [homeUrl]
import { createRequire } from 'module';
const require = createRequire((process.env.QA_TOOLS || '/workspace/colorworks/website/qa-tools') + '/package.json');
const puppeteer = require('puppeteer-core');
const { PNG } = require('pngjs');
const url = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const lum = ([r, g, b]) => { const f = c => { c /= 255; return c <= .03928 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
const cr = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
const GROUPS = [
  { name: 'hero', sel: '.hero h1, .hero .eyebrow, .hero .lead, .hero .btn, .site-header .brand, .site-header .nav-menu a, .site-header .nav .btn, .site-header .menu-toggle', hide: '.hero *, .site-header *', scroll: null },
  { name: 'who-we-are', sel: '#about h2, #about .subhead, #about .split p, #about .btn, #about .btn-link', hide: '#about *', scroll: 'each' },
  { name: 'contact', sel: '#contact h2, #contact .lead', hide: '#contact *', scroll: 'each' },
];
const b = await puppeteer.launch({ executablePath: '/home/box/.local/bin/google-chrome', args: ['--no-sandbox', '--hide-scrollbars'] });
let fails = 0, n = 0;
async function measure(p, w, label, sel, hide, idx) {
  const it = await p.evaluate((sel, hide, idx) => {
    const el = document.querySelectorAll(sel)[idx]; if (!el) return null;
    document.querySelectorAll('.reveal').forEach(r => r.classList.add('is-in'));
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    if (!r.width || !r.height || cs.display === 'none' || cs.visibility === 'hidden') return { skip: true };
    const rects = []; const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    while (tw.nextNode()) { if (!tw.currentNode.textContent.trim()) continue; const rg = document.createRange(); rg.selectNodeContents(tw.currentNode); for (const q of rg.getClientRects()) rects.push([q.x, q.y, q.width, q.height]); }
    if (!rects.length) { const s = el.querySelector('svg'); const q = (s || el).getBoundingClientRect(); const x0 = Math.max(q.x, r.x), y0 = Math.max(q.y, r.y), x1 = Math.min(q.right, r.right), y1 = Math.min(q.bottom, r.bottom); rects.push([x0, y0, x1 - x0, y1 - y0]); }
    const m = cs.color.match(/[\d.]+/g).map(Number);
    const st = document.createElement('style'); st.id = 'qa-hide';
    st.textContent = hide + '{color:transparent!important;text-shadow:none!important;caret-color:transparent!important;transition:none!important;animation:none!important} ' + hide.split(',').map(h => h.trim().replace(/\*$/, 'svg')).join(',') + '{visibility:hidden!important;transition:none!important}';
    document.head.appendChild(st);
    return { name: (el.className || el.tagName) + ' "' + (el.textContent.trim().slice(0, 28) || el.getAttribute('aria-label')) + '"', color: m.slice(0, 3), size: parseFloat(cs.fontSize), weight: +cs.fontWeight, rects };
  }, sel, hide, idx);
  if (!it || it.skip) return !!it;
  await new Promise(r => setTimeout(r, 350));
  const shot = await p.screenshot({ type: 'png' }); const png = PNG.sync.read(shot); if (process.env.QA_DUMP) (await import('fs')).writeFileSync(`/tmp/hc-${w}-${label}-${idx}.png`, shot);
  await p.evaluate(() => document.getElementById('qa-hide').remove());
  const vals = [];
  for (const [x, y, rw, rh] of it.rects) for (let yy = Math.max(0, Math.floor(y)); yy < Math.min(png.height, Math.ceil(y + rh)); yy++) for (let xx = Math.max(0, Math.floor(x)); xx < Math.min(png.width, Math.ceil(x + rw)); xx++) { const o = (yy * png.width + xx) * 4; vals.push(cr(it.color, [png.data[o], png.data[o + 1], png.data[o + 2]])); }
  if (!vals.length) return true;
  vals.sort((a, c) => a - c);
  const min = vals[0], p5 = vals[Math.floor(vals.length * .05)];
  const large = it.size >= 24 || (it.size >= 18.66 && it.weight >= 700);
  const need = large ? 3 : 4.5; const ok = min >= need; n++;
  if (!ok) fails++;
  console.log(`${w} ${label} ${ok ? 'PASS' : 'FAIL'} min=${min.toFixed(2)} p5=${p5.toFixed(2)} need=${need} color=${it.color.join(",")} ${it.name}`);
  return true;
}
for (const [w, h] of [[1440, 900], [390, 844]]) {
  const p = await b.newPage();
  await p.setViewport({ width: w, height: h, deviceScaleFactor: 1, isMobile: w < 500, hasTouch: w < 500 });
  await p.goto(url, { waitUntil: 'load', timeout: 30000 });
  await p.addStyleTag({ content: '*,*::before,*::after{transition:none!important;animation:none!important}' });
  await p.evaluate(() => Promise.all([...document.images].filter(i => i.loading !== 'lazy').map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; }))));
  for (const g of GROUPS) {
    const count = await p.evaluate(s => document.querySelectorAll(s).length, g.sel);
    for (let i = 0; i < count; i++) {
      if (g.scroll === 'each') {
        await p.evaluate((s, i) => { const el = document.querySelectorAll(s)[i]; el.scrollIntoView({ block: 'center', behavior: 'instant' }); }, g.sel, i);
        await p.evaluate(() => Promise.all([...document.images].map(im => { im.loading = 'eager'; return im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; }); })));
        await new Promise(r => setTimeout(r, 250));
      } else { await p.evaluate(() => window.scrollTo(0, 0)); }
      await measure(p, w, g.name, g.sel, g.hide, i);
    }
  }
  await p.close();
}
await b.close();
console.log(`SUMMARY text-over-image contrast elements=${n} fails=${fails}`);
process.exit(fails ? 1 : 0);
