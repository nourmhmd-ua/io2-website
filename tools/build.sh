#!/bin/sh
# io2.agency build: minify CSS/JS into assets/build/ (cached 31 days by Cloudflare), bundle the
# self-hosted fonts and vendor libraries, stamp asset versions, regenerate the Arabic page and sitemap.
# Usage (from anywhere):  sh tools/build.sh
# Edit the sources: index.html, styles.css, rtl.css, main.js, tools/*_data.py.
# Never edit assets/build/*, ar/index.html, services/, ar/services/ or sitemap.xml by hand (they are generated).
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

# 2. JS: vendor libraries (GSAP + ScrollTrigger, already minified) and the site script
cat assets/vendor/gsap.min.js assets/vendor/ScrollTrigger.min.js > $OUT/vendor.min.js
$ESBUILD main.js --minify --log-level=warning --outfile=$OUT/main.min.js
$ESBUILD page.js --minify --log-level=warning --outfile=$OUT/page.min.js   # service pages (no GSAP)

# 3. English services grid from tools/services_data.py, then cache-busting version on the English page
python3 -c "import re,sys; sys.path.insert(0,'tools'); from services_data import EN,render; from clients_data import EN as CE, render as rc; from work_data import EN as WE, render as rw; p='index.html'; h=open(p,encoding='utf-8').read(); h,n=re.subn(r'<section class=\"services\".*?</section>', lambda m: render(EN), h, count=1, flags=re.S); h,k=re.subn(r'<section class=\"clients\".*?</section>', lambda m: rc(CE), h, count=1, flags=re.S); h,j=re.subn(r'<section class=\"work\".*?</section>', lambda m: rw(WE), h, count=1, flags=re.S); assert n==1 and k==1 and j==1; open(p,'w',encoding='utf-8').write(h)"
sed -E -i '' "s#(assets/build/[a-z]+\.min\.(css|js))\?v=[0-9]+#\1?v=$V#g" index.html

# 4. Arabic page (built from index.html)
python3 tools/build_ar.py .

# 5. Service pages (/services/..., /ar/services/...), built from the home pages' nav and footer
python3 tools/build_services.py

# 6. Sitemap (all pages, hreflang pairs, images in use)
python3 tools/sitemap.py

echo "Built v$V:"; ls -la $OUT | awk 'NR>3 {print "  "$5" bytes  "$9}'
