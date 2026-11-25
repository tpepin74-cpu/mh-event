/* MH Event — V2 · interactions */
(function(){
  "use strict";
  var d=document, html=d.documentElement, body=d.body;
  var RM=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(s,c){return (c||d).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}

  /* ---------- Préchargeur : logo seul, retiré dès que la page est prête ---------- */
  var loader=$(".loader");
  if(loader){
    var first=html.classList.contains("ld-first"), t0=window.__mhT0||Date.now();
    var hide=function(){ if(loader.classList.contains("out")) return; var wait=Math.max(0,(first?1100:250)-(Date.now()-t0));
      setTimeout(function(){ loader.classList.add("out"); body.classList.add("ready"); setTimeout(function(){ if(loader.parentNode) loader.parentNode.removeChild(loader) },900) },wait) };
    if(d.readyState==="complete") hide(); else window.addEventListener("load",hide);
    setTimeout(hide,first?3200:1500);
  }

  /* ---------- En-tête : plein au défilement, masqué en descendant ---------- */
  var hdr=$(".hdr"), tab=$(".tabbar"), lastY=0, ticking=false, light=hdr&&hdr.classList.contains("light");
  function onScroll(){
    var y=window.scrollY;
    if(hdr){ if(!light) hdr.classList.toggle("solid",y>40);
      if(y>480&&y>lastY+4&&!body.classList.contains("menu-open")) hdr.classList.add("hide"); else if(y<lastY-4||y<480) hdr.classList.remove("hide"); }
    if(tab){ var nearEnd=(window.innerHeight+y)>=(d.documentElement.scrollHeight-40); tab.classList.toggle("hide",nearEnd) }
    var prog=$(".ev-progress"); if(prog){ var h=d.documentElement.scrollHeight-window.innerHeight; prog.style.transform="scaleX("+(h>0?y/h:0)+")" }
    lastY=y; ticking=false;
  }
  window.addEventListener("scroll",function(){ if(!ticking){ requestAnimationFrame(onScroll); ticking=true } },{passive:true});
  onScroll();

  /* ---------- Menu plein écran ---------- */
  var menu=$("#menu"), mv=menu?$("video",menu):null, lastFocus=null;
  function openMenu(){ if(!menu) return; lastFocus=d.activeElement; menu.classList.add("on"); menu.setAttribute("aria-hidden","false"); body.classList.add("menu-open");
    $$(".m-nav>li",menu).forEach(function(li,i){ li.style.transitionDelay=(RM?0:.35+i*.05)+"s" });
    if(mv&&!RM){ if(!mv.src&&mv.dataset.src){ mv.src=mv.dataset.src } var p=mv.play(); if(p&&p.catch) p.catch(function(){}) }
    setTimeout(function(){ var c=$(".m-close",menu); if(c) c.focus({preventScroll:true}) },80) }
  function closeMenu(){ if(!menu||!menu.classList.contains("on")) return; menu.classList.remove("on"); menu.setAttribute("aria-hidden","true"); body.classList.remove("menu-open");
    $$(".m-nav>li",menu).forEach(function(li){ li.style.transitionDelay="0s" }); if(mv) setTimeout(function(){ mv.pause() },900); if(lastFocus) lastFocus.focus({preventScroll:true}) }
  $$("[data-menu]").forEach(function(b){ b.addEventListener("click",function(e){ e.preventDefault(); openMenu() }) });
  $$("[data-menu-close]").forEach(function(b){ b.addEventListener("click",closeMenu) });
  d.addEventListener("keydown",function(e){ if(e.key==="Escape") closeMenu() });
  if(menu) menu.addEventListener("keydown",function(e){ if(e.key!=="Tab") return; var f=$$("a,button",menu).filter(function(x){return x.offsetParent!==null}); if(!f.length) return;
    if(e.shiftKey&&d.activeElement===f[0]){ e.preventDefault(); f[f.length-1].focus() } else if(!e.shiftKey&&d.activeElement===f[f.length-1]){ e.preventDefault(); f[0].focus() } });

  /* ---------- Vidéo d'accueil : pause accessible, coupée si animations réduites ---------- */
  var hv=$(".hero video"), hp=$(".v-pause");
  if(hv){
    var save=navigator.connection&&navigator.connection.saveData;
    var setP=function(p){ if(p) hv.pause(); else { var r=hv.play(); if(r&&r.catch) r.catch(function(){}) } if(hp){ hp.setAttribute("aria-pressed",p?"true":"false"); hp.setAttribute("aria-label",p?"Lire la vidéo":"Mettre la vidéo en pause"); hp.innerHTML=p?'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg>':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg>' } };
    if(RM||save){ hv.removeAttribute("autoplay"); setP(true) }
    if(hp) hp.addEventListener("click",function(){ setP(!hv.paused) });
  }
  var hero=$(".hero,.ev-hero");
  if(hero&&"IntersectionObserver" in window){ new IntersectionObserver(function(es){ body.classList.toggle("hero-in",es[0].intersectionRatio>.4) },{threshold:[0,.4,.7,1]}).observe(hero) }

  /* ---------- Apparition douce des textes ---------- */
  var fades=$$(".fade");
  if("IntersectionObserver" in window&&!RM){ var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); io.unobserve(e.target) } }) },{rootMargin:"0px 0px -8% 0px"}); fades.forEach(function(f){ io.observe(f) }) }
  else fades.forEach(function(f){ f.classList.add("in") });

  /* ---------- Réalisations : filtres ---------- */
  var fl=$(".filters");
  if(fl){
    var items=$$(".vg"), live=$("#vign-live"), empty=$(".vign-empty");
    var state={cat:"all",time:"all"};
    var apply=function(){ var n=0; items.forEach(function(it){ var ok=(state.cat==="all"||it.dataset.cat===state.cat)&&(state.time==="all"||it.dataset.time===state.time); it.hidden=!ok; if(ok) n++ });
      if(live) live.textContent=n+" événement"+(n>1?"s":""); if(empty) empty.hidden=n>0 };
    $$("button",fl).forEach(function(b){ b.addEventListener("click",function(){ var g=b.dataset.g;
      if(b.getAttribute("aria-pressed")==="true"&&b.dataset.v!=="all"){ state[g]="all"; b.setAttribute("aria-pressed","false"); var a=$('button[data-g="'+g+'"][data-v="all"]',fl); if(a) a.setAttribute("aria-pressed","true") }
      else { $$('button[data-g="'+g+'"]',fl).forEach(function(x){ x.setAttribute("aria-pressed","false") }); b.setAttribute("aria-pressed","true"); state[g]=b.dataset.v }
      apply() }) });
    var q=location.hash.replace("#","");
    if(q){ var pre=$('button[data-v="'+q+'"]',fl); if(pre) pre.click() }
  }

  /* ---------- Page événement : chapitres ---------- */
  var idx=$$(".ev-index a");
  if(idx.length&&"IntersectionObserver" in window){
    var secs=idx.map(function(a){ return d.getElementById(a.getAttribute("href").slice(1)) });
    var io2=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ var i=secs.indexOf(e.target); idx.forEach(function(a,j){ a.classList.toggle("on",j===i) }) } }) },{rootMargin:"-45% 0px -50% 0px"});
    secs.forEach(function(s){ if(s) io2.observe(s) });
  }

  /* ---------- Formulaires : message prêt à envoyer ---------- */
  function mailForm(form,subjectFn,labels){
    form.addEventListener("submit",function(e){
      e.preventDefault();
      var bad=null; $$("[required]",form).forEach(function(i){ var ok=i.type==="checkbox"?i.checked:(i.type==="radio"?!!form.querySelector('input[name="'+i.name+'"]:checked'):!!i.value.trim()); if(i.type==="email"&&ok) ok=/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(i.value.trim()); i.setAttribute("aria-invalid",ok?"false":"true"); if(!ok&&!bad) bad=i });
      if(bad){ bad.focus(); return }
      var fd=new FormData(form), acc={}, lines=[];
      fd.forEach(function(v,k){ if(k==="consent"||!String(v).trim()) return; acc[k]=acc[k]?acc[k]+", "+v:v });
      Object.keys(acc).forEach(function(k){ lines.push((labels[k]||k)+" : "+acc[k]) });
      var text=lines.join("\n"), done=form.parentNode.querySelector(".done");
      form.hidden=true; done.hidden=false;
      var rc=$(".recap",done); if(rc) rc.textContent=text;
      $("[data-mailto]",done).href="mailto:contact@mh-event.fr?subject="+encodeURIComponent(subjectFn(acc))+"&body="+encodeURIComponent(text);
      var cp=$("[data-copy]",done); if(cp) cp.addEventListener("click",function(){ try{ navigator.clipboard.writeText(text).then(function(){ cp.textContent="Copié" }) }catch(err){} });
      done.scrollIntoView({behavior:RM?"auto":"smooth",block:"center"});
    });
  }
  var dv=$("#devis-form");
  if(dv) mailForm(dv,function(a){ return "Demande de devis — "+(a.type||"événement")+(a.date?" — "+a.date:"") },{type:"Type d'événement",date:"Date souhaitée",lieu:"Lieu / ville",invites:"Nombre d'invités",budget:"Budget estimatif",prestations:"Prestations",details:"Projet",prenom:"Prénom",nom:"Nom",societe:"Société",tel:"Téléphone",email:"E-mail"});
  var cf=$("#contact-form");
  if(cf) mailForm(cf,function(a){ return "Message — "+(a.sujet||"site") },{nom:"Nom",email:"E-mail",tel:"Téléphone",sujet:"Sujet",message:"Message"});
  var pre=$("#devis-form [name=type]") ? new URLSearchParams(location.search).get("type") : null;
  if(pre){ $$("#devis-form input[name=type]").forEach(function(r){ if(r.value===pre) r.checked=true }) }

  $$("[data-year]").forEach(function(e){ e.textContent=new Date().getFullYear() });
})();

