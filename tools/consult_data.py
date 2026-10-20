"""Free one-time consultation section (EN + AR). Single source of truth for both pages."""

ICONS = [
    '<path d="M3 4h18l-7 8v6l-4 2v-8z"/>',                                   # funnel
    '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',                          # bars
    '<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/>',                       # growth
    '<path d="M9 6h11M9 12h11M9 18h11"/><path d="M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2"/>',  # plan
]

EN = {
    "eyebrow": "Free consultation",
    "h2a": "A free 1:1 session", "h2b": "with growth experts.",
    "lead": "Not sure where to start? Book a one-time, no-obligation consultation with io2's marketing and business experts. We review your business, your marketing and your numbers, and you leave with clear next steps whether you work with us or not.",
    "items": [
        ("Marketing &amp; funnel review", "Where your leads come from, where they drop off and what each one costs you."),
        ("Competitor snapshot", "How you compare with the brands winning your market in Oman and the GCC."),
        ("Growth opportunities", "The fastest wins across social media, SEO, paid ads, content and automation."),
        ("Your action plan", "A clear, prioritised list of next steps you can act on straight away."),
    ],
    "chips": ["30 minutes", "Online or in Muscat", "Arabic or English", "No obligation"],
    "card_k": "One free session per business",
    "card_t": "Book your free consultation",
    "name": "Name", "phone": "WhatsApp number", "company": "Company", "company_opt": "(optional)",
    "need": "What do you need help with?",
    "needs": ["Marketing strategy", "Social media marketing", "SEO &amp; paid ads", "Branding &amp; website", "Sales &amp; business growth", "AI &amp; automation"],
    "time": "Preferred time",
    "times": ["Morning", "Afternoon", "Evening"],
    "err_name": "Please enter your name.", "err_phone": "Please enter a valid WhatsApp number.",
    "btn": "Book my free consultation",
    "note": "Opens WhatsApp with your request pre-filled. We'll confirm your slot there.",
    "card_t2": "Book your free 30-min strategy call", "badge": "30 min",
    "who_t": "io2 marketing &amp; business experts", "who_s": "Muscat, Oman · Arabic &amp; English",
    "steps": [("Pick a time", "Choose a slot that suits you. It takes 30 seconds."), ("Meet the experts", "A 30-minute video call, or in person at our Muscat office."), ("Leave with a plan", "Clear, prioritised next steps for your marketing and growth.")],
    "days_label": "Choose a day to see open times",
    "see_all": "See all available times",
    "trust": ["100% free", "No obligation", "Calendar invite &amp; reminders"],
    "wa_alt": "Prefer WhatsApp? Message us",
    "cal_aria": "Booking calendar for a free consultation",
    "cal_loading": "Loading the booking calendar…",
    "cal_open": "Open the booking calendar",
    "cal_note": "Pick a time that suits you and you'll get a calendar invite and reminders by email.",
    "cal_done": "You're booked! Check your email for the calendar invite. Speak soon.",
}

AR = {
    "eyebrow": "استشارة مجانية",
    "h2a": "جلسة مجانية فردية", "h2b": "مع خبراء النمو.",
    "lead": "لا تعرف من أين تبدأ؟ احجز استشارة مجانية لمرة واحدة ودون أي التزام مع خبراء التسويق والأعمال في io2. نراجع نشاطك وتسويقك وأرقامك، وتخرج بخطوات واضحة، سواء عملت معنا أم لا.",
    "items": [
        ("مراجعة التسويق ومسار المبيعات", "من أين يأتي عملاؤك المحتملون، وأين يتسرّبون، وكم يكلّفك كل عميل."),
        ("لمحة عن المنافسين", "كيف تقارن بالعلامات التي تتصدّر سوقك في عُمان والخليج."),
        ("فرص النمو", "أسرع المكاسب عبر السوشال ميديا وSEO والإعلانات المدفوعة والمحتوى والأتمتة."),
        ("خطة العمل", "قائمة واضحة ومرتّبة حسب الأولوية بالخطوات التالية لتنفيذها فوراً."),
    ],
    "chips": ["٣٠ دقيقة", "أونلاين أو في مسقط", "بالعربية أو الإنجليزية", "دون أي التزام"],
    "card_k": "جلسة مجانية واحدة لكل نشاط تجاري",
    "card_t": "احجز استشارتك المجانية",
    "name": "الاسم", "phone": "رقم الواتساب", "company": "الشركة", "company_opt": "(اختياري)",
    "need": "بماذا تحتاج المساعدة؟",
    "needs": ["الاستراتيجية التسويقية", "التسويق عبر السوشال ميديا", "SEO والإعلانات المدفوعة", "الهوية والموقع الإلكتروني", "المبيعات ونمو الأعمال", "الذكاء الاصطناعي والأتمتة"],
    "time": "الوقت المفضّل",
    "times": ["صباحاً", "بعد الظهر", "مساءً"],
    "err_name": "يرجى إدخال اسمك.", "err_phone": "يرجى إدخال رقم واتساب صحيح.",
    "btn": "احجز استشارتي المجانية",
    "note": "سيفتح واتساب وطلبك جاهز للإرسال، وسنؤكد موعدك هناك.",
    "card_t2": "احجز مكالمتك الاستراتيجية المجانية", "badge": "٣٠ دقيقة",
    "who_t": "خبراء التسويق والأعمال في io2", "who_s": "مسقط، عُمان · بالعربية والإنجليزية",
    "steps": [("اختر الموعد", "اختر الوقت المناسب لك، يستغرق ذلك ٣٠ ثانية فقط."), ("قابل الخبراء", "مكالمة فيديو لمدة ٣٠ دقيقة، أو لقاء حضوري في مكتبنا بمسقط."), ("اخرج بخطة", "خطوات واضحة ومرتّبة حسب الأولوية لتسويقك ونموّك.")],
    "days_label": "اختر يوماً لعرض المواعيد المتاحة",
    "see_all": "عرض كل المواعيد المتاحة",
    "trust": ["مجانية ١٠٠٪", "دون أي التزام", "دعوة تقويم وتذكيرات"],
    "wa_alt": "تفضّل واتساب؟ راسلنا",
    "cal_aria": "تقويم حجز الاستشارة المجانية",
    "cal_loading": "جارٍ تحميل تقويم الحجز…",
    "cal_open": "افتح تقويم الحجز",
    "cal_note": "اختر الوقت المناسب لك، ستصلك دعوة التقويم والتذكيرات عبر البريد الإلكتروني.",
    "cal_done": "تم الحجز! تحقّق من بريدك الإلكتروني لدعوة التقويم. نراك قريباً.",
}


