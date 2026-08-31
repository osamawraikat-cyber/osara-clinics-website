import json,re,sys,time
from urllib.parse import urljoin,urlparse
import requests
from bs4 import BeautifulSoup
BASE='https://osaraclinics.com'
ROUTES=['/','/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment','/vitiligo-jordan','/mole-removal','/school-health','/botox-hyperhidrosis']
AFFECTED=['/dermatology','/ophthalmology','/doctors/dr-osama-alwreikat','/doctors/dr-sara-abu-touq','/psoriasis-treatment','/acne-scar-treatment']
EXPECTED={r:'https://osaraclinics.com'+r for r in ROUTES}; EXPECTED['/']='https://osaraclinics.com/'
MID='G-72BY7LC2V2'; s=requests.Session(); s.headers['User-Agent']='OSara-PR4-production-validator/1.0'; errors=[]; report={'routes':{},'broken_links':[],'broken_images':[],'narration_hits':{}}
def get(url,redirects=True):
  last=None
  for i in range(4):
    try:return s.get(url,allow_redirects=redirects,timeout=20)
    except requests.RequestException as e:last=e;time.sleep(1.5*(i+1))
  raise last
def meta(soup,name=None,prop=None):
  el=soup.find('meta',attrs={'name':name}) if name else soup.find('meta',attrs={'property':prop}); return el.get('content') if el else None
for r in ROUTES:
  rr=get(BASE+r); soup=BeautifulSoup(rr.text,'html.parser'); can=(soup.find('link',rel='canonical') or {}).get('href') if soup.find('link',rel='canonical') else None
  if rr.status_code!=200: errors.append(f'{r} status {rr.status_code}')
  if can!=EXPECTED[r]: errors.append(f'{r} canonical {can}')
  if not soup.title or not soup.title.get_text(strip=True): errors.append(f'{r} missing title')
  if not meta(soup,name='description'): errors.append(f'{r} missing description')
  if len(soup.find_all('h1'))!=1: errors.append(f'{r} H1 count {len(soup.find_all("h1"))}')
  for raw in [(x.string or x.get_text()).strip() for x in soup.find_all('script',type='application/ld+json')]:
    try: json.loads(raw)
    except Exception as e: errors.append(f'{r} JSON-LD invalid {e}')
  loaders=[x.get('src','') for x in soup.find_all('script',src=True) if 'googletagmanager.com/gtag/js' in x.get('src','')]
  if loaders!=[f'https://www.googletagmanager.com/gtag/js?id={MID}']: errors.append(f'{r} GA loader')
  inline='\n'.join((x.string or x.get_text()) for x in soup.find_all('script') if not x.get('src'))
  if len(re.findall(r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]G-72BY7LC2V2['\"]",inline))!=1: errors.append(f'{r} GA config')
  report['routes'][r]={'status':rr.status_code,'canonical':can,'title':soup.title.get_text(strip=True) if soup.title else None,'description':meta(soup,name='description')}
patterns=[r'تربط هذه الصفحة',r'تعمل صفحة',r'بنية عيادات',r'هذه البوابة لا تكرر',r'الموقع الحالي يذكر',r'this page links',r'this page is part of',r'site structure',r'entity relationship',r'internal link',r'SEO']
for r in AFFECTED:
  text=BeautifulSoup(get(BASE+r).text,'html.parser').get_text(' ',strip=True); hits=[p for p in patterns if re.search(p,text,re.I)]; report['narration_hits'][r]=hits
  if hits: errors.append(f'{r} narration {hits}')
seen=set(); imgs=set()
for r in ROUTES:
  soup=BeautifulSoup(get(BASE+r).text,'html.parser')
  for a in soup.find_all('a',href=True):
    h=a['href']
    if h.startswith(('#','tel:','mailto:','javascript:','https://wa.me','https://www.google.com','https://maps.app.goo.gl','https://goo.gl/maps')): continue
    u=urljoin(BASE+r,h); pu=urlparse(u)
    if pu.netloc not in ('osaraclinics.com','www.osaraclinics.com'): continue
    path=pu.path or '/'
    if path in seen: continue
    seen.add(path); x=get(BASE+path)
    if x.status_code>=400: errors.append(f'broken internal {path} {x.status_code}'); report['broken_links'].append([path,x.status_code])
  for im in soup.find_all('img',src=True):
    u=urljoin(BASE+r,im['src']); pu=urlparse(u)
    if pu.netloc!='osaraclinics.com' or pu.path in imgs: continue
    imgs.add(pu.path); x=get(u)
    if x.status_code>=400: errors.append(f'broken image {pu.path} {x.status_code}'); report['broken_images'].append([pu.path,x.status_code])
rob=get(BASE+'/robots.txt'); sm=get(BASE+'/sitemap.xml'); locs=re.findall(r'<loc>(.*?)</loc>',sm.text)
if rob.status_code!=200 or 'Sitemap: https://osaraclinics.com/sitemap.xml' not in rob.text: errors.append('robots')
if sm.status_code!=200 or len(locs)!=11 or set(locs)!=set(EXPECTED.values()): errors.append(f'sitemap {len(locs)}')
report['sitemap_count']=len(locs)
www=get('https://www.osaraclinics.com/',False)
if www.status_code not in (301,302,307,308) or urlparse(www.headers.get('location','')).netloc!='osaraclinics.com': errors.append('www normalization')
for r in ROUTES[1:]:
  for suffix in ['.html','/']:
    x=get(BASE+r+suffix,False); report.setdefault('variants',{})[r+suffix]={'status':x.status_code,'location':x.headers.get('location')}
report['errors']=errors; open('pr4-prod-static.json','w').write(json.dumps(report,ensure_ascii=False,indent=2)); print(json.dumps(report,ensure_ascii=False,indent=2)); sys.exit(1 if errors else 0)