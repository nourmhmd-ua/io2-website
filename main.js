/* io2 — interactions & motion
   GSAP 3.13 (ScrollTrigger, SplitText) + Lenis smooth scroll.
   Everything degrades to a fully readable static page without JS / with reduced motion. */
(() => {
  "use strict";

  const root = document.documentElement;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const hasGSAP = typeof window.gsap !== "undefined" && typeof window.ScrollTrigger !== "undefined";

  $(".js-year").textContent = new Date().getFullYear();

  /* ---------- Manifesto: split into words (works with or without GSAP) ---------- */
  const highlight = new Set(["growth", "systems:", "multiply.", "io2", "revenue"]);
  $$(".reveal-words").forEach((el) => {
    const words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words
      .map((w) => `<span class="w${highlight.has(w.toLowerCase().replace(/['’]s$/, "")) ? " hl" : ""}">${w}</span>`)
      .join(" ");
  });

  /* ---------- Static fallback ---------- */
  const showStatic = () => {
    const loader = $(".loader");
    if (loader) loader.remove();
    $$(".reveal-words .w").forEach((w) => w.classList.add("on"));
    $$(".demo [data-step]").forEach((s) => { if (!s.classList.contains("typing")) s.classList.add("show"); });
    $$(".counter").forEach((c) => (c.textContent = String(c.dataset.to).padStart(+c.dataset.pad || 1, "0")));
  };

  if (!hasGSAP || reduce) {
    showStatic();
    initUI(null);
    initHeroCanvas(true);
    return;
  }

  const { gsap, ScrollTrigger } = window;
  gsap.registerPlugin(ScrollTrigger);
  if (window.SplitText) gsap.registerPlugin(window.SplitText);

  /* ---------- Smooth scroll ---------- */
  let lenis = null;
  if (window.Lenis) {
    lenis = new window.Lenis({ duration: 1.15, easing: (t) => 1 - Math.pow(1 - t, 4), smoothWheel: true });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    lenis.stop();
  }

  initUI(lenis);
  initHeroCanvas(false);

  /* ---------- Split headlines ---------- */
  const splits = {};
  const canSplit = !!window.SplitText;
  const heroSplits = $$(".hero__title .split");
  if (canSplit) {
    splits.hero = heroSplits.map((el) => new window.SplitText(el, { type: "chars", charsClass: "ch" }));
  }

  /* ---------- Preloader → intro ---------- */
  const intro = gsap.timeline({ paused: true });
  if (canSplit) {
    intro.from(splits.hero.flatMap((s) => s.chars), {
      yPercent: 115, rotate: 8, duration: 1.1, ease: "expo.out", stagger: 0.028,
    }, 0);
  } else {
    intro.from(heroSplits, { yPercent: 110, duration: 1.1, ease: "expo.out", stagger: 0.1 }, 0);
  }
  intro
    .from(".hero__title .slash", { clipPath: "inset(100% 0 0 0)", duration: .8, ease: "expo.out" }, .35)
    .from(".hero__eyebrow", { y: 20, autoAlpha: 0, duration: .8, ease: "power3.out" }, .2)
    .from(".hero__lead", { y: 30, autoAlpha: 0, duration: 1, ease: "power3.out" }, .55)
    .from(".hero__ctas .btn", { y: 30, autoAlpha: 0, duration: .9, ease: "power3.out", stagger: .08 }, .65)
    .from(".nav", { y: -40, autoAlpha: 0, duration: 1, ease: "expo.out", clearProps: "transform,opacity,visibility" }, .4)
    .from(".console", { x: 60, autoAlpha: 0, duration: 1.1, ease: "expo.out" }, .7)
    .from(".tag", { scale: 0, autoAlpha: 0, duration: .9, ease: "back.out(2)", stagger: .1 }, .9)
    .from(".hero__scroll", { autoAlpha: 0, duration: .6 }, 1.2)
    .add(() => scramble($(".scramble")), .25);

  const sparkPath = $(".console__spark path");
  if (sparkPath) {
    const len = sparkPath.getTotalLength();
    gsap.set(sparkPath, { strokeDasharray: len, strokeDashoffset: len });
    intro.to(sparkPath, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" }, 1);
  }

  const loader = $(".loader");
  const count = $(".js-count");
  const counter = { v: 0 };
  gsap.timeline({
    onComplete: () => {
      loader.remove();
      if (lenis) lenis.start();
      ScrollTrigger.refresh();
    },
  })
    .to(counter, {
      v: 100, duration: 1.7, ease: "power2.inOut",
      onUpdate: () => (count.textContent = String(Math.round(counter.v)).padStart(3, "0")),
    }, 0)
    .to(".loader__bar span", { scaleX: 1, duration: 1.7, ease: "power2.inOut" }, 0)
    .to(".loader__logo", { clipPath: "inset(0 0% 0 0)", duration: 1.4, ease: "expo.inOut" }, .1)
    .to(".loader__inner", { y: -30, autoAlpha: 0, duration: .5, ease: "power2.in" }, 1.85)
    .to(loader, { clipPath: "inset(0 0 100% 0)", duration: 1, ease: "expo.inOut" }, 2.1)
    .add(() => intro.play(), 2.35);

  /* ---------- Section headlines ---------- */
  $$("section:not(.hero) .split").forEach((el) => {
    let targets = el;
    if (canSplit) {
      const s = new window.SplitText(el, { type: "words", mask: "words", wordsClass: "w" });
      targets = s.words;
    }
    gsap.from(targets, {
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
  gsap.set(".lead:not(.hero__lead), .eyebrow:not(.hero__eyebrow), .stat, .why li, .faq__list details, .contact__link, .form, .plan, .card, .demo", { y: 40, autoAlpha: 0 });
  ScrollTrigger.batch(".lead:not(.hero__lead), .eyebrow:not(.hero__eyebrow), .stat, .why li, .faq__list details, .contact__link, .form, .plan, .card, .demo", {
    start: "top 90%",
    onEnter: (els) => gsap.to(els, { y: 0, autoAlpha: 1, duration: 1, ease: "expo.out", stagger: .08, overwrite: true }),
  });
  gsap.from(".row", {
    y: 40, autoAlpha: 0, duration: .9, ease: "expo.out", stagger: .07,
    scrollTrigger: { trigger: ".rows", start: "top 85%" },
  });

  /* ---------- Hero scroll-out parallax ---------- */
  gsap.to(".hero__title", {
    yPercent: -18, ease: "none",
    scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
  });
  gsap.to([".hero__bottom", ".console"], {
    y: -60, autoAlpha: 0, ease: "none",
    scrollTrigger: { trigger: ".hero", start: "40% top", end: "bottom top", scrub: true },
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

  /* ======================================================================
     UI that works with or without GSAP
     ====================================================================== */
  function initUI(lenis) {
    const nav = $(".nav");
    const bar = $(".progress span");
    const themed = $$("section[data-theme], footer[data-theme]");
    const links = $$(".nav__links a");
    let lastY = window.scrollY;

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
      nav.classList.toggle("on-light", theme === "light" || theme === "yellow");

      const mid = window.innerHeight * .4;
      links.forEach((a) => {
        const t = document.querySelector(a.getAttribute("href"));
        if (!t) return;
        const r = t.getBoundingClientRect();
        a.classList.toggle("is-active", r.top <= mid && r.bottom > mid);
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    /* anchors */
    const burger = $(".nav__burger");
    const menu = $("#menu");
    const setMenu = (open) => {
      root.classList.toggle("menu-open", open);
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
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

    /* form → WhatsApp */
    const form = $(".form");
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = form.name.value.trim();
      const field = form.name.closest(".field");
      field.classList.toggle("invalid", !name);
      form.name.setAttribute("aria-invalid", String(!name));
      form.name.setAttribute("aria-describedby", "e-name");
      if (!name) { form.name.focus(); return; }
      const lines = [
        `Hi io2, I'm ${name}${form.company.value.trim() ? " from " + form.company.value.trim() : ""}.`,
        `Main goal: ${form.goal.value}.`,
        form.message.value.trim(),
      ].filter(Boolean);
      window.open("https://wa.me/96877220770?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    });
    form.name.addEventListener("input", () => form.name.closest(".field").classList.remove("invalid"));

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

    const COLORS = ["#FFE000", "#00E385", "#FFFFFF"];

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
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const mobile = w < 900;
      cx = mobile ? w * .62 : w * .7;
      cy = mobile ? h * .3 : h * .44;
      R = Math.min(w, h) * (mobile ? .16 : .14);
      const n = Math.min(Math.round((w * h) / 11000), mobile ? 70 : 150);
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
          p.color = COLORS[(Math.random() * 2) | 0];
          p.v *= 1.6;
          const twin = Object.assign({}, p, { dir: -1, spread: .25 + Math.random() * .9, color: COLORS[(Math.random() * 2) | 0] });
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
        ctx.strokeStyle = p.phase === 0 ? `rgba(255,255,255,${a})` : p.color;
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
      glow.addColorStop(0, "rgba(94,45,247,.55)");
      glow.addColorStop(1, "rgba(94,45,247,0)");
      ctx.fillStyle = glow;
      ctx.beginPath(); ctx.arc(cx, cy, R * 2.2, 0, Math.PI * 2); ctx.fill();

      ctx.lineWidth = 2;
      ctx.strokeStyle = "rgba(255,255,255,.18)";
      ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke();

      ctx.lineWidth = 4;
      ctx.strokeStyle = "#7A55FF";
      ctx.beginPath(); ctx.arc(cx, cy, R, tt * .9, tt * .9 + Math.PI * 1.2); ctx.stroke();

      ctx.lineWidth = 2;
      ctx.strokeStyle = "#FFE000";
      ctx.beginPath(); ctx.arc(cx, cy, R * .72, -tt * 1.4, -tt * 1.4 + Math.PI * .7); ctx.stroke();

      ctx.setLineDash([2, 9]);
      ctx.strokeStyle = "rgba(255,255,255,.35)";
      ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(cx, cy, R * 1.35, tt * .3, tt * .3 + Math.PI * 2); ctx.stroke();
      ctx.setLineDash([]);

      // orbiting nodes
      [[1.35, .5, "#00E385", 4], [1.35, -.35, "#FF6741", 3.5], [1, 1.1, "#FFFFFF", 3]].forEach(([r, s, c, size]) => {
        const ang = tt * s;
        ctx.fillStyle = c;
        ctx.beginPath(); ctx.arc(cx + Math.cos(ang) * R * r, cy + Math.sin(ang) * R * r, size, 0, Math.PI * 2); ctx.fill();
      });

      ctx.font = "600 11px 'JetBrains Mono', monospace";
      ctx.fillStyle = "rgba(255,255,255,.5)";
      ctx.textAlign = "center";
      ctx.fillText("INPUT", cx - R * 2.6, cy - R * 1.6);
      ctx.fillStyle = "rgba(255,224,0,.85)";
      ctx.fillText("OUTPUT ×2", cx + R * 2.6, cy - R * 1.6);
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
      for (let i = 0; i < 600; i++) { parts.forEach((p) => step(p, 1)); parts = parts.filter((p) => !(p.phase === 1 && p.x > w + 20)); }
      parts.forEach((p) => { p.x2 = p.x - 6; });
      draw(performance.now());
      return;
    }
    // warm-up so the first painted frame already shows input → output
    for (let i = 0; i < 400; i++) { parts.forEach((p) => step(p, 1)); parts = parts.filter((p) => !(p.phase === 1 && p.x > w + 20)); }
    new IntersectionObserver(([e]) => (visible = e.isIntersecting)).observe(hero);
    hero.addEventListener("pointermove", (e) => {
      const r = hero.getBoundingClientRect();
      mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    });
    hero.addEventListener("pointerleave", () => (mouse = { x: -9999, y: -9999 }));
    raf = requestAnimationFrame(loop);
  }
})();
