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
    if(!scrim){ scrim=document.createElement('div'); scrim.className='osara-nav-scrim'; scrim.setAttribute('aria-hidden','true'); header.appendChild(scrim); }
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
    window.addEventListener('resize',function(){var breakpoint=header.classList.contains('osara-global-header')?980:768;if(window.innerWidth>breakpoint)setOpen(false);});
    // Keep homepage section highlighting intact; it already owns scroll state.
    // Internal pages use the same static menu, with a single active destination.
    if (header.classList.contains('osara-global-header')) {
      var path=window.location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';
      var eyeRoutes=[
        '/ophthalmology','/cataract-surgery','/glaucoma-treatment',
        '/diabetic-eye-exam-retinopathy','/dry-eye-treatment',
        '/pediatric-ophthalmology','/pterygium-treatment-surgery',
        '/strabismus-treatment'
      ];
      var current='/dermatology';
      if (path==='/skincare') current='/skincare';
      else if (path.indexOf('/doctors/')===0) current='/#doctors';
      else if (eyeRoutes.indexOf(path)!==-1) current='/ophthalmology';
      else if (path==='/botox-hyperhidrosis') current='/#cosmetic-derm';
      nav.querySelectorAll('.nav-links a').forEach(function(a){
        a.classList.remove('active');
        a.removeAttribute('aria-current');
        var href=a.getAttribute('href')||'';
        if(href===current){
          a.classList.add('active');
          if(path===href) a.setAttribute('aria-current','page');
        }
      });
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();