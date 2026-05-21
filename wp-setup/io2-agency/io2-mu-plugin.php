<?php
/**
 * Plugin Name: IO2 Agency - Site Setup
 * Description: Serves the IO2 homepage as a complete styled HTML document.
 * Version: 2.0
 */

defined('ABSPATH') || exit;

// __DIR__ is always the real filesystem path of this file — no path guessing.
define('IO2_DIR', __DIR__ . '/');

/* ── HOMEPAGE: intercept and serve complete styled HTML ── */
add_action('template_redirect', 'io2_serve_homepage');
function io2_serve_homepage() {
    // Only fire on the front page, never in admin or REST API
    if (!is_front_page() || is_admin() || (defined('REST_REQUEST') && REST_REQUEST)) {
        return;
    }

    $dir   = IO2_DIR;
    $seo   = @file_get_contents($dir . 'io2-SEO-HEAD.html');
    $css   = @file_get_contents($dir . 'io2-STYLES.css');
    $body  = @file_get_contents($dir . 'io2-BODY.html');
    $js    = @file_get_contents($dir . 'io2-SCRIPTS.js');

    // Bail gracefully if any file is missing so WP renders normally
    if (!$css || !$body) {
        return;
    }

    // Suppress any output already buffered by WordPress or other plugins
    while (ob_get_level()) {
        ob_end_clean();
    }

    header('Content-Type: text/html; charset=UTF-8');
    header('X-IO2-Rendered: true');

    echo '<!DOCTYPE html>' . "\n";
    echo '<html lang="en">' . "\n";
    echo '<head>' . "\n";
    echo '<meta charset="UTF-8">' . "\n";
    echo '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">' . "\n";

    // Google Fonts
    echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
    echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
    echo '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">' . "\n";

    // SEO tags
    if ($seo) {
        echo "\n<!-- IO2: SEO -->\n" . $seo . "\n";
    }

    // All CSS inline in <style>
    echo "\n<style>\n" . $css . "\n</style>\n";

    echo '</head>' . "\n";
    echo '<body>' . "\n";

    // Page content
    echo $body . "\n";

    // JS before </body>
    echo "\n<script>\n" . $js . "\n</script>\n";

    echo '</body>' . "\n";
    echo '</html>';

    exit;
}

/* ── NON-HOMEPAGE PAGES: still inject CSS/JS via hooks ── */
add_action('wp_head', 'io2_inject_head', 1);
function io2_inject_head() {
    if (is_front_page()) return; // handled by template_redirect above
    $dir = IO2_DIR;
    $css = @file_get_contents($dir . 'io2-STYLES.css');
    if ($css) {
        echo "\n<style>\n" . $css . "\n</style>\n";
    }
}

add_action('wp_footer', 'io2_inject_footer', 99);
function io2_inject_footer() {
    if (is_front_page()) return;
    $dir = IO2_DIR;
    $js = @file_get_contents($dir . 'io2-SCRIPTS.js');
    if ($js) {
        echo "\n<script>\n" . $js . "\n</script>\n";
    }
}
