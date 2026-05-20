<?php
/**
 * Plugin Name: IO2 Agency - Site Setup
 * Description: Injects custom CSS, SEO meta, Google Fonts, JS and creates the Home page with Elementor Canvas template.
 * Version: 1.0
 */

defined('ABSPATH') || exit;

define('IO2_DIR', WPMU_PLUGIN_DIR . '/io2-agency/');

/* ── HEAD: Google Fonts + SEO tags + CSS ── */
add_action('wp_head', 'io2_inject_head', 1);
function io2_inject_head() {
    // Google Fonts (also present in SEO file preconnects, but adding the stylesheet here)
    echo "\n<!-- IO2: Google Fonts -->\n";
    echo '<link rel="preconnect" href="https://fonts.googleapis.com">' . "\n";
    echo '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' . "\n";
    echo '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">' . "\n";

    // SEO meta tags
    $seo = IO2_DIR . 'io2-SEO-HEAD.html';
    if (file_exists($seo)) {
        echo "\n<!-- IO2: SEO -->\n";
        echo file_get_contents($seo) . "\n";
    }

    // Custom CSS
    $css = IO2_DIR . 'io2-STYLES.css';
    if (file_exists($css)) {
        echo "\n<!-- IO2: Styles -->\n<style>\n";
        echo file_get_contents($css);
        echo "\n</style>\n";
    }
}

/* ── FOOTER: JS before </body> ── */
add_action('wp_footer', 'io2_inject_footer', 99);
function io2_inject_footer() {
    $js = IO2_DIR . 'io2-SCRIPTS.js';
    if (file_exists($js)) {
        echo "\n<!-- IO2: Scripts -->\n<script>\n";
        echo file_get_contents($js);
        echo "\n</script>\n";
    }
}

/* ── INIT: Create Home page once ── */
add_action('init', 'io2_setup_homepage');
function io2_setup_homepage() {
    if (get_option('io2_setup_done_v1')) return;

    $body_file = IO2_DIR . 'io2-BODY.html';
    if (!file_exists($body_file)) return;

    $body = file_get_contents($body_file);

    // Find or create the Home page
    $existing = get_posts([
        'post_type'   => 'page',
        'post_status' => ['publish', 'draft'],
        'title'       => 'Home',
        'numberposts' => 1,
    ]);

    $page_args = [
        'post_title'    => 'Home',
        'post_name'     => 'home',
        'post_content'  => $body,
        'post_status'   => 'publish',
        'post_type'     => 'page',
        'meta_input'    => [
            '_wp_page_template' => 'elementor_canvas',
        ],
    ];

    if (!empty($existing)) {
        $page_args['ID'] = $existing[0]->ID;
        $page_id = wp_update_post($page_args, true);
    } else {
        $page_id = wp_insert_post($page_args, true);
    }

    if (is_wp_error($page_id) || !$page_id) return;

    // Set as static front page
    update_option('show_on_front', 'page');
    update_option('page_on_front', $page_id);

    // Mark done so this only runs once
    update_option('io2_setup_done_v1', true);
}
