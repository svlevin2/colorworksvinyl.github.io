// Device and browser QA with Playwright engines (emulation, not real devices or branded browsers).
// Usage: node tools/qa/devices.mjs [baseUrl] [outDir]
import { createRequire } from 'module';
const require = createRequire((process.env.QA_TOOLS || '/workspace/colorworks/website/qa-tools') + '/package.json');
const { chromium, webkit, firefox } = require('playwright');
import fs from 'fs';
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/v2/devices';
fs.mkdirSync(out + '/webkit-iphone-390', { recursive: true });
const PAGES = ['', 'services/indoor-wall-graphics/', 'services/storefront-signage/', 'services/vehicle-graphics/', 'services/banners-large-format/', 'services/decals-stickers/', 'services/event-decals/', 'services/wall-murals/', 'services/lobby-logo-decals/', 'services/wayfinding-decals/', 'services/window-graphics/', 'services/store-hours-decals/', 'services/storefront-lettering/', 'services/vehicle-lettering/', 'services/fleet-decals/', 'services/banners/', 'services/logo-stickers/', 'services/die-cut-stickers/', 'services/dance-floor-decals/', 'services/wedding-monograms/', 'services/large-format-event-graphics/', 'services/full-color-vinyl-prints/', 'services/custom-vinyl-decals/', 'faq/', 'privacy/', 'terms/', 'accessibility/', '404.html'];
if (process.env.PAGES) PAGES.splice(0, PAGES.length, ...process.env.PAGES.split(',').map(x => x === '/' ? '' : x));   // optional page filter
const STUBS = { 'business-signage/': 'services/storefront-signage/', 'stickers-decals/': 'services/decals-stickers/', 'events/': 'services/event-decals/' };
const PH = [[320, 568], [568, 320], [375, 667], [667, 375], [390, 844], [844, 390], [414, 896], [896, 414], [768, 1024], [1024, 768]];
const ALL = [...PH, [1440, 900]];
const CONFIGS = [
  { id: 'chrome-desktop', label: 'Chrome desktop (Chromium engine; also stands in for Edge, same engine)', engine: chromium, vps: ALL, mobile: false },
  { id: 'chrome-android', label: 'Chrome Android (Chromium, Pixel-style emulation: mobile, touch, DPR 2.625)', engine: chromium, vps: PH, mobile: true, dpr: 2.625, ua: 'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36' },
  { id: 'safari-ios', label: 'Safari iOS stand-in (Playwright WebKit, iPhone emulation: mobile, touch, DPR 3)', engine: webkit, vps: PH, mobile: true, dpr: 3, ua: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' },
  { id: 'safari-desktop', label: 'Safari desktop stand-in (Playwright WebKit)', engine: webkit, vps: [[768, 1024], [1024, 768], [1440, 900]], mobile: false },
  { id: 'firefox', label: 'Firefox (Playwright Firefox; no mobile emulation)', engine: firefox, vps: ALL, mobile: false },
];
const only = process.env.ONLY ? process.env.ONLY.split(',') : null;
const results = [];
function pageChecks() {
  const vw = document.documentElement.clientWidth, phone = Math.min(innerWidth, innerHeight) <= 430;
  const f = [];
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth) f.push(`hscroll ${de.scrollWidth}>${de.clientWidth}`);
  const visible = e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0 && !e.closest('[hidden],[aria-hidden="true"]') && !(e.closest('details:not([open])') && !e.closest('summary')); };
  const name = e => (e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '') + ' "' + (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 28) + '"');
  if (phone) {
    for (const e of document.querySelectorAll('a[href], button, summary, input, select, textarea')) {
      if (!visible(e)) continue;
      // inline links inside a sentence are exempt (WCAG 2.5.8 inline exception); stretched card links use the card box
      const par = e.parentElement; const inline = getComputedStyle(e).display === 'inline' && par && /^(P|LI|SPAN|DD)$/.test(par.tagName) && par.textContent.trim().length > e.textContent.trim().length + 3;
      if (inline) continue;
      const card = e.closest('.card-link'); const r = (card || e).getBoundingClientRect();
      if (r.width < 44 - 0.5 || r.height < 44 - 0.5) f.push(`tap ${Math.round(r.width)}x${Math.round(r.height)} ${name(e)}`);
    }
    for (const e of document.querySelectorAll('main p, main li, main dd, footer p, footer li')) {
      if (!visible(e) || !e.textContent.trim() || e.closest('.eyebrow,.step-num,.tile-label') || e.classList.contains('eyebrow')) continue;
      const fs_ = parseFloat(getComputedStyle(e).fontSize); if (fs_ < 16) f.push(`font ${fs_}px ${name(e)}`);
      for (const s of e.querySelectorAll('span,a,strong')) { const z = parseFloat(getComputedStyle(s).fontSize); if (visible(s) && s.textContent.trim() && z < 16 && !s.closest('.eyebrow,.step-num,.tile-label')) f.push(`font ${z}px ${name(s)}`); }
    }
  }
  // text clipping: text box wider than its element (with clipping overflow), or text past the viewport edge
  const blocks = [...document.querySelectorAll('h1,h2,h3,h4,p,li,a,button,span,strong,summary,dt,dd,label')].filter(e => visible(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
  const boxes = [];
  for (const e of blocks) {
    const cs = getComputedStyle(e);
    if (e.scrollWidth > e.clientWidth + 1 && /hidden|clip/.test(cs.overflowX) && cs.textOverflow !== 'ellipsis' && !e.classList.contains('skip-link')) f.push(`clip ${name(e)}`);
    for (const n of e.childNodes) {
      if (n.nodeType !== 3 || !n.textContent.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const q of rg.getClientRects()) { if (q.width < 1) continue; if ((q.right > vw + 1 || q.left < -1) && !e.closest('.skip-link')) f.push(`offscreen ${name(e)}`); boxes.push([e, q]); }
    }
  }
  const seen = new Set();
  for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
    const [a, p] = boxes[i], [b, q] = boxes[j]; if (a === b || a.contains(b) || b.contains(a)) continue;
    const ix = Math.min(p.right, q.right) - Math.max(p.left, q.left), iy = Math.min(p.bottom, q.bottom) - Math.max(p.top, q.top);
    if (ix > 2 && iy > 2) { const k = name(a) + '|' + name(b); if (!seen.has(k)) { seen.add(k); f.push(`overlap ${name(a)} / ${name(b)}`); } }
  }
  // images: object-fit cover on cropped media
  for (const im of document.querySelectorAll('.hero img, .hero-art img, .card-media img, .split-media img')) {
    if (!visible(im)) continue; const cs = getComputedStyle(im);
    const r = im.getBoundingClientRect(); const ar = im.naturalWidth / im.naturalHeight, br = r.width / r.height;
    if (Math.abs(ar - br) > 0.02 && cs.objectFit === 'fill') f.push(`img-distorted ${im.getAttribute('src').split('/').pop()}`);
  }
  // tel and mailto
  for (const a of document.querySelectorAll('a[href^="tel:"]')) { if (a.getAttribute('href') !== 'tel:+18332984695') f.push('tel-href ' + a.getAttribute('href')); if (!/1\.833\.CWVINYL/.test(a.textContent) && !a.getAttribute('aria-label')) f.push('tel-text "' + a.textContent.trim() + '"'); if (a.hasAttribute('onclick')) f.push('tel-onclick'); }
  for (const a of document.querySelectorAll('a[href^="mailto:"]')) { if (a.getAttribute('href') !== 'mailto:info@colorworksvinyl.com') f.push('mailto-href ' + a.getAttribute('href')); const t = a.textContent.trim().replace(/\s+/g, ' '); if (!['Request a quote', 'Contact us', 'info@colorworksvinyl.com'].includes(t) && !t.includes('info@colorworksvinyl.com')) f.push('mailto-text "' + t + '"'); if (a.hasAttribute('onclick')) f.push('mailto-onclick'); }
  return { f, tel: document.querySelectorAll('a[href^="tel:"]').length, mail: document.querySelectorAll('a[href^="mailto:"]').length };
}
async function linkNotBlocked(page) {
  return page.evaluate(() => {
    const bad = [];
    for (const a of document.querySelectorAll('a[href^="tel:"], a[href^="mailto:"]')) {
      let prevented = null; const h = e => { prevented = e.defaultPrevented; e.preventDefault(); };
      window.addEventListener('click', h); a.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true })); window.removeEventListener('click', h);
      if (prevented) bad.push('js-blocked ' + a.getAttribute('href'));
    }
    return bad;
  });
}
async function navChecks(page) {
  const f = [];
  const tg = page.locator('.menu-toggle'); if (!(await tg.isVisible())) return { f, nav: 'n/a (desktop nav)' };
  await tg.click(); await page.waitForTimeout(80);
  if (!(await page.evaluate(() => document.getElementById('site-menu').classList.contains('is-open')))) f.push('nav-no-open');
  const inMenu = () => page.evaluate(() => !!document.activeElement.closest('#site-menu') || document.activeElement.classList.contains('menu-toggle'));
  let trapped = true; for (let i = 0; i < 14; i++) { await page.keyboard.press('Tab'); if (!(await inMenu())) { trapped = false; break; } }
  for (let i = 0; i < 4 && trapped; i++) { await page.keyboard.press('Shift+Tab'); if (!(await inMenu())) trapped = false; }
  if (!trapped) f.push('nav-focus-not-trapped');
  await page.keyboard.press('Escape'); await page.waitForTimeout(50);
  if (await page.evaluate(() => document.getElementById('site-menu').classList.contains('is-open'))) f.push('nav-escape-no-close');
  if (!(await page.evaluate(() => document.activeElement.classList.contains('menu-toggle')))) f.push('nav-escape-focus-not-returned');
  await tg.click(); await page.waitForTimeout(80);
  await page.evaluate(() => { document.documentElement.style.scrollBehavior = 'auto'; });
  const link = page.locator('#site-menu a[href*="#contact"]').first(); await link.click(); await page.waitForTimeout(150);
  if (await page.evaluate(() => document.getElementById('site-menu').classList.contains('is-open'))) f.push('nav-link-tap-no-close');
  return { f, nav: 'ok' };
}
async function anchorChecks(page) {
  return page.evaluate(async () => {
    const f = []; document.documentElement.style.scrollBehavior = 'auto';
    const ids = [...new Set([...document.querySelectorAll('a[href*="#"]')].map(a => new URL(a.href)).filter(u => u.pathname === location.pathname && u.hash.length > 1).map(u => u.hash.slice(1)))];
    const hdr = document.querySelector('.site-header');
    for (const id of ids) {
      const el = document.getElementById(id); if (!el) { f.push('anchor-missing #' + id); continue; }
      location.hash = id; await new Promise(r => setTimeout(r, 60));
      const max = document.documentElement.scrollHeight - innerHeight;
      const top = el.getBoundingClientRect().top, hb = hdr.getBoundingClientRect().bottom;
      if (top < hb - 1 && scrollY < max - 2 && !(id === 'main' && scrollY === 0)) f.push(`anchor-covered #${id} top=${Math.round(top)} header=${Math.round(hb)}`);
    }
    history.replaceState(null, '', location.pathname); scrollTo(0, 0);
    return { f, n: ids.length };
  });
}
for (const c of CONFIGS) {
  if (only && !only.includes(c.id)) continue;
  let browser; try { browser = await c.engine.launch(c.engine === chromium ? { executablePath: undefined } : {}); } catch (e) { results.push({ cfg: c.id, error: 'launch failed: ' + e.message.split('\n')[0] }); console.log('LAUNCH-FAIL', c.id, e.message.split('\n')[0]); continue; }
  for (const [w, h] of c.vps) {
    if (process.env.VPS && !process.env.VPS.split(',').includes(`${w}x${h}`)) continue;
    const opts = { viewport: { width: w, height: h } };
    if (c.mobile) Object.assign(opts, { isMobile: true, hasTouch: true, deviceScaleFactor: c.dpr, userAgent: c.ua });
    const ctx = await browser.newContext(opts);
    const ext = []; ctx.on('request', r => { const u = new URL(r.url()); if (!['localhost', '127.0.0.1'].includes(u.hostname) && !u.protocol.startsWith('data')) ext.push(r.url()); });
    for (const p of PAGES) {
      const page = await ctx.newPage(); const errs = [];
      page.on('pageerror', e => errs.push('pageerror ' + e.message));
      await page.goto(base + p, { waitUntil: 'load' });
      await page.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')));
      await page.waitForTimeout(450);
      const r = await page.evaluate(pageChecks);
      const f = [...r.f, ...(await linkNotBlocked(page)), ...errs];
      const cookies = (await ctx.cookies()).length; if (cookies) f.push('cookies ' + cookies);
      const a = await anchorChecks(page); f.push(...a.f);
      const n = await navChecks(page); f.push(...n.f);
      if (c.id === 'safari-ios' && w === 390 && h === 844) {
        await page.goto(base + p, { waitUntil: 'load' }); await page.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in'))); await page.waitForTimeout(400);
        await page.screenshot({ path: `${out}/webkit-iphone-390/${(p || 'home').replace(/\//g, '_').replace(/_$/, '') || 'home'}.png`, fullPage: true });
      }
      results.push({ cfg: c.id, vp: `${w}x${h}`, page: p || '/', fails: [...new Set(f)], tel: r.tel, mail: r.mail, anchors: a.n, nav: n.nav });
      await page.close();
    }
    for (const [o, t] of Object.entries(STUBS)) {
      const page = await ctx.newPage(); await page.goto(base + o, { waitUntil: 'load' }); await page.waitForTimeout(400);
      const ok = page.url().endsWith(t); results.push({ cfg: c.id, vp: `${w}x${h}`, page: o, fails: ok ? [] : ['redirect ' + page.url()], stub: true }); await page.close();
    }
    if (ext.length) results.push({ cfg: c.id, vp: `${w}x${h}`, page: '(all)', fails: ['external-requests ' + ext.length] });
    await ctx.close();
    const nf = results.filter(x => x.cfg === c.id && x.vp === `${w}x${h}` && x.fails && x.fails.length).length;
    console.log(`${c.id} ${w}x${h} pages-with-fails=${nf}`);
    if (process.env.VERBOSE) for (const x of results.filter(x => x.cfg === c.id && x.vp === `${w}x${h}` && x.fails && x.fails.length)) console.log('  ', x.page, JSON.stringify(x.fails));
  }
  await browser.close();
}
fs.writeFileSync(out + '/devices' + (process.env.ONLY ? '-' + process.env.ONLY.replace(/,/g, '+') : '') + '.json', JSON.stringify({ configs: CONFIGS.map(c => ({ id: c.id, label: c.label, vps: c.vps.map(v => v.join('x')) })), results }, null, 1));
console.log(`SUMMARY devices runs=${results.length} with-fails=${results.filter(x => (x.fails || []).length || x.error).length}`);
