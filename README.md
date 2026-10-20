# io2 — premium website

Static site — no build step. Upload the whole folder to any host (GitHub Pages, Netlify, Vercel, cPanel), or serve locally:

```
python3 -m http.server 5178
```

## Files
- `index.html` — all content, SEO meta and schema (MarketingAgency + FAQ)
- `styles.css` — brand tokens (Indigo #5E2DF7, Golden Yellow #FFE000, Electric Navy, Spring Green, Tomato), Inter
- `main.js` — GSAP 3.13 + ScrollTrigger + SplitText, Lenis smooth scroll, hero "input → system → output ×2" canvas
- `assets/` — web exports of the **original** logo files in `IO2/logo-02/` (trimmed and resized only; the artwork isn't changed)

## Before going live
- Social links in the footer still point to the URLs from the old site (`creator.hub1` / `creatoradv`). Swap them for the official io2 handles (e.g. @io2agency).
- Add a 1200×630 OG image and update `og:image`.
- Add client logos and real case-study numbers when you have them. The site doesn't include any made-up metrics.
