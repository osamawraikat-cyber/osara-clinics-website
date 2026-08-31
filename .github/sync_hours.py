from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

old = '''      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Saturday",
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday"
          ],
          "opens": "09:00",
          "closes": "20:00"
        }
      ],'''
new = '''      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Saturday", "Sunday"],
          "opens": "16:30",
          "closes": "20:30"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"],
          "opens": "08:00",
          "closes": "13:30"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"],
          "opens": "16:30",
          "closes": "20:30"
        }
      ],'''
if old not in s:
    raise SystemExit('old openingHoursSpecification block not found')
s = s.replace(old, new, 1)
s = s.replace('ساعات العمل: اتصل للاستفسار | Working hours: Call to enquire', 'ساعات العمل المنتظمة | Regular clinic hours', 1)

hours = '''<ul class="hours-list">
                        <li class="hours-item">
                            <div class="day-title">
                                <span class="day-ar">السبت - الأحد</span>
                                <span class="day-en">Saturday - Sunday</span>
                            </div>
                            <div class="time-val">
                                <span class="time-ar">16:30 - 20:30</span>
                                <span class="time-en">4:30 PM - 8:30 PM</span>
                            </div>
                        </li>
                        <li class="hours-item">
                            <div class="day-title">
                                <span class="day-ar">الإثنين - الخميس</span>
                                <span class="day-en">Monday - Thursday</span>
                            </div>
                            <div class="time-val">
                                <span class="time-ar">08:00 - 13:30<br>16:30 - 20:30</span>
                                <span class="time-en">8:00 AM - 1:30 PM<br>4:30 PM - 8:30 PM</span>
                            </div>
                        </li>
                        <li class="hours-item">
                            <div class="day-title">
                                <span class="day-ar">الجمعة</span>
                                <span class="day-en">Friday</span>
                            </div>
                            <div class="time-val">
                                <span class="time-ar" style="color: #EF4444;">مغلق</span>
                                <span class="time-en">Closed</span>
                            </div>
                        </li>
                    </ul>
                    <div data-hours-notice="true">
                        <div style="margin:0 0 14px;padding:14px 16px;border-radius:10px;background:#F7F3EC;color:#475569;">
                            <p style="margin:0 0 8px;"><strong>ملاحظة المواعيد:</strong> قد تختلف المواعيد والتوافر أحياناً؛ يرجى الاتصال أو التواصل عبر واتساب للتأكيد.</p>
                            <p class="en-text" style="margin:0;">Appointments and availability may occasionally vary; please call or WhatsApp to confirm.</p>
                        </div>
                        <div style="margin:0 0 14px;padding:16px;border:1px solid rgba(13,92,96,.18);border-radius:10px;background:#E6F3F4;">
                            <p style="margin:0 0 8px;"><strong>تواصل للحالات العاجلة خارج ساعات العمل:</strong> للحالات الجلدية أو العينية العاجلة، يمكن التواصل معنا <a href="tel:+962778423361">هاتفياً</a> أو عبر <a href="https://wa.me/962778423361" target="_blank" rel="noopener">واتساب</a>. في الحالات الشديدة أو المهددة للبصر أو الحياة، توجّه إلى أقرب قسم طوارئ مناسب.</p>
                            <p class="en-text" style="margin:0;">For urgent dermatological or ophthalmological concerns outside regular clinic hours, you may contact OSara Clinics by <a href="tel:+962778423361">phone</a> or <a href="https://wa.me/962778423361" target="_blank" rel="noopener">WhatsApp</a>. For severe, sight-threatening, or life-threatening emergencies, go to the nearest appropriate emergency department.</p>
                        </div>
                    </div>'''

m = re.search(r'<ul class="hours-list">.*?</ul>', s, re.S)
if not m:
    raise SystemExit('visible hours list not found')
s = s[:m.start()] + hours + s[m.end():]
p.write_text(s)
