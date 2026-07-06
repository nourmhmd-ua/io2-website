// duplicate marquee content for seamless loop
const mq=document.getElementById('marquee');
mq.innerHTML+=mq.innerHTML;

// nav scroll state
const nav=document.getElementById('nav');
addEventListener('scroll',()=>{nav.classList.toggle('scrolled',scrollY>40)},{passive:true});

// mobile menu
const burger=document.getElementById('burger'),menu=document.getElementById('mobileMenu');
burger.addEventListener('click',()=>{burger.classList.toggle('open');menu.classList.toggle('open')});
menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{burger.classList.remove('open');menu.classList.remove('open')}));

// reveal on scroll (staggered)
const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
document.querySelectorAll('.rv').forEach((el,i)=>{el.style.transitionDelay=(i%3)*90+'ms';io.observe(el)});

// animated counters
const cio=new IntersectionObserver(es=>{es.forEach(e=>{
  if(!e.isIntersecting)return;
  const el=e.target,to=+el.dataset.to,t0=performance.now(),dur=1400;
  const tick=n=>{const p=Math.min((n-t0)/dur,1);el.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(tick)};
  requestAnimationFrame(tick);cio.unobserve(el);
})},{threshold:.6});
document.querySelectorAll('.count').forEach(el=>cio.observe(el));
