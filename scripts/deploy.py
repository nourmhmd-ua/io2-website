#!/usr/bin/env python3
"""
IO2 Agency — deploy step. Uploads dist/ to the WordPress host over FTP.

Two independent mechanisms keep the homepage alive:
  1. /public_html/index.php                          — fast path, no WP boot
  2. /public_html/wp-content/mu-plugins/io2-homepage.php — survives core updates

Credentials come from the repository secrets FTP_HOST / FTP_USERNAME / FTP_PASSWORD.
"""

import ftplib, os, sys

HOST = os.environ.get('FTP_HOST', '')
USER = os.environ.get('FTP_USER', '')
PASS = os.environ.get('FTP_PASS', '')
if not all([HOST, USER, PASS]):
    sys.exit("ERROR: FTP_HOST, FTP_USER and FTP_PASS must be set")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')
WEB  = '/public_html'

print(f"Connecting to {HOST}:21 ...")
ftp = ftplib.FTP()
ftp.connect(HOST, 21, timeout=90)
ftp.login(USER, PASS)
ftp.set_pasv(True)
print(f"  {ftp.getwelcome()}\n")


def ensure_dir(path):
    """mkdir -p over FTP"""
    parts, cur = [p for p in path.split('/') if p], ''
    for part in parts:
        cur += '/' + part
        try:
            ftp.mkd(cur)
            print(f"  created dir  {cur}")
        except ftplib.error_perm:
            pass  # already exists


def put(local, remote):
    size = os.path.getsize(local)
    with open(local, 'rb') as f:
        ftp.storbinary(f'STOR {remote}', f, blocksize=32768)
    print(f"  ✓ {os.path.basename(local):<22} {size:>9,} b  →  {remote}")


# ── 1. remove files from earlier, abandoned approaches ───────────────────────
STALE = [
    f'{WEB}/wp-content/mu-plugins/io2-agency-loader.php',
    f'{WEB}/wp-content/mu-plugins/io2-agency/io2-mu-plugin.php',
    f'{WEB}/wp-content/mu-plugins/io2-agency/io2-BODY.html',
    f'{WEB}/wp-content/mu-plugins/io2-agency/io2-STYLES.css',
    f'{WEB}/wp-content/mu-plugins/io2-agency/io2-SCRIPTS.js',
    f'{WEB}/wp-content/mu-plugins/io2-agency/io2-SEO-HEAD.html',
    f'{WEB}/io2-setup-run.php',
    f'{WEB}/io2-img-01.png',
    f'{WEB}/io2-img-02.png',
]
print("[1/4] Removing stale files from previous approaches...")
for path in STALE:
    try:
        ftp.delete(path)
        print(f"  deleted  {path}")
    except ftplib.error_perm:
        pass

# ── 2. directories ───────────────────────────────────────────────────────────
print("\n[2/4] Ensuring directories...")
ensure_dir(f'{WEB}/wp-content/mu-plugins')
ensure_dir(f'{WEB}/wp-content/io2-static')

# ── 3. page + server glue ────────────────────────────────────────────────────
print("\n[3/4] Uploading page and handlers...")
put(os.path.join(DIST, 'io2-home.html'),    f'{WEB}/io2-home.html')
put(os.path.join(DIST, 'io2-home.html'),    f'{WEB}/wp-content/io2-static/io2-home.html')
put(os.path.join(DIST, 'index.php'),        f'{WEB}/index.php')
put(os.path.join(DIST, 'io2-homepage.php'), f'{WEB}/wp-content/mu-plugins/io2-homepage.php')

# ── 4. images ────────────────────────────────────────────────────────────────
print("\n[4/4] Uploading image assets...")
imgs = sorted(n for n in os.listdir(DIST) if n.endswith('.webp'))
for n in imgs:
    put(os.path.join(DIST, n), f'{WEB}/{n}')

ftp.quit()
print(f"\nDone — {len(imgs)} images + 4 files uploaded. Visit https://io2.agency/")
