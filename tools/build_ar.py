import re, sys, json, os
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(__file__))
from services_data import AR as SVC_AR, render as render_services
from consult_data import AR as CON_AR, render as render_consult
root = sys.argv[1]
h = open(f'{root}/index.html', encoding='utf-8').read()
B = 'https://io2.agency/'

def R(a, b, n=1):
    global h
    if a not in h:
        raise SystemExit('MISSING: ' + a[:100])
    h = h.replace(a, b) if n == -1 else h.replace(a, b, n)

# ---------- paths (page lives in /ar/) ----------
h = h.replace('="assets/', '="../assets/').replace(', assets/', ', ../assets/')
h, _n = re.subn(r'href="\.\./assets/build/styles\.min\.css(\?v=\d+)?"', lambda m: 'href="../assets/build/styles.min.css' + (m.group(1) or '') + '">\n<link rel="stylesheet" href="../assets/build/rtl.min.css' + (m.group(1) or '') + '"', h, count=1)
assert _n == 1, 'rtl stylesheet link not inserted'
R('href="site.webmanifest"', 'href="../site.webmanifest"')
R('<html lang="en">', '<html lang="ar" dir="rtl">')

# ---------- head / SEO ----------
R('<title>io2 | Growth Marketing Agency in Muscat, Oman &amp; GCC</title>',
  '<title>io2 | وكالة تسويق للنمو في مسقط، عُمان والخليج</title>')
h = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="io2 وكالة تسويق للنمو في مسقط، عُمان: تسويق عبر السوشال ميديا، SEO، إعلانات مدفوعة، محتوى، هوية تجارية، مواقع وذكاء اصطناعي للشركات في الخليج.">', h, 1)
R(f'<link rel="canonical" href="{B}">', f'<link rel="canonical" href="{B}ar/">')
R('<meta property="og:url" content="' + B + '">', '<meta property="og:url" content="' + B + 'ar/">')
h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="io2 | وكالة تسويق للنمو في مسقط، عُمان والخليج">', h, 1)
h = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="وكالة تسويق متكاملة للنمو في مسقط: سوشال ميديا وSEO وإعلانات مدفوعة ومحتوى وهوية ومواقع، مدعومة بالبيانات والذكاء الاصطناعي لعلامات الخليج.">', h, 1)
R('<meta property="og:locale" content="en_OM">\n<meta property="og:locale:alternate" content="ar_OM">',
  '<meta property="og:locale" content="ar_OM">\n<meta property="og:locale:alternate" content="en_OM">')
h = re.sub(r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="io2، من المُدخل إلى الأثر. وكالة تسويق بالذكاء الاصطناعي، مسقط، عُمان، الخليج">', h, 1)
h = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="io2 | وكالة تسويق رقمي ونمو بالذكاء الاصطناعي في عُمان والخليج">', h, 1)
h = re.sub(r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="البيانات ووكلاء الذكاء الاصطناعي والاستراتيجية الإبداعية في نظام نمو واحد للشركات في عُمان والخليج.">', h, 1)
R('<meta name="geo.placename" content="Muscat, Oman">', '<meta name="geo.placename" content="مسقط، عُمان">')
# Arabic font (Tajawal) alongside Inter
R('<link rel="preload" href="../assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>', '<link rel="preload" href="../assets/fonts/tajawal-800-arabic.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="../assets/fonts/tajawal-400-arabic.woff2" as="font" type="font/woff2" crossorigin>')

# structured data: Arabic agency + FAQ
a = h.index('<script type="application/ld+json">'); b = h.index('</script>', h.index('<script type="application/ld+json">', a + 10)) + len('</script>')
agency = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": ["MarketingAgency", "LocalBusiness"], "@id": B + "#agency", "name": "io2 Agency", "alternateName": ["io2", "آي أو تو"],
     "url": B + "ar/", "logo": B + "assets/io2-logo.png", "image": B + "og-image.png",
     "description": "io2 وكالة تسويق للنمو متكاملة الخدمات في مسقط، سلطنة عُمان: التسويق عبر السوشال ميديا، التسويق بالأداء والإعلانات المدفوعة، تحسين محركات البحث، صناعة المحتوى، الهوية التجارية، تصميم المواقع، التسويق بالبريد وCRM، الاستراتيجية التسويقية ووكلاء الذكاء الاصطناعي للشركات في دول الخليج.",
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "خدمات التسويق للنمو", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t.replace("&amp;", "&"), "areaServed": "GCC"}} for _, t, _, _ in SVC_AR["items"]]},
     "slogan": "من المُدخل إلى الأثر", "email": "contact@io2.agency", "telephone": "+968 7722 0770", "priceRange": "$$",
     "address": {"@type": "PostalAddress", "addressLocality": "مسقط", "addressRegion": "محافظة مسقط", "addressCountry": "OM"},
     "geo": {"@type": "GeoCoordinates", "latitude": 23.5880, "longitude": 58.3829},
     "areaServed": [{"@type": "Country", "name": n} for n in ["عُمان", "الإمارات العربية المتحدة", "المملكة العربية السعودية", "قطر", "الكويت", "البحرين"]],
     "knowsLanguage": ["ar", "en"],
     "sameAs": ["https://www.instagram.com/io2.agency/", "https://www.linkedin.com/company/io2agency/", "https://www.facebook.com/io2agency/", "https://wa.me/96877220770"]},
    {"@type": "WebPage", "@id": B + "ar/#webpage", "url": B + "ar/", "inLanguage": "ar",
     "name": "io2 | وكالة تسويق للنمو في مسقط، عُمان والخليج", "about": {"@id": B + "#agency"}}
  ]}
