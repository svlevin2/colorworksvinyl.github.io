// Captures reference sites (top 2400px at 1440) next to our Home for a side-by-side review.
// Usage: node tools/qa/benchmark.mjs <ourUrl> <outDir> <refUrl ...>
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire((process.env.QA_TOOLS || '/workspace/colorworks/website/qa-tools') + '/package.json');
const puppeteer = require('puppeteer-core');
const [ours, out, ...refs] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
const b = await puppeteer.launch({ executablePath: '/home/box/.local/bin/google-chrome', args: ['--no-sandbox', '--hide-scrollbars'] });
for (const [i, u] of [ours, ...refs].entries()) {
  const p = await b.newPage(); await p.setViewport({ width: 1440, height: 900 });
  await p.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36');
  try { await p.goto(u, { waitUntil: 'networkidle2', timeout: 45000 }); } catch (e) { console.log('timeout', u); }
  await p.evaluate(async () => { for (let y = 0; y < 2400; y += 400) { scrollTo(0, y); await new Promise(r => setTimeout(r, 250)); } scrollTo(0, 0); document.querySelectorAll('.reveal').forEach(e => e.classList.add('is-in')); });
  await new Promise(r => setTimeout(r, 1200));
  const f = `${out}/${i}-${new URL(u).hostname}.png`;
  await p.screenshot({ path: f, clip: { x: 0, y: 0, width: 1440, height: 2400 } });
  console.log(f); await p.close();
}
await b.close();
