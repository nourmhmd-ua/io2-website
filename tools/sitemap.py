"""Regenerate sitemap.xml from the built pages (EN + AR pairs with hreflang, images actually used)."""
import re, datetime, os, sys, xml.dom.minidom
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, 'tools')
from services_data import SLUGS
from service_pages_data import ORDER
B = 'https://io2.agency/'

def used(f):
    return sorted(set(re.findall(r'assets/img/([\w-]+)-1440\.webp', open(f, encoding='utf-8').read())))

today = datetime.date.today().isoformat()

def url(loc, prio, page, en, ar):
    alt = '\n'.join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{u}"/>'
                    for l, u in (('en', en), ('ar', ar), ('x-default', en)))
    imgs = ''.join(f'\n    <image:image><image:loc>{B}assets/img/{n}-1440.webp</image:loc></image:image>' for n in used(page))
    return f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n{alt}{imgs}\n  </url>'

# (path without language prefix, EN priority, AR priority)
PAGES = [('', '1.0', '0.9'), ('services/', '0.8', '0.7')] + [(f'services/{SLUGS[k]}/', '0.8', '0.7') for k in ORDER]
urls = []
for p, pe, pa in PAGES:
    en, ar = B + p, B + 'ar/' + p
    urls.append(url(en, pe, p + 'index.html', en, ar))
    urls.append(url(ar, pa, 'ar/' + p + 'index.html', en, ar))

out = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
       'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
       + '\n'.join(urls) + '\n</urlset>\n')
open('sitemap.xml', 'w', encoding='utf-8').write(out)
xml.dom.minidom.parse('sitemap.xml')
print(f'sitemap.xml regenerated ({len(urls)} URLs)')