faq = [
  ("هل تقدم io2 استشارة تسويقية مجانية؟", "نعم. يمكن لكل نشاط تجاري حجز استشارة مجانية فردية لمرة واحدة مع خبراء التسويق والأعمال في io2، في مسقط أو أونلاين، بالعربية أو الإنجليزية، ودون أي التزام."),
  ("ما هي خدمات التسويق التي تقدمها io2؟", "التسويق عبر السوشال ميديا، التسويق بالأداء والإعلانات المدفوعة (Google وMeta وTikTok وSnapchat)، تحسين محركات البحث، صناعة المحتوى والفيديو، الهوية التجارية، تصميم وتطوير المواقع، التسويق بالبريد وCRM والأتمتة، الاستراتيجية التسويقية والتحليلات، بالإضافة إلى وكلاء الذكاء الاصطناعي لواتساب والمحادثة والصوت."),
  ("ما هي io2؟", "io2 وكالة نمو وتسويق رقمي مدعومة بالذكاء الاصطناعي مقرها مسقط، عُمان. نبني أنظمة نمو تجمع البيانات ووكلاء الذكاء الاصطناعي والأتمتة والتسويق بالأداء والاستراتيجية الإبداعية للشركات في دول الخليج."),
  ("هل io2 شركة تسويق رقمي في عُمان؟", "نعم. مقر io2 في مسقط، ونقدم التسويق بالأداء وتحسين محركات البحث والسوشال ميديا والمحتوى والهوية والمواقع وأتمتة الذكاء الاصطناعي للشركات العُمانية والخليجية."),
  ("بماذا تختلف io2 عن وكالات التسويق التقليدية؟", "الوكالات التقليدية تبيع الوصول، أما io2 فتُحاسَب على النمو: كل مشروع يُبنى كنظام مرتبط بمؤشرات الإيرادات مع ذكاء اصطناعي يعمل داخله على مدار الساعة."),
  ("ما الأسواق التي تخدمها io2؟", "مقرنا في مسقط ونخدم الشركات في عُمان والإمارات والسعودية وقطر والكويت والبحرين، بالعربية والإنجليزية."),
  ("هل يتحدث وكلاء الذكاء الاصطناعي العربية؟", "نعم. وكلاء io2 مهيّؤون للمحادثة بالعربية والإنجليزية عبر واتساب وإنستغرام والمواقع والهاتف، ومدرَّبون على منتجات كل عميل وسياساته."),
  ("كيف أبدأ مع io2؟", "احجز تدقيق النمو عبر واتساب على ‎+968 7722 0770 أو راسلنا على contact@io2.agency."),
]
faqld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ar",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in faq]}
h = h[:a] + '<script type="application/ld+json">\n' + json.dumps(agency, ensure_ascii=False, indent=2) + '\n</script>\n<script type="application/ld+json">\n' + json.dumps(faqld, ensure_ascii=False, indent=2) + '\n</script>' + h[b:]

# ---------- chrome ----------
R('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">تخطَّ إلى المحتوى</a>')
R('<span class="loader__label">Booting growth system</span>', '<span class="loader__label">تشغيل نظام النمو</span>')
R('aria-label="io2 Agency home"', 'aria-label="io2، الصفحة الرئيسية"')
R('<nav class="nav__links" aria-label="Primary">', '<nav class="nav__links" aria-label="القائمة الرئيسية">')
for en, ar in [("Services", "الخدمات"), ("System", "النظام"), ("Growth", "النمو"), ("AI Agents", "الوكلاء الأذكياء"), ("Process", "المنهجية"), ("Packages", "الباقات"), ("Markets", "الأسواق"), ("Contact", "تواصل")]:
    h = h.replace(f'</span>{en}</a>', f'</span>{ar}</a>')
    h = re.sub(rf'(<a href="#[a-z]+">){re.escape(en)}(</a>)', rf'\g<1>{ar}\g<2>', h)
R('<a class="lang-switch" href="ar/" hreflang="ar" lang="ar" aria-label="العربية">ع</a>',
  '<a class="lang-switch" href="../" hreflang="en" lang="en" aria-label="English">EN</a>')
R('aria-label="Switch to light mode"', 'aria-label="التبديل إلى الوضع الفاتح"')
R('<span>Free consultation</span></a>', '<span>استشارة مجانية</span></a>')
R('<span class="mono">★</span>Free consultation</a>', '<span class="mono">★</span>استشارة مجانية</a>')
R('aria-label="Open menu"', 'aria-label="فتح القائمة"')
R('<nav aria-label="Mobile">', '<nav aria-label="قائمة الجوال">')
h = h.replace('>+968 7722 0770</a>', '><bdi dir="ltr">+968 7722 0770</bdi></a>')

# ---------- hero ----------
R('<span class="scramble">GROWTH MARKETING · DATA · AI · MUSCAT → GCC</span>', '<span class="scramble">تسويق للنمو · بيانات · ذكاء اصطناعي، من مسقط إلى الخليج</span>')
R('Growth marketing agency in Muscat, Oman. Social media, SEO, paid ads, branding and AI for businesses across the GCC.', 'وكالة تسويق للنمو في مسقط، عُمان، سوشال ميديا وSEO وإعلانات مدفوعة وهوية وذكاء اصطناعي لدول الخليج')
R('<span class="split">From input</span>', '<span class="split">من المُدخل</span>')
R('<span class="split">to impact.</span>', '<span class="split">إلى الأثر.</span>')
R("We're a full-service growth marketing agency. <strong>Social media, SEO, paid ads, content, branding and websites</strong>, planned with data, supported by AI and measured by the revenue they bring to GCC businesses.",
  'نحن وكالة تسويق للنمو متكاملة الخدمات. <strong>سوشال ميديا وSEO وإعلانات مدفوعة ومحتوى وهوية ومواقع</strong>، تُخطَّط بالبيانات، ويدعمها الذكاء الاصطناعي، وتُقاس بالإيرادات للشركات الطموحة في الخليج.')
R('<span>Build my growth system</span>', '<span>ابدأ بناء نظام نموك</span>')
R('<span>Explore our services</span>', '<span>استكشف خدماتنا</span>')
R('aria-label="io2 system status"', 'aria-label="حالة نظام io2"')
R('<span class="console__status">ONLINE</span>', '<span class="console__status">متصل</span>')
R('<li><span>Services</span>', '<li><span>الخدمات</span>')
R('<li><span>AI agents</span>', '<li><span>الوكلاء الأذكياء</span>')
R('<li><span>Markets</span>', '<li><span>الأسواق</span>')
R('<li><span>Mode</span>', '<li><span>الوضع</span>')
R('>Social media</li>', '>سوشال ميديا</li>')
R('>SEO &amp; Ads</li>', '>SEO وإعلانات</li>')
R('>AI-powered</li>', '>بقوة الذكاء الاصطناعي</li>')
R('>Branding</li>', '>الهوية التجارية</li>')
R('aria-label="Scroll to next section"><span>Scroll</span>', 'aria-label="انتقل إلى القسم التالي"><span>مرّر</span>')

