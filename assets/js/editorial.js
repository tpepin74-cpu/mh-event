/* Progressive enhancement for the editorial homepage only. */
(function(){
  "use strict";
  function ready(){
    if(!document.body.classList.contains("home-editorial"))return;
    var reduced=window.matchMedia("(prefers-reduced-motion: reduce)");
    var video=document.querySelector(".film-frame video");
    var button=document.querySelector(".film-pause");
    var userPaused=false, loaded=false;
    function load(){
      if(loaded||!video)return;
      var source=video.querySelector("source[data-film-src]");
      if(source){source.src=source.dataset.filmSrc;video.load();loaded=true;}
    }
    function label(){
      if(!button||!video)return;
      button.setAttribute("aria-pressed",video.paused?"true":"false");
      button.setAttribute("aria-label",video.paused?"Lire la vidéo":"Mettre la vidéo en pause");
      button.innerHTML=video.paused?'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor"/></svg>':'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z" fill="currentColor"/></svg>';
    }
    if(video&&button){
      /* mh.js owns click-to-toggle; loading happens first during capture. */
      button.addEventListener("click",function(){load();userPaused=!video.paused;},true);
      video.addEventListener("play",label);video.addEventListener("pause",label);
      label();
      if("IntersectionObserver" in window){
        new IntersectionObserver(function(entries){
          var visible=entries[0].isIntersecting;
          if(!visible){video.pause();return;}
          if(!reduced.matches&&!userPaused&&!(navigator.connection&&navigator.connection.saveData)){
            load();var p=video.play();if(p)p.catch(label);
          }
        },{threshold:.25}).observe(video);
      }
      document.addEventListener("visibilitychange",function(){if(document.hidden)video.pause();});
      reduced.addEventListener("change",function(){if(reduced.matches)video.pause();});
    }
    /* Keep the menu state explicit without changing its established controls. */
    var menu=document.getElementById("menu");
    var trigger=document.querySelector("[data-menu]");
    if(menu&&trigger){
      trigger.setAttribute("aria-expanded","false");
      new MutationObserver(function(){trigger.setAttribute("aria-expanded",menu.classList.contains("on")?"true":"false");}).observe(menu,{attributes:true,attributeFilter:["class"]});
    }
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",ready);else ready();
})();
