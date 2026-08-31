import json,re,sys,requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urljoin
BASE='https://osaraclinics.com'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
errors=[]; pages={}
s=requests.Session(); s.headers['User-Agent']='OSara-PR2-production-validator/1.0'
for r in ROUTES:
    resp=s.get(BASE+r,allow_redirects=False,timeout=20)
    if resp.status_code!=200: errors.append(f'{r} status {resp.status_code}')
    soup=BeautifulSoup(resp.text,'html.parser'); pages[r]=soup
    exp=BASE+('/' if r=='/' else r)
    can=(soup.find('link',rel='canonical') or {}).get('href') if soup.find('link',rel='canonical') else None
    og=(soup.find('meta',attrs={'property':'og:url'}) or {}).get('content') if soup.find('meta',attrs={'property':'og:url'}) else None
    if can!=exp: errors.append(f'{r} canonical {can}')
    if og!=exp: errors.append(f'{r} og {og}')
    for ld in soup.find_all('script',type='application/ld+json'):
        try: json.loads(ld.string or ld.get_text())
        except Exception as e: errors.append(f'{r} JSON-LD {e}')
rob=s.get(BASE+'/robots.txt',timeout=20)
if rob.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in rob.text: errors.append('robots')
sm=s.get(BASE+'/sitemap.xml',timeout=20); locs=re.findall(r'<loc>(.*?)</loc>',sm.text)
expected=[BASE+('/' if r=='/' else r) for r in ROUTES]
if locs!=expected: errors.append(f'sitemap {locs}')
req={'/dermatology':['/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal'],'/':['/psoriasis-treatment','/acne-scar-treatment'],'/vitiligo-jordan':['/dermatology','/psoriasis-treatment','/acne-scar-treatment'],'/botox-hyperhidrosis':['/dermatology','/psoriasis-treatment','/acne-scar-treatment'],'/mole-removal':['/dermatology','/psoriasis-treatment','/acne-scar-treatment']}
for r,need in req.items():
    hrefs=[a.get('href') for a in pages[r].find_all('a',href=True)]
    for n in need:
        if n not in hrefs: errors.append(f'{r} missing {n}')
seen=set()
for r,soup in pages.items():
    for a in soup.find_all('a',href=True):
        h=a['href']
        if h.startswith(('#','tel:','mailto:','http://','https://')): continue
        p=urlparse(urljoin(BASE+r,h)).path
        if p in seen: continue
        seen.add(p); rr=s.get(BASE+p,allow_redirects=True,timeout=20)
        if rr.status_code>=400: errors.append(f'broken {r}->{p}:{rr.status_code}')
for r in ['/psoriasis-treatment','/acne-scar-treatment']:
    raw=''.join((x.string or x.get_text()) for x in pages[r].find_all('script',type='application/ld+json'))
    for n in ['https://osaraclinics.com/#clinic','https://osaraclinics.com/dermatology#webpage','https://osaraclinics.com/doctors/dr-osama-alwreikat#physician']:
        if n not in raw: errors.append(f'{r} entity {n}')
ps=pages['/psoriasis-treatment'].get_text(' ',strip=True).lower()
ac_raw=pages['/acne-scar-treatment'].get_text(' ',strip=True)
ac=ac_raw.lower()
if 'ordinary stable plaque psoriasis is not, by itself, a medical emergency' not in ps: errors.append('stable plaque emergency clarification missing')
for phrase in ['rapid widespread or severe worsening','widespread pustulation','systemic illness','other severe acute symptoms']:
    if phrase not in ps: errors.append(f'psoriasis urgent phrase missing {phrase}')
if 'في حالات مختارة، خصوصاً بعض الندبات المتدحرجة أو الملتصقة' not in ac_raw: errors.append('subcision individualized rolling wording missing')
if 'في حالات مختارة من الندبات العميقة والضيقة، وخصوصاً بعض ندبات ice-pick' not in ac_raw: errors.append('TCA individualized ice-pick wording missing')
if re.search(r'\b\d{1,3}%\b',ac): errors.append('percentage guarantee present')
if 'complete scar removal should not be promised' not in ac: errors.append('anti-complete-removal wording missing')
for r in ['/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']:
    h=s.get(BASE+r+'.html',allow_redirects=False,timeout=20)
    if h.status_code!=200: errors.append(f'{r}.html {h.status_code}')
www=s.get('https://www.osaraclinics.com/',allow_redirects=False,timeout=20)
if www.status_code not in (301,302,307,308) or not www.headers.get('location','').startswith(BASE): errors.append(f'www {www.status_code} {www.headers.get("location")}')
report={'sitemap_count':len(locs),'internal_checked':len(seen),'errors':errors}
open('prod-http.json','w').write(json.dumps(report,ensure_ascii=False,indent=2)); print(json.dumps(report,ensure_ascii=False,indent=2))
if errors: sys.exit(1)
