<?php
/**
 * Plugin Name: IO2 Agency Loader
 * Description: Loads the IO2 Agency mu-plugin from its subdirectory.
 * Version: 1.0
 *
 * WordPress only auto-loads PHP files directly in mu-plugins/, not subdirectories.
 * This loader bridges that gap.
 */

defined('ABSPATH') || exit;

require_once __DIR__ . '/io2-agency/io2-mu-plugin.php';
