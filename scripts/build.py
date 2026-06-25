#!/usr/bin/env python3
"""
Build: combines the 4 source files into:
  dist/io2-home.html  — complete self-contained page (all CSS/JS inline)
  dist/index.php      — WordPress front controller with homepage check
"""

import base64, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
os.makedirs(DIST, exist_ok=True)

def read(name):
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        sys.exit(f"ERROR: {path} not found")
    with open(path, encoding='utf-8') as f:
        return f.read()

seo  = read('io2-SEO-HEAD.html')   # already contains charset, viewport, Google Fonts
css  = read('io2-STYLES.css')
body = read('io2-BODY.html')
js   = read('io2-SCRIPTS.js')

# ── 0. Extract large base64 images → real files ──────────────────────────────
# 38 KB+ data URIs in <img src="..."> can fail in browsers/servers. We pull
# each one out, save it as a PNG, and replace the src with a plain file path.
def extract_images(html):
    counter = [0]
    def replace(m):
        mime   = m.group(1)   # e.g. "image/png"
        b64    = m.group(2)
        ext    = mime.split('/')[-1].split('+')[0]  # png, jpeg, svg, webp …
        counter[0] += 1
        fname  = f'io2-img-{counter[0]:02d}.{ext}'
        fpath  = os.path.join(DIST, fname)
        with open(fpath, 'wb') as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(fpath) / 1024
        print(f'  extracted /{fname}  ({size_kb:.0f} KB)')
        return f'src="/{fname}"'
    # Only extract large data URIs (>5 KB encoded = >3.75 KB decoded)
    pattern = r'src="data:(image/[^;]+);base64,([A-Za-z0-9+/=]{5000,})"'
    return re.sub(pattern, replace, html)

body = extract_images(body)

# ── 1. Complete standalone HTML page ─────────────────────────────────────────
html = (
    '<!DOCTYPE html>\n'
    '<html lang="en">\n'
    '<head>\n'
    + seo + '\n'
    '<style>\n' + css + '\n</style>\n'
    '</head>\n'
    '<body>\n'
    + body + '\n'
    '<script>\n' + js + '\n</script>\n'
    '</body>\n'
    '</html>\n'
)

out_html = os.path.join(DIST, 'io2-home.html')
with open(out_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"  dist/io2-home.html   {os.path.getsize(out_html):>9,} bytes")

# ── 2. WordPress front controller with homepage intercept ─────────────────────
index_php = """\
<?php
/**
 * IO2 Agency – WordPress front controller.
 *
 * Intercepts the root URL and serves the static homepage directly.
 * All other URLs are handled by WordPress as normal.
 */

$path = strtok( $_SERVER['REQUEST_URI'] ?? '/', '?' );
if ( $path === '/' || $path === '' ) {
    header( 'Content-Type: text/html; charset=UTF-8' );
    readfile( __DIR__ . '/io2-home.html' );
    exit;
}

define( 'WP_USE_THEMES', true );
require __DIR__ . '/wp-blog-header.php';
"""

out_php = os.path.join(DIST, 'index.php')
with open(out_php, 'w', encoding='utf-8') as f:
    f.write(index_php)
print(f"  dist/index.php       {os.path.getsize(out_php):>9,} bytes")
print("Build complete.")
