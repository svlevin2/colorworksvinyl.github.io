#!/usr/bin/env bash
# Recursive link check of the served site (internal links and assets). mailto/tel skipped; external links listed but not fetched.
QA=${QA_TOOLS:-/workspace/colorworks/website/qa-tools}
BASE=${1:-http://localhost:8765/colorworksvinyl.github.io/}
node "$QA/node_modules/linkinator/build/src/cli.js" "$BASE" --recurse --skip '^(mailto|tel):' --skip '^https?://(?!localhost)' --format csv > /tmp/links.csv 2>/tmp/links.err
total=$(($(wc -l < /tmp/links.csv)-1)); broken=$(grep -c ',BROKEN,' /tmp/links.csv || true); skipped=$(grep -c ',SKIPPED,' /tmp/links.csv || true)
grep ',BROKEN,' /tmp/links.csv
echo "SUMMARY links checked=$total broken=$broken skipped=$skipped"
[ "$broken" = 0 ]
