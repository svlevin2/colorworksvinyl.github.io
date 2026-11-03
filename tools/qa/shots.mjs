// Full-page screenshots at 1440 and 390 for every page, plus console-error capture.
// Usage: [QA_TOOLS=/path/to/qa-tools] node tools/qa/shots.mjs <baseUrl> <outDir> [page ...]
import { createRequire } from 'module';
const require = createRequire((process.env.QA_TOOLS || '/workspace/colorworks/website/qa-tools') + '/package.json');
const puppeteer = require('puppeteer-core');
import fs from 'fs';
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const out = process.argv[3] || '/workspace/colorworks/website/qa-output/shots';
const pages = process.argv.slice(4).length ? process.argv.slice(4) : ['', 'services/indoor-wall-graphics/', 'services/storefront-signage/', 'services/vehicle-graphics/', 'services/banners-large-format/', 'services/decals-stickers/', 'services/event-decals/', 'faq/', 'privacy/', 'terms/', 'accessibility/', '404.html'];
fs.mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({ executablePath: '/home/box/.local/bin/google-chrome', args: ['--no-sandbox', '--hide-scrollbars'] });
const report = [];
for (const p of pages) {
  for (const w of [1440, 390]) {
    const page = await browser.newPage();
    const errs = [];
    page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(m.type() + ': ' + m.text()); });
    page.on('pageerror', e => errs.push('pageerror: ' + e.message));
    const notes = [];
    // A browser cancelling a responsive-image candidate (net::ERR_ABORTED) is not a broken asset; log it as a note.
    page.on('requestfailed', r => { const t = r.failure()?.errorText || ''; (t === 'net::ERR_ABORTED' ? notes : errs).push('requestfailed: ' + r.url() + ' ' + t); });
    const ext = [];
    page.on('request', r => { const u = new URL(r.url()); if (!['localhost', '127.0.0.1', new URL(base).hostname].includes(u.hostname) && !u.protocol.startsWith('data')) ext.push(r.url()); });
    await page.setViewport({ width: w, height: w === 390 ? 844 : 900, deviceScaleFactor: 1, isMobile: w === 390, hasTouch: w === 390 });
    const resp = await page.goto(base + p, { waitUntil: 'networkidle0' });
    // reveal everything so the full-page capture shows final state
    await page.evaluate(async () => {
      document.querySelectorAll('.reveal').forEach(el => el.classList.add('is-in'));
      document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; });
      for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); }
      window.scrollTo(0, 0);
      await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
    });
    await new Promise(r => setTimeout(r, 700));
    // The 404 page's own document status is logged by Chrome as a console error; that is expected, not an asset failure.
    if (resp.status() === 404) { const i = errs.indexOf('error: Failed to load resource: the server responded with a status of 404 ()'); if (i > -1) { errs.splice(i, 1); notes.push('document 404 (expected)'); } }
    const name = (p.replace(/\/$/, '').replace(/\//g, '_') || 'home') + '-' + w + '.png';
    await page.screenshot({ path: `${out}/${name}`, fullPage: true });
    const hscroll = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    const cookies = await page.cookies();
    report.push({ page: p || '/', width: w, status: resp.status(), errors: errs, external: ext, hscroll, cookies: cookies.length, notes, shot: `${out}/${name}` });
    await page.close();
  }
}
await browser.close();
fs.writeFileSync(`${out}/report.json`, JSON.stringify(report, null, 2));
for (const r of report) console.log(r.status, r.width, r.page, 'errors:', r.errors.length, 'ext:', r.external.length, 'hscroll:', r.hscroll, 'cookies:', r.cookies, r.errors.join(' | '), r.notes.length ? 'notes: ' + r.notes.join(' | ') : '');
