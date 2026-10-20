#!/bin/sh
# io2.agency build: minify CSS/JS (fonts bundled in), stamp asset versions, regenerate the Arabic page.
# Usage (from anywhere):  sh tools/build.sh
# Edit the sources: index.html, styles.css, rtl.css, main.js, tools/*_data.py. Never edit *.min.* or ar/index.html by hand.
set -e
cd "$(dirname "$0")/.."
ESBUILD="npx --yes esbuild@0.24.0"
V=$(date +%Y%m%d%H%M)

# 1. CSS: self-hosted fonts + site styles -> styles.min.css ; RTL overrides -> rtl.min.css
{ sed 's#url(#url(assets/fonts/#g' assets/fonts/fonts.css; cat styles.css; } > .bundle.tmp.css
$ESBUILD .bundle.tmp.css --minify --log-level=warning --outfile=styles.min.css
rm -f .bundle.tmp.css
$ESBUILD rtl.css --minify --log-level=warning --outfile=rtl.min.css

# 2. JS
$ESBUILD main.js --minify --log-level=warning --outfile=main.min.js

# 3. Cache-busting version on the English page
sed -E -i '' "s#(styles|main)\.min\.(css|js)\?v=[0-9]+#\1.min.\2?v=$V#g" index.html

# 4. Arabic page (built from index.html)
python3 tools/build_ar.py .

# 5. Sitemap (EN + AR, hreflang, images in use)
python3 tools/sitemap.py

echo "Built v$V:"; ls -la styles.min.css rtl.min.css main.min.js | awk '{print "  "$5" bytes  "$9}'
