# io2 — premium website

Static site. Live at https://io2.agency (GitHub Pages, repo nourmhmd-ua/io2-website, branch main).

## Editing workflow
1. Edit the **sources**: `index.html` (English), `styles.css`, `rtl.css`, `main.js`, and the shared section data in `tools/services_data.py` / `tools/consult_data.py`. Arabic copy lives in `tools/build_ar.py`.
2. Run `sh tools/build.sh`. It minifies CSS/JS (self-hosted fonts bundled in), stamps a cache-busting version, regenerates `ar/index.html` and `sitemap.xml`. Needs Node (for `npx esbuild`) and Python 3.
3. Never hand-edit `*.min.css`, `*.min.js`, `ar/index.html` or `sitemap.xml` (they are generated).
4. Commit and push to `main`; GitHub Pages publishes in ~30 seconds.

Preview locally:

```
python3 -m http.server 5178
```

## Files
- `index.html` — English page: content, SEO meta, schema (MarketingAgency + FAQ), hreflang
- `ar/index.html` — Arabic (RTL) page, Tajawal font, Arabic SEO title/description/schema; `rtl.css` mirrors the layout
- `styles.css` — brand tokens (Indigo #5E2DF7, Golden Yellow #FFE000, Electric Navy, Spring Green, Tomato), Inter
- `main.js` — GSAP 3.13 + ScrollTrigger and Lenis (self-hosted in assets/vendor, bundled to assets/build/vendor.min.js); own lightweight headline splitter, hero "input → system → output ×2" canvas
- `assets/fonts/` — self-hosted Inter, JetBrains Mono and Tajawal (Latin + Arabic subsets); no Google Fonts requests
- `llms.txt` — summary for AI search engines (ChatGPT, Claude, Perplexity)
- `tools/` — build scripts (see Editing workflow)
- `assets/` — web exports of the **original** logo files in `IO2/logo-02/` (trimmed and resized only; the artwork isn't changed)
- `assets/video/` — cinematic background loops generated with Higgsfield (Seedance 2.0): 720p H.264 for desktop/iPad, `-sm` 480p for phones, `.webp` poster; full-quality originals in ../video-masters/. Played at low opacity, lazy-loaded, paused off-screen, poster-only with reduced motion or Data Saver
- `assets/img/` — photos as responsive WebP (720 / 1440 px). People & workplace scenes generated with Magnific; GCC city skylines, Muscat corniche and the analytics screen are from Unsplash (free licence, commercial use allowed)
- `robots.txt`, `sitemap.xml` (with image entries), `site.webmanifest` — SEO + add-to-home-screen on iPhone/iPad

## Free consultation → Calendly
Booking uses https://calendly.com/io2agency/30min, set once per page in
`<meta name="io2:calendly" content="...">` (index.html and ar/index.html).
- The consultation card is a branded booking card (experts, 3 steps, next 6 days, weekends included). Picking a day opens the Calendly popup on that date; "See all available times" and every "Free consultation" button open it too. Calendly's script is pre-loaded when the card is near so the popup opens instantly.
- Bookings are tagged utm_source=website, utm_medium=cta, utm_campaign=free-consultation, utm_content=nav|mobile-menu|day-picker|booking-card (+ -en/-ar) — visible in Calendly's booking details.
- On booking, a confirmation shows and a `consultation_booked` event is pushed to `dataLayer` (for GA4/GTM).
- Empty the meta content to fall back to the WhatsApp booking form.
- Brand colours in the widget need a paid Calendly plan; on the free plan Calendly shows its default colours.

## Dark / light mode
Toggle in the nav (sun/moon). Choice is remembered per visitor; default is dark.

## Before going live
- Social links: Instagram @io2.agency, LinkedIn /company/io2agency, Facebook /io2agency, WhatsApp wa.me/96877220770 (footer, contact section, schema sameAs, llms.txt).
- Live on https://io2.agency (GitHub Pages custom domain via the CNAME file; DNS at Hostinger). Submit https://io2.agency/sitemap.xml in Google Search Console.
- Create / verify the Google Business Profile for io2 in Muscat (biggest lever for local "marketing agency Muscat" searches).
- Add client logos and real case-study numbers when you have them. The site doesn't include any made-up metrics.

## 404 page
`404.html` is a branded, noindex "page has moved" page (English, or Arabic under /ar/) for old WordPress URLs.
