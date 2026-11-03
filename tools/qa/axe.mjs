// axe-core WCAG 2.2 AA scan at 1440 and 390 for each page. Usage: node tools/qa/axe.mjs <baseUrl> [page ...]
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire((process.env.QA_TOOLS || '/workspace/colorworks/website/qa-tools') + '/package.json');
const puppeteer = require('puppeteer-core');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');
const base = process.argv[2] || 'http://localhost:8765/colorworksvinyl.github.io/';
const pages = process.argv.slice(3).length ? process.argv.slice(3) : ['', 'business-signage/', 'stickers-decals/', 'events/', 'faq/', 'privacy/', 'terms/', 'accessibility/', '404.html'];
const b = await puppeteer.launch({ executablePath: '/home/box/.local/bin/google-chrome', args: ['--no-sandbox'] });
let total = 0;
for (const p of pages) for (const w of [1440, 390]) {
  const pg = await b.newPage(); await pg.setViewport({ width: w, height: 900 });
  await pg.goto(base + p, { waitUntil: 'networkidle0' });
  await pg.evaluate(() => document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')));
  await new Promise(r => setTimeout(r, 800));
  await pg.evaluate(axeSrc);
  const res = await pg.evaluate(() => axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'] } }));
  total += res.violations.length;
  console.log(`${p || '/'} @${w}: violations=${res.violations.length} passes=${res.passes.length} incomplete=${res.incomplete.length}`);
  for (const v of res.violations) console.log('  -', v.id, v.impact, v.nodes.length, v.nodes.slice(0, 3).map(n => n.target.join(' ')).join(' | '));
  for (const v of res.incomplete.filter(v => v.id === 'color-contrast')) console.log('  ? contrast needs review on', v.nodes.length, 'nodes');
  await pg.close();
}
await b.close();
console.log('SUMMARY axe violations total=' + total);
process.exit(total ? 1 : 0);
