"""Results section (EN + AR): combined campaign numbers with no client names.
Source: Meta Ads Manager (all client ad accounts io2 runs, lifetime to Oct 2026) and Google Analytics 4.
Every figure is rounded down. Reach is summed per account, so one person reached by two clients counts twice.
Highlights name the sector only, never the client, the account or the country."""

AS_OF = {"en": "October 2026", "ar": "أكتوبر 2026"}

# (prefix, number, decimals, suffix, EN label, AR label)
STATS = [
    ("$", 210, 0, "K+", "Ad spend managed on Meta", "ميزانية إعلانات أدرناها على Meta"),
    ("", 194, 0, "M+", "Ad impressions", "ظهور إعلاني"),
    ("", 15, 0, "M+", "People reached, combined across accounts", "شخص وصلنا إليهم عبر الحسابات مجتمعة"),
    ("", 130, 0, "M+", "Video plays", "مشاهدة فيديو"),
    ("", 28, 0, "M+", "Post engagements", "تفاعل مع المنشورات"),
    ("", 1.9, 1, "M+", "Link clicks to websites and stores", "نقرة على روابط المواقع والمتاجر"),
    ("", 40, 0, "K+", "WhatsApp and Messenger conversations started", "محادثة بدأت على واتساب وماسنجر"),
    ("", 4, 0, "M+", "Users across a marketplace website and app we market", "مستخدم لمنصة سوق إلكتروني (موقع وتطبيق) نسوّق لها"),
]

# (EN sector, AR sector, big figure, EN detail, AR detail)
CASES = [
    ("Automotive", "السيارات", "7,238",
     "WhatsApp conversations from one vehicle-arrival campaign, at $1.72 each.",
     "محادثة واتساب من حملة واحدة لوصول سيارات، بتكلفة 1.72$ للمحادثة."),
    ("Retail", "التجزئة", "$0.61",
     "Cost per WhatsApp conversation across 3,766 chats for a toy retailer.",
     "تكلفة المحادثة على واتساب عبر 3,766 محادثة لمتجر ألعاب."),
    ("E-commerce", "التجارة الإلكترونية", "244",
     "Website purchases at $6.74 each, with a 3.76% click-through rate.",
     "عملية شراء من الموقع بتكلفة 6.74$ للعملية، ونسبة نقر 3.76%."),
    ("Marketplace", "المنصات", "$0.03",
     "Cost per link click across 224,235 clicks, with a 3.30% click-through rate.",
     "تكلفة النقرة عبر 224,235 نقرة، ونسبة نقر 3.30%."),
    ("Awareness", "الوعي بالعلامة", "1.69M",
     "People reached by one awareness campaign at $0.17 per 1,000 impressions.",
     "شخص وصلت إليهم حملة وعي واحدة بتكلفة 0.17$ لكل 1,000 ظهور."),
    ("Automotive", "السيارات", "$1.39",
     "Cost per WhatsApp conversation in a recent car dealer campaign, across 994 chats.",
     "تكلفة محادثة واتساب في حملة حديثة لمعرض سيارات، عبر 994 محادثة."),
]

EN = {"lang": "en", "eyebrow": "Results", "h2a": "Real campaigns.", "h2b": "Real numbers.",
      "lead": "Combined results from the campaigns io2 plans and runs for clients across the GCC. Client names and account details stay private.",
      "label": "Campaign results", "cases": "Campaign highlights",
      "note": "Source: Meta Ads Manager and Google Analytics 4, all client accounts, to {d}. Figures rounded down. Reach is summed per account."}
AR = {"lang": "ar", "eyebrow": "النتائج", "h2a": "حملات حقيقية.", "h2b": "أرقام حقيقية.",
      "lead": "نتائج مجمّعة من الحملات التي تخطط لها io2 وتديرها لعملائها في الخليج. أسماء العملاء وتفاصيل الحسابات تبقى خاصة.",
      "label": "نتائج الحملات", "cases": "أبرز الحملات",
      "note": "المصدر: مدير إعلانات Meta وGoogle Analytics 4، جميع حسابات العملاء حتى {d}. الأرقام مقرّبة للأسفل، والوصول مجموع لكل حساب."}


def render(d, prefix="assets/"):
    ar = d["lang"] == "ar"
    stats = []
    for pre, num, dec, suf, en, a in STATS:
        shown = f"{num:.{dec}f}"
        stats.append(f'<div class="stat"><b dir="ltr">{pre}<span class="counter" data-to="{num}" data-dec="{dec}">{shown}</span>{suf}</b><span>{a if ar else en}</span></div>')
    cases = []
    for se, sa, big, en, a in CASES:
        cases.append(f'<li class="results__case"><span class="results__tag mono">{sa if ar else se}</span><b dir="ltr">{big}</b><p>{a if ar else en}</p></li>')
    return f'''<section class="results" id="results" data-theme="dark" aria-label="{d["label"]}">
  <div class="wrap">
    <div class="results__head">
      <p class="eyebrow mono"><span class="idx">●</span> {d["eyebrow"]}</p>
      <h2 class="h2"><span class="split">{d["h2a"]}</span><br><span class="slash" aria-hidden="true"></span><span class="split">{d["h2b"]}</span></h2>
      <p class="lead">{d["lead"]}</p>
    </div>
    <div class="stats results__stats">
      {"".join(stats)}
    </div>
    <h3 class="results__sub mono">{d["cases"]}</h3>
    <ul class="results__cases">
      {"".join(cases)}
    </ul>
    <p class="results__note">{d["note"].format(d=AS_OF[d["lang"]])}</p>
  </div>
</section>'''
