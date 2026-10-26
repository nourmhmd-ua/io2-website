/* io2: interactions & motion
   GSAP 3.13 (ScrollTrigger) + Lenis smooth scroll, both self-hosted. Headline splitting is done here (no SplitText).
   Everything degrades to a fully readable static page without JS / with reduced motion. */
(() => {
  "use strict";

  const root = document.documentElement;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const RTL = document.documentElement.dir === "rtl";
  const T = RTL ? {
    openMenu: "فتح القائمة", closeMenu: "إغلاق القائمة",
    toLight: "التبديل إلى الوضع الفاتح", toDark: "التبديل إلى الوضع الداكن",
    hi: (n, c) => `مرحباً io2، معكم ${n}${c ? " من " + c : ""}.`, goal: "الهدف الرئيسي",
    sending: "جارٍ الإرسال…", sent: "شكراً لك! تم إرسال رسالتك، وسنرد عليك عبر البريد الإلكتروني قريباً.",
    sendFailed: "عذراً، تعذّر إرسال الرسالة. راسلنا على contact@io2.agency أو عبر واتساب +968 7722 0770.",
    consult: (f) => [`مرحباً io2، أود حجز الاستشارة المجانية.`, `الاسم: ${f.name}`, f.company && `الشركة: ${f.company}`, `واتساب: ${f.phone}`, `أحتاج المساعدة في: ${f.need}`, `الوقت المفضّل: ${f.time}`],
  } : {
    openMenu: "Open menu", closeMenu: "Close menu",
    toLight: "Switch to light mode", toDark: "Switch to dark mode",
    hi: (n, c) => `Hi io2, I'm ${n}${c ? " from " + c : ""}.`, goal: "Main goal",
    sending: "Sending…", sent: "Thank you! Your message has been sent. We'll reply by email soon.",
    sendFailed: "Sorry, the message couldn't be sent. Please email contact@io2.agency or WhatsApp +968 7722 0770.",
    consult: (f) => [`Hi io2, I'd like to book my free consultation.`, `Name: ${f.name}`, f.company && `Company: ${f.company}`, `WhatsApp: ${f.phone}`, `Help needed with: ${f.need}`, `Preferred time: ${f.time}`],
  };
  // GA4 events (gtag is loaded in the page <head>; silently skipped if blocked)
  const trackEvent = (name, params = {}) => { try { if (typeof window.gtag === "function") window.gtag("event", name, Object.assign({ page_language: RTL ? "ar" : "en" }, params)); } catch (e) {} };
  const hasGSAP = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";

  $(".js-year").textContent = new Date().getFullYear();

  // always start at the top (the intro plays from the hero), unless a #section link was opened
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  if (!location.hash) window.scrollTo(0, 0);

  /* ---------- Manifesto: split into words (works with or without GSAP) ---------- */
  const highlight = new Set(["leads", "sales", "revenue", "عملاء", "مبيعات", "بالإيرادات"]);
  $$(".reveal-words").forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words
      .map((w) => `<span class="w${highlight.has(w.toLowerCase().replace(/[.,:;!?،]/g, "")) ? " hl" : ""}">${w}</span>`)
      .join(" ");
  });

  /* ---------- Static fallback ---------- */
  const showStatic = () => {
    const sys = $(".system"); if (sys) sys.classList.add("glyphs-on");
    const loader = $(".loader");
    if (loader) loader.remove();
    $$(".reveal-words .w").forEach((w) => w.classList.add("on"));
    $$(".demo [data-step]").forEach((s) => { if (!s.classList.contains("typing")) s.classList.add("show"); });
    $$(".counter").forEach((c) => (c.textContent = String(c.dataset.to).padStart(+c.dataset.pad || 1, "0")));
  };

  if (!hasGSAP || reduce) {
    showStatic();
    initUI(null);
    initBgVideos();
    initHeroCanvas(true);
    return;
  }

  const { gsap, ScrollTrigger } = window;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (window.Lenis) {
    lenis = new window.Lenis({ duration: .9, easing: (t) => 1 - Math.pow(1 - t, 4), smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    lenis.stop();
  }

  initUI(lenis);
  initBgVideos();
  initHeroCanvas(false);

  // Build all motion once web fonts are ready (so headline measurements use the real glyphs).
  // The preloader covers this moment; a timeout guards against a stalled font request.
  let motionStarted = false;
  const startMotion = () => {
    if (motionStarted) return;
    motionStarted = true;
    /* ---------- Split headlines (lightweight, no SplitText) ---------- */
    const esc = (t) => t.replace(/&/g, "&amp;").replace(/</g, "&lt;");
    // Section headlines: each word rises inside its own mask
    const splitWords = (el) => {
      el.innerHTML = el.textContent.trim().split(/\s+/).map((w) => `<span class="wm"><span class="wi">${esc(w)}</span></span>`).join(" ");
      return $$(".wi", el);
    };
    // Hero: letters in English, words in Arabic (letters must stay joined).
    // Screen readers get one clean text copy; the animated pieces are hidden from them.
    const heroSplits = $$(".hero__title .split");
    const heroParts = heroSplits.flatMap((el) => {
      const text = el.textContent.trim();
      const sr = document.createElement("span");
      sr.className = "sr-only"; sr.textContent = text;
      el.before(sr);
      el.setAttribute("aria-hidden", "true");
      el.innerHTML = RTL
        ? text.split(/\s+/).map((w) => `<span class="ch">${esc(w)}</span>`).join(" ")
        : text.split(/\s+/).map((w) => `<span class="hw">${[...w].map((c) => `<span class="ch">${esc(c)}</span>`).join("")}</span>`).join(" ");
      return $$(".ch", el);
    });

    /* ---------- Preloader → intro ---------- */
    const intro = gsap.timeline({ paused: true });
    intro.from(heroParts, {
      yPercent: 115, rotate: 8, duration: 1.1, ease: "expo.out", stagger: RTL ? 0.08 : 0.028,
    }, 0);
    intro
      .from(".hero__title .slash", { clipPath: "inset(100% 0 0 0)", duration: .8, ease: "expo.out" }, .35)
      .from(".hero__eyebrow", { y: 20, autoAlpha: 0, duration: .8, ease: "power3.out" }, .2)
      .from(".hero__kicker", { y: 16, autoAlpha: 0, duration: .8, ease: "power3.out" }, .3)

      .from(".hero__lead", { y: 30, autoAlpha: 0, duration: 1, ease: "power3.out" }, .55)
      .from(".hero__ctas .btn", { y: 30, autoAlpha: 0, duration: .9, ease: "power3.out", stagger: .08 }, .65)
      .from(".nav", { y: -40, autoAlpha: 0, duration: 1, ease: "expo.out", clearProps: "transform,opacity,visibility" }, .4)
      .from(".console", { x: 60, autoAlpha: 0, duration: 1.1, ease: "expo.out" }, .7)
      .from(".tag", { scale: 0, autoAlpha: 0, duration: .9, ease: "back.out(2)", stagger: .1 }, .9)
      .from(".hero__scroll", { autoAlpha: 0, duration: .6 }, 1.2)
      .add(() => { if (!RTL) scramble($(".scramble")); }, .25);

    const sparkPath = $(".console__spark path");
    if (sparkPath) {
      const len = sparkPath.getTotalLength();
      gsap.set(sparkPath, { strokeDasharray: len, strokeDashoffset: len });
      intro.to(sparkPath, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" }, 1);
    }

    const loader = $(".loader");
    const count = $(".js-count");
    const counter = { v: 0 };
    let finished = false;
    const finish = () => {
      if (finished) return;
      finished = true;
      if (loader) loader.remove();
      if (!location.hash) { window.scrollTo(0, 0); if (lenis) lenis.scrollTo(0, { immediate: true, force: true }); }
      if (lenis) lenis.start();
      ScrollTrigger.refresh();
    };
    // Full brand preloader only on the first visit of a session (and kept short);
    // returning visitors go straight to the page.
    let seen = false;
    try { seen = sessionStorage.getItem("io2-intro") === "1"; sessionStorage.setItem("io2-intro", "1"); } catch (e) { /* storage blocked */ }
    if (seen) {
      finish();
      intro.timeScale(1.6).play();
    } else {
      const tl = gsap.timeline({ onComplete: finish })
        .to(counter, {
          v: 100, duration: .9, ease: "power2.inOut",
          onUpdate: () => (count.textContent = String(Math.round(counter.v)).padStart(3, "0")),
        }, 0)
        .to(".loader__bar span", { scaleX: 1, duration: .9, ease: "power2.inOut" }, 0)
        .to(".loader__logo", { clipPath: "inset(0 0% 0 0)", duration: .8, ease: "expo.inOut" }, 0)
        .to(".loader__inner", { y: -30, autoAlpha: 0, duration: .35, ease: "power2.in" }, .95)
        .to(loader, { clipPath: "inset(0 0 100% 0)", duration: .7, ease: "expo.inOut" }, 1.1)
        .add(() => intro.play(), 1.2);
      // Safety net: never hold the page hostage (slow device, background tab, throttled frames)
      setTimeout(() => { if (!finished) { tl.kill(); intro.progress(1); finish(); } }, 2600);
    }

    /* ---------- Section headlines ---------- */
    $$("section:not(.hero) .split").forEach((el) => {
      gsap.from(splitWords(el), {
        yPercent: 110, duration: 1, ease: "expo.out", stagger: .06,
        scrollTrigger: { trigger: el, start: "top 88%" },
      });
    });
    $$("section:not(.hero) h2 .slash, .footer__tag .slash").forEach((el) => {
      gsap.from(el, {
        clipPath: "inset(100% 0 0 0)", duration: .9, ease: "expo.out",
        scrollTrigger: { trigger: el, start: "top 90%" },
      });
    });

    /* ---------- Generic reveals ---------- */
    gsap.set(".lead:not(.hero__lead), .eyebrow:not(.hero__eyebrow), .stat, .why li, .faq__list details, .contact__link, .form, .plan, .card, .demo, .market, .agents__wide, .svc, .consult__list li, .consult__card", { y: 40, autoAlpha: 0 });
    ScrollTrigger.batch(".lead:not(.hero__lead), .eyebrow:not(.hero__eyebrow), .stat, .why li, .faq__list details, .contact__link, .form, .plan, .card, .demo, .market, .agents__wide, .svc, .consult__list li, .consult__card", {
      start: "top 90%",
      onEnter: (els) => gsap.to(els, { y: 0, autoAlpha: 1, duration: 1, ease: "expo.out", stagger: .08, overwrite: true }),
    });
    gsap.utils.toArray(".svc").forEach((c, i) => gsap.fromTo(c.querySelector(".svc__icon svg"), { scale: .3, rotate: -40 }, {
      scale: 1, rotate: 0, duration: 1, ease: "back.out(2)", delay: (i % 3) * .08,
      scrollTrigger: { trigger: c, start: "top 88%" },
    }));

    /* ---------- Hero scroll-out parallax ---------- */
    gsap.to(".hero__title", {
      yPercent: -18, ease: "none",
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });
    gsap.to([".hero__bottom", ".console"], {
      y: -60, autoAlpha: 0, ease: "none",
      scrollTrigger: { trigger: ".hero", start: "40% top", end: "bottom top", scrub: true },
    });

    /* ---------- Showcase: cinematic clip reveal + parallax ---------- */
    gsap.fromTo(".showcase__frame",
      { clipPath: "inset(10% 7% 10% 7% round 40px)" },
      { clipPath: "inset(0% 0% 0% 0% round 0px)", ease: "none",
        scrollTrigger: { trigger: ".showcase", start: "top bottom", end: "top 10%", scrub: true } });
    gsap.fromTo(".bgv--showcase .bgv__video", { yPercent: -6 }, {
      yPercent: 6, ease: "none",
      scrollTrigger: { trigger: ".showcase", start: "top bottom", end: "bottom top", scrub: true },
    });
    gsap.from(".showcase__overlay > *", {
      y: 50, autoAlpha: 0, duration: 1.1, ease: "expo.out", stagger: .12,
      scrollTrigger: { trigger: ".showcase__overlay", start: "top 90%" },
    });

    /* ---------- Photo parallax inside frames ---------- */
    $$(".agents__wide img").forEach((img) => {
      gsap.fromTo(img, { yPercent: -5, scale: 1.12 }, {
        yPercent: 5, scale: 1.12, ease: "none",
        scrollTrigger: { trigger: img.parentElement, start: "top bottom", end: "bottom top", scrub: true },
      });
    });

    /* ---------- Manifesto word fill ---------- */
    const words = $$(".reveal-words .w");
    ScrollTrigger.create({
      trigger: ".reveal-words",
      start: "top 80%",
      end: "bottom 45%",
      scrub: true,
      onUpdate: (self) => {
        const n = Math.round(self.progress * words.length);
        words.forEach((w, i) => w.classList.toggle("on", i < n));
      },
    });

    /* ---------- Counters ---------- */
    $$(".counter").forEach((el) => {
      const to = +el.dataset.to;
      const pad = +el.dataset.pad || 1;
      const o = { v: 0 };
      gsap.to(o, {
        v: to, duration: 1.8, ease: "power3.out",
        scrollTrigger: { trigger: el, start: "top 90%" },
        onUpdate: () => (el.textContent = String(Math.round(o.v)).padStart(pad, "0")),
      });
    });

    /* ---------- Marquees (scroll-velocity reactive) ---------- */
    $$(".marquee").forEach((m) => {
      const track = $(".marquee__track", m);
      m.appendChild(track.cloneNode(true)).setAttribute("aria-hidden", "true");
      const dir = m.classList.contains("marquee--rev") ? 1 : -1;
      const tracks = $$(".marquee__track", m);
      const tween = gsap.fromTo(tracks,
        { xPercent: dir === -1 ? 0 : -100 },
        { xPercent: dir === -1 ? -100 : 0, duration: 28 / (+m.dataset.speed || 1), ease: "none", repeat: -1 });
      let boost = { t: 1 };
      ScrollTrigger.create({
        trigger: m, start: "top bottom", end: "bottom top",
        onUpdate: (self) => {
          const v = Math.min(Math.abs(self.getVelocity()) / 400, 5);
          gsap.to(boost, { t: 1 + v, duration: .2, overwrite: true, onUpdate: () => tween.timeScale(boost.t) });
          gsap.to(boost, { t: 1, duration: 1.2, delay: .2, ease: "power2.out", onUpdate: () => tween.timeScale(boost.t) });
        },
      });
    });
    gsap.fromTo(".marquee-band", { rotate: -4 }, {
      rotate: 0, ease: "none",
      scrollTrigger: { trigger: ".marquee-band", start: "top bottom", end: "bottom top", scrub: true },
    });

    /* ---------- System: horizontal pinned journey ---------- */
    const mm = gsap.matchMedia();
    mm.add("(min-width: 681px)", () => {
      const track = $(".system__track");
      const distance = () => track.scrollWidth - window.innerWidth;
      const horiz = gsap.to(track, {
        x: () => -distance(), ease: "none",
        scrollTrigger: {
          trigger: ".system__pin", start: "top top", end: () => "+=" + distance(),
          pin: true, scrub: 1, invalidateOnRefresh: true, anticipatePin: 1,
        },
      });
      gsap.from(".viz-output .bar", {
        scaleY: 0, duration: 1, ease: "expo.out", stagger: .1,
        scrollTrigger: { trigger: ".panel--output", containerAnimation: horiz, start: "left 70%" },
      });
      gsap.from(".viz-output .trend", {
        strokeDasharray: 400, strokeDashoffset: 400, duration: 1.4, ease: "power2.inOut",
        scrollTrigger: { trigger: ".panel--output", containerAnimation: horiz, start: "left 60%" },
      });
      $$(".panel").forEach((p) => {
        gsap.from($(".glyph", p), {
          xPercent: 20, ease: "none",
          scrollTrigger: { trigger: p, containerAnimation: horiz, start: "left right", end: "right left", scrub: true },
        });
      });
    });
    mm.add("(max-width: 680px)", () => {
      gsap.from(".viz-output .bar", {
        scaleY: 0, duration: 1, ease: "expo.out", stagger: .1,
        scrollTrigger: { trigger: ".viz-output", start: "top 85%" },
      });
    });

    /* ---------- Process line + steps ---------- */
    gsap.to(".steps__line span", {
      scaleY: 1, ease: "none",
      scrollTrigger: { trigger: ".steps", start: "top 60%", end: "bottom 60%", scrub: true },
    });
    $$(".step").forEach((s) => {
      ScrollTrigger.create({
        trigger: s, start: "top 60%", end: "bottom 60%",
        onEnter: () => s.classList.add("is-on"),
        onLeaveBack: () => s.classList.remove("is-on"),
      });
    });

    /* ---------- GCC map ---------- */
    const arcs = $$(".arcs path");
    arcs.forEach((p) => {
      const l = p.getTotalLength();
      gsap.set(p, { strokeDasharray: l, strokeDashoffset: l });
    });
    gsap.timeline({ scrollTrigger: { trigger: ".map", start: "top 75%" } })
      .from(".city--hub", { scale: 0, transformOrigin: "center", transformBox: "fill-box", duration: .7, ease: "back.out(2)" })
      .to(arcs, { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut", stagger: .15 }, .2)
      .from(".city:not(.city--hub)", { scale: 0, autoAlpha: 0, transformOrigin: "center", transformBox: "fill-box", duration: .6, ease: "back.out(2.5)", stagger: .15 }, .9);

    /* ---------- Contact headline scale ---------- */
    gsap.from(".contact__title", {
      scale: .92, transformOrigin: "left bottom", ease: "none",
      scrollTrigger: { trigger: ".contact", start: "top bottom", end: "top 30%", scrub: true },
    });

    /* ---------- Agents demo ---------- */
    initDemo();

    window.addEventListener("load", () => ScrollTrigger.refresh());
  };
  (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(startMotion);
  setTimeout(startMotion, 2500);

  /* ======================================================================
     UI that works with or without GSAP
     ====================================================================== */
  function initUI(lenis) {
    const nav = $(".nav");
    const bar = $(".progress span");
    const themed = $$("section[data-theme], footer[data-theme]");
    const links = $$(".nav__links a");
    let lastY = window.scrollY;

    const linkTargets = links.map((a) => document.querySelector(a.getAttribute("href")));
    const onScroll = () => {
      const y = window.scrollY;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
      const menuOpen = root.classList.contains("menu-open");
      nav.classList.toggle("is-hidden", !menuOpen && y > lastY && y > 400);
      lastY = y;

      const probe = 44;
      let theme = "dark";
      for (const s of themed) {
        const r = s.getBoundingClientRect();
        if (r.top <= probe && r.bottom > probe) { theme = s.dataset.theme; break; }
      }
      const lightMode = root.dataset.mode === "light";
      nav.classList.toggle("on-light", lightMode || theme === "light" || theme === "yellow");

      const mid = window.innerHeight * .4;
      links.forEach((a, i) => {
        const t = linkTargets[i];
        if (!t) return;
        const r = t.getBoundingClientRect();
        a.classList.toggle("is-active", r.top <= mid && r.bottom > mid);
      });
    };
    let ticking = false;
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => { ticking = false; onScroll(); });
    }, { passive: true });
    onScroll();

    /* anchors */
    const burger = $(".nav__burger");
    const menu = $("#menu");
    const setMenu = (open) => {
      root.classList.toggle("menu-open", open);
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? T.closeMenu : T.openMenu);
      menu.setAttribute("aria-hidden", String(!open));
      if (lenis) open ? lenis.stop() : lenis.start();
    };
    burger.addEventListener("click", () => setMenu(!root.classList.contains("menu-open")));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });

    $$('a[href^="#"]').forEach((a) => {
      a.addEventListener("click", (e) => {
        const id = a.getAttribute("href");
        const target = id === "#top" ? document.body : document.querySelector(id);
        if (!target) return;
        e.preventDefault();
        setMenu(false);
        if (lenis) lenis.scrollTo(id === "#top" ? 0 : target, { duration: 1.6 });
        else window.scrollTo({ top: id === "#top" ? 0 : target.getBoundingClientRect().top + window.scrollY, behavior: reduce ? "auto" : "smooth" });
      });
    });

    /* dark / light mode */
    const toggle = $(".mode-toggle");
    const metas = $$('meta[name="theme-color"]');
    const applyMode = (mode) => {
      if (mode === "light") root.dataset.mode = "light"; else delete root.dataset.mode;
      const light = mode === "light";
      toggle.setAttribute("aria-pressed", String(light));
      toggle.setAttribute("aria-label", light ? T.toDark : T.toLight);
      metas.forEach((m) => m.setAttribute("content", light ? "#F7F5FF" : "#0B0821"));
      onScroll();
    };
    applyMode(root.dataset.mode === "light" ? "light" : "dark");
    toggle.addEventListener("click", () => {
      const next = root.dataset.mode === "light" ? "dark" : "light";
      try { localStorage.setItem("io2-mode", next); } catch (e) { /* storage unavailable */ }
      applyMode(next);
    });

    /* Calendly booking: inline calendar in the consultation card + popup from every "Free consultation" button */
    initCalendly(setMenu);

    /* service rows accordion */
    const rows = $$(".row");
    rows.forEach((row, i) => {
      const head = $(".row__head", row);
      const id = "row-body-" + i;
      $(".row__body", row).id = id;
      head.setAttribute("aria-controls", id);
      head.addEventListener("click", () => {
        const open = !row.classList.contains("is-open");
        row.classList.toggle("is-open", open);
        head.setAttribute("aria-expanded", String(open));
        if (window.ScrollTrigger) setTimeout(() => window.ScrollTrigger.refresh(), 650);
      });
    });
    if (rows[0]) { rows[0].classList.add("is-open"); $(".row__head", rows[0]).setAttribute("aria-expanded", "true"); }

    /* contact form → email (FormSubmit → contact@io2.agency) */
    const form = $(".form");
    const status = $(".form__status", form);
    const sendBtn = $('button[type="submit"]', form);
    const showStatus = (msg, ok) => { status.hidden = false; status.textContent = msg; status.classList.toggle("is-ok", ok); status.classList.toggle("is-err", !ok); };
    const mark = (input, ok, errId) => {
      input.closest(".field").classList.toggle("invalid", !ok);
      input.setAttribute("aria-invalid", String(!ok));
      input.setAttribute("aria-describedby", errId);
      return ok;
    };
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (form._honey && form._honey.value) return; // bot
      const okName = mark(form.name, !!form.name.value.trim(), "e-name");
      const okEmail = mark(form.email, /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(form.email.value.trim()), "e-email");
      if (!okName) { form.name.focus(); return; }
      if (!okEmail) { form.email.focus(); return; }
      const data = Object.fromEntries(new FormData(form).entries());
      delete data._next;
      sendBtn.disabled = true;
      showStatus(T.sending, true);
      try {
        const res = await fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(data),
        });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || String(out.success) === "false") throw new Error(out.message || res.status);
        trackEvent("generate_lead", { lead_source: "contact_form", lead_goal: data.goal });
        form.reset();
        showStatus(T.sent, true);
      } catch (err) {
        showStatus(T.sendFailed, false);
      } finally {
        sendBtn.disabled = false;
      }
    });
    ["name", "email"].forEach((n) => form[n].addEventListener("input", () => form[n].closest(".field").classList.remove("invalid")));
    // no-JS fallback lands back here with ?sent=1
    if (/[?&]sent=1/.test(location.search)) showStatus(T.sent, true);

    /* free consultation booking → WhatsApp */
    const cf = $(".consult__form");
    if (cf) {
      const check = (input, ok, errId) => {
        input.closest(".field").classList.toggle("invalid", !ok);
        input.setAttribute("aria-invalid", String(!ok));
        input.setAttribute("aria-describedby", errId);
        return ok;
      };
      cf.addEventListener("submit", (e) => {
        e.preventDefault();
        const f = {
          name: cf.name.value.trim(), phone: cf.phone.value.trim(), company: cf.company.value.trim(),
          need: cf.need.value, time: cf.time.value,
        };
        const okName = check(cf.name, !!f.name, "ce-name");
        const okPhone = check(cf.phone, f.phone.replace(/\D/g, "").length >= 8, "ce-phone");
        if (!okName) { cf.name.focus(); return; }
        if (!okPhone) { cf.phone.focus(); return; }
        trackEvent("generate_lead", { lead_source: "consultation_form", lead_goal: f.need });
        window.open("https://wa.me/96877220770?text=" + encodeURIComponent(T.consult(f).filter(Boolean).join("\n")), "_blank", "noopener");
      });
      ["name", "phone"].forEach((n) => cf[n].addEventListener("input", () => cf[n].closest(".field").classList.remove("invalid")));
    }

    if (reduce) return;

    /* card spotlight */
    $$(".spot").forEach((c) => {
      c.addEventListener("pointermove", (e) => {
        const r = c.getBoundingClientRect();
        c.style.setProperty("--mx", e.clientX - r.left + "px");
        c.style.setProperty("--my", e.clientY - r.top + "px");
      });
    });

    if (!finePointer || !window.gsap) return;
    const g = window.gsap;

    /* magnetic buttons */
    $$(".magnetic").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        g.to(el, { x: (e.clientX - r.left - r.width / 2) * .3, y: (e.clientY - r.top - r.height / 2) * .4, duration: .5, ease: "power3.out" });
      });
      el.addEventListener("pointerleave", () => g.to(el, { x: 0, y: 0, duration: .9, ease: "elastic.out(1, .4)" }));
    });

    /* plan tilt */
    $$(".tilt").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - .5;
        const py = (e.clientY - r.top) / r.height - .5;
        g.to(el, { rotateY: px * 8, rotateX: -py * 8, y: -8, duration: .6, ease: "power3.out" });
      });
      el.addEventListener("pointerleave", () => g.to(el, { rotateY: 0, rotateX: 0, y: 0, duration: .8, ease: "power3.out" }));
    });

    /* hero tag parallax */
    const hero = $(".hero");
    const tags = $$(".tag");
    hero.addEventListener("pointermove", (e) => {
      const cx = e.clientX / window.innerWidth - .5;
      const cy = e.clientY / window.innerHeight - .5;
      tags.forEach((t) => g.to(t, { x: cx * 60 * +t.dataset.depth, y: cy * 40 * +t.dataset.depth, duration: 1, ease: "power3.out" }));
      g.to(".console", { x: cx * -18, duration: 1.2, ease: "power3.out" });
    });

    /* custom cursor */
    root.classList.add("has-cursor");
    const cur = $(".cursor");
    const dot = $(".cursor__dot");
    const ring = $(".cursor__ring");
    const label = $(".cursor__label");
    const dx = g.quickSetter(dot, "x", "px"), dy = g.quickSetter(dot, "y", "px");
    const rx = g.quickTo(ring, "x", { duration: .45, ease: "power3.out" });
    const ry = g.quickTo(ring, "y", { duration: .45, ease: "power3.out" });
    g.set([dot, ring], { xPercent: -50, yPercent: -50 });
    window.addEventListener("pointermove", (e) => { dx(e.clientX); dy(e.clientY); rx(e.clientX); ry(e.clientY); });
    document.addEventListener("pointerover", (e) => {
      const t = e.target.closest("a, button, summary, input, select, textarea, [data-cursor]");
      const lab = e.target.closest(".row__head") ? "Open" : "";
      cur.classList.toggle("is-link", !!t && !lab);
      cur.classList.toggle("is-label", !!lab);
      label.textContent = lab;
    });
    document.addEventListener("pointerleave", () => g.to(cur, { autoAlpha: 0, duration: .2 }));
    document.addEventListener("pointerenter", () => g.to(cur, { autoAlpha: 1, duration: .2 }));
  }

  /* ---------- Lazy panel logos in the System section ---------- */
  (function lazyGlyphs() {
    const sys = $(".system");
    if (!sys) return;
    if (!("IntersectionObserver" in window)) { sys.classList.add("glyphs-on"); return; }
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { sys.classList.add("glyphs-on"); io.disconnect(); } }, { rootMargin: "800px 0px" });
    io.observe(sys);
  })();

  /* ---------- Cinematic background videos (lazy, paused off-screen) ---------- */
  function initBgVideos() {
    const vids = $$(".bgv__video");
    const saveData = navigator.connection && navigator.connection.saveData;
    const still = reduce || saveData;
    const setPoster = (v) => { if (v.dataset.poster && !v.poster) v.poster = v.dataset.poster; };
    vids.forEach((v) => {
      v.muted = true;
      if (still) setPoster(v);
      v.addEventListener("loadeddata", () => v.classList.add("is-ready"), { once: true });
      if (still) { v.classList.add("is-ready"); } // poster frame only
    });
    if (still || !("IntersectionObserver" in window)) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(({ target: v, isIntersecting }) => {
        if (isIntersecting) {
          setPoster(v);
          if (!v.src) {
            // phones get the light encode (~220 KB); desktop/iPad the 720p master
            v.src = window.innerWidth < 700 ? v.dataset.src.replace(".mp4", "-sm.mp4") : v.dataset.src;
            v.load();
          }
          const p = v.play(); if (p && p.catch) p.catch(() => v.classList.add("is-ready"));
        } else if (!v.paused) v.pause();
      });
    }, { rootMargin: "300px 0px" });
    // start after the page has finished loading, so videos never compete with first paint
    const observeAll = () => vids.forEach((v) => io.observe(v));
    const later = () => ("requestIdleCallback" in window ? requestIdleCallback(observeAll, { timeout: 2500 }) : setTimeout(observeAll, 1200));
    if (document.readyState === "complete") later(); else window.addEventListener("load", later, { once: true });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) vids.forEach((v) => v.pause());
    });
  }

  /* ---------- Calendly ---------- */
  function initCalendly(setMenu) {
    const meta = document.querySelector('meta[name="io2:calendly"]');
    const base = meta && meta.content.trim();
    if (!base || !/^https:\/\/calendly\.com\//.test(base)) return; // not configured → WhatsApp form stays

    root.classList.add("has-calendly");
    const cal = $(".cal");
    const form = $(".consult__form");
    if (cal) cal.hidden = false;
    if (form) form.hidden = true;

    // brand the widget (colour params apply on paid Calendly plans; harmless otherwise)
    const light = () => root.dataset.mode === "light";
    const url = (date) => {
      const u = new URL(base);
      if (date) { u.searchParams.set("month", date.slice(0, 7)); u.searchParams.set("date", date); }
      u.searchParams.set("hide_gdpr_banner", "1");
      u.searchParams.set("primary_color", "5e2df7");
      if (!light()) { u.searchParams.set("background_color", "140f38"); u.searchParams.set("text_color", "ffffff"); }
      return u.toString();
    };
    const utm = (content) => ({ utmSource: "website", utmMedium: "cta", utmCampaign: "free-consultation", utmContent: content + (RTL ? "-ar" : "-en") });

    let loading = null;
    const load = () => loading || (loading = new Promise((resolve, reject) => {
      const css = document.createElement("link");
      css.rel = "stylesheet"; css.href = "https://assets.calendly.com/assets/external/widget.css";
      document.head.appendChild(css);
      const js = document.createElement("script");
      js.src = "https://assets.calendly.com/assets/external/widget.js"; js.async = true;
      js.onload = () => resolve(window.Calendly);
      js.onerror = reject;
      document.head.appendChild(js);
    }));
    const fallback = () => { if (cal) cal.hidden = true; if (form) form.hidden = false; root.classList.remove("has-calendly"); };

    // branded day picker: the next six days (io2 takes bookings 7 days a week). Picking one opens Calendly on that date.
    const days = $(".cal__days");
    if (days) {
      const loc = RTL ? "ar-OM" : "en-GB";
      const fmt = (d, o) => new Intl.DateTimeFormat(loc, o).format(d);
      const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
      const d = new Date(); d.setHours(12, 0, 0, 0);
      let added = 0;
      while (added < 6) {
        d.setDate(d.getDate() + 1);
        const b = document.createElement("button");
        b.type = "button";
        b.className = "cal__day";
        b.dataset.calendly = "";
        b.dataset.date = iso(d);
        b.innerHTML = `<span class="cal__dow">${fmt(d, { weekday: "short" })}</span><b>${fmt(d, { day: "numeric" })}</b><span class="cal__mon">${fmt(d, { month: "short" })}</span>`;
        b.setAttribute("aria-label", fmt(d, { weekday: "long", day: "numeric", month: "long" }));
        days.appendChild(b);
        added++;
      }
      // warm up the widget script once the card is near, so the popup opens instantly
      const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { io.disconnect(); load().catch(fallback); } }, { rootMargin: "400px 0px" });
      io.observe(days);
    }

    // every [data-calendly] button opens the popup straight away
    $$("[data-calendly]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopImmediatePropagation();
        if (setMenu) setMenu(false);
        const src = btn.classList.contains("nav__cta") ? "nav" : btn.classList.contains("menu__free") ? "mobile-menu" : btn.dataset.date ? "day-picker" : "booking-card";
        load().then((C) => C.initPopupWidget({ url: url(btn.dataset.date), utm: utm(src) })).catch(() => { fallback(); window.location.hash = "consultation"; });
      }, true);
    });

    // confirmation + analytics hook when a meeting is booked
    window.addEventListener("message", (e) => {
      if (e.origin !== "https://calendly.com" || !e.data || e.data.event !== "calendly.event_scheduled") return;
      const done = $(".cal__done");
      if (done) done.hidden = false;
      trackEvent("consultation_booked", { lead_source: "calendly" });
    });
  }

  /* ---------- Text scramble ---------- */
  function scramble(el) {
    if (!el) return;
    const final = el.textContent;
    const chars = "01<>/\\[]{}#*+=io2";
    let frame = 0;
    const total = 32;
    const tick = () => {
      frame++;
      el.textContent = final
        .split("")
        .map((c, i) => (c === " " || i < (frame / total) * final.length ? c : chars[(Math.random() * chars.length) | 0]))
        .join("");
      if (frame < total) requestAnimationFrame(tick);
      else el.textContent = final;
    };
    tick();
  }

  /* ---------- AI agent demo loop ---------- */
  function initDemo() {
    const demo = $(".demo");
    const steps = $$("[data-step]", demo).sort((a, b) => a.dataset.step - b.dataset.step);
    const time = $(".demo__time", demo);
    const delays = [600, 900, 1500, 1500, 1300, 900, 700, 700];
    let timers = [];
    let running = false;
    let start = 0;
    let clock;

    const reset = () => { timers.forEach(clearTimeout); timers = []; steps.forEach((s) => s.classList.remove("show")); };
    const run = () => {
      reset();
      running = true;
      start = performance.now();
      let t = 0;
      steps.forEach((s, i) => {
        t += delays[i] || 800;
        timers.push(setTimeout(() => {
          s.classList.add("show");
          if (s.classList.contains("typing")) timers.push(setTimeout(() => s.classList.remove("show"), 1100));
        }, t));
      });
      timers.push(setTimeout(run, t + 5000));
    };
    const fmt = (ms) => {
      const s = Math.floor(ms / 1000);
      return `00:00:${String(s % 60).padStart(2, "0")}`;
    };
    const io = new IntersectionObserver(([e]) => {
      if (e.isIntersecting && !running) {
        run();
        clock = setInterval(() => (time.textContent = fmt(performance.now() - start)), 250);
      } else if (!e.isIntersecting && running) {
        running = false; reset(); clearInterval(clock);
      }
    }, { threshold: .35 });
    io.observe(demo);
  }

  /* ---------- Hero canvas: input → system → output ×2 ---------- */
  function initHeroCanvas(isStatic) {
    const canvas = $(".hero__canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const hero = $(".hero");
    let w, h, dpr, cx, cy, R;
    let parts = [];
    let visible = true;
    let mouse = { x: -9999, y: -9999 };
    let t0 = performance.now();

    const isLight = () => root.dataset.mode === "light";
    const COLORS = ["#FFE000", "#00E385", "#FFFFFF"];
    const LIGHT_COLORS = ["#5E2DF7", "#00B86B"];

    const spawn = (atStart) => ({
      phase: 0,
      x: atStart ? Math.random() * cx : -20 - Math.random() * 200,
      y0: Math.random() * h,
      y: 0,
      v: .6 + Math.random() * 1.1,
      wob: Math.random() * Math.PI * 2,
      dir: 0, spread: 0, color: "#FFFFFF",
    });

    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = hero.clientWidth; h = hero.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(RTL ? -dpr : dpr, 0, 0, dpr, RTL ? w * dpr : 0, 0);
      const mobile = w < 900;
      cx = mobile ? w * .62 : w * .7;
      cy = mobile ? h * .3 : h * .44;
      R = Math.min(w, h) * (mobile ? .16 : .14);
      // desktop: the "system" ring orbits the hero photo
      const ph = $(".hero__photo");
      if (ph && w >= 1100) {
        const pr = ph.getBoundingClientRect(), hr = hero.getBoundingClientRect();
        cx = pr.left - hr.left + pr.width / 2;
        cy = pr.top - hr.top + pr.height / 2;
        R = pr.width * .78;
      }
      const n = Math.min(Math.round((w * h) / 14000), mobile ? 50 : 110);
      parts = Array.from({ length: n }, () => spawn(true));
    };

    const step = (p, dt) => {
      if (p.phase === 0) {
        p.x += p.v * dt;
        const prog = Math.max(0, Math.min(1, p.x / cx));
        const ease = Math.pow(1 - prog, 1.6);
        p.y = cy + (p.y0 - cy) * ease + Math.sin(p.wob + p.x * .01) * 14 * ease;
        if (p.x >= cx) {
          // pass through the system: split into two amplified outputs
          p.phase = 1; p.dir = 1; p.spread = .25 + Math.random() * .9;
          p.c = (Math.random() * 2) | 0;
          p.v *= 1.6;
          const twin = Object.assign({}, p, { dir: -1, spread: .25 + Math.random() * .9, c: (Math.random() * 2) | 0 });
          parts.push(twin);
          parts.push(spawn(false));
        }
      } else {
        p.x += p.v * dt;
        const q = (p.x - cx) / Math.max(1, w - cx);
        p.y = cy + p.dir * p.spread * Math.pow(q, 1.15) * h * .55;
      }
      // pointer repulsion
      const dx = p.x - mouse.x, dy = p.y - mouse.y;
      const d2 = dx * dx + dy * dy;
      if (d2 < 12000) { const f = (1 - d2 / 12000) * 18; p.y += (dy / Math.sqrt(d2 + .01)) * f; }
      p.x2 = p.x - p.v * 7; p.y2 = p.y;
    };

    const draw = (time) => {
      ctx.clearRect(0, 0, w, h);
      const tt = (time - t0) / 1000;

      // particles
      ctx.lineCap = "round";
      for (let i = parts.length - 1; i >= 0; i--) {
        const p = parts[i];
        if (!isStatic) step(p, 1);
        else if (p.y === 0) { step(p, 0); }
        if (p.phase === 1 && p.x > w + 20) { parts.splice(i, 1); continue; }
        const a = p.phase === 0 ? .25 + .5 * Math.min(1, p.x / cx) : .9;
        const L = isLight();
        ctx.strokeStyle = p.phase === 0 ? (L ? `rgba(59,34,168,${a * .7})` : `rgba(255,255,255,${a})`) : (L ? LIGHT_COLORS : COLORS)[p.c || 0];
        ctx.globalAlpha = p.phase === 0 ? 1 : .85;
        ctx.lineWidth = p.phase === 0 ? 1.4 : 2.2;
        ctx.beginPath();
        ctx.moveTo(p.x2 ?? p.x - 6, p.y2 ?? p.y);
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
      }
      ctx.globalAlpha = 1;

      // system ring (the "o")
      const glow = ctx.createRadialGradient(cx, cy, R * .2, cx, cy, R * 2.2);
      glow.addColorStop(0, isLight() ? "rgba(94,45,247,.16)" : "rgba(94,45,247,.55)");
      glow.addColorStop(1, "rgba(94,45,247,0)");
      ctx.fillStyle = glow;
      ctx.beginPath(); ctx.arc(cx, cy, R * 2.2, 0, Math.PI * 2); ctx.fill();

      ctx.lineWidth = 2;
      ctx.strokeStyle = isLight() ? "rgba(18,12,51,.14)" : "rgba(255,255,255,.18)";
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke();

      ctx.lineWidth = 4;
      ctx.strokeStyle = "#7A55FF";
      ctx.beginPath(); ctx.arc(cx, cy, R, tt * .9, tt * .9 + Math.PI * 1.2); ctx.stroke();

      ctx.lineWidth = 2;
      ctx.strokeStyle = isLight() ? "#3B22A8" : "#FFE000";
      ctx.beginPath(); ctx.arc(cx, cy, R * .72, -tt * 1.4, -tt * 1.4 + Math.PI * .7); ctx.stroke();

      ctx.setLineDash([2, 9]);
      ctx.strokeStyle = isLight() ? "rgba(18,12,51,.3)" : "rgba(255,255,255,.35)";
      ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(cx, cy, R * 1.35, tt * .3, tt * .3 + Math.PI * 2); ctx.stroke();
      ctx.setLineDash([]);

      // orbiting nodes
      [[1.35, .5, "#00E385", 4], [1.35, -.35, "#FF6741", 3.5], [1, 1.1, isLight() ? "#3B22A8" : "#FFFFFF", 3]].forEach(([r, s, c, size]) => {
        const ang = tt * s;
        ctx.fillStyle = c;
        ctx.beginPath(); ctx.arc(cx + Math.cos(ang) * R * r, cy + Math.sin(ang) * R * r, size, 0, Math.PI * 2); ctx.fill();
      });

      if (w >= 1100 && !RTL) {
        ctx.font = "600 11px 'JetBrains Mono', monospace";
        ctx.fillStyle = isLight() ? "rgba(18,12,51,.5)" : "rgba(255,255,255,.5)";
        ctx.textAlign = "center";
        ctx.fillText("INPUT", cx - R * 2.6, cy - R * 1.6);
        ctx.fillStyle = isLight() ? "#5E2DF7" : "rgba(255,224,0,.85)";
        ctx.fillText("OUTPUT ×2", cx + R * 2.6, cy - R * 1.6);
      }
    };

    let raf;
    const loop = (time) => {
      if (visible) draw(time);
      raf = requestAnimationFrame(loop);
    };

    resize();
    window.addEventListener("resize", () => { resize(); if (isStatic) draw(performance.now()); });
    if (isStatic) {
      // warm the system so a static frame shows the full flow
      for (let i = 0; i < 160; i++) { parts.forEach((p) => step(p, 1)); parts = parts.filter((p) => !(p.phase === 1 && p.x > w + 20)); }
      parts.forEach((p) => { p.x2 = p.x - 6; });
      draw(performance.now());
      return;
    }
    // warm-up so the first painted frame already shows input → output
    for (let i = 0; i < 90; i++) { parts.forEach((p) => step(p, 1)); parts = parts.filter((p) => !(p.phase === 1 && p.x > w + 20)); }
    new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(hero);
    hero.addEventListener("pointermove", (e) => {
      const r = hero.getBoundingClientRect();
      mouse.x = RTL ? r.right - e.clientX : e.clientX - r.left; mouse.y = e.clientY - r.top;
    });
    hero.addEventListener("pointerleave", () => (mouse = { x: -9999, y: -9999 }));
    raf = requestAnimationFrame(loop);
  }
})();
