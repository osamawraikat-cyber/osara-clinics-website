from pathlib import Path
import re

CSS = r'''
:root{--primary:#0D5C60;--primary-hover:#094548;--primary-light:#E6F3F4;--accent:#C5A880;--accent-dark:#A3855B;--accent-light:#F7F3EC;--text:#1E293B;--muted:#64748B;--bg:#FCFAF7;--card:#fff;--wa:#25D366;--wa-hover:#20BA5A;--shadow:0 10px 28px rgba(15,23,42,.07)}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:'Cairo',Arial,'Noto Sans Arabic',sans-serif;line-height:1.8}a{color:var(--primary)}h1,h2,h3{color:var(--primary);line-height:1.35}.site-header{position:sticky;top:0;z-index:1000;background:rgba(255,255,255,.96);backdrop-filter:blur(12px);border-bottom:1px solid rgba(13,92,96,.08)}.site-header-inner{max-width:1040px;margin:auto;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:18px}.site-brand img{height:56px;width:auto;display:block}.site-nav{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px 16px}.site-nav a{text-decoration:none;font-weight:700;font-size:.94rem}.page-main{max-width:1000px;margin:auto;padding:0 20px 44px}.hero,.profile{margin:0 -20px 34px;padding:72px max(20px,calc((100vw - 1000px)/2 + 20px)) 48px;text-align:center;background:linear-gradient(135deg,#FCFAF7 36%,rgba(230,243,244,.8) 100%);border-radius:0}.hero h1,.profile h1{font-size:clamp(2rem,5vw,2.7rem);margin:12px 0 8px}.hero>p,.profile p{max-width:760px;margin:0 auto 12px}.hero .en,.profile [lang=en]{direction:ltr;text-align:center;color:var(--accent-dark);font-family:'Outfit',Arial,sans-serif}.badge{display:inline-flex;padding:6px 14px;border-radius:999px;background:var(--accent-light);color:var(--accent-dark);font-weight:700;font-size:.86rem}.cta-row{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:24px}.cta{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:13px 20px;border-radius:10px;text-decoration:none;font-weight:800;border:1px solid transparent;min-height:48px}.wa,.book-appointment{background:var(--wa);color:#fff;box-shadow:0 6px 18px rgba(37,211,102,.22)}.wa:hover,.book-appointment:hover{background:var(--wa-hover)}.call{background:var(--primary);color:#fff}.outline{border-color:var(--primary);background:#fff;color:var(--primary)}main>section:not(.hero):not(.profile),.card{background:var(--card);border:1px solid rgba(13,92,96,.07);border-radius:20px;padding:30px;margin:0 0 24px;box-shadow:var(--shadow)}main>section>h2,.card h2{margin-top:0;font-size:1.55rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}.card,.mini{background:#fff}.grid .card,.mini{padding:20px;border-radius:15px;border:1px solid #e8ecec;box-shadow:none}.grid .card h3,.mini strong{color:var(--primary)}.grid .card a,.links a{display:inline-flex;margin-top:8px;font-weight:800;text-decoration:none}.links{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.links a{padding:14px 16px;background:var(--primary-light);border-radius:12px;align-items:center}.en{direction:ltr;text-align:left;color:var(--muted);font-family:'Outfit',Arial,sans-serif}.note{background:#fff8e8;border-right:4px solid var(--accent);padding:15px 17px;border-radius:10px}.crumbs{max-width:1000px;margin:0 auto;padding:14px 20px;display:flex;flex-wrap:wrap;gap:8px;color:var(--muted);font-size:.92rem}.guide-header .site-header-inner{padding-bottom:4px}.footer{background:#0F172A;color:#94A3B8;padding:34px 20px;text-align:center}.footer-inner{max-width:1000px;margin:auto}.footer a{color:var(--accent);text-decoration:none;font-weight:700}.whatsapp-float{position:fixed;left:22px;bottom:22px;width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:var(--wa);color:#fff;text-decoration:none;font-size:1.5rem;box-shadow:0 6px 20px rgba(37,211,102,.38);z-index:999}.profile-card{max-width:760px;margin:0 auto}.kicker{color:var(--accent-dark);font-weight:800}.muted{color:var(--muted)}
@media(max-width:720px){.site-header-inner{align-items:flex-start}.site-brand img{height:48px}.site-nav{gap:6px 12px}.site-nav a{font-size:.86rem}.hero,.profile{padding-top:48px;padding-bottom:38px}.page-main{padding-left:16px;padding-right:16px}.hero,.profile{margin-left:-16px;margin-right:-16px}.card,main>section:not(.hero):not(.profile){padding:22px}.cta-row{display:grid}.cta{width:100%}.grid,.links{grid-template-columns:1fr}.whatsapp-float{left:16px;bottom:16px}}
'''
Path('assets/guide-layout.css').write_text(CSS.strip()+"\n",encoding='utf-8')

