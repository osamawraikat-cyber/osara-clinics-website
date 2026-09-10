from pathlib import Path
import re, json, sys, subprocess
import xml.etree.ElementTree as ET

BASE='e36fccf5c72781ba7314ceddf8d42a0b57b4e0f6'
NEW=['vitiligo-surgery-jordan','melanocyte-transplantation-vitiligo','punch-grafting-vitiligo','acne-treatment','hair-loss-treatment','wart-removal-cryotherapy','skin-biopsy','melasma-pigmentation-treatment','cataract-surgery','glaucoma-treatment','diabetic-eye-exam-retinopathy','pterygium-treatment-surgery','pediatric-ophthalmology','strabismus-treatment','dry-eye-treatment']
OLD=['','dermatology','ophthalmology','doctors/dr-osama-alwreikat','doctors/dr-sara-abu-touq','vitiligo-jordan','botox-hyperhidrosis','mole-removal','school-health','psoriasis-treatment','acne-scar-treatment']
MARK='<!-- WAVE1-INTERNAL-LINKS -->'

def add(path, fragment):
    p=Path(path); s=p.read_text()
    if MARK in s: return
    needle='<section class="osara-contact-block"'
    if needle not in s: raise SystemExit(f'contact block missing: {path}')
    p.write_text(s.replace(needle, MARK+'\n'+fragment+'\n'+needle, 1))

add('dermatology.html','''<section class="card"><h2>أدلة العلاج والخدمات | Treatment & service guides</h2><div class="links"><a href="/vitiligo-surgery-jordan">جراحة البهاق | Vitiligo Surgery</a><a href="/melanocyte-transplantation-vitiligo">زراعة الخلايا الصبغية | NCMT</a><a href="/punch-grafting-vitiligo">Punch Minigrafting للبهاق</a><a href="/acne-treatment">علاج حب الشباب | Acne Treatment</a><a href="/hair-loss-treatment">علاج تساقط الشعر | Hair Loss</a><a href="/wart-removal-cryotherapy">الثآليل والكرايوثيرابي | Warts & Cryotherapy</a><a href="/skin-biopsy">خزعة الجلد | Skin Biopsy</a><a href="/melasma-pigmentation-treatment">الكلف والتصبغات | Melasma & Pigmentation</a></div></section>''')
add('ophthalmology.html','''<section class="card"><h2>أدلة طب العيون | Eye-care guides</h2><div class="links"><a href="/cataract-surgery">عملية المياه البيضاء / الساد | Cataract Surgery</a><a href="/glaucoma-treatment">الجلوكوما / المياه الزرقاء | Glaucoma</a><a href="/diabetic-eye-exam-retinopathy">فحص العين للسكري واعتلال الشبكية</a><a href="/pterygium-treatment-surgery">علاج وعملية الظفرة | Pterygium</a><a href="/pediatric-ophthalmology">طب عيون الأطفال | Pediatric Ophthalmology</a><a href="/strabismus-treatment">علاج الحول | Strabismus</a><a href="/dry-eye-treatment">علاج جفاف العين | Dry Eye</a></div></section>''')
add('vitiligo-jordan.html','''<section class="card-box"><h2>جراحة البهاق للحالات المختارة</h2><div class="h2-en">Vitiligo surgery for selected patients</div><p>في بعض حالات البهاق المستقر وبعد التقييم الطبي قد تُناقش خيارات جراحية منفصلة عن العلاج العام.</p><div class="links"><a href="/vitiligo-surgery-jordan">جراحة البهاق | Vitiligo Surgery</a><a href="/melanocyte-transplantation-vitiligo">زراعة الخلايا الصبغية غير المزروعة | NCMT</a><a href="/punch-grafting-vitiligo">Punch Minigrafting</a></div></section>''')
add('doctors/dr-osama-alwreikat.html','''<section class="card"><h2>أدلة مرتبطة بخدمات الجلدية | Related dermatology guides</h2><div class="links"><a href="/vitiligo-surgery-jordan">جراحة البهاق</a><a href="/melanocyte-transplantation-vitiligo">NCMT</a><a href="/punch-grafting-vitiligo">Punch Minigrafting</a><a href="/acne-treatment">حب الشباب</a><a href="/hair-loss-treatment">تساقط الشعر</a><a href="/wart-removal-cryotherapy">الثآليل والكرايوثيرابي</a><a href="/skin-biopsy">خزعة الجلد</a><a href="/melasma-pigmentation-treatment">الكلف والتصبغات</a></div></section>''')
add('doctors/dr-sara-abu-touq.html','''<section class="card"><h2>أدلة مرتبطة بطب العيون | Related ophthalmology guides</h2><p>للحالات الجراحية التي تحتاج غرفة عمليات، تكون الاستشارة والتخطيط والمتابعة عبر مسار الرعاية مع د. سارة، وتتم العملية في مستشفى أو منشأة جراحية مناسبة عند الحاجة.</p><div class="links"><a href="/cataract-surgery">عملية المياه البيضاء / الساد</a><a href="/glaucoma-treatment">الجلوكوما</a><a href="/diabetic-eye-exam-retinopathy">فحص العين للسكري</a><a href="/pterygium-treatment-surgery">الظفرة</a><a href="/pediatric-ophthalmology">طب عيون الأطفال</a><a href="/strabismus-treatment">الحول</a><a href="/dry-eye-treatment">جفاف العين</a></div></section>''')
add('school-health.html','''<section class="card-box"><h2>روابط عيون الأطفال | Pediatric eye links</h2><div class="links"><a href="/pediatric-ophthalmology">طب عيون الأطفال | Pediatric Ophthalmology</a><a href="/strabismus-treatment">الحول | Strabismus</a></div></section>''')

