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
 * Version: 4.0
 * Built: automatically by scripts/build-plugin.py — do not edit by hand.
 */

defined('ABSPATH') || exit;

function io2_assets() {{
    static $c = null;
    if ($c) return $c;
    $c = [
        'seo'  => base64_decode('{b64(seo)}'),
        'css'  => base64_decode('{b64(css)}'),
        'body' => base64_decode('{b64(body)}'),
        'js'   => base64_decode('{b64(js)}'),
    ];
    return $c;
}}

/* ── Detect the homepage by REQUEST_URI — no is_front_page() needed ── */
function io2_is_homepage() {{
    if (is_admin() || wp_doing_ajax() || wp_doing_cron()) return false;
    if (defined('REST_REQUEST') && REST_REQUEST)          return false;
    $path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
    return ($path === '/' || $path === '');
}}

/* ── Start output buffer on muplugins_loaded (before any theme/plugin output) ── */
add_action('muplugins_loaded', 'io2_start_buffer', 0);
function io2_start_buffer() {{
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX)) return;
    ob_start('io2_filter_output');
}}

function io2_filter_output($html) {{
    /* Skip non-HTML responses (AJAX, REST, cron, empty) */
    if (!$html || strlen($html) < 200 || stripos($html, '<html') === false) {{
        return $html;
    }}

    $a = io2_assets();

    if (io2_is_homepage()) {{
        /* Homepage: replace entire output with our clean document */
        header_remove('X-IO2-Version');
        header('X-IO2-Version: 4.0');
        return implode(PHP_EOL, [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">',
            '<link rel="preconnect" href="https://fonts.googleapis.com">',
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">',
            $a['seo'],
            '<style>',
            $a['css'],
            '</style>',
            '</head>',
            '<body>',
            $a['body'],
            '<script>',
            $a['js'],
            '</script>',
            '</body>',
            '</html>',
        ]);
    }}

    /* All other pages: inject CSS into existing <head> */
    $style = '<style>' . $a['css'] . '</style>';
    return str_ireplace('</head>', $style . PHP_EOL . '</head>', $html);
}}
"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(plugin)

kb = os.path.getsize(OUT) / 1024
print(f"  → {OUT}")
print(f"  → output size: {kb:.1f} KB")
print("  Build complete.")
