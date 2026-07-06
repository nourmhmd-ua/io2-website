(function(){
'use strict';
var SCENES = 8;
var GLOWS = ['#5E2DF7','#FF6741','#4D9FFF','#5E2DF7','#00E385','#4D9FFF','#FFE000','#5E2DF7'];
var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var mobile = window.matchMedia('(max-width: 760px)').matches;
var stacked = reduced || mobile;

var nav = document.getElementById('nav');
addEventListener('scroll', function(){ nav.classList.toggle('scrolled', scrollY > 40); }, {passive:true});

var burger = document.getElementById('burger'), menu = document.getElementById('mobileMenu');
burger.addEventListener('click', function(){
  var open = burger.classList.toggle('open');
  menu.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', open);
});
menu.querySelectorAll('a').forEach(function(a){
  a.addEventListener('click', function(){ burger.classList.remove('open'); menu.classList.remove('open'); });
});

var texts = [].slice.call(document.querySelectorAll('.scene-text'));
var imgs  = [].slice.call(document.querySelectorAll('.scene-img'));
var track = document.getElementById('storyTrack');
var stageBg = document.getElementById('stageBg');
var hudNum = document.getElementById('hudNum');
var hudBar = document.getElementById('hudBar');

function setGlow(i){
  stageBg.style.setProperty('--glow', GLOWS[i]);
  var vis = document.getElementById('sceneVisual');
  if (vis) vis.style.setProperty('--glow', GLOWS[i]);
}

if (stacked) {
  document.body.classList.add('story-stacked');
  // move each robot image inside its matching text block for stacked flow
  texts.forEach(function(t){
    var i = +t.dataset.scene;
    var img = imgs[i];
    if (img) {
      img.className = 'm-scene-img';
      img.removeAttribute('data-scene');
      t.appendChild(img);
    }
  });
} else {
  var current = -1;
  function activate(i){
    if (i === current) return;
    current = i;
    texts.forEach(function(t,k){ t.classList.toggle('active', k===i); });
    imgs.forEach(function(m,k){ m.classList.toggle('active', k===i); });
    hudNum.textContent = ('0'+(i+1)).slice(-2);
    setGlow(i);
  }
  function onScroll(){
    var r = track.getBoundingClientRect();
    var total = r.height - innerHeight;
    var p = Math.min(Math.max(-r.top / total, 0), 1);
    hudBar.style.width = (p*100) + '%';
    activate(Math.min(Math.floor(p * SCENES), SCENES-1));
  }
  addEventListener('scroll', onScroll, {passive:true});
  addEventListener('resize', onScroll);
  activate(0);
  onScroll();
}

// reveal on scroll
var io = new IntersectionObserver(function(es){
  es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
},{threshold:.12});
document.querySelectorAll('.rv').forEach(function(el,i){
  el.style.transitionDelay = (i%3)*90 + 'ms';
  io.observe(el);
});

// particles
if (!reduced) {
  var cv = document.getElementById('stars'), ctx = cv.getContext('2d'), P = [];
  function size(){ cv.width = innerWidth; cv.height = innerHeight; }
  size(); addEventListener('resize', size);
  for (var i=0;i<55;i++) P.push({x:Math.random(),y:Math.random(),z:Math.random()*.7+.3,s:Math.random()*.25+.05});
  (function tick(){
    ctx.clearRect(0,0,cv.width,cv.height);
    for (var i=0;i<P.length;i++){
      var p = P[i];
      p.y -= p.s/1000; if (p.y < 0) { p.y = 1; p.x = Math.random(); }
      ctx.globalAlpha = p.z * .8;
      ctx.fillStyle = i%9===0 ? '#FFE000' : '#8F7BFF';
      ctx.fillRect(p.x*cv.width, p.y*cv.height, p.z*1.8, p.z*1.8);
    }
    requestAnimationFrame(tick);
  })();
} else {
  var c = document.getElementById('stars'); if (c) c.remove();
}
})();
