import json,re,sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
BASE='https://osaraclinics.com'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/vitiligo-jordan','/botox-hyperhidrosis','/mole-removal','/school-health']
expected={p:(BASE+'/' if p=='/' else BASE+p) for p in ROUTES}
errors=[]; report={'routes':[]}
for p in ROUTES:
    r=requests.get(BASE+p,allow_redirects=False,timeout=30)
    soup=BeautifulSoup(r.text,'html.parser')
    c=soup.find('link',rel='canonical')
    canon=c.get('href') if c else None
    report['routes'].append({'path':p,'status':r.status_code,'canonical':canon})
    if r.status_code!=200: errors.append(f'{p} status {r.status_code}')
    if canon!=expected[p]: errors.append(f'{p} canonical {canon!r}')
robots=requests.get(BASE+'/robots.txt',timeout=30)
report['robots']={'status':robots.status_code,'text':robots.text}
if robots.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in robots.text: errors.append('robots')
sm=requests.get(BASE+'/sitemap.xml',timeout=30)
report['sitemap_status']=sm.status_code
soup=BeautifulSoup(sm.text,'xml')
locs=[x.get_text(strip=True) for x in soup.find_all('loc')]
report['sitemap_urls']=locs
expected_locs=[expected[p] for p in ROUTES]
if sm.status_code!=200 or set(locs)!=set(expected_locs) or len(locs)!=9: errors.append('sitemap')
# homepage source schema
home=requests.get(BASE+'/',timeout=30).text
soup=BeautifulSoup(home,'html.parser'); clinic=None
for s in soup.find_all('script',type='application/ld+json'):
    try:x=json.loads(s.get_text())
    except Exception:continue
    if isinstance(x,dict) and x.get('@type')=='MedicalClinic' and x.get('@id')=='https://osaraclinics.com/#clinic': clinic=x
expected_hours=[
 {'@type':'OpeningHoursSpecification','dayOfWeek':['Saturday','Sunday'],'opens':'16:30','closes':'20:30'},
 {'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday'],'opens':'08:00','closes':'13:30'},
 {'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday'],'opens':'16:30','closes':'20:30'}]
report['source_hours']=clinic.get('openingHoursSpecification') if clinic else None
if not clinic or clinic.get('openingHoursSpecification')!=expected_hours: errors.append('source hours')
# physician source image checks
report['physicians']={}
for p in ['/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq']:
    t=requests.get(BASE+p,timeout=30).text; s=BeautifulSoup(t,'html.parser')
    og=bool(s.find('meta',attrs={'property':'og:image'})); imgs=[i.get('src') for i in s.find_all('img')]
    schema_img=False
    for sc in s.find_all('script',type='application/ld+json'):
        try:x=json.loads(sc.get_text())
        except:continue
        if '"image"' in json.dumps(x): schema_img=True
    report['physicians'][p]={'og_image':og,'img_tags':imgs,'schema_image':schema_img}
    if og or imgs or schema_img: errors.append(f'physician image {p}')
# internal links among target routes
broken=[]
for p in ROUTES:
    t=requests.get(BASE+p,timeout=30).text; s=BeautifulSoup(t,'html.parser')
    for a in s.find_all('a',href=True):
        h=a['href']
        if h.startswith('/') and not h.startswith('//'):
            path=h.split('#')[0].split('?')[0] or '/'
            rr=requests.get(BASE+path,allow_redirects=False,timeout=30)
            if rr.status_code>=400: broken.append((p,h,rr.status_code))
report['broken_internal_links']=broken
if broken: errors.append('internal links')
# www redirect
rw=requests.get('https://www.osaraclinics.com/',allow_redirects=True,timeout=30)
report['www']={'final_status':rw.status_code,'final_url':rw.url,'history':[(x.status_code,x.headers.get('location')) for x in rw.history]}
if rw.status_code!=200 or rw.url!='https://osaraclinics.com/' or len(rw.history)==0 or len(rw.history)>3: errors.append('www redirect')
report['errors']=errors
open('production-static-report.json','w').write(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps(report,indent=2,ensure_ascii=False))
sys.exit(1 if errors else 0)
