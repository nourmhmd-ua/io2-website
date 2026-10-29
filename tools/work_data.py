"""Work section (EN + AR): vertical portfolio videos in a swipeable row; tap opens the full video with sound.
Video files are made by tools/work_videos.sh into assets/work/ (<slug>.mp4, <slug>-p.mp4 preview, <slug>.webp poster)."""
import json

TAGS = {
    "cgi": ("CGI", "CGI"),
    "vfx": ("VFX", "مؤثرات بصرية"),
    "holo": ("Hologram", "هولوغرام"),
    "reel": ("Social reel", "ريلز"),
    "video": ("Video production", "إنتاج فيديو"),
}

# slug, EN title, AR title, tag
WORK = [
    ("oman-national-day", "Oman National Day", "اليوم الوطني العُماني", "cgi"),
    ("moc-hologram", "Ministry of Commerce, hologram", "وزارة التجارة، هولوغرام", "holo"),
    ("avenues-labubu", "Avenues Mall, Labubu trend", "أفنيوز مول، ترند لابوبو", "reel"),
    ("g-wagon-cgi", "Mercedes G-Class", "مرسيدس G-Class", "cgi"),
    ("pagani-cgi", "Pagani", "باغاني", "cgi"),
    ("chanel-cgi", "Chanel", "شانيل", "cgi"),
    ("uae-national-day", "UAE National Day", "اليوم الوطني الإماراتي", "cgi"),
    ("moc-video", "Ministry of Commerce, campaign video", "وزارة التجارة، فيديو الحملة", "video"),
    ("zomorod-cgi", "Zomorod Agency", "وكالة زمرد", "cgi"),
    ("star-wars-vfx", "Star Wars", "Star Wars", "vfx"),
    ("cinema-vfx", "Cinema VFX", "مؤثرات سينمائية", "vfx"),
    ("cars-cgi", "Cars", "سيارات", "cgi"),
]

EN = {"lang": 0, "eyebrow": "Our work", "h2a": "Made by io2.", "h2b": "Reels, CGI and VFX.",
      "lead": "A selection of reels, CGI and visual effects produced by our studio in Muscat. Tap any video to watch it with sound.",
      "play": "Play video", "prev": "Previous videos", "next": "Next videos", "close": "Close video",
      "pnext": "Next video", "pprev": "Previous video", "label": "Portfolio videos"}
AR = {"lang": 1, "eyebrow": "أعمالنا", "h2a": "من إنتاج io2.", "h2b": "ريلز وCGI ومؤثرات بصرية.",
      "lead": "مختارات من الريلز وأعمال CGI والمؤثرات البصرية التي أنتجها فريقنا في مسقط. اضغط على أي فيديو لمشاهدته بالصوت.",
      "play": "تشغيل الفيديو", "prev": "الفيديوهات السابقة", "next": "الفيديوهات التالية", "close": "إغلاق الفيديو",
      "pnext": "الفيديو التالي", "pprev": "الفيديو السابق", "label": "فيديوهات الأعمال"}

PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def render(d, prefix="assets/"):
    i = d["lang"]
    cards = []
    for n, (slug, en, ar, tag) in enumerate(WORK, 1):
        title = (en, ar)[i]
        t = TAGS[tag][i]
        cards.append(f'''      <li class="work__item">
        <button type="button" class="work__card" data-video="{prefix}work/{slug}.mp4" data-title="{title}" aria-label="{d["play"]}: {title}">
          <video class="work__prev" muted loop playsinline preload="none" poster="{prefix}work/{slug}.webp" data-src="{prefix}work/{slug}-p.mp4" aria-hidden="true"></video>
          <span class="work__shade" aria-hidden="true"></span>
          <span class="work__meta"><span class="mono work__tag">{n:02d} · {t}</span><span class="work__title">{title}</span></span>
          <span class="work__play" aria-hidden="true">{PLAY}</span>
        </button>
      </li>''')
    base = "https://io2.agency/"
    schema = {"@context": "https://schema.org", "@type": "ItemList", "name": d["label"], "itemListElement": [
        {"@type": "ListItem", "position": n, "item": {
            "@type": "VideoObject", "name": f"{(en, ar)[i]} | io2", "description": f"{TAGS[tag][0]} by io2, Muscat",
            "thumbnailUrl": f"{base}assets/work/{slug}.webp", "contentUrl": f"{base}assets/work/{slug}.mp4",
            "uploadDate": "2026-10-29", "publisher": {"@id": base + "#agency"}}}
        for n, (slug, en, ar, tag) in enumerate(WORK, 1)]}
    return f'''<section class="work" id="work" data-theme="light" aria-label="{d["label"]}">
  <div class="wrap work__head">
    <div>
      <p class="eyebrow mono"><span class="idx">●</span> {d["eyebrow"]}</p>
      <h2 class="h2"><span class="split">{d["h2a"]}</span><br><span class="slash" aria-hidden="true"></span><span class="split">{d["h2b"]}</span></h2>
      <p class="lead">{d["lead"]}</p>
    </div>
    <div class="work__nav">
      <button type="button" class="work__btn work__btn--prev" aria-label="{d["prev"]}">{ARROW}</button>
      <button type="button" class="work__btn work__btn--next" aria-label="{d["next"]}">{ARROW}</button>
    </div>
  </div>
  <ul class="work__rail">
{chr(10).join(cards)}
  </ul>
  <dialog class="vbox" aria-label="{d["label"]}">
    <div class="vbox__frame">
      <video class="vbox__video" controls playsinline preload="none"></video>
      <p class="vbox__title"></p>
    </div>
    <button type="button" class="vbox__close" aria-label="{d["close"]}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
    <button type="button" class="vbox__step vbox__step--prev" aria-label="{d["pprev"]}">{ARROW}</button>
    <button type="button" class="vbox__step vbox__step--next" aria-label="{d["pnext"]}">{ARROW}</button>
  </dialog>
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</section>'''
