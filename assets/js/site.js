/* MH Event — interactions */
(function(){
  "use strict";
  var doc=document.documentElement;
  var RM=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(RM) doc.classList.add("rm");
  var M=window.Motion||null;
  var EASE=[0.23,1,0.32,1];
  var L=window.MH_LOTTIE||{};
  function $(s,c){return (c||document).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))}
  function store(k,v){try{if(v===undefined)return sessionStorage.getItem(k);sessionStorage.setItem(k,v)}catch(e){return null}}
  function lottie(el,name,opts){
    if(!window.lottie||!L[name]||!el) return null;
    return window.lottie.loadAnimation(Object.assign({container:el,renderer:"svg",loop:false,autoplay:true,animationData:JSON.parse(JSON.stringify(L[name]))},opts||{}));
  }
  window.MH={lottie:lottie};

  /* ---------- Split text into lines (Motion) ---------- */
  function splitLines(el){
    if(el.dataset.split==="done") return [];
    var words=[];
    (function walk(node){
      Array.prototype.slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          n.textContent.split(/(\s+)/).forEach(function(w){ if(w.trim()) words.push({t:w}); else if(w) words.push({space:true}); });
        } else if(n.nodeType===1){
          if(n.tagName==="BR"){ words.push({br:true}); return; }
          var tag=n.tagName.toLowerCase();
          n.textContent.split(/(\s+)/).forEach(function(w){ if(w.trim()) words.push({t:w,tag:tag}); else if(w) words.push({space:true}); });
        }
      });
    })(el);
    el.innerHTML="";
    var spans=[],sp=false;
    words.forEach(function(w){
      if(w.br){el.appendChild(document.createElement("br"));sp=true;return}
      if(w.space){el.appendChild(document.createTextNode(" "));sp=true;return}
      var s=document.createElement("span"); s.style.display="inline-block"; s._sp=sp; sp=false;
      if(w.tag){var t=document.createElement(w.tag);t.textContent=w.t;s.appendChild(t)}else s.textContent=w.t;
      el.appendChild(s); spans.push(s);
    });
    // group by offsetTop into lines
    var lines=[],cur=null,top=null;
    spans.forEach(function(s){ if(top===null||Math.abs(s.offsetTop-top)>4){cur=[];lines.push(cur);top=s.offsetTop} cur.push(s) });
    el.innerHTML="";
    var inner=[];
    lines.forEach(function(line,i){
      var ln=document.createElement("span");ln.className="ln";
      var inn=document.createElement("span");
      line.forEach(function(s,j){ if(j>0&&s._sp) inn.appendChild(document.createTextNode(" ")); inn.appendChild(s.firstChild&&s.firstChild.nodeType===1?s.firstChild:document.createTextNode(s.textContent)) });
      ln.appendChild(inn); el.appendChild(ln); inner.push(inn);
    });
    el.dataset.split="done"; el.classList.add("split");
    return inner;
  }
  function animateSplit(el,delay){
    if(!M||RM){return}
    var lines=splitLines(el);
    lines.forEach(function(l){l.style.transform="translateY(105%)";l.style.filter="blur(6px)"});
    M.animate(lines,{transform:["translateY(105%)","translateY(0%)"],filter:["blur(6px)","blur(0px)"]},{duration:1.05,delay:M.stagger(0.09,{startDelay:delay||0}),easing:EASE});
  }

  /* ---------- Curtain (opening) ---------- */
  var curtain=$(".curtain");
  function heroIn(d){
    $$("[data-hero-split]").forEach(function(h){animateSplit(h,d)});
    if(M&&!RM){
      var hm=$(".hero-media img"); if(hm) M.animate(hm,{transform:["scale(1.14)","scale(1)"]},{duration:2.4,easing:EASE});
      M.animate($$(".hero [data-hero-fade]"),{opacity:[0,1],transform:["translateY(14px)","translateY(0)"]},{duration:.9,delay:M.stagger(.08,{startDelay:(d||0)+.45}),easing:EASE});
    } else $$(".hero [data-hero-fade]").forEach(function(e){e.style.opacity=1});
  }
  if(curtain){
    var seen=store("mh-open");
    if(seen||RM||!M){ curtain.remove(); heroIn(0.1); }
    else{
      store("mh-open","1");
      document.body.style.overflow="hidden";
      var anim=lottie($(".curtain-lottie"),"arcade",{rendererSettings:{preserveAspectRatio:"xMidYMid meet"}});
      M.animate(".curtain-mark",{opacity:[0,1],transform:["translateY(8px)","translateY(0)"]},{duration:.9,delay:.55,easing:EASE});
      var closed=false;
      var close=function(){
        if(closed) return; closed=true;
        document.body.style.overflow="";
        M.animate(curtain,{clipPath:["inset(0 0 0 0 round 0px)","inset(0 0 100% 0 round 0px)"]},{duration:1,easing:[0.77,0,0.175,1]}).finished.then(function(){curtain.remove()});
        heroIn(0.35);
      };
      setTimeout(close,2300);
      curtain.addEventListener("click",close);
      document.addEventListener("keydown",close,{once:true});
    }
  } else heroIn(0.05);

  /* ---------- Scroll reveals ---------- */
  if(M&&!RM){
    $$("[data-split]").forEach(function(el){ if(el.hasAttribute("data-hero-split")) return; M.inView(el,function(){animateSplit(el,0)},{margin:"0px 0px -12% 0px"}) });
    // pre-hide split headings to avoid flash
    $$("[data-fade]").forEach(function(el){
      M.inView(el,function(){ M.animate(el,{opacity:[0,1],transform:["translateY(18px)","translateY(0)"]},{duration:.9,delay:(+el.dataset.fade||0),easing:EASE}) },{margin:"0px 0px -10% 0px"});
    });
    $$(".reveal-img").forEach(function(el){
      M.inView(el,function(){ M.animate(el,{clipPath:["inset(0% 0% 100% 0%)","inset(0% 0% 0% 0%)"]},{duration:1.4,easing:EASE}); var im=el.querySelector("img"); if(im) M.animate(im,{transform:["scale(1.18)","scale(1)"]},{duration:1.6,easing:EASE}) },{margin:"0px 0px -15% 0px"});
    });
    $$(".rule").forEach(function(r){ r.classList.add("is-pending"); M.inView(r,function(){ r.classList.remove("is-pending") }) });
    $$(".band>.bg").forEach(function(bg){ M.scroll(M.animate(bg,{transform:["translateY(-4%)","translateY(4%)"]},{easing:"linear"}),{target:bg.parentElement,offset:["start end","end start"]}) });
    $$("[data-cypress]").forEach(function(el){ M.inView(el,function(){ lottie(el,"cypress") }) });
    $$(".mosaic").forEach(function(mo){ var sh=$$(".mo-shape",mo); sh.forEach(function(x){x.style.opacity=0});
      M.inView(mo,function(){ M.animate(sh,{opacity:[0,1],transform:["scale(.92)","scale(1)"],filter:["blur(8px)","blur(0px)"]},{duration:.9,delay:M.stagger(.09),easing:EASE}).finished.then(function(){sh.forEach(function(x){x.style.transform="";x.style.filter=""})}) },{margin:"0px 0px -15% 0px"}) });
  } else {
    $$("[data-fade]").forEach(function(e){e.style.opacity=1;e.style.transform="none"});
    $$("[data-cypress]").forEach(function(el){ var a=lottie(el,"cypress",{autoplay:false}); if(a) a.addEventListener("DOMLoaded",function(){a.goToAndStop(a.totalFrames-1,true)}) });
  }

  /* ---------- Header behaviour ---------- */
  var hdr=$(".hdr"), tab=$(".tabbar"), lastY=0, ticking=false;
  var lightTop=hdr&&hdr.classList.contains("light-top");
  function onScroll(){
    var y=window.scrollY;
    if(hdr){ if(!lightTop) hdr.classList.toggle("solid",y>40); hdr.classList.toggle("hide",y>500&&y>lastY+4&&!document.body.classList.contains("sheet-open")); if(y<lastY-4) hdr.classList.remove("hide"); }
    if(tab){ tab.classList.toggle("hide",y>300&&y>lastY+6); if(y<lastY-4||y<300) tab.classList.remove("hide"); }
    lastY=y; ticking=false;
  }
  window.addEventListener("scroll",function(){ if(!ticking){requestAnimationFrame(onScroll);ticking=true} },{passive:true});
  onScroll();

  /* ---------- Sheets ---------- */
  var scrim=$(".scrim"), openSheet=null, lastFocus=null;
  function showSheet(id){
    var s=document.getElementById(id); if(!s) return;
    lastFocus=document.activeElement;
    s.classList.add("on"); s.setAttribute("aria-hidden","false"); scrim.classList.add("on");
    document.body.classList.add("sheet-open"); openSheet=s;
    var f=s.querySelector("a,button"); if(f) setTimeout(function(){f.focus({preventScroll:true})},60);
  }
  function hideSheet(){
    if(!openSheet) return;
    openSheet.classList.remove("on"); openSheet.setAttribute("aria-hidden","true"); scrim.classList.remove("on");
    document.body.classList.remove("sheet-open"); openSheet=null;
    if(lastFocus) lastFocus.focus({preventScroll:true});
  }
  $$("[data-sheet]").forEach(function(b){ b.addEventListener("click",function(e){ e.preventDefault(); showSheet(b.dataset.sheet) }) });
  $$("[data-close]").forEach(function(b){ b.addEventListener("click",hideSheet) });
  if(scrim) scrim.addEventListener("click",function(){ hideSheet(); if(window.MHChat) window.MHChat.close() });
  document.addEventListener("keydown",function(e){ if(e.key==="Escape"){ hideSheet(); closeLb(); } });
  // swipe down to close (momentum)
  $$(".sheet").forEach(function(s){
    var y0=null,t0=0,dy=0;
    s.addEventListener("touchstart",function(e){ if(s.scrollTop>0) return; y0=e.touches[0].clientY; t0=Date.now(); dy=0; s.style.transition="none" },{passive:true});
    s.addEventListener("touchmove",function(e){ if(y0===null) return; dy=e.touches[0].clientY-y0; var d=dy<0?dy*0.2:dy; s.style.transform="translateY("+d+"px)" },{passive:true});
    s.addEventListener("touchend",function(){ if(y0===null) return; s.style.transition=""; s.style.transform=""; var v=Math.abs(dy)/Math.max(1,Date.now()-t0); if(dy>110||(dy>20&&v>0.11)) hideSheet(); y0=null });
  });

  /* ---------- Rails ---------- */
  $$("[data-rail]").forEach(function(wrap){
    var rail=wrap.querySelector(".rail"); if(!rail) return;
    $$("[data-dir]",wrap).forEach(function(b){ b.addEventListener("click",function(){ rail.scrollBy({left:(+b.dataset.dir)*rail.clientWidth*0.8,behavior:RM?"auto":"smooth"}) }) });
  });

  /* ---------- Filters (team building / réalisations) ---------- */
  $$("[data-filter-group]").forEach(function(g){
    var target=document.getElementById(g.dataset.filterGroup);
    var items=$$("[data-cat]",target);
    $$(".chip",g).forEach(function(c){
      c.addEventListener("click",function(){
        $$(".chip",g).forEach(function(x){x.setAttribute("aria-pressed","false")}); c.setAttribute("aria-pressed","true");
        var f=c.dataset.f; var shown=[];
        items.forEach(function(it){ var ok=f==="all"||(" "+it.dataset.cat+" ").indexOf(" "+f+" ")>-1; it.hidden=!ok; if(ok) shown.push(it) });
        if(M&&!RM) M.animate(shown,{opacity:[0,1],transform:["translateY(10px)","translateY(0)"]},{duration:.45,delay:M.stagger(.035),easing:EASE});
        var live=document.getElementById(g.dataset.filterGroup+"-live"); if(live) live.textContent=shown.length+" résultat"+(shown.length>1?"s":"");
      });
    });
  });

  /* ---------- Lightbox ---------- */
  var lb=$(".lightbox");
  function closeLb(){ if(lb&&lb.classList.contains("on")){ lb.classList.remove("on"); lb.setAttribute("aria-hidden","true") } }
  if(lb){
    $$(".gal figure").forEach(function(f){
      f.tabIndex=0; f.setAttribute("role","button");
      var open=function(){ var im=f.querySelector("img"); $("img",lb).src=im.currentSrc.replace("-m.webp",".webp"); $("img",lb).alt=im.alt; $("p",lb).textContent=f.querySelector("figcaption").innerText.replace(/\n/g," · "); lb.classList.add("on"); lb.setAttribute("aria-hidden","false"); $("button",lb).focus() };
      f.addEventListener("click",open); f.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" "){e.preventDefault();open()} });
    });
    lb.addEventListener("click",function(e){ if(e.target===lb||e.target.closest("button")) closeLb() });
  }

  /* ---------- Devis stepper ---------- */
  var form=$("#devis-form");
  if(form){
    var steps=$$(".step",form), idx=0, bar=$(".progress i",form), count=$("[data-count]",form);
    function go(n){
      steps[idx].hidden=true; idx=n; steps[idx].hidden=false;
      bar.style.width=((idx+1)/steps.length*100)+"%"; if(count) count.textContent=(idx+1)+" / "+steps.length;
      if(M&&!RM) M.animate(steps[idx],{opacity:[0,1],transform:["translateX(14px)","translateX(0)"]},{duration:.4,easing:EASE});
      var top=form.getBoundingClientRect().top+window.scrollY-110; if(window.scrollY>top) window.scrollTo({top:top,behavior:RM?"auto":"smooth"});
      var f=steps[idx].querySelector("input,textarea,select"); if(f&&window.matchMedia("(pointer:fine)").matches) f.focus({preventScroll:true});
    }
    function valid(step){
      var ok=true;
      $$("[required]",step).forEach(function(i){
        var err=i.closest(".field")?i.closest(".field").querySelector(".err"):null, bad=false;
        if(i.type==="radio"){ bad=!step.querySelector('input[name="'+i.name+'"]:checked') }
        else if(i.type==="checkbox"){ bad=!i.checked }
        else if(i.type==="email"){ bad=!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(i.value.trim()) }
        else bad=!i.value.trim();
        if(i.type!=="radio") i.setAttribute("aria-invalid",bad?"true":"false");
        if(err) err.textContent=bad?(i.dataset.err||"Ce champ est nécessaire pour vous répondre."):"";
        if(bad) ok=false;
      });
      return ok;
    }
    $$("[data-next]",form).forEach(function(b){ b.addEventListener("click",function(){ if(valid(steps[idx])) go(idx+1); else { var f=steps[idx].querySelector('[aria-invalid=true]'); if(f) f.focus() } }) });
    $$("[data-prev]",form).forEach(function(b){ b.addEventListener("click",function(){ go(idx-1) }) });
    form.addEventListener("submit",function(e){
      e.preventDefault(); if(!valid(steps[idx])) return;
      var fd=new FormData(form), lines=[];
      var labels={type:"Type d'événement",date:"Date souhaitée",lieu:"Lieu / ville",invites:"Nombre d'invités",budget:"Budget estimatif",prestations:"Prestations",details:"Projet",prenom:"Prénom",nom:"Nom",email:"E-mail",tel:"Téléphone",societe:"Société"};
      var acc={}; fd.forEach(function(v,k){ if(k==="consent"||!String(v).trim()) return; acc[k]=acc[k]?acc[k]+", "+v:v });
      Object.keys(acc).forEach(function(k){ lines.push((labels[k]||k)+" : "+acc[k]) });
      var body=lines.join("\n");
      var done=$(".done",form.parentElement);
      form.hidden=true; done.hidden=false;
      $(".recap",done).textContent=body;
      var subject="Demande de devis — "+(acc.type||"événement")+(acc.date?" — "+acc.date:"");
      $("[data-mailto]",done).href="mailto:contact@mh-event.fr?subject="+encodeURIComponent(subject)+"&body="+encodeURIComponent(body);
      $("[data-copy]",done).addEventListener("click",function(ev){ var b=ev.currentTarget; try{ navigator.clipboard.writeText(body).then(function(){b.textContent="Copié"}) }catch(err){} });
      lottie($(".done-lottie",done),"success");
      done.scrollIntoView({behavior:RM?"auto":"smooth",block:"center"});
    });
  }
  // contact form (simple)
  var cf=$("#contact-form");
  if(cf){ cf.addEventListener("submit",function(e){ e.preventDefault(); var fd=new FormData(cf); var body="Nom : "+fd.get("nom")+"\nE-mail : "+fd.get("email")+"\nTéléphone : "+(fd.get("tel")||"")+"\n\n"+fd.get("message"); var a=$("[data-mailto]",cf.parentElement); a.href="mailto:contact@mh-event.fr?subject="+encodeURIComponent("Message — "+(fd.get("sujet")||"site"))+"&body="+encodeURIComponent(body); cf.hidden=true; a.closest(".done").hidden=false; lottie($(".done-lottie",cf.parentElement),"success") }) }

  /* ---------- Year ---------- */
  $$("[data-year]").forEach(function(e){ e.textContent=new Date().getFullYear() });
})();
;(function(){var els=document.querySelectorAll('.echo,.ghost');function on(t){t.classList.add('is-in')}
if(!('IntersectionObserver' in window)){els.forEach(on);return}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var t=e.target._echo||e.target;on(t);io.unobserve(e.target)}})},{threshold:.2});
els.forEach(function(e){var w=e.classList.contains('echo')&&e.previousElementSibling;if(w){w._echo=e;io.observe(w)}else io.observe(e)})})();
/* Parallaxe + effet liquide + arrivées */
;(function(){
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var NS='http://www.w3.org/2000/svg';
  var svg=document.createElementNS(NS,'svg');svg.setAttribute('width','0');svg.setAttribute('height','0');svg.setAttribute('aria-hidden','true');svg.style.position='absolute';document.body.appendChild(svg);
  var uid=0;
  function liquid(img,from,dur){
    return;
    if(reduce||!img)return;
    var id='mhliq'+(uid++),f=document.createElementNS(NS,'filter');f.setAttribute('id',id);f.setAttribute('x','-10%');f.setAttribute('y','-10%');f.setAttribute('width','120%');f.setAttribute('height','120%');
    var t=document.createElementNS(NS,'feTurbulence');t.setAttribute('type','fractalNoise');t.setAttribute('baseFrequency','0.008 0.022');t.setAttribute('numOctaves','2');t.setAttribute('seed',String(Math.floor(Math.random()*90)));t.setAttribute('result','n');
    var d=document.createElementNS(NS,'feDisplacementMap');d.setAttribute('in','SourceGraphic');d.setAttribute('in2','n');d.setAttribute('xChannelSelector','R');d.setAttribute('yChannelSelector','G');d.setAttribute('scale',String(from));
    f.appendChild(t);f.appendChild(d);svg.appendChild(f);img.style.filter='url(#'+id+')';
    var t0=performance.now();
    (function step(now){var k=Math.min(1,(now-t0)/dur),e=1-Math.pow(1-k,3);
      d.setAttribute('scale',(from*(1-e)).toFixed(2));
      t.setAttribute('baseFrequency',(0.008+0.006*Math.sin(k*3.1)).toFixed(4)+' '+(0.022-0.008*k).toFixed(4));
      if(k<1)requestAnimationFrame(step);else{img.style.filter='';f.remove()}})(t0);
  }
  var sel='.arch,.frame,.tile,.gal figure,.place,.mo-img,.band>.bg';
  var boxes=[].slice.call(document.querySelectorAll(sel)).filter(function(b){return b.querySelector('img')});
  boxes.forEach(function(b){b.classList.add('px')});
  var fine=window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  /* parallaxe */
  if(!reduce){
    var ticking=false;
    function upd(){ticking=false;var vh=innerHeight;boxes.forEach(function(b){var r=b.getBoundingClientRect();if(r.bottom<-50||r.top>vh+50)return;var p=(r.top+r.height/2-vh/2)/(vh/2+r.height/2);var amp=b.matches('.band>.bg')?9:6;b.style.setProperty('--py',(-p*amp).toFixed(2)+'%')})}
    addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(upd)}},{passive:true});addEventListener('resize',upd);upd();
  }
  /* liquide : à l'arrivée et au survol */
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){var big=e.target.getBoundingClientRect().width<900;if(big)liquid(e.target.querySelector('img'),70,1500);io.unobserve(e.target)}})},{threshold:.25});
    boxes.forEach(function(b){if(!b.closest('.hero'))io.observe(b)});
  }
  if(fine){boxes.forEach(function(b){var busy=0;b.addEventListener('pointerenter',function(){var now=Date.now();if(now-busy<1000)return;busy=now;liquid(b.querySelector('img'),34,1000)})})}
  /* arrivées en cascade */
  var groups=[['.act','.acts, .grid, main'],['.tile',''],['.gal figure',''],['.pole',''],['.post',''],['.faq details',''],['.mo-shape','']];
  var items=[];
  groups.forEach(function(g){var els=document.querySelectorAll(g[0]);var byParent=new Map();els.forEach(function(el){var p=el.parentElement;var n=byParent.get(p)||0;el.style.setProperty('--i',n%4);byParent.set(p,n+1);el.classList.add(el.matches('.mo-shape')?'shape-in':'rise');items.push(el)})});
  document.querySelectorAll('.hero-shape,.cs-q,.cs-p,.cs-c,.sep').forEach(function(el,i){if(!el.matches('.sep')){el.classList.add('shape-in');el.style.setProperty('--i',i%3);items.push(el)}});
  if('IntersectionObserver' in window&&!reduce){var io2=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io2.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});items.forEach(function(el){io2.observe(el)})}else items.forEach(function(el){el.classList.add('in')});
})();
/* Vidéo du hero : pause accessible, coupée si animations réduites ou économie de données */
;(function(){var v=document.querySelector('.hv-video'),b=document.querySelector('.hv-pause');if(!v)return;
 var rm=matchMedia('(prefers-reduced-motion: reduce)').matches,save=navigator.connection&&navigator.connection.saveData;
 function set(p){if(p){v.pause()}else{var r=v.play();if(r&&r.catch)r.catch(function(){})}if(b){b.setAttribute('aria-pressed',p?'true':'false');b.setAttribute('aria-label',p?'Lire la vidéo':'Mettre la vidéo en pause')}}
 if(rm||save){v.removeAttribute('autoplay');set(true)}
 if(b)b.addEventListener('click',function(){set(!v.paused)});
 if('IntersectionObserver' in window)new IntersectionObserver(function(es){es.forEach(function(e){if(b&&b.getAttribute('aria-pressed')==='true')return;if(e.isIntersecting)set(false);else v.pause()})}).observe(v);
})();
;(function(){var h=document.querySelector('.hero-v');if(!h||!('IntersectionObserver' in window))return;new IntersectionObserver(function(es){document.body.classList.toggle('hero-in',es[0].intersectionRatio>.35)},{threshold:[0,.35,.6,1]}).observe(h)})();