# ---------- marquee ----------
R('<section class="marquee-band" aria-label="What we do">', '<section class="marquee-band" aria-label="ما نقدمه">')
for en, ar in [("Social Media Marketing", "التسويق عبر السوشال ميديا"), ("SEO", "تحسين محركات البحث"), ("Paid Advertising", "الإعلانات المدفوعة"), ("Content Production", "صناعة المحتوى"), ("Branding", "الهوية التجارية"), ("Web Design", "تصميم المواقع"), ("Growth Marketing", "التسويق للنمو"), ("AI Automation", "أتمتة الذكاء الاصطناعي")]:
    R(f'<span>{en}</span><i class="slash"', f'<span>{ar}</span><i class="slash"')

# ---------- manifesto ----------
R('<span class="idx">00</span> Manifesto', '<span class="idx">00</span> بياننا')
R("Many agencies report on reach: impressions, likes and followers. We focus on what moves your business: more leads, more sales and customers who come back. Every campaign is planned with data, supported by AI and judged on revenue.",
  "كثير من الوكالات تقيس نجاحها بالوصول: المشاهدات والإعجابات والمتابعين. نحن نركّز على ما يحرّك أعمالك فعلاً: عملاء محتملون أكثر، مبيعات أكثر، وعملاء يعودون للشراء. كل حملة تُخطَّط بالبيانات، ويدعمها الذكاء الاصطناعي، وتُقاس بالإيرادات.")
R('<span>AI agents answering your customers around the clock</span>', '<span>وكلاء ذكاء اصطناعي يردّون على عملائك على مدار الساعة</span>')
R('<span>Marketing services under one roof</span>', '<span>خدمات تسويقية تحت سقف واحد</span>')
R('<span>GCC markets served from Muscat</span>', '<span>أسواق خليجية نخدمها من مسقط</span>')
R('<span>Our aim: twice the results from the same budget</span>', '<span>هدفنا: ضعف النتائج بنفس الميزانية</span>')

# ---------- showcase ----------
R('aria-label="io2 team in Muscat"', 'aria-label="فريق io2 في مسقط"')
R('Muscat HQ · Strategy · Data · Creative · AI', 'المقر في مسقط · استراتيجية · بيانات · إبداع · ذكاء اصطناعي')
R('One team. <span class="slash" aria-hidden="true"></span>One system.<br>Built for Gulf growth.', 'فريق واحد. <span class="slash" aria-hidden="true"></span>نظام واحد.<br>مصمَّم لنمو الخليج.')

# ---------- system ----------
R('<span class="idx">02</span> The io2 System', '<span class="idx">02</span> نظام io2')
R('<span class="split">Three letters.</span>', '<span class="split">ثلاثة أحرف.</span>')
R('<span class="split">One way of working.</span>', '<span class="split">طريقة عمل واحدة.</span>')
R('Our logo describes how we work: we take your inputs, build them into a system and turn that into measurable growth.', 'شعارنا يصف طريقة عملنا: نأخذ مُدخلاتك، ونبنيها في نظام، ونحوّلها إلى نمو قابل للقياس.')
R('i · Input', 'i، المُدخل'); R('Capture every signal.', 'التقط كل إشارة.')
R('Ads, social, web, calls, CRM, sales data. We unify scattered inputs into one clean data layer, so decisions are based on evidence.',
  'الإعلانات والسوشال ميديا والموقع والمكالمات وCRM وبيانات المبيعات. نوحّد المُدخلات المبعثرة في طبقة بيانات واحدة نظيفة، لتُبنى القرارات على الأدلة لا الآراء.')
R('<li>Tracking &amp; attribution</li><li>Audits</li><li>Data unification</li>', '<li>التتبع والإسناد</li><li>التدقيق</li><li>توحيد البيانات</li>')
R('o · System', 'o، النظام'); R('Turn it into a plan.', 'حوّلها إلى خطة.')
R('Strategy, creative and automation work as one connected process. AI agents qualify and follow up with leads, while our team finds the audiences and messages that convert.',
  'الاستراتيجية والإبداع والأتمتة تعمل كعملية واحدة مترابطة. وكلاء الذكاء الاصطناعي يؤهّلون العملاء ويتابعونهم، وفريقنا يحدد الجماهير والرسائل التي تحقق التحويل.')
R('<li>AI agents</li><li>Automation</li><li>Creative ops</li>', '<li>وكلاء أذكياء</li><li>الأتمتة</li><li>عمليات إبداعية</li>')
R('2 · Output ×2', '2، المُخرج ×2'); R('Multiply the result.', 'ضاعِف النتيجة.')
R('Leads, pipeline, sales, retention. We review results every month and adjust spend, creative and messaging, so growth builds month after month.',
  'عملاء محتملون وصفقات ومبيعات واحتفاظ. النظام يتعلّم في كل دورة، يحسّن الإنفاق والمحتوى والمحادثات ليتراكم النمو بدل أن يبدأ من الصفر كل شهر.')
R('<li>Revenue KPIs</li><li>Live dashboards</li><li>Monthly reviews</li>', '<li>مؤشرات الإيرادات</li><li>لوحات مباشرة</li><li>مراجعات شهرية</li>')

# ---------- free consultation ----------
h = re.sub(r'<section class="consult".*?</section>', lambda m: render_consult(CON_AR).replace('="assets/', '="../assets/'), h, count=1, flags=re.S)

# ---------- services ----------
h = re.sub(r'<section class="services".*?</section>', lambda m: render_services(SVC_AR), h, count=1, flags=re.S)