FILES=['dermatology.html','ophthalmology.html','doctors/dr-osama-alwreikat.html','doctors/dr-sara-abu-touq.html','psoriasis-treatment.html','acne-scar-treatment.html']
for fn in FILES:
    p=Path(fn); s=p.read_text(encoding='utf-8')
    s=re.sub(r'\s*<style>.*?</style>', '\n  <link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n  <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">\n  <link rel="stylesheet" href="/assets/guide-layout.css">', s, count=1, flags=re.S)
    p.write_text(s,encoding='utf-8')

def shell_header(nav,crumbs=''):
    return f'''<header class="site-header guide-header"><div class="site-header-inner"><a class="site-brand" href="/"><img src="/assets/logo.png" alt="عيادات أوسارا | OSara Clinics"></a><nav class="site-nav">{nav}</nav></div>{crumbs}</header>'''

nav_derm='<a href="/">الرئيسية</a><a href="/dermatology" aria-current="page">الجلدية</a><a href="/ophthalmology">العيون</a><a href="/doctors/dr-osama-alwreikat">د. أسامة</a><a href="/doctors/dr-sara-abu-touq">د. سارة</a>'
nav_oph='<a href="/">الرئيسية</a><a href="/dermatology">الجلدية</a><a href="/ophthalmology" aria-current="page">العيون</a><a href="/doctors/dr-osama-alwreikat">د. أسامة</a><a href="/doctors/dr-sara-abu-touq">د. سارة</a>'
nav_os='<a href="/">الرئيسية</a><a href="/dermatology">الجلدية</a><a href="/ophthalmology">العيون</a><a href="/doctors/dr-osama-alwreikat" aria-current="page">د. أسامة</a><a href="/doctors/dr-sara-abu-touq">د. سارة</a>'
nav_sa='<a href="/">الرئيسية</a><a href="/dermatology">الجلدية</a><a href="/ophthalmology">العيون</a><a href="/doctors/dr-osama-alwreikat">د. أسامة</a><a href="/doctors/dr-sara-abu-touq" aria-current="page">د. سارة</a>'

def finish(s,specialty):
    s=s.replace('<main>','<main class="page-main">',1)
    s=re.sub(r'<footer>.*?</footer>',f'<footer class="footer"><div class="footer-inner"><a href="tel:+962778423361" data-specialty="{specialty}">اتصل بالعيادة</a> · <a href="https://www.google.com/maps/search/?api=1&query=32.062463,35.864789" target="_blank" rel="noopener">الاتجاهات</a></div></footer>',s,count=1,flags=re.S)
    s=s.replace('<script src="/assets/analytics.js" defer></script>',f'<a class="whatsapp-float" href="https://wa.me/962778423361" data-specialty="{specialty}" target="_blank" rel="noopener" aria-label="واتساب">✆</a>\n<script src="/assets/analytics.js" defer></script>',1)
    return s

p=Path('dermatology.html'); s=p.read_text(encoding='utf-8')
s=re.sub(r'<header><nav>.*?</nav></header>',shell_header(nav_derm),s,count=1,flags=re.S)
s=s.replace('<section class="hero"><p>عيادات أوسارا — أبو نصير، عمّان</p>','<section class="hero"><span class="badge">الأمراض الجلدية | Dermatology</span><p class="kicker">عيادات أوسارا — أبو نصير، عمّان</p>',1)
s=s.replace('توجد أيضاً صفحة مشتركة حول <a href="/school-health">صحة الجلد والعيون للأطفال وطلاب المدارس</a>. هذه البوابة لا تكرر تفاصيل كل حالة؛ الهدف منها توجيهك إلى الصفحة الأكثر صلة ثم إلى التقييم الطبي عند الحاجة.','يمكنك أيضاً الاطلاع على <a href="/school-health">صحة الجلد والعيون للأطفال وطلاب المدارس</a> للحصول على معلومات موجهة للعائلات والطلاب، ثم حجز تقييم طبي عند الحاجة.')
s=s.replace('<h2>الطبيب المرتبط بالتخصص</h2>','<h2>طبيب الجلدية في عيادات أوسارا</h2>')
s=finish(s,'dermatology'); p.write_text(s,encoding='utf-8')

