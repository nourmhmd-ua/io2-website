<?php
/**
 * IO2 Agency — One-time WordPress setup trigger.
 * Uploaded temporarily to WP root, called via HTTPS, then deleted.
 *
 * Security: aborts unless the correct token is supplied as ?token=
 */

define('TOKEN', 'io2-setup-2025');

if (empty($_GET['token']) || $_GET['token'] !== TOKEN) {
    http_response_code(403);
    exit('Forbidden');
}

// Bootstrap WordPress
$wp_load = __DIR__ . '/wp-load.php';
if (!file_exists($wp_load)) {
    http_response_code(500);
    exit('wp-load.php not found — wrong directory?');
}
require_once $wp_load;

$log = [];

// ── 1. Read the body content from the mu-plugin's asset directory ──────────
$body_file = WP_CONTENT_DIR . '/mu-plugins/io2-agency/io2-BODY.html';
if (!file_exists($body_file)) {
    http_response_code(500);
    exit('Body file not found at: ' . $body_file);
}
$body = file_get_contents($body_file);
$log[] = 'Body file loaded (' . strlen($body) . ' bytes)';

// ── 2. Find or create the Home page ────────────────────────────────────────
$existing = get_posts([
    'post_type'      => 'page',
    'post_status'    => ['publish', 'draft'],
    'posts_per_page' => 1,
    's'              => 'Home',
    'exact'          => true,
    'title'          => 'Home',
]);

$page_args = [
    'post_title'   => 'Home',
    'post_name'    => 'home',
    'post_content' => $body,
    'post_status'  => 'publish',
    'post_type'    => 'page',
    'meta_input'   => [
        '_wp_page_template' => 'elementor_canvas',
    ],
];

if (!empty($existing)) {
    $page_args['ID'] = $existing[0]->ID;
    $page_id = wp_update_post($page_args, true);
    $log[] = 'Updated existing page ID ' . $page_args['ID'];
} else {
    $page_id = wp_insert_post($page_args, true);
    $log[] = 'Created new page ID ' . $page_id;
}

if (is_wp_error($page_id)) {
    http_response_code(500);
    exit('Page error: ' . $page_id->get_error_message());
}

// ── 3. Set the Elementor Canvas template explicitly via update_post_meta ───
update_post_meta($page_id, '_wp_page_template', 'elementor_canvas');
$log[] = 'Elementor Canvas template applied';

// ── 4. Set as static front page ────────────────────────────────────────────
update_option('show_on_front', 'page');
update_option('page_on_front', $page_id);
$log[] = 'Set as static front page (show_on_front=page, page_on_front=' . $page_id . ')';

// ── 5. Mark the mu-plugin init as done (so it won't overwrite later) ───────
update_option('io2_setup_done_v1', true);
$log[] = 'Marked io2_setup_done_v1 = true';

// ── 6. Self-delete ─────────────────────────────────────────────────────────
@unlink(__FILE__);
$log[] = 'Setup script deleted';

// ── Output result ──────────────────────────────────────────────────────────
header('Content-Type: application/json');
echo json_encode([
    'status'  => 'success',
    'page_id' => $page_id,
    'log'     => $log,
], JSON_PRETTY_PRINT);