# ---------- agents ----------
R('<span class="idx">03</span> AI Agents · Service 09', '<span class="idx">03</span> وكلاء الذكاء الاصطناعي · الخدمة 09')
R('<span class="split">Customers get answers,</span>', '<span class="split">عملاؤك يجدون الرد،</span>')
R('<span class="split">day and night.</span>', '<span class="split">ليلاً ونهاراً.</span>')
R('Our own AI agents answer questions, qualify leads, take bookings and update your CRM in Arabic and English, on every channel your customers use.', 'وكلاء ذكاء اصطناعي خاصّون بنا يجيبون ويؤهّلون ويبيعون ويحدّثون CRM، بالعربية والإنجليزية، عبر كل قناة يستخدمها عملاؤك.')
R('aria-label="Example AI agent conversation"', 'aria-label="مثال على محادثة وكيل ذكاء اصطناعي"')
R('WhatsApp Agent · live demo', 'وكيل واتساب · عرض مباشر')
R('السلام عليكم, do you have the SUV in white? I need it this month.', 'السلام عليكم، عندكم السيارة الـ SUV باللون الأبيض؟ أحتاجها هذا الشهر.')
R('وعليكم السلام! Yes, we have 2 white units at our Muscat showroom. Would you like a test drive this week?', 'وعليكم السلام! نعم، متوفر سيارتان باللون الأبيض في معرضنا بمسقط. تحب تحجز تجربة قيادة هذا الأسبوع؟')
R('>Thursday after 5?<', '>الخميس بعد الساعة ٥؟<')
R("Booked: Thursday 5:30 PM ✓ I've sent the location and a finance estimate.", 'تم الحجز: الخميس ٥:٣٠ مساءً ✓ أرسلت لك الموقع وتقدير التمويل.')
R('Lead qualified · intent: high', 'تم تأهيل العميل، نية الشراء: عالية')
R('CRM updated · stage: test drive', 'تم تحديث CRM، المرحلة: تجربة قيادة')
R('Sales rep notified · follow-up queued', 'تم إشعار مندوب المبيعات، المتابعة مجدولة')
R('alt="Omani customer service agent with headset in a Muscat contact centre, supported by io2 voice AI agents"', 'alt="موظفة خدمة عملاء عُمانية في مركز اتصال بمسقط يدعمها وكلاء io2 الصوتيون بالذكاء الاصطناعي"')
R('<span class="mono">Voice + chat AI</span><b>Your team handles the conversations that matter. <span class="slash" aria-hidden="true"></span>AI covers the rest around the clock, in Arabic and English.</b>',
  '<span class="mono">ذكاء صوتي + محادثة</span><b>فريقك يتولى المحادثات المهمة. <span class="slash" aria-hidden="true"></span>والذكاء الاصطناعي يتولى الباقي، على مدار الساعة، بالعربية والإنجليزية.</b>')
cards = [
 ("E-Commerce &amp; Social Agent", "وكيل التجارة الإلكترونية والسوشال", "Instant answers on Instagram, WhatsApp, Facebook and Telegram. Orders, tracking, bookings and AI-powered upsells.", "ردود فورية على إنستغرام وواتساب وفيسبوك وتيليغرام. طلبات وتتبع وحجوزات وبيع إضافي بالذكاء الاصطناعي."),
 ("Voice Sales Agent", "وكيل المبيعات الصوتي", "Handles inbound calls and runs outbound campaigns. It qualifies leads, books appointments and never misses a call.", "يستقبل المكالمات الواردة ويدير الحملات الصادرة، يؤهّل العملاء ويحجز المواعيد ولا يفوّت أي مكالمة."),
 ("AI Consultant Agent", "الوكيل الاستشاري الذكي", "Trained on your products and knowledge. Guides customers through complex decisions and supports internal teams.", "مُدرَّب على منتجاتك ومعرفتك. يرشد العملاء في القرارات المعقدة ويدعم فرقك الداخلية."),
 ("AI Chat Agent", "وكيل المحادثة الذكي", "Website and messaging assistants that answer instantly, capture leads and route complex cases to humans.", "مساعدون على موقعك وتطبيقات المراسلة يجيبون فوراً ويلتقطون بيانات العملاء ويحوّلون الحالات المعقدة إلى فريقك."),
 ("CRM Agent", "وكيل CRM", "Works inside your CRM. It logs every interaction, moves deals through the pipeline and sends follow-ups automatically.", "يعمل داخل نظام CRM، يسجّل كل تفاعل وينقل مراحل الصفقات ويرسل المتابعات تلقائياً."),
 ("Speech-to-Data Agent", "وكيل تحويل الكلام إلى بيانات", "Turns calls and meetings into structured, searchable data and enters it into your systems with no manual typing.", "يحوّل المكالمات والاجتماعات إلى بيانات منظمة قابلة للبحث ويدخلها في أنظمتك، دون أي إدخال يدوي."),
]
for t, ta, p, pa in cards:
    R(f'<h3>{t}</h3>', f'<h3>{ta}</h3>'); R(p, pa)

# ---------- values ----------
R('aria-label="Brand values"', 'aria-label="قيم العلامة"')
for en, ar in [("Clarity over noise", "الوضوح قبل الضجيج"), ("Impact over aesthetics", "الأثر قبل الشكل"), ("Systems over randomness", "الأنظمة قبل العشوائية"), ("Innovation with purpose", "ابتكار بهدف"), ("Precision in execution", "دقة في التنفيذ"), ("Consistency at scale", "اتساق على نطاق واسع")]:
    R(f'">{en}</span>', f'">{ar}</span>')

