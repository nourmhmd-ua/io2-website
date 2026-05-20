/* ══ CURSOR ══ */
const cur=document.getElementById('cur'),curR=document.getElementById('cur-r');
let mx=0,my=0,rx=0,ry=0;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;});
(function t(){
  cur.style.left=mx+'px';cur.style.top=my+'px';
  rx+=(mx-rx)*.1;ry+=(my-ry)*.1;
  curR.style.left=rx+'px';curR.style.top=ry+'px';
  requestAnimationFrame(t);
})();

/* ══ PROGRESS + NAV ══ */
const barEl=document.getElementById('bar'),navEl=document.getElementById('nav');
window.addEventListener('scroll',()=>{
  barEl.style.width=(window.scrollY/(document.body.scrollHeight-window.innerHeight)*100)+'%';
  navEl.classList.toggle('solid',window.scrollY>60);
},{passive:true});

/* ══ HERO WORDS ══ */
document.querySelectorAll('.hl-w').forEach(w=>{
  setTimeout(()=>w.classList.add('in'),350+parseInt(w.dataset.d||0));
});

/* ══ SCROLL MORPH DATA ══ */
const MKT_SVGS = [
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M22 12h-4l-3 9L9 3l-3 9H2" stroke="#FFE000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><circle cx="11" cy="11" r="8" stroke="#00E385" stroke-width="1.5"/><path d="m21 21-4.35-4.35" stroke="#00E385" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" stroke="#FF6741" stroke-width="1.5"/><polyline points="22,6 12,13 2,6" stroke="#FF6741" stroke-width="1.5"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="#b39dff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><rect x="3" y="3" width="18" height="18" rx="2" stroke="#FFE000" stroke-width="1.5"/><path d="M3 9h18M9 21V9" stroke="#FFE000" stroke-width="1.5"/></svg>`
];
const MKT_DATA=[
  {bg:'#0d0820',sn:'10×',sl:'Avg engagement growth'},
  {bg:'#041420',sn:'3×',sl:'ROI on ad spend'},
  {bg:'#0a1808',sn:'45%',sl:'Email open rate avg'},
  {bg:'#150820',sn:'100%',sl:'Brand consistency'},
  {bg:'#0a0a1a',sn:'99%',sl:'Site uptime'},
];
const AI_SVGS = [
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="#FFE000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 014.68 11.9a19.79 19.79 0 01-3.07-8.67A2 2 0 013.59 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L7.91 8.56a16 16 0 006.53 6.53l.62-.62a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z" stroke="#00E385" stroke-width="1.5"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18" stroke="#FF6741" stroke-width="1.5"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" stroke="#b39dff" stroke-width="1.5"/><circle cx="9" cy="10" r="1" fill="#b39dff"/><circle cx="12" cy="10" r="1" fill="#b39dff"/><circle cx="15" cy="10" r="1" fill="#b39dff"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M9 3H5a2 2 0 00-2 2v4m6-6h10a2 2 0 012 2v4M9 3v18m0 0h10a2 2 0 002-2V9M9 21H5a2 2 0 01-2-2V9m0 0h18" stroke="#FFE000" stroke-width="1.5"/><path d="M12 8v4l3 3" stroke="#FFE000" stroke-width="1.5" stroke-linecap="round"/></svg>`,
  `<svg width="72" height="72" viewBox="0 0 24 24" fill="none"><path d="M12 2a3 3 0 013 3v7a3 3 0 01-6 0V5a3 3 0 013-3z" stroke="#00E385" stroke-width="1.5"/><path d="M19 10v2a7 7 0 01-14 0v-2M12 19v3M8 22h8" stroke="#00E385" stroke-width="1.5" stroke-linecap="round"/></svg>`
];
const AI_DATA=[
  {bg:'#0d0418',sn:'24/7',sl:'Always-on availability'},
  {bg:'#051520',sn:'∞',sl:'Calls handled per day'},
  {bg:'#14040a',sn:'100%',sl:'Accurate guidance'},
  {bg:'#06061a',sn:'<1s',sl:'Avg response time'},
  {bg:'#040c18',sn:'0',sl:'Manual CRM updates needed'},
  {bg:'#031410',sn:'99%',sl:'Transcription accuracy'},
];

