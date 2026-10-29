/* io2: service pages (/services/..., /ar/services/...)
   Lightweight, no GSAP: nav, mobile menu, dark/light mode, Calendly popup, scroll reveal, GA4 events.
   The pages are fully readable without JS. */
(() => {
  "use strict";

  const root = document.documentElement;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => Array.from(c.querySelectorAll(s));
  const RTL = root.dir === "rtl";
  const T = RTL
    ? { openMenu: "فتح القائمة", closeMenu: "إغلاق القائمة", toLight: "التبديل إلى الوضع الفاتح", toDark: "التبديل إلى الوضع الداكن" }
    : { openMenu: "Open menu", closeMenu: "Close menu", toLight: "Switch to light mode", toDark: "Switch to dark mode" };
  const trackEvent = (name, params = {}) => { try { if (typeof window.gtag === "function") window.gtag("event", name, Object.assign({ page_language: RTL ? "ar" : "en" }, params)); } catch (e) {} };
  const page = location.pathname.replace(/^\/(ar\/)?services\/?/, "").replace(/\/$/, "") || "hub";

  $$(".js-year").forEach((el) => { el.textContent = new Date().getFullYear(); });

  /* nav: hide on scroll down, light style over light sections, progress bar */
  const nav = $(".nav");
  const bar = $(".progress span");
  const themed = $$("section[data-theme], footer[data-theme]");
  let lastY = window.scrollY;
  const onScroll = () => {
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    nav.classList.toggle("is-hidden", !root.classList.contains("menu-open") && y > lastY && y > 400);
    lastY = y;
    let theme = "dark";
    for (const s of themed) {
      const r = s.getBoundingClientRect();
      if (r.top <= 44 && r.bottom > 44) { theme = s.dataset.theme; break; }
    }
    nav.classList.toggle("on-light", root.dataset.mode === "light" || theme === "light" || theme === "yellow");
  };
  let ticking = false;
  window.addEventListener("scroll", () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; onScroll(); });
  }, { passive: true });
  onScroll();

  /* mobile menu */
  const burger = $(".nav__burger");
  const menu = $("#menu");
  const setMenu = (open) => {
    root.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? T.closeMenu : T.openMenu);
    menu.setAttribute("aria-hidden", String(!open));
  };
  burger.addEventListener("click", () => setMenu(!root.classList.contains("menu-open")));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(false); });
  $$("#menu a").forEach((a) => a.addEventListener("click", () => setMenu(false)));

  /* dark / light mode (same storage key as the home page) */
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

  /* Calendly popup from every "Free consultation" button; falls back to the home page booking section */
  const meta = $('meta[name="io2:calendly"]');
  const base = meta && meta.content.trim();
  if (base && /^https:\/\/calendly\.com\//.test(base)) {
    const url = () => {
      const u = new URL(base);
      u.searchParams.set("hide_gdpr_banner", "1");
      u.searchParams.set("primary_color", "5e2df7");
      if (root.dataset.mode !== "light") { u.searchParams.set("background_color", "140f38"); u.searchParams.set("text_color", "ffffff"); }
      return u.toString();
    };
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
    $$("[data-calendly]").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        setMenu(false);
        const src = btn.classList.contains("nav__cta") ? "nav" : btn.classList.contains("menu__free") ? "mobile-menu" : btn.dataset.src || "service-" + page;
        load()
          .then((C) => C.initPopupWidget({ url: url(), utm: { utmSource: "website", utmMedium: "cta", utmCampaign: "free-consultation", utmContent: src + (RTL ? "-ar" : "-en") } }))
          .catch(() => { location.href = btn.getAttribute("href"); });
      });
    });
    window.addEventListener("message", (e) => {
      if (e.origin !== "https://calendly.com" || !e.data || e.data.event !== "calendly.event_scheduled") return;
      trackEvent("consultation_booked", { lead_source: "calendly", service_page: page });
    });
  }

  /* WhatsApp clicks from a service page */
  $$('a[href^="https://wa.me/"]').forEach((a) => a.addEventListener("click", () => trackEvent("whatsapp_click", { service_page: page })));

  /* scroll reveal */
  const items = $$(".sp-inc__item, .sp-step, .sp-who__list li, .faq__list details, .svc, .sp-cta__in");
  if (!reduce && "IntersectionObserver" in window) {
    items.forEach((el) => el.classList.add("sp-r"));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach((el) => io.observe(el));
  }
})();
