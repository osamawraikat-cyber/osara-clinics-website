import json,re,sys
from urllib.parse import urljoin,urlparse
import requests
from bs4 import BeautifulSoup
BASE='https://osaraclinics.com'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
EXPECTED={r:BASE+r for r in ROUTES}; EXPECTED['/']=BASE+'/'
s=requests.Session(); s.headers['User-Agent']='OSara-PR2-production-validator/1.0'
errors=[]; pages={}
for r in ROUTES:
    resp=s.get(BASE+r,allow_redirects=False,timeout=20)
    if resp.status_code!=200: errors.append(f'{r} status {resp.status_code}')
    soup=BeautifulSoup(resp.text,'html.parser'); pages[r]=soup
    c=soup.find('link',rel='canonical'); canon=c.get('href') if c else None
    o=soup.find('meta',attrs={'property':'og:url'}); og=o.get('content') if o else None
    if canon!=EXPECTED[r]: errors.append(f'{r} canonical {canon}')
    if og!=EXPECTED[r]: errors.append(f'{r} og {og}')
    for ld in soup.find_all('script',type='application/ld+json'):
        try: json.loads(ld.string or ld.get_text())
        except Exception as e: errors.append(f'{r} JSON-LD {e}')
for r in ['/psoriasis-treatment','/acne-scar-treatment']:
    raw=''.join(x.string or x.get_text() for x in pages[r].find_all('script',type='application/ld+json'))
    for n in ['https://osaraclinics.com/#clinic','https://osaraclinics.com/doctors/dr-osama-alwreikat#physician','https://osaraclinics.com/dermatology#webpage']:
        if n not in raw: errors.append(f'{r} missing entity {n}')
rob=s.get(BASE+'/robots.txt',timeout=20)
if rob.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in rob.text: errors.append('robots invalid')
sm=s.get(BASE+'/sitemap.xml',timeout=20); locs=re.findall(r'<loc>(.*?)</loc>',sm.text)
if sm.status_code!=200 or locs!=[EXPECTED[r] for r in ROUTES]: errors.append(f'sitemap mismatch {locs}')
req={'/dermatology':['/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal'],'/':['/psoriasis-treatment','/acne-scar-treatment'],'/vitiligo-jordan':['/dermatology','/psoriasis-treatment','/acne-scar-treatment'],'/botox-hyperhidrosis':['/dermatology','/psoriasis-treatment','/acne-scar-treatment'],'/mole-removal':['/dermatology','/psoriasis-treatment','/acne-scar-treatment']}
for r,need in req.items():
    hrefs=[a.get('href') for a in pages[r].find_all('a',href=True)]
    for n in need:
        if n not in hrefs: errors.append(f'{r} missing link {n}')
seen=set()
for r,soup in pages.items():
    for a in soup.find_all('a',href=True):
        h=a['href']
        if h.startswith(('#','tel:','mailto:','http://','https://')): continue
        p=urlparse(urljoin(BASE+r,h)).path
        if p and p not in seen:
            seen.add(p); rr=s.get(BASE+p,allow_redirects=True,timeout=20)
            if rr.status_code>=400: errors.append(f'broken {r}->{p} {rr.status_code}')
ps=pages['/psoriasis-treatment'].find('main').get_text(' ',strip=True).lower()
for x in ['ordinary stable plaque psoriasis is not, by itself, a medical emergency','rapid widespread or severe worsening','widespread pustulation particularly with fever or systemic illness','other severe acute symptoms']:
    if x not in ps: errors.append(f'psoriasis wording missing: {x}')
ac=pages['/acne-scar-treatment'].find('main').get_text(' ',strip=True).lower()
for x in ['rolling scars','ice-pick scars','حالات مختارة','الندبات المتدحرجة أو الملتصقة','الندبات العميقة والضيقة','complete scar removal should not be promised']:
    if x not in ac: errors.append(f'acne wording missing: {x}')
if re.search(r'\b\d+\s*%',ac): errors.append('scar percentage guarantee found')
www=s.get('https://www.osaraclinics.com/',allow_redirects=False,timeout=20)
if www.status_code not in (301,302,307,308) or not www.headers.get('location','').startswith('https://osaraclinics.com'): errors.append(f'www redirect {www.status_code} {www.headers.get("location")}')
for r in ['/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health','/psoriasis-treatment','/acne-scar-treatment']:
    h=s.get(BASE+r+'.html',allow_redirects=False,timeout=20)
    if h.status_code!=200: errors.append(f'{r}.html changed {h.status_code}')
report={'sitemap_count':len(locs),'checked_internal':sorted(seen),'errors':errors}; open('http-report.json','w').write(json.dumps(report,ensure_ascii=False,indent=2)); print(json.dumps(report,ensure_ascii=False,indent=2)); sys.exit(1 if errors else 0)
