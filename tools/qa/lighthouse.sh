#!/usr/bin/env bash
# Lighthouse (mobile default + desktop preset) for each page. Usage: tools/qa/lighthouse.sh <baseUrl> <outDir> [page ...]
set -u
QA=${QA_TOOLS:-/workspace/colorworks/website/qa-tools}
BASE=${1:-http://localhost:8765/colorworksvinyl.github.io/}; OUT=${2:-/workspace/colorworks/website/qa-output/lighthouse}; shift 2 || true
PAGES=("$@"); [ ${#PAGES[@]} -eq 0 ] && PAGES=("" services/indoor-wall-graphics/ services/storefront-signage/ services/vehicle-graphics/ services/banners-large-format/ services/decals-stickers/ services/event-decals/ faq/ privacy/ terms/ accessibility/)
mkdir -p "$OUT"; export CHROME_PATH=/home/box/.local/bin/google-chrome
for p in "${PAGES[@]}"; do
  n=$(echo "${p:-home}" | tr -d '/'); [ -z "$n" ] && n=home
  for mode in mobile desktop; do
    extra=""; [ $mode = desktop ] && extra="--preset=desktop"
    node "$QA/node_modules/lighthouse/cli/index.js" "$BASE$p" $extra --quiet --chrome-flags="--headless=new --no-sandbox" \
      --output=json --output-path="$OUT/$n-$mode.json" >/dev/null 2>&1
    python3 -c "import json,sys;d=json.load(open('$OUT/$n-$mode.json'));c=d['categories'];a=d['audits'];print('$n $mode', ' '.join(f\"{k}={round(v['score']*100)}\" for k,v in c.items()), 'LCP=%s CLS=%s TBT=%s'%(a['largest-contentful-paint']['displayValue'],a['cumulative-layout-shift']['displayValue'],a['total-blocking-time']['displayValue']))"
  done
done