/* ---------- Accueil : animations d'entrée au défilement (titres mot à mot, images en rideau, chiffres) ---------- */
(function(){
  var body=document.body; if(!body.classList.contains("home")) return;
  if(window.matchMedia("(prefers-reduced-motion: reduce)").matches||!("IntersectionObserver" in window)) return;
  var html=document.documentElement; html.classList.add("anim");
  function split(el,unit){
    var n=0, walk=function(node){
      [].slice.call(node.childNodes).forEach(function(c){
        if(c.nodeType===3){
          var parts=c.textContent.split(/(\s+)/), frag=document.createDocumentFragment();
          parts.forEach(function(p){
            if(!p) return;
            if(/^\s+$/.test(p)){ frag.appendChild(document.createTextNode(" ")); return }
            var w=document.createElement("span"); w.className="sw";
            if(unit==="char"){ p.split("").forEach(function(ch){ var i=document.createElement("span"); i.className="si"; i.style.setProperty("--i",n++); i.textContent=ch; w.appendChild(i) }) }
            else { var i=document.createElement("span"); i.className="si"; i.style.setProperty("--i",n++); i.textContent=p; w.appendChild(i) }
            frag.appendChild(w);
          });
          c.parentNode.replaceChild(frag,c);
        } else if(c.nodeType===1 && !c.classList.contains("sr")) walk(c);
      });
    };
    walk(el); el.classList.add("split"); el.classList.remove("fade"); return el;
  }
  var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ var t=e.target; (t._cur||t).classList.add("on"); io.unobserve(t) } }) },{rootMargin:"0px 0px -12% 0px",threshold:.05});
  var q=function(s){ return [].slice.call(document.querySelectorAll(s)) };

  /* Hero : lettres une à une, villes en cascade */
  q(".hh-t").forEach(function(t){ split(t,"char"); setTimeout(function(){ t.classList.add("on") },html.classList.contains("ld-first")?1300:350) });
  q(".hh-c>span").forEach(function(s,i){ s.style.setProperty("--i",i) });

  /* Grands titres : mot à mot */
  q("main .t-xl, main .t-h2, .pb-end").forEach(function(t){ split(t,"word"); io.observe(t) });
  /* « PROBLÉMATIQUES » : lettre à lettre */
  q(".pb-t em").forEach(function(t){ split(t,"char") }); q(".pb-t").forEach(function(t){ t.classList.remove("fade"); t.classList.add("split"); io.observe(t) });
  /* Citation : mot à mot */
  q(".quote blockquote").forEach(function(t){ split(t,"word"); io.observe(t) });

  /* Images : rideau + léger zoom arrière */
  q(".door .ph, .card .ph, .intro figure .ph, .vg .tile").forEach(function(p){ p.classList.add("cur"); var w=p.parentElement; w._cur=p; io.observe(w) });
  /* Listes : cascade */
  q(".doors, .cards, .vign, .rows, .cityg, .faq, .figs, .logos").forEach(function(l){ l.classList.add("casc"); [].forEach.call(l.children,function(c,i){ c.style.setProperty("--k",i%6) }); io.observe(l) });

  /* Chiffres clés : compteur */
  q(".figs b").forEach(function(b){
    var raw=b.textContent, m=raw.match(/^([\d]+)(,(\d))?(.*)$/); if(!m) return;
    var target=parseFloat(m[1]+(m[3]?"."+m[3]:"")), dec=m[3]?1:0, suf=m[4];
    var o=new IntersectionObserver(function(es){ if(!es[0].isIntersecting) return; o.disconnect(); var t0=null;
      (function step(t){ if(!t0) t0=t; var k=Math.min(1,(t-t0)/1600), e=1-Math.pow(1-k,3); b.textContent=(target*e).toFixed(dec).replace(".",",")+suf; if(k<1) requestAnimationFrame(step) })(performance.now()) },{threshold:.6});
    b.textContent=(0).toFixed(dec).replace(".",",")+suf; o.observe(b);
  });
})();

