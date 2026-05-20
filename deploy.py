#!/usr/bin/env python3
"""
IO2 Agency — WordPress FTP Deployment Script
Connects via FTP and sets up the WordPress site.
"""

import ftplib
import os
import time
import sys

# ── Credentials ──────────────────────────────────────────
FTP_HOST = "195.35.10.250"
FTP_PORT = 21
FTP_USER = "u595982465.io2.agency"
FTP_PASS = "Noor.1995NM"            # without brackets (try first)
WP_PATH  = "/public_html"
# ─────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FILES_TO_UPLOAD = {
    "io2-BODY.html":    os.path.join(SCRIPT_DIR, "io2-BODY.html"),
    "io2-STYLES.css":   os.path.join(SCRIPT_DIR, "io2-STYLES.css"),
    "io2-SCRIPTS.js":   os.path.join(SCRIPT_DIR, "io2-SCRIPTS.js"),
    "io2-SEO-HEAD.html":os.path.join(SCRIPT_DIR, "io2-SEO-HEAD.html"),
    "io2-mu-plugin.php":os.path.join(SCRIPT_DIR, "io2-mu-plugin.php"),
}

MU_PLUGIN_DIR = f"{WP_PATH}/wp-content/mu-plugins/io2-agency"
MU_PLUGIN_FILE = f"{WP_PATH}/wp-content/mu-plugins/io2-agency.php"  # loader


def connect_ftp(use_tls=False):
    if use_tls:
        ftp = ftplib.FTP_TLS()
    else:
        ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT, timeout=30)
    ftp.login(FTP_USER, FTP_PASS)
    if use_tls:
        ftp.prot_p()
    ftp.set_pasv(True)
    print(f"  Connected ({'FTPS' if use_tls else 'FTP'}): {ftp.getwelcome()}")
    return ftp


def ensure_dir(ftp, path):
    """Create directory recursively if it doesn't exist."""
    parts = path.split("/")
    current = ""
    for part in parts:
        if not part:
            continue
        current += "/" + part
        try:
            ftp.mkd(current)
            print(f"  Created dir: {current}")
        except ftplib.error_perm:
            pass  # already exists


def upload_file(ftp, local_path, remote_path, label=None):
    size = os.path.getsize(local_path)
    label = label or os.path.basename(local_path)
    print(f"  Uploading {label} ({size:,} bytes) → {remote_path}")
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f)
    print(f"    ✓ Done")


def upload_string(ftp, content, remote_path, label=None):
    import io
    data = content.encode("utf-8")
    label = label or os.path.basename(remote_path)
    print(f"  Uploading {label} ({len(data):,} bytes) → {remote_path}")
    ftp.storbinary(f"STOR {remote_path}", io.BytesIO(data))
    print(f"    ✓ Done")


def dir_exists(ftp, path):
    try:
        ftp.cwd(path)
        ftp.cwd("/")
        return True
    except ftplib.error_perm:
        return False


def main():
    print("\n═══════════════════════════════════════")
    print("  IO2 Agency — WordPress FTP Deployment")
    print("═══════════════════════════════════════\n")

    ftp = None

    # Try plain FTP first, then FTPS
    for use_tls in [False, True]:
        try:
            print(f"Connecting to {FTP_HOST}:{FTP_PORT} ({'FTPS' if use_tls else 'FTP'})...")
            ftp = connect_ftp(use_tls=use_tls)
            break
        except Exception as e:
            print(f"  Failed: {e}")
            if use_tls:
                print("Could not connect via FTP or FTPS. Aborting.")
                sys.exit(1)
            print("  Trying FTPS...")

    # ── 1. Explore WordPress structure ──────────────────
    print("\n[1/4] Verifying WordPress installation...")
    try:
        ftp.cwd(WP_PATH)
        files = ftp.nlst()
        wp_files = [f for f in files if "wp-" in f or "wp-config" in f]
        print(f"  Found in {WP_PATH}: {', '.join(wp_files[:8])}")
    except Exception as e:
        print(f"  Warning: {e}")

    # ── 2. Create mu-plugins/io2-agency/ directory ──────
    print("\n[2/4] Creating mu-plugin directory...")
    ensure_dir(ftp, f"{WP_PATH}/wp-content/mu-plugins")
    ensure_dir(ftp, MU_PLUGIN_DIR)

    # ── 3. Upload content files ─────────────────────────
    print("\n[3/4] Uploading asset files...")
    asset_files = ["io2-BODY.html", "io2-STYLES.css", "io2-SCRIPTS.js", "io2-SEO-HEAD.html"]
    for fname in asset_files:
        local = FILES_TO_UPLOAD[fname]
        remote = f"{MU_PLUGIN_DIR}/{fname}"
        upload_file(ftp, local, remote)

    # ── 4. Upload the mu-plugin PHP file ────────────────
    print("\n[4/4] Uploading must-use plugin...")
    upload_file(ftp, FILES_TO_UPLOAD["io2-mu-plugin.php"],
                f"{MU_PLUGIN_DIR}/io2-mu-plugin.php")

    # Create the loader file in mu-plugins root (WordPress only auto-loads
    # PHP files directly in mu-plugins/, not subdirectories)
    loader = """<?php
/**
 * IO2 Agency Loader — auto-loads the plugin from subdirectory
 */
require_once __DIR__ . '/io2-agency/io2-mu-plugin.php';
"""
    upload_string(ftp, loader, MU_PLUGIN_FILE, "io2-agency-loader.php")

    ftp.quit()

    print("\n═══════════════════════════════════════")
    print("  Deployment complete!")
    print("═══════════════════════════════════════")
    print()
    print("Next steps:")
    print("  1. Visit your WordPress site — the Home page will be created")
    print("     automatically on first page load (via the mu-plugin init hook).")
    print("  2. The site front page will be set to the new 'Home' page.")
    print("  3. CSS, SEO tags, and JS are injected on every page.")
    print()
    print("If the page already existed, it will be updated with the new content.")
    print()


if __name__ == "__main__":
    main()
