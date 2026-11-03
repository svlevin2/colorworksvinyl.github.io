#!/usr/bin/env bash
# Full scripted QA. Usage: tools/qa/run_all.sh [baseUrl]   (serve first: cd /tmp/serve && python3 -m http.server 8765, with
# /tmp/serve/colorworksvinyl.github.io -> this folder, to mimic the github.io project path)
cd "$(dirname "$0")/../.."
BASE=${1:-http://localhost:8765/colorworksvinyl.github.io/}
OUT=/workspace/colorworks/website/qa-output
python3 tools/build.py >/dev/null
python3 tools/qa/check_text.py | grep -E 'SUMMARY|FAIL|WARN'
python3 tools/qa/contrast.py | tail -1
tools/qa/links.sh "$BASE" | tail -3
node tools/qa/axe.mjs "$BASE" | grep -E 'SUMMARY|^  -'
node tools/qa/shots.mjs "$BASE" "$OUT/shots" | awk '{e+=$5; x+=$7} END {print "SUMMARY shots console-errors=" e " external-requests=" x}'
tools/qa/lighthouse.sh "$BASE" "$OUT/lighthouse"
tools/qa/seo_copy.sh >/dev/null && tools/qa/lighthouse.sh "$(echo "$BASE" | sed 's#colorworksvinyl.github.io/#seo-test/#')" "$OUT/lighthouse-seo-copy" | sed 's/^/no-noindex copy: /'
python3 "$(dirname "$0")/contact_sheet.py" "${OUT:-/workspace/colorworks/website/qa-output}/shots" "${OUT:-/workspace/colorworks/website/qa-output}/contact-sheet-local.png"