# ---------- process ----------
R('<span class="idx">04</span> How we work', '<span class="idx">04</span> كيف نعمل')
R('<span class="split">Input → Output</span>', '<span class="split">مُدخل ← مُخرج</span>')
R('A clear process, sped up by AI: we find the gaps, fix them and keep improving every month.', 'منهجية شفافة يسرّعها الذكاء الاصطناعي، من تشخيص الفجوات إلى نظام يتراكم أثره في كل دورة.')
R('<span>Start with a diagnosis</span>', '<span>ابدأ بالتشخيص</span>')
steps = [
 ("Diagnose", "التشخيص", "We audit your funnel, data, brand and tools to find the biggest opportunities and where budget is being wasted.", "ندقّق في مسار المبيعات والبيانات والعلامة والأدوات التقنية، لنكشف أين تختبئ الفرص وأين تتسرّب الميزانية.", "<li>Growth audit</li><li>Data review</li><li>Gap analysis</li>", "<li>تدقيق النمو</li><li>مراجعة البيانات</li><li>تحليل الفجوات</li>"),
 ("Architect", "الهندسة", "We plan the full system before anything is produced: strategy, KPIs, AI agent setup, content and automation.", "نصمّم النظام بالكامل، الاستراتيجية ومؤشرات الأداء ومنطق الوكلاء الأذكياء ومسارات المحتوى والأتمتة، قبل إنتاج أي محتوى.", "<li>System design</li><li>KPI model</li><li>Agent config</li>", "<li>تصميم النظام</li><li>نموذج المؤشرات</li><li>إعداد الوكلاء</li>"),
 ("Build &amp; Deploy", "البناء والإطلاق", "Content, campaigns and AI agents launch together, with tracking in place from day one.", "المحتوى والحملات والوكلاء الأذكياء ينطلقون كنظام واحد مترابط، مع قياس شامل من اليوم الأول.", "<li>Launch</li><li>AI deployment</li><li>Tracking</li>", "<li>الإطلاق</li><li>نشر الذكاء الاصطناعي</li><li>التتبع</li>"),
 ("Multiply", "المضاعفة", "We monitor, test and scale. Each month builds on the last instead of starting over.", "نراقب ونختبر ونوسّع. النظام يتعلّم في كل دورة، فتتراكم النتائج بدل أن تبدأ من جديد.", "<li>Optimisation</li><li>Experiments</li><li>Scale</li>", "<li>التحسين</li><li>التجارب</li><li>التوسّع</li>"),
]
for t, ta, p, pa, c, ca in steps:
    R(f'<h3>{t}</h3>', f'<h3>{ta}</h3>'); R(p, pa); R(c, ca)

# ---------- packages ----------
R('<span class="idx">05</span> AI Packages', '<span class="idx">05</span> باقات الذكاء الاصطناعي')
R('<span class="split">Choose your</span>', '<span class="split">اختر</span>')
R('<span class="split">automation level.</span>', '<span class="split">مستوى الأتمتة.</span>')
R('From your first AI agent to a full team of AI agents, built around where your business is today.', 'من أول وكيل ذكاء اصطناعي إلى فريق كامل من وكلاء الذكاء الاصطناعي، مصمَّمة لمرحلتك الحالية.')
R('01 / Starter</p>\n        <h3>Starter</h3>', '01 / البداية</p>\n        <h3>البداية</h3>')
R('Get your first AI agents live fast and stop losing leads after hours.', 'أطلق أول وكلائك الأذكياء بسرعة وتوقّف عن خسارة العملاء خارج أوقات الدوام.')
R('<li>AI Chat Agent</li><li>Social media response automation</li><li>Basic CRM integration</li><li>FAQ automation</li>', '<li>وكيل محادثة ذكي</li><li>أتمتة الردود على السوشال ميديا</li><li>ربط أساسي مع CRM</li><li>أتمتة الأسئلة الشائعة</li>')
R('Best for: startups, small businesses, online shops', 'الأنسب لـ: الشركات الناشئة والصغيرة والمتاجر الإلكترونية')
R('Most popular', 'الأكثر طلباً')
R('02 / Growth</p>\n        <h3>Growth</h3>', '02 / النمو</p>\n        <h3>النمو</h3>')
R('Automate sales and customer support at scale with our complete AI setup.', 'أتمتة المبيعات وخدمة العملاء على نطاق واسع، محرك النمو الكامل بالذكاء الاصطناعي.')
R('<li>Advanced e-commerce AI agent</li><li>Chat &amp; social media AI</li><li>CRM agent</li><li>Lead capture automation</li><li>Appointment booking automation</li>', '<li>وكيل تجارة إلكترونية متقدم</li><li>ذكاء اصطناعي للمحادثات والسوشال</li><li>وكيل CRM</li><li>أتمتة التقاط العملاء المحتملين</li><li>أتمتة حجز المواعيد</li>')
R('Best for: e-commerce, service companies, car dealerships', 'الأنسب لـ: التجارة الإلكترونية وشركات الخدمات ووكالات السيارات')
R('03 / Enterprise</p>\n        <h3>Enterprise</h3>', '03 / المؤسسات</p>\n        <h3>المؤسسات</h3>')
R('AI agents that automate communication, sales and operations from start to finish.', 'وكلاء ذكاء اصطناعي يؤتمتون التواصل والمبيعات والعمليات من البداية إلى النهاية.')
R('<li>Voice Sales AI agent</li><li>Advanced chat &amp; social agents</li><li>CRM automation agent</li><li>Data entry &amp; speech-to-text</li><li>Custom integrations &amp; workflows</li>', '<li>وكيل مبيعات صوتي</li><li>وكلاء محادثة وسوشال متقدمون</li><li>وكيل أتمتة CRM</li><li>إدخال البيانات وتحويل الكلام إلى نص</li><li>تكاملات وسير عمل مخصّصة</li>')
R('Best for: large businesses, call centres, marketplaces', 'الأنسب لـ: الشركات الكبرى ومراكز الاتصال والأسواق الإلكترونية')
h = h.replace('<span>Get started</span>', '<span>ابدأ الآن</span>')
R('<span>Talk to us</span>', '<span>تحدّث معنا</span>')
from urllib.parse import quote
for en, ar in [("Starter", "البداية"), ("Growth", "النمو")]:
    h = re.sub(r'https://wa\.me/96877220770\?text=Hi%20io2%2C%20I%27m%20interested%20in%20the%20' + en + r'%20AI%20package\.',
               'https://wa.me/96877220770?text=' + quote(f'مرحباً io2، أنا مهتم بباقة {ar} للذكاء الاصطناعي.'), h)
