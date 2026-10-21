#!/bin/sh
# io2.agency build: minify CSS/JS into assets/build/ (cached 31 days by Cloudflare), bundle the
# self-hosted fonts and vendor libraries, stamp asset versions, regenerate the Arabic page and sitemap.
# Usage (from anywhere):  sh tools/build.sh
# Edit the sources: index.html, styles.css, rtl.css, main.js, tools/*_data.py.
# Never edit assets/build/*, ar/index.html or sitemap.xml by hand (they are generated).
set -e
cd "$(dirname "$0")/.."
ESBUILD="npx --yes esbuild@0.24.0"
V=$(date +%Y%m%d%H%M)
OUT=assets/build
mkdir -p $OUT

# 1. CSS: self-hosted fonts + site styles -> styles.min.css ; RTL overrides -> rtl.min.css
#    (paths are rewritten because the bundle lives in assets/build/)
{ sed 's#url(#url(../fonts/#g' assets/fonts/fonts.css; sed 's#url("assets/#url("../#g' styles.css; } > .bundle.tmp.css
$ESBUILD .bundle.tmp.css --minify --log-level=warning --outfile=$OUT/styles.min.css
rm -f .bundle.tmp.css
$ESBUILD rtl.css --minify --log-level=warning --outfile=$OUT/rtl.min.css

# 2. JS: vendor libraries (GSAP + ScrollTrigger + Lenis, already minified) and the site script
cat assets/vendor/gsap.min.js assets/vendor/ScrollTrigger.min.js assets/vendor/lenis.min.js > $OUT/vendor.min.js
$ESBUILD main.js --minify --log-level=warning --outfile=$OUT/main.min.js

# 3. Cache-busting version on the English page
sed -E -i '' "s#(assets/build/[a-z]+\.min\.(css|js))\?v=[0-9]+#\1?v=$V#g" index.html

# 4. Arabic page (built from index.html)
python3 tools/build_ar.py .

# 5. Sitemap (EN + AR, hreflang, images in use)
python3 tools/sitemap.py

echo "Built v$V:"; ls -la $OUT | awk 'NR>3 {print "  "$5" bytes  "$9}'
