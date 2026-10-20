# io2 — premium website

Static site — no build step. Upload the whole folder to any host (GitHub Pages, Netlify, Vercel, cPanel), or serve locally:

```
python3 -m http.server 5178
```

## Files
- `index.html` — English page: content, SEO meta, schema (MarketingAgency + FAQ), hreflang
- `ar/index.html` — Arabic (RTL) page, Tajawal font, Arabic SEO title/description/schema; `rtl.css` mirrors the layout
- `styles.css` — brand tokens (Indigo #5E2DF7, Golden Yellow #FFE000, Electric Navy, Spring Green, Tomato), Inter
- `main.js` — GSAP 3.13 + ScrollTrigger + SplitText, Lenis smooth scroll, hero "input → system → output ×2" canvas
- `assets/` — web exports of the **original** logo files in `IO2/logo-02/` (trimmed and resized only; the artwork isn't changed)
- `assets/video/` — cinematic background loops generated with Higgsfield (Seedance 2.0): 720p master for desktop/iPad, `-sm` light encode (~220 KB) for phones, `.jpg` poster. Played at low opacity, lazy-loaded, paused off-screen, poster-only with reduced motion or Data Saver
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
- Social links in the footer still point to the URLs from the old site (`creator.hub1` / `creatoradv`). Swap them for the official io2 handles (e.g. @io2agency).
- Live on https://io2.agency (GitHub Pages custom domain via the CNAME file; DNS at Hostinger). Submit https://io2.agency/sitemap.xml in Google Search Console.
- Create / verify the Google Business Profile for io2 in Muscat (biggest lever for local "marketing agency Muscat" searches).
- Add client logos and real case-study numbers when you have them. The site doesn't include any made-up metrics.
