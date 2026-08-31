(function () {
  'use strict';

  var regularHours = [
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Saturday', 'Sunday'],
      opens: '16:30',
      closes: '20:30'
    },
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
      opens: '08:00',
      closes: '13:30'
    },
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
      opens: '16:30',
      closes: '20:30'
    }
  ];

  function updateClinicHoursSchema() {
    var scripts = document.querySelectorAll('script[type="application/ld+json"]');

    scripts.forEach(function (script) {
      try {
        var data = JSON.parse(script.textContent);
        if (data && data['@type'] === 'MedicalClinic' && data['@id'] === 'https://osaraclinics.com/#clinic') {
          data.openingHoursSpecification = regularHours;
          script.textContent = JSON.stringify(data);
        }
      } catch (error) {
        // Leave unrelated or malformed structured-data blocks untouched.
      }
    });
  }

  function updateVisibleClinicHours() {
    var topBarItems = document.querySelectorAll('.top-bar-item span');
    topBarItems.forEach(function (item) {
      if (item.textContent.indexOf('Working hours: Call to enquire') !== -1) {
        item.textContent = 'ساعات العمل المنتظمة | Regular clinic hours';
      }
    });

    var hoursList = document.querySelector('.hours-list');
    if (!hoursList) return;

    hoursList.innerHTML = [
      '<li class="hours-item">',
      '  <div class="day-title"><span class="day-ar">السبت - الأحد</span><span class="day-en">Saturday - Sunday</span></div>',
      '  <div class="time-val"><span class="time-ar">16:30 - 20:30</span><span class="time-en">4:30 PM - 8:30 PM</span></div>',
      '</li>',
      '<li class="hours-item">',
      '  <div class="day-title"><span class="day-ar">الإثنين - الخميس</span><span class="day-en">Monday - Thursday</span></div>',
      '  <div class="time-val"><span class="time-ar">08:00 - 13:30<br>16:30 - 20:30</span><span class="time-en">8:00 AM - 1:30 PM<br>4:30 PM - 8:30 PM</span></div>',
      '</li>',
      '<li class="hours-item">',
      '  <div class="day-title"><span class="day-ar">الجمعة</span><span class="day-en">Friday</span></div>',
      '  <div class="time-val"><span class="time-ar" style="color:#EF4444;">مغلق</span><span class="time-en">Closed</span></div>',
      '</li>'
    ].join('');

    var container = hoursList.closest('.hours-container');
    if (!container || container.querySelector('[data-hours-notice]')) return;

    var notice = document.createElement('div');
    notice.setAttribute('data-hours-notice', 'true');
    notice.innerHTML = [
      '<div style="margin:0 0 14px;padding:14px 16px;border-radius:10px;background:#F7F3EC;color:#475569;">',
      '  <p style="margin:0 0 8px;"><strong>ملاحظة المواعيد:</strong> قد تختلف المواعيد والتوافر أحياناً؛ يرجى الاتصال أو التواصل عبر واتساب للتأكيد.</p>',
      '  <p class="en-text" style="margin:0;">Appointments and availability may occasionally vary; please call or WhatsApp to confirm.</p>',
      '</div>',
      '<div style="margin:0 0 14px;padding:16px;border:1px solid rgba(13,92,96,.18);border-radius:10px;background:#E6F3F4;">',
      '  <p style="margin:0 0 8px;"><strong>تواصل للحالات العاجلة خارج ساعات العمل:</strong> للحالات الجلدية أو العينية العاجلة، يمكن التواصل معنا <a href="tel:+962778423361">هاتفياً</a> أو عبر <a href="https://wa.me/962778423361" target="_blank" rel="noopener">واتساب</a>. في الحالات الشديدة أو المهددة للبصر أو الحياة، توجّه إلى أقرب قسم طوارئ مناسب.</p>',
      '  <p class="en-text" style="margin:0;">For urgent dermatological or ophthalmological concerns outside regular clinic hours, you may contact OSara Clinics by <a href="tel:+962778423361">phone</a> or <a href="https://wa.me/962778423361" target="_blank" rel="noopener">WhatsApp</a>. For severe, sight-threatening, or life-threatening emergencies, go to the nearest appropriate emergency department.</p>',
      '</div>'
    ].join('');

    container.insertBefore(notice, hoursList.nextSibling);
  }

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

  updateClinicHoursSchema();
  updateVisibleClinicHours();

  document.addEventListener('click', function (event) {
    var anchor = event.target.closest && event.target.closest('a[href]');
    if (!anchor) return;
    var eventName = classify(anchor);
    if (eventName) pushEvent(eventName, anchor);
  }, { passive: true });
})();