/* ══ MORPH ENGINE ══ */
function buildMorph(pinId, visId, bgnId, svgId, snId, slId, progId, dotsId, blockClass, DATA, SVGS){
  const pin=document.getElementById(pinId);
  const vis=document.getElementById(visId);
  const bgn=document.getElementById(bgnId);
  const svgEl=document.getElementById(svgId);
  const snEl=document.getElementById(snId);
  const slEl=document.getElementById(slId);
  const progEl=document.getElementById(progId);
  const dotEls=document.querySelectorAll('#'+dotsId+' .vis-dot');
  const blocks=document.querySelectorAll('.'+blockClass);
  let last=-1;

  function set(idx, p){
    progEl.style.height=(p*100)+'%';
    if(idx===last)return;
    last=idx;
    const d=DATA[idx];
    vis.style.background=d.bg;
    bgn.textContent=String(idx+1).padStart(2,'0');
    svgEl.innerHTML=SVGS[idx];
    snEl.textContent=d.sn;
    slEl.textContent=d.sl;
    dotEls.forEach((dot,i)=>dot.classList.toggle('on',i===idx));
    blocks.forEach((bl,i)=>{
      bl.classList.remove('active','above');
      if(i===idx)bl.classList.add('active');
      else if(i<idx)bl.classList.add('above');
    });
    /* update corner label */
    const lbl=vis.querySelector('.vis-corner-label');
    if(lbl) lbl.textContent=(idx+1).toString().padStart(2,'0')+' / '+DATA.length;
    /* show robot only on step 0 of AI section */
    const robotScene = document.getElementById('robot-scene');
    if(robotScene){
      if(idx === 0){ robotScene.classList.add('visible'); }
      else { robotScene.classList.remove('visible'); }
    }
    /* activate vis lines */
    vis.classList.remove('active');
    void vis.offsetWidth;
    vis.classList.add('active');
  }

  return ()=>{
    const r=pin.getBoundingClientRect();
    if(r.top<0&&r.bottom>window.innerHeight){
      const p=Math.max(0,Math.min(1,-r.top/(pin.offsetHeight-window.innerHeight)));
      set(Math.min(DATA.length-1,Math.floor(p*DATA.length)), p);
    }
  };
}

const updateMkt=buildMorph('pin-mkt','mkt-vis','mkt-bgn','mkt-svg','mkt-sn','mkt-sl','mkt-prog','mkt-dots','svc-block',MKT_DATA,MKT_SVGS);

const updateAi=buildMorph('pin-ai','ai-vis','ai-bgn','ai-svg','ai-sn','ai-sl','ai-prog','ai-dots','ai-block',AI_DATA,AI_SVGS);


/* ══ INTERSECTION OBSERVER (reveal) ══ */
const io=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in');});
},{threshold:.1});
document.querySelectorAll('.reveal,.reveal-l,.reveal-r,.why-card,.testi-card,.pkg-card').forEach(el=>io.observe(el));

/* ══ COUNT UP ══ */
const co=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(!e.isIntersecting)return;
    const el=e.target,t=parseInt(el.dataset.target),s=el.dataset.suffix||'';
    if(!t)return;
    let v=0;
    const ti=setInterval(()=>{
      v+=t/80;if(v>=t){v=t;clearInterval(ti);}
      el.textContent=Math.floor(v)+s;
    },14);
    co.unobserve(el);
  });
},{threshold:.5});
document.querySelectorAll('[data-target]').forEach(el=>co.observe(el));

/* ══ MAIN SCROLL ══ */
window.addEventListener('scroll',()=>{
  if(!isMobile()){ updateMkt(); updateAi(); }
  /* hero orb parallax */
  const h=document.getElementById('hero').getBoundingClientRect();
  if(h.bottom>0){
    const p=-h.top/window.innerHeight;
    document.getElementById('orb1').style.transform=`translate(${p*30}px,${p*-40}px)`;
    document.getElementById('orb2').style.transform=`translate(${p*-20}px,${p*30}px)`;
  }
},{passive:true});

/* ── MOBILE MENU ── */
const mobBtn    = document.getElementById('mob-btn');
const mobDrawer = document.getElementById('mob-drawer');
const mobClose  = document.getElementById('mob-close');
const mobLinks  = document.querySelectorAll('.mob-link');

function openMenu(){ mobDrawer.classList.add('open'); document.body.style.overflow='hidden'; }
function closeMenu(){ mobDrawer.classList.remove('open'); document.body.style.overflow=''; }

if(mobBtn)    mobBtn.addEventListener('click', openMenu);
if(mobClose)  mobClose.addEventListener('click', closeMenu);
mobLinks.forEach(l => l.addEventListener('click', closeMenu));

/* ── DISABLE SCROLL MORPH ON MOBILE (handled by static CSS) ── */
const isMobile = () => window.innerWidth <= 768;

/* Init first SVGs */
document.getElementById('mkt-svg').innerHTML = MKT_SVGS[0];
/* AI slide 01 starts with robot — no SVG needed until slide 2 */
document.getElementById('ai-svg').innerHTML = AI_SVGS[1];
/* Make sure robot is visible, network hidden on load */