p=Path('ophthalmology.html'); s=p.read_text(encoding='utf-8')
s=re.sub(r'<header><nav>.*?</nav></header>',shell_header(nav_oph),s,count=1,flags=re.S)
s=s.replace('<section class="hero"><p>عيادات أوسارا — أبو نصير، عمّان</p>','<section class="hero"><span class="badge">طب العيون | Ophthalmology</span><p class="kicker">عيادات أوسارا — أبو نصير، عمّان</p>',1)
s=s.replace('<h2>الطبيبة المرتبطة بالتخصص</h2>','<h2>طبيبة العيون في عيادات أوسارا</h2>')
s=finish(s,'ophthalmology'); p.write_text(s,encoding='utf-8')

p=Path('doctors/dr-osama-alwreikat.html'); s=p.read_text(encoding='utf-8')
s=re.sub(r'<header><nav>.*?</nav></header>',shell_header(nav_os),s,count=1,flags=re.S)
s=s.replace('<section class="profile"><div><p>الفريق الطبي | Medical Team</p>','<section class="profile"><div class="profile-card"><span class="badge">الفريق الطبي | Medical Team</span>',1)
s=s.replace('طبيب جلدية وتجميل في عيادات أوسارا، أبو نصير، عمّان. تربط هذه الصفحة الطبيب بتخصص الجلدية وبالأدلة والخدمات الجلدية المنشورة على الموقع دون إضافة مؤهلات أو ألقاب غير موثقة.','طبيب جلدية وتجميل في عيادات أوسارا، أبو نصير، عمّان. يمكنك الاطلاع على خدمات الجلدية والمعلومات المرتبطة بالحالات الجلدية، ثم حجز موعد للتقييم عند الحاجة.')
s=s.replace('<h2>التخصص والخدمات المرتبطة</h2>','<h2>الخدمات والمعلومات المرتبطة بالجلدية</h2>')
s=s.replace('<h2>عيادات أوسارا</h2><p>تعمل صفحة الطبيب كجزء من بنية عيادات أوسارا في أبو نصير، عمّان، وتعيد المستخدم إلى صفحة التخصص والخدمات ذات الصلة والحجز.</p>','<h2>الحجز والتواصل</h2><p>تتوفر المواعيد في عيادات أوسارا، أبو نصير، عمّان. للحجز أو الاستفسار عن موعد مناسب يمكنك التواصل عبر واتساب أو الاتصال بالعيادة.</p>')
s=finish(s,'dermatology'); p.write_text(s,encoding='utf-8')

p=Path('doctors/dr-sara-abu-touq.html'); s=p.read_text(encoding='utf-8')
s=re.sub(r'<header><nav>.*?</nav></header>',shell_header(nav_sa),s,count=1,flags=re.S)
s=s.replace('<section class="profile"><div><p>الفريق الطبي | Medical Team</p>','<section class="profile"><div class="profile-card"><span class="badge">الفريق الطبي | Medical Team</span>',1)
s=s.replace('طبيبة عيون في عيادات أوسارا، أبو نصير، عمّان. تربط هذه الصفحة الطبيبة بتخصص طب العيون وبالمحتوى المرتبط المنشور على الموقع دون إضافة مؤهلات أو ألقاب غير موثقة.','طبيبة عيون في عيادات أوسارا، أبو نصير، عمّان. يمكنك الاطلاع على خدمات طب العيون والمعلومات المرتبطة بصحة العيون، ثم حجز موعد للتقييم عند الحاجة.')
s=s.replace('<h2>التخصص والخدمات المرتبطة</h2>','<h2>الخدمات والمعلومات المرتبطة بطب العيون</h2>')
s=s.replace('<h2>عيادات أوسارا</h2><p>تعمل صفحة الطبيبة كجزء من بنية عيادات أوسارا في أبو نصير، عمّان، وتعيد المستخدم إلى صفحة تخصص العيون والحجز والمعلومات المرتبطة.</p>','<h2>الحجز والتواصل</h2><p>تتوفر المواعيد في عيادات أوسارا، أبو نصير، عمّان. للحجز أو الاستفسار عن موعد مناسب يمكنك التواصل عبر واتساب أو الاتصال بالعيادة.</p>')
s=finish(s,'ophthalmology'); p.write_text(s,encoding='utf-8')