/* ---------- Accueil : problématiques en défilement fixe (une crainte par écran) ---------- */
(function(){
  var fx=document.querySelector(".fx"); if(!fx) return;
  var sl=[].slice.call(fx.querySelectorAll(".fx-s")), bg=[].slice.call(fx.querySelectorAll(".fx-bg")), dots=[].slice.call(fx.querySelectorAll(".fx-dots li")), bar=fx.querySelector(".fx-bar i");
  var n=sl.length, cur=0, tick=false;
  function set(i){ if(i===cur) return; sl[cur].classList.remove("on"); sl[cur].classList.add("out"); var prev=sl[cur]; setTimeout(function(){ prev.classList.remove("out") },700);
    bg[cur].classList.remove("on"); if(dots[cur]) dots[cur].classList.remove("on"); cur=i; sl[i].classList.add("on"); bg[i].classList.add("on"); if(dots[i]) dots[i].classList.add("on") }
  function upd(){ tick=false; var r=fx.getBoundingClientRect(), h=fx.offsetHeight-window.innerHeight; var p=Math.max(0,Math.min(1,-r.top/(h||1)));
    set(Math.min(n-1,Math.floor(p*n*0.9999))); if(bar) bar.style.transform="scaleX("+p+")" }
  window.addEventListener("scroll",function(){ if(!tick){ tick=true; requestAnimationFrame(upd) } },{passive:true});
  window.addEventListener("resize",upd); upd();
})();

