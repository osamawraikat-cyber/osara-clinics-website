import json,re,requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
BASE='https://osaraclinics.com'
MAP='https://maps.app.goo.gl/FMrYnf8xmhJJETsG9?g_st=ac'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/mole-removal','/school-health','/botox-hyperhidrosis']
S=requests.Session(); S.headers['User-Agent']='OSara-PR5-production-validation/1.0'
errors=[]; rep={'routes':{},'directions':{},'schema_geo':{},'variants':{},'broken_links':[],'broken_images':[],'hours':None,'specialty':None}
all_internal=set()
for r in ROUTES:
    resp=S.get(BASE+r,timeout=25); soup=BeautifulSoup(resp.text,'html.parser')
    can=soup.find('link',rel='canonical'); meta=soup.find('meta',attrs={'name':'description'}); title=soup.title.string.strip() if soup.title and soup.title.string else None
    if resp.status_code!=200: errors.append(f'{r} status {resp.status_code}')
    expected=BASE+('/' if r=='/' else r)
    if not can or can.get('href')!=expected: errors.append(f'{r} canonical')
    if not title or not meta or not meta.get('content'): errors.append(f'{r} title/meta missing')
    if len(soup.find_all('h1'))!=1: errors.append(f'{r} H1 count {len(soup.find_all("h1"))}')
    if '32.062463' in resp.text or '35.864789' in resp.text: errors.append(f'{r} old coordinates remain')
    if r in ('/','/doctors/dr-osama-alwreikat') and 'جلدية وتجميل' in resp.text: errors.append(f'{r} old Dr Osama specialty wording remains')
    if r=='/doctors/dr-osama-alwreikat':
        rep['specialty']='جلدية وتناسلية وليزر' if 'جلدية وتناسلية وليزر' in resp.text else None
        if not rep['specialty']: errors.append('Dr Osama specialty missing')
    for sc in soup.find_all('script',type='application/ld+json'):
        try: data=json.loads(sc.string or sc.get_text())
        except Exception as e: errors.append(f'{r} JSON-LD parse {e}'); continue
        stack=[data]
        while stack:
            x=stack.pop()
            if isinstance(x,dict):
                if x.get('@type')=='GeoCoordinates': rep['schema_geo'][r]={'latitude':x.get('latitude'),'longitude':x.get('longitude')}
                if r=='/' and x.get('@type')=='MedicalClinic': rep['hours']=x.get('openingHoursSpecification')
                stack.extend(x.values())
            elif isinstance(x,list): stack.extend(x)
    dirs=[]
    for a in soup.find_all('a',href=True):
        href=a['href']; text=' '.join(a.stripped_strings)
        if 'الاتجاهات' in text or 'Directions' in text or 'maps.app.goo.gl' in href or 'google.com/maps' in href or 'maps.google.com' in href: dirs.append(href)
        if href.startswith('/'): all_internal.add(href.split('#')[0])
    rep['directions'][r]=dirs
    for href in dirs:
        if href!=MAP: errors.append(f'{r} non-authoritative directions {href}')
    for iframe in soup.find_all('iframe',src=True):
        if 'maps' in iframe['src'].lower(): errors.append(f'{r} interactive map iframe remains')
    for img in soup.find_all('img',src=True):
        u=urljoin(BASE+r,img['src']); ir=S.get(u,timeout=15)
        if ir.status_code>=400: rep['broken_images'].append((r,u,ir.status_code)); errors.append(f'broken image {u}')
    rep['routes'][r]={'status':resp.status_code,'canonical':can.get('href') if can else None,'title':title,'description':meta.get('content') if meta else None,'h1':len(soup.find_all('h1'))}
geo=rep['schema_geo'].get('/')
if geo!={'latitude':32.056335,'longitude':35.871691}: errors.append(f'homepage geo mismatch {geo}')
expected_hours=[
 {'@type':'OpeningHoursSpecification','dayOfWeek':['Saturday','Sunday'],'opens':'16:30','closes':'20:30'},
 {'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday'],'opens':'08:00','closes':'13:30'},
 {'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday'],'opens':'16:30','closes':'20:30'}]
if rep['hours']!=expected_hours: errors.append(f'opening hours changed {rep["hours"]}')
for href in sorted(all_internal):
    if href.startswith('//'): continue
    rr=S.get(BASE+href,allow_redirects=True,timeout=25)
    if rr.status_code>=400: rep['broken_links'].append((href,rr.status_code)); errors.append(f'broken internal {href}')
sm=S.get(BASE+'/sitemap.xml',timeout=25); urls=re.findall(r'<loc>(.*?)</loc>',sm.text)
expected=[BASE+('/' if r=='/' else r) for r in ROUTES]
rep['sitemap_count']=len(urls); rep['sitemap_urls']=urls
if len(urls)!=11 or set(urls)!=set(expected): errors.append('sitemap not exact 11 canonical URLs')
rob=S.get(BASE+'/robots.txt',timeout=25).text; rep['robots']=rob
if rob!='User-agent: *\nAllow: /\n\nSitemap: https://osaraclinics.com/sitemap.xml\n': errors.append('robots changed')
for r in ROUTES[1:]:
    a=S.get(BASE+r+'.html',allow_redirects=False,timeout=25); b=S.get(BASE+r+'/',allow_redirects=False,timeout=25)
    rep['variants'][r]={'html':[a.status_code,a.headers.get('location')],'slash':[b.status_code,b.headers.get('location')]}
    if a.status_code!=200 or a.headers.get('location') is not None: errors.append(f'.html behavior changed {r}')
    if b.status_code!=301 or b.headers.get('location')!=r: errors.append(f'trailing slash behavior changed {r}')
w=S.get('https://www.osaraclinics.com/',allow_redirects=False,timeout=25); rep['www']=[w.status_code,w.headers.get('location')]
if w.status_code!=301 or w.headers.get('location')!='https://osaraclinics.com/': errors.append('www redirect changed')
rep['errors']=errors
open('pr5-static.json','w',encoding='utf-8').write(json.dumps(rep,ensure_ascii=False,indent=2)); print(json.dumps(rep,ensure_ascii=False,indent=2)); raise SystemExit(1 if errors else 0)