for fn,label,crumb in [
('psoriasis-treatment.html','الأمراض الجلدية | Dermatology','<nav class="crumbs" aria-label="Breadcrumb"><a href="/">الرئيسية</a><span>›</span><a href="/dermatology">الجلدية</a><span>›</span><span>الصدفية</span></nav>'),
('acne-scar-treatment.html','الأمراض الجلدية | Dermatology','<nav class="crumbs" aria-label="Breadcrumb"><a href="/">الرئيسية</a><span>›</span><a href="/dermatology">الجلدية</a><span>›</span><span>ندبات حب الشباب</span></nav>')]:
    p=Path(fn); s=p.read_text(encoding='utf-8')
    s=re.sub(r'<header>.*?</header>',shell_header('<a href="/">الرئيسية</a><a href="/dermatology">الجلدية</a><a href="/ophthalmology">العيون</a><a href="/doctors/dr-osama-alwreikat">د. أسامة</a>',crumb),s,count=1,flags=re.S)
    s=s.replace('<main>','<main class="page-main">',1)
    s=s.replace('<section class="hero">','<section class="hero"><span class="badge">'+label+'</span>',1)
    s=re.sub(r'<footer>.*?</footer>','<footer class="footer"><div class="footer-inner"><a href="/">عيادات أوسارا</a> · <a href="/dermatology">الأمراض الجلدية</a> · <a href="https://www.google.com/maps/search/?api=1&query=32.062463,35.864789" target="_blank" rel="noopener">الاتجاهات</a></div></footer>',s,count=1,flags=re.S)
    s=s.replace('<script src="/assets/analytics.js" defer></script>','<a class="whatsapp-float" href="https://wa.me/962778423361" data-specialty="dermatology" target="_blank" rel="noopener" aria-label="واتساب">✆</a>\n<script src="/assets/analytics.js" defer></script>',1)
    p.write_text(s,encoding='utf-8')

p=Path('acne-scar-treatment.html'); s=p.read_text(encoding='utf-8')
s=s.replace('<h2>ما الذي نعرف أنه متاح في عيادات أوسارا؟</h2><p>الموقع الحالي يذكر بالفعل خدمات الديرمابن/الميكرونيدلينغ والتقشير الكيميائي وPRP ضمن خدمات العيادة. أما السبسجن وTCA CROSS وتقنيات إعادة التسطيح الأخرى، فيتم ذكرها هنا كخيارات علاج عامة يجب مناقشة ملاءمتها وتوافرها أثناء الاستشارة بدلاً من افتراض توفرها تلقائياً.</p><p class="en">The current site already lists Dermapen/microneedling, chemical peels and PRP among clinic services. Subcision, TCA CROSS and other resurfacing approaches are described here as general options whose suitability and availability should be confirmed during consultation.</p>', '<h2>الخدمات المرتبطة بعلاج ندبات حب الشباب</h2><p>تشمل الخدمات المتاحة في عيادات أوسارا الديرمابن/الميكرونيدلينغ والتقشير الكيميائي وPRP. أما السبسجن وTCA CROSS وتقنيات إعادة التسطيح الأخرى فتُناقش كخيارات علاجية عامة، وتُحدد ملاءمتها وتوافرها بعد التقييم.</p><p class="en">Available clinic services include Dermapen/microneedling, chemical peels and PRP. Subcision, TCA CROSS and other resurfacing approaches are general options whose suitability and availability should be confirmed during consultation.</p>')
p.write_text(s,encoding='utf-8')