/* ---------- Accueil : fil d'Ariane vertical (section active, couleur sur fonds sombres) ---------- */
(function(){
  var nav=document.querySelector(".snav"); if(!nav) return;
  var links=[].slice.call(nav.querySelectorAll("a")), secs=links.map(function(a){ return document.getElementById(a.getAttribute("href").slice(1)) });
  var tick=false;
  function upd(){ tick=false; var mid=window.innerHeight*.45, act=-1;
    secs.forEach(function(s,i){ if(s&&s.getBoundingClientRect().top<=mid) act=i });
    links.forEach(function(a,i){ a.classList.toggle("on",i===act) });
    document.body.classList.toggle("snav-on",act>=0&&!document.body.classList.contains("menu-open"));
    var r=nav.getBoundingClientRect(), x=r.left+r.width/2, y=r.top+r.height/2, dark=false;
    nav.style.pointerEvents="none"; var el=document.elementFromPoint(x,y); nav.style.pointerEvents="";
    while(el&&el!==document.body){ if(el.classList&&(el.classList.contains("on-dark")||el.classList.contains("fx")||el.classList.contains("cta-band")||el.tagName==="FOOTER")){ dark=true; break } el=el.parentElement }
    nav.classList.toggle("light",dark);
  }
  window.addEventListener("scroll",function(){ if(!tick){ tick=true; requestAnimationFrame(upd) } },{passive:true});
  window.addEventListener("resize",upd); upd();
})();