h = re.sub(r'https://wa\.me/96877220770\?text=Hi%20io2%2C%20I%27d%20like%20to%20talk%20about%20the%20Enterprise%20AI%20package\.',
           'https://wa.me/96877220770?text=' + quote('مرحباً io2، أود التحدث عن باقة المؤسسات للذكاء الاصطناعي.'), h)

# ---------- reach ----------
R('<span class="idx">06</span> Built in Muscat', '<span class="idx">06</span> صُنع في مسقط')
R('<span class="split">Local insight.</span>', '<span class="split">فهمٌ محلي.</span>')
R('<span class="split">Gulf-wide scale.</span>', '<span class="split">وانتشار خليجي.</span>')
R('We understand Arabic audiences, regional platforms and how GCC buyers decide. Headquartered in Muscat, growing brands across the Gulf.', 'نفهم الجمهور العربي والمنصات الإقليمية وكيف يتخذ المشتري الخليجي قراره. مقرّنا في مسقط، ونطوّر العلامات في كل دول الخليج.')
R('<li><b>Full-service + AI, one team.</b> Marketing, brand, web and AI agents under one strategy, with no vendors to juggle.</li>', '<li><b>خدمات متكاملة + ذكاء اصطناعي، فريق واحد.</b> التسويق والعلامة والمواقع والوكلاء الأذكياء، استراتيجية واحدة دون تعدّد الموردين.</li>')
R('<li><b>Growth hacking first.</b> Faster experiments, smarter targeting and results that build over time.</li>', '<li><b>هندسة النمو أولاً.</b> تجارب أسرع، استهداف أذكى، ونتائج تتحسّن مع الوقت.</li>')
R('<li><b>Measured on business impact.</b> Clear KPIs tied to revenue. We report on results you can bank.</li>', '<li><b>نُقاس بالأثر على أعمالك.</b> مؤشرات واضحة مرتبطة بالإيرادات، ونتائج يمكنك قياسها.</li>')
R('aria-label="Map of GCC markets connected to Muscat: Oman, UAE, Saudi Arabia, Qatar, Bahrain, Kuwait"', 'aria-label="خريطة أسواق الخليج المرتبطة بمسقط: عُمان، الإمارات، السعودية، قطر، البحرين، الكويت"')
for en, ar in [("DUBAI", "دبي"), ("DOHA", "الدوحة"), ("MANAMA", "المنامة"), ("RIYADH", "الرياض"), ("KUWAIT", "الكويت"), ("MUSCAT · HQ", "مسقط · المقر")]:
    R(f'text-anchor="middle">{en}</text>', f'text-anchor="middle">{ar}</text>')

# ---------- markets ----------
R('<span class="idx">07</span> Markets we grow', '<span class="idx">07</span> الأسواق التي ننمّيها')
R('<span class="split">One agency.</span>', '<span class="split">وكالة واحدة.</span>')
R('<span class="split">Six GCC markets.</span>', '<span class="split">ستة أسواق خليجية.</span>')
R('A digital marketing and AI growth partner for Oman, the UAE, Saudi Arabia, Qatar, Kuwait and Bahrain, with campaigns in Arabic and English tailored to how each market buys.', 'شريك تسويق رقمي ونمو بالذكاء الاصطناعي في عُمان والإمارات والسعودية وقطر والكويت والبحرين، حملات بالعربية والإنجليزية مصمَّمة لطريقة الشراء في كل سوق.')
markets = [
 ('alt="Muttrah Corniche in Muscat, Oman at dusk"', 'alt="كورنيش مطرح في مسقط، عُمان عند الغروب"', 'Oman', 'عُمان', 'Digital marketing agency in Muscat, Oman', 'شركة تسويق رقمي في مسقط، عُمان', 'Our home market. Performance campaigns, SEO and AI agents for Omani brands from Muscat to Sohar and Salalah.', 'سوقنا الأم. حملات أداء وSEO ووكلاء ذكاء اصطناعي للعلامات العُمانية، من مسقط إلى صحار وصلالة.'),
 ('alt="Downtown Dubai skyline with the Burj Khalifa at dusk"', 'alt="أفق وسط دبي وبرج خليفة عند الغروب"', 'UAE', 'الإمارات', 'Growth marketing in Dubai &amp; Abu Dhabi', 'تسويق النمو في دبي وأبوظبي', "Data-led acquisition for one of the region's most competitive markets, focused on cost per lead rather than impressions.", 'استقطاب مبني على البيانات في أحد أكثر أسواق المنطقة تنافساً، هدفه خفض تكلفة العميل المحتمل لا زيادة المشاهدات.'),
 ('alt="Kingdom Centre tower in Riyadh, Saudi Arabia at sunset"', 'alt="برج المملكة في الرياض، السعودية عند الغروب"', 'Saudi Arabia', 'السعودية', 'AI marketing for Riyadh, Jeddah &amp; KSA', 'التسويق بالذكاء الاصطناعي في الرياض وجدة والمملكة', "Arabic-first campaigns, WhatsApp commerce and voice agents scaled for the Kingdom's Vision 2030 growth.", 'حملات عربية أولاً وتجارة عبر واتساب ووكلاء صوتيون مصمَّمون لنمو المملكة ضمن رؤية 2030.'),
 ('alt="West Bay skyline in Doha, Qatar"', 'alt="أفق الخليج الغربي في الدوحة، قطر"', 'Qatar', 'قطر', 'Performance marketing in Doha', 'التسويق بالأداء في الدوحة', "Premium positioning plus precise targeting for Qatar's high-value audiences.", 'تموضع فاخر واستهداف دقيق لجمهور قطر عالي القيمة.'),
 ('alt="Kuwait Towers in Kuwait City under a blue sky"', 'alt="أبراج الكويت في مدينة الكويت تحت سماء زرقاء"', 'Kuwait', 'الكويت', 'Social &amp; e-commerce growth in Kuwait', 'نمو السوشال والتجارة الإلكترونية في الكويت', "Social-first campaigns and AI customer service for Kuwait's mobile-native shoppers.", 'محركات نمو تعتمد على السوشال أولاً وخدمة عملاء بالذكاء الاصطناعي للمتسوقين الكويتيين عبر الجوال.'),
 ('alt="Bahrain World Trade Center in Manama at sunrise"', 'alt="مركز البحرين التجاري العالمي في المنامة عند الشروق"', 'Bahrain', 'البحرين', 'Digital growth in Manama, Bahrain', 'النمو الرقمي في المنامة، البحرين', "Lean, measurable systems for Bahrain's fintech, retail and service brands.", 'أنظمة رشيقة وقابلة للقياس لعلامات التقنية المالية والتجزئة والخدمات في البحرين.'),
]
for alt, alta, c, ca, t, ta, p, pa in markets:
    R(alt, alta); R(f'<p class="market__country">{c}</p>', f'<p class="market__country">{ca}</p>'); R(f'<h3>{t}</h3>', f'<h3>{ta}</h3>'); R(p, pa)

