(function(){
  'use strict';
  function init(){
    var header=document.querySelector('.osara-global-header, .main-header');
    if(!header) return;
    var nav=header.querySelector('.main-nav');
    var toggle=header.querySelector('.mobile-menu-btn');
    if(!nav||!toggle) return;
    if(!nav.querySelector('.osara-drawer-head')){
      var head=document.createElement('div');
      head.className='osara-drawer-head';
      head.innerHTML='<a class="osara-drawer-logo" href="/" aria-label="OSara Clinics home"><img src="/assets/logo.png" alt="عيادات أوسارا | OSara Clinics"></a><button type="button" class="osara-drawer-close" aria-label="Close menu">×</button>';
      nav.insertBefore(head,nav.firstChild);
    }
    var scrim=document.querySelector('.osara-nav-scrim');
    if(!scrim){ scrim=document.createElement('div'); scrim.className='osara-nav-scrim'; scrim.setAttribute('aria-hidden','true'); document.body.appendChild(scrim); }
    var closeBtn=nav.querySelector('.osara-drawer-close');
    function setOpen(open){
      nav.classList.toggle('active',open); scrim.classList.toggle('active',open); document.body.classList.toggle('osara-nav-open',open);
      toggle.setAttribute('aria-expanded',open?'true':'false'); scrim.setAttribute('aria-hidden',open?'false':'true');
    }
    toggle.setAttribute('aria-expanded','false'); toggle.setAttribute('aria-controls',nav.id||'main-nav');
    toggle.addEventListener('click',function(){setOpen(!nav.classList.contains('active'));});
    closeBtn.addEventListener('click',function(){setOpen(false);});
    scrim.addEventListener('click',function(){setOpen(false);});
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){setOpen(false);});});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false);});
    window.addEventListener('resize',function(){if(window.innerWidth>768)setOpen(false);});
    var path=window.location.pathname;
    nav.querySelectorAll('.nav-links a').forEach(function(a){
      a.classList.remove('active');
      var href=a.getAttribute('href')||'';
      if((path==='/'&&href==='/#hero')||(path==='/dermatology'&&href==='/dermatology')||(path==='/ophthalmology'&&href==='/ophthalmology')) a.classList.add('active');
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();