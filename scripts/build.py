#!/usr/bin/env python3
"""
IO2 Agency — build step.

Combines the four source files into a single self-contained homepage and
produces everything the deploy step uploads:

  dist/io2-home.html   complete page (CSS + JS inlined, images stay as files)
  dist/index.php       WordPress front controller (fast path)
  dist/io2-homepage.php  must-use plugin (durable path, survives WP updates)
  dist/robot-*.webp    image assets copied through
"""

import os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

if os.path.isdir(DIST):
    try:
        shutil.rmtree(DIST)
    except OSError:
        pass  # read-only mount in some environments; files are overwritten below
os.makedirs(DIST, exist_ok=True)


def read(name):
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        sys.exit(f"ERROR: missing source file {path}")
    with open(path, encoding='utf-8') as f:
        return f.read()


seo  = read('io2-SEO-HEAD.html')
css  = read('io2-STYLES.css')
body = read('io2-BODY.html')
js   = read('io2-SCRIPTS.js')

# ── 1. the page ───────────────────────────────────────────────────────────────
html = (
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
    + seo.strip() + '\n'
    '<style>\n' + css.strip() + '\n</style>\n'
    '</head>\n<body>\n'
    + body.strip() + '\n'
    '<script>\n' + js.strip() + '\n</script>\n'
    '</body>\n</html>\n'
)

out_html = os.path.join(DIST, 'io2-home.html')
with open(out_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"  dist/io2-home.html        {os.path.getsize(out_html):>9,} bytes")

# ── 2. assets ─────────────────────────────────────────────────────────────────
# All scene visuals are inline SVG, so the only asset is the social share card.
assets = [n for n in ('og-image.png',) if os.path.exists(os.path.join(ROOT, n))]
for n in assets:
    shutil.copy2(os.path.join(ROOT, n), os.path.join(DIST, n))
    print(f"  {n:<24} {os.path.getsize(os.path.join(DIST, n)):>9,} bytes")

# the page must not reference any file we are not shipping
refs = set(re.findall(r'(?:src|href)="(?!https?:|#|mailto:|tel:)([^"]+)"', html))
missing = sorted(r for r in refs if r not in assets)
if missing:
    sys.exit(f"ERROR: page references files that are not shipped: {missing}")
print(f"  page is self-contained ({len(refs)} local refs, all shipped)")

# ── 3. WordPress front controller (fast path) ─────────────────────────────────
index_php = """<?php
/**
 * IO2 Agency — front controller.
 *
 * Serves the static homepage at the site root and hands every other URL
 * to WordPress untouched. If a WordPress core update ever replaces this
 * file, the must-use plugin in wp-content/mu-plugins keeps the homepage
 * working, so the site cannot silently fall back to a broken template.
 */

$io2_path = strtok( $_SERVER['REQUEST_URI'] ?? '/', '?' );
$io2_home = __DIR__ . '/io2-home.html';

if ( ( $io2_path === '/' || $io2_path === '' ) && is_readable( $io2_home ) ) {
    header( 'Content-Type: text/html; charset=UTF-8' );
    header( 'X-IO2-Home: front-controller' );
    readfile( $io2_home );
    exit;
}

define( 'WP_USE_THEMES', true );
require __DIR__ . '/wp-blog-header.php';
"""
p = os.path.join(DIST, 'index.php')
with open(p, 'w', encoding='utf-8') as f:
    f.write(index_php)
print(f"  dist/index.php            {os.path.getsize(p):>9,} bytes")

# ── 4. must-use plugin (durable path) ─────────────────────────────────────────
mu_plugin = """<?php
/**
 * Plugin Name: IO2 Static Homepage
 * Description: Serves the IO2 static homepage on the front page. Lives in
 *              mu-plugins so WordPress core updates can never remove it.
 * Version:     2.0
 * Author:      IO2 Agency
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'template_redirect', function () {
    if ( is_admin() || is_feed() || is_robots() ) { return; }
    if ( ! is_front_page() && ! is_home() ) { return; }
    if ( ! empty( $_GET['io2-wp'] ) ) { return; }   // escape hatch: ?io2-wp=1

    $file = WP_CONTENT_DIR . '/io2-static/io2-home.html';
    if ( ! is_readable( $file ) ) { return; }

    if ( ! headers_sent() ) {
        header( 'Content-Type: text/html; charset=UTF-8' );
        header( 'X-IO2-Home: mu-plugin' );
    }
    readfile( $file );
    exit;
}, 0 );
"""
p = os.path.join(DIST, 'io2-homepage.php')
with open(p, 'w', encoding='utf-8') as f:
    f.write(mu_plugin)
print(f"  dist/io2-homepage.php     {os.path.getsize(p):>9,} bytes")

print("Build complete.")