sm=Path('sitemap.xml'); tree=ET.parse(sm); root=tree.getroot(); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
existing={u.find(ns+'loc').text for u in root.findall(ns+'url')}
for r in NEW:
    url='https://osaraclinics.com/'+r
    if url not in existing:
        e=ET.SubElement(root,ns+'url'); ET.SubElement(e,ns+'loc').text=url; ET.SubElement(e,ns+'lastmod').text='2026-09-10'
ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9'); tree.write(sm,encoding='utf-8',xml_declaration=True)

p=Path('MEDICAL_REVIEW_REQUIRED.md'); s=p.read_text(); heading='## Wave 1 pre-deployment pages — PHYSICIAN REVIEW REQUIRED'
if heading not in s:
    rows='\n'.join(f'| `/{r}` | Contextual medical review before production. | **PENDING** |' for r in NEW)
    p.write_text(s+f'''\n\n{heading}\n\nThese implementation drafts are **not physician-approved yet**. Existing pending/approved distinctions above remain unchanged.\n\n| URL | Review focus | Status |\n|---|---|---|\n{rows}\n\nNo numerical success rates, guarantees, permanent/scar-free/best/safe claims, fixed durations, FDA claims or absolute indications are approved by this section. Surgical pages must distinguish service availability through the OSara/physician care pathway from the physical operating location.\n''')

routes=OLD+NEW; errs=[]; titles={}; cans={}; inbound={r:0 for r in routes}
for r in routes:
    f=Path('index.html') if not r else Path(r+'.html')
    if not f.exists(): errs.append(f'missing {f}'); continue
    h=f.read_text(); label=r or '/'
    if len(re.findall(r'<h1\b',h,re.I))!=1: errs.append(label+': H1')
    tm=re.search(r'<title>(.*?)</title>',h,re.I|re.S); title=tm.group(1).strip() if tm else ''
    cm=re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"',h,re.I); can=cm.group(1) if cm else ''
    expected='https://osaraclinics.com/' if not r else 'https://osaraclinics.com/'+r
    if can!=expected: errs.append(label+': canonical')
    if title in titles: errs.append(label+': duplicate title')
    titles[title]=label
    if can in cans: errs.append(label+': duplicate canonical')
    cans[can]=label
    if not re.search(r'<meta\s+name="description"\s+content="[^"]+"',h,re.I): errs.append(label+': meta description')
    for prop in ['og:type','og:title','og:description','og:url','og:image']:
        if prop not in h: errs.append(label+': '+prop)
    for b in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',h,re.I|re.S):
        try: json.loads(b)
        except Exception: errs.append(label+': JSON-LD')
    if 'G-72BY7LC2V2' not in h or '/assets/analytics.js' not in h or '/assets/site-nav.js' not in h: errs.append(label+': required scripts')
    for href in re.findall(r'href="(/[^"]*)"',h):
        t=href.split('#')[0].split('?')[0].rstrip('/').lstrip('/')
        if t in inbound: inbound[t]+=1
for i,r in enumerate(NEW):
    h=Path(r+'.html').read_text()
    if inbound[r]==0: errs.append(r+': orphan')
    doctor='dr-osama-alwreikat#physician' if i<8 else 'dr-sara-abu-touq#physician'
    if doctor not in h: errs.append(r+': physician entity')
    for token in ['962778423361','FMrYnf8xmhJJETsG9','data-appointment']:
        if token not in h: errs.append(r+': '+token)
    if re.search(r'data-(diagnosis|condition|message|patient|symptom)',h,re.I): errs.append(r+': sensitive analytics data')

ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'; t=ET.parse('sitemap.xml'); urls=[u.find(ns+'loc').text for u in t.getroot().findall(ns+'url')]
expected_urls={'https://osaraclinics.com/' if not r else 'https://osaraclinics.com/'+r for r in routes}
if len(urls)!=26 or set(urls)!=expected_urls: errs.append(f'sitemap count/set {len(urls)}')
for protected in ['OSARA_SEO_HANDOFF.md','robots.txt','netlify.toml','assets/analytics.js','assets/site-nav.js','assets/site-nav.css','assets/contact-cta.css','assets/guide-layout.css']:
    if subprocess.run(['git','diff','--quiet',BASE,'--',protected]).returncode: errs.append('protected changed '+protected)

print('NEW INBOUND:',{r:inbound[r] for r in NEW})
if errs:
    print('ERRORS:'); print('\n'.join(errs)); sys.exit(1)
print('PASS: 26 routes; 15 new; unique title/canonical; OG complete; JSON-LD parses; analytics preserved; no orphans; sitemap exact; protected files unchanged.')
