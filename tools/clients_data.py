"""Clients section (EN + AR): two rows of scrolling client logos.
Logos are made by tools/clients_logos.py (white marks with transparent background in assets/clients/)."""
import os
from PIL import Image

# slug, name (alt text). Order = display order; split into two rows.
CLIENTS = [
    ("ministry-of-commerce", "Ministry of Commerce, Industry and Investment Promotion"),
    ("talabat", "talabat"),
    ("muscat-university", "Muscat University"),
    ("comex", "COMEX, Oman's official technology show"),
    ("alsaada-group", "Alsaada Group"),
    ("sama-real-estate", "Sama Real Estate"),
    ("icem", "ICEM, International College of Engineering and Management"),
    ("seapearls", "seaPearls Gold and Diamond Jewellery"),
    ("bayan", "Bayan"),
    ("al-majd-cars", "Al-Majd Cars"),
    ("qsd", "Qurm Stone Development"),
    ("liquid-sky", "Liquid Sky restaurant and lounge"),
    ("al-hajis", "Al Hajis Perfumes"),
    ("gpo", "GPO Gaming PC Oman"),
    ("venice", "Venice Construction, Decor and Design"),
    ("doctor-station", "Doctor Station Dental Clinic"),
    ("lu2lu2", "Lu2Lu2 Beauty Spa"),
    ("plamore", "Plamore Manufacture"),
    ("spine-line", "Spine Line Chiropractic Care"),
    ("sip", "S.I.P Stable Investment Projects"),
    ("kely", "Kely Marketing"),
    ("cc", "CC"),
]

EN = {"eyebrow": "Our clients", "h2a": "Brands that grow", "h2b": "with io2.",
      "lead": "From government and education to retail, real estate, hospitality and technology, businesses across Oman work with io2 on their marketing.",
      "label": "Client logos"}
AR = {"eyebrow": "عملاؤنا", "h2a": "علامات تنمو", "h2b": "مع io2.",
      "lead": "من الجهات الحكومية والتعليم إلى التجزئة والعقارات والضيافة والتقنية، تعمل شركات في أنحاء عُمان مع io2 في تسويقها.",
      "label": "شعارات العملاء"}

ROOT = os.path.join(os.path.dirname(__file__), '..')
AREA = 8200  # visual size: every logo gets about the same area, so wide and square marks look balanced


def size(slug):
    w, h = Image.open(os.path.join(ROOT, 'assets', 'clients', slug + '.webp')).size
    r = w / h
    dh = min(76, (AREA / r) ** .5)
    dw = min(190, dh * r)
    return round(dw), round(dw / r)


def render(d, prefix="assets/"):
    half = (len(CLIENTS) + 1) // 2
    rows = []
    for n, row in enumerate((CLIENTS[:half], CLIENTS[half:])):
        def items(hidden):
            out = []
            for slug, name in row:
                w, h = size(slug)
                alt = '' if hidden else name
                out.append(f'<li><img src="{prefix}clients/{slug}.webp" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></li>')
            return ''.join(out)
        rows.append(f'''    <div class="clients__row{' clients__row--rev' if n else ''}">
      <ul class="clients__track">{items(False)}</ul>
      <ul class="clients__track" aria-hidden="true">{items(True)}</ul>
    </div>''')
    return f'''<section class="clients" id="clients" data-theme="dark" aria-label="{d["label"]}">
  <div class="wrap clients__head">
    <p class="eyebrow mono"><span class="idx">●</span> {d["eyebrow"]}</p>
    <h2 class="h2"><span class="split">{d["h2a"]}</span><br><span class="slash" aria-hidden="true"></span><span class="split">{d["h2b"]}</span></h2>
    <p class="lead">{d["lead"]}</p>
  </div>
  <div class="clients__rows">
{chr(10).join(rows)}
  </div>
</section>'''
