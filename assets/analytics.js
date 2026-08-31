(function () {
  'use strict';

  function buildPayload(anchor) {
    var payload = {
      source_page: window.location.pathname || '/',
      specialty: anchor.dataset.specialty || undefined,
      service: anchor.dataset.service || undefined,
      campaign: anchor.dataset.campaign || undefined
    };

    Object.keys(payload).forEach(function (key) {
      if (payload[key] === undefined || payload[key] === '') delete payload[key];
    });

    return payload;
  }

  function pushEvent(eventName, anchor) {
    var payload = buildPayload(anchor);

    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, payload);
      return;
    }

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: eventName }, payload));
  }

  function classify(anchor) {
    var explicit = anchor.dataset.analyticsEvent;
    if (explicit) return explicit;

    var href = (anchor.getAttribute('href') || '').toLowerCase();
    if (anchor.matches('[data-appointment], .appointment-link, .book-appointment')) return 'appointment_click';
    if (href.indexOf('wa.me/') !== -1 || href.indexOf('whatsapp.com/') !== -1) return 'whatsapp_click';
    if (href.indexOf('tel:') === 0) return 'phone_click';
    if (href.indexOf('google.com/maps') !== -1 || href.indexOf('maps.app.goo.gl') !== -1 || href.indexOf('goo.gl/maps') !== -1) return 'directions_click';
    return null;
  }

  document.addEventListener('click', function (event) {
    var anchor = event.target.closest && event.target.closest('a[href]');
    if (!anchor) return;
    var eventName = classify(anchor);
    if (eventName) pushEvent(eventName, anchor);
  }, { passive: true });
})();
