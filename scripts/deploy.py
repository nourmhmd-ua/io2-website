#!/usr/bin/env python3
"""
Deploy: connects via FTP, removes old mu-plugin files, uploads the built files.
Run after scripts/build.py.

Credentials come from environment variables:
  FTP_HOST, FTP_USER, FTP_PASS
"""

import ftplib, os, sys

HOST = os.environ.get('FTP_HOST', '')
USER = os.environ.get('FTP_USER', '')
PASS = os.environ.get('FTP_PASS', '')

if not all([HOST, USER, PASS]):
    sys.exit("ERROR: FTP_HOST, FTP_USER, FTP_PASS must be set")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

# ── Connect ───────────────────────────────────────────────────────────────────
print(f"Connecting to {HOST}:21 ...")
ftp = ftplib.FTP()
ftp.connect(HOST, 21, timeout=60)
ftp.login(USER, PASS)
ftp.set_pasv(True)
print(f"  {ftp.getwelcome()}\n")

# ── 1. Remove old mu-plugin files left from previous attempts ─────────────────
OLD = [
    '/public_html/wp-content/mu-plugins/io2-agency-loader.php',
    '/public_html/wp-content/mu-plugins/io2-agency/io2-mu-plugin.php',
    '/public_html/wp-content/mu-plugins/io2-agency/io2-BODY.html',
    '/public_html/wp-content/mu-plugins/io2-agency/io2-STYLES.css',
    '/public_html/wp-content/mu-plugins/io2-agency/io2-SCRIPTS.js',
    '/public_html/wp-content/mu-plugins/io2-agency/io2-SEO-HEAD.html',
    '/public_html/io2-setup-run.php',
]
print("[1/2] Cleaning up old files...")
for path in OLD:
    try:
        ftp.delete(path)
        print(f"  deleted  {path}")
    except ftplib.error_perm:
        print(f"  skipped  {path}  (not found — ok)")

# ── 2. Upload new files ───────────────────────────────────────────────────────
UPLOADS = [
    (os.path.join(DIST, 'io2-home.html'), '/public_html/io2-home.html'),
    (os.path.join(DIST, 'index.php'),     '/public_html/index.php'),
]
print("\n[2/2] Uploading...")
for local, remote in UPLOADS:
    size = os.path.getsize(local)
    print(f"  {os.path.basename(local)} ({size:,} bytes) → {remote}")
    with open(local, 'rb') as f:
        ftp.storbinary(f'STOR {remote}', f)
    print(f"  ✓")

ftp.quit()
print("\nDone. Visit https://io2.agency/ to verify.")
