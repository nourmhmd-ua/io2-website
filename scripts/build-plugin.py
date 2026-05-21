#!/usr/bin/env python3
"""
Build step: reads the 4 source files and generates a self-contained
io2-mu-plugin.php with every byte of CSS/JS/HTML embedded as a PHP
string. No file I/O at runtime — no path or permission issues possible.
"""

import base64
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, 'wp-setup', 'io2-agency', 'io2-mu-plugin.php')

def read(name):
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        sys.exit(f"ERROR: {path} not found")
    with open(path, 'rb') as f:
        return f.read()

def b64(data: bytes) -> str:
    return base64.b64encode(data).decode('ascii')

seo  = read('io2-SEO-HEAD.html')
css  = read('io2-STYLES.css')
body = read('io2-BODY.html')
js   = read('io2-SCRIPTS.js')

print(f"  io2-SEO-HEAD.html  {len(seo):>7,} bytes")
print(f"  io2-STYLES.css     {len(css):>7,} bytes")
print(f"  io2-BODY.html      {len(body):>7,} bytes")
print(f"  io2-SCRIPTS.js     {len(js):>7,} bytes")

plugin = f"""<?php
/**
 * Plugin Name: IO2 Agency - Site Setup
 * Description: Self-contained homepage renderer. All assets embedded at build time.
 * Version: 3.0
 * Built: automatically by scripts/build-plugin.py — do not edit by hand.
 */

defined('ABSPATH') || exit;

/* Content is base64-encoded at build time so there are no path or
   permission dependencies at runtime. */
function io2_assets() {{
    static $cache = null;
    if ($cache !== null) return $cache;
    $cache = [
        'seo'  => base64_decode('{b64(seo)}'),
        'css'  => base64_decode('{b64(css)}'),
        'body' => base64_decode('{b64(body)}'),
        'js'   => base64_decode('{b64(js)}'),
    ];
    return $cache;
}}

/* ── HOMEPAGE: intercept and serve complete HTML document ── */
add_action('template_redirect', 'io2_serve_homepage');
function io2_serve_homepage() {{
    if (!is_front_page() || is_admin() || (defined('REST_REQUEST') && REST_REQUEST)) {{
        return;
    }}

    $a = io2_assets();

    // Clear any output WordPress or other plugins may have buffered
    while (ob_get_level()) {{
        ob_end_clean();
    }}

    header('Content-Type: text/html; charset=UTF-8');
    header('X-IO2-Version: 3.0');

    echo '<!DOCTYPE html>' . PHP_EOL;
    echo '<html lang="en">' . PHP_EOL;
    echo '<head>' . PHP_EOL;
    echo '<meta charset="UTF-8">' . PHP_EOL;
    echo '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">' . PHP_EOL;
    // Google Fonts
    echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . PHP_EOL;
    echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . PHP_EOL;
    echo '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">' . PHP_EOL;
    // SEO meta tags
    echo $a['seo'] . PHP_EOL;
    // All styles inline — no external file needed
    echo '<style>' . PHP_EOL . $a['css'] . PHP_EOL . '</style>' . PHP_EOL;
    echo '</head>' . PHP_EOL;
    echo '<body>' . PHP_EOL;
    // Page content
    echo $a['body'] . PHP_EOL;
    // Scripts before </body>
    echo '<script>' . PHP_EOL . $a['js'] . PHP_EOL . '</script>' . PHP_EOL;
    echo '</body>' . PHP_EOL;
    echo '</html>';
    exit;
}}
"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(plugin)

kb = os.path.getsize(OUT) / 1024
print(f"  → {OUT}")
print(f"  → output size: {kb:.1f} KB")
print("  Build complete.")