# ---------- FAQ ----------
R('<span class="idx">08</span> FAQ', '<span class="idx">08</span> الأسئلة الشائعة')
R('<span class="split">Straight</span>', '<span class="split">إجابات</span>')
R('<span class="split">answers.</span>', '<span class="split">مباشرة.</span>')
a = h.index('<div class="faq__list">'); b = h.index('</div>', a) + len('</div>')
qa = [
 ("هل الاستشارة مجانية فعلاً؟", "نعم. يمكن لكل نشاط تجاري حجز استشارة فردية مجانية واحدة مع خبراء التسويق والأعمال لدينا، مدتها ٣٠ دقيقة، أونلاين أو في مسقط، بالعربية أو الإنجليزية، ودون أي التزام بالعمل معنا."),
 ("ما هي خدمات التسويق التي تقدمونها؟", "التسويق عبر السوشال ميديا، التسويق بالأداء والإعلانات المدفوعة (Google وMeta وTikTok وSnapchat)، تحسين محركات البحث، صناعة المحتوى والفيديو، الهوية التجارية، تصميم وتطوير المواقع، التسويق بالبريد وCRM والأتمتة، الاستراتيجية التسويقية والتحليلات، بالإضافة إلى وكلاء الذكاء الاصطناعي لواتساب والمحادثة والصوت."),
 ("بماذا تختلف io2 عن وكالات التسويق التقليدية؟", "الوكالات التقليدية تبيع الوصول. نحن نُحاسَب على النمو: كل مشروع يُبنى كنظام مرتبط بمؤشرات الإيرادات، العملاء المحتملون والصفقات والتحويل وقيمة العميل، مع ذكاء اصطناعي يعمل داخله على مدار الساعة."),
 ("هل io2 شركة تسويق رقمي في عُمان؟", "نعم، مقر io2 في مسقط. نقدم التسويق بالأداء وتحسين محركات البحث والسوشال ميديا والمحتوى والهوية والمواقع وأتمتة الذكاء الاصطناعي للشركات العُمانية وللعلامات في دول الخليج."),
 ("ما الأسواق التي تخدمونها؟", "مقرنا في مسقط ونعمل مع الشركات في دول الخليج، عُمان والإمارات والسعودية وقطر والكويت والبحرين، بالعربية والإنجليزية."),
 ("هل يتحدث الوكلاء الأذكياء العربية؟", "نعم. وكلاؤنا مهيّؤون للمحادثة بالعربية والإنجليزية، ومدرَّبون على منتجاتك وسياساتك وأسلوب علامتك."),
 ("كم يستغرق إطلاق وكيل ذكاء اصطناعي؟", "يعتمد ذلك على التكاملات ونطاق العمل. نبدأ بالتشخيص، ونتفق على تصميم النظام، ثم نُطلق على مراحل لترى القيمة مبكراً."),
 ("كيف نبدأ؟", 'احجز تدقيق النمو عبر واتساب (<bdi dir="ltr">+968 7722 0770</bdi>) أو راسلنا على contact@io2.agency. نرسم مسار مبيعاتك وبياناتك وأدواتك، ثم نقترح النظام المناسب.'),
]
h = h[:a] + '<div class="faq__list">\n' + '\n'.join(f'      <details><summary>{q}</summary><p>{t}</p></details>' for q, t in qa) + '\n    </div>' + h[b:]

# ---------- contact ----------
R('<span class="idx">09</span> Get in touch', '<span class="idx">09</span> تواصل معنا')
R('<span class="split">Ready to</span>', '<span class="split">مستعد</span>')
R('<span class="split">scale your system?</span>', '<span class="split">لتوسيع نظامك؟</span>')
R("Tell us where you want to grow. We'll come back with a clear diagnosis and practical next steps.", 'أخبرنا أين تريد أن تنمو. سنعود إليك بتشخيص واضح وخطوات عملية.')
R('<span class="mono">Email</span>', '<span class="mono">البريد الإلكتروني</span>')
R('<span class="mono">WhatsApp</span>', '<span class="mono">واتساب</span>')
R('<span class="mono">HQ</span>Muscat, Sultanate of Oman', '<span class="mono">المقر</span>مسقط، سلطنة عُمان')
R('<label for="f-name">Name</label>', '<label for="f-name">الاسم</label>')
R('Please enter your name.', 'يرجى إدخال اسمك.')
R('<label for="f-company">Company</label>', '<label for="f-company">الشركة</label>')
R('<label for="f-goal">Main goal</label>', '<label for="f-goal">الهدف الرئيسي</label>')
for en, ar in [("More qualified leads", "عملاء محتملون أعلى جودة"), ("More online sales", "مبيعات أونلاين أكثر"), ("Deploy AI agents", "إطلاق وكلاء ذكاء اصطناعي"), ("Automate operations &amp; CRM", "أتمتة العمليات وCRM"), ("Brand &amp; website", "الهوية والموقع الإلكتروني")]:
    R(f'<option>{en}</option>', f'<option>{ar}</option>')
