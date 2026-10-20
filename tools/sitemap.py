"""Regenerate sitemap.xml from the built pages (EN + AR, hreflang, images actually used)."""
import re, datetime, os, xml.dom.minidom
os.chdir(os.path.join(os.path.dirname(__file__), '..'))
B = 'https://io2.agency/'

def used(f):
    return sorted(set(re.findall(r'assets/img/([\w-]+)-1440\.webp', open(f, encoding='utf-8').read())))

today = datetime.date.today().isoformat()
alt = '\n'.join(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{u}"/>'
                for l, u in (('en', B), ('ar', B + 'ar/'), ('x-default', B)))
def url(loc, prio, page):
    imgs = '\n'.join(f'    <image:image><image:loc>{B}assets/img/{n}-1440.webp</image:loc></image:image>' for n in used(page))
    return f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{prio}</priority>\n{alt}\n{imgs}\n  </url>'

out = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
       'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
       + url(B, '1.0', 'index.html') + '\n' + url(B + 'ar/', '0.9', 'ar/index.html') + '\n</urlset>\n')
open('sitemap.xml', 'w', encoding='utf-8').write(out)
xml.dom.minidom.parse('sitemap.xml')
print('sitemap.xml regenerated')
