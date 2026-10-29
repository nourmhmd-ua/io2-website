"""Generate the service pages from tools/service_pages_data.py:
  /services/index.html, /services/<slug>/index.html      (English)
  /ar/services/index.html, /ar/services/<slug>/index.html (Arabic, RTL)
Nav, menu and footer are copied from the built index.html / ar/index.html so they never drift.
Run after build_ar.py (build.sh does this)."""
import html, json, os, re, shutil
from urllib.parse import quote
from services_data import ICONS, EN as SVC_EN, AR as SVC_AR, SLUGS
from service_pages_data import ORDER, UI, PAGES

os.chdir(os.path.join(os.path.dirname(__file__), '..'))
SITE = 'https://io2.agency'
WA = 'https://wa.me/96877220770?text='
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
COUNTRIES = ["Oman", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Bahrain"]

SRC = {'en': open('index.html', encoding='utf-8').read(), 'ar': open('ar/index.html', encoding='utf-8').read()}
CHIPS = {'en': {k: c for k, _, _, c in SVC_EN['items']}, 'ar': {k: c for k, _, _, c in SVC_AR['items']}}
CARD = {'en': {k: (t, d) for k, t, d, _ in SVC_EN['items']}, 'ar': {k: (t, d) for k, t, d, _ in SVC_AR['items']}}


def base(lang):
    return '/ar/' if lang == 'ar' else '/'


def path(lang, key=None):
    return base(lang) + 'services/' + (SLUGS[key] + '/' if key else '')


def grab(lang, pattern):
    m = re.search(pattern, SRC[lang], re.S)
    assert m, f'{lang}: block not found: {pattern[:40]}'
    return m.group(0)


def absolutize(chunk, lang):
    """Rewrite relative URLs from the home page so they work from any subpage."""
    def one(u):
        if not u or u == '#top' or re.match(r'(https?:|mailto:|tel:|data:|/)', u):
            return u
        if u.startswith('../'):
            return '/' + u[3:]
        return base(lang) + u
    chunk = re.sub(r'\b(href|src)="([^"]*)"', lambda m: f'{m.group(1)}="{one(m.group(2))}"', chunk)
    return re.sub(r'srcset="([^"]*)"', lambda m: 'srcset="' + ', '.join(
        ' '.join([one(p.split()[0])] + p.split()[1:]) for p in m.group(1).split(',')) + '"', chunk)


def chrome(lang, other_url):
    """Head bits, nav, menu and footer taken from the built home page."""
    s = SRC[lang]
    ga = grab(lang, r'<!-- Google tag.*?</script>\s*<script>.*?</script>')
    nav = grab(lang, r'<header class="nav".*?</header>')
    menu = grab(lang, r'<div class="menu" id="menu".*?\n</div>')
    foot = grab(lang, r'<footer class="footer".*?</footer>')
    nav = re.sub(r'(<a class="lang-switch" href=)"[^"]*"', rf'\1"{other_url}"', nav)
    foot = re.sub(r'<a href="[^"]*"( class="footer__lang")', rf'<a href="{other_url}"\1', foot)
    nav, menu, foot = (absolutize(x, lang) for x in (nav, menu, foot))
    b = base(lang)
    nav = nav.replace(f'href="{b}#top" class="nav__logo"', f'href="{b}" class="nav__logo"')
    nav, menu, foot = (x.replace(f'href="{b}#services"', f'href="{b}services/"') for x in (nav, menu, foot))
    ver = re.search(r'styles\.min\.css\?v=(\d+)', s).group(1)
    return ga, nav, menu, foot, ver


def head(lang, title, desc, url, alt_url, ver, schema, ga):
    rtl = lang == 'ar'
    fonts = ('<link rel="preload" href="/assets/fonts/tajawal-800-arabic.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="/assets/fonts/tajawal-400-arabic.woff2" as="font" type="font/woff2" crossorigin>') if rtl else \
        '<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>'
    css = f'<link rel="stylesheet" href="/assets/build/styles.min.css?v={ver}">' + (
        f'\n<link rel="stylesheet" href="/assets/build/rtl.min.css?v={ver}">' if rtl else '')
    en_url, ar_url = (alt_url, url) if rtl else (url, alt_url)
    t = html.escape(html.unescape(title), quote=True)
    d = html.escape(html.unescape(desc), quote=True)
    return f'''<!doctype html>
<html lang="{lang}"{' dir="rtl"' if rtl else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{ga}
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="io2:calendly" content="https://calendly.com/io2agency/30min">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="ar" href="{ar_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="theme-color" content="#0B0821">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="io2 Agency">
<meta property="og:locale" content="{'ar_OM' if rtl else 'en_OM'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@io2agency">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{fonts}
{css}
<script>document.documentElement.classList.add("js");try{{var m=localStorage.getItem("io2-mode");if(m)document.documentElement.dataset.mode=m;}}catch(e){{}}</script>
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=1)}
</script>
</head>
<body class="sp">
<a class="skip" href="#main">{'تخطَّ إلى المحتوى' if rtl else 'Skip to content'}</a>
<div class="progress" aria-hidden="true"><span></span></div>
'''


def crumbs_schema(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": html.unescape(n), "item": SITE + u} for i, (n, u) in enumerate(items, 1)]}


def crumbs_html(lang, items):
    li = []
    for i, (n, u) in enumerate(items):
        last = i == len(items) - 1
        cur = ' aria-current="page"' if last else ''
        li.append(f'<li><a href="{u}"{cur}>{n}</a></li>')
    label = 'مسار التنقل' if lang == 'ar' else 'Breadcrumb'
    return f'<nav class="crumbs mono" aria-label="{label}"><ol>{"".join(li)}</ol></nav>'


def card(lang, i, key, cta):
    t, d = CARD[lang][key]
    chips = ''.join(f'<li>{c}</li>' for c in CHIPS[lang][key])
    return f'''      <article class="svc{' svc--ai' if key == 'ai' else ''}">
        <div class="svc__top"><span class="mono svc__n">{i:02d}</span><span class="svc__icon"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[key]}</svg></span></div>
        <h3>{t}</h3>
        <p>{d}</p>
        <ul class="chips chips--dark">{chips}</ul>
        <a class="svc__link" href="{path(lang, key)}"><span>{cta}</span><span class="sr-only">: {t}</span>{ARROW}</a>
      </article>'''


def tail(foot):
    return f'''{foot}

<script src="/assets/build/page.min.js?v=VER" defer></script>
</body>
</html>
'''


def cta_band(lang, u, name, key):
    plain = html.unescape(name)
    return f'''<section class="sp-cta" data-theme="yellow">
  <div class="wrap sp-cta__in">
    <h2 class="h2">{u["cta_h2"]}</h2>
    <p>{u["cta_p"]}</p>
    <div class="sp-cta__btns">
      <a href="{base(lang)}#consultation" class="btn btn--dark btn--lg" data-calendly data-src="service-{key}-cta"><span>{u["book"]}</span>{ARROW}</a>
      <a href="{WA}{quote(u["wa_text"].format(s=plain))}" class="sp-cta__wa" target="_blank" rel="noopener">{u["wa"]}</a>
    </div>
  </div>
</section>'''


def service_page(lang, key, i):
    u, p = UI[lang], PAGES[key][lang]
    other = 'en' if lang == 'ar' else 'ar'
    url, alt = SITE + path(lang, key), SITE + path(other, key)
    ga, nav, menu, foot, ver = chrome(lang, path(other, key))
    trail = [(u['home'], base(lang)), (u['services'], path(lang)), (p['name'], path(lang, key))]
    plain = html.unescape(p['name'])
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "@id": url + "#service", "name": plain, "serviceType": plain, "url": url,
         "description": html.unescape(p['desc']), "inLanguage": lang,
         "provider": {"@id": SITE + "/#agency"},
         "areaServed": [{"@type": "Country", "name": c} for c in COUNTRIES],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": plain, "itemListElement": [
             {"@type": "Offer", "itemOffered": {"@type": "Service", "name": html.unescape(t)}} for t, _ in p['inc']]}},
        crumbs_schema(trail),
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
    ]}
    inc = '\n'.join(f'''      <li class="sp-inc__item"><span class="mono sp-inc__n">{n:02d}</span><h3>{t}</h3><p>{d}</p></li>'''
                    for n, (t, d) in enumerate(p['inc'], 1))
    steps = '\n'.join(f'''      <li class="sp-step"><span class="mono sp-step__n">{n:02d}</span><h3>{t}</h3><p>{d}</p></li>'''
                      for n, (t, d) in enumerate(u['steps'], 1))
    who = '\n'.join(f'      <li>{w}</li>' for w in p['who'])
    faq = '\n'.join(f'      <details><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq'])
    chips = ''.join(f'<li>{c}</li>' for c in CHIPS[lang][key])
    rel = '\n'.join(card(lang, ORDER.index(k) + 1, k, u['more']) for k in PAGES[key]['related'])
    body = f'''{nav}

{menu}

<main id="main">
<section class="sp-hero" id="top" data-theme="dark">
  <div class="sp-hero__glow" aria-hidden="true"></div>
  <div class="wrap">
    {crumbs_html(lang, trail)}
    <div class="sp-hero__grid">
      <div>
        <p class="eyebrow mono"><span class="idx">{i:02d}</span> {u["eyebrow"]}</p>
        <h1 class="sp-hero__title">{p["h1"]}</h1>
        <p class="sp-hero__lead">{p["intro"]}</p>
        <div class="sp-hero__ctas">
          <a href="{base(lang)}#consultation" class="btn btn--yellow btn--lg magnetic" data-calendly data-src="service-{key}-hero"><span>{u["book"]}</span>{ARROW}</a>
          <a href="{WA}{quote(u["wa_text"].format(s=plain))}" class="btn btn--ghost btn--lg" target="_blank" rel="noopener"><span>{u["wa"]}</span></a>
        </div>
      </div>
      <div class="sp-hero__badge" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[key]}</svg></div>
    </div>
    <ul class="chips sp-hero__chips">{chips}</ul>
  </div>
</section>

<section class="sp-inc" data-theme="light">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow mono"><span class="idx">01</span> {u["inc_eyebrow"]}</p>
      <h2 class="h2">{u["inc_h2"]}</h2>
    </div>
    <ul class="sp-inc__grid">
{inc}
    </ul>
  </div>
</section>

<section class="sp-steps" data-theme="indigo">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow mono"><span class="idx">02</span> {u["steps_eyebrow"]}</p>
      <h2 class="h2">{u["steps_h2"]}</h2>
    </div>
    <ol class="sp-steps__list">
{steps}
    </ol>
  </div>
</section>

<section class="sp-who" data-theme="dark">
  <div class="wrap sp-who__wrap">
    <div>
      <p class="eyebrow mono"><span class="idx">03</span> {u["who_eyebrow"]}</p>
      <h2 class="h2">{u["who_h2"]}</h2>
    </div>
    <ul class="sp-who__list">
{who}
    </ul>
  </div>
</section>

<section class="faq" id="faq" data-theme="light">
  <div class="wrap faq__wrap">
    <div>
      <p class="eyebrow mono"><span class="idx">04</span> {u["faq_eyebrow"]}</p>
      <h2 class="h2">{u["faq_h2"]}</h2>
    </div>
    <div class="faq__list">
{faq}
    </div>
  </div>
</section>

{cta_band(lang, u, p["name"], key)}

<section class="services sp-rel" data-theme="light">
  <div class="wrap">
    <div class="sec-head sp-rel__head">
      <div>
        <p class="eyebrow mono"><span class="idx">05</span> {u["rel_eyebrow"]}</p>
        <h2 class="h2">{u["rel_h2"]}</h2>
      </div>
      <a class="sp-rel__all" href="{path(lang)}">{u["all"]} {ARROW}</a>
    </div>
    <div class="svc-grid">
{rel}
    </div>
  </div>
</section>
</main>

'''
    return head(lang, p['title'], p['desc'], url, alt, ver, schema, ga) + body + tail(foot), ver


