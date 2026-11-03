# ColorWorks Vinyl website (pre-launch preview)

Hand-coded static site for GitHub Pages. Pages are noindex and robots.txt disallows all until launch.

- Edit pages in src/pages, shared parts in src/partials, styles in assets/css/styles.css, script in assets/js/main.js.
- Build: `python3 tools/build.py` (writes index.html, the page folders, 404.html, robots.txt, sitemap.xml, .nojekyll).
- Assets: `python3 tools/prep_assets.py` regenerates fonts, images and icons from the brand kit sources.
- QA: serve a copy at a github.io-like path, then run `tools/qa/run_all.sh`:
  `mkdir -p /tmp/serve && ln -sfn "$PWD" /tmp/serve/colorworksvinyl.github.io && (cd /tmp/serve && python3 -m http.server 8765)`
  QA needs the Node tools in /workspace/colorworks/website/qa-tools (puppeteer-core, lighthouse, axe-core, linkinator), or set QA_TOOLS.
- Products: src/data/products.py (16 pages, template src/partials/product.html). Examples: src/data/examples.py, EXAMPLES_APPROVED = True (COO - CW approved 2026-11-03 10:37 CT, text as in e3d634c); 5 per product page, gradient icon tiles until each ex-<slug>-<n> photo lands. `python3 tools/examples_md.py` regenerates the approved text record. QA extras: tools/qa/final_data.py (business-days, Fast turn-around, breadcrumb/JSON-LD tables), tools/qa/shots_phone_full.mjs (WebKit 390 full-page shots).
- Launch checklist: remove the noindex meta in src/partials/head.html, change robots.txt in tools/build.py, finish the legal drafts.