R('Tell us more <span>(optional)</span>', 'أخبرنا المزيد <span>(اختياري)</span>')
R('<span>Send message</span>', '<span>أرسل الرسالة</span>')
R('Goes straight to contact@io2.agency. Prefer WhatsApp? <a href="https://wa.me/96877220770" target="_blank" rel="noopener">Message us</a>', 'تصل مباشرة إلى contact@io2.agency. تفضّل واتساب؟ <a href="https://wa.me/96877220770" target="_blank" rel="noopener">راسلنا</a>')
R('<label for="f-email">Email</label>', '<label for="f-email">البريد الإلكتروني</label>')
R('Please enter a valid email address.', 'يرجى إدخال بريد إلكتروني صحيح.')
R('<label for="f-phone">Phone / WhatsApp <span>(optional)</span></label>', '<label for="f-phone">الهاتف / واتساب <span>(اختياري)</span></label>')
R('<label for="f-hp">Leave this field empty</label>', '<label for="f-hp">اترك هذا الحقل فارغاً</label>')
R('name="_subject" value="New enquiry from io2.agency"', 'name="_subject" value="رسالة جديدة من io2.agency (الموقع العربي)"')
R('name="_next" value="https://io2.agency/?sent=1#contact"', 'name="_next" value="https://io2.agency/ar/?sent=1#contact"')
R('name="website_language" value="English"', 'name="website_language" value="Arabic"')

# ---------- footer ----------
R('<span class="slash" aria-hidden="true"></span>From input to impact.</p>', '<span class="slash" aria-hidden="true"></span>من المُدخل إلى الأثر.</p>')
R('<h3 class="mono footer__h">Services</h3><a href="services/social-media-marketing/">Social Media Marketing</a><a href="services/performance-marketing/">Paid Ads &amp; Performance</a><a href="services/seo/">SEO</a><a href="services/content-production/">Content Production</a><a href="services/branding/">Branding</a><a href="services/web-design/">Web Design</a><a href="services/email-crm-automation/">Email &amp; CRM</a><a href="services/marketing-strategy/">Marketing Strategy</a><a href="services/ai-agents/">AI Agents</a><a href="services/">All services</a>',
  '<h3 class="mono footer__h">الخدمات</h3><a href="services/social-media-marketing/">التسويق عبر السوشال ميديا</a><a href="services/performance-marketing/">الإعلانات المدفوعة والأداء</a><a href="services/seo/">تحسين محركات البحث</a><a href="services/content-production/">صناعة المحتوى</a><a href="services/branding/">الهوية التجارية</a><a href="services/web-design/">تصميم المواقع</a><a href="services/email-crm-automation/">البريد وCRM</a><a href="services/marketing-strategy/">الاستراتيجية التسويقية</a><a href="services/ai-agents/">وكلاء الذكاء الاصطناعي</a><a href="services/">كل الخدمات</a>')
R('<h3 class="mono footer__h">AI Agents</h3><a href="#agents">E-Commerce Agent</a><a href="#agents">Voice Sales Agent</a><a href="#agents">CRM Agent</a><a href="#packages">الباقات</a>',
  '<h3 class="mono footer__h">الوكلاء الأذكياء</h3><a href="#agents">وكيل التجارة الإلكترونية</a><a href="#agents">وكيل المبيعات الصوتي</a><a href="#agents">وكيل CRM</a><a href="#packages">الباقات</a>')
R('<h3 class="mono footer__h">Contact</h3>', '<h3 class="mono footer__h">تواصل</h3>')
R('<span>Muscat, Sultanate of Oman</span>', '<span>مسقط، سلطنة عُمان</span>')
R('<h3 class="mono footer__h">Social</h3>', '<h3 class="mono footer__h">تابعنا</h3>')
R('<span>Instagram</span>', '<span>إنستغرام</span>')
R('<span>LinkedIn</span>', '<span>لينكدإن</span>')
R('<span>Facebook</span>', '<span>فيسبوك</span>')
R('<span>WhatsApp</span></a></div>', '<span>واتساب</span></a></div>')
for en, ar in [('io2 on Instagram', 'io2 على إنستغرام'), ('io2 on LinkedIn', 'io2 على لينكدإن'), ('io2 on Facebook', 'io2 على فيسبوك'), ('Chat with io2 on WhatsApp', 'تواصل مع io2 عبر واتساب')]:
    R(f'aria-label="{en}"', f'aria-label="{ar}"')
h = h.replace('https://wa.me/96877220770?text=Hi%20io2%2C%20I%27d%20like%20to%20know%20more%20about%20your%20services.', 'https://wa.me/96877220770?text=' + quote('مرحباً io2، أود معرفة المزيد عن خدماتكم.'))
h = re.sub(r'<p class="footer__seo">.*?</p>', '<p class="footer__seo">io2 وكالة تسويق للنمو في مسقط، سلطنة عُمان، نقدم التسويق عبر السوشال ميديا والتسويق بالأداء والإعلانات المدفوعة وتحسين محركات البحث وصناعة المحتوى والفيديو والهوية التجارية وتصميم المواقع والتسويق بالبريد وCRM والاستراتيجية التسويقية وأتمتة الذكاء الاصطناعي وروبوتات المحادثة ووكلاء الذكاء الاصطناعي الصوتيين وأتمتة CRM والتسويق والهوية البصرية وتطوير المواقع للشركات في عُمان والإمارات والسعودية وقطر والكويت والبحرين.</p>', h, 1, flags=re.S)
R('io2 Agency. All rights reserved.', 'io2 Agency. جميع الحقوق محفوظة.')
R('Back to top ↑', 'العودة للأعلى ↑')
R('<a href="ar/" class="footer__lang" hreflang="ar" lang="ar">النسخة العربية</a>', '<a href="../" class="footer__lang" hreflang="en" lang="en">English version</a>')

open(f'{root}/ar/index.html', 'w', encoding='utf-8').write(h)
# leftover English check (visible text only)
body = re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>', '', h[h.index('<body'):], flags=re.S)
txt = re.sub(r'<[^>]+>', '\n', body)
left = [t.strip() for t in txt.split('\n') if re.search(r'[A-Za-z]{4,}', t) and t.strip()]
print('written; english-looking leftovers:', len(left))
for t in left: print('  ·', t[:90])
