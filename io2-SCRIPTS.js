/* IO2 Agency — interaction layer
   Progressive enhancement: the page is fully readable and usable without any of this. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  var deskQ   = window.matchMedia('(min-width: 901px)');
  var raf     = window.requestAnimationFrame || function (f) { return setTimeout(f, 16); };

  /* ---------------- nav ---------------- */
  var nav = document.getElementById('nav');
  var onScrollNav = function () { nav.classList.toggle('is-stuck', window.scrollY > 24); };
  window.addEventListener('scroll', onScrollNav, { passive: true });
  onScrollNav();

  var burger = document.getElementById('burger');
  var drawer = document.getElementById('drawer');
  function setDrawer(open) {
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    drawer.classList.toggle('is-open', open);
    document.documentElement.style.overflow = open ? 'hidden' : '';
  }
  burger.addEventListener('click', function () {
    setDrawer(burger.getAttribute('aria-expanded') !== 'true');
  });
  drawer.addEventListener('click', function (e) { if (e.target.tagName === 'A') setDrawer(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDrawer(false); });

  /* ---------------- marquee ---------------- */
  var mq = document.getElementById('marquee');
  if (mq) mq.innerHTML += mq.innerHTML;

  /* ---------------- reveal on scroll ---------------- */
  var revealables = [].slice.call(document.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !reduced.matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealables.forEach(function (el, i) {
      el.style.transitionDelay = (i % 3) * 85 + 'ms';
      io.observe(el);
    });
  } else {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------------- film grain ---------------- */
  (function grain() {
    var c = document.getElementById('grain');
    if (!c) return;
    if (reduced.matches) { c.remove(); return; }
    var ctx = c.getContext('2d'), T = 140;
    var tile = document.createElement('canvas'); tile.width = tile.height = T;
    var tctx = tile.getContext('2d');
    var img = tctx.createImageData(T, T), d = img.data;
    for (var i = 0; i < d.length; i += 4) {
      var v = (Math.random() * 255) | 0;
      d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 9;
    }
    tctx.putImageData(img, 0, 0);
    function paint() {
      c.width = window.innerWidth; c.height = window.innerHeight;
      var p = ctx.createPattern(tile, 'repeat');
      ctx.fillStyle = p; ctx.fillRect(0, 0, c.width, c.height);
    }
    paint();
    var t; window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(paint, 220); });
  })();

  /* ---------------- the 8-scene story ---------------- */
  var source = document.getElementById('storySource');
  var track  = document.getElementById('storyTrack');
  if (!source || !track) return;

  var cards = [].slice.call(source.querySelectorAll('.mscene'));
  var GLOWS = cards.map(function (c) { return c.getAttribute('data-glow') || '#5E2DF7'; });
  var N = cards.length;
  var built = false, current = -1;
  var wash, media, copy, hudNo, hudRail, scenes = [], plates = [];

  function build() {
    if (built) return;
    track.innerHTML =
      '<div class="stage">' +
        '<div class="stage-wash" id="stageWash" aria-hidden="true"></div>' +
        '<div class="stage-inner">' +
          '<div class="scene-copy" id="sceneCopy"></div>' +
          '<div class="stage-media" id="stageMedia"></div>' +
        '</div>' +
        '<div class="hud" aria-hidden="true">' +
          '<p class="hud-no"><b id="hudNo">01</b> / 0' + N + '</p>' +
          '<div class="hud-rail"><i id="hudRail"></i></div>' +
          '<p class="hud-hint">Scroll</p>' +
        '</div>' +
      '</div>';
    wash    = track.querySelector('#stageWash');
    copy    = track.querySelector('#sceneCopy');
    media   = track.querySelector('#stageMedia');
    hudNo   = track.querySelector('#hudNo');
    hudRail = track.querySelector('#hudRail');
    scenes = []; plates = [];

    cards.forEach(function (card) {
      var body  = card.querySelector('.scene-body');
      var plate = card.querySelector('.viz');
      if (body)  { body.classList.add('scene');  copy.appendChild(body);   scenes.push(body); }
      if (plate) { media.appendChild(plate); plates.push(plate); }
    });
    track.style.height = (N * 100) + 'vh';
    document.body.classList.add('is-pinned');
    built = true;
    current = -1;
    activate(0);
    onScrollStory();
  }

  function teardown() {
    if (!built) return;
    cards.forEach(function (card, i) {
      if (scenes[i]) { scenes[i].classList.remove('scene', 'is-on'); card.appendChild(scenes[i]); }
      if (plates[i]) { plates[i].classList.remove('is-on'); card.insertBefore(plates[i], card.firstChild); }
    });
    track.innerHTML = '';
    document.body.classList.remove('is-pinned');
    built = false; current = -1;
  }

  function activate(i) {
    if (i === current || !built) return;
    current = i;
    for (var k = 0; k < scenes.length; k++) scenes[k].classList.toggle('is-on', k === i);
    for (var j = 0; j < plates.length; j++) plates[j].classList.toggle('is-on', j === i);
    hudNo.textContent = ('0' + (i + 1)).slice(-2);
    var g = GLOWS[i];
    wash.style.setProperty('--glow', g);
    if (plates[i]) plates[i].style.setProperty('--glow', g);
  }

  var ticking = false;
  function onScrollStory() {
    if (!built || ticking) return;
    ticking = true;
    raf(function () {
      ticking = false;
      var r = track.getBoundingClientRect();
      var span = r.height - window.innerHeight;
      if (span <= 0) return;
      var p = Math.min(Math.max(-r.top / span, 0), 1);
      hudRail.style.width = (p * 100).toFixed(2) + '%';
      activate(Math.min(Math.floor(p * N), N - 1));
    });
  }
  window.addEventListener('scroll', onScrollStory, { passive: true });
  window.addEventListener('resize', onScrollStory);

  function sync() {
    if (deskQ.matches && !reduced.matches) build(); else teardown();
  }
  (deskQ.addEventListener ? deskQ.addEventListener('change', sync) : deskQ.addListener(sync));
  (reduced.addEventListener ? reduced.addEventListener('change', sync) : reduced.addListener(sync));
  sync();
})();
