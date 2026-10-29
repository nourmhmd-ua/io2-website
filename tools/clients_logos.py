"""Turn the client logos in ../io2 portfolio/logos into clean, transparent, single-colour (white) WebP marks.
Background is removed by colour keying (or gold keying / existing alpha), then the mark is upscaled with
smoothed edges so small source files stay sharp on retina screens. Output: assets/clients/<slug>.webp
Usage: python3 tools/clients_logos.py   (needs Pillow + numpy)"""
import os, numpy as np
from PIL import Image, ImageFilter
SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'io2 portfolio', 'logos')
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'clients')
BOX = (560, 200)  # 2x the largest display size

# slug, file, mode, crop
LOGOS = [
    ("venice", "14.webp", "alpha", None),
    ("bayan", "775b08_b868477ffb6f46cda08016d03bb980c8~mv2.jpg", "key", None),
    ("sip", "Black-And-White-Illustrative-Furniture-Logo-1-3.webp", "alpha", None),
    ("comex", "images (1).jpeg", "key-soft", (225, 90, 765, 280)),  # larger file; "32nd edition" cropped off
    ("doctor-station", "IMG_8096.PNG", "key", (0, 790, 1284, 1640)),
    ("al-majd-cars", "IMG_8097.PNG", "gold", (100, 840, 1185, 1925)),
    ("alsaada-group", "Logo 2.png", "alpha+black", None),
    ("cc", "channels4_profile.jpg", "key", (120, 200, 780, 700)),
    ("ministry-of-commerce", "images (1) copy.jpeg", "key", None),
    ("sama-real-estate", "images (1).png", "key", None),
    ("liquid-sky", "images (2) copy.jpeg", "key", None),
    ("lu2lu2", "images (2).jpeg", "key", None),
    ("al-hajis", "images (3).jpeg", "key", None),
    ("gpo", "images (4).jpeg", "key", None),
    ("qsd", "images copy.jpeg", "key", None),
    ("muscat-university", "images copy.png", "key", None),
    ("seapearls", "images.jpeg", "key", None),
    ("icem", "images.png", "key", None),
    ("kely", "logo (1).png", "alpha", None),
    ("spine-line", "logo-spine-line.png", "alpha", None),
    ("plamore", "logo.png", "alpha", None),
    ("talabat", "talabat-oman-430x430.webp", "key", None),
]

def smooth(x, a, b):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)

def mask(im, mode):
    rgba = np.asarray(im.convert('RGBA')).astype(np.float32)
    rgb, a0 = rgba[..., :3], rgba[..., 3] / 255
    if mode == 'alpha':
        return a0
    if mode == 'alpha+black':
        return a0 * smooth(np.linalg.norm(rgb, axis=2), 60, 140)
    if mode == 'gold':
        mx, mn = rgb.max(2), rgb.min(2)
        sat = (mx - mn) / np.maximum(mx, 1)
        return smooth(sat * mx / 255, .14, .32)
    border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    bg = np.median(border, axis=0)
    lo, hi = (10, 45) if mode == 'key-soft' else (22, 95)  # soft: light gradients inside the mark
    return smooth(np.linalg.norm(rgb - bg, axis=2), lo, hi)

os.makedirs(OUT, exist_ok=True)
for slug, f, mode, crop in LOGOS:
    im = Image.open(os.path.join(SRC, f))
    if crop: im = im.crop(crop)
    a = Image.fromarray((mask(im, mode) * 255).astype(np.uint8))
    if mode == 'key-soft': a = a.filter(ImageFilter.MedianFilter(3))  # JPEG speckle
    bb = a.point(lambda v: 255 if v > 24 else 0).getbbox()
    a = a.crop(bb)
    w, h = a.size
    s = min(BOX[0] / w, BOX[1] / h)
    a = a.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    if s > 1.3:  # upscaled: soften the stair-steps, then re-sharpen the edge
        a = a.filter(ImageFilter.GaussianBlur(min(2.5, s * .3)))
        a = a.point(lambda v: int(max(0, min(255, (v - 128) * 1.9 + 128))))
    out = Image.new('RGBA', a.size, (255, 255, 255, 0))
    out.putalpha(a)
    out = Image.composite(Image.new('RGBA', a.size, (255, 255, 255, 255)), out, a)
    out.save(os.path.join(OUT, slug + '.webp'), 'WEBP', lossless=True, quality=100, method=6)
    print(f'{slug:22s} {mode:12s} src {w}x{h} -> {a.size[0]}x{a.size[1]} (x{s:.1f})')
