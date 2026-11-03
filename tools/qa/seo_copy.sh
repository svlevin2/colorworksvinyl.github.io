#!/usr/bin/env bash
# Makes a throwaway copy without noindex and with an allow-all robots.txt, to read the launch-day Lighthouse SEO score.
# Serves under the same local server: <server>/seo-test/ . Never deploy this copy.
set -e
SRC=$(cd "$(dirname "$0")/../.." && pwd); DST=/tmp/serve/seo-test
rm -rf "$DST" && mkdir -p "$DST" && cp -r "$SRC"/. "$DST"/ && rm -rf "$DST/.git"
find "$DST" -name '*.html' -exec sed -i 's#<meta name="robots" content="noindex, nofollow">##' {} +
printf 'User-agent: *\nAllow: /\n' > "$DST/robots.txt"
echo "$DST"
