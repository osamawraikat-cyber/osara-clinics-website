from pathlib import Path
import re

MAP='https://maps.app.goo.gl/FMrYnf8xmhJJETsG9?g_st=ac'
ROOT=Path('.')
htmls=[p for p in ROOT.rglob('*.html') if '.github' not in p.parts]

for p in htmls:
    s=p.read_text(encoding='utf-8')
    s=s.replace('د. أسامة الوريكات — جلدية وتجميل.', 'د. أسامة الوريكات — جلدية وتناسلية وليزر.')
    if p.as_posix()=='doctors/dr-osama-alwreikat.html':
        s=s.replace('طبيب جلدية وتجميل في عيادات أوسارا، أبو نصير، عمّان.', 'جلدية وتناسلية وليزر في عيادات أوسارا، أبو نصير، عمّان.')
    if p.as_posix()=='dermatology.html':
        s=s.replace('د. أسامة الوريكات</a> — طبيب جلدية وتجميل في عيادات أوسارا.', 'د. أسامة الوريكات</a> — جلدية وتناسلية وليزر في عيادات أوسارا.')
    s=s.replace('https://www.google.com/maps/search/?api=1&query=32.062463,35.864789', MAP)
    p.write_text(s,encoding='utf-8')

idx=Path('index.html')
s=idx.read_text(encoding='utf-8')
s=s.replace('د. أسامة الوريكات — جلدية وتجميل.', 'د. أسامة الوريكات — جلدية وتناسلية وليزر.')
s=s.replace('''                <div class="map-container">\n                    <iframe src="https://maps.google.com/maps?q=OSara%20Clinics%20Dermatology%20%26%20Ophthalmology%20Abu%20Nusair%20Amman%20Jordan&t=&z=15&ie=UTF8&iwloc=&output=embed" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>\n                </div>''', f'''                <div class="map-container map-static-card" aria-label="موقع عيادات أوسارا | OSara Clinics location">\n                    <div class="map-static-icon" aria-hidden="true">⌖</div>\n                    <h3>عيادات أوسارا | OSara Clinics</h3>\n                    <p>أبو نصير، عمّان | Abu Nusair, Amman</p>\n                    <p class="en-text">Open the verified clinic listing in Google Maps for the exact location and directions.</p>\n                    <div class="osara-contact-actions map-actions">\n                        <a class="osara-contact-btn osara-contact-wa" href="https://wa.me/962778423361" target="_blank" rel="noopener">احجز عبر واتساب <span>WhatsApp</span></a>\n                        <a class="osara-contact-btn osara-contact-call" href="tel:+962778423361">اتصل بالعيادة <span>Call</span></a>\n                        <a class="osara-contact-btn osara-contact-directions" href="{MAP}" target="_blank" rel="noopener">الاتجاهات <span>Directions</span></a>\n                    </div>\n                </div>''')
s=s.replace('''.map-container iframe {\n            width: 100%;\n            height: 100%;\n            border: 0;\n        }''','''.map-container iframe {\n            width: 100%;\n            height: 100%;\n            border: 0;\n        }\n\n        .map-static-card {\n            display: flex;\n            flex-direction: column;\n            align-items: center;\n            justify-content: center;\n            text-align: center;\n            padding: 36px;\n            background: linear-gradient(145deg, #ffffff 0%, #E6F3F4 100%);\n        }\n\n        .map-static-icon {\n            width: 76px;\n            height: 76px;\n            border-radius: 50%;\n            display: flex;\n            align-items: center;\n            justify-content: center;\n            margin-bottom: 18px;\n            background: var(--primary);\n            color: #fff;\n            font-size: 2rem;\n            box-shadow: var(--shadow-md);\n        }\n\n        .map-static-card h3 { margin-bottom: 8px; font-size: 1.45rem; }\n        .map-static-card > p { margin-bottom: 8px; }\n        .map-actions { margin-top: 22px; width: 100%; max-width: 620px; }''')
if '/assets/contact-cta.css' not in s:
    s=s.replace('</head>','    <link rel="stylesheet" href="/assets/contact-cta.css">\n</head>',1)
idx.write_text(s,encoding='utf-8')

for p in htmls:
    if p.as_posix()=='index.html': continue
    s=p.read_text(encoding='utf-8')
    if '/assets/contact-cta.css' not in s:
        s=s.replace('</head>','  <link rel="stylesheet" href="/assets/contact-cta.css">\n</head>',1)
    if 'class="osara-contact-block"' not in s:
        specialty='ophthalmology' if p.as_posix() in ['ophthalmology.html','doctors/dr-sara-abu-touq.html'] else 'dermatology'
        block=f'''\n<section class="osara-contact-block" aria-label="التواصل والموقع | Contact and location">\n  <h2>الحجز والتواصل | Contact</h2>\n  <div class="osara-contact-actions">\n    <a class="osara-contact-btn osara-contact-wa" data-specialty="{specialty}" href="https://wa.me/962778423361" target="_blank" rel="noopener">احجز عبر واتساب <span>WhatsApp</span></a>\n    <a class="osara-contact-btn osara-contact-call" data-specialty="{specialty}" href="tel:+962778423361">اتصل بالعيادة <span>Call</span></a>\n    <a class="osara-contact-btn osara-contact-directions" data-specialty="{specialty}" href="{MAP}" target="_blank" rel="noopener">الاتجاهات <span>Directions</span></a>\n  </div>\n</section>\n'''
        if '</main>' in s:
            s=s.replace('</main>',block+'</main>',1)
        elif '<!-- FOOTER -->' in s:
            s=s.replace('<!-- FOOTER -->',block+'\n    <!-- FOOTER -->',1)
        elif '<footer' in s:
            s=s.replace('<footer',block+'\n<footer',1)
    p.write_text(s,encoding='utf-8')

for p in htmls:
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'https://www\.google\.com/maps[^\"\']*', MAP, s)
    s=re.sub(r'https://maps\.google\.com/maps[^\"\']*', MAP, s)
    p.write_text(s,encoding='utf-8')
