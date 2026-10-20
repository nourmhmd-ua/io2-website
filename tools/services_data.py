"""Single source of truth for the io2 services section (EN + AR)."""
from urllib.parse import quote

ICONS = {
    "social": '<path d="M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4z"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/>',
    "ads": '<path d="M3 11v2a1 1 0 0 0 1 1h3l5 4V6L7 10H4a1 1 0 0 0-1 1z"/><path d="M16 8.5a5 5 0 0 1 0 7M19 5.5a9 9 0 0 1 0 13"/>',
    "seo": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/><path d="M7.5 12l2-2.5 2 1.5 2.5-3"/>',
    "content": '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10.5 21 8v8l-5-2.5"/>',
    "brand": '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z"/>',
    "web": '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 8h18M8 21h8M12 18v3"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "strategy": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "ai": '<rect x="5" y="7" width="14" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9.5 16h5"/>',
}

EN = {
    "eyebrow": "Growth Marketing Services",
    "h2a": "Every marketing service.", "h2b": "One growth team.",
    "lead": "io2 is a full-service growth marketing agency in Muscat. From social media and SEO to paid ads, content, branding and websites, every service is planned with data, delivered by specialists and measured by the revenue it brings.",
    "cta": "Discuss this service",
    "wa": "Hi io2, I'd like to discuss {s}.",
    "items": [
        ("social", "Social Media Marketing", "Strategy, content calendars, community management and paid social that turn followers into customers across every GCC platform.", ["Instagram", "TikTok", "Snapchat", "LinkedIn", "X"]),
        ("ads", "Performance Marketing &amp; Paid Ads", "Google, Meta, TikTok and Snapchat campaigns where every rial is tracked, tested and moved to what converts.", ["Google Ads", "Meta Ads", "TikTok Ads", "Snap Ads", "CRO"]),
        ("seo", "SEO &amp; AI Search", "Technical SEO, Arabic and English content and authority building, so you rank on Google and show up in AI answers.", ["Technical SEO", "Local SEO", "Content", "AEO / GEO"]),
        ("content", "Content Marketing &amp; Production", "Reels, photo and video shoots, CGI and bilingual copy produced as a steady content engine, not one-off posts.", ["Video &amp; reels", "Photography", "CGI", "Copywriting"]),
        ("brand", "Branding &amp; Identity", "Brand strategy, logos, visual identity and guidelines that make you look like the market leader you want to be.", ["Brand strategy", "Logo", "Guidelines", "Packaging"]),
        ("web", "Website Design &amp; Development", "Fast, SEO-ready websites, landing pages and e-commerce stores designed to convert visitors into leads and sales.", ["Websites", "Landing pages", "E-commerce", "UI/UX"]),
        ("email", "Email, CRM &amp; Marketing Automation", "Lead nurturing, newsletters, WhatsApp broadcasts and follow-up campaigns that bring customers back.", ["Email", "WhatsApp", "CRM", "Automation"]),
        ("strategy", "Marketing Strategy &amp; Analytics", "Market research, go-to-market plans, funnel audits and live KPI dashboards that show exactly what drives growth.", ["Research", "Go-to-market", "Funnel audit", "Dashboards"]),
        ("ai", "AI Agents &amp; Automation", "WhatsApp, chat and voice AI agents that answer, qualify and book customers 24/7 in Arabic and English.", ["WhatsApp AI", "Voice AI", "Chatbots", "CRM AI"]),
    ],
}