def render(d):
    items = "\n".join(
        f'''          <li><span class="consult__ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[i]}</svg></span><div><h3>{t}</h3><p>{p}</p></div></li>'''
        for i, (t, p) in enumerate(d["items"]))
    chips = "".join(f"<li>{c}</li>" for c in d["chips"])
    needs = "".join(f"<option>{n}</option>" for n in d["needs"])
    times = "".join(f"<option>{t}</option>" for t in d["times"])
    steps = "\n".join(f'          <li><span class="cal__step-n mono">{i:02d}</span><div><b>{t}</b><span>{p}</span></div></li>' for i, (t, p) in enumerate(d["steps"], 1))
    trust = "".join(f'<li><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>{t}</li>' for t in d["trust"])
    return f'''<section class="consult" id="consultation" data-theme="indigo">
  <div class="bgv bgv--indigo" aria-hidden="true"><video class="bgv__video" muted loop playsinline preload="none" data-poster="assets/video/office-night.jpg" data-src="assets/video/office-night.mp4"></video></div>
  <div class="wrap consult__wrap">
    <div class="consult__copy">
      <p class="eyebrow mono"><span class="idx">●</span> {d["eyebrow"]}</p>
      <h2 class="h2"><span class="split">{d["h2a"]}</span><br><span class="slash" aria-hidden="true"></span><span class="split">{d["h2b"]}</span></h2>
      <p class="lead">{d["lead"]}</p>
      <ul class="consult__list">
{items}
      </ul>
      <ul class="chips consult__chips">{chips}</ul>
    </div>
    <div class="consult__card">
      <p class="mono consult__k"><span class="dot dot--live"></span>{d["card_k"]}</p>
      <h3 class="consult__t"><span class="t-form">{d["card_t"]}</span><span class="t-cal">{d["card_t2"]}</span></h3>
      <div class="cal" hidden>
        <div class="cal__who">
          <span class="cal__mark"><img src="assets/io2-logo-white.png" alt="" width="1200" height="663"></span>
          <div><p class="cal__who-t">{d["who_t"]}</p><p class="cal__who-s mono">{d["who_s"]}</p></div>
          <span class="cal__badge mono">{d["badge"]}</span>
        </div>
        <ol class="cal__steps">
{steps}
        </ol>
        <p class="cal__label mono">{d["days_label"]}</p>
        <div class="cal__days" role="list" aria-label="{d["days_label"]}"></div>
        <button type="button" class="btn btn--yellow btn--lg magnetic cal__all" data-calendly><span>{d["see_all"]}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
        <ul class="cal__trust">{trust}</ul>
        <a class="cal__wa" href="https://wa.me/96877220770" target="_blank" rel="noopener">{d["wa_alt"]} →</a>
        <p class="cal__done" hidden role="status">{d["cal_done"]}</p>
      </div>
      <form class="consult__form" novalidate>
      <div class="field"><label for="c-name">{d["name"]}</label><input id="c-name" name="name" autocomplete="name" required><p class="err" id="ce-name">{d["err_name"]}</p></div>
        <div class="field"><label for="c-phone">{d["phone"]}</label><input id="c-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" placeholder="+968" required><p class="err" id="ce-phone">{d["err_phone"]}</p></div>
        <div class="field"><label for="c-company">{d["company"]} <span>{d["company_opt"]}</span></label><input id="c-company" name="company" autocomplete="organization"></div>
        <div class="field"><label for="c-need">{d["need"]}</label><select id="c-need" name="need">{needs}</select></div>
        <div class="field"><label for="c-time">{d["time"]}</label><select id="c-time" name="time">{times}</select></div>
        <button class="btn btn--yellow btn--lg magnetic" type="submit"><span>{d["btn"]}</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
        <p class="consult__note mono">{d["note"]}</p>
      </form>
    </div>
  </div>
</section>'''