def hub_page(lang):
    u = UI[lang]
    other = 'en' if lang == 'ar' else 'ar'
    url, alt = SITE + path(lang), SITE + path(other)
    ga, nav, menu, foot, ver = chrome(lang, path(other))
    trail = [(u['home'], base(lang)), (u['services'], path(lang))]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": html.unescape(u['hub_title']),
         "description": html.unescape(u['hub_desc']), "inLanguage": lang, "about": {"@id": SITE + "/#agency"},
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": n, "url": SITE + path(lang, k), "name": html.unescape(PAGES[k][lang]['name'])}
             for n, k in enumerate(ORDER, 1)]}},
        crumbs_schema(trail),
    ]}
    cards = '\n'.join(card(lang, n, k, u['more']) for n, k in enumerate(ORDER, 1))
    body = f'''{nav}

{menu}

<main id="main">
<section class="sp-hero sp-hero--hub" id="top" data-theme="dark">
  <div class="sp-hero__glow" aria-hidden="true"></div>
  <div class="wrap">
    {crumbs_html(lang, trail)}
    <p class="eyebrow mono"><span class="idx">io2</span> {u["services"]}</p>
    <h1 class="sp-hero__title">{u["hub_h1"]}</h1>
    <p class="sp-hero__lead">{u["hub_intro"]}</p>
    <div class="sp-hero__ctas">
      <a href="{base(lang)}#consultation" class="btn btn--yellow btn--lg magnetic" data-calendly data-src="services-hub"><span>{u["book"]}</span>{ARROW}</a>
    </div>
  </div>
</section>

<section class="services sp-hub" data-theme="light">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow mono"><span class="idx">01</span> {SVC_AR["eyebrow"] if lang == "ar" else SVC_EN["eyebrow"]}</p>
      <h2 class="h2">{u["hub_h2"]}</h2>
    </div>
    <div class="svc-grid">
{cards}
    </div>
  </div>
</section>

{cta_band(lang, u, u["services"], "hub")}
</main>

'''
    return head(lang, u['hub_title'], u['hub_desc'], url, alt, ver, schema, ga) + body + tail(foot), ver


def write(rel, content, ver):
    os.makedirs(os.path.dirname(rel), exist_ok=True)
    open(rel, 'w', encoding='utf-8').write(content.replace('page.min.js?v=VER', f'page.min.js?v={ver}'))


# fresh output each build (slugs may change)
for d in ('services', 'ar/services'):
    shutil.rmtree(d, ignore_errors=True)

for lang in ('en', 'ar'):
    pre = 'ar/' if lang == 'ar' else ''
    page, ver = hub_page(lang)
    write(f'{pre}services/index.html', page, ver)
    for i, key in enumerate(ORDER, 1):
        page, ver = service_page(lang, key, i)
        write(f'{pre}services/{SLUGS[key]}/index.html', page, ver)
        p = PAGES[key][lang]
        tl, dl = len(html.unescape(p['title'])), len(html.unescape(p['desc']))
        if tl > 60 or dl > 160:
            print(f'  warn {lang}/{key}: title {tl} chars, description {dl} chars')
        assert '—' not in page, f'em dash in {lang}/{key}'

print(f'service pages: {2 * (len(ORDER) + 1)} written')