AR = {
    "eyebrow": "خدمات التسويق للنمو",
    "h2a": "كل خدمات التسويق.", "h2b": "في فريق نمو واحد.",
    "lead": "io2 وكالة تسويق للنمو متكاملة الخدمات في مسقط. من السوشال ميديا وتحسين محركات البحث إلى الإعلانات المدفوعة والمحتوى والهوية والمواقع، كل خدمة تُخطَّط بالبيانات، ينفّذها مختصون، وتُقاس بالإيرادات التي تحققها.",
    "cta": "ناقش هذه الخدمة",
    "wa": "مرحباً io2، أود مناقشة خدمة {s}.",
    "items": [
        ("social", "التسويق عبر السوشال ميديا", "استراتيجية وتقويم محتوى وإدارة مجتمع وإعلانات سوشال تحوّل المتابعين إلى عملاء على كل منصات الخليج.", ["Instagram", "TikTok", "Snapchat", "LinkedIn", "X"]),
        ("ads", "التسويق بالأداء والإعلانات المدفوعة", "حملات Google وMeta وTikTok وSnapchat يُتتبَّع فيها كل ريال ويُختبر ويُوجَّه نحو ما يحقق التحويل.", ["إعلانات Google", "إعلانات Meta", "إعلانات TikTok", "إعلانات Snap", "تحسين التحويل"]),
        ("seo", "تحسين محركات البحث SEO", "SEO تقني ومحتوى عربي وإنجليزي وبناء سلطة النطاق، لتتصدّر نتائج Google وتظهر في إجابات الذكاء الاصطناعي.", ["SEO تقني", "SEO محلي", "المحتوى", "AEO / GEO"]),
        ("content", "صناعة المحتوى والإنتاج", "ريلز وتصوير فوتوغرافي وفيديو وCGI وكتابة إعلانية بالعربية والإنجليزية، محرّك محتوى مستمر لا منشورات متفرقة.", ["فيديو وريلز", "تصوير", "CGI", "كتابة إعلانية"]),
        ("brand", "الهوية التجارية والعلامة", "استراتيجية العلامة والشعار والهوية البصرية والإرشادات لتظهر كقائد السوق الذي تطمح أن تكونه.", ["استراتيجية العلامة", "الشعار", "دليل الهوية", "التغليف"]),
        ("web", "تصميم وتطوير المواقع", "مواقع سريعة جاهزة لمحركات البحث وصفحات هبوط ومتاجر إلكترونية مصمَّمة لتحويل الزوار إلى عملاء ومبيعات.", ["المواقع", "صفحات الهبوط", "المتاجر الإلكترونية", "UI/UX"]),
        ("email", "التسويق بالبريد وCRM والأتمتة", "رعاية العملاء المحتملين والنشرات ورسائل واتساب الجماعية ورحلات العملاء التي تعيدهم للشراء.", ["البريد الإلكتروني", "واتساب", "CRM", "الأتمتة"]),
        ("strategy", "الاستراتيجية التسويقية والتحليلات", "أبحاث السوق وخطط دخول السوق وتدقيق مسار المبيعات ولوحات مؤشرات مباشرة تُظهر بدقة ما يقود النمو.", ["أبحاث السوق", "خطة الدخول للسوق", "تدقيق المسار", "لوحات المؤشرات"]),
        ("ai", "وكلاء الذكاء الاصطناعي والأتمتة", "وكلاء واتساب ومحادثة وصوت بالذكاء الاصطناعي يجيبون ويؤهّلون ويحجزون للعملاء على مدار الساعة بالعربية والإنجليزية.", ["واتساب AI", "الذكاء الصوتي", "روبوتات المحادثة", "CRM AI"]),
    ],
}


def render(d):
    cards = []
    for i, (icon, title, desc, chips) in enumerate(d["items"], 1):
        plain = title.replace("&amp;", "&")
        href = "https://wa.me/96877220770?text=" + quote(d["wa"].format(s=plain))
        chip_html = "".join(f"<li>{c}</li>" for c in chips)
        cards.append(f'''      <article class="svc{' svc--ai' if icon == 'ai' else ''}">
        <div class="svc__top"><span class="mono svc__n">{i:02d}</span><span class="svc__icon"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[icon]}</svg></span></div>
        <h3>{title}</h3>
        <p>{desc}</p>
        <ul class="chips chips--dark">{chip_html}</ul>
        <a class="svc__link" href="{href}" target="_blank" rel="noopener"><span>{d["cta"]}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      </article>''')
    return f'''<section class="services" id="services" data-theme="light">
  <div class="wrap">
    <div class="sec-head services__head">
      <div>
        <p class="eyebrow mono"><span class="idx">01</span> {d["eyebrow"]}</p>
        <h2 class="h2"><span class="split">{d["h2a"]}</span><br><span class="slash" aria-hidden="true"></span><span class="split">{d["h2b"]}</span></h2>
      </div>
      <p class="lead">{d["lead"]}</p>
    </div>
    <div class="svc-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>'''